#!/usr/bin/env python3
"""Build a beautiful, user-friendly client_base.xlsx."""

from __future__ import annotations

from datetime import datetime

from openpyxl import Workbook
from openpyxl.formatting.rule import FormulaRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.worksheet.table import Table, TableStyleInfo

# Brand colours
NAVY = "1A365D"
NAVY_LIGHT = "2C5282"
GOLD = "D69E2E"
WHITE = "FFFFFF"
ROW_ALT = "F7FAFC"
ROW_NEW = "E6FFFA"
HOT_BG = "FED7D7"
CLIENT_BG = "C6F6D5"
WARM_BG = "FEEBC8"
LOW_BG = "EDF2F7"

FONT = "Calibri"
THIN = Side(style="thin", color="CBD5E0")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)

# Main table columns (user-friendly order)
CLIENT_HEADERS = [
    "Rank",
    "Category",
    "Score",
    "Next Action",
    "Stage",
    "Client?",
    "English Name",
    "Nickname",
    "Phone",
    "Gender",
    "Age",
    "Relationship",
    "Rel (1-5)",
    "Poss (1-5)",
    "Job",
    "Area",
    "Income",
    "Product Interest",
    "Remarks",
    "Last Note",
    "L0",
    "L1",
    "L2",
]

# Map from OUT_HEADERS indices in upgrade_pipeline rows
# 0 rank, 1 cat, 2 score, 3 next, 4 stage, 5 is client, 6 policy match, 7 products,
# 8 en, 9 nick, 10 phone, ...
def slim_row(full: list) -> list:
    return [
        full[0],
        full[1],
        full[2],
        full[3],
        full[4],
        full[5],
        full[8],
        full[9],
        full[10],
        full[11],
        full[12],
        full[13],
        full[14],
        full[15],
        full[16],
        full[17],
        full[18],
        full[7],
        full[19],
        full[20],
        full[23],
        full[24],
        full[25],
    ]


def _fill(hex_color: str) -> PatternFill:
    return PatternFill(start_color=hex_color, end_color=hex_color, fill_type="solid")


def _font(bold=False, size=11, color="000000") -> Font:
    return Font(name=FONT, bold=bold, size=size, color=color)


def style_header_row(ws, row: int, ncol: int) -> None:
    for c in range(1, ncol + 1):
        cell = ws.cell(row=row, column=c)
        cell.fill = _fill(NAVY)
        cell.font = _font(bold=True, size=11, color=WHITE)
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = BORDER


def set_col_widths(ws, widths: dict[int, float]) -> None:
    for col, w in widths.items():
        ws.column_dimensions[get_column_letter(col)].width = w


def add_list_validation(ws, cell_range: str, options: str) -> None:
    dv = DataValidation(type="list", formula1=f'"{options}"', allow_blank=True)
    dv.error = "Please pick from the list"
    dv.errorTitle = "Invalid value"
    ws.add_data_validation(dv)
    dv.add(cell_range)


def build_guide(wb: Workbook) -> None:
    ws = wb.create_sheet("Start Here", 0)
    ws.sheet_properties.tabColor = GOLD
    ws.merge_cells("A1:F1")
    t = ws["A1"]
    t.value = "Client Base — Welcome"
    t.font = _font(bold=True, size=22, color=NAVY)
    t.alignment = Alignment(horizontal="left", vertical="center")
    ws.row_dimensions[1].height = 40

    steps = [
        ("", ""),
        ("Quick start", ""),
        ("1", "Add a new person → open sheet 「➕ Add New Client」, fill the yellow form."),
        ("2", "Click 「Add to Client List」 area → copy the green row → paste into 「Clients」 first empty row."),
        ("3", "Work daily from 「This Week」 or sort 「Clients」 by Score (column C)."),
        ("4", "Policyholders are in 「Policies」 tab."),
        ("", ""),
        ("Tips", ""),
        ("•", "Use dropdowns for Category, Stage, Gender — fewer typos."),
        ("•", "Rows colour automatically: Hot = red tint, Client = green, Warm = orange."),
        ("•", "Refresh data from Google: run upgrade_pipeline.py in client-base folder."),
        ("", ""),
        ("Updated", datetime.now().strftime("%Y-%m-%d %H:%M")),
    ]
    for i, (a, b) in enumerate(steps, 3):
        ws.cell(row=i, column=1, value=a).font = _font(bold=a in ("Quick start", "Tips"))
        ws.cell(row=i, column=2, value=b).font = _font(size=11)
        ws.merge_cells(start_row=i, start_column=2, end_row=i, end_column=6)
    set_col_widths(ws, {1: 6, 2: 72})


