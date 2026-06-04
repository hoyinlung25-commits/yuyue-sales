#!/usr/bin/env python3
"""Combine gift + plant mockup posters; add QR placeholder & Quick Come Quick Serve."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

BASE = Path(__file__).parent
GIFT = BASE / "plant-gift-poster-v2.png"
MOCKUP = BASE / "plant-mockup-poster.png"
OUTPUT = BASE / "plant-combined-poster.png"
W = 1080
FOOTER_H = 420
QR_SIZE = 280


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


def draw_dashed_rect(draw, box, color=(16, 185, 129), width=3, dash=12):
    x0, y0, x1, y1 = box
    for x in range(x0, x1, dash * 2):
        draw.line([(x, y0), (min(x + dash, x1), y0)], fill=color, width=width)
        draw.line([(x, y1), (min(x + dash, x1), y1)], fill=color, width=width)
    for y in range(y0, y1, dash * 2):
        draw.line([(x0, y), (x0, min(y + dash, y1))], fill=color, width=width)
        draw.line([(x1, y), (x1, min(y + dash, y1))], fill=color, width=width)


def build_footer(height: int) -> Image.Image:
    foot = Image.new("RGB", (W, height), (236, 253, 245))
    draw = ImageDraw.Draw(foot)

    # Quick Come Quick Serve banner
    draw.rounded_rectangle((40, 24, W - 40, 118), radius=20, fill=(4, 120, 87))
    draw.text((W // 2, 52), "Quick Come · Quick Serve", fill=(255, 255, 255), font=font(36, True), anchor="mm")
    draw.text((W // 2, 92), "快捷服務 · 快來快約 · 盡快為您安排", fill=(209, 250, 229), font=font(26), anchor="mm")

    # QR zone (right side)
    qr_x = W - QR_SIZE - 56
    qr_y = 130
    draw.rounded_rectangle(
        (qr_x - 12, qr_y - 12, qr_x + QR_SIZE + 12, qr_y + QR_SIZE + 12),
        radius=16,
        fill=(255, 255, 255),
    )
    draw.rectangle((qr_x, qr_y, qr_x + QR_SIZE, qr_y + QR_SIZE), fill=(255, 255, 255))
    draw_dashed_rect(draw, (qr_x, qr_y, qr_x + QR_SIZE, qr_y + QR_SIZE))

    draw.text(
        (qr_x + QR_SIZE // 2, qr_y + QR_SIZE // 2 - 18),
        "QR CODE",
        fill=(156, 163, 175),
        font=font(22, True),
        anchor="mm",
    )
    draw.text(
        (qr_x + QR_SIZE // 2, qr_y + QR_SIZE // 2 + 18),
        "貼上登記二維碼",
        fill=(107, 114, 128),
        font=font(20),
        anchor="mm",
    )

    # Scan / register text (left of QR)
    lx = 48
    draw.text((lx, 150), "掃描登記", fill=(6, 78, 59), font=font(40, True))
    draw.text((lx, 200), "SCAN TO REGISTER", fill=(5, 150, 105), font=font(24, True))
    draw.text(
        (lx, 248),
        "請於 Canva 貼上您的\n登記 QR Code 於右方方框",
        fill=(75, 85, 99),
        font=font(22),
    )
    draw.text(
        (lx, 330),
        "🌱 特選客戶免費獲贈小盆栽",
        fill=(4, 120, 87),
        font=font(24, True),
    )

    return foot


def main():
    gift = Image.open(GIFT).convert("RGB")
    mock = Image.open(MOCKUP).convert("RGB")
    gift_r = fit_width(gift, W)
    mock_r = fit_width(mock, W)
    footer = build_footer(FOOTER_H)

    total_h = gift_r.height + mock_r.height + FOOTER_H
    canvas = Image.new("RGB", (W, total_h), (255, 255, 255))
    y = 0
    canvas.paste(gift_r, (0, y))
    y += gift_r.height
    # thin divider
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((0, y, W, y + 6), fill=(167, 243, 208))
    y += 6
    canvas.paste(mock_r, (0, y))
    y += mock_r.height
    canvas.paste(footer, (0, y))

    canvas.save(OUTPUT, quality=95)
    print(f"Saved {OUTPUT} ({W}x{total_h})")


if __name__ == "__main__":
    main()
