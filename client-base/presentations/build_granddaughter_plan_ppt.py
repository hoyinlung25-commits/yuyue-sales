#!/usr/bin/env python3
"""Build PowerPoint: savings plan for granddaughter (from BOC proposal PDF)."""

from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt

OUT = Path(__file__).parent / "Granddaughter_Savings_Plan_BOC.pptx"

NAVY = RGBColor(0x1A, 0x36, 0x5D)
GOLD = RGBColor(0xD6, 0x9E, 0x2E)
GREEN = RGBColor(0x05, 0x96, 0x69)
LIGHT = RGBColor(0xF0, 0xFD, 0xF4)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
GRAY = RGBColor(0x4A, 0x55, 0x68)
MUTED = RGBColor(0x71, 0x85, 0x90)

TOTAL_PREMIUM = 161_022

# From BOC proposal 說明摘要 (insured age 9 at issue)
LIFE_STAGES = [
    ("供款完成 · 中學", "14", "5", 67_264, "保費已繳清，保單靜靜為她滾存"),
    ("升學進修（DSE／大專）", "19", "10", 200_527, "進修、海外交流或生活開支補助"),
    ("大學畢業 · 初入職場", "24", "15", 286_059, "畢業旅行、進修或創業起步資金"),
    ("事業穩定 · 置業首期", "29", "20", 434_249, "買樓首期、進修專業資格"),
    ("結婚成家", "34", "25", 606_259, "婚禮、蜜月或新婚置業"),
    ("育兒 · 家庭責任", "39", "30", 825_491, "子女教育、家庭醫療或生活儲備"),
    ("事業發展 · 創業支援", "44", "35", 1_104_542, "創業資金、生意周轉（需按保單條款提取）"),
    ("退休規劃參考", "65", "56", 3_752_770, "長線退休或傳承下一代"),
]


def fmt_hkd(n: int) -> str:
    return f"{n:,}"


def return_multiple(cash: int) -> str:
    mult = cash / TOTAL_PREMIUM
    return f"{mult:.2f} 倍"


def set_bg(slide, color: RGBColor) -> None:
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = color


def add_textbox(
    slide,
    left,
    top,
    width,
    height,
    text,
    size=18,
    bold=False,
    color=GRAY,
    align=PP_ALIGN.LEFT,
    font_name="Microsoft JhengHei",
):
    box = slide.shapes.add_textbox(left, top, width, height)
    tf = box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(size)
    p.font.bold = bold
    p.font.color.rgb = color
    p.font.name = font_name
    p.alignment = align
    return box


def add_title_slide(prs, title, subtitle=""):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(slide, NAVY)
    add_textbox(
        slide,
        Inches(0.6),
        Inches(2.0),
        Inches(8.8),
        Inches(1.2),
        title,
        size=40,
        bold=True,
        color=WHITE,
        align=PP_ALIGN.CENTER,
    )
    if subtitle:
        add_textbox(
            slide,
            Inches(0.8),
            Inches(3.3),
            Inches(8.4),
            Inches(1.6),
            subtitle,
            size=20,
            color=RGBColor(0xD1, 0xFA, 0xE5),
            align=PP_ALIGN.CENTER,
        )
    add_textbox(
        slide,
        Inches(0.6),
        Inches(6.8),
        Inches(8.8),
        Inches(0.5),
        "中銀集團人壽 · 寰御安心環球終身保險計劃",
        size=14,
        color=GOLD,
        align=PP_ALIGN.CENTER,
    )


def add_section_header(slide, title, subtitle=""):
    set_bg(slide, LIGHT)
    bar = slide.shapes.add_shape(1, Inches(0), Inches(0), Inches(10), Inches(0.12))
    bar.fill.solid()
    bar.fill.fore_color.rgb = GOLD
    bar.line.fill.background()
    add_textbox(slide, Inches(0.6), Inches(0.45), Inches(8.8), Inches(0.7), title, size=32, bold=True, color=NAVY)
    if subtitle:
        add_textbox(slide, Inches(0.6), Inches(1.15), Inches(8.8), Inches(0.55), subtitle, size=16, color=MUTED)


def add_bullets(slide, items, top=Inches(1.9), size=20, color=GRAY):
    y = top
    for item in items:
        add_textbox(slide, Inches(0.75), y, Inches(8.5), Inches(0.7), f"• {item}", size=size, color=color)
        y += Inches(0.68)


def add_table_slide(prs, title, headers, rows, subtitle="", table_top=Inches(1.85), table_height=Inches(4.9)):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_section_header(slide, title, subtitle)
    rows_n = len(rows) + 1
    cols_n = len(headers)
    tbl = slide.shapes.add_table(rows_n, cols_n, Inches(0.35), table_top, Inches(9.3), table_height).table

    for c, h in enumerate(headers):
        cell = tbl.cell(0, c)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = NAVY
        for p in cell.text_frame.paragraphs:
            p.font.bold = True
            p.font.size = Pt(11)
            p.font.color.rgb = WHITE
            p.font.name = "Microsoft JhengHei"
            p.alignment = PP_ALIGN.CENTER

    for r, row in enumerate(rows, start=1):
        for c, val in enumerate(row):
            cell = tbl.cell(r, c)
            cell.text = str(val)
            if r % 2 == 0:
                cell.fill.solid()
                cell.fill.fore_color.rgb = WHITE
            for p in cell.text_frame.paragraphs:
                p.font.size = Pt(10)
                p.font.name = "Microsoft JhengHei"
                p.alignment = PP_ALIGN.CENTER