def build_dashboard(wb: Workbook, rows: list[list]) -> None:
    ws = wb.create_sheet("Dashboard")
    ws.sheet_properties.tabColor = NAVY_LIGHT

    ws.merge_cells("A1:H1")
    ws["A1"].value = "Sales Pipeline Overview"
    ws["A1"].font = _font(bold=True, size=20, color=WHITE)
    ws["A1"].fill = _fill(NAVY)
    ws["A1"].alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[1].height = 44

    hot = sum(1 for r in rows if r[1] == "Hot")
    warm = sum(1 for r in rows if r[1] == "Warm")
    nurture = sum(1 for r in rows if r[1] == "Nurture")
    clients = sum(1 for r in rows if r[1] == "Client")
    low = sum(1 for r in rows if r[1] == "Low")
    with_action = sum(1 for r in rows if r[3])
    l1l2 = sum(1 for r in rows if r[4] in ("L1", "L2", "L3"))

    cards = [
        ("Total Contacts", len(rows), NAVY_LIGHT),
        ("Hot Leads", hot, "C53030"),
        ("Warm", warm, "DD6B20"),
        ("Clients", clients, "276749"),
        ("Need Action", with_action, "6B46C1"),
        ("L1 / L2 / L3", l1l2, "2B6CB0"),
    ]
    col = 1
    for label, val, color in cards:
        ws.merge_cells(start_row=3, start_column=col, end_row=4, end_column=col + 1)
        box = ws.cell(row=3, column=col)
        box.value = label
        box.font = _font(bold=True, size=11, color=WHITE)
        box.fill = _fill(color)
        box.alignment = Alignment(horizontal="center", vertical="top", wrap_text=True)
        ws.merge_cells(start_row=5, start_column=col, end_row=6, end_column=col + 1)
        val_cell = ws.cell(row=5, column=col)
        val_cell.value = val
        val_cell.font = _font(bold=True, size=28, color=WHITE)
        val_cell.fill = _fill(color)
        val_cell.alignment = Alignment(horizontal="center", vertical="center")
        col += 2

    ws["A8"] = "Category breakdown"
    ws["A8"].font = _font(bold=True, size=12)
    breakdown = [("Hot", hot), ("Warm", warm), ("Nurture", nurture), ("Client", clients), ("Low", low)]
    for i, (name, cnt) in enumerate(breakdown, 9):
        ws.cell(row=i, column=1, value=name).font = _font(bold=True)
        ws.cell(row=i, column=2, value=cnt)
        if len(rows):
            ws.cell(row=i, column=3, value=round(100 * cnt / len(rows), 1))
            ws.cell(row=i, column=3).number_format = '0.0"%"'

    ws["A16"] = "Go to sheet →"
    ws["B16"] = "Clients (full list)"
    ws["B17"] = "➕ Add New Client"
    ws["B18"] = "This Week"
    for r in (16, 17, 18):
        ws.cell(row=r, column=2).font = _font(bold=True, color=NAVY_LIGHT)

    set_col_widths(ws, {1: 18, 2: 14, 3: 10})


