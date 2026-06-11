#!/usr/bin/env python3
"""Build 俊才坊行政系統 Excel workbook — Upgrade Edition v2."""

from __future__ import annotations

from datetime import date
from pathlib import Path

from openpyxl import Workbook
from openpyxl.formatting.rule import FormulaRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.worksheet.table import Table, TableStyleInfo

OUT = Path(__file__).parent / "output"
OUT.mkdir(exist_ok=True)

# Colours
NAVY, GOLD, WHITE = "1E3A5F", "D4A843", "FFFFFF"
ALT, GREEN, RED, YELLOW, BLUE = "F8FAFC", "DCFCE7", "FEE2E2", "FEF3C7", "DBEAFE"
ORANGE, MUTED = "FFEDD5", "64748B"

THIN = Side(style="thin", color="CBD5E0")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
DATA_START = 5  # header row
MAX_ROWS = 200


def F(bold=False, size=10, color="000000"):
    return Font(name="Calibri", bold=bold, size=size, color=color)


def fill(hex_color: str) -> PatternFill:
    return PatternFill("solid", fgColor=hex_color)


TITLE_FONT = F(bold=True, size=14, color=NAVY)
HDR_FONT = F(bold=True, size=10, color=WHITE)
HDR_FILL = fill(NAVY)
ALT_FILL = fill(ALT)
GOLD_FILL = fill(GOLD)


class SheetBuilder:
    def __init__(self, ws, title: str, subtitle: str = "", merge_cols: int = 10):
        self.ws = ws
        self.start = DATA_START
        self.merge_cols = merge_cols
        self._title(title, subtitle)

    def _title(self, title: str, subtitle: str):
        mc = self.merge_cols
        self.ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=mc)
        self.ws.cell(1, 1, f"俊才坊補習社 · {title}").font = TITLE_FONT
        if subtitle:
            self.ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=mc)
            self.ws.cell(2, 1, subtitle).font = F(size=10, color=MUTED)

    def headers(self, headers: list[str], widths: list[int]):
        r = self.start
        for c, h in enumerate(headers, 1):
            cell = self.ws.cell(r, c, h)
            cell.font = HDR_FONT
            cell.fill = HDR_FILL
            cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
            cell.border = BORDER
            self.ws.column_dimensions[get_column_letter(c)].width = widths[c - 1]
        self.ws.row_dimensions[r].height = 30
        self.headers_list = headers
        return r

    def row(self, r: int, values: list, formulas: dict[int, str] | None = None, alt: bool = False):
        formulas = formulas or {}
        for c, v in enumerate(values, 1):
            cell = self.ws.cell(r, c)
            if c in formulas:
                cell.value = formulas[c]
            else:
                cell.value = v
            cell.font = BODY if not formulas.get(c) else F(color="1D4ED8")
            cell.border = BORDER
            cell.alignment = Alignment(vertical="center", wrap_text=True)
            if alt:
                cell.fill = ALT_FILL

    def dropdown(self, col: int, options: str, end_row: int | None = None):
        end_row = end_row or MAX_ROWS
        col_l = get_column_letter(col)
        dv = DataValidation(type="list", formula1=f'"{options}"', allow_blank=True)
        self.ws.add_data_validation(dv)
        dv.add(f"{col_l}{self.start + 1}:{col_l}{end_row}")

    def table(self, col_count: int, row_count: int, name: str):
        ref = f"A{self.start}:{get_column_letter(col_count)}{self.start + row_count}"
        tab = Table(displayName=name, ref=ref)
        tab.tableStyleInfo = TableStyleInfo(
            name="TableStyleMedium2", showFirstColumn=False,
            showLastColumn=False, showRowStripes=True, showColumnStripes=False,
        )
        self.ws.add_table(tab)

    def freeze(self):
        self.ws.freeze_panes = f"A{self.start + 1}"

    def kpi_box(self, row: int, col: int, label: str, formula: str, width: int = 14):
        ws = self.ws
        c = col
        ws.merge_cells(start_row=row, start_column=c, end_row=row, end_column=c + 1)
        ws.cell(row, c, label).font = F(bold=True, size=9, color=MUTED)
        ws.merge_cells(start_row=row + 1, start_column=c, end_row=row + 1, end_column=c + 1)
        cell = ws.cell(row + 1, c, formula)
        cell.font = F(bold=True, size=16, color=NAVY)
        cell.alignment = Alignment(horizontal="center")
        ws.column_dimensions[get_column_letter(c)].width = width

    def cond_format(self, range_str: str, formula: str, bg: str):
        rule = FormulaRule(formula=[formula], fill=fill(bg))
        self.ws.conditional_formatting.add(range_str, rule)

    def summary_row(self, r: int, label: str, col: int, formula: str):
        self.ws.cell(r, 1, label).font = F(bold=True, color=NAVY)
        cell = self.ws.cell(r, col, formula)
        cell.font = F(bold=True, size=11, color=NAVY)
        cell.fill = fill(YELLOW)
        cell.border = BORDER


BODY = F()


