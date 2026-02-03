"""
YouTube再生リスト情報取得スクリプト
OAuth 2.0を使用して、非公開/限定公開の再生リストからBGM情報を取得します。
"""

import os
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# YouTube Data API v3のスコープ
SCOPES = ['https://www.googleapis.com/auth/youtube.readonly']

def get_authenticated_service():
    """
    OAuth 2.0認証を行い、YouTube API サービスを返す
    """
    creds = None
    script_dir = os.path.dirname(os.path.abspath(__file__))
    token_path = os.path.join(script_dir, 'token.json')
    client_secret_path = os.path.join(script_dir, 'youtube_client_secret.json')
    
    # トークンファイルがあれば読み込む
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    
    # 有効な認証情報がない場合は認証フローを実行
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                client_secret_path, SCOPES)
            creds = flow.run_local_server(port=0)
        
        # トークンを保存
        with open(token_path, 'w') as token:
            token.write(creds.to_json())
    
    return build('youtube', 'v3', credentials=creds)

def get_playlist_items(youtube, playlist_id):
    """
    再生リストの動画情報を取得
    """
    items = []
    request = youtube.playlistItems().list(
        part='snippet,contentDetails',
        playlistId=playlist_id,
        maxResults=50
    )
    
    while request:
        response = request.execute()
        items.extend(response['items'])
        request = youtube.playlistItems().list_next(request, response)
    
    return items

def get_video_details(youtube, video_ids):
    """
    動画の詳細情報を取得（複数の動画を一度に取得）
    """
    request = youtube.videos().list(
        part='snippet,contentDetails',
        id=','.join(video_ids)
    )
    response = request.execute()
    return response['items']

def format_bgm_data(playlist_items, video_details):
    """
    取得したデータをBGMテーブル用に整形
    """
    bgm_list = []
    video_details_dict = {item['id']: item for item in video_details}
    
    for idx, item in enumerate(playlist_items, 1):
        video_id = item['contentDetails']['videoId']
        video_detail = video_details_dict.get(video_id, {})
        snippet = video_detail.get('snippet', item['snippet'])
        
        bgm_info = {
            'no': idx,
            'title': snippet['title'],
            'channel': snippet['channelTitle'],
            'video_id': video_id,
            'video_url': f'https://www.youtube.com/watch?v={video_id}'
        }
        bgm_list.append(bgm_info)
    
    return bgm_list

def print_bgm_list(bgm_list):
    """
    BGMリストを見やすく表示
    """
    print("\n" + "="*80)
    print("BGMリスト")
    print("="*80)
    
    for bgm in bgm_list:
        print(f"\n{bgm['no']}. {bgm['title']}")
        print(f"   演奏: {bgm['channel']}")
        print(f"   URL: {bgm['video_url']}")
    
    print("\n" + "="*80)

def save_bgm_json(bgm_list, output_file='bgm_data.json'):
    """
    BGMリストをJSONファイルに保存
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, output_file)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(bgm_list, f, ensure_ascii=False, indent=2)
    
    print(f"\nデータを保存しました: {output_path}")

def main():
    """
    メイン処理
    """
    # 再生リストIDを指定
    # URLが https://www.youtube.com/playlist?list=PLwwX__d11ZExUA06lzRGj2MVR_Jhi-3UH の場合
    # 再生リストIDは PLwwX__d11ZExUA06lzRGj2MVR_Jhi-3UH
    playlist_id = input("再生リストID (または URL) を入力してください: ").strip()
    
    # URLから再生リストIDを抽出
    if 'youtube.com' in playlist_id or 'youtu.be' in playlist_id:
        if 'list=' in playlist_id:
            playlist_id = playlist_id.split('list=')[1].split('&')[0]
    
    print(f"\n再生リスト ID: {playlist_id}")
    print("認証を開始します...")
    
    try:
        # YouTube API サービスを取得
        youtube = get_authenticated_service()
        print("認証成功！")
        
        # 再生リストの動画情報を取得
        print("再生リスト情報を取得中...")
        playlist_items = get_playlist_items(youtube, playlist_id)
        
        if not playlist_items:
            print("再生リストが空です。")
            return
        
        # 動画IDのリストを作成
        video_ids = [item['contentDetails']['videoId'] for item in playlist_items]
        
        # 動画の詳細情報を取得
        print("動画詳細情報を取得中...")
        video_details = get_video_details(youtube, video_ids)
        
        # データを整形
        bgm_list = format_bgm_data(playlist_items, video_details)
        
        # 結果を表示
        print_bgm_list(bgm_list)
        
        # JSONファイルに保存
        save_bgm_json(bgm_list)
        
        print("\n✓ 処理が完了しました！")
        
    except Exception as e:
        print(f"\nエラーが発生しました: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