def build_add_client(wb: Workbook) -> None:
    ws = wb.create_sheet("➕ Add New Client")
    ws.sheet_properties.tabColor = "38A169"

    ws.merge_cells("B1:E1")
    ws["B1"].value = "➕ Add New Client"
    ws["B1"].font = _font(bold=True, size=18, color=WHITE)
    ws["B1"].fill = _fill("276749")
    ws["B1"].alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[1].height = 40

    ws.merge_cells("B2:E2")
    ws["B2"].value = (
        "Step 1: Fill yellow cells  |  Step 2: Copy the green row below  |  "
        "Step 3: Paste into 「Clients」 in the first empty green row at the bottom"
    )
    ws["B2"].alignment = Alignment(wrap_text=True, vertical="center")
    ws.row_dimensions[2].height = 36

    ws["B3"] = "Field"
    ws["C3"] = "Your input"
    style_header_row(ws, 3, 3)

    labels = [
        "English Name *",
        "Nickname",
        "Phone (8 digits)",
        "Gender",
        "Age",
        "Relationship",
        "Rel score (1-5)",
        "Possibility (1-5)",
        "Category",
        "Stage",
        "Next Action",
        "Job",
        "Area",
        "Income",
        "Product Interest",
        "Remarks",
    ]
    first_in = 4
    for i, label in enumerate(labels):
        r = first_in + i
        ws.cell(row=r, column=2, value=label).font = _font(bold=True)
        ws.cell(row=r, column=2).alignment = Alignment(vertical="center")
        inp = ws.cell(row=r, column=3)
        inp.fill = _fill("FFFFF0")
        inp.border = BORDER

    add_list_validation(ws, "C7", "Male,Female,Other")
    add_list_validation(ws, "C12", "Hot,Warm,Nurture,Low,Client")
    add_list_validation(ws, "C13", "NEW,L0,L1,L2,L3")

    paste_hdr = first_in + len(labels) + 2
    ws.merge_cells(start_row=paste_hdr, start_column=2, end_row=paste_hdr, end_column=6)
    ws.cell(row=paste_hdr, column=2, value="▼ Copy this row (select entire row) → paste in Clients").font = _font(
        bold=True, color="C53030", size=12
    )

    hdr_row = paste_hdr + 1
    paste_row = paste_hdr + 2
    for c, h in enumerate(CLIENT_HEADERS, 1):
        ws.cell(row=hdr_row, column=c, value=h)
    style_header_row(ws, hdr_row, len(CLIENT_HEADERS))

    # C4..C19 map to form fields
    fr = first_in
    formulas = [
        "",
        f"$C${fr + 8}",  # Category
        f'=IF($C${fr + 6}="","",$C${fr + 6}+$C${fr + 7})',  # Score
        f"$C${fr + 10}",  # Next action
        f"$C${fr + 9}",  # Stage
        "",
        f"$C${fr}",
        f"$C${fr + 1}",
        f"$C${fr + 2}",
        f"$C${fr + 3}",
        f"$C${fr + 4}",
        f"$C${fr + 5}",
        f"$C${fr + 6}",
        f"$C${fr + 7}",
        f"$C${fr + 11}",
        f"$C${fr + 12}",
        f"$C${fr + 13}",
        f"$C${fr + 14}",
        f"$C${fr + 15}",
        "",
        "",
        "",
        "",
    ]
    for c, fml in enumerate(formulas, 1):
        cell = ws.cell(row=paste_row, column=c)
        if fml:
            cell.value = f"={fml}" if not fml.startswith("=") else fml
        cell.fill = _fill(ROW_NEW)
        cell.border = BORDER
        cell.font = _font(size=11)

    set_col_widths(ws, {2: 26, 3: 34})
    for c in range(1, len(CLIENT_HEADERS) + 1):
        ws.column_dimensions[get_column_letter(c)].width = 13