# ─── 儀表板 ───────────────────────────────────────────────
def sheet_dashboard(wb: Workbook):
    ws = wb.create_sheet("儀表板", 0)
    b = SheetBuilder(ws, "營運儀表板", "即時 KPI · 自動連動各工作表", merge_cols=12)

    ws.merge_cells("A4:L4")
    ws.cell(4, 1, f"更新日期：{date.today().isoformat()}").font = F(size=9, color=MUTED)

    # KPI row
    b.kpi_box(6, 1, "在讀學生", '=COUNTA(學生資料庫!A6:A200)-COUNTIF(學生資料庫!P6:P200,"畢業")-COUNTIF(學生資料庫!P6:P200,"退學")', 12)
    b.kpi_box(6, 3, "欠費學生", '=COUNTIF(學生資料庫!I6:I200,"欠費")', 12)
    b.kpi_box(6, 5, "本月實收", '=SUMIF(收費記錄!E6:E200,TEXT(TODAY(),"YYYY-MM"),收費記錄!H6:H200)', 14)
    b.kpi_box(6, 7, "本月應收", '=SUMIF(收費記錄!E6:E200,TEXT(TODAY(),"YYYY-MM"),收費記錄!G6:G200)', 14)
    b.kpi_box(6, 9, "待跟進通訊", '=COUNTIF(家長通訊!H6:H200,"跟進中")+COUNTIF(家長通訊!H6:H200,"待處理")', 12)
    b.kpi_box(6, 11, "今日課堂", '=COUNTIF(排課表!A6:A200,TEXT(TODAY(),"AAAA"))', 10)

    # Alert section
    ws.cell(10, 1, "⚠️ 待處理提醒").font = F(bold=True, size=12, color="DC2626")
    alerts = [
        ("欠費學生名單", "請查看「學生資料庫」付款狀態 = 欠費"),
        ("合約 30 天內到期", "請查看「學生資料庫」合約到期欄 ≤ 30 天"),
        ("今日行政未完成", "請查看「每日行政」完成? 欄"),
        ("待發送進度報告", "請查看「學習進度」已發送 = ✗"),
        ("導師合約即將到期", "請查看「導師資料」合約到期欄"),
    ]
    for i, (title, desc) in enumerate(alerts, 11):
        ws.cell(i, 1, title).font = F(bold=True)
        ws.cell(i, 2, desc).font = F(size=9, color=MUTED)
        ws.merge_cells(start_row=i, start_column=2, end_row=i, end_column=8)

    # Quick links
    ws.cell(17, 1, "快速導航").font = F(bold=True, size=12, color=NAVY)
    links = [
        ("學生資料庫", "管理學生及家長資料"),
        ("收費記錄", "FPS/PayMe 收款"),
        ("出席記錄", "每日點名"),
        ("排課表", "每週課程"),
        ("財務月結", "月度 P&L"),
        ("每日行政", "今日待辦清單"),
    ]
    for i, (name, desc) in enumerate(links, 18):
        ws.cell(i, 1, f"→ {name}").font = F(bold=True, color="1D4ED8")
        ws.cell(i, 2, desc).font = F(size=9)

    # Monthly target
    ws.cell(25, 1, "本月財務目標").font = F(bold=True, size=12, color=NAVY)
    targets = [
        ("目標月營收", 192000, "升級目標情景"),
        ("目標月成本", 110000, "租金談判後"),
        ("目標月淨利", 82000, "60人 × $3,200 ARPU"),
        ("目標學生數", 60, ""),
    ]
    for i, (label, val, note) in enumerate(targets, 26):
        ws.cell(i, 1, label).font = F(bold=True)
        ws.cell(i, 2, val).font = F(bold=True, size=12, color=NAVY)
        ws.cell(i, 2).number_format = "#,##0"
        ws.cell(i, 3, note).font = F(size=9, color=MUTED)

    for c in range(1, 13):
        ws.column_dimensions[get_column_letter(c)].width = 14


