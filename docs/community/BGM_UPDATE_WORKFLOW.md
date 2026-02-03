# 観音台カフェ BGM 選曲リスト 更新ワークフロー

## 📋 概要

このドキュメントは、観音台カフェの毎月の BGM 選曲リスト (`cafe_bgm_selection.html`) を更新する際の作業手順をまとめたものです。このセッション終了後も、GitHub Copilot が作業を再開する際に参照できるように、詳細な手順と技術情報を記載しています。

## 🎯 作業の目的

- **効率化**: 毎月の更新作業を自動化・効率化する
- **質の向上**: Wikipedia リンクによる教育的価値の提供
- **よいマナー**: YouTube プライベートプレイリストは OAuth 2.0 で正式にアクセス (公開前は非公開で管理)

## 🗂️ ファイル構成

```
kannondai-community/
├── docs/
│   └── community/
│       └── 2025__/
│           └── cafe_bgm_selection.html  # 公開用 BGM リスト (メインファイル)
├── tools/
│   ├── fetch_youtube_playlist.py        # YouTube プレイリスト抽出スクリプト
│   ├── youtube_client_secret.json       # OAuth 2.0 クライアント認証情報 (.gitignore)
│   ├── token.json                       # OAuth トークンキャッシュ (.gitignore)
│   └── bgm_data.json                    # 抽出された BGM データ (一時ファイル)
└── .gitignore                           # 秘密情報除外設定
```

## 🔧 技術スタック

### YouTube Data API v3
- **認証方式**: OAuth 2.0 (Desktop Application Flow)
- **スコープ**: `https://www.googleapis.com/auth/youtube.readonly`
- **クォータ**: 10,000 ユニット/日 (月間使用量: 約 7 ユニット)
- **GCP プロジェクト**: `kannondai-cafe-bgm` (Project ID: 951784409210)

### Python 環境
- **バージョン**: Python 3.13 (Global Environment)
- **必須パッケージ**:
  - `google-auth-oauthlib`
  - `google-auth-httplib2`
  - `google-api-python-client`

### HTML/CSS
- **スタイル**: `docs/styles/bgm-table.css`
- **構造**: セクション単位 (各回ごとに h2 + テーブル)

## 📅 月次更新ワークフロー

### Step 1: YouTube プレイリスト作成
1. YouTube で新規プレイリストを作成 (非公開設定)
2. 5曲程度を選曲してプレイリストに追加
3. プレイリスト URL から ID を取得
   - 形式: `https://www.youtube.com/playlist?list=PLwwX__d11ZExUA06lzRGj2MVR_Jhi-3UH`
   - ID: `PLwwX__d11ZExUA06lzRGj2MVR_Jhi-3UH`

### Step 2: Python スクリプト実行
```powershell
cd c:\Users\takahashi\GitHub\kannondai-community\tools
python fetch_youtube_playlist.py
```

**実行内容**:
1. OAuth 2.0 認証 (初回のみブラウザで承認)
2. プレイリスト情報取得 (曲名、チャンネル名、動画 ID、URL)
3. `bgm_data.json` に出力

**出力例** (`bgm_data.json`):
```json
[
  {
    "title": "HALLELUJAH - guitar inspiration...",
    "channel": "RockMilady",
    "video_id": "NuNRXq2025o",
    "url": "https://www.youtube.com/watch?v=NuNRXq2025o"
  }
]
```

### Step 3: Wikipedia リサーチ
各曲について以下の情報を Wikipedia で調査:

#### 調査項目
1. **曲名の正式表記** (日本語・英語)
2. **作曲者名** (日本語・英語)
3. **作曲者の国籍・職業**
4. **Wikipedia URL** (楽曲ページ・作曲者ページ)

#### リサーチ手法
- **Copilot Agent モード推奨**: 自動で Wikipedia 検索・情報抽出
- **検索クエリ例**:
  - `"曲名 作曲者名 Wikipedia"` (日本語)
  - `"Song Title composer name Wikipedia"` (英語)
- **注意点**:
  - 同名曲に注意 (例: "The Last Waltz" は映画と楽曲が別)
  - 日本語版がない場合は英語版を使用

#### Wikipedia 検索で得られた情報 (2026年3月の例)

