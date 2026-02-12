r"""
3階層構造の比較図を生成（昔 vs 今）

このスクリプトは年報第1部で説明している「自治会に期待する3階層」の
時代による意味の違いを視覚化します。

Requirements:
- matplotlib (install if needed)

Usage:
    cd E:\GitHub\kannondai-community
    & "C:\Program Files\Python313\python.exe" tools\create_hierarchy_diagram.py

Output:
    docs/community/2026__/images/hierarchy_diagram.png
"""

import sys
from pathlib import Path

try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    from matplotlib.patches import FancyBboxPatch
    import matplotlib.gridspec as gridspec
    
    print("matplotlib imported successfully", flush=True)
    
    # 日本語フォント設定
    plt.rcParams['font.sans-serif'] = ['MS Gothic', 'Yu Gothic', 'Meiryo']
    plt.rcParams['axes.unicode_minus'] = False
    
    # 図の作成（GridSpecで左右の幅比を調整）
    fig = plt.figure(figsize=(16, 8))
    gs = gridspec.GridSpec(1, 2, width_ratios=[4, 6], wspace=0.1)
    ax1 = fig.add_subplot(gs[0])
    ax2 = fig.add_subplot(gs[1])
    
    # 階層のデータ（面積を近づけるため、幅が広い層ほど高さを低く）
    # わずかな隙間を入れて重なりを防ぐ
    layers = [
        {'name': '第3階層', 'desc': '交流・イベント', 'y': 1.10, 'width': 3, 'height': 0.8, 'color': '#E8F4F8'},
        {'name': '第2階層', 'desc': '防災・防犯・見守り', 'y': 0.50, 'width': 4.5, 'height': 0.55, 'color': '#B8D8E8'},
        {'name': '第1階層', 'desc': 'ゴミ出し（必須）', 'y': 0, 'width': 6, 'height': 0.45, 'color': '#7FB3D5'}
    ]
    
    # ===== 左の図（昔） =====
    ax1.set_xlim(-4, 4.5)
    ax1.set_ylim(-0.6, 2.45)
    ax1.axis('off')
    ax1.set_title('昔（貧しい時代）', fontsize=20, fontweight='bold')
    
    # ピラミッドを描画
    for layer in layers:
        # 台形（ピラミッド）
        width = layer['width']
        x_center = 0
        y_bottom = layer['y']
        height = layer['height']
        
        rect = FancyBboxPatch(
            (x_center - width/2, y_bottom),
            width, height,
            boxstyle="round,pad=0.02",
            edgecolor='#2C5F8D',
            facecolor=layer['color'],
            linewidth=2
        )
        ax1.add_patch(rect)
        
        # テキスト
        ax1.text(x_center, y_bottom + height/2, 
                f"{layer['name']}\n{layer['desc']}", 
                ha='center', va='center', fontsize=14, fontweight='bold')
    
    # 下から上への矢印（ニーズの流れ）
    # 第1階層の底辺(0)から第3階層の上辺(1.90)まで
    ax1.annotate('', xy=(3.2, 1.90), xytext=(3.2, 0),
                arrowprops=dict(arrowstyle='->', lw=3.5, color='#D32F2F'))
    
    # 左側の凡例（横矢印）縦矢印の上あたりに配置
    legend_y_left = 2.15
    legend_x_start_left = 2.0
    ax1.plot([legend_x_start_left, legend_x_start_left+0.5], [legend_y_left, legend_y_left], 
            color='#D32F2F', linewidth=3.5, solid_capstyle='round')
    ax1.plot(legend_x_start_left+0.5, legend_y_left, marker='>', markersize=8, color='#D32F2F')
    ax1.text(legend_x_start_left+0.65, legend_y_left, '一律に自治会に期待', va='center', fontsize=14)
    
    # ===== 右の図（今） =====
    ax2.set_xlim(-4, 6.5)
    ax2.set_ylim(-0.6, 2.45)
    ax2.axis('off')
    ax2.set_title('今（豊かな時代）', fontsize=20, fontweight='bold')
    
    # ピラミッドを描画（すべて同じ色で統一）
    for i, layer in enumerate(layers):
        width = layer['width']
        x_center = 0
        y_bottom = layer['y']
        height = layer['height']
        
        rect = FancyBboxPatch(
            (x_center - width/2, y_bottom),
            width, height,
            boxstyle="round,pad=0.02",
            edgecolor='#2C5F8D',
            facecolor='#B8D8E8',  # 全階層を第2階層と同じ色に統一
            linewidth=2,
            alpha=1.0
        )
        ax2.add_patch(rect)
        
        # テキスト
        ax2.text(x_center, y_bottom + height/2, 
                f"{layer['name']}\n{layer['desc']}", 
                ha='center', va='center', fontsize=14, fontweight='bold')
    
    # 3つの矢印パターン（右側に配置）
    arrow_x_positions = [3.8, 4.6, 5.4]
    
    # 1. 左：全階層（赤）
    ax2.annotate('', xy=(arrow_x_positions[0], 1.90), xytext=(arrow_x_positions[0], 0),
                arrowprops=dict(arrowstyle='->', lw=3.5, color='#D32F2F'))
    ax2.text(arrow_x_positions[0], -0.25, '全階層', ha='center', fontsize=14, fontweight='bold')
    
    # 2. 中央：第1+第2階層（赤）+ 第3階層（緑）
    ax2.annotate('', xy=(arrow_x_positions[1], 1.05), xytext=(arrow_x_positions[1], 0),
                arrowprops=dict(arrowstyle='->', lw=3.5, color='#D32F2F'))
    ax2.annotate('', xy=(arrow_x_positions[1], 1.90), xytext=(arrow_x_positions[1], 1.10),
                arrowprops=dict(arrowstyle='->', lw=3.5, color='#558B2F'))
    ax2.text(arrow_x_positions[1], -0.25, '第1+2', ha='center', fontsize=14, fontweight='bold')
    
    # 3. 右：第1階層のみ（赤）+ 第2・第3階層（緑）
    ax2.annotate('', xy=(arrow_x_positions[2], 0.45), xytext=(arrow_x_positions[2], 0),
                arrowprops=dict(arrowstyle='->', lw=3.5, color='#D32F2F'))
    ax2.annotate('', xy=(arrow_x_positions[2], 1.90), xytext=(arrow_x_positions[2], 0.50),
                arrowprops=dict(arrowstyle='->', lw=3.5, color='#558B2F'))
    ax2.text(arrow_x_positions[2], -0.25, '第1のみ', ha='center', fontsize=14, fontweight='bold')
    
    # タイトル：多様なニーズのパターン（凡例の上）
    ax2.text(4.6, 2.28, 'ニーズの多様化', 
            ha='center', fontsize=14, fontweight='bold', color='#333333')
    
    # 凡例（矢印の上部、横並びに配置）
    legend_y = 2.15
    legend_x_start = 2.8
    # 赤い矢印
    ax2.plot([legend_x_start, legend_x_start+0.5], [legend_y, legend_y], 
            color='#D32F2F', linewidth=3.5, solid_capstyle='round')
    ax2.plot(legend_x_start+0.5, legend_y, marker='>', markersize=8, color='#D32F2F')
    ax2.text(legend_x_start+0.65, legend_y, '自治会に期待', va='center', fontsize=14)
    
    # 緑の矢印（横並び、赤矢印と間隔を空ける）
    ax2.plot([legend_x_start+2.2, legend_x_start+2.7], [legend_y, legend_y], 
            color='#558B2F', linewidth=3.5, solid_capstyle='round')
    ax2.plot(legend_x_start+2.7, legend_y, marker='>', markersize=8, color='#558B2F')
    ax2.text(legend_x_start+2.85, legend_y, '自分で充足', va='center', fontsize=14)
    
    # 説明文（削除）
    # 「多様なニーズのパターン」は凡例の上に移動済み
    
    # 全体のタイトル
    fig.suptitle('自治会に期待する要望階層の時代による違い', 
                fontsize=28, fontweight='bold', y=0.95)
    
    # 余白調整（左右の余白をさらに増やす）
    plt.subplots_adjust(left=0.05, right=0.95, top=0.80, bottom=0.02)
    
    # 保存
    output_path = Path(__file__).parent.parent / 'docs' / 'community' / '2026__' / 'images' / 'hierarchy_diagram.png'
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.savefig(output_path)
    print(f"✓ SUCCESS! 図を作成しました", flush=True)
    print(f"✓ Output: {output_path.relative_to(Path.cwd())}", flush=True)
    print(f"✓ File size: {output_path.stat().st_size:,} bytes", flush=True)
    
    plt.close()
    
except ImportError as e:
    print(f"ERROR: Missing required library - {e}", file=sys.stderr, flush=True)
    print("\nInstall missing libraries:", flush=True)
    print('  & "C:\\Program Files\\Python313\\python.exe" -m pip install matplotlib', flush=True)
    sys.exit(1)
    
except Exception as e:
    print(f"ERROR: {e}", file=sys.stderr, flush=True)
    import traceback
    traceback.print_exc()
    sys.exit(1)