# ─── 學生資料庫 ───────────────────────────────────────────
def sheet_students(wb: Workbook):
    ws = wb.create_sheet("學生資料庫")
    b = SheetBuilder(ws, "學生資料庫", "★ 接手首週必完成 · 含自動計算欄位", merge_cols=18)
    hdrs = [
        "學號", "中文姓名", "英文姓名", "就讀學校", "年級", "報讀課程",
        "課程類別", "上課日", "月費", "付款狀態", "欠費金額",
        "家長姓名", "家長電話", "WhatsApp", "入學日期", "合約到期",
        "合約剩餘天數", "學生狀態", "導師", "轉介來源", "備註",
    ]
    widths = [7, 9, 10, 13, 5, 16, 8, 8, 8, 9, 9, 9, 12, 6, 11, 11, 9, 8, 8, 10, 16]
    b.headers(hdrs, widths)

    samples = [
        ["S001", "陳小明", "Chan Siu Ming", "九龍塘官小", "P5", "小學功課輔導（每日）", "功課輔導", "一至五", 1980, "已付", 0, "陳太", "9123 4567", "✓", "2024-09-01", "2026-08-31", None, "在讀", "導師A", "舊生", ""],
        ["S002", "李美儀", "Lee Mei Yee", "喇沙書院", "S3", "中學功課+DSE英文", "功課+DSE", "一至五", 3180, "已付", 0, "李先生", "6234 5678", "✓", "2023-02-01", "2026-08-31", None, "在讀", "導師B", "舊生", ""],
        ["S003", "黃俊軒", "Wong Chun Hin", "瑪利諾中學", "S5", "DSE三科套餐", "DSE", "一至六", 3180, "欠費", 3180, "黃太", "5345 6789", "✓", "2024-01-15", "2026-08-31", None, "在讀", "導師A", "舊生", "欠6月學費"],
        ["S004", "張詠琳", "Cheung Wing Lam", "嘉諾撒聖心", "P3", "小學功課（每週3日）", "功課輔導", "一三五", 1580, "已付", 0, "張太", "9876 5432", "✓", "2025-09-01", "2026-08-31", None, "在讀", "導師A", "舊生帶新生", "半價優惠"],
        ["S005", "何家樂", "Ho Ka Lok", "拔萃男書院", "S6", "DSE英文+數學", "DSE", "二四六", 2360, "部分", 1180, "何生", "8765 4321", "✓", "2023-09-01", "2026-06-30", None, "在讀", "導師B", "學校門口", ""],
    ]
    for i, row in enumerate(samples):
        r = b.start + 1 + i
        formulas = {
            17: f'=IF(P{r}="","",P{r}-TODAY())',  # 合約剩餘天數
        }
        b.row(r, row, formulas, alt=i % 2 == 1)

    b.dropdown(5, "P1,P2,P3,P4,P5,P6,S1,S2,S3,S4,S5,S6")
    b.dropdown(7, "功課輔導,DSE,習慣養成,體育運動,暑期班,VIP,混合")
    b.dropdown(10, "已付,欠費,部分,豁免")
    b.dropdown(18, "在讀,暫停,退學,畢業,試堂")
    b.dropdown(20, "舊生,舊生帶新生,學校門口,Facebook,Instagram,朋友轉介,其他")
    b.freeze()
    b.table(21, len(samples), "Students")

    # Conditional formatting
    b.cond_format(f"J{b.start+1}:J{MAX_ROWS}", f'$J{b.start+1}="欠費"', RED)
    b.cond_format(f"J{b.start+1}:J{MAX_ROWS}", f'$J{b.start+1}="部分"', ORANGE)
    b.cond_format(f"Q{b.start+1}:Q{MAX_ROWS}", f"AND(Q{b.start+1}<>\"\",Q{b.start+1}<=30,Q{b.start+1}>0)", YELLOW)
    b.cond_format(f"Q{b.start+1}:Q{MAX_ROWS}", f"AND(Q{b.start+1}<>\"\",Q{b.start+1}<=0)", RED)

    # Summary
    sr = b.start + len(samples) + 3
    ws = b.ws
    ws.cell(sr, 1, "月費總額").font = F(bold=True, color=NAVY)
    ws.cell(sr, 9, f"=SUM(I{b.start+1}:I{b.start+len(samples)})").font = F(bold=True, size=12, color=NAVY)
    ws.cell(sr, 9).number_format = "#,##0"
    ws.cell(sr + 1, 1, "在讀人數").font = F(bold=True, color=NAVY)
    ws.cell(sr + 1, 9, f'=COUNTIF(R{b.start+1}:R{MAX_ROWS},"在讀")').font = F(bold=True, color=NAVY)
    ws.cell(sr + 2, 1, "欠費人數").font = F(bold=True, color="DC2626")
    ws.cell(sr + 2, 9, f'=COUNTIF(J{b.start+1}:J{MAX_ROWS},"欠費")').font = F(bold=True, color="DC2626")
    ws.cell(sr + 3, 1, "平均月費 (ARPU)").font = F(bold=True, color=NAVY)
    ws.cell(sr + 3, 9, f'=IFERROR(AVERAGEIF(R{b.start+1}:R{MAX_ROWS},"在讀",I{b.start+1}:I{MAX_ROWS}),0)').font = F(bold=True, color=NAVY)
    ws.cell(sr + 3, 9).number_format = "#,##0"


# ─── 收費記錄 ───────────────────────────────────────────────
def sheet_fees(wb: Workbook):
    ws = wb.create_sheet("收費記錄")
    b = SheetBuilder(ws, "收費記錄", "FPS / PayMe · 自動計算差額及收款狀態", merge_cols=15)
    hdrs = [
        "日期", "收據編號", "學號", "學生姓名", "月份", "課程",
        "應繳金額", "實收金額", "差額", "收款狀態", "付款方式",
        "轉帳參考號", "經手人", "已開收據", "備註",
    ]
    widths = [11, 11, 7, 9, 10, 16, 9, 9, 8, 9, 9, 14, 8, 8, 14]
    b.headers(hdrs, widths)

    samples = [
        ["2026-06-01", None, "S001", None, "2026-06", None, 1980, 1980, None, None, "FPS", "FRN12345", "營運者", "✓", ""],
        ["2026-06-01", None, "S002", None, "2026-06", None, 3180, 3180, None, None, "PayMe", "PM98765", "營運者", "✓", ""],
        ["2026-06-05", None, "S003", None, "2026-06", None, 3180, 0, None, None, "—", "—", "—", "✗", "待追繳"],
        ["2026-06-10", None, "S004", None, "2026-06", None, 1580, 1580, None, None, "FPS", "FRN12399", "營運者", "✓", "半價優惠"],
    ]
    for i, row in enumerate(samples):
        r = b.start + 1 + i
        formulas = {
            2: f'="R-"&RIGHT(E{r},4)&TEXT(ROW()-{b.start},"000")',
            4: f'=IFERROR(VLOOKUP(C{r},學生資料庫!$A${b.start+1}:$B${MAX_ROWS},2,FALSE),"")',
            6: f'=IFERROR(VLOOKUP(C{r},學生資料庫!$A${b.start+1}:$F${MAX_ROWS},6,FALSE),"")',
            9: f'=G{r}-H{r}',
            10: f'=IF(H{r}=0,"未付",IF(H{r}>=G{r},"已付清",IF(H{r}>0,"部分","未付")))',
        }
        b.row(r, row, formulas, alt=i % 2 == 1)

    b.dropdown(11, "FPS,PayMe,現金,支票,—")
    b.dropdown(14, "✓,✗")
    b.freeze()
    b.table(15, len(samples), "Fees")

    b.cond_format(f"J{b.start+1}:J{MAX_ROWS}", f'$J{ b.start+1}="未付"', RED)
    b.cond_format(f"J{b.start+1}:J{MAX_ROWS}", f'$J{ b.start+1}="部分"', ORANGE)
    b.cond_format(f"J{b.start+1}:J{MAX_ROWS}", f'$J{ b.start+1}="已付清"', GREEN)

    sr = b.start + len(samples) + 3
    ws = b.ws
    ws.cell(sr, 1, "本月實收合計").font = F(bold=True, color=NAVY)
    ws.cell(sr, 8, f'=SUMIF(E{b.start+1}:E{MAX_ROWS},TEXT(TODAY(),"YYYY-MM"),H{b.start+1}:H{MAX_ROWS})').font = F(bold=True, size=12, color=NAVY)
    ws.cell(sr, 8).number_format = "#,##0"
    ws.cell(sr + 1, 1, "本月未收合計").font = F(bold=True, color="DC2626")
    ws.cell(sr + 1, 8, f'=SUMIF(E{b.start+1}:E{MAX_ROWS},TEXT(TODAY(),"YYYY-MM"),I{b.start+1}:I{MAX_ROWS})').font = F(bold=True, color="DC2626")
    ws.cell(sr + 1, 8).number_format = "#,##0"


