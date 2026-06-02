#!/usr/bin/env python3
"""Export Day 3 SVG to 1080x1350 PNG with 已讀 on phone."""
import urllib.request
from pathlib import Path

import cairosvg
from PIL import Image, ImageDraw, ImageFont

SVG = Path("/workspace/assets/axo/pen/axo-pen-day3-seen.svg")
OUT = Path("/workspace/assets/axo/pen/png/axo-pen-day3-seen.png")
FONT = Path("/tmp/NotoSansTC-Bold.otf")
FONT_URL = (
    "https://cdn.jsdelivr.net/gh/notofonts/noto-cjk@main/"
    "Sans/OTF/TraditionalChinese/NotoSansCJKtc-Bold.otf"
)
W, H = 1080, 1350


def ensure_font() -> Path:
    if not FONT.exists():
        print("Downloading Noto Sans TC...")
        urllib.request.urlretrieve(FONT_URL, FONT)
    return FONT


def main() -> None:
    ensure_font()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    cairosvg.svg2png(url=f"file://{SVG}", write_to=str(OUT), output_width=W, output_height=H)

    sx, sy = W / 400, H / 640
    # phone group: translate(48,290) + (118,168) + screen center (34,47)
    cx = (48 + 118 + 34) * sx
    cy = (290 + 168 + 47) * sy

    im = Image.open(OUT).convert("RGBA")
    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype(str(FONT), 46)
    text = "\u5df2\u8b80"  # 已讀
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text((cx - tw / 2, cy - th / 2), text, fill="#2A2420", font=font)
    im.save(OUT, "PNG")
    print(f"Wrote {OUT} ({W}x{H})")


if __name__ == "__main__":
    main()
