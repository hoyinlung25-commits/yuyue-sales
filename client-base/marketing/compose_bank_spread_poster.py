#!/usr/bin/env python3
"""WhatsApp poster: bank interest-spread offer (~HK$300k, 5-year)."""

from pathlib import Path

from PIL import Image, ImageDraw

from poster_fonts import poster_font

OUT = Path(__file__).parent / "bank-spread-offer-poster.png"
W, H = 1080, 1350

NAVY = (15, 23, 42)
GOLD = (245, 158, 11)
GOLD_LIGHT = (254, 243, 199)
WHITE = (255, 255, 255)
TEAL = (13, 148, 136)
MUTED = (71, 85, 105)
BG = (248, 250, 252)


def fnt(size: int, bold: bool = False):
    return poster_font(size + (4 if bold else 0), bold)


def rounded(draw, box, fill, radius=22):
    draw.rounded_rectangle(box, radius=radius, fill=fill)


def center(draw, xy, text, font, fill, max_w):
    x, y = xy
    lines = []
    for para in text.split("\n"):
        cur = ""
        for ch in para:
            test = cur + ch
            if draw.textlength(test, font=font) <= max_w:
                cur = test
            else:
                if cur:
                    lines.append(cur)
                cur = ch
        if cur:
            lines.append(cur)
    lh = font.size + 10
    for line in lines:
        tw = draw.textlength(line, font=font)
        draw.text((x + (max_w - tw) / 2, y), line, fill=fill, font=font)
        y += lh


def build():
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    rounded(draw, (0, 0, W, 300), NAVY, radius=0)
    draw.rectangle((0, 260, W, 300), fill=TEAL)
    draw.text((W // 2, 56), "新資訊 · 名額有限", fill=GOLD, font=fnt(28, True), anchor="mm")
    draw.text((W // 2, 130), "銀行息差配置", fill=WHITE, font=fnt(64, True), anchor="mm")
    draw.text((W // 2, 210), "閒置資金 · 中線增值參考", fill=GOLD_LIGHT, font=fnt(30), anchor="mm")

    rounded(draw, (48, 330, W - 48, 410), GOLD, radius=18)
    draw.text((W // 2, 370), "我手頭尚餘少量 quota · 先到先得", fill=NAVY, font=fnt(30, True), anchor="mm")

    stats = [
        ("入場", "約 HK$30 萬"),
        ("參考年化*", "7 – 9%"),
        ("建議年期", "5 年"),
        ("5年總回報*", "35 – 44%"),
    ]
    y = 440
    gw = (W - 48 * 2 - 18) // 2
    gh = 150
    for i, (label, val) in enumerate(stats):
        col, row = i % 2, i // 2
        x0 = 48 + col * (gw + 18)
        y0 = y + row * (gh + 18)
        rounded(draw, (x0, y0, x0 + gw, y0 + gh), WHITE, radius=20)
        draw.rectangle((x0, y0, x0 + gw, y0 + 8), fill=TEAL)
        draw.text((x0 + gw // 2, y0 + 48), label, fill=MUTED, font=fnt(24), anchor="mm")
        draw.text((x0 + gw // 2, y0 + 100), val, fill=NAVY, font=fnt(36, True), anchor="mm")

    y2 = y + 2 * (gh + 18) + 28
    rounded(draw, (48, y2, W - 48, y2 + 220), NAVY, radius=22)
    draw.text((W // 2, y2 + 42), "點解有人留意？", fill=GOLD, font=fnt(30, True), anchor="mm")
    for i, line in enumerate(
        [
            "利用銀行體系賺息差，唔係單純擺定期",
            "適合可鎖定 5 年、追求穩健參考回報",
            "唔係人人啱——要睇資金年期同風險承受",
        ]
    ):
        draw.text((80, y2 + 88 + i * 52), f"✓  {line}", fill=WHITE, font=fnt(26))

    y3 = y2 + 248
    rounded(draw, (48, y3, W - 48, y3 + 120), TEAL, radius=22)
    draw.text((W // 2, y3 + 38), "想了解啱唔啱你？", fill=WHITE, font=fnt(30, True), anchor="mm")
    draw.text((W // 2, y3 + 82), "message 我 · reply「息差」", fill=WHITE, font=fnt(28), anchor="mm")

    disc = (
        "*僅供參考；投資涉及風險，回報非保證。\n"
        "實際回報視乎產品條款、市場及銀行安排，以正式文件為準。"
    )
    center(draw, (56, H - 100), disc, fnt(20), MUTED, W - 112)

    img.save(OUT, quality=95)
    print(f"Saved {OUT}")


if __name__ == "__main__":
    build()