# ─── 出席記錄 ───────────────────────────────────────────────
def sheet_attendance(wb: Workbook):
    ws = wb.create_sheet("出席記錄")
    b = SheetBuilder(ws, "出席記錄", "每日點名 · 自動計算遲到分鐘及月出席率", merge_cols=14)
    hdrs = [
        "日期", "學號", "學生姓名", "課程", "應到時間", "實到時間",
        "遲到(分鐘)", "出席狀態", "離開時間", "功課完成", "導師", "家長已通知", "補課安排", "備註",
    ]
    widths = [11, 7, 9, 15, 9, 9, 8, 9, 9, 9, 8, 9, 10, 14]
    b.headers(hdrs, widths)

    today = date.today().isoformat()
    samples = [
        [today, "S001", None, None, "15:30", "15:25", None, "出席", "18:30", "完成", "導師A", "—", "—", ""],
        [today, "S002", None, None, "16:00", "16:10", None, "遲到", "19:00", "完成", "導師B", "—", "—", ""],
        [today, "S003", None, None, "18:30", "—", None, "缺席", "—", "—", "導師A", "✓", "2026-06-12", "家長已請假"],
        [today, "S004", None, None, "15:30", "15:30", None, "出席", "18:00", "完成", "導師A", "—", "—", ""],
    ]
    for i, row in enumerate(samples):
        r = b.start + 1 + i
        formulas = {
            3: f'=IFERROR(VLOOKUP(B{r},學生資料庫!$A${DATA_START+1}:$B${MAX_ROWS},2,FALSE),"")',
            4: f'=IFERROR(VLOOKUP(B{r},學生資料庫!$A${DATA_START+1}:$F${MAX_ROWS},6,FALSE),"")',
            7: "",  # 遲到分鐘：手動填寫（或使用時間格式後以公式計算）
        }
        b.row(r, row, formulas, alt=i % 2 == 1)

    b.dropdown(8, "出席,遲到,缺席,請假")
    b.dropdown(10, "完成,未完成,部分,—")
    b.dropdown(12, "✓,✗,—")
    b.freeze()
    b.table(14, len(samples), "Attendance")

    b.cond_format(f"H{b.start+1}:H{MAX_ROWS}", f'$H{ b.start+1}="缺席"', RED)
    b.cond_format(f"H{b.start+1}:H{MAX_ROWS}", f'$H{ b.start+1}="遲到"', ORANGE)
    b.cond_format(f"H{b.start+1}:H{MAX_ROWS}", f'$H{ b.start+1}="出席"', GREEN)

    # Monthly attendance summary per student
    sr = b.start + len(samples) + 3
    ws = b.ws
    ws.cell(sr, 1, "本月出席統計（按學號）").font = F(bold=True, size=11, color=NAVY)
    sum_hdrs = ["學號", "姓名", "應到", "出席", "遲到", "缺席", "出席率"]
    for c, h in enumerate(sum_hdrs, 1):
        ws.cell(sr + 1, c, h).font = F(bold=True, color=WHITE)
        ws.cell(sr + 1, c).fill = HDR_FILL
    for i, sid in enumerate(["S001", "S002", "S003", "S004"], 1):
        r = sr + 1 + i
        ws.cell(r, 1, sid)
        ws.cell(r, 2, f'=IFERROR(VLOOKUP(A{r},學生資料庫!$A${DATA_START+1}:$B${MAX_ROWS},2,FALSE),"")')
        ws.cell(r, 3, f'=COUNTIF(B${b.start+1}:B${MAX_ROWS},A{r})')
        ws.cell(r, 4, f'=COUNTIFS(B${b.start+1}:B${MAX_ROWS},A{r},H${b.start+1}:H${MAX_ROWS},"出席")')
        ws.cell(r, 5, f'=COUNTIFS(B${b.start+1}:B${MAX_ROWS},A{r},H${b.start+1}:H${MAX_ROWS},"遲到")')
        ws.cell(r, 6, f'=COUNTIFS(B${b.start+1}:B${MAX_ROWS},A{r},H${b.start+1}:H${MAX_ROWS},"缺席")')
        ws.cell(r, 7, f'=IF(C{r}=0,"—",TEXT(D{r}/C{r},"0%"))')


