#!/usr/bin/env python3
"""
Generate 俊才坊 logo, summer poster, and A4 flyer with pricing and discounts.
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

BASE = Path(__file__).parent
OUTPUT = BASE / "output"
OUTPUT.mkdir(parents=True, exist_ok=True)

# Brand palette
NAVY = (30, 58, 95)
GOLD = (212, 168, 67)
LIGHT_GOLD = (245, 230, 190)
WHITE = (255, 255, 255)
CREAM = (252, 249, 243)
SOFT_BLUE = (232, 240, 250)
RED = (200, 50, 50)
DARK = (35, 45, 60)
MUTED = (100, 110, 125)


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    paths = [
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc" if bold else "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc" if bold else "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
    ]
    for p in paths:
        if Path(p).exists():
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def draw_rounded_rect(draw, box, radius, fill=None, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def draw_logo(size: int = 800) -> Image.Image:
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    cx, cy = size // 2, size // 2

    # Outer ring
    pad = size * 0.08
    draw.ellipse((pad, pad, size - pad, size - pad), fill=NAVY + (255,))

    # Inner cream circle
    inner = size * 0.14
    draw.ellipse((inner, inner, size - inner, size - inner), fill=CREAM + (255,))

    # Open book shape
    book_w = size * 0.38
    book_h = size * 0.28
    bx0 = cx - book_w / 2
    by0 = cy - book_h * 0.15
    bx1 = cx + book_w / 2
    by1 = by0 + book_h
    draw.polygon(
        [
            (bx0, by1),
            (cx, by0 + book_h * 0.2),
            (bx1, by1),
            (bx1, by0 + book_h * 0.55),
            (cx, by0),
            (bx0, by0 + book_h * 0.55),
        ],
        fill=WHITE + (255,),
        outline=GOLD + (255,),
        width=max(2, size // 200),
    )

    # Book spine line
    draw.line([(cx, by0), (cx, by1)], fill=GOLD + (255,), width=max(2, size // 180))

    # Star / talent sprout
    star_y = by0 - size * 0.12
    star_r = size * 0.055
    points = []
    for i in range(10):
        angle = i * 36 - 90
        import math

        rad = math.radians(angle)
        r = star_r if i % 2 == 0 else star_r * 0.45
        points.append((cx + r * math.cos(rad), star_y + r * math.sin(rad)))
    draw.polygon(points, fill=GOLD + (255,))

    # Chinese name (below emblem, outside inner circle)
    name_font = font(int(size * 0.11), bold=True)
    sub_font = font(int(size * 0.042), bold=True)
    draw.text((cx, size * 0.78), "俊才坊", fill=NAVY + (255,), font=name_font, anchor="mm")
    draw.text((cx, size * 0.88), "培育俊才 · 成就未來", fill=MUTED + (255,), font=sub_font, anchor="mm")

    return img


def draw_header_band(draw, w: int, y: int, h: int, title: str, subtitle: str):
    draw.rectangle((0, y, w, y + h), fill=NAVY)
    draw.rectangle((0, y + h - 8, w, y + h), fill=GOLD)
    draw.text((w // 2, y + h * 0.32), title, fill=WHITE, font=font(52, True), anchor="mm")
    draw.text((w // 2, y + h * 0.68), subtitle, fill=LIGHT_GOLD, font=font(26), anchor="mm")


def draw_discount_badges(draw, w: int, y: int):
    badges = [
        ("舊生 9 折", NAVY),
        ("早鳥減 $300", GOLD),
        ("二人同行各減 $200", NAVY),
        ("舊生帶新生半價", GOLD),
    ]
    gap = 16
    badge_h = 52
    total_w = w - 80
    badge_w = (total_w - gap * 3) // 4
    x = 40
    for text, color in badges:
        fg = WHITE if color == NAVY else NAVY
        draw_rounded_rect(draw, (x, y, x + badge_w, y + badge_h), 10, fill=color)
        draw.text((x + badge_w // 2, y + badge_h // 2), text, fill=fg, font=font(20, True), anchor="mm")
        x += badge_w + gap


def draw_course_card(draw, x, y, w, h, title, price, original, details, accent=NAVY):
    draw_rounded_rect(draw, (x, y, x + w, y + h), 16, fill=WHITE, outline=accent, width=2)
    draw_rounded_rect(draw, (x, y, x + w, y + 44), 16, fill=accent)
    draw.rectangle((x, y + 30, x + w, y + 44), fill=accent)
    draw.text((x + 16, y + 22), title, fill=WHITE, font=font(22, True), anchor="lm")
    draw.text((x + 16, y + 62), details, fill=MUTED, font=font(17), anchor="la")
    if original:
        draw.text((x + w - 16, y + 62), original, fill=MUTED, font=font(16), anchor="ra")
        # strikethrough
        tw = draw.textlength(original, font=font(16))
        draw.line((x + w - 16 - tw, y + 70, x + w - 16, y + 70), fill=MUTED, width=1)
    draw.text((x + 16, y + h - 20), price, fill=RED, font=font(28, True), anchor="lb")


def build_poster() -> Image.Image:
    w, h = 1080, 1520
    img = Image.new("RGB", (w, h), CREAM)
    draw = ImageDraw.Draw(img)

    draw_header_band(draw, w, 0, 200, "俊才坊補習社", "2026 暑期課程 · 現正招生")

    # Logo inset
    logo = draw_logo(220).convert("RGBA")
    img.paste(logo, (40, 220), logo)

    # Hero text
    draw.text((290, 250), "功課輔導穩根基", fill=NAVY, font=font(38, True))
    draw.text((290, 305), "DSE 精讀創佳績 · 升班銜接贏起跑", fill=DARK, font=font(26))
    draw_rounded_rect(draw, (290, 360, 700, 410), 8, fill=GOLD)
    draw.text((495, 385), "教育局註冊補習社 · 小班教學 8–12 人", fill=NAVY, font=font(20, True), anchor="mm")

    draw_discount_badges(draw, w, 460)

    # Course cards - row 1
    y0 = 540
    cw, ch, gap = 490, 175, 20
    draw_course_card(
        draw, 40, y0, cw, ch,
        "小學功課輔導營（4週）",
        "優惠價 $1,392 起",
        "原價 $1,880",
        "小一至小六 · 上午 9am–12pm\n升班預習 + 暑期功課督導",
    )
    draw_course_card(
        draw, 40 + cw + gap, y0, cw, ch,
        "DSE 暑期精讀班（4週）",
        "優惠價 $2,112/科 起",
        "原價 $2,680/科",
        "中四至中六 · 下午 2pm–5pm\nPast Paper 操卷 + 試題拆解",
        accent=(50, 90, 140),
    )

    # row 2
    y1 = y0 + ch + gap
    draw_course_card(
        draw, 40, y1, cw, ch,
        "升班銜接課程（4週）",
        "優惠價 $1,612 起",
        "原價 $2,180",
        "小六升中一 / 中三升中四\n中英數銜接 · 下午班",
    )
    draw_course_card(
        draw, 40 + cw + gap, y1, cw, ch,
        "日間託管加強班（4週）",
        "優惠價 $2,652 起",
        "原價 $3,280",
        "9am–6pm · 雙職家庭首選\n上午學習 + 下午輔導",
        accent=(50, 90, 140),
    )

    # row 3 - smaller cards
    y2 = y1 + ch + gap
    sw = (w - 80 - gap * 2) // 3
    small = [
        ("中學功課輔導", "$1,264 起", "原 $1,580", "傍晚 6–8pm"),
        ("STEM 科學班", "$704 起", "原 $880", "週六 2–4pm"),
        ("創意美術班", "$624 起", "原 $780", "週日 10am–12pm"),
    ]
    x = 40
    for title, price, orig, det in small:
        draw_rounded_rect(draw, (x, y2, x + sw, y2 + 130), 12, fill=SOFT_BLUE, outline=NAVY, width=1)
        draw.text((x + 14, y2 + 16), title, fill=NAVY, font=font(20, True))
        draw.text((x + 14, y2 + 48), det, fill=MUTED, font=font(16))
        draw.text((x + 14, y2 + 78), orig, fill=MUTED, font=font(15))
        draw.text((x + 14, y2 + 100), price, fill=RED, font=font(24, True))
        x += sw + gap

    # Discount explainer
    y3 = y2 + 155
    draw_rounded_rect(draw, (40, y3, w - 40, y3 + 200), 16, fill=NAVY)
    draw.text((w // 2, y3 + 30), "優惠疊加示例（舊生 + 早鳥）", fill=GOLD, font=font(24, True), anchor="mm")
    lines = [
        "① 舊生報讀任何暑期課程享 9 折",
        "② 6 月 30 日前報名，每科額外減 $300",
        "③ 二人同行各減 $200 ｜ 舊生帶新生首月半價",
        "④ 報讀 2 科或以上額外 95 折 ｜ 兩期連報第二期減 $500",
    ]
    ly = y3 + 60
    for line in lines:
        draw.text((70, ly), line, fill=WHITE, font=font(20))
        ly += 34

    # Footer CTA
    y4 = y3 + 220
    draw_rounded_rect(draw, (40, y4, w - 40, y4 + 120), 16, fill=GOLD)
    draw.text((w // 2, y4 + 35), "立即報名 · 名額有限", fill=NAVY, font=font(36, True), anchor="mm")
    draw.text((w // 2, y4 + 80), "WhatsApp: XXXX XXXX  ｜  早鳥截止：2026 年 6 月 30 日", fill=NAVY, font=font(22), anchor="mm")

    draw.text((w // 2, h - 30), "俊才坊補習社 · 培育俊才，成就未來", fill=MUTED, font=font(18), anchor="mm")

    return img


def build_flyer() -> Image.Image:
    """A4 portrait flyer at 150dpi-ish (1240 x 1754)."""
    w, h = 1240, 1754
    img = Image.new("RGB", (w, h), WHITE)
    draw = ImageDraw.Draw(img)

    # Top banner
    draw.rectangle((0, 0, w, 280), fill=NAVY)
    draw.rectangle((0, 270, w, 280), fill=GOLD)

    logo = draw_logo(180).convert("RGBA")
    img.paste(logo, (50, 50), logo)

    draw.text((260, 80), "俊才坊補習社", fill=WHITE, font=font(56, True))
    draw.text((260, 150), "2026 暑期課程傳單", fill=LIGHT_GOLD, font=font(32))
    draw.text((260, 210), "功課輔導 · DSE 精讀 · 升班銜接 · 日間託管 · 興趣班", fill=WHITE, font=font(22))

    # Discount strip
    y = 300
    draw_rounded_rect(draw, (40, y, w - 40, y + 90), 12, fill=(255, 240, 240), outline=RED, width=2)
    draw.text((w // 2, y + 30), "限時優惠", fill=RED, font=font(30, True), anchor="mm")
    draw.text(
        (w // 2, y + 62),
        "舊生 9 折 ｜ 早鳥減 $300（6/30 前）｜ 二人同行各減 $200 ｜ 舊生帶新生半價",
        fill=DARK,
        font=font(20),
        anchor="mm",
    )

    # Course table header
    y = 420
    draw_rounded_rect(draw, (40, y, w - 40, y + 50), 8, fill=NAVY)
    cols = [300, 480, 200, 180]
    headers = ["課程", "時間 / 對象", "原價", "優惠價"]
    x = 50
    for header, col_w in zip(headers, cols):
        draw.text((x + col_w // 2, y + 25), header, fill=WHITE, font=font(20, True), anchor="mm")
        x += col_w

    courses = [
        ("小學功課輔導營（4週）", "小一至小六 · 上午 9–12", "$1,880", "$1,392 起"),
        ("小學升班預習班（4週）", "小四至小六 · 上午 9–12", "$1,880", "$1,392 起"),
        ("日間託管加強班（4週）", "小一至小六 · 9am–6pm", "$3,280", "$2,652 起"),
        ("升班銜接課程（4週）", "小六升中一 / 中三升中四", "$2,180", "$1,612 起"),
        ("DSE 暑期精讀班（4週/科）", "中四至中六 · 下午 2–5", "$2,680", "$2,112 起"),
        ("DSE 兩科套餐（4週）", "中四至中六 · 自選兩科", "$4,880", "$3,852 起"),
        ("中學功課輔導（4週）", "中一至中三 · 傍晚 6–8", "$1,580", "$1,264 起"),
        ("STEM 科學實驗班（4堂）", "小學 · 週六 2–4pm", "$880", "$704 起"),
        ("創意美術班（4堂）", "小學 · 週日 10am–12pm", "$780", "$624 起"),
        ("程式邏輯入門（4堂）", "小學 · 週日 2–4pm", "$980", "$784 起"),
    ]

    row_h = 52
    y += 50
    for i, (name, time, orig, disc) in enumerate(courses):
        bg = CREAM if i % 2 == 0 else WHITE
        draw.rectangle((40, y, w - 40, y + row_h), fill=bg)
        x = 50
        values = [name, time, orig, disc]
        for val, col_w in zip(values, cols):
            color = RED if col_w == 180 else DARK
            weight = True if col_w == 180 else False
            draw.text((x + 8, y + row_h // 2), val, fill=color, font=font(18, weight), anchor="lm")
            x += col_w
        y += row_h

    # Border around table
    draw.rectangle((40, 420, w - 40, y), outline=NAVY, width=2)

    # Regular courses section
    y += 30
    draw.text((50, y), "常規課程（9 月學期）", fill=NAVY, font=font(28, True))
    y += 45
    regular = [
        "小學功課輔導（每日）$1,680/月 ｜ 每週 3 日 $1,280/月",
        "中學功課輔導（每日）$2,180/月 ｜ 每週 3 日 $1,680/月",
        "DSE 專科班 $980/科/月 ｜ 三科套餐 $2,580/月",
        "1對1 VIP $380/堂 ｜ 1對2 $280/人/堂",
    ]
    for line in regular:
        draw.text((60, y), f"• {line}", fill=DARK, font=font(19))
        y += 32

    # Why us
    y += 20
    draw_rounded_rect(draw, (40, y, w - 40, y + 160), 12, fill=SOFT_BLUE)
    draw.text((60, y + 20), "俊才坊優勢", fill=NAVY, font=font(24, True))
    perks = [
        "✓  教育局註冊補習社，持牌經營",
        "✓  本區名校 Past Paper 獨家操練",
        "✓  小班教學 8–12 人，資深導師親自督導",
        "✓  1,000 呎舒適校舍，多用途 VIP 輔導室",
    ]
    py = y + 55
    for perk in perks:
        draw.text((70, py), perk, fill=DARK, font=font(19))
        py += 28

    # Footer
    y += 185
    draw_rounded_rect(draw, (40, y, w - 40, y + 130), 12, fill=NAVY)
    draw.text((w // 2, y + 35), "立即報名", fill=GOLD, font=font(34, True), anchor="mm")
    draw.text((w // 2, y + 80), "WhatsApp: XXXX XXXX", fill=WHITE, font=font(28), anchor="mm")
    draw.text((w // 2, y + 115), "地址：[請填寫]  ｜  查詢：一至六 10am–8pm", fill=LIGHT_GOLD, font=font(20), anchor="mm")

    draw.text((w // 2, h - 25), "優惠不可與其他推廣同時使用（舊生帶新生半價除外）· 俊才坊保留最終解釋權", fill=MUTED, font=font(14), anchor="mm")

    return img


def main():
    logo = draw_logo(1024)
    logo_path = OUTPUT / "jun-caifang-logo.png"
    logo.save(logo_path, "PNG")

    # White background version for print
    logo_white = Image.new("RGBA", (1024, 1024), WHITE + (255,))
    logo_white.paste(logo, (0, 0), logo)
    logo_white.convert("RGB").save(OUTPUT / "jun-caifang-logo-white-bg.png", "PNG")

    poster = build_poster()
    poster.save(OUTPUT / "jun-caifang-summer-poster.png", "PNG", quality=95)

    flyer = build_flyer()
    flyer.save(OUTPUT / "jun-caifang-summer-flyer.png", "PNG", quality=95)

    print("Generated:")
    for p in sorted(OUTPUT.glob("*.png")):
        im = Image.open(p)
        print(f"  {p} ({im.width}x{im.height})")


if __name__ == "__main__":
    main()