def main():
    prs = Presentation()
    prs.slide_width = Inches(10)
    prs.slide_height = Inches(7.5)

    add_title_slide(
        prs,
        "爺爺為 9 歲孫女\n準備的長遠儲蓄心意",
        "寰御安心環球終身保險計劃｜一次性預繳約 HK$150,000\n"
        "按孫女人生階段，看保單如何為她累積資金",
    )

    # Why 寰御安心 for granddaughter savings
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_section_header(
        slide,
        "為什麼為孫女選擇「寰御安心環球終身」？",
        "儲蓄 + 終身保障 + 跨代傳承，一次過預繳完成責任",
    )
    add_bullets(
        slide,
        [
            "孫女儲蓄：以受保人身份投保，紅利在長年期內滾存，配合她由升學到置業的人生節奏",
            "爺爺一次過預繳約 HK$150,000，5 年保費責任完結，無需年年操心繳費",
            "兼備人壽保障：即使爺爺或孫女遇上人生變故，保單仍可延續安排",
            "可更改受保人／後備受保人：日後可把保單傳給她的子女，財富跨代延續",
            "週年紅利 + 終期紅利（非保證）：為日後提取、退保或傳承提供彈性",
        ],
        top=Inches(1.95),
        size=18,
    )

    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_section_header(slide, "爺爺的心意", "60+ 男客 · 為 9 歲孫女建立專屬儲蓄保單")
    add_bullets(
        slide,
        [
            "您現時有能力，希望趁孫女尚小，為她預留一筆會隨時間增長的資產",
            "保單以孫女為受保人，權益人為您；日後可按需要調整受益人及傳承安排",
            "重點不是短期回報，而是覆蓋她畢業、工作、結婚、育兒、買樓、創業等人生階段",
            "預繳完成後，這份保單會一直陪伴她成長，成為爺孫之間的一份具體心意",
        ],
        top=Inches(2.0),
        size=19,
    )

    add_table_slide(
        prs,
        "供款安排（建議書）",
        ["項目", "內容"],
        [
            ["受保人", "孫女 · 9 歲 · 女（非吸煙）"],
            ["保費繳費年期", "5 年（已繳總保費 HK$161,022）"],
            ["爺爺一次過預繳", "約 HK$150,000.10（含徵費）"],
            ["預繳戶口保證年利率", "3.50%"],
        ],
        table_height=Inches(3.2),
    )

    # Life stage roadmap - main table
    stage_rows = []
    for stage, age, year, cash, use in LIFE_STAGES:
        stage_rows.append(
            [
                stage,
                f"{age} 歲",
                f"第 {year} 年",
                f"HK$ {fmt_hkd(cash)}",
                return_multiple(cash),
            ]
        )

    add_table_slide(
        prs,
        "孫女人生階段 × 保單回報參考",
        ["人生階段", "孫女年齡", "保單年度", "預期現金價值總額*", "相對已繳保費"],
        stage_rows,
        "*非保證；含週年紅利及終期紅利。第 15 保單年度預期現金價值 HK$286,059（建議書）",
        table_top=Inches(1.78),
        table_height=Inches(5.0),
    )

    # Detailed life stage uses
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_section_header(
        slide,
        "各人生階段，這筆資金可以支援什麼？",
        "數字來自建議書「說明摘要」；實際提取須符合保單條款",
    )
    add_bullets(
        slide,
        [
            "19 歲（第 10 年）約 HK$200,527：DSE 後升學、大專生活費或進修",
            "24 歲（第 15 年）約 HK$286,059：大學畢業、初入職或小型創業起步",
            "29 歲（第 20 年）約 HK$434,249：事業穩定、買樓首期或進修專業資格",
            "34 歲（第 25 年）約 HK$606,259：結婚、新婚置業或家庭開支",
            "39 歲（第 30 年）約 HK$825,491：育兒、子女教育或家庭醫療儲備",
            "44 歲（第 35 年）約 HK$1,106,259：事業擴張、創業周轉或進一步置業",
        ],
        top=Inches(1.88),
        size=17,
    )

    # Highlight year 15 correction
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_section_header(slide, "重點參考：第 15 保單年度", "孫女約 24 歲 · 大學畢業／初入職場")
    add_textbox(
        slide,
        Inches(0.65),
        Inches(1.85),
        Inches(8.7),
        Inches(1.4),
        "預期現金價值總額\nHK$ 286,059",
        size=36,
        bold=True,
        color=GREEN,
        align=PP_ALIGN.CENTER,
    )
    add_textbox(
        slide,
        Inches(0.65),
        Inches(3.35),
        Inches(8.7),
        Inches(2.8),
        "建議書顯示：第 15 個保單年度（非第 5 年）現金價值總額約 HK$286,059。\n"
        f"已繳總保費 HK$161,022，約為 {return_multiple(286_059)}。\n\n"
        "此階段正值畢業與踏入社會，可作進修、創業或生活儲備的參考金額。\n"
        "紅利非保證，實際金額可升可跌。",
        size=17,
        color=GRAY,
        align=PP_ALIGN.CENTER,
    )

    # Buy house / business focus
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_section_header(slide, "買樓 · 創業 · 成家 — 回報對照", "保單年度與預期現金價值總額（建議書）")
    add_bullets(
        slide,
        [
            "買樓首期參考：第 20 年（29 歲）約 HK$434,249 · 約 2.7 倍已繳保費",
            "結婚成家參考：第 25 年（34 歲）約 HK$606,259 · 約 3.8 倍",
            "育兒家庭參考：第 30 年（39 歲）約 HK$825,491 · 約 5.1 倍",
            "創業／生意周轉參考：第 35 年（44 歲）約 HK$1,104,542 · 約 6.9 倍",
            "提取方式：部分退保、紅利提取或保單貸款等，須按條款及當時保單價值",
        ],
        top=Inches(1.95),
        size=18,
    )

    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_section_header(slide, "計劃功能（配合孫女長線儲蓄）", "")
    add_bullets(
        slide,
        [
            "週年紅利（非保證）：可積存生息，日後按人生需要提取",
            "終期紅利（非保證）：退保或身故時派發，長線增值主力",
            "更改受保人：孫女長大後可傳予下一代，保單繼續生效",
            "保單分拆、貨幣轉換（如適用）：配合移民、置業或多元配置",
            "「智富長傳」：可預設身故賠償分期給受益人，避免一次過揮霍",
        ],
        top=Inches(1.95),
        size=17,
    )

    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_section_header(slide, "長遠參考：孫女 65 歲", "第 56 保單年度 · 非保證演示")
    add_textbox(
        slide,
        Inches(0.7),
        Inches(1.9),
        Inches(8.6),
        Inches(1.3),
        "預期現金價值總額約 HK$3,752,770\n"
        "約為已繳總保費的 23.3 倍*",
        size=24,
        bold=True,
        color=GREEN,
        align=PP_ALIGN.CENTER,
    )
    add_textbox(
        slide,
        Inches(0.7),
        Inches(3.4),
        Inches(8.6),
        Inches(2.4),
        "可作退休或再傳承予第三代之長線參考。\n"
        "過往演示不代表將來；紅利可為零或調整。",
        size=16,
        color=MUTED,
        align=PP_ALIGN.CENTER,
    )

    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_section_header(slide, "預繳保費戶口", "配合爺爺一次過 HK$150,000")
    add_bullets(
        slide,
        [
            "預繳約 HK$150,000.10 後，每年保費於保單週年日自動扣除",
            "預繳餘額以保證年利率 3.50% 積存，直至第 5 保單年度",
            "第 5 年後無需再繳費，保單繼續為孫女滾存",
            "提早退保或提取預繳餘額可能須付退回費用（現行 6%）",
        ],
        top=Inches(2.0),
        size=18,
    )

    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_section_header(slide, "重要提示", "")
    add_bullets(
        slide,
        [
            "除非有意就全期 5 年繳清保費，否則不應投保",
            "提早退保可能蒙受重大損失；非保證紅利可升可跌",
            "人生階段金額僅為建議書演示，不等同保證可取回金額",
            "建議書有效期 30 日（2026年6月4日起）",
        ],
        top=Inches(2.0),
        size=17,
        color=RGBColor(0x9B, 0x2C, 0x2C),
    )

    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(slide, NAVY)
    add_textbox(
        slide,
        Inches(0.6),
        Inches(1.6),
        Inches(8.8),
        Inches(1),
        "建議下一步",
        size=36,
        bold=True,
        color=WHITE,
        align=PP_ALIGN.CENTER,
    )
    add_bullets(
        slide,
        [
            "確認以孫女為受保人、您為保單權益人",
            "確認一次過預繳及 5 年供款意願",
            "討論各人生階段資金用途（升學、置業、成家、創業）",
            "完成投保申請；保單生效後定期檢視紅利與保單價值",
        ],
        top=Inches(2.9),
        size=19,
        color=RGBColor(0xE2, 0xE8, 0xF0),
    )
    add_textbox(
        slide,
        Inches(0.6),
        Inches(6.2),
        Inches(8.8),
        Inches(1.2),
        "保險中介人：龍浩賢｜徐語希管理組\n"
        "建議書編號：131HK0520260604094001",
        size=16,
        color=GOLD,
        align=PP_ALIGN.CENTER,
    )

    prs.save(OUT)
    print(f"Saved {OUT}")


if __name__ == "__main__":
    main()
