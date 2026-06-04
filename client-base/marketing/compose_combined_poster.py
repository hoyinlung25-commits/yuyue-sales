#!/usr/bin/env python3
"""
Combined poster:
  1) Original gift poster (full)
  2) Plant mock-up strip only (3 varieties) at the end
  3) Footer: 掃碼登記 + QR placeholder (no Quick Come Quick Serve)
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

BASE = Path(__file__).parent
GIFT = BASE / "plant-gift-poster-v2.png"
MOCKUP = BASE / "plant-mockup-poster.png"
OUTPUT = BASE / "plant-combined-poster.png"
W = 1080
FOOTER_H = 360
QR_SIZE = 260
# Crop mock-up image to the three-plant row only (tune if needed)
MOCK_CROP_TOP_RATIO = 0.36
MOCK_CROP_BOTTOM_RATIO = 0.94


def font(size: int, bold: bool = False):
    paths = [
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc" if bold else "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc" if bold else "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
    ]
    for p in paths:
        if Path(p).exists():
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def fit_width(img: Image.Image, width: int) -> Image.Image:
    h = int(img.height * width / img.width)
    return img.resize((width, h), Image.Resampling.LANCZOS)


def extract_plant_mockup_strip(mock: Image.Image) -> Image.Image:
    w, h = mock.size
    y0 = int(h * MOCK_CROP_TOP_RATIO)
    y1 = int(h * MOCK_CROP_BOTTOM_RATIO)
    return mock.crop((0, y0, w, y1))


def draw_dashed_rect(draw, box, color=(16, 185, 129), width=3, dash=12):
    x0, y0, x1, y1 = box
    for x in range(x0, x1, dash * 2):
        draw.line([(x, y0), (min(x + dash, x1), y0)], fill=color, width=width)
        draw.line([(x, y1), (min(x + dash, x1), y1)], fill=color, width=width)
    for y in range(y0, y1, dash * 2):
        draw.line([(x0, y), (x0, min(y + dash, y1))], fill=color, width=width)
        draw.line([(x1, y), (x1, min(y + dash, y1))], fill=color, width=width)


def build_footer(height: int) -> Image.Image:
    foot = Image.new("RGB", (W, height), (248, 250, 252))
    draw = ImageDraw.Draw(foot)

    # Title centred
    draw.text((W // 2, 42), "掃碼登記", fill=(6, 78, 59), font=font(48, True), anchor="mm")
    draw.text((W // 2, 88), "SCAN TO REGISTER", fill=(5, 150, 105), font=font(22), anchor="mm")

    qr_x = (W - QR_SIZE) // 2
    qr_y = 118
    draw.rounded_rectangle(
        (qr_x - 14, qr_y - 14, qr_x + QR_SIZE + 14, qr_y + QR_SIZE + 14),
        radius=18,
        fill=(255, 255, 255),
        outline=(167, 243, 208),
        width=2,
    )
    draw.rectangle((qr_x, qr_y, qr_x + QR_SIZE, qr_y + QR_SIZE), fill=(255, 255, 255))
    draw_dashed_rect(draw, (qr_x, qr_y, qr_x + QR_SIZE, qr_y + QR_SIZE))

    draw.text(
        (W // 2, qr_y + QR_SIZE // 2 - 12),
        "QR CODE",
        fill=(156, 163, 175),
        font=font(20, True),
        anchor="mm",
    )
    draw.text(
        (W // 2, qr_y + QR_SIZE // 2 + 16),
        "請於 Canva 貼上登記二維碼",
        fill=(107, 114, 128),
        font=font(20),
        anchor="mm",
    )

    return foot


def build_mockup_section(mock: Image.Image) -> Image.Image:
    """Plant strip + small heading bar."""
    strip = extract_plant_mockup_strip(mock)
    strip_r = fit_width(strip, W)
    bar_h = 56
    section = Image.new("RGB", (W, bar_h + strip_r.height), (240, 253, 244))
    draw = ImageDraw.Draw(section)
    draw.rectangle((0, 0, W, bar_h), fill=(209, 250, 229))
    draw.text(
        (W // 2, bar_h // 2),
        "精選小盆栽 · 碰碰香 ／ 碧玉 ／ 金魚花",
        fill=(6, 95, 70),
        font=font(28, True),
        anchor="mm",
    )
    section.paste(strip_r, (0, bar_h))
    return section


def main():
    gift = Image.open(GIFT).convert("RGB")
    mock = Image.open(MOCKUP).convert("RGB")

    gift_r = fit_width(gift, W)
    mock_section = build_mockup_section(mock)
    footer = build_footer(FOOTER_H)

    total_h = gift_r.height + mock_section.height + FOOTER_H
    canvas = Image.new("RGB", (W, total_h), (255, 255, 255))
    y = 0
    canvas.paste(gift_r, (0, y))
    y += gift_r.height

    draw = ImageDraw.Draw(canvas)
    draw.rectangle((0, y, W, y + 8), fill=(167, 243, 208))
    y += 8

    canvas.paste(mock_section, (0, y))
    y += mock_section.height

    canvas.paste(footer, (0, y))

    canvas.save(OUTPUT, quality=95)
    print(f"Saved {OUTPUT} ({W}x{total_h})")


if __name__ == "__main__":
    main()
