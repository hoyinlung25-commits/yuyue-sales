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

# Phone screen center: SVG (128+8+24, 268+188+12+32) -> scale to 1080x1350
sx, sy = W / 400, H / 640
cx = (36 + 128 + 8 + 24) * sx
cy = (268 + 188 + 12 + 32) * sy
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
draw.text((cx - tw // 2, cy - th // 2), text, fill="#2A2420", font=font)

im.save(OUT, "PNG")
print(f"Wrote {OUT}")
