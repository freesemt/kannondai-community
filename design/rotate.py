import cv2
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = ["MS Gothic"]  # "MS Gothic", "MS Mincho", "Meiryo" 

# 入力画像ファイル
input_path = r"E:\GitHub\design\base.png"
angle = 5 # 回転角度（度単位、反時計回り）

# 画像読み込み（BGR）
img = cv2.imread(input_path)
if img is None:
    raise FileNotFoundError(f"{input_path} が見つかりません")

# 画像中心・回転行列
(h, w) = img.shape[:2]
center = (w // 2, h // 2)
M = cv2.getRotationMatrix2D(center, angle, 1.0)

# 回転後の画像サイズを計算
cos = abs(M[0, 0])
sin = abs(M[0, 1])
new_w = int((h * sin) + (w * cos))
new_h = int((h * cos) + (w * sin))

# 回転行列を調整
M[0, 2] += (new_w / 2) - center[0]
M[1, 2] += (new_h / 2) - center[1]

# 回転画像生成
rotated = cv2.warpAffine(img, M, (new_w, new_h), borderValue=(255,255,255))

# BGR→RGB変換
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
rotated_rgb = cv2.cvtColor(rotated, cv2.COLOR_BGR2RGB)

# 並べて表示
fig, axes = plt.subplots(1, 2, figsize=(12, 6))
axes[0].imshow(img_rgb)
axes[0].set_title("元画像")
axes[0].axis("off")
axes[1].imshow(rotated_rgb)
axes[1].set_title(f"{angle}度回転後")
axes[1].axis("off")
plt.tight_layout()
plt.show()

# 回転画像を保存
output_path = r"E:\GitHub\design\base-rotated.png"
cv2.imwrite(output_path, rotated)
print(f"回転画像を保存しました: {output_path}")