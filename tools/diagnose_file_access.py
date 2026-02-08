#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ファイルアクセス診断スクリプト
グローバルPython環境でのファイル操作の問題を特定する
"""
import sys
import os
import time

print("=" * 60, flush=True)
print("ファイルアクセス診断開始", flush=True)
print("=" * 60, flush=True)

# 環境情報
print("\n[1] Python環境情報", flush=True)
print(f"実行ファイル: {sys.executable}", flush=True)
print(f"Pythonバージョン: {sys.version}", flush=True)
print(f"カレントディレクトリ: {os.getcwd()}", flush=True)

# ファイル情報
file_path = r'e:\GitHub\kannondai-community\docs\community\2026__\annual_report_philosophy.md'
print(f"\n[2] 対象ファイル情報", flush=True)
print(f"パス: {file_path}", flush=True)
print(f"存在確認: {os.path.exists(file_path)}", flush=True)

if os.path.exists(file_path):
    file_stat = os.stat(file_path)
    print(f"ファイルサイズ: {file_stat.st_size} bytes", flush=True)
    print(f"最終更新時刻: {time.ctime(file_stat.st_mtime)}", flush=True)

# 読み込みテスト
print("\n[3] 読み込みテスト", flush=True)
try:
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    print(f"✓ 読み込み成功: {len(lines)}行", flush=True)
    print(f"  最初の行: {lines[0].strip()}", flush=True)
    print(f"  最後の行: {lines[-1].strip()}", flush=True)
except Exception as e:
    print(f"✗ 読み込みエラー: {type(e).__name__}: {e}", flush=True)
    sys.exit(1)

# 書き込みテスト（テストファイル）
test_file = r'e:\GitHub\kannondai-community\tools\test_write.txt'
print(f"\n[4] 書き込みテスト（テストファイル）", flush=True)
print(f"テストファイル: {test_file}", flush=True)
try:
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write("書き込みテスト\n")
    print(f"✓ 書き込み成功", flush=True)
    
    # テストファイル削除
    os.remove(test_file)
    print(f"✓ テストファイル削除成功", flush=True)
except Exception as e:
    print(f"✗ 書き込みエラー: {type(e).__name__}: {e}", flush=True)
    sys.exit(1)

# 対象ファイルへの書き込みアクセステスト
print(f"\n[5] 対象ファイルへの書き込みアクセステスト", flush=True)
try:
    # 読み込みモードで開いて即座に閉じる（ロック確認）
    with open(file_path, 'r', encoding='utf-8') as f:
        pass
    print(f"✓ 読み込みアクセス: OK", flush=True)
    
    # 書き込みモードで開いてみる（実際には書き込まない）
    with open(file_path, 'r+', encoding='utf-8') as f:
        pass
    print(f"✓ 書き込みアクセス（r+モード）: OK", flush=True)
    
except PermissionError as e:
    print(f"✗ アクセス拒否: {e}", flush=True)
    print(f"  原因: 他のプロセス（VS Code等）がファイルを開いている可能性", flush=True)
    sys.exit(1)
except Exception as e:
    print(f"✗ 予期しないエラー: {type(e).__name__}: {e}", flush=True)
    sys.exit(1)

# 実際の削除処理シミュレーション（実行しない）
print(f"\n[6] 削除処理シミュレーション", flush=True)
lines_to_keep = lines[:175]
print(f"現在の行数: {len(lines)}", flush=True)
print(f"保持する行数: {len(lines_to_keep)}", flush=True)
print(f"削除予定行数: {len(lines) - len(lines_to_keep)}", flush=True)

print("\n" + "=" * 60, flush=True)
print("診断完了: すべてのチェックに合格しました", flush=True)
print("実際の削除を実行するには trim_philosophy.py を実行してください", flush=True)
print("=" * 60, flush=True)
