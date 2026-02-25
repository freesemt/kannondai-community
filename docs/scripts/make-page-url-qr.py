"""
QRコード生成スクリプト
docs/page_url.png を生成する（ページURLのQRコード）

使い方:
    python docs/scripts/make-page-url-qr.py
"""

import qrcode
from pathlib import Path

URL = "https://kannondai.github.io/kannondai-community/top.html"
OUTPUT = Path(__file__).parent.parent / "page_url.png"

qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_M,
    box_size=10,
    border=4,
)
qr.add_data(URL)
qr.make(fit=True)

img = qr.make_image(fill_color="black", back_color="white")
img.save(OUTPUT)
print(f"QRコードを保存しました: {OUTPUT}")
print(f"対象URL: {URL}")