# ─── 排課表 ───────────────────────────────────────────────
def sheet_schedule(wb: Workbook):
    ws = wb.create_sheet("排課表")
    b = SheetBuilder(ws, "每週排課表", "自動計算滿班率及預估月營收", merge_cols=14)
    hdrs = [
        "星期", "時段", "課程名稱", "課程類別", "導師", "課室",
        "對象", "班額", "已報", "候補", "滿班率", "月費參考", "預估月營收", "狀態", "備註",
    ]
    widths = [7, 12, 17, 9, 8, 7, 8, 5, 5, 5, 7, 9, 10, 7, 12]
    b.headers(hdrs, widths)

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
        r = b.start + 1 + i
        formulas = {
            11: f'=IF(H{r}=0,"—",TEXT(I{r}/H{r},"0%"))',
            13: f'=I{r}*L{r}',
        }
        b.row(r, row, formulas, alt=i % 2 == 1)

    b.dropdown(4, "功課輔導,DSE,習慣養成,體育運動,暑期班,VIP")
    b.dropdown(14, "開班,滿班,候補,暫停,取消")
    b.freeze()
    b.table(15, len(rows), "Schedule")

    b.cond_format(f"K{b.start+1}:K{MAX_ROWS}", f'IFERROR(I{b.start+1}/H{b.start+1},0)>=1', RED)
    b.cond_format(f"K{b.start+1}:K{MAX_ROWS}", f'AND(IFERROR(I{b.start+1}/H{b.start+1},0)>=0.8,IFERROR(I{b.start+1}/H{b.start+1},0)<1)', YELLOW)

    sr = b.start + len(rows) + 3
    ws = b.ws
    ws.cell(sr, 1, "預估月營收合計").font = F(bold=True, color=NAVY)
    ws.cell(sr, 13, f'=SUM(M{b.start+1}:M{b.start+len(rows)})').font = F(bold=True, size=12, color=NAVY)
    ws.cell(sr, 13).number_format = "#,##0"
    ws.cell(sr + 1, 1, "總已報人數").font = F(bold=True)
    ws.cell(sr + 1, 9, f'=SUM(I{b.start+1}:I{b.start+len(rows)})').font = F(bold=True)


# ─── 課室使用表 ───────────────────────────────────────────
def sheet_rooms(wb: Workbook):
    ws = wb.create_sheet("課室使用表")
    b = SheetBuilder(ws, "課室使用表", "每週時段矩陣 · 標示空閒時段供 VIP/興趣班", merge_cols=10)
    hdrs = [
        "星期", "時段", "課室A", "課室A狀態", "課室B", "課室B狀態",
        "VIP室", "VIP室狀態", "負責導師", "每呎產值", "備註",
    ]
    widths = [7, 12, 16, 8, 16, 8, 14, 8, 9, 9, 14]
    b.headers(hdrs, widths)

    rows = [
        ["星期一", "15:30–18:30", "小學功課輔導", "使用中", "中學功課輔導", "使用中", "—", "空閒", "導師A/B", None, ""],
        ["星期一", "18:30–20:30", "DSE英文", "使用中", "—", "空閒", "1對1 VIP", "使用中", "導師A", None, ""],
        ["星期二", "15:30–18:30", "小學功課輔導", "使用中", "中學功課輔導", "使用中", "—", "空閒", "導師A/B", None, ""],
        ["星期三", "15:30–18:30", "小學功課輔導", "使用中", "—", "空閒", "—", "空閒", "導師A", None, "B室可用"],
        ["星期六", "10:00–12:00", "—", "空閒", "習慣班", "使用中", "—", "空閒", "兼職C", None, ""],
        ["星期六", "14:00–18:00", "—", "空閒", "—", "空閒", "1對2 數學", "使用中", "兼職D", None, "週末VIP"],
    ]
    for i, row in enumerate(rows):
        r = b.start + 1 + i
        formulas = {10: f'=IF(D{r}="空閒",200,IF(F{r}="空閒",150,IF(H{r}="空閒",250,100)))'}
        b.row(r, row, formulas, alt=i % 2 == 1)

    b.dropdown(4, "使用中,空閒,清潔中,維修")
    b.dropdown(6, "使用中,空閒,清潔中,維修")
    b.dropdown(8, "使用中,空閒,清潔中,維修")
    b.freeze()

    b.cond_format(f"D{b.start+1}:D{MAX_ROWS}", f'$D{ b.start+1}="空閒"', GREEN)
    b.cond_format(f"F{b.start+1}:F{MAX_ROWS}", f'$F{ b.start+1}="空閒"', GREEN)
    b.cond_format(f"H{b.start+1}:H{MAX_ROWS}", f'$H{ b.start+1}="空閒"', GREEN)

    sr = b.start + len(rows) + 3
    ws = b.ws
    ws.cell(sr, 1, "空閒時段統計").font = F(bold=True, color=NAVY)
    ws.cell(sr, 2, f'=COUNTIF(D{b.start+1}:D{b.start+len(rows)},"空閒")+COUNTIF(F{b.start+1}:F{b.start+len(rows)},"空閒")+COUNTIF(H{b.start+1}:H{b.start+len(rows)},"空閒")').font = F(bold=True)
    ws.cell(sr, 3, "個空閒時段可供 VIP / 興趣班使用").font = F(size=9, color=MUTED)


