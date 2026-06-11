#!/usr/bin/env python3
"""Build 俊才坊行政系統 Excel workbook — Upgrade Edition v3."""

from __future__ import annotations

from datetime import date
from pathlib import Path

from openpyxl import Workbook
from openpyxl.formatting.rule import FormulaRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

OUT = Path(__file__).parent / "output"
OUT.mkdir(exist_ok=True)

NAVY, GOLD_HEX, MUTED, WHITE = "1E3A5F", "D4A843", "64748B", "FFFFFF"
SUBTITLE = "所有工作表關鍵總數 · 自動連動更新"
ALT, GREEN, RED, YELLOW, BLUE = "F8FAFC", "DCFCE7", "FEE2E2", "FEF3C7", "DBEAFE"
ORANGE = "FFEDD5"

HDR_ROW = 5
DATA_FIRST = 6
DATA_LAST = 200
TOTAL_ROW = 203

THIN = Side(style="thin", color="CBD5E0")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
GOLD_FILL = PatternFill("solid", fgColor=GOLD_HEX)
HDR_FILL = PatternFill("solid", fgColor=NAVY)
ALT_FILL = PatternFill("solid", fgColor=ALT)
TOTAL_FILL = PatternFill("solid", fgColor="FEF9C3")


def F(bold=False, size=10, color="000000"):
    return Font(name="Calibri", bold=bold, size=size, color=color)


TITLE_FONT = F(bold=True, size=14, color=NAVY)
HDR_FONT = F(bold=True, size=10, color=WHITE)
BODY = F()
FORMULA_FONT = F(color="1D4ED8")


def fill(c: str) -> PatternFill:
    return PatternFill("solid", fgColor=c)


def rng(col: str) -> str:
    return f"{col}{DATA_FIRST}:{col}{DATA_LAST}"


class SheetBuilder:
    def __init__(self, ws, title: str, subtitle: str = SUBTITLE, merge_cols: int = 10):
        self.ws = ws
        self.start = HDR_ROW
        self.merge_cols = merge_cols
        ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=merge_cols)
        ws.cell(1, 1, f"俊才坊補習社 · {title}").font = TITLE_FONT
        if subtitle:
            ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=merge_cols)
            ws.cell(2, 1, subtitle).font = F(size=10, color=MUTED)

    def headers(self, headers: list[str], widths: list[int]) -> int:
        r = self.start
        for c, h in enumerate(headers, 1):
            cell = self.ws.cell(r, c, h)
            cell.font = HDR_FONT
            cell.fill = HDR_FILL
            cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
            cell.border = BORDER
            self.ws.column_dimensions[get_column_letter(c)].width = widths[c - 1]
        self.ws.row_dimensions[r].height = 30
        return r

    def row(self, r: int, values: list, formulas: dict[int, str] | None = None, alt: bool = False):
        for c, v in enumerate(values, 1):
            cell = self.ws.cell(r, c)
            cell.value = formulas[c] if formulas and c in formulas else v
            cell.font = FORMULA_FONT if formulas and c in formulas else BODY
            cell.border = BORDER
            cell.alignment = Alignment(vertical="center", wrap_text=True)
            if alt:
                cell.fill = ALT_FILL

    def dropdown(self, col: int, options: str):
        dv = DataValidation(type="list", formula1=f'"{options}"', allow_blank=True)
        self.ws.add_data_validation(dv)
        dv.add(f"{get_column_letter(col)}{DATA_FIRST}:{get_column_letter(col)}{DATA_LAST}")

    def freeze(self):
        self.ws.freeze_panes = f"A{DATA_FIRST}"

    def cond_format(self, range_str: str, formula: str, bg: str):
        self.ws.conditional_formatting.add(range_str, FormulaRule(formula=[formula], fill=fill(bg)))

    def kpi_box(self, row: int, col: int, label: str, formula: str, width: int = 14):
        ws = self.ws
        ws.merge_cells(start_row=row, start_column=col, end_row=row, end_column=col + 1)
        ws.cell(row, col, label).font = F(bold=True, size=9, color=MUTED)
        ws.merge_cells(start_row=row + 1, start_column=col, end_row=row + 1, end_column=col + 1)
        c = ws.cell(row + 1, col, formula)
        c.font = F(bold=True, size=16, color=NAVY)
        c.alignment = Alignment(horizontal="center")
        ws.column_dimensions[get_column_letter(col)].width = width


def add_totals_block(ws, title: str, metrics: list[tuple[str, int, str, str]]):
    """
    Add standardized 總數統計 block at TOTAL_ROW.
    metrics: [(label, value_col, formula, number_format), ...]
    """
    r = TOTAL_ROW
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=4)
    c = ws.cell(r, 1, f"📊 {title}")
    c.font = F(bold=True, size=12, color=NAVY)
    c.fill = GOLD_FILL
    c.border = BORDER
    for cc in range(2, 5):
        ws.cell(r, cc).fill = GOLD_FILL
        ws.cell(r, cc).border = BORDER

    for i, (label, vcol, formula, fmt) in enumerate(metrics):
        row = r + 1 + i
        ws.cell(row, 1, label).font = F(bold=True, color=NAVY)
        ws.cell(row, 1).border = BORDER
        ws.cell(row, 1).fill = TOTAL_FILL
        for cc in range(2, vcol):
            ws.cell(row, cc).fill = TOTAL_FILL
            ws.cell(row, cc).border = BORDER
        vc = ws.cell(row, vcol, formula)
        vc.font = F(bold=True, size=11, color=NAVY)
        vc.fill = TOTAL_FILL
        vc.border = BORDER
        vc.alignment = Alignment(horizontal="right")
        if fmt:
            vc.number_format = fmt
        ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=max(2, vcol - 1))


