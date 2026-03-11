"""
get_playlist.py  —  YouTubeプレイリストの曲目一覧を取得する

使い方:
  python get_playlist.py <playlist_url_or_id> [<playlist_url_or_id> ...]

例:
  python get_playlist.py https://www.youtube.com/playlist?list=PLwwX__d11ZExUA06lzRGj2MVR_Jhi-3UH
  python get_playlist.py PLwwX__d11ZExUA06lzRGj2MVR_Jhi-3UH PLwwX__d11ZEwtNypRi7xQV5HdTs1XlJ3v

出力:
  各曲を "No. タイトル | チャンネル | https://youtu.be/<id>" 形式で表示
  最後に bgm_data.json 互換のJSONも出力（tools/bgm_data.json に保存）

OAuth認証:
  token.json が有効なら自動使用。
  無効・期限切れなら自動でブラウザを開いて再認証し、token.json を更新する。
"""

import json
import os
import re
import sys
import urllib.request
from pathlib import Path

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

TOOLS_DIR = Path(__file__).parent
TOKEN_FILE = TOOLS_DIR / "token.json"
CLIENT_SECRET_FILE = TOOLS_DIR / "youtube_client_secret.json"
SCOPES = ["https://www.googleapis.com/auth/youtube.readonly"]


def get_credentials() -> Credentials:
    """有効なOAuth認証情報を返す。必要なら再認証してtoken.jsonを更新する。"""
    creds = None

    if TOKEN_FILE.exists():
        with open(TOKEN_FILE) as f:
            t = json.load(f)
        creds = Credentials(
            token=t.get("token"),
            refresh_token=t.get("refresh_token"),
            token_uri=t.get("token_uri", "https://oauth2.googleapis.com/token"),
            client_id=t.get("client_id"),
            client_secret=t.get("client_secret"),
            scopes=t.get("scopes", SCOPES),
        )

    # 有効・更新可能か試みる
    if creds and creds.refresh_token:
        try:
            creds.refresh(Request())
            _save_token(creds)
            print("[認証] トークンを更新しました。")
            return creds
        except Exception as e:
            print(f"[認証] トークン更新失敗: {e}")
            print("[認証] ブラウザで再認証します...")

    # 再認証フロー
    if not CLIENT_SECRET_FILE.exists():
        raise FileNotFoundError(
            f"クライアントシークレットファイルが見つかりません: {CLIENT_SECRET_FILE}\n"
            "Google Cloud Console からダウンロードして tools/ に配置してください。"
        )
    flow = InstalledAppFlow.from_client_secrets_file(str(CLIENT_SECRET_FILE), SCOPES)
    creds = flow.run_local_server(port=0, open_browser=True)
    _save_token(creds)
    print("[認証] 認証が完了しました。トークンを保存しました。")
    return creds


def _save_token(creds: Credentials):
    data = {
        "token": creds.token,
        "refresh_token": creds.refresh_token,
        "token_uri": creds.token_uri,
        "client_id": creds.client_id,
        "client_secret": creds.client_secret,
        "scopes": list(creds.scopes) if creds.scopes else SCOPES,
        "universe_domain": "googleapis.com",
        "account": "",
        "expiry": creds.expiry.isoformat() if creds.expiry else None,
    }
    with open(TOKEN_FILE, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def extract_playlist_id(arg: str) -> str:
    """URLまたはIDからプレイリストIDを取り出す。"""
    m = re.search(r"list=([A-Za-z0-9_-]+)", arg)
    if m:
        return m.group(1)
    # プレーンIDとして扱う
    return arg.strip()


def fetch_playlist(playlist_id: str, access_token: str) -> list[dict]:
    """プレイリストの全アイテムを取得する。"""
    items = []
    page_token = ""
    while True:
        url = (
            "https://www.googleapis.com/youtube/v3/playlistItems"
            "?part=snippet&maxResults=50"
            f"&playlistId={playlist_id}"
            + (f"&pageToken={page_token}" if page_token else "")
        )
        req = urllib.request.Request(
            url, headers={"Authorization": f"Bearer {access_token}"}
        )
        with urllib.request.urlopen(req) as r:
            data = json.loads(r.read())

        for item in data.get("items", []):
            s = item["snippet"]
            vid = s["resourceId"]["videoId"]
            items.append(
                {
                    "no": len(items) + 1,
                    "title": s["title"],
                    "channel": s.get("videoOwnerChannelTitle", "(private)"),
                    "video_id": vid,
                    "video_url": f"https://www.youtube.com/watch?v={vid}",
                }
            )
        page_token = data.get("nextPageToken", "")
        if not page_token:
            break
    return items


def print_playlist(playlist_id: str, items: list[dict]):
    print(f"\n=== プレイリスト: {playlist_id} ({len(items)}曲) ===")
    for x in items:
        print(f"  {x['no']}. {x['title']}")
        print(f"      チャンネル : {x['channel']}")
        print(f"      URL       : https://youtu.be/{x['video_id']}")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    playlist_ids = [extract_playlist_id(a) for a in sys.argv[1:]]

    creds = get_credentials()
    access_token = creds.token

    all_items = {}
    for pid in playlist_ids:
        print(f"\nプレイリスト取得中: {pid} ...")
        items = fetch_playlist(pid, access_token)
        all_items[pid] = items
        print_playlist(pid, items)

    # bgm_data.json を最初のプレイリストの内容で更新（複数指定時は最初のもの）
    first_pid = playlist_ids[0]
    out_path = TOOLS_DIR / "bgm_data.json"
    # 複数の場合は全プレイリストを結合
    combined = []
    for pid, items in all_items.items():
        for item in items:
            combined.append({**item, "playlist_id": pid})
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(combined, f, ensure_ascii=False, indent=2)
    print(f"\n✅ bgm_data.json に {len(combined)} 件を保存しました: {out_path}")

    # Copilot向けサマリーをTSV形式でも表示
    print("\n--- Copilot/テキスト用サマリー ---")
    for pid, items in all_items.items():
        print(f"\n【{pid}】")
        for x in items:
            print(f"{x['no']}\t{x['title']}\t{x['channel']}\thttps://youtu.be/{x['video_id']}")


if __name__ == "__main__":
    main()