def build_clients_sheet(wb: Workbook, rows: list[list]) -> int:
    ws = wb.create_sheet("Clients")
    ws.sheet_properties.tabColor = NAVY

    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=len(CLIENT_HEADERS))
    banner = ws["A1"]
    banner.value = "Client Pipeline  |  徐語希管理組 · 龍浩賢"
    banner.font = _font(bold=True, size=14, color=WHITE)
    banner.fill = _fill(NAVY)
    banner.alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[1].height = 32

    header_row = 2
    for c, h in enumerate(CLIENT_HEADERS, 1):
        ws.cell(row=header_row, column=c, value=h)
    style_header_row(ws, header_row, len(CLIENT_HEADERS))

    slim = [slim_row(r) for r in rows]
    data_start = 3
    for ri, row in enumerate(slim):
        excel_row = data_start + ri
        bg = ROW_ALT if ri % 2 else WHITE
        for c, val in enumerate(row, 1):
            cell = ws.cell(row=excel_row, column=c, value=val if val != "" else None)
            cell.font = _font(size=11)
            cell.border = BORDER
            cell.fill = _fill(bg)
            if c == 9:  # Phone as text
                cell.number_format = "@"
            if c in (3, 11, 13, 14):  # numbers
                try:
                    if val != "":
                        cell.value = int(val)
                except (TypeError, ValueError):
                    pass
        for c in (4, 18, 19):
            ws.cell(row=excel_row, column=c).alignment = Alignment(wrap_text=True, vertical="top")

    last_data = data_start + len(slim) - 1
    new_rows = 15
    new_start = last_data + 2
    ws.cell(row=new_start - 1, column=1, value="▼ ADD NEW CLIENTS BELOW (use dropdowns)").font = _font(
        bold=True, color="276749", size=12
    )
    for i in range(new_rows):
        r = new_start + i
        for c in range(1, len(CLIENT_HEADERS) + 1):
            cell = ws.cell(row=r, column=c)
            cell.fill = _fill(ROW_NEW)
            cell.border = BORDER
            cell.font = _font(size=11, color="2D3748")
            if c == 9:
                cell.number_format = "@"

    table_end = new_start + new_rows - 1
    ws.freeze_panes = "A3"
    ws.auto_filter.ref = f"A{header_row}:{get_column_letter(len(CLIENT_HEADERS))}{table_end}"

    # Excel table
    tab = Table(
        displayName="ClientPipeline",
        ref=f"A{header_row}:{get_column_letter(len(CLIENT_HEADERS))}{table_end}",
    )
    tab.tableStyleInfo = TableStyleInfo(
        name="TableStyleMedium2",
        showFirstColumn=False,
        showLastColumn=False,
        showRowStripes=True,
        showColumnStripes=False,
    )
    ws.add_table(tab)

    # Validations on new + existing rows
    add_list_validation(ws, f"B{data_start}:B{table_end}", "Hot,Warm,Nurture,Low,Client")
    add_list_validation(ws, f"E{data_start}:E{table_end}", "NEW,L0,L1,L2,L3")
    add_list_validation(ws, f"J{data_start}:J{table_end}", "Male,Female,Other")

    # Conditional formatting on Category column B
    col_b = f"B{data_start}:B{table_end}"
    ws.conditional_formatting.add(
        col_b, FormulaRule(formula=[f'$B{data_start}="Hot"'], fill=_fill(HOT_BG))
    )
    ws.conditional_formatting.add(
        col_b, FormulaRule(formula=[f'$B{data_start}="Client"'], fill=_fill(CLIENT_BG))
    )
    ws.conditional_formatting.add(
        col_b, FormulaRule(formula=[f'$B{data_start}="Warm"'], fill=_fill(WARM_BG))
    )

    widths = {
        1: 6,
        2: 10,
        3: 7,
        4: 32,
        5: 8,
        6: 8,
        7: 18,
        8: 12,
        9: 11,
        10: 8,
        11: 6,
        12: 14,
        13: 6,
        14: 6,
        15: 16,
        16: 14,
        18: 18,
        19: 28,
    }
    set_col_widths(ws, widths)
    ws.row_dimensions[header_row].height = 28
    return table_end


def build_this_week(wb: Workbook, rows: list[list]) -> None:
    ws = wb.create_sheet("This Week")
    ws.sheet_properties.tabColor = "C53030"
    ws.merge_cells("A1:K1")
    ws["A1"].value = "This Week — Priority calls"
    ws["A1"].font = _font(bold=True, size=16, color=WHITE)
    ws["A1"].fill = _fill("C53030")
    ws["A1"].alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[1].height = 32

    headers = CLIENT_HEADERS[:11]
    style_header_row(ws, 2, len(headers))
    for c, h in enumerate(headers, 1):
        ws.cell(row=2, column=c, value=h)

    week_data = [
        slim_row(r)[:11]
        for r in rows
        if r[1] in ("Hot", "Client") or (r[3] and r[1] != "Low")
    ][:30]

    for ri, row in enumerate(week_data, 3):
        for c, val in enumerate(row, 1):
            cell = ws.cell(row=ri, column=c, value=val if val != "" else None)
            cell.border = BORDER
            cell.font = _font(size=11)
            if c == 2:
                cat = str(val)
                if cat == "Hot":
                    cell.fill = _fill(HOT_BG)
                elif cat == "Client":
                    cell.fill = _fill(CLIENT_BG)
                elif cat == "Warm":
                    cell.fill = _fill(WARM_BG)
    ws.freeze_panes = "A3"
    set_col_widths(ws, {1: 6, 2: 10, 3: 7, 4: 36, 5: 8, 7: 18, 9: 11})


