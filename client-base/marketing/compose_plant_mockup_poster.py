#!/usr/bin/env python3
"""
Build WhatsApp poster from YOUR plant photos.

Save 3 photos in plant-photos/ (any common image format):
  pengpengxiang.*  → 碰碰香
  biyu.*           → 碧玉
  jinyuhua.*       → 金魚花

Run: python3 compose_plant_mockup_poster.py
"""

from __future__ import annotations

import glob
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

BASE = Path(__file__).parent
PHOTOS = BASE / "plant-photos"
OUTPUT = BASE / "plant-mockup-poster.png"
W, H = 1080, 1920

LABELS = [
    ("pengpengxiang", "碰碰香", "樂觀開朗 · 幸福快樂"),
    ("biyu", "碧玉", "吉祥平安 · 招財進寶"),
    ("jinyuhua", "金魚花", "生命力 · 生生不息"),
]


def find_photo(stem: str) -> Path | None:
    for ext in ("jpg", "jpeg", "png", "webp", "JPG", "PNG"):
        hits = list(PHOTOS.glob(f"{stem}.{ext}"))
        if hits:
            return hits[0]
    return None


def load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    paths = [
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc" if bold else "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc" if bold else "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for p in paths:
        if Path(p).exists():
            try:
                return ImageFont.truetype(p, size)
            except OSError:
                continue
    return ImageFont.load_default()


def enhance_photo(img: Image.Image) -> Image.Image:
    img = img.convert("RGB")
    img = ImageEnhance.Brightness(img).enhance(1.06)
    img = ImageEnhance.Contrast(img).enhance(1.1)
    img = ImageEnhance.Color(img).enhance(1.12)
    img = img.filter(ImageFilter.UnsharpMask(radius=1.2, percent=90, threshold=3))
    return img


def crop_center_square(img: Image.Image, size: int) -> Image.Image:
    w, h = img.size
    side = min(w, h)
    left = (w - side) // 2
    top = (h - side) // 2
    img = img.crop((left, top, left + side, top + side))
    return img.resize((size, size), Image.Resampling.LANCZOS)


def draw_rounded_card(
    canvas: Image.Image,
    xy: tuple[int, int, int, int],
    radius: int,
    fill: tuple[int, int, int],
) -> None:
    draw = ImageDraw.Draw(canvas)
    x0, y0, x1, y1 = xy
    draw.rounded_rectangle(xy, radius=radius, fill=fill)


def paste_photo_card(
    canvas: Image.Image,
    photo: Image.Image,
    x: int,
    y: int,
    card_w: int,
    card_h: int,
) -> None:
    pad = 16
    shadow = Image.new("RGBA", (card_w + 8, card_h + 8), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rounded_rectangle((4, 4, card_w + 4, card_h + 4), radius=24, fill=(0, 0, 0, 40))
    canvas.paste(shadow, (x - 4, y - 2), shadow)

    card = Image.new("RGB", (card_w, card_h), (255, 255, 255))
    draw_rounded_card(card, (0, 0, card_w, card_h), 22, (255, 255, 255))
    inner = card_w - pad * 2
    ph = crop_center_square(photo, inner)
    card.paste(ph, (pad, pad))
    canvas.paste(card, (x, y))


def wrap_text(draw: ImageDraw.ImageDraw, text: str, font, max_width: int) -> list[str]:
    lines: list[str] = []
    for para in text.split("\n"):
        if not para:
            lines.append("")
            continue
        buf = ""
        for ch in para:
            test = buf + ch
            if draw.textlength(test, font=font) <= max_width:
                buf = test
            else:
                if buf:
                    lines.append(buf)
                buf = ch
        if buf:
            lines.append(buf)
    return lines


def build(photos: list[tuple[str, Image.Image]]) -> Image.Image:
    bg = Image.new("RGB", (W, H), (240, 253, 244))
    draw = ImageDraw.Draw(bg)
    for y in range(H):
        t = y / H
        g = int(240 + (220 - 240) * t)
        b = int(244 + (230 - 244) * t)
        draw.line([(0, y), (W, y)], fill=(230, g, b))

    title_f = load_font(52, True)
    sub_f = load_font(30, False)
    body_f = load_font(26, False)
    small_f = load_font(22, False)
    label_f = load_font(34, True)

    draw.text((W // 2, 70), "特選客戶可免費🆓獲贈", fill=(6, 78, 59), font=title_f, anchor="mm")
    draw.text(
        (W // 2, 130),
        "【Muji同款日本有機無土種植小盆栽】",
        fill=(5, 150, 105),
        font=sub_f,
        anchor="mm",
    )
    draw.text((W // 2, 175), "🌱🌿☘️🍀🪴", fill=(16, 185, 129), font=sub_f, anchor="mm")

    card_w, card_h = 300, 340
    gap = 24
    total = 3 * card_w + 2 * gap
    x0 = (W - total) // 2
    y_cards = 220

    for i, ((name_cn, tagline), (_, photo)) in enumerate(zip(LABELS, photos)):
        x = x0 + i * (card_w + gap)
        paste_photo_card(bg, photo, x, y_cards, card_w, card_h)
        draw.text((x + card_w // 2, y_cards + card_h + 28), name_cn, fill=(6, 95, 70), font=label_f, anchor="mm")
        draw.text(
            (x + card_w // 2, y_cards + card_h + 68),
            tagline,
            fill=(107, 114, 128),
            font=small_f,
            anchor="mm",
        )

    box_y = 640
    draw.rounded_rectangle((48, box_y, W - 48, box_y + 420), radius=28, fill=(255, 255, 255))
    meaning_title = "為何「為植物 · 為地球」種一棵植物？"
    draw.text((72, box_y + 28), meaning_title, fill=(6, 78, 59), font=load_font(32, True))

    body = (
        "🌍 每一盆小植物，都是為地球多一分綠色\n"
        "♻️ 日本有機無土介質 PAFCAL（Toyota & Suntory 研發）\n"
        "   乾淨、無蟲蟻、易打理，減少浪費\n"
        "💚 桌面上一抹綠，也是為環境出一分力\n"
        "🌱 一齊做 Plant Plant 播種小農夫\n\n"
        "A little gift for you — plant for the planet"
    )
    lines = wrap_text(draw, body, body_f, W - 120)
    ty = box_y + 85
    for line in lines:
        draw.text((72, ty), line, fill=(55, 65, 81), font=body_f)
        ty += 36

    draw.text(
        (W // 2, H - 55),
        "特選客戶可揀選一盆 · 推廣環境綠化",
        fill=(4, 120, 87),
        font=small_f,
        anchor="mm",
    )
    return bg


def main() -> None:
    PHOTOS.mkdir(parents=True, exist_ok=True)
    loaded: list[tuple[str, Image.Image]] = []
    for stem, cn, _ in LABELS:
        path = find_photo(stem)
        if not path:
            print(f"Missing photo: plant-photos/{stem}.jpg (or .png)")
            print("See plant-photos/README.md")
            raise SystemExit(1)
        loaded.append((cn, enhance_photo(Image.open(path))))

    poster = build(loaded)
    poster.save(OUTPUT, quality=95)
    print(f"Saved {OUTPUT}")


if __name__ == "__main__":
    main()
