#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
annual_report_philosophy.md の最初の175行のみを保持するスクリプト
診断機能を追加して問題を特定する
"""
import sys
import os

print("=== Python環境情報 ===", flush=True)
print(f"実行ファイル: {sys.executable}", flush=True)
print(f"Pythonバージョン: {sys.version}", flush=True)
print(f"カレントディレクトリ: {os.getcwd()}", flush=True)

file_path = r'e:\GitHub\kannondai-community\docs\community\2026__\annual_report_philosophy.md'

print(f"\n=== ファイル情報 ===", flush=True)
print(f"対象ファイル: {file_path}", flush=True)
print(f"ファイル存在: {os.path.exists(file_path)}", flush=True)

try:
    # ファイルを読み込み
    print("\n読み込み開始...", flush=True)
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    print(f"✓ 読み込み成功: {len(lines)}行", flush=True)
    
    # 最初の175行のみを保持
    lines_to_keep = lines[:175]
    print(f"保持する行数: {len(lines_to_keep)}", flush=True)
    
    # ファイルに書き戻し
    print("\n書き込み開始...", flush=True)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(lines_to_keep)
    
    print(f"✓ 書き込み成功", flush=True)
    print(f"✓ 完了: {len(lines) - len(lines_to_keep)}行を削除しました", flush=True)
    
except PermissionError as e:
    print(f"\n✗ エラー: ファイルがロックされています", flush=True)
    print(f"  詳細: {e}", flush=True)
    print(f"  原因: VS Code または他のプロセスがファイルを開いている可能性", flush=True)
    sys.exit(1)
    
except Exception as e:
    print(f"\n✗ 予期しないエラー: {type(e).__name__}", flush=True)
    print(f"  詳細: {e}", flush=True)
    import traceback
    traceback.print_exc()
    sys.exit(1)