# ─── 總數一覽 ─────────────────────────────────────────────
def sheet_totals_overview(wb: Workbook):
    ws = wb.create_sheet("總數一覽", 1)
    b = SheetBuilder(ws, "各表總數一覽", merge_cols=6)
    b.headers(["模組", "總數項目", "數值", "單位", "來源工作表", "更新方式"], [14, 22, 14, 8, 14, 18])

    items = [
        ("學生資料庫", "在讀學生總數", f'=COUNTIF(學生資料庫!{rng("R")},"在讀")', "人", "學生資料庫", "自動"),
        ("學生資料庫", "欠費學生總數", f'=COUNTIF(學生資料庫!{rng("J")},"欠費")', "人", "學生資料庫", "自動"),
        ("學生資料庫", "月費總額", f'=SUMIF(學生資料庫!{rng("R")},"在讀",學生資料庫!{rng("I")})', "港元", "學生資料庫", "自動"),
        ("學生資料庫", "欠費金額總數", f'=SUM(學生資料庫!{rng("K")})', "港元", "學生資料庫", "自動"),
        ("學生資料庫", "平均 ARPU", f'=IFERROR(AVERAGEIF(學生資料庫!{rng("R")},"在讀",學生資料庫!{rng("I")}),0)', "港元", "學生資料庫", "自動"),
        ("收費記錄", "累計應收總數", f'=SUM(收費記錄!{rng("G")})', "港元", "收費記錄", "自動"),
        ("收費記錄", "累計實收總數", f'=SUM(收費記錄!{rng("H")})', "港元", "收費記錄", "自動"),
        ("收費記錄", "累計未收總數", f'=SUM(收費記錄!{rng("I")})', "港元", "收費記錄", "自動"),
        ("收費記錄", "收款筆數", f'=COUNTA(收費記錄!{rng("A")})', "筆", "收費記錄", "自動"),
        ("收費記錄", "本月實收", f'=SUMIF(收費記錄!{rng("E")},TEXT(TODAY(),"YYYY-MM"),收費記錄!{rng("H")})', "港元", "收費記錄", "自動"),
        ("出席記錄", "出席記錄總數", f'=COUNTA(出席記錄!{rng("A")})', "筆", "出席記錄", "自動"),
        ("出席記錄", "出席人次", f'=COUNTIF(出席記錄!{rng("H")},"出席")', "次", "出席記錄", "自動"),
        ("出席記錄", "遲到人次", f'=COUNTIF(出席記錄!{rng("H")},"遲到")', "次", "出席記錄", "自動"),
        ("出席記錄", "缺席人次", f'=COUNTIF(出席記錄!{rng("H")},"缺席")', "次", "出席記錄", "自動"),
        ("排課表", "開班課程總數", f'=COUNTA(排課表!{rng("A")})', "班", "排課表", "自動"),
        ("排課表", "已報學生總數", f'=SUM(排課表!{rng("I")})', "人", "排課表", "自動"),
        ("排課表", "預估月營收總數", f'=SUM(排課表!{rng("M")})', "港元", "排課表", "自動"),
        ("排課表", "候補總數", f'=SUM(排課表!{rng("J")})', "人", "排課表", "自動"),
        ("課室使用表", "空閒時段總數", f'=COUNTIF(課室使用表!{rng("D")},"空閒")+COUNTIF(課室使用表!{rng("F")},"空閒")+COUNTIF(課室使用表!{rng("H")},"空閒")', "個", "課室使用表", "自動"),
        ("財務月結", "年度營收總數", f'=SUM(財務月結!{rng("D")})', "港元", "財務月結", "自動"),
        ("財務月結", "年度成本總數", f'=SUM(財務月結!{rng("L")})', "港元", "財務月結", "自動"),
        ("財務月結", "年度淨利總數", f'=SUM(財務月結!{rng("M")})', "港元", "財務月結", "自動"),
        ("學習進度", "進度報告總數", f'=COUNTA(學習進度!{rng("B")})', "份", "學習進度", "自動"),
        ("學習進度", "待發送總數", f'=COUNTIF(學習進度!{rng("N")},"✗")', "份", "學習進度", "自動"),
        ("每日行政", "任務總數", f'=COUNTA(每日行政!B{DATA_FIRST}:B{DATA_FIRST+19})', "項", "每日行政", "自動"),
        ("每日行政", "已完成總數", f'=COUNTIF(每日行政!C{DATA_FIRST}:C{DATA_FIRST+19},"✓")', "項", "每日行政", "自動"),
        ("家長通訊", "通訊記錄總數", f'=COUNTA(家長通訊!{rng("A")})', "則", "家長通訊", "自動"),
        ("家長通訊", "待處理總數", f'=COUNTIF(家長通訊!{rng("H")},"待處理")+COUNTIF(家長通訊!{rng("H")},"跟進中")', "則", "家長通訊", "自動"),
        ("導師資料", "在職導師總數", f'=COUNTIF(導師資料!{rng("M")},"在職")', "人", "導師資料", "自動"),
        ("導師資料", "負責學生總數", f'=SUM(導師資料!{rng("F")})', "人", "導師資料", "自動"),
        ("導師資料", "全職月薪總數", f'=SUMIF(導師資料!{rng("C")},"全職導師",導師資料!{rng("H")})', "港元", "導師資料", "自動"),
    ]
    for i, (mod, item, formula, unit, src, upd) in enumerate(items):
        r = DATA_FIRST + i
        b.row(r, [mod, item, None, unit, src, upd], {3: formula}, alt=i % 2 == 1)
        ws.cell(r, 3).number_format = "#,##0"
    b.freeze()

    add_totals_block(ws, "總數一覽 · 跨表匯總", [
        ("在讀學生總數", 3, f'=COUNTIF(學生資料庫!{rng("R")},"在讀")', "#,##0"),
        ("本月實收總數", 3, f'=SUMIF(收費記錄!{rng("E")},TEXT(TODAY(),"YYYY-MM"),收費記錄!{rng("H")})', "#,##0"),
        ("年度淨利總數", 3, f'=SUM(財務月結!{rng("M")})', "#,##0"),
        ("預估月營收總數", 3, f'=SUM(排課表!{rng("M")})', "#,##0"),
    ])