# ─── 財務月結 ───────────────────────────────────────────────
def sheet_finance(wb: Workbook):
    ws = wb.create_sheet("財務月結")
    b = SheetBuilder(ws, "財務月結表", "自動計算總成本、淨利、淨利率及目標達成率", merge_cols=16)
    hdrs = [
        "月份", "學生數", "ARPU", "月營收", "租金", "全職導師",
        "兼職導師", "水電", "雜費", "推廣", "其他", "總成本",
        "月淨利", "淨利率", "目標達成率", "備註",
    ]
    widths = [9, 7, 8, 10, 8, 9, 9, 7, 7, 7, 7, 10, 10, 8, 9, 14]
    b.headers(hdrs, widths)

    rows = [
        ["2026-06", 50, 3000, 150000, 40000, 45000, 12000, 5500, 5000, 3000, 0, None, None, None, None, "接手首月"],
        ["2026-07", 65, 3231, 210000, 35000, 45000, 20000, 6000, 5000, 5000, 0, None, None, None, None, "暑假高峰"],
        ["2026-08", 70, 3500, 245000, 35000, 45000, 22000, 6000, 5000, 3000, 0, None, None, None, None, "暑假高峰"],
        ["2026-09", 60, 3200, 192000, 35000, 45000, 15000, 5500, 5000, 3000, 0, None, None, None, None, "新學期"],
    ]
    for i, row in enumerate(rows):
        r = b.start + 1 + i
        formulas = {
            12: f"=SUM(E{r}:K{r})",
            13: f"=D{r}-L{r}",
            14: f'=IF(D{r}=0,"—",TEXT(M{r}/D{r},"0%"))',
            15: f"=IFERROR(M{r}/82000,\"—\")",
        }
        b.row(r, row, formulas, alt=i % 2 == 1)

    b.freeze()
    b.table(16, len(rows), "Finance")

    b.cond_format(f"M{b.start+1}:M{MAX_ROWS}", f"M{b.start+1}>=82000", GREEN)
    b.cond_format(f"M{b.start+1}:M{MAX_ROWS}", f"AND(M{b.start+1}<82000,M{b.start+1}>=40000)", YELLOW)
    b.cond_format(f"M{b.start+1}:M{MAX_ROWS}", f"M{b.start+1}<40000", RED)

    sr = b.start + len(rows) + 3
    ws = b.ws
    ws.cell(sr, 1, "年度累積淨利").font = F(bold=True, color=NAVY)
    ws.cell(sr, 13, f'=SUM(M{b.start+1}:M{b.start+len(rows)})').font = F(bold=True, size=12, color=NAVY)
    ws.cell(sr, 13).number_format = "#,##0"
    ws.cell(sr + 1, 1, "平均月淨利").font = F(bold=True)
    ws.cell(sr + 1, 13, f'=AVERAGE(M{b.start+1}:M{b.start+len(rows)})').font = F(bold=True)
    ws.cell(sr + 1, 13).number_format = "#,##0"
    ws.cell(sr + 2, 1, "最佳月份淨利").font = F(bold=True)
    ws.cell(sr + 2, 13, f'=MAX(M{b.start+1}:M{b.start+len(rows)})').font = F(bold=True, color="16A34A")


# ─── 學習進度 ───────────────────────────────────────────────
def sheet_progress(wb: Workbook):
    ws = wb.create_sheet("學習進度")
    b = SheetBuilder(ws, "學習進度報告", "自動生成 WhatsApp 進度訊息 · 每月發送家長", merge_cols=14)
    hdrs = [
        "月份", "學號", "學生姓名", "課程", "出席率", "功課完成率",
        "測驗分數", "上次分數", "進步幅度", "進步重點", "待改善",
        "導師評語", "WhatsApp訊息", "已發送",
    ]
    widths = [9, 7, 9, 14, 8, 10, 9, 9, 8, 16, 12, 16, 30, 7]
    b.headers(hdrs, widths)

    rows = [
        ["2026-06", "S001", None, None, "95%", "90%", 78, 72, None, "數學應用題進步", "中文造句", "表現穩定，繼續保持", None, "✓"],
        ["2026-06", "S002", None, None, "88%", "85%", 72, 68, None, "閱讀理解提升", "寫作結構", "需加強 Past Paper 操練", None, "✓"],
        ["2026-06", "S003", None, None, "70%", "60%", 55, 58, None, "—", "出席率偏低", "請家長協助督促出席", None, "✗"],
    ]
    for i, row in enumerate(rows):
        r = b.start + 1 + i
        formulas = {
            3: f'=IFERROR(VLOOKUP(B{r},學生資料庫!$A${DATA_START+1}:$B${MAX_ROWS},2,FALSE),"")',
            4: f'=IFERROR(VLOOKUP(B{r},學生資料庫!$A${DATA_START+1}:$F${MAX_ROWS},6,FALSE),"")',
            9: f'=IF(OR(G{r}="",H{r}=""),"—",G{r}-H{r})',
            13: (
                f'="【俊才坊學習進度】"&C{r}&"同學 "&A{r}&" 報告："&CHAR(10)&"出席率："&E{r}'
                f'&"  功課："&F{r}&CHAR(10)&"測驗："&G{r}&"分  進步："&J{r}&"  待改善："&K{r}'
                f'&CHAR(10)&"導師評語："&L{r}'
            ),
        }
        b.row(r, row, formulas, alt=i % 2 == 1)

    b.dropdown(14, "✓,✗")
    b.freeze()
    b.table(14, len(rows), "Progress")

    b.cond_format(f"E{b.start+1}:E{MAX_ROWS}", f'VALUE(LEFT(E{b.start+1},LEN(E{b.start+1})-1))<80', ORANGE)
    b.cond_format(f"I{b.start+1}:I{MAX_ROWS}", f"I{b.start+1}<0", RED)
    b.cond_format(f"I{b.start+1}:I{MAX_ROWS}", f"I{b.start+1}>=5", GREEN)


