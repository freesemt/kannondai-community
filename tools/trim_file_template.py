#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
汎用ファイル削除スクリプト（テンプレート）
Usage: 最初のN行を保持し、それ以降を削除する

このファイルをコピーして使用してください：
1. file_path を対象ファイルに変更
2. lines_to_keep の数値を変更
3. フルパスのPythonで実行: & "C:\Program Files\Python313\python.exe" tools\your_script.py
"""
import sys
import os

print("=" * 60, flush=True)
print("ファイル削除スクリプト", flush=True)
print("=" * 60, flush=True)

# ===== 設定（ここを編集） =====
file_path = r'path\to\your\file.md'  # 対象ファイルのフルパス
lines_to_keep = 175  # 保持する行数
# ============================

print(f"\n[環境情報]", flush=True)
print(f"Python: {sys.executable}", flush=True)
print(f"Version: {sys.version.split()[0]}", flush=True)
print(f"対象ファイル: {file_path}", flush=True)

# ファイル存在確認
if not os.path.exists(file_path):
    print(f"\n✗ エラー: ファイルが見つかりません", flush=True)
    sys.exit(1)

try:
    # 読み込み
    print(f"\n[読み込み中...]", flush=True)
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    print(f"✓ 現在の行数: {len(lines)}", flush=True)
    
    if len(lines) <= lines_to_keep:
        print(f"\n⚠ 警告: ファイルは既に{lines_to_keep}行以下です（{len(lines)}行）", flush=True)
        print(f"削除は不要です", flush=True)
        sys.exit(0)
    
    # 削除対象の確認
    lines_kept = lines[:lines_to_keep]
    lines_deleted = len(lines) - lines_to_keep
    
    print(f"✓ 保持する行数: {len(lines_kept)}", flush=True)
    print(f"✓ 削除する行数: {lines_deleted}", flush=True)
    
    # 書き込み
    print(f"\n[書き込み中...]", flush=True)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(lines_kept)
    
    print(f"✓ 書き込み成功", flush=True)
    print(f"\n" + "=" * 60, flush=True)
    print(f"✓ 完了: {lines_deleted}行を削除しました", flush=True)
    print(f"=" * 60, flush=True)
    
except PermissionError as e:
    print(f"\n✗ エラー: ファイルへのアクセスが拒否されました", flush=True)
    print(f"  原因: 他のプロセス（VS Codeなど）がファイルを開いている可能性", flush=True)
    print(f"  対策: VS Codeでファイルを閉じてから再実行してください", flush=True)
    sys.exit(1)
    
except Exception as e:
    print(f"\n✗ 予期しないエラー: {type(e).__name__}", flush=True)
    print(f"  詳細: {e}", flush=True)
    import traceback
    traceback.print_exc()
    sys.exit(1)