# ─── 儀表板 ───────────────────────────────────────────────
def sheet_dashboard(wb: Workbook):
    ws = wb.create_sheet("儀表板", 0)
    b = SheetBuilder(ws, "營運儀表板", merge_cols=12)
    ws.cell(4, 1, f"更新日期：{date.today().isoformat()}").font = F(size=9, color=MUTED)

    b.kpi_box(6, 1, "在讀學生", f'=COUNTIF(學生資料庫!{rng("R")},"在讀")', 12)
    b.kpi_box(6, 3, "欠費學生", f'=COUNTIF(學生資料庫!{rng("J")},"欠費")', 12)
    b.kpi_box(6, 5, "本月實收", f'=SUMIF(收費記錄!{rng("E")},TEXT(TODAY(),"YYYY-MM"),收費記錄!{rng("H")})', 14)
    b.kpi_box(6, 7, "本月應收", f'=SUMIF(收費記錄!{rng("E")},TEXT(TODAY(),"YYYY-MM"),收費記錄!{rng("G")})', 14)
    b.kpi_box(6, 9, "待跟進通訊", f'=COUNTIF(家長通訊!{rng("H")},"跟進中")+COUNTIF(家長通訊!{rng("H")},"待處理")', 12)
    b.kpi_box(6, 11, "預估月營收", f'=SUM(排課表!{rng("M")})', 12)

    ws.cell(10, 1, "各表總數速覽").font = F(bold=True, size=12, color=NAVY)
    quick = [
        ("學生月費總額", f'=SUMIF(學生資料庫!{rng("R")},"在讀",學生資料庫!{rng("I")})'),
        ("欠費金額總數", f'=SUM(學生資料庫!{rng("K")})'),
        ("出席記錄總數", f'=COUNTA(出席記錄!{rng("A")})'),
        ("收款筆數", f'=COUNTA(收費記錄!{rng("A")})'),
        ("年度淨利", f'=SUM(財務月結!{rng("M")})'),
        ("待發送進度", f'=COUNTIF(學習進度!{rng("N")},"✗")'),
    ]
    for i, (label, formula) in enumerate(quick, 11):
        ws.cell(i, 1, label).font = F(bold=True)
        c = ws.cell(i, 3, formula)
        c.font = F(bold=True, size=12, color=NAVY)
        c.number_format = "#,##0"

    ws.cell(18, 1, "→ 詳細總數請查看「總數一覽」工作表").font = F(size=10, color="1D4ED8")
    for c in range(1, 13):
        ws.column_dimensions[get_column_letter(c)].width = 14


# ─── 學生資料庫 ───────────────────────────────────────────
def sheet_students(wb: Workbook):
    ws = wb.create_sheet("學生資料庫")
    b = SheetBuilder(ws, "學生資料庫", merge_cols=18)
    hdrs = [
        "學號", "中文姓名", "英文姓名", "就讀學校", "年級", "報讀課程",
        "課程類別", "上課日", "月費", "付款狀態", "欠費金額",
        "家長姓名", "家長電話", "WhatsApp", "入學日期", "合約到期",
        "合約剩餘天數", "學生狀態", "導師", "轉介來源", "備註",
    ]
    b.headers(hdrs, [7, 9, 10, 13, 5, 16, 8, 8, 8, 9, 9, 9, 12, 6, 11, 11, 9, 8, 8, 10, 16])

    samples = [
        ["S001", "陳小明", "Chan Siu Ming", "九龍塘官小", "P5", "小學功課輔導（每日）", "功課輔導", "一至五", 1980, "已付", 0, "陳太", "9123 4567", "✓", "2024-09-01", "2026-08-31", None, "在讀", "導師A", "舊生", ""],
        ["S002", "李美儀", "Lee Mei Yee", "喇沙書院", "S3", "中學功課+DSE英文", "功課+DSE", "一至五", 3180, "已付", 0, "李先生", "6234 5678", "✓", "2023-02-01", "2026-08-31", None, "在讀", "導師B", "舊生", ""],
        ["S003", "黃俊軒", "Wong Chun Hin", "瑪利諾中學", "S5", "DSE三科套餐", "DSE", "一至六", 3180, "欠費", 3180, "黃太", "5345 6789", "✓", "2024-01-15", "2026-08-31", None, "在讀", "導師A", "舊生", ""],
        ["S004", "張詠琳", "Cheung Wing Lam", "嘉諾撒聖心", "P3", "小學功課（每週3日）", "功課輔導", "一三五", 1580, "已付", 0, "張太", "9876 5432", "✓", "2025-09-01", "2026-08-31", None, "在讀", "導師A", "舊生帶新生", ""],
        ["S005", "何家樂", "Ho Ka Lok", "拔萃男書院", "S6", "DSE英文+數學", "DSE", "二四六", 2360, "部分", 1180, "何生", "8765 4321", "✓", "2023-09-01", "2026-06-30", None, "在讀", "導師B", "學校門口", ""],
        ["S006", "林思穎", "Lam Si Wing", "真光小學", "P4", "小學功課（每日）", "功課輔導", "一至五", 1980, "已付", 0, "林太", "6543 2109", "✓", "2025-01-01", "2026-08-31", None, "在讀", "導師A", "朋友轉介", ""],
    ]
    for i, row in enumerate(samples):
        r = DATA_FIRST + i
        b.row(r, row, {17: f'=IF(P{r}="","",P{r}-TODAY())'}, alt=i % 2 == 1)

    b.dropdown(5, "P1,P2,P3,P4,P5,P6,S1,S2,S3,S4,S5,S6")
    b.dropdown(7, "功課輔導,DSE,習慣養成,體育運動,暑期班,VIP,混合")
    b.dropdown(10, "已付,欠費,部分,豁免")
    b.dropdown(18, "在讀,暫停,退學,畢業,試堂")
    b.dropdown(20, "舊生,舊生帶新生,學校門口,Facebook,Instagram,朋友轉介,其他")
    b.freeze()
    b.cond_format(f"J{DATA_FIRST}:J{DATA_LAST}", f'$J{DATA_FIRST}="欠費"', RED)
    b.cond_format(f"J{DATA_FIRST}:J{DATA_LAST}", f'$J{DATA_FIRST}="部分"', ORANGE)

    add_totals_block(ws, "學生資料庫 · 總數統計", [
        ("學生記錄總數", 9, f"=COUNTA({rng('A')})", "#,##0"),
        ("在讀學生總數", 9, f'=COUNTIF({rng("R")},"在讀")', "#,##0"),
        ("欠費學生總數", 9, f'=COUNTIF({rng("J")},"欠費")', "#,##0"),
        ("月費總額（在讀）", 9, f'=SUMIF({rng("R")},"在讀",{rng("I")})', "#,##0"),
        ("欠費金額總數", 9, f"=SUM({rng('K')})", "#,##0"),
        ("平均月費 ARPU", 9, f'=IFERROR(AVERAGEIF({rng("R")},"在讀",{rng("I")}),0)', "#,##0"),
    ])


