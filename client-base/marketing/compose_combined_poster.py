#!/usr/bin/env python3
"""
Combined poster (fixed):
  1) Original gift poster (scaled, max height so lower sections show on phone)
  2) Plant mock-up panel: 3 plants + 「為植物·為地球」 meaning box
  3) 掃碼登記 + QR placeholder
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

BASE = Path(__file__).parent
GIFT = BASE / "plant-gift-poster-v2.png"
MOCKUP = BASE / "plant-mockup-poster.png"
OUTPUT = BASE / "plant-combined-poster.png"
W = 1080
MAX_GIFT_H = 760
FOOTER_H = 380
QR_SIZE = 268


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


def limit_height(img: Image.Image, max_h: int) -> Image.Image:
    if img.height <= max_h:
        return img
    w = int(img.width * max_h / img.height)
    return img.resize((w, max_h), Image.Resampling.LANCZOS)


def center_on_canvas(img: Image.Image, canvas_w: int, bg: tuple[int, int, int]) -> Image.Image:
    out = Image.new("RGB", (canvas_w, img.height), bg)
    x = (canvas_w - img.width) // 2
    out.paste(img, (x, 0))
    return out


def extract_plant_panel(mock: Image.Image) -> Image.Image:
    """Plants row + meaning white box (matches user reference layout)."""
    w, h = mock.size
    # Include from just below top headline through the meaning card (not footer slogans if duplicated)
    y0 = int(h * 0.10)
    y1 = int(h * 0.98)
    return mock.crop((0, y0, w, y1))


def draw_dashed_rect(draw, box, color=(16, 185, 129), width=3, dash=12):
    x0, y0, x1, y1 = box
    for x in range(x0, x1, dash * 2):
        draw.line([(x, y0), (min(x + dash, x1), y0)], fill=color, width=width)
        draw.line([(x, y1), (min(x + dash, x1), y1)], fill=color, width=width)
    for y in range(y0, y1, dash * 2):
        draw.line([(x0, y), (x0, min(y + dash, y1))], fill=color, width=width)
        draw.line([(x1, y), (x1, min(y + dash, y1))], fill=color, width=width)


def section_band(text: str, height: int = 52) -> Image.Image:
    band = Image.new("RGB", (W, height), (5, 150, 105))
    draw = ImageDraw.Draw(band)
    draw.text((W // 2, height // 2), text, fill=(255, 255, 255), font=font(26, True), anchor="mm")
    return band


def build_footer() -> Image.Image:
    foot = Image.new("RGB", (W, FOOTER_H), (236, 253, 245))
    draw = ImageDraw.Draw(foot)

    draw.text((W // 2, 48), "掃碼登記", fill=(6, 78, 59), font=font(52, True), anchor="mm")
    draw.text((W // 2, 98), "SCAN TO REGISTER", fill=(5, 150, 105), font=font(22), anchor="mm")

    qr_x = (W - QR_SIZE) // 2
    qr_y = 128
    draw.rounded_rectangle(
        (qr_x - 16, qr_y - 16, qr_x + QR_SIZE + 16, qr_y + QR_SIZE + 16),
        radius=20,
        fill=(255, 255, 255),
        outline=(16, 185, 129),
        width=3,
    )
    draw_dashed_rect(draw, (qr_x, qr_y, qr_x + QR_SIZE, qr_y + QR_SIZE))

    draw.text(
        (W // 2, qr_y + QR_SIZE // 2 - 14),
        "QR CODE",
        fill=(156, 163, 175),
        font=font(22, True),
        anchor="mm",
    )
    draw.text(
        (W // 2, qr_y + QR_SIZE // 2 + 18),
        "請於 Canva 貼上登記二維碼",
        fill=(75, 85, 99),
        font=font(22),
        anchor="mm",
    )

    return foot


def build_plant_panel_fallback() -> Image.Image:
    """Fallback if mockup file missing — drawn panel."""
    panel_h = 900
    img = Image.new("RGB", (W, panel_h), (240, 253, 244))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle((40, 40, W - 40, panel_h - 40), radius=24, fill=(255, 255, 255))
    draw.text((W // 2, 80), "碰碰香    碧玉    金魚花", fill=(6, 78, 59), font=font(32, True), anchor="mm")
    lines = [
        "為何「為植物 · 為地球」種一棵植物？",
        "",
        "每一棵小小的植物，都是為地球增添綠意的力量。",
        "採用 PAFCAL® 無土種植介質，乾淨衛生、無蟲害。",
        "為地球種下一抹綠意，從生活開始改變。",
        "一起成為 Plant Plant 農夫，守護地球。",
    ]
    y = 140
    for line in lines:
        draw.text((72, y), line, fill=(55, 65, 81), font=font(24))
        y += 40
    return img


def main():
    if not GIFT.exists():
        raise SystemExit(f"Missing {GIFT}")

    gift = Image.open(GIFT).convert("RGB")
    gift_r = fit_width(gift, W)
    gift_r = limit_height(gift_r, MAX_GIFT_H)
    gift_r = center_on_canvas(gift_r, W, (240, 253, 244))

    if MOCKUP.exists():
        mock = Image.open(MOCKUP).convert("RGB")
        plant_panel = extract_plant_panel(mock)
        plant_panel = fit_width(plant_panel, W)
    else:
        plant_panel = build_plant_panel_fallback()

    footer = build_footer()

    parts = [
        gift_r,
        section_band("▼  小盆栽款式  ▼"),
        plant_panel,
        section_band("▼  掃碼登記  ▼"),
        footer,
    ]
    total_h = sum(p.height for p in parts)
    canvas = Image.new("RGB", (W, total_h), (240, 253, 244))
    y = 0
    for part in parts:
        canvas.paste(part, (0, y))
        y += part.height

    canvas.save(OUTPUT, quality=95, optimize=True)
    print(f"Saved {OUTPUT} ({W}x{total_h})")
    print(f"  gift: {gift_r.height}px | plants+meaning: {plant_panel.height}px | footer: {FOOTER_H}px")


if __name__ == "__main__":
    main()
