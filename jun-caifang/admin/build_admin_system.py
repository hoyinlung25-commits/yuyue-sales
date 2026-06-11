#!/usr/bin/env python3
"""Build 俊才坊行政系統 Excel workbook."""

from __future__ import annotations

from datetime import date
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

OUT = Path(__file__).parent / "output"
OUT.mkdir(exist_ok=True)

NAVY = "1E3A5F"
GOLD = "D4A843"
WHITE = "FFFFFF"
ALT = "F8FAFC"
GREEN = "DCFCE7"
RED = "FEE2E2"
YELLOW = "FEF3C7"

THIN = Side(style="thin", color="CBD5E0")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
TITLE_FONT = Font(name="Calibri", bold=True, size=14, color=NAVY)
HDR_FONT = Font(name="Calibri", bold=True, size=10, color=WHITE)
BODY_FONT = Font(name="Calibri", size=10)
HDR_FILL = PatternFill("solid", fgColor=NAVY)
ALT_FILL = PatternFill("solid", fgColor=ALT)


def style_header(ws, row: int, headers: list[str], widths: list[int] | None = None):
    for col, h in enumerate(headers, 1):
        cell = ws.cell(row=row, column=col, value=h)
        cell.font = HDR_FONT
        cell.fill = HDR_FILL
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = BORDER
        if widths and col <= len(widths):
            ws.column_dimensions[get_column_letter(col)].width = widths[col - 1]
    ws.row_dimensions[row].height = 28


def add_rows(ws, start_row: int, rows: list[list], alt: bool = True):
    for i, row_data in enumerate(rows):
        r = start_row + i
        for col, val in enumerate(row_data, 1):
            cell = ws.cell(row=r, column=col, value=val)
            cell.font = BODY_FONT
            cell.border = BORDER
            cell.alignment = Alignment(vertical="center", wrap_text=True)
            if alt and i % 2 == 1:
                cell.fill = ALT_FILL


def add_title(ws, title: str, subtitle: str = ""):
    ws.merge_cells("A1:H1")
    ws["A1"] = f"俊才坊補習社 · {title}"
    ws["A1"].font = TITLE_FONT
    if subtitle:
        ws.merge_cells("A2:H2")
        ws["A2"] = subtitle
        ws["A2"].font = Font(name="Calibri", size=10, color="64748B")
        return 4
    return 3


def sheet_students(wb: Workbook):
    ws = wb.active
    ws.title = "學生資料庫"
    start = add_title(ws, "學生資料庫", "主要業務資產 · 接手後第一週必須完成")
    headers = [
        "學號", "中文姓名", "就讀學校", "年級", "報讀課程",
        "上課日", "月費", "付款狀態", "家長姓名", "家長電話",
        "WhatsApp", "入學日期", "合約到期", "導師", "備註",
    ]
    widths = [8, 10, 14, 6, 18, 10, 8, 10, 10, 14, 8, 12, 12, 10, 20]
    style_header(ws, start, headers, widths)
    sample = [
        ["S001", "陳小明", "九龍塘官小", "P5", "小學功課輔導（每日）", "一至五", 1980, "已付", "陳太", "9123 4567", "✓", "2024-09-01", "2026-08-31", "導師A", "舊生"],
        ["S002", "李美儀", "喇沙書院", "S3", "中學功課輔導+DSE英文", "一至五", 3180, "已付", "李先生", "6234 5678", "✓", "2023-02-01", "2026-08-31", "導師B", ""],
        ["S003", "黃俊軒", "瑪利諾中學", "S5", "DSE三科套餐", "一至六", 3180, "欠費", "黃太", "5345 6789", "✓", "2024-01-15", "2026-08-31", "導師A", "欠9月學費"],
    ]
    add_rows(ws, start + 1, sample)
    dv = DataValidation(type="list", formula1='"已付,欠費,部分,豁免"', allow_blank=True)
    ws.add_data_validation(dv)
    dv.add(f"H{start+1}:H500")
    ws.freeze_panes = f"A{start+1}"