# ─── 收費記錄 ───────────────────────────────────────────────
def sheet_fees(wb: Workbook):
    ws = wb.create_sheet("收費記錄")
    b = SheetBuilder(ws, "收費記錄", merge_cols=15)
    hdrs = [
        "日期", "收據編號", "學號", "學生姓名", "月份", "課程",
        "應繳金額", "實收金額", "差額", "收款狀態", "付款方式",
        "轉帳參考號", "經手人", "已開收據", "備註",
    ]
    b.headers(hdrs, [11, 11, 7, 9, 10, 16, 9, 9, 8, 9, 9, 14, 8, 8, 14])

    samples = [
        ["2026-06-01", None, "S001", None, "2026-06", None, 1980, 1980, None, None, "FPS", "FRN12345", "營運者", "✓", ""],
        ["2026-06-01", None, "S002", None, "2026-06", None, 3180, 3180, None, None, "PayMe", "PM98765", "營運者", "✓", ""],
        ["2026-06-05", None, "S003", None, "2026-06", None, 3180, 0, None, None, "—", "—", "—", "✗", "待追繳"],
        ["2026-06-10", None, "S004", None, "2026-06", None, 1580, 1580, None, None, "FPS", "FRN12399", "營運者", "✓", ""],
        ["2026-05-28", None, "S005", None, "2026-05", None, 2360, 1180, None, None, "FPS", "FRN12200", "營運者", "✓", "部分付款"],
    ]
    for i, row in enumerate(samples):
        r = DATA_FIRST + i
        b.row(r, row, {
            2: f'="R-"&RIGHT(E{r},4)&TEXT(ROW()-{HDR_ROW},"000")',
            4: f'=IFERROR(VLOOKUP(C{r},學生資料庫!$A${DATA_FIRST}:$B${DATA_LAST},2,FALSE),"")',
            6: f'=IFERROR(VLOOKUP(C{r},學生資料庫!$A${DATA_FIRST}:$F${DATA_LAST},6,FALSE),"")',
            9: f"=G{r}-H{r}",
            10: f'=IF(H{r}=0,"未付",IF(H{r}>=G{r},"已付清",IF(H{r}>0,"部分","未付")))',
        }, alt=i % 2 == 1)

    b.dropdown(11, "FPS,PayMe,現金,支票,—")
    b.dropdown(14, "✓,✗")
    b.freeze()
    b.cond_format(f"J{DATA_FIRST}:J{DATA_LAST}", f'$J{DATA_FIRST}="未付"', RED)
    b.cond_format(f"J{DATA_FIRST}:J{DATA_LAST}", f'$J{DATA_FIRST}="已付清"', GREEN)

    add_totals_block(ws, "收費記錄 · 總數統計", [
        ("收款筆數總數", 8, f"=COUNTA({rng('A')})", "#,##0"),
        ("應收金額總數", 8, f"=SUM({rng('G')})", "#,##0"),
        ("實收金額總數", 8, f"=SUM({rng('H')})", "#,##0"),
        ("未收金額總數", 8, f"=SUM({rng('I')})", "#,##0"),
        ("本月應收", 8, f'=SUMIF({rng("E")},TEXT(TODAY(),"YYYY-MM"),{rng("G")})', "#,##0"),
        ("本月實收", 8, f'=SUMIF({rng("E")},TEXT(TODAY(),"YYYY-MM"),{rng("H")})', "#,##0"),
        ("已付清筆數", 8, f'=COUNTIF({rng("J")},"已付清")', "#,##0"),
        ("未付筆數", 8, f'=COUNTIF({rng("J")},"未付")', "#,##0"),
    ])


# ─── 出席記錄 ───────────────────────────────────────────────
def sheet_attendance(wb: Workbook):
    ws = wb.create_sheet("出席記錄")
    b = SheetBuilder(ws, "出席記錄", merge_cols=14)
    hdrs = [
        "日期", "學號", "學生姓名", "課程", "應到時間", "實到時間",
        "遲到(分鐘)", "出席狀態", "離開時間", "功課完成", "導師", "家長已通知", "補課安排", "備註",
    ]
    b.headers(hdrs, [11, 7, 9, 15, 9, 9, 8, 9, 9, 9, 8, 9, 10, 14])

    today = date.today().isoformat()
    samples = [
        [today, "S001", None, None, "15:30", "15:25", 0, "出席", "18:30", "完成", "導師A", "—", "—", ""],
        [today, "S002", None, None, "16:00", "16:10", 10, "遲到", "19:00", "完成", "導師B", "—", "—", ""],
        [today, "S003", None, None, "18:30", "—", 0, "缺席", "—", "—", "導師A", "✓", "2026-06-12", ""],
        [today, "S004", None, None, "15:30", "15:30", 0, "出席", "18:00", "完成", "導師A", "—", "—", ""],
        [today, "S005", None, None, "18:30", "18:35", 5, "遲到", "20:30", "完成", "導師B", "—", "—", ""],
        [today, "S006", None, None, "15:30", "15:28", 0, "出席", "18:30", "完成", "導師A", "—", "—", ""],
    ]
    for i, row in enumerate(samples):
        r = DATA_FIRST + i
        b.row(r, row, {
            3: f'=IFERROR(VLOOKUP(B{r},學生資料庫!$A${DATA_FIRST}:$B${DATA_LAST},2,FALSE),"")',
            4: f'=IFERROR(VLOOKUP(B{r},學生資料庫!$A${DATA_FIRST}:$F${DATA_LAST},6,FALSE),"")',
        }, alt=i % 2 == 1)

    b.dropdown(8, "出席,遲到,缺席,請假")
    b.dropdown(10, "完成,未完成,部分,—")
    b.freeze()
    b.cond_format(f"H{DATA_FIRST}:H{DATA_LAST}", f'$H{DATA_FIRST}="缺席"', RED)
    b.cond_format(f"H{DATA_FIRST}:H{DATA_LAST}", f'$H{DATA_FIRST}="出席"', GREEN)

    add_totals_block(ws, "出席記錄 · 總數統計", [
        ("點名記錄總數", 8, f"=COUNTA({rng('A')})", "#,##0"),
        ("出席人次總數", 8, f'=COUNTIF({rng("H")},"出席")', "#,##0"),
        ("遲到人次總數", 8, f'=COUNTIF({rng("H")},"遲到")', "#,##0"),
        ("缺席人次總數", 8, f'=COUNTIF({rng("H")},"缺席")', "#,##0"),
        ("請假人次總數", 8, f'=COUNTIF({rng("H")},"請假")', "#,##0"),
        ("出席率", 8, f'=IFERROR(COUNTIF({rng("H")},"出席")/COUNTA({rng("A")}),0)', "0%"),
        ("功課完成總數", 8, f'=COUNTIF({rng("J")},"完成")', "#,##0"),
        ("遲到分鐘總數", 8, f"=SUM({rng('G')})", "#,##0"),
    ])


