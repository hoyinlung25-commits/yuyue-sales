#!/usr/bin/env python3
"""Bupa 保柏易增值 (VTop) — informational WhatsApp poster from bupa.com.hk."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).parent / "bupa-vtop-poster.png"
W, H = 1080, 1920

# Bupa-inspired palette (teal + navy)
NAVY = (0, 51, 102)
TEAL = (0, 130, 150)
TEAL_LIGHT = (224, 247, 250)
WHITE = (255, 255, 255)
GOLD = (255, 193, 7)
SOFT = (240, 248, 255)
MUTED = (71, 85, 105)


def font(size: int, bold: bool = False):
    paths = [
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc" if bold else "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc" if bold else "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
    ]
    for p in paths:
        if Path(p).exists():
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def rounded_rect(draw, box, fill, radius=24):
    x0, y0, x1, y1 = box
    draw.rounded_rectangle(box, radius=radius, fill=fill)


def wrap(draw, text, fnt, max_w):
    lines = []
    for para in text.split("\n"):
        if not para:
            lines.append("")
            continue
        cur = ""
        for ch in para:
            test = cur + ch
            if draw.textlength(test, font=fnt) <= max_w:
                cur = test
            else:
                if cur:
                    lines.append(cur)
                cur = ch
        if cur:
            lines.append(cur)
    return lines


def draw_centered_block(draw, xy, text, fnt, fill, max_w, line_gap=8):
    x, y = xy
    lines = wrap(draw, text, fnt, max_w)
    lh = fnt.size + line_gap
    for line in lines:
        tw = draw.textlength(line, font=fnt)
        draw.text((x + (max_w - tw) / 2, y), line, fill=fill, font=fnt)
        y += lh
    return y


def build():
    img = Image.new("RGB", (W, H), SOFT)
    draw = ImageDraw.Draw(img)

    # Top wave header
    draw.rectangle((0, 0, W, 420), fill=NAVY)
    draw.polygon([(0, 380), (W, 320), (W, 460), (0, 460)], fill=TEAL)

    draw.text((W // 2, 72), "新資訊 · 保柏團體醫保會員必讀", fill=GOLD, font=font(28, True), anchor="mm")
    draw.text((W // 2, 145), "保柏易增值", fill=WHITE, font=font(72, True), anchor="mm")
    draw.text((W // 2, 230), "VTop 醫療保障", fill=TEAL_LIGHT, font=font(40, True), anchor="mm")
    draw.text((W // 2, 310), "離職 · 退休 · 轉工\n醫療保障都可以延續", fill=WHITE, font=font(34, True), anchor="mm")

    # Promo ribbon
    ribbon_y = 480
    rounded_rect(draw, (48, ribbon_y, W - 48, ribbon_y + 88), GOLD, radius=20)
    draw.text(
        (W // 2, ribbon_y + 44),
        "現有保柏團體會員投保　首年保費 9 折",
        fill=NAVY,
        font=font(32, True),
        anchor="mm",
    )

    # Four fact cards (no bullet list — poster tiles)
    cards = [
        ("無須核保", "住院及手術保障\n及自選附加醫療保障"),
        ("不設等候期", "保單生效即時受保\n避免保障真空期"),
        ("保證終生續保", "保費按年齡調整\n索償多亦會續保"),
        ("保障已存在病症", "團體醫保 + 易增值\n連續 12 個月可保"),
    ]
    y = 600
    gap = 20
    card_h = 200
    card_w = (W - 48 * 2 - gap) // 2
    for i, (title, body) in enumerate(cards):
        col, row = i % 2, i // 2
        x0 = 48 + col * (card_w + gap)
        y0 = y + row * (card_h + gap)
        rounded_rect(draw, (x0, y0, x0 + card_w, y0 + card_h), WHITE, radius=22)
        draw.rectangle((x0, y0, x0 + card_w, y0 + 10), fill=TEAL)
        draw.text((x0 + card_w // 2, y0 + 52), title, fill=NAVY, font=font(30, True), anchor="mm")
        draw_centered_block(draw, (x0 + 16, y0 + 88), body, font(24), MUTED, card_w - 32, line_gap=6)

    # Who + when strip
    y2 = y + 2 * (card_h + gap) + 36
    rounded_rect(draw, (48, y2, W - 48, y2 + 200), TEAL_LIGHT, radius=24)
    draw.text((W // 2, y2 + 42), "什麼時候可以投保？", fill=NAVY, font=font(32, True), anchor="mm")
    when = "新入職 60 天內　｜　團體續保週年 60 天內\n離職／退休前後 30 天　｜　結婚或子女出生 30 天內"
    draw_centered_block(draw, (72, y2 + 78), when, font(26), MUTED, W - 144, line_gap=10)

    # Value props
    y3 = y2 + 230
    rounded_rect(draw, (48, y3, W - 48, y3 + 280), NAVY, radius=24)
    draw.text((W // 2, y3 + 48), "為什麼要知？", fill=GOLD, font=font(30, True), anchor="mm")
    points = [
        "在團體醫保之上加一重：先團體賠，再易增值補餘額",
        "退休後失去團體醫保，個人計劃仍可延續",
        "提升病房級別、癌症／洗腎／精神科等保障",
    ]
    py = y3 + 95
    for p in points:
        draw.text((80, py), f"✓  {p}", fill=WHITE, font=font(26))
        py += 58

    # Price anchor
    y4 = y3 + 310
    rounded_rect(draw, (48, y4, W - 48, y4 + 120), WHITE, radius=22)
    draw.text((W // 2, y4 + 38), "保費低至", fill=MUTED, font=font(26), anchor="mm")
    draw.text((W // 2, y4 + 82), "HK$ 143 / 月起*", fill=TEAL, font=font(48, True), anchor="mm")

    # Footer CTA
    y5 = y4 + 150
    rounded_rect(draw, (48, y5, W - 48, y5 + 130), TEAL, radius=22)
    draw.text((W // 2, y5 + 40), "想了解更多？", fill=WHITE, font=font(30, True), anchor="mm")
    draw.text((W // 2, y5 + 88), "致電 2517 5860  ｜  bupa.com.hk/vtop", fill=WHITE, font=font(28, True), anchor="mm")

    # Disclaimer
    disc = (
        "*計劃 1–6 保費不同，須受條款及細則約束。\n"
        "無須核保只適用住院及手術及自選附加醫療；終生只限投保一次。\n"
        "資料摘自 Bupa 官網，僅供參考，以合約為準。"
    )
    draw_centered_block(draw, (56, H - 130), disc, font(20), MUTED, W - 112, line_gap=6)

    img.save(OUT, quality=95)
    print(f"Saved {OUT}")


if __name__ == "__main__":
    build()