| 曲名 | 作曲者 | 国籍 | Wikipedia URL |
|------|--------|------|---------------|
| Hallelujah (ハレルヤ) | Leonard Cohen (レナード・コーエン) | カナダ (シンガーソングライター・詩人) | [楽曲](https://ja.wikipedia.org/wiki/ハレルヤ_(レナード・コーエンの曲)) / [作曲者](https://ja.wikipedia.org/wiki/レナード・コーエン) |
| Despacito (デスパシート) | Luis Fonsi (ルイス・フォンシ) & Erika Ender (エリカ・エンダー) | プエルトリコ (米国市民権) / パナマ | [楽曲](https://ja.wikipedia.org/wiki/デスパシート) / [作曲者](https://ja.wikipedia.org/wiki/ルイス・フォンシ) |
| The Last Waltz (ラスト・ワルツ) | Barry Mason (バリー・メイソン) & Les Reed (レス・リード) | イギリス (Engelbert Humperdinck 歌唱) | [楽曲 (英語)](https://en.wikipedia.org/wiki/The_Last_Waltz_(song)) |
| Sweet Memories (スウィート・メモリーズ) | 大村雅朗 (Masaaki Omura) | 日本 (松田聖子の楽曲) | [楽曲](https://ja.wikipedia.org/wiki/ガラスの林檎/SWEET_MEMORIES) |
| 北の国から〜遥かなる大地より〜 | さだまさし (Masashi Sada) | 日本 (テレビドラマ主題歌) | [ドラマ・楽曲](https://ja.wikipedia.org/wiki/北の国から) / [作曲者](https://ja.wikipedia.org/wiki/さだまさし) |

### Step 4: HTML セクション生成
`cafe_bgm_selection.html` に新しいセクションを追加。

#### HTML 構造テンプレート
```html
<section id="cafe-20260301">
    <h2>🗓️ 2026年3月1日 (日) 第９回 観音台カフェ 🍵 予定</h2>
    <p>
        (イベント説明文)
    </p>
    <table>
        <thead>
            <tr>
                <th>No</th>
                <th>曲名🔗</th>
                <th>作曲🔗</th>
                <th>演奏🔗</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>1</td>
                <td><a href="https://ja.wikipedia.org/wiki/ハレルヤ_(レナード・コーエンの曲)" target="_blank">ハレルヤ</a></td>
                <td><a href="https://ja.wikipedia.org/wiki/レナード・コーエン" target="_blank">レナード・コーエン</a></td>
                <td><a href="https://www.youtube.com/watch?v=NuNRXq2025o" target="_blank">RockMilady</a></td>
            </tr>
            <!-- 他の曲も同様 -->
        </tbody>
    </table>
</section>
```

#### 挿入位置
- **新しいイベント= 最上部に挿入** (時系列順: 新→古)
- 最新のイベントが常にページトップに表示される

### Step 5: Git コミット
```powershell
cd c:\Users\takahashi\GitHub\kannondai-community
git add docs/community/2025__/cafe_bgm_selection.html
git commit -m "Add BGM selection for March 2026 (Event #9)"
git push origin main
```

## 🔐 OAuth 2.0 セットアップ (初回のみ)

### 1. Google Cloud Console 設定
1. [Google Cloud Console](https://console.cloud.google.com/) にログイン
2. プロジェクト `kannondai-cafe-bgm` を選択
3. **API とサービス > ライブラリ** から `YouTube Data API v3` を有効化
4. **API とサービス > 認証情報** から OAuth 2.0 クライアント ID を作成
   - アプリケーションの種類: **デスクトップ アプリ**
   - クライアント ID とシークレットをダウンロード
5. ダウンロードした JSON を `tools/youtube_client_secret.json` として保存

### 2. Python 実行 (初回のみ)
```powershell
python fetch_youtube_playlist.py
```
- ブラウザが開き、Google アカウントでの承認を求められる
- 承認後、`token.json` が自動生成される (次回以降は自動認証)

### 3. .gitignore 設定
```
# YouTube API credentials
tools/youtube_client_secret.json
tools/token.json
tools/bgm_data.json
```

## 🛠️ トラブルシューティング

### OAuth エラー
- **問題**: `invalid_grant` エラー
- **原因**: トークンの有効期限切れ
- **解決**: `token.json` を削除して再認証

### Wikipedia リサーチの注意点
- **同名曲対策**: 作曲者名を含めた検索クエリを使用
- **日本語記事がない場合**: 英語版 Wikipedia を使用 (例: The Last Waltz)
- **ドラマ/映画記事**: 主題歌情報が含まれていれば利用可 (例: 北の国から)

### クォータ超過
- **月間使用量**: 約 7 ユニット (10,000 ユニットまで余裕あり)
- **超過時**: 翌日まで待機 (太平洋時間 午前0時にリセット)

## 📚 参考情報

### HTML テーブル構造
- **No**: 連番 (1, 2, 3, ...)
- **曲名🔗**: Wikipedia 楽曲ページへのリンク
- **作曲🔗**: Wikipedia 作曲者ページへのリンク
- **演奏🔗**: YouTube 動画へのリンク (チャンネル名を表示)

### CSS スタイル
- ファイル: `docs/styles/bgm-table.css`
- 表の幅、色、ホバーエフェクトなどを定義

## 🎓 教育的価値

### Wikipedia リンクの意義
- 音楽文化の理解促進
- 作曲者の背景・時代背景の学習
- 国際的な音楽の多様性を認識

### 作曲者の国籍例 (2026年3月)
- カナダ: Leonard Cohen
- プエルトリコ/パナマ: Luis Fonsi & Erika Ender
- イギリス: Barry Mason & Les Reed
- 日本: 大村雅朗、さだまさし

## 📝 Copilot 向けメモ

### このセッション再開時の手順
1. このファイル (`BGM_UPDATE_WORKFLOW.md`) を読む
2. `bgm_data.json` が存在するか確認
3. Wikipedia リサーチが必要な場合は Agent モードで自動実行
4. HTML 生成前にユーザーに確認を求める

### よくあるリクエスト
- "来月の BGM リストを作りたい" → このワークフローの Step 2 から開始
- "Wikipedia リンクを追加したい" → Step 3 のリサーチを実行
- "HTML が崩れている" → `bgm-table.css` を確認

## 📅 更新履歴

| 日付 | イベント回数 | 備考 |
|------|------------|------|
| 2026-02-03 | 第9回 (2026年3月) | このワークフローを初作成 |
| (今後追記) | | |

---

**作成者**: takahashi  
**作成日**: 2026年2月3日  
**最終更新**: 2026年2月3日