# ─── 排課表 ───────────────────────────────────────────────
def sheet_schedule(wb: Workbook):
    ws = wb.create_sheet("排課表")
    b = SheetBuilder(ws, "每週排課表", merge_cols=15)
    hdrs = [
        "星期", "時段", "課程名稱", "課程類別", "導師", "課室",
        "對象", "班額", "已報", "候補", "滿班率", "月費參考", "預估月營收", "狀態", "備註",
    ]
    b.headers(hdrs, [7, 12, 17, 9, 8, 7, 8, 5, 5, 5, 7, 9, 10, 7, 12])

    rows = [
        ["星期一", "15:30–18:30", "小學功課輔導", "功課輔導", "導師A", "課室A", "P1–P6", 12, 10, 2, None, 1980, None, "開班", ""],
        ["星期一", "16:00–19:00", "中學功課輔導", "功課輔導", "導師B", "課室B", "S1–S3", 10, 8, 0, None, 2480, None, "開班", ""],
        ["星期一", "18:30–20:30", "DSE 英文", "DSE", "導師A", "課室A", "S4–S6", 12, 9, 1, None, 1180, None, "開班", ""],
        ["星期二", "18:30–20:30", "DSE 中文", "DSE", "導師B", "課室B", "S4–S6", 12, 7, 0, None, 1180, None, "開班", ""],
        ["星期三", "18:30–20:30", "DSE 英文", "DSE", "導師A", "課室A", "S4–S6", 12, 9, 0, None, 1180, None, "開班", ""],
        ["星期四", "18:30–20:30", "DSE 中文", "DSE", "導師B", "課室B", "S4–S6", 12, 7, 0, None, 1180, None, "開班", ""],
        ["星期五", "18:30–20:30", "DSE 數學", "DSE", "導師A", "課室A", "S4–S6", 12, 8, 0, None, 1180, None, "開班", ""],
        ["星期六", "10:00–12:00", "時間管理習慣班", "習慣養成", "兼職C", "課室B", "P1–S3", 10, 6, 0, None, 680, None, "開班", ""],
        ["星期六", "14:00–16:00", "籃球基礎班", "體育運動", "兼職D", "戶外", "P1–S6", 12, 8, 2, None, 720, None, "開班", ""],
        ["星期日", "10:00–12:00", "專注力學習班", "習慣養成", "兼職C", "課室A", "P1–S3", 10, 5, 0, None, 680, None, "開班", ""],
    ]
    for i, row in enumerate(rows):
        r = DATA_FIRST + i
        b.row(r, row, {
            11: f'=IF(H{r}=0,"—",TEXT(I{r}/H{r},"0%"))',
            13: f"=I{r}*L{r}",
        }, alt=i % 2 == 1)

    b.dropdown(4, "功課輔導,DSE,習慣養成,體育運動,暑期班,VIP")
    b.dropdown(14, "開班,滿班,候補,暫停,取消")
    b.freeze()

    add_totals_block(ws, "排課表 · 總數統計", [
        ("開班課程總數", 9, f"=COUNTA({rng('A')})", "#,##0"),
        ("班額總數", 9, f"=SUM({rng('H')})", "#,##0"),
        ("已報學生總數", 9, f"=SUM({rng('I')})", "#,##0"),
        ("候補總數", 9, f"=SUM({rng('J')})", "#,##0"),
        ("預估月營收總數", 9, f"=SUM({rng('M')})", "#,##0"),
        ("平均滿班率", 9, f'=IFERROR(SUM({rng("I")})/SUM({rng("H")}),0)', "0%"),
        ("功課輔導班數", 9, f'=COUNTIF({rng("D")},"功課輔導")', "#,##0"),
        ("DSE班數", 9, f'=COUNTIF({rng("D")},"DSE")', "#,##0"),
    ])


# ─── 課室使用表 ───────────────────────────────────────────
def sheet_rooms(wb: Workbook):
    ws = wb.create_sheet("課室使用表")
    b = SheetBuilder(ws, "課室使用表", merge_cols=11)
    hdrs = [
        "星期", "時段", "課室A", "課室A狀態", "課室B", "課室B狀態",
        "VIP室", "VIP室狀態", "負責導師", "每呎產值", "備註",
    ]
    b.headers(hdrs, [7, 12, 16, 8, 16, 8, 14, 8, 9, 9, 14])

    rows = [
        ["星期一", "15:30–18:30", "小學功課輔導", "使用中", "中學功課輔導", "使用中", "—", "空閒", "導師A/B", None, ""],
        ["星期一", "18:30–20:30", "DSE英文", "使用中", "—", "空閒", "1對1 VIP", "使用中", "導師A", None, ""],
        ["星期二", "15:30–18:30", "小學功課輔導", "使用中", "中學功課輔導", "使用中", "—", "空閒", "導師A/B", None, ""],
        ["星期三", "15:30–18:30", "小學功課輔導", "使用中", "—", "空閒", "—", "空閒", "導師A", None, ""],
        ["星期六", "10:00–12:00", "—", "空閒", "習慣班", "使用中", "—", "空閒", "兼職C", None, ""],
        ["星期六", "14:00–18:00", "—", "空閒", "—", "空閒", "1對2 數學", "使用中", "兼職D", None, ""],
    ]
    for i, row in enumerate(rows):
        r = DATA_FIRST + i
        b.row(r, row, {10: f'=IF(D{r}="空閒",200,IF(F{r}="空閒",150,IF(H{r}="空閒",250,100)))'}, alt=i % 2 == 1)

    b.dropdown(4, "使用中,空閒,清潔中,維修")
    b.dropdown(6, "使用中,空閒,清潔中,維修")
    b.dropdown(8, "使用中,空閒,清潔中,維修")
    b.freeze()
    b.cond_format(f"D{DATA_FIRST}:D{DATA_LAST}", f'$D{DATA_FIRST}="空閒"', GREEN)

    add_totals_block(ws, "課室使用表 · 總數統計", [
        ("時段記錄總數", 10, f"=COUNTA({rng('A')})", "#,##0"),
        ("課室A 空閒總數", 10, f'=COUNTIF({rng("D")},"空閒")', "#,##0"),
        ("課室B 空閒總數", 10, f'=COUNTIF({rng("F")},"空閒")', "#,##0"),
        ("VIP室 空閒總數", 10, f'=COUNTIF({rng("H")},"空閒")', "#,##0"),
        ("空閒時段合計", 10, f'=COUNTIF({rng("D")},"空閒")+COUNTIF({rng("F")},"空閒")+COUNTIF({rng("H")},"空閒")', "#,##0"),
        ("使用中時段合計", 10, f'=COUNTIF({rng("D")},"使用中")+COUNTIF({rng("F")},"使用中")+COUNTIF({rng("H")},"使用中")', "#,##0"),
        ("平均呎產值", 10, f'=IFERROR(AVERAGE({rng("J")}),0)', "#,##0"),
    ])


