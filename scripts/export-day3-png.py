#!/usr/bin/env python3
"""Export Day 3 SVG to PNG and stamp 已讀 on phone screen."""
import cairosvg
from PIL import Image, ImageDraw, ImageFont

SVG = "/workspace/assets/axo/pen/axo-pen-day3-seen.svg"
OUT = "/workspace/assets/axo/pen/png/axo-pen-day3-seen.png"
W, H = 1080, 1350

cairosvg.svg2png(url=f"file://{SVG}", write_to=OUT, output_width=W, output_height=H)

im = Image.open(OUT).convert("RGBA")
draw = ImageDraw.Draw(im)

# Phone screen center ~ (432, 720) in 1080x1350 (from SVG layout)
font = None
for path in (
    "/tmp/NotoSansTC-Bold.otf",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
    "/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc",
):
    try:
        font = ImageFont.truetype(path, 52)
        break
    except OSError:
        continue
if font is None:
    font = ImageFont.load_default()

text = "已讀"
bbox = draw.textbbox((0, 0), text, font=font)
tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
cx, cy = 432, 718
draw.text((cx - tw // 2, cy - th // 2), text, fill="#2A2420", font=font)

im.save(OUT, "PNG")
print(f"Wrote {OUT}")
