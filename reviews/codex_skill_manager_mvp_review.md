# Codex Skill Manager MVP Review

## 結論

- 判定: **Conditional Pass**
- 主な理由:
  - 主要コマンド（scan/analyze/report/recommend/generate）は実装済みで、ローカル実行でも概ね動作する。
  - 一方で、`generate`の`--force`が既存ディレクトリを`rmtree`で丸ごと削除するため、安全性仕様（不用意な既存ファイル削除回避）に抵触する。
  - `report.py`のMarkdown出力はHTMLエスケープ未実施で、悪意文字列を含む場合に表示崩れ/XSS媒介リスクがある。
  - parser/classifierの日本語見出し対応・表記ゆれ耐性が限定的で、期待仕様に対して不足がある。

## 重大な問題

| 優先度 | 対象 | 問題 | 影響 | 修正案 |
|---|---|---|---|---|
| High | `src/skill_manager/generator.py` | `--force`時に`shutil.rmtree(target)`で対象ディレクトリを全削除してから再生成 | 意図しないファイル消失。既存のexamples/templates以外も削除される | `--force`は`SKILL.md`と管理対象サブディレクトリの更新に限定し、削除は明示オプション（例: `--purge`）に分離 |
| High | `src/skill_manager/report.py` | Markdownレポートのテーブル/箇条書きが未エスケープ | 表示崩れ・Markdownレンダラ依存で危険なHTMLが混入する可能性 | Markdown向けに`|`改行・HTMLタグをエスケープするユーティリティを追加 |

## 中程度の問題

| 優先度 | 対象 | 問題 | 影響 | 修正案 |
|---|---|---|---|---|
| Medium | `src/skill_manager/parser.py` | 見出し別名が英語中心（`When to use`等）で日本語見出し判定が不足 | 日本語SKILL.mdで品質スコアが不当に低下 | `SECTION_ALIASES`に日本語同義語（例: `使いどころ`, `入力`, `出力`, `手順`, `注意`, `トラブルシューティング`）を追加 |
| Medium | `src/skill_manager/parser.py` | `summary`抽出長の上限がない | 異常に長い1行で可読性低下・レポート肥大化 | 例: 200〜300文字で切る（末尾`…`） |
| Medium | `src/skill_manager/scanner.py` | 隠しフォルダの除外ポリシーなし | `.git`等をスキル候補として誤認する可能性 | `child.name.startswith('.')`を除外（オプション化も可） |
| Medium | `src/skill_manager/cli.py` | 出力先が常に`output/`固定でCLIオプションなし | CIや任意ディレクトリ運用時に不便 | `--output-dir`を全コマンド共通オプションとして追加 |

## 軽微な問題

| 対象 | 問題 | 修正案 |
|---|---|---|
| `src/skill_manager/parser.py` | `try: import yaml except Exception`が広すぎる | `ImportError`限定にする |
| `src/skill_manager/classifier.py` | `PR`誤判定回避のための`" pr "`は文脈次第で取りこぼしあり | 単語境界regexで`pr`を厳密判定し、英語以外は個別ルール化 |
| `README.md` | `pip install -e .`前提だがオフライン環境で失敗し得る説明なし | `python -m src.skill_manager.cli`の代替実行を追記 |

## 仕様充足チェック

| 項目 | 判定 | コメント |
|---|---|---|
| scan | OK | `output/skills_inventory.json`生成を確認 |
| analyze | OK | 解析・分類・品質診断後に`skills_analysis.json`生成 |
| report md | OK | `skills_report.md`生成 |
| report html | OK | `skills_report.html`生成 |
| recommend | OK | 理由付きJSON提案を出力 |
| generate | 条件付きOK | 非`--force`の安全失敗はOK、`--force`が破壊的 |
| README | 条件付きOK | 基本項目あり。実環境制約（オフライン）記述不足 |
| 安全性 | NG | `--force`削除設計とMarkdown未エスケープが問題 |

## 実行確認結果

- `pip install -e .` は実行したが、ネットワーク制約下でbuild dependency取得に失敗。
- 代替として `python -m src.skill_manager.cli` で全コマンドを実行し、主要機能を確認。
- `generate`は既存名で2回目に安全に失敗し、`--force`で再生成される挙動を確認。

## 修正パッチ案

最小差分の方向性:

1. `generator.py`
   - `--force`時に`rmtree`しない。
   - 既存`SKILL.md`の上書きのみ許可、`examples/`と`templates/`は`mkdir(exist_ok=True)`。
   - 既存ファイル削除を伴う動作は新オプション化（必要時のみ）。

2. `report.py`
   - Markdown出力向け`escape_md_cell()`を追加し、`|`, 改行, `<`, `>`を無害化。

3. `parser.py`
   - `SECTION_ALIASES`に日本語同義語を追加。
   - summaryは上限文字数を設定。

4. `cli.py`
   - `--output-dir`を導入し、既定値`output`。

## 追加で入れるとよいテスト

- `generator`:
  - `--force`で既存の非管理ファイル（例: `notes.txt`）が残ること。
  - `../danger`等の入力が拒否されること。
- `report`:
  - スキル名に`<script>`や`|`が入るケースでMarkdown/HTMLが壊れないこと。
- `parser`:
  - 日本語見出し (`## 手順`, `## 注意点`) が検出されること。
  - コードブロック内`#`を見出し誤認しないこと。
- `scanner`:
  - 隠しディレクトリを除外すること。
  - root直下の通常ファイルを候補にしないこと。

## 次にCodexへ戻すべき指示

```text
Codex Skill Manager MVPの最小修正を行ってください。大規模リファクタリングは禁止です。

必須修正（高優先）:
1) generator.py
- --force時にshutil.rmtreeで対象ディレクトリを丸ごと削除しないでください。
- 既存ディレクトリがある場合:
  - 通常: これまで通り安全に失敗
  - --force: SKILL.mdの上書き + examples/templatesの存在保証のみ（非管理ファイルは消さない）

2) report.py
- Markdownレポート生成時にセル値をエスケープしてください。
- 少なくとも `|`, 改行, `<`, `>` を無害化し、テーブル崩壊と注入リスクを防いでください。

中優先修正:
3) parser.py
- 日本語見出しの別名を追加してください（使いどころ/入力/出力/手順/注意/トラブルシューティング など）。
- summary抽出に最大文字数を設定してください（例: 240文字）。

4) cli.py
- --output-dirオプションを追加し、既定値はoutput。
- scan/analyze/reportで同オプションを使用できるようにしてください。

テスト追加:
- 上記4修正に対する単体テストを最小追加してください。
- 既存テストを壊さず、`pytest`で通る状態にしてください。
```
