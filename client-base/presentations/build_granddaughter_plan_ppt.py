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
        Inches(2.2),
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
            Inches(3.5),
            Inches(8.4),
            Inches(1.5),
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
        add_textbox(slide, Inches(0.6), Inches(1.15), Inches(8.8), Inches(0.5), subtitle, size=16, color=MUTED)


def add_bullets(slide, items, top=Inches(1.9), size=20, color=GRAY):
    y = top
    for item in items:
        add_textbox(slide, Inches(0.75), y, Inches(8.5), Inches(0.65), f"• {item}", size=size, color=color)
        y += Inches(0.72)


def add_table_slide(prs, title, headers, rows, subtitle=""):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_section_header(slide, title, subtitle)
    rows_n = len(rows) + 1
    cols_n = len(headers)
    tbl = slide.shapes.add_table(rows_n, cols_n, Inches(0.5), Inches(1.85), Inches(9), Inches(4.8)).table

    for c, h in enumerate(headers):
        cell = tbl.cell(0, c)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = NAVY
        for p in cell.text_frame.paragraphs:
            p.font.bold = True
            p.font.size = Pt(13)
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
                p.font.size = Pt(12)
                p.font.name = "Microsoft JhengHei"
                p.alignment = PP_ALIGN.CENTER


def main():
    prs = Presentation()
    prs.slide_width = Inches(10)
    prs.slide_height = Inches(7.5)

    # 1 Title
    add_title_slide(
        prs,
        "為孫女準備的一份長遠心意",
        "寰御安心環球終身保險計劃｜一次性預繳 HK$150,000\n建議書日期：2026年6月4日",
    )

    # 2 Grandfather story
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_section_header(slide, "爺爺的心意：為孫女鋪路未來", "Male client 60+ · 希望為 9 歲孫女建立儲蓄與保障")
    add_bullets(
        slide,
        [
            "您希望以一次過資金，為孫女建立長線儲蓄，減輕日後供款壓力",
            "孫女現年 9 歲，保障年期長，時間複利可發揮更大作用",
            "即使爺爺不在身邊，保單仍可延續保障與財富傳承安排",
            "預繳保費後，5 年內無需再操心每年繳費",
        ],
        top=Inches(2.0),
        size=19,
    )

    # 3 Plan overview
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_section_header(slide, "方案概覽", "中銀集團人壽保險有限公司")
    add_bullets(
        slide,
        [
            "基本計劃：寰御安心環球終身保險計劃（港元）",
            "兼備人壽保障、儲蓄增值與財富傳承功能",
            "週年紅利（非保證）＋終期紅利（非保證）",
            "保費繳費年期：5 年｜保障年期：終身",
        ],
        top=Inches(2.0),
    )

    # 4 Insured
    add_table_slide(
        prs,
        "受保人資料（建議書）",
        ["項目", "內容"],
        [
            ["與您的關係", "孫女（擬受保人）"],
            ["年齡 / 性別", "9 歲 / 女（非吸煙者）"],
            ["保障年期", "終身"],
            ["保單貨幣", "港元（HKD）"],
            ["名義金額", "161,022"],
        ],
        "保單權益人：Vip 先生｜申請人",
    )

    # 5 Premium / prepaid
    add_table_slide(
        prs,
        "供款安排：一次性預繳 HK$150,000",
        ["項目", "金額（港元）"],
        [
            ["每年保費（標準）", "32,204.40"],
            ["5 年總保費（已繳總保費）", "161,022"],
            ["優惠後預繳保費總額", "149,849.62"],
            ["優惠後預繳保費總額及徵費", "150,000.10"],
            ["預繳保費戶口保證年利率", "3.50%"],
        ],
        "推廣：寰御安心環球終身保險計劃保費折扣（至 2026-06-30）",
    )

    # 6 Why age 9
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_section_header(slide, "為什麼 9 歲開始特別合適？", "長線規劃角度")
    add_bullets(
        slide,
        [
            "供款期僅 5 年，爺爺在退休前後可一次過完成責任",
            "孫女仍有很長人生路，非保證紅利有較長時間滾存",
            "可預留「更改受保人」「後備受保人」作日後傳承",
            "日後孫女長大，可按需要作保單分拆或貨幣轉換（如適用）",
        ],
        top=Inches(2.0),
    )

    # 7 Highlights
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_section_header(slide, "計劃重點（與儲蓄＋傳承相關）", "")
    add_bullets(
        slide,
        [
            "週年紅利（非保證）：可積存生息或提取",
            "終期紅利（非保證）：退保或身故時可獲派",
            "更改受保人：可把保障延續予下一代",
            "後備受保人：現受保人身故後，可指定後備受保人承接",
            "「智富長傳」預設保單指示：可預設身故賠償如何分配予受益人",
            "保費延繳保障、安心2gether 精神上無行為能力保障",
        ],
        top=Inches(1.95),
        size=17,
    )

    # 8 Cash value milestones for granddaughter
    add_table_slide(
        prs,
        "孫女成長里程碑｜預期現金價值總額（說明摘要）",
        ["孫女年齡", "保單年度", "已繳總保費", "預期現金價值總額*"],
        [
            ["14 歲", "5", "161,022", "286,059"],
            ["19 歲", "10", "161,022", "434,249"],
            ["24 歲", "15", "161,022", "606,259"],
            ["29 歲", "20", "161,022", "825,491"],
            ["34 歲", "25", "161,022", "1,106,259"],
            ["65 歲", "56", "161,022", "3,752,770"],
        ],
        "*含非保證週年紅利及終期紅利；實際或較高或較低",
    )

    # 9 At age 65 illustration from PDF
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_section_header(slide, "長遠參考：受保人 65 歲保單週年日", "非保證；僅作說明摘要演示")
    add_textbox(
        slide,
        Inches(0.7),
        Inches(1.9),
        Inches(8.6),
        Inches(1.2),
        "預期現金價值總額約 HK$3,752,770（已繳總保費 HK$161,022）\n"
        "約為已繳總保費的 23.3 倍*",
        size=22,
        bold=True,
        color=GREEN,
    )
    add_textbox(
        slide,
        Inches(0.7),
        Inches(3.3),
        Inches(8.6),
        Inches(2.5),
        "此數字包含保證現金價值、累積週年紅利（非保證）及終期紅利（非保證）。"
        "紅利並非保證，可升可跌，過往表現不代表將來。",
        size=16,
        color=MUTED,
    )

    # 10 Prepaid account
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_section_header(slide, "預繳保費戶口（配合您的一次過供款）", "")
    add_bullets(
        slide,
        [
            "您打算一次過預繳約 HK$150,000（含徵費後約 HK$150,000.10）",
            "每年保費及徵費於保單週年日從預繳戶口自動扣除",
            "基本計劃預繳餘額以保證年利率 3.50% 積存生息",
            "第 5 個保單年度後預繳戶口餘額為 0，之後無需再繳費",
            "提早退保或提取預繳餘額可能須付預繳保費退回費用（現行 6%）",
        ],
        top=Inches(2.0),
        size=18,
    )

    # 11 Warnings
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_section_header(slide, "重要提示", "請與爺爺充分溝通風險")
    add_bullets(
        slide,
        [
            "除非有意就全期 5 年繳清保費，否則不應投保",
            "提早退保或停止供款可能蒙受重大損失",
            "非保證利益（週年紅利、終期紅利）可為零或調整",
            "建議書有效期 30 日（2026年6月4日起）",
            "此簡報僅供說明，以保單條款及正式建議書為準",
        ],
        top=Inches(2.0),
        size=17,
        color=RGBColor(0x9B, 0x2C, 0x2C),
    )

    # 12 Next steps
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(slide, NAVY)
    add_textbox(
        slide,
        Inches(0.6),
        Inches(1.8),
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
            "確認孫女為受保人、您為保單權益人及受益人安排",
            "確認一次過預繳金額及5年供款意願",
            "完成投保申請及健康告知",
            "保單生效後，定期檢視週年紅利與保單價值",
        ],
        top=Inches(3.2),
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
        "建議書編號：131HK0520260604094001（中銀人壽正式建議書）",
        size=16,
        color=GOLD,
        align=PP_ALIGN.CENTER,
    )

    prs.save(OUT)
    print(f"Saved {OUT}")


if __name__ == "__main__":
    main()