# ─── 財務月結 ───────────────────────────────────────────────
def sheet_finance(wb: Workbook):
    ws = wb.create_sheet("財務月結")
    b = SheetBuilder(ws, "財務月結表", merge_cols=16)
    hdrs = [
        "月份", "學生數", "ARPU", "月營收", "租金", "全職導師",
        "兼職導師", "水電", "雜費", "推廣", "其他", "總成本",
        "月淨利", "淨利率", "目標達成率", "備註",
    ]
    b.headers(hdrs, [9, 7, 8, 10, 8, 9, 9, 7, 7, 7, 7, 10, 10, 8, 9, 14])

    rows = [
        ["2026-06", 50, 3000, 150000, 40000, 45000, 12000, 5500, 5000, 3000, 0, None, None, None, None, "接手首月"],
        ["2026-07", 65, 3231, 210000, 35000, 45000, 20000, 6000, 5000, 5000, 0, None, None, None, None, "暑假高峰"],
        ["2026-08", 70, 3500, 245000, 35000, 45000, 22000, 6000, 5000, 3000, 0, None, None, None, None, "暑假高峰"],
        ["2026-09", 60, 3200, 192000, 35000, 45000, 15000, 5500, 5000, 3000, 0, None, None, None, None, "新學期"],
        ["2026-10", 62, 3250, 201500, 35000, 45000, 14000, 5500, 5000, 3000, 0, None, None, None, None, ""],
    ]
    for i, row in enumerate(rows):
        r = DATA_FIRST + i
        b.row(r, row, {
            12: f"=SUM(E{r}:K{r})",
            13: f"=D{r}-L{r}",
            14: f'=IF(D{r}=0,"—",TEXT(M{r}/D{r},"0%"))',
            15: f"=IFERROR(M{r}/82000,\"—\")",
        }, alt=i % 2 == 1)

    b.freeze()
    b.cond_format(f"M{DATA_FIRST}:M{DATA_LAST}", f"M{DATA_FIRST}>=82000", GREEN)

    add_totals_block(ws, "財務月結 · 總數統計", [
        ("記錄月數總數", 13, f"=COUNTA({rng('A')})", "#,##0"),
        ("年度營收總數", 13, f"=SUM({rng('D')})", "#,##0"),
        ("年度成本總數", 13, f"=SUM({rng('L')})", "#,##0"),
        ("年度淨利總數", 13, f"=SUM({rng('M')})", "#,##0"),
        ("平均月營收", 13, f'=IFERROR(AVERAGE({rng("D")}),0)', "#,##0"),
        ("平均月淨利", 13, f'=IFERROR(AVERAGE({rng("M")}),0)', "#,##0"),
        ("最高月淨利", 13, f"=MAX({rng('M')})", "#,##0"),
        ("平均學生數", 13, f'=IFERROR(AVERAGE({rng("B")}),0)', "#,##0"),
        ("平均 ARPU", 13, f'=IFERROR(AVERAGE({rng("C")}),0)', "#,##0"),
    ])


# ─── 學習進度 ───────────────────────────────────────────────
def sheet_progress(wb: Workbook):
    ws = wb.create_sheet("學習進度")
    b = SheetBuilder(ws, "學習進度報告", merge_cols=14)
    hdrs = [
        "月份", "學號", "學生姓名", "課程", "出席率", "功課完成率",
        "測驗分數", "上次分數", "進步幅度", "進步重點", "待改善",
        "導師評語", "WhatsApp訊息", "已發送",
    ]
    b.headers(hdrs, [9, 7, 9, 14, 8, 10, 9, 9, 8, 16, 12, 16, 30, 7])

    rows = [
        ["2026-06", "S001", None, None, "95%", "90%", 78, 72, None, "數學應用題進步", "中文造句", "表現穩定", None, "✓"],
        ["2026-06", "S002", None, None, "88%", "85%", 72, 68, None, "閱讀理解提升", "寫作結構", "需加強操卷", None, "✓"],
        ["2026-06", "S003", None, None, "70%", "60%", 55, 58, None, "—", "出席率偏低", "請家長督促", None, "✗"],
        ["2026-06", "S004", None, None, "92%", "88%", 82, 75, None, "英文進步", "—", "表現良好", None, "✓"],
    ]
    for i, row in enumerate(rows):
        r = DATA_FIRST + i
        b.row(r, row, {
            3: f'=IFERROR(VLOOKUP(B{r},學生資料庫!$A${DATA_FIRST}:$B${DATA_LAST},2,FALSE),"")',
            4: f'=IFERROR(VLOOKUP(B{r},學生資料庫!$A${DATA_FIRST}:$F${DATA_LAST},6,FALSE),"")',
            9: f'=IF(OR(G{r}="",H{r}=""),"—",G{r}-H{r})',
            13: f'="【俊才坊學習進度】"&C{r}&" "&A{r}&"：出席"&E{r}&" 功課"&F{r}&" 測驗"&G{r}&"分 評語："&L{r}',
        }, alt=i % 2 == 1)

    b.dropdown(14, "✓,✗")
    b.freeze()

    add_totals_block(ws, "學習進度 · 總數統計", [
        ("進度報告總數", 9, f"=COUNTA({rng('B')})", "#,##0"),
        ("已發送總數", 9, f'=COUNTIF({rng("N")},"✓")', "#,##0"),
        ("待發送總數", 9, f'=COUNTIF({rng("N")},"✗")', "#,##0"),
        ("進步人數（>0）", 9, f'=COUNTIF({rng("I")},">0")', "#,##0"),
        ("退步人數（<0）", 9, f'=COUNTIF({rng("I")},"<0")', "#,##0"),
        ("平均測驗分數", 9, f'=IFERROR(AVERAGE({rng("G")}),0)', "#,##0"),
    ])