def sheet_fees(wb: Workbook):
    ws = wb.create_sheet("收費記錄")
    start = add_title(ws, "收費記錄", "FPS / PayMe 轉帳 · 每月初發繳費通知")
    headers = [
        "日期", "學號", "學生姓名", "月份", "課程", "應繳金額",
        "實收金額", "付款方式", "轉帳參考號", "經手人", "收據編號", "備註",
    ]
    widths = [12, 8, 10, 10, 18, 10, 10, 10, 16, 8, 12, 16]
    style_header(ws, start, headers, widths)
    sample = [
        ["2026-06-01", "S001", "陳小明", "2026-06", "小學功課輔導", 1980, 1980, "FPS", "FRN12345", "營運者", "R-06001", ""],
        ["2026-06-01", "S002", "李美儀", "2026-06", "功課+DSE英文", 3180, 3180, "PayMe", "PM98765", "營運者", "R-06002", ""],
        ["2026-06-05", "S003", "黃俊軒", "2026-06", "DSE三科套餐", 3180, 0, "—", "—", "—", "—", "待追繳"],
    ]
    add_rows(ws, start + 1, sample)
    ws.freeze_panes = f"A{start+1}"


def sheet_attendance(wb: Workbook):
    ws = wb.create_sheet("出席記錄")
    start = add_title(ws, "出席記錄", "每日點名 · 放學後更新")
    headers = [
        "日期", "學號", "學生姓名", "課程", "應到時間", "實到時間",
        "出席狀態", "離開時間", "導師", "功課完成", "備註",
    ]
    widths = [12, 8, 10, 18, 10, 10, 10, 10, 10, 10, 16]
    style_header(ws, start, headers, widths)
    today = date.today().isoformat()
    sample = [
        [today, "S001", "陳小明", "小學功課輔導", "15:30", "15:25", "出席", "18:30", "導師A", "完成", ""],
        [today, "S002", "李美儀", "中學功課輔導", "16:00", "16:10", "遲到", "19:00", "導師B", "完成", "遲10分鐘"],
        [today, "S003", "黃俊軒", "DSE精讀班", "18:30", "—", "缺席", "—", "導師A", "—", "家長已通知"],
    ]
    add_rows(ws, start + 1, sample)
    dv = DataValidation(type="list", formula1='"出席,遲到,缺席,請假"', allow_blank=True)
    ws.add_data_validation(dv)
    dv.add(f"G{start+1}:G500")
    ws.freeze_panes = f"A{start+1}"


def sheet_schedule(wb: Workbook):
    ws = wb.create_sheet("排課表")
    start = add_title(ws, "每週排課表", "避免撞堂 · 同步 Google Calendar")
    headers = [
        "星期", "時段", "課程名稱", "導師", "課室", "對象",
        "班額", "已報", "狀態", "備註",
    ]
    widths = [8, 14, 20, 10, 8, 10, 6, 6, 8, 16]
    style_header(ws, start, headers, widths)
    rows = [
        ["星期一", "15:30–18:30", "小學功課輔導", "導師A", "課室A", "P1–P6", 12, 10, "開班", ""],
        ["星期一", "16:00–19:00", "中學功課輔導", "導師B", "課室B", "S1–S3", 10, 8, "開班", ""],
        ["星期一", "18:30–20:30", "DSE 英文", "導師A", "課室A", "S4–S6", 12, 9, "開班", ""],
        ["星期二", "18:30–20:30", "DSE 中文", "導師B", "課室B", "S4–S6", 12, 7, "開班", ""],
        ["星期三", "18:30–20:30", "DSE 英文", "導師A", "課室A", "S4–S6", 12, 9, "開班", ""],
        ["星期四", "18:30–20:30", "DSE 中文", "導師B", "課室B", "S4–S6", 12, 7, "開班", ""],
        ["星期五", "18:30–20:30", "DSE 數學", "導師A", "課室A", "S4–S6", 12, 8, "開班", ""],
        ["星期六", "10:00–12:00", "時間管理習慣班", "兼職C", "課室B", "P1–S3", 10, 6, "開班", ""],
        ["星期六", "14:00–16:00", "籃球基礎班", "兼職D", "戶外", "P1–S6", 12, 8, "開班", ""],
        ["星期日", "10:00–12:00", "專注力學習班", "兼職C", "課室A", "P1–S3", 10, 5, "開班", ""],
    ]
    add_rows(ws, start + 1, rows)
    ws.freeze_panes = f"A{start+1}"


def sheet_rooms(wb: Workbook):
    ws = wb.create_sheet("課室使用表")
    start = add_title(ws, "課室使用表", "主課室A · 主課室B · 多用途VIP室")
    headers = ["日期", "時段", "課室A", "課室B", "VIP室", "負責導師", "備註"]
    widths = [12, 14, 18, 18, 18, 10, 16]
    style_header(ws, start, headers, widths)
    rows = [
        ["星期一", "15:30–18:30", "小學功課輔導", "中學功課輔導", "—", "導師A/B", ""],
        ["星期一", "18:30–20:30", "DSE英文", "—", "1對1 VIP", "導師A", ""],
        ["星期六", "10:00–12:00", "—", "習慣班", "—", "兼職C", ""],
        ["星期六", "14:00–18:00", "—", "—", "1對2 數學", "兼職D", "週末VIP"],
    ]
    add_rows(ws, start + 1, rows)


