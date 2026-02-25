# GitHub Organization 移行計画

**記録日**: 2026-02-25  
**関連**: `ai_agent_community_governance.md` Section「GitHub Organization 構造（案A）」  
**現状**: `github.com/kannondai` org は取得済み（2026-02-20）

---

## 現状の問題点

現在の `kannondai-community` リポジトリは**公開リポジトリ**であるにもかかわらず、以下の機密性の高い内容が混在している：

| 種別 | 具体例 | 問題 |
|---|---|---|
| 個人名を含む分析 | `kanaya_deep_analysis.md`、`survey_details_班*.md` | 実名が公開状態 |
| 個人宛の文書 | `chairman_letter_20260225.md`、`2026_chairman_communications.md` | 個人間の連絡が公開状態 |
| 内部戦略文書 | `annual_report_challenge3_defense_strategies.md`、`annual_report_legality.md` | 内部の意思決定過程が公開状態 |
| 内部会議記録 | `board_meeting_4th.md`、`meeting_agenda_20260222.md` | 役員会の内部議論が公開状態 |
| 個人の依頼・相談記録 | `2026_nakayama_consultation_20260225.md` | 個人名と内情が公開状態 |

> **注記**: GitHub Pages は `.md` ファイルを Jekyll なしでも raw text として配信する。  
> URLを知れば誰でも参照できる状態にある。

---

## 設計：リポジトリの分離（改訂版 2026-02-25）

### 命名規則の考え方

`jichikai-1` / `jichikai-2` の数字は **第一自治会 / 第二自治会** の番号。  
公開 / 非公開は `-pub` / `-priv` の postfix で識別する。

| リポジトリ名 | 公開設定 | 役割 |
|---|---|---|
| `kannondai/kannondai-community` | **Public** | 観音台地域の共通公開サイト（HTML） |
| `kannondai/jichikai-2-pub` | **Public** | 第二自治会の住民向け公開情報・発行物 |
| `kannondai/jichikai-2-priv` | **Private** | 第二自治会の内部文書・個人情報含む考察 |

> 将来、第一自治会（山岡さん）と連携する場合は `jichikai-1-pub` / `jichikai-1-priv` で対応する。

---

### `kannondai/kannondai-community`（Public）

**役割**: 観音台地域全体の公開サイト

```
kannondai-community/
├── docs/
│   ├── index.html
│   ├── top.html
│   ├── about_this_site.html
│   ├── climate-change/
│   ├── environment/
│   ├── philosophy/         ← 個人名・内部情報を含まないもののみ
│   ├── styles/
│   ├── scripts/
│   └── images/
├── README.md
└── LICENSE
```

`docs/philosophy/` の扱い：個人名・内部情報を含まないもの。  
（公開可：`ai_agent_community_governance.md`、`community_ethics_ai_framework.md` 等）  
（要精査：`privacy_misconceptions.md` 等）

---

### `kannondai/jichikai-2-pub`（Public）

**役割**: 第二自治会として住民・外部に公開する情報

```
jichikai-2-pub/
├── docs/
│   ├── annual_report/      ← 年報案の最終版（発行後に配置）
│   └── hall-reserve.html   ← 集会所予約（将来）
└── README.md
```

当面はほぼ空でよい。年報案の最終版を発行後にここに置く運用を想定。

---

### `kannondai/jichikai-2-priv`（Private）

**役割**: 第二自治会の内部業務・作業文書・AI作業コンテキスト

```
jichikai-2-priv/
├── COPILOT-INIT.md
├── AI_CONTEXT_STANDARD.md
├── PROJECT_STATUS.md
├── APPLY_CONTEXT.md
├── HOWTO_FEEDBACK.md
├── community/              ← 現 docs/community/ の全内容
│   ├── 2026__/
│   ├── officer_system_discussion.md
│   └── ...
├── tools/
├── design/
└── scripts/
```

---

## 境界の原則

| 公開（`kannondai-community` / `jichikai-2-pub`）| 非公開（`jichikai-2-priv`） |
|---|---|
| 住民向けに公開する情報 | 役員の内部議論・戦略 |
| 個人名を含まない考察 | 個人名・個人の発言・行動の記録 |
| 発行後の年報最終版 | 年報の草稿・作業過程 |
| 汎用的な仕組み・哲学 | 特定の人物・事案への対応記録 |
| 自治会会則・公式資料 | アンケートの個別分析 |
| 集会所予約など公開サービス | 会計・財務の作業データ |

---

## 移行手順（早期実施）

### Step 1：`jichikai-2-priv` プライベートリポジトリを作成（ブラウザ）
```
github.com/kannondai → New repository
名前: jichikai-2-priv
公開設定: Private
初期化: README なし（空のまま）
```

### Step 2：現在のリポジトリを `jichikai-2-priv` として push（ターミナル）
```powershell
cd E:\GitHub\kannondai-community
git add -A
git commit -m "2026-02-25 本日作業分をコミット"
git remote add jichikai-2-priv https://github.com/kannondai/jichikai-2-priv.git
git push jichikai-2-priv main
```

### Step 3：`kannondai-community` を org に Transfer（ブラウザ）
```
freesemt/kannondai-community → Settings → Danger Zone → Transfer ownership
転送先: kannondai org
```

### Step 4：内部文書を `kannondai-community` から削除（ターミナル）
```powershell
# Step 2 で jichikai-2-priv への push が完了してから実施
git rm -r docs/community/
git rm COPILOT-INIT.md AI_CONTEXT_STANDARD.md PROJECT_STATUS.md APPLY_CONTEXT.md HOWTO_FEEDBACK.md
git rm -r tools/ design/ scripts/
git commit -m "Remove internal documents (moved to jichikai-2-priv)"
git push
```

### Step 5：`jichikai-2-pub` パブリックリポジトリを作成（ブラウザ）
```
github.com/kannondai → New repository
名前: jichikai-2-pub
公開設定: Public
```
当面は空。年報案発行後に最終版を配置。

### Step 6：ローカルの作業ディレクトリを新設
```powershell
cd E:\GitHub
git clone https://github.com/kannondai/jichikai-2-priv.git
# 以後の内部作業は E:\GitHub\jichikai-2-priv\ で行う
```

### Step 7：GitHub Pages の確認
`kannondai-community` の Pages 設定が org 移管後も正常動作するか確認。

---

## COPILOT-INIT.md の更新

移行後、`jichikai-2-priv` の `COPILOT-INIT.md` のパス参照を  
`E:\GitHub\jichikai-2-priv\` に更新する。

---

## スケジュール

| 時期 | 作業 |
|---|---|
| 本日（2/25） | Step 1〜4 を実施 |
| 本日〜2/28 | Step 5〜7 を実施 |
| 3/2 印刷発注後 | `jichikai-2-pub` に年報案最終版を配置 |

---

## リスクと注意点

- **Step 4 は Step 2 完了後に実施**：バックアップ確保が先
- **GitHub Pages の URL 変化**：`freesemt.github.io/kannondai-community/` → `kannondai.github.io/kannondai-community/` に変わる可能性。sitemap.xml・robots.txt の更新が必要
- **COPILOT-INIT の参照パス**：`E:\GitHub\jichikai-2-priv\` に更新が必要