# ─── 每日行政 ───────────────────────────────────────────────
def sheet_daily(wb: Workbook):
    ws = wb.create_sheet("每日行政")
    b = SheetBuilder(ws, "每日行政檢查表", merge_cols=8)

    ws.cell(4, 1, "日期：").font = F(bold=True)
    ws.cell(4, 2, date.today().isoformat()).font = F(bold=True, color=NAVY)
    ws.cell(4, 4, "完成率：").font = F(bold=True)
    ws.cell(4, 5, f'=IFERROR(TEXT(COUNTIF(C{DATA_FIRST}:C{DATA_FIRST+19},"✓")/COUNTA(B{DATA_FIRST}:B{DATA_FIRST+19}),"0%"),"0%")').font = F(bold=True, size=14, color=NAVY)

    hdrs = ["時段", "任務", "完成?", "用時(分)", "負責人", "相關工作表", "備註"]
    b.headers(hdrs, [12, 36, 7, 8, 8, 12, 16])

    tasks = [
        ["🌅 早上", "確認當日課表，WhatsApp 通知所有導師", "", "", "營運者", "排課表", ""],
        ["🌅 早上", "檢查收費記錄，列出欠費名單並標記", "", "", "營運者", "收費記錄", ""],
        ["🌅 早上", "回覆家長 WhatsApp 查詢（30分鐘內）", "", "", "營運者", "家長通訊", ""],
        ["☀️ 下午", "學生到達點名，記錄出席狀態", "", "", "導師/營運者", "出席記錄", ""],
        ["☀️ 下午", "確保課室整潔、教材準備充足", "", "", "導師", "課室使用表", ""],
        ["☀️ 下午", "處理即時家長查詢並記錄", "", "", "營運者", "家長通訊", ""],
        ["🌙 晚上", "更新出席記錄（遲到/缺席/功課）", "", "", "營運者", "出席記錄", ""],
        ["🌙 晚上", "核對當日收款，記入收費記錄", "", "", "營運者", "收費記錄", ""],
        ["🌙 晚上", "規劃翌日課堂，補課提前通知家長", "", "", "營運者", "排課表", ""],
        ["🌙 晚上", "更新學習進度備註（如有測驗）", "", "", "導師", "學習進度", ""],
    ]
    for i, row in enumerate(tasks):
        b.row(DATA_FIRST + i, row, alt=i % 2 == 1)

    b.dropdown(3, "✓,✗,—,進行中")
    b.freeze()

    task_end = DATA_FIRST + len(tasks) - 1
    add_totals_block(ws, "每日行政 · 總數統計", [
        ("任務總數", 4, f"=COUNTA(B{DATA_FIRST}:B{task_end})", "#,##0"),
        ("已完成總數", 4, f'=COUNTIF(C{DATA_FIRST}:C{task_end},"✓")', "#,##0"),
        ("未完成總數", 4, f'=COUNTIF(C{DATA_FIRST}:C{task_end},"✗")', "#,##0"),
        ("總用時(分鐘)", 4, f"=SUM(D{DATA_FIRST}:D{task_end})", "#,##0"),
        ("完成率", 4, f'=IFERROR(COUNTIF(C{DATA_FIRST}:C{task_end},"✓")/COUNTA(B{DATA_FIRST}:B{task_end}),0)', "0%"),
    ])


# ─── 家長通訊 ───────────────────────────────────────────────
def sheet_parents(wb: Workbook):
    ws = wb.create_sheet("家長通訊")
    b = SheetBuilder(ws, "家長通訊記錄", merge_cols=13)
    hdrs = [
        "日期", "學號", "家長姓名", "聯絡方式", "類型", "優先級",
        "內容摘要", "處理狀態", "回覆時限", "跟進日期", "逾期?", "負責人", "備註",
    ]
    b.headers(hdrs, [11, 7, 9, 9, 10, 7, 22, 9, 10, 11, 6, 8, 14])

    rows = [
        ["2026-06-10", "S003", None, "WhatsApp", "欠費提醒", "高", "6月學費未繳", "跟進中", "2026-06-12", "2026-06-15", None, "營運者", ""],
        ["2026-06-10", "S001", None, "WhatsApp", "進度查詢", "中", "查詢數學進度", "已完成", "2026-06-10", "—", None, "營運者", ""],
        ["2026-06-11", "—", "王太（新生）", "電話", "招生查詢", "高", "查詢暑假班", "跟進中", "2026-06-13", "2026-06-13", None, "營運者", "潛在新生"],
        ["2026-06-11", "S005", None, "WhatsApp", "續報查詢", "中", "查詢9月學費", "待處理", "2026-06-12", "2026-06-14", None, "營運者", ""],
        ["2026-06-12", "S006", None, "WhatsApp", "進度查詢", "低", "查詢英文進度", "已完成", "2026-06-12", "—", None, "營運者", ""],
    ]
    for i, row in enumerate(rows):
        r = DATA_FIRST + i
        b.row(r, row, {
            3: f'=IF(B{r}="","",IFERROR(VLOOKUP(B{r},學生資料庫!$A${DATA_FIRST}:$L${DATA_LAST},12,FALSE),""))',
            11: f'=IF(OR(J{r}="—",J{r}=""),"",IF(AND(H{r}<>"已完成",TODAY()>J{r}),"⚠️",""))',
        }, alt=i % 2 == 1)

    b.dropdown(5, "欠費提醒,進度查詢,招生查詢,續報查詢,投訴,其他")
    b.dropdown(6, "高,中,低")
    b.dropdown(8, "已完成,跟進中,待處理")
    b.freeze()
    b.cond_format(f"F{DATA_FIRST}:F{DATA_LAST}", f'$F{DATA_FIRST}="高"', RED)

    add_totals_block(ws, "家長通訊 · 總數統計", [
        ("通訊記錄總數", 8, f"=COUNTA({rng('A')})", "#,##0"),
        ("已完成總數", 8, f'=COUNTIF({rng("H")},"已完成")', "#,##0"),
        ("跟進中總數", 8, f'=COUNTIF({rng("H")},"跟進中")', "#,##0"),
        ("待處理總數", 8, f'=COUNTIF({rng("H")},"待處理")', "#,##0"),
        ("高優先級總數", 8, f'=COUNTIF({rng("F")},"高")', "#,##0"),
        ("逾期總數", 8, f'=COUNTIF({rng("K")},"⚠️")', "#,##0"),
        ("招生查詢總數", 8, f'=COUNTIF({rng("E")},"招生查詢")', "#,##0"),
    ])


