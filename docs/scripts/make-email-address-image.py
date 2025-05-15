from PIL import Image, ImageDraw, ImageFont

# 画像サイズと背景色
width, height = 400, 100
background_color = "white"
text_color = "black"
text = "xxxxxxxxxx@gmail.com"

# フォント設定（フォントパスを適宜変更）
font_path = "arial.ttf"  # システムにインストールされているフォントを指定
font_size = 20
font = ImageFont.truetype(font_path, font_size)

# 画像作成
image = Image.new("RGB", (width, height), background_color)
draw = ImageDraw.Draw(image)

# テキストの位置を計算して中央揃え
text_bbox = draw.textbbox((0, 0), text, font=font)  # テキストのバウンディングボックスを取得
text_width = text_bbox[2] - text_bbox[0]
text_height = text_bbox[3] - text_bbox[1]
text_x = (width - text_width) // 2
text_y = (height - text_height) // 2
draw.text((text_x, text_y), text, fill=text_color, font=font)

# 画像を保存
image.save("email-address.png")
print("画像が保存されました: email-address.png")