def sheet_finance(wb: Workbook):
    ws = wb.create_sheet("財務月結")
    start = add_title(ws, "財務月結表", "每月底結算 · 對比目標月淨利")
    headers = [
        "月份", "學生數", "月營收", "租金", "全職導師",
        "兼職導師", "水電", "雜費", "推廣", "總成本", "月淨利", "淨利率", "備註",
    ]
    widths = [10, 8, 10, 8, 10, 10, 8, 8, 8, 10, 10, 8, 16]
    style_header(ws, start, headers, widths)
    rows = [
        ["2026-06", 50, 150000, 40000, 45000, 12000, 5500, 5000, 3000, 110500, 39500, "26%", "接手首月"],
        ["2026-07", 65, 210000, 35000, 45000, 20000, 6000, 5000, 5000, 116000, 94000, "45%", "暑假高峰"],
        ["2026-08", 70, 245000, 35000, 45000, 22000, 6000, 5000, 3000, 116000, 129000, "53%", "暑假高峰"],
        ["2026-09", 60, 192000, 35000, 45000, 15000, 5500, 5000, 3000, 108500, 83500, "43%", "新學期"],
    ]
    add_rows(ws, start + 1, rows)


def sheet_progress(wb: Workbook):
    ws = wb.create_sheet("學習進度")
    start = add_title(ws, "學習進度報告", "每月 WhatsApp 發送給家長")
    headers = [
        "月份", "學號", "學生姓名", "課程", "出席率",
        "功課完成率", "測驗分數", "進步重點", "待改善", "導師評語", "已發送",
    ]
    widths = [10, 8, 10, 18, 8, 10, 10, 20, 16, 20, 8]
    style_header(ws, start, headers, widths)
    rows = [
        ["2026-06", "S001", "陳小明", "小學功課輔導", "95%", "90%", "78/100",
         "數學應用題進步", "中文造句", "表現穩定，繼續保持", "✓"],
        ["2026-06", "S002", "李美儀", "DSE英文", "88%", "85%", "B+", "閱讀理解提升", "寫作結構", "需加強 Past Paper 操練", "✓"],
    ]
    add_rows(ws, start + 1, rows)
    dv = DataValidation(type="list", formula1='"✓,✗"', allow_blank=True)
    ws.add_data_validation(dv)
    dv.add(f"K{start+1}:K500")


def sheet_daily(wb: Workbook):
    ws = wb.create_sheet("每日行政")
    start = add_title(ws, "每日行政檢查表", "營運者每日 1–2 小時 · 按時段執行")
    headers = ["時段", "任務", "完成?", "時間", "備註"]
    widths = [10, 40, 8, 10, 20]
    style_header(ws, start, headers, widths)
    tasks = [
        ["早上（開門前）", "確認當日課表，通知所有導師", "", "", ""],
        ["早上", "檢查前日收費記錄，列出欠費名單", "", "", ""],
        ["早上", "回覆 WhatsApp 家長查詢（限時30分鐘內）", "", "", ""],
        ["下午（上課中）", "學生到達點名，記錄出席", "", "", ""],
        ["下午", "確保課室整潔、教材準備充足", "", "", ""],
        ["下午", "處理即時家長查詢", "", "", ""],
        ["晚上（收班後）", "更新出席記錄至系統", "", "", ""],
        ["晚上", "整理當日收費，核對轉帳", "", "", ""],
        ["晚上", "規劃翌日課堂，如有補課提前通知", "", "", ""],
        ["晚上", "更新學習進度備註（如有測驗）", "", "", ""],
    ]
    add_rows(ws, start + 1, tasks)
    dv = DataValidation(type="list", formula1='"✓,✗,—"', allow_blank=True)
    ws.add_data_validation(dv)
    dv.add(f"C{start+1}:C50")