# ─── 每日行政 ───────────────────────────────────────────────
def sheet_daily(wb: Workbook):
    ws = wb.create_sheet("每日行政")
    b = SheetBuilder(ws, "每日行政檢查表", "按時段執行 · 自動計算完成率", merge_cols=8)

    ws.cell(4, 1, "日期：").font = F(bold=True)
    ws.cell(4, 2, date.today().isoformat()).font = F(bold=True, color=NAVY)
    ws.cell(4, 4, "完成率：").font = F(bold=True)
    ws.cell(4, 5, f'=IFERROR(TEXT(COUNTIF(C{b.start+1}:C{b.start+20},"✓")/COUNTA(C{b.start+1}:C{b.start+20}),"0%"),"0%")').font = F(bold=True, size=14, color=NAVY)

    hdrs = ["時段", "任務", "完成?", "用時(分)", "負責人", "相關工作表", "備註"]
    widths = [12, 36, 7, 8, 8, 12, 16]
    b.headers(hdrs, widths)

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
        ["🌙 晚上", "更新學習進度備註（如有測驗/測驗）", "", "", "導師", "學習進度", ""],
    ]
    for i, row in enumerate(tasks):
        b.row(b.start + 1 + i, row, alt=i % 2 == 1)

    b.dropdown(3, "✓,✗,—,進行中")
    b.dropdown(5, "營運者,導師A,導師B,兼職")
    b.freeze()


# ─── 家長通訊 ───────────────────────────────────────────────
def sheet_parents(wb: Workbook):
    ws = wb.create_sheet("家長通訊")
    b = SheetBuilder(ws, "家長通訊記錄", "追蹤回覆時效 · 標記逾期跟進", merge_cols=13)
    hdrs = [
        "日期", "學號", "家長姓名", "聯絡方式", "類型", "優先級",
        "內容摘要", "處理狀態", "回覆時限", "跟進日期", "逾期?", "負責人", "備註",
    ]
    widths = [11, 7, 9, 9, 10, 7, 22, 9, 10, 11, 6, 8, 14]
    b.headers(hdrs, widths)

    rows = [
        ["2026-06-10", "S003", None, "WhatsApp", "欠費提醒", "高", "6月學費未繳，已發提醒", "跟進中", "2026-06-12", "2026-06-15", None, "營運者", ""],
        ["2026-06-10", "S001", None, "WhatsApp", "進度查詢", "中", "查詢數學進度，已回覆", "已完成", "2026-06-10", "—", None, "營運者", ""],
        ["2026-06-11", "—", "王太（新生）", "電話", "招生查詢", "高", "查詢暑假班，已發傳單", "跟進中", "2026-06-13", "2026-06-13", None, "營運者", "潛在新生"],
        ["2026-06-11", "S005", None, "WhatsApp", "續報查詢", "中", "查詢9月學期學費", "待處理", "2026-06-12", "2026-06-14", None, "營運者", ""],
    ]
    for i, row in enumerate(rows):
        r = b.start + 1 + i
        formulas = {
            3: f'=IF(B{r}="","",IFERROR(VLOOKUP(B{r},學生資料庫!$A${DATA_START+1}:$L${MAX_ROWS},12,FALSE),""))',
            11: f'=IF(OR(J{r}="—",J{r}=""),"",IF(AND(H{r}<>"已完成",TODAY()>J{r}),"⚠️",""))',
        }
        b.row(r, row, formulas, alt=i % 2 == 1)

    b.dropdown(5, "欠費提醒,進度查詢,招生查詢,續報查詢,投訴,其他")
    b.dropdown(6, "高,中,低")
    b.dropdown(8, "已完成,跟進中,待處理")
    b.freeze()
    b.table(13, len(rows), "Parents")

    b.cond_format(f"F{b.start+1}:F{MAX_ROWS}", f'$F{ b.start+1}="高"', RED)
    b.cond_format(f"K{b.start+1}:K{MAX_ROWS}", f'$K{ b.start+1}="⚠️"', RED)