# ─── 導師資料 ───────────────────────────────────────────────
def sheet_tutors(wb: Workbook):
    ws = wb.create_sheet("導師資料")
    b = SheetBuilder(ws, "導師及員工資料", merge_cols=14)
    hdrs = [
        "編號", "姓名", "職位", "電話", "負責課程", "負責學生數",
        "薪酬", "月薪估算", "入職日期", "合約到期", "合約剩餘天數",
        "通知期", "狀態", "備註",
    ]
    b.headers(hdrs, [7, 9, 10, 12, 18, 8, 12, 10, 11, 11, 9, 8, 7, 16])

    rows = [
        ["T001", "導師A", "全職導師", "9XXX XXXX", "功課輔導、DSE", None, "$22,500/月", 22500, "2020-03-01", "2026-12-31", None, "2個月", "在職", "核心導師"],
        ["T002", "導師B", "全職導師", "9XXX XXXX", "功課輔導、DSE", None, "$22,500/月", 22500, "2019-09-01", "2026-12-31", None, "2個月", "在職", "核心導師"],
        ["T003", "兼職C", "兼職導師", "9XXX XXXX", "習慣班", None, "$150/時", None, "2025-01-01", "—", None, "1個月", "在職", ""],
        ["T004", "兼職D", "兼職導師", "9XXX XXXX", "籃球班", None, "$200/時", None, "2025-06-01", "—", None, "1個月", "在職", "外聘教練"],
    ]
    for i, row in enumerate(rows):
        r = DATA_FIRST + i
        b.row(r, row, {
            6: f'=COUNTIF(學生資料庫!S{DATA_FIRST}:S{DATA_LAST},B{r})',
            8: f'=IF(ISNUMBER(SEARCH("/月",G{r})),VALUE(SUBSTITUTE(SUBSTITUTE(G{r},"$",""),"/月","")),"")',
            11: f'=IF(OR(J{r}="—",J{r}=""),"",J{r}-TODAY())',
        }, alt=i % 2 == 1)

    b.dropdown(13, "在職,離職,試用,顧問")
    b.freeze()

    add_totals_block(ws, "導師資料 · 總數統計", [
        ("導師記錄總數", 8, f"=COUNTA({rng('A')})", "#,##0"),
        ("在職導師總數", 8, f'=COUNTIF({rng("M")},"在職")', "#,##0"),
        ("全職導師總數", 8, f'=COUNTIF({rng("C")},"全職導師")', "#,##0"),
        ("兼職導師總數", 8, f'=COUNTIF({rng("C")},"兼職導師")', "#,##0"),
        ("負責學生總數", 8, f"=SUM({rng('F')})", "#,##0"),
        ("全職月薪總數", 8, f'=SUMIF({rng("C")},"全職導師",{rng("H")})', "#,##0"),
        ("合約60天內到期", 8, f'=COUNTIFS({rng("K")},">0",{rng("K")},"<=60")', "#,##0"),
    ])


# ─── 使用說明 ───────────────────────────────────────────────
def sheet_readme(wb: Workbook):
    ws = wb.create_sheet("使用說明")
    ws.column_dimensions["A"].width = 14
    ws.column_dimensions["B"].width = 28
    ws.column_dimensions["C"].width = 50
    ws["A1"] = "俊才坊行政系統"
    ws["A1"].font = F(bold=True, size=16, color=NAVY)
    ws["A2"] = SUBTITLE
    ws["A2"].font = F(size=10, color=MUTED)

    for c, h in enumerate(["工作表", "總數統計項目", "升級功能"], 1):
        ws.cell(4, c, h).font = F(bold=True, color=WHITE)
        ws.cell(4, c).fill = HDR_FILL

    features = [
        ("儀表板", "6 項 KPI + 6 項總數速覽", "每日開啟，連動所有工作表"),
        ("總數一覽", "31 項跨表總數自動匯總", "一頁看清中心所有關鍵數字"),
        ("學生資料庫", "在讀/欠費/月費總額/ARPU/欠費金額", "底部第203行起 · 自動更新"),
        ("收費記錄", "應收/實收/未收/本月/已付清/未付", "每筆收款即時累計"),
        ("出席記錄", "出席/遲到/缺席/請假/出席率/功課完成", "每日放學後更新"),
        ("排課表", "班額/已報/候補/營收/滿班率/各班型", "每學期更新"),
        ("課室使用表", "各室空閒/使用中/平均呎產值", "規劃 VIP 時段"),
        ("財務月結", "年度營收/成本/淨利/平均/最高", "每月底結算"),
        ("學習進度", "報告/已發送/待發送/進退步/平均分", "每月25-28日"),
        ("每日行政", "任務/完成/未完成/用時/完成率", "每日執行"),
        ("家長通訊", "通訊/完成/跟進/待處理/逾期/招生", "每次通訊後記錄"),
        ("導師資料", "在職/全職/兼職/學生數/月薪/合約", "接手時核查"),
    ]
    for i, (name, totals, usage) in enumerate(features, 5):
        ws.cell(i, 1, name).font = F(bold=True, color=NAVY)
        ws.cell(i, 2, totals).font = F(size=9)
        ws.cell(i, 3, usage).font = F(size=9, color=MUTED)

    r = 5 + len(features) + 2
    ws.cell(r, 1, "總數位置").font = F(bold=True, size=12, color=NAVY)
    ws.cell(r + 1, 1, "每個工作表底部第 203 行起有金色「📊 總數統計」區塊，公式覆蓋第 6–200 行，新增資料會自動計入總數。").font = F(size=9)
    ws.merge_cells(start_row=r + 1, start_column=1, end_row=r + 1, end_column=3)


def main():
    wb = Workbook()
    sheet_dashboard(wb)
    sheet_totals_overview(wb)
    sheet_readme(wb)
    sheet_students(wb)
    sheet_fees(wb)
    sheet_attendance(wb)
    sheet_schedule(wb)
    sheet_rooms(wb)
    sheet_finance(wb)
    sheet_progress(wb)
    sheet_daily(wb)
    sheet_parents(wb)
    sheet_tutors(wb)
    if "Sheet" in wb.sheetnames:
        del wb["Sheet"]

    out = OUT / "俊才坊行政系統.xlsx"
    wb.save(out)
    print(f"Saved {out}")
    print("Sheets:", ", ".join(wb.sheetnames))


if __name__ == "__main__":
    main()