def build_policies(wb: Workbook, policy_rows: list[list]) -> None:
    if not policy_rows:
        return
    ws = wb.create_sheet("Policies")
    ws.sheet_properties.tabColor = "805AD5"
    headers = [
        "Team",
        "Agent",
        "Policyowner",
        "Insured",
        "Policy #",
        "Plan",
        "App Date",
        "Issue Date",
        "Status",
        "Term",
        "Expiry",
        "Tracking",
    ]
    ws.merge_cells("A1:L1")
    ws["A1"].value = "In-force policies (from book)"
    ws["A1"].font = _font(bold=True, size=14, color=WHITE)
    ws["A1"].fill = _fill("553C9A")
    ws["A1"].alignment = Alignment(horizontal="center")

    for c, h in enumerate(headers, 1):
        ws.cell(row=2, column=c, value=h)
    style_header_row(ws, 2, len(headers))

    for ri, row in enumerate(policy_rows, 3):
        for c, val in enumerate(row, 1):
            cell = ws.cell(row=ri, column=c, value=val if val != "" else None)
            cell.border = BORDER
            cell.font = _font(size=10)
            if ri % 2 == 0:
                cell.fill = _fill(ROW_ALT)
    ws.freeze_panes = "A3"
    ws.auto_filter.ref = f"A2:L{2 + len(policy_rows)}"
    set_col_widths(ws, {5: 14, 6: 42, 7: 12, 8: 12})


def build_lookup(wb: Workbook) -> None:
    ws = wb.create_sheet("Lookup")
    ws.sheet_properties.tabColor = "A0AEC0"
    ws.sheet_state = "hidden"
    data = [
        ("Stage", "Meaning"),
        ("NEW", "Not contacted yet"),
        ("L0", "First contact"),
        ("L1", "Meeting / needs"),
        ("L2", "Quote / follow-up"),
        ("L3", "Closing"),
        ("", ""),
        ("Category", "Action"),
        ("Hot", "Call this week"),
        ("Warm", "Book L1"),
        ("Client", "Service + referral"),
        ("Nurture", "Monthly touch"),
        ("Low", "Batch only"),
    ]
    for r, row in enumerate(data, 1):
        for c, v in enumerate(row, 1):
            ws.cell(row=r, column=c, value=v)


def build_workbook(rows: list[list], policy_rows: list[list], output_path) -> None:
    wb = Workbook()
    wb.remove(wb.active)
    build_guide(wb)
    build_dashboard(wb, rows)
    build_add_client(wb)
    build_clients_sheet(wb, rows)
    build_this_week(wb, rows)
    build_policies(wb, policy_rows)
    build_lookup(wb)
    wb.save(output_path)


if __name__ == "__main__":
    import csv
    from pathlib import Path

    from upgrade_pipeline import (
        OUTPUT_XLSX,
        POLICIES_CSV,
        RAW_CSV,
        load_policy_names,
        read_raw_rows,
        transform,
    )

    if not RAW_CSV.exists():
        from import_google_sheet import fetch_google_sheet

        fetch_google_sheet()
    policy_names = load_policy_names()
    records = read_raw_rows()
    rows = transform(records, policy_names)
    policy_data = []
    if POLICIES_CSV.exists():
        with POLICIES_CSV.open(encoding="utf-8") as f:
            policy_data = list(csv.reader(f))[1:]
    build_workbook(rows, policy_data, OUTPUT_XLSX)
    print(f"Built beautiful {OUTPUT_XLSX}")