# ─── 導師資料 ───────────────────────────────────────────────
def sheet_tutors(wb: Workbook):
    ws = wb.create_sheet("導師資料")
    b = SheetBuilder(ws, "導師及員工資料", "合約到期提醒 · 學生數及成本估算", merge_cols=14)
    hdrs = [
        "編號", "姓名", "職位", "電話", "負責課程", "負責學生數",
        "薪酬", "月薪估算", "入職日期", "合約到期", "合約剩餘天數",
        "通知期", "狀態", "備註",
    ]
    widths = [7, 9, 10, 12, 18, 8, 12, 10, 11, 11, 9, 8, 7, 16]
    b.headers(hdrs, widths)

    rows = [
        ["T001", "導師A", "全職導師", "9XXX XXXX", "功課輔導、DSE", None, "$22,500/月", 22500, "2020-03-01", "2026-12-31", None, "2個月", "在職", "核心導師"],
        ["T002", "導師B", "全職導師", "9XXX XXXX", "功課輔導、DSE", None, "$22,500/月", 22500, "2019-09-01", "2026-12-31", None, "2個月", "在職", "核心導師"],
        ["T003", "兼職C", "兼職導師", "9XXX XXXX", "習慣班", None, "$150/時", None, "2025-01-01", "—", None, "1個月", "在職", ""],
        ["T004", "兼職D", "兼職導師", "9XXX XXXX", "籃球班", None, "$200/時", None, "2025-06-01", "—", None, "1個月", "在職", "外聘教練"],
    ]
    for i, row in enumerate(rows):
        r = b.start + 1 + i
        formulas = {
            6: f'=COUNTIF(學生資料庫!S{b.start+1}:S{MAX_ROWS},B{r})',
            8: f'=IF(ISNUMBER(SEARCH("/月",G{r})),VALUE(SUBSTITUTE(SUBSTITUTE(G{r},"$",""),"/月","")),"")',
            11: f'=IF(J{r}="—","",IF(J{r}="","",J{r}-TODAY()))',
        }
        b.row(r, row, formulas, alt=i % 2 == 1)

    b.dropdown(13, "在職,離職,試用,顧問")
    b.freeze()
    b.table(14, len(rows), "Tutors")

    b.cond_format(f"K{b.start+1}:K{MAX_ROWS}", f'AND(K{b.start+1}<>"",K{b.start+1}<=60,K{b.start+1}>0)', YELLOW)
    b.cond_format(f"K{b.start+1}:K{MAX_ROWS}", f'AND(K{b.start+1}<>"",K{b.start+1}<=0)', RED)

    sr = b.start + len(rows) + 3
    ws = b.ws
    ws.cell(sr, 1, "全職導師月薪合計").font = F(bold=True, color=NAVY)
    ws.cell(sr, 8, f'=SUMIF(C{b.start+1}:C{b.start+len(rows)},"全職導師",H{b.start+1}:H{b.start+len(rows)})').font = F(bold=True, size=12, color=NAVY)
    ws.cell(sr, 8).number_format = "#,##0"


# ─── 使用說明 ───────────────────────────────────────────────
def sheet_readme(wb: Workbook):
    ws = wb.create_sheet("使用說明")
    ws.column_dimensions["A"].width = 16
    ws.column_dimensions["B"].width = 22
    ws.column_dimensions["C"].width = 50
    ws["A1"] = "俊才坊行政系統"
    ws["A1"].font = F(bold=True, size=16, color=NAVY)
    ws["A2"] = "Upgrade Edition v2.0 · 2026"
    ws["A2"].font = F(size=10, color=MUTED)

    hdrs = ["工作表", "升級功能", "使用說明"]
    for c, h in enumerate(hdrs, 1):
        ws.cell(4, c, h).font = F(bold=True, color=WHITE)
        ws.cell(4, c).fill = HDR_FILL

    features = [
        ("儀表板", "即時 KPI、待處理提醒、財務目標", "每日開啟第一頁，掌握中心狀態"),
        ("學生資料庫", "合約倒數、ARPU統計、欠費標紅、轉介來源", "★ 接手首週必完成"),
        ("收費記錄", "自動收據編號、VLOOKUP姓名、差額/狀態自動計算", "每次收款即時記錄"),
        ("出席記錄", "遲到分鐘、月出席率統計、補課安排", "每日放學後更新"),
        ("排課表", "滿班率、預估月營收、候補人數", "每學期更新"),
        ("課室使用表", "空閒時段標綠、每呎產值估算", "週末規劃VIP用"),
        ("財務月結", "自動總成本/淨利/達成率、年度累計", "每月底結算"),
        ("學習進度", "自動生成WhatsApp訊息、進步幅度", "每月25-28日發送"),
        ("每日行政", "完成率自動計算、關聯工作表", "每日按時段執行"),
        ("家長通訊", "優先級標色、逾期提醒", "每次通訊後記錄"),
        ("導師資料", "負責學生數、合約倒數、月薪合計", "接手時核查合約"),
    ]
    for i, (name, upgrade, usage) in enumerate(features, 5):
        ws.cell(i, 1, name).font = F(bold=True, color=NAVY)
        ws.cell(i, 2, upgrade).font = F(size=9)
        ws.cell(i, 3, usage).font = F(size=9, color=MUTED)
        if i % 2 == 0:
            for c in range(1, 4):
                ws.cell(i, c).fill = ALT_FILL

    r = 5 + len(features) + 2
    ws.cell(r, 1, "實施順序").font = F(bold=True, size=12, color=NAVY)
    steps = [
        ("Day 1", "開啟儀表板 → 填入學生資料庫 → 設置 WhatsApp Business"),
        ("Week 1", "收費記錄 + 導師資料 + 每日行政"),
        ("Week 2", "排課表 + 出席記錄 + 課室使用表"),
        ("Week 3", "上傳 Google Sheets + 安裝 Apps Script"),
        ("Monthly", "學習進度報告 + 財務月結"),
    ]
    for i, (when, what) in enumerate(steps, r + 1):
        ws.cell(i, 1, when).font = F(bold=True)
        ws.cell(i, 2, what).font = F(size=9)
        ws.merge_cells(start_row=i, start_column=2, end_row=i, end_column=3)


def main():
    wb = Workbook()
    # Remove default sheet after creating others
    sheet_dashboard(wb)
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