def sheet_parents(wb: Workbook):
    ws = wb.create_sheet("家長通訊")
    start = add_title(ws, "家長通訊記錄", "WhatsApp Business 官方帳號")
    headers = [
        "日期", "學號", "家長姓名", "聯絡方式", "類型",
        "內容摘要", "處理狀態", "跟進日期", "負責人", "備註",
    ]
    widths = [12, 8, 10, 10, 10, 24, 10, 12, 8, 16]
    style_header(ws, start, headers, widths)
    rows = [
        ["2026-06-10", "S003", "黃太", "WhatsApp", "欠費提醒", "9月學費未繳，已發提醒", "跟進中", "2026-06-15", "營運者", ""],
        ["2026-06-10", "S001", "陳太", "WhatsApp", "進度查詢", "查詢數學進度，已回覆", "已完成", "—", "營運者", ""],
        ["2026-06-11", "—", "王太（新生）", "電話", "招生查詢", "查詢暑假班，已發傳單", "跟進中", "2026-06-13", "營運者", "潛在新生"],
    ]
    add_rows(ws, start + 1, rows)
    dv = DataValidation(type="list", formula1='"已完成,跟進中,待處理"', allow_blank=True)
    ws.add_data_validation(dv)
    dv.add(f"G{start+1}:G500")


def sheet_tutors(wb: Workbook):
    ws = wb.create_sheet("導師資料")
    start = add_title(ws, "導師及員工資料", "薪酬、合約、通知期記錄")
    headers = [
        "編號", "姓名", "職位", "電話", "負責課程",
        "月薪/時薪", "入職日期", "合約到期", "通知期", "狀態", "備註",
    ]
    widths = [8, 10, 12, 14, 20, 12, 12, 12, 8, 8, 20]
    style_header(ws, start, headers, widths)
    rows = [
        ["T001", "導師A", "全職導師", "9XXX XXXX", "功課輔導、DSE", "$22,500/月", "2020-03-01", "2026-12-31", "2個月", "在職", "核心導師"],
        ["T002", "導師B", "全職導師", "9XXX XXXX", "功課輔導、DSE", "$22,500/月", "2019-09-01", "2026-12-31", "2個月", "在職", "核心導師"],
        ["T003", "兼職C", "兼職導師", "9XXX XXXX", "習慣班", "$150/時", "2025-01-01", "—", "1個月", "在職", ""],
        ["T004", "兼職D", "兼職導師", "9XXX XXXX", "籃球班", "$200/時", "2025-06-01", "—", "1個月", "在職", "外聘教練"],
    ]
    add_rows(ws, start + 1, rows)


def sheet_readme(wb: Workbook):
    ws = wb.create_sheet("使用說明", 0)
    ws.column_dimensions["A"].width = 18
    ws.column_dimensions["B"].width = 60
    ws["A1"] = "俊才坊行政系統"
    ws["A1"].font = Font(name="Calibri", bold=True, size=16, color=NAVY)
    lines = [
        ("版本", "Upgrade Edition v1.0 · 2026"),
        ("用途", "接手後數碼化行政，一人管理 50–70 名學生"),
        ("", ""),
        ("工作表一覽", ""),
        ("學生資料庫", "所有學生及家長聯絡 · 第一週必完成"),
        ("收費記錄", "FPS/PayMe 轉帳記錄 · 每月初發繳費通知"),
        ("出席記錄", "每日點名 · 放學後更新"),
        ("排課表", "每週課程安排 · 同步 Google Calendar"),
        ("課室使用表", "避免撞堂 · 最大化空間產值"),
        ("財務月結", "每月底 P&L 結算"),
        ("學習進度", "每月 WhatsApp 進度報告"),
        ("每日行政", "營運者每日檢查清單"),
        ("家長通訊", "查詢、欠費、招生記錄"),
        ("導師資料", "薪酬、合約、通知期"),
        ("", ""),
        ("實施順序", ""),
        ("Week 1", "學生資料庫 + 收費記錄 + WhatsApp Business"),
        ("Week 2–3", "排課表 + 出席記錄 + 課室使用表"),
        ("Month 1–2", "學習進度 + 財務月結 + 家長通訊"),
        ("", ""),
        ("Google Sheets", "可將各表上傳至 Google Drive 共用"),
        ("備份", "每週五備份至 Google Drive / 本地"),
    ]
    for i, (k, v) in enumerate(lines, 3):
        ws.cell(row=i, column=1, value=k).font = Font(bold=bool(k and k not in ("", "工作表一覽", "實施順序")))
        ws.cell(row=i, column=2, value=v).font = BODY_FONT


def main():
    wb = Workbook()
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

    out = OUT / "俊才坊行政系統.xlsx"
    wb.save(out)
    print(f"Saved {out}")


if __name__ == "__main__":
    main()
