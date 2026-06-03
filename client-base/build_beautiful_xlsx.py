#!/usr/bin/env python3
"""Build a beautiful, user-friendly client_base.xlsx."""

from __future__ import annotations

import re
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

# Column indexes (1-based) — keep in sync with CLIENT_HEADERS
C = {
    "rank": 1,
    "category": 2,
    "score": 3,
    "action": 4,
    "stage": 5,
    "is_client": 6,
    "name": 7,
    "nick": 8,
    "phone": 9,
    "gender": 10,
    "age": 11,
    "relationship": 12,
    "rel_sc": 13,
    "poss": 14,
    "job": 15,
    "area": 16,
    "income": 17,
    "product": 18,
    "remarks": 19,
    "last_note": 20,
    "approach": 21,
    "next_touch": 22,
    "birthday": 23,
    "days_to_bday": 24,
    "bday_soon": 25,
    "ref_tier": 26,
    "ref_asked": 27,
    "ref_given": 28,
    "ref_by": 29,
    "ref_date": 30,
    "ref_notes": 31,
    "l0": 32,
    "l1": 33,
    "l2": 34,
}

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
    "Approach Status",
    "Next Touch Date",
    "Birthday",
    "Days to Birthday",
    "Birthday ≤30d?",
    "Referral Tier",
    "Referral Asked?",
    "Referrals Given",
    "Referred By",
    "Last Referral Date",
    "Referral Notes",
    "L0",
    "L1",
    "L2",
]

APPROACH_OPTIONS = (
    "Not contacted,First contact,Meeting scheduled,Needs analysis,"
    "Quoted,Follow-up,Negotiating,Won - pending,Active client,"
    "Referral partner,Nurture,Lost"
)
REF_ASKED_OPTIONS = "No,Yes - declined,Yes - will refer,Yes - referred someone"

# Map from OUT_HEADERS indices in upgrade_pipeline rows
# 0 rank, 1 cat, 2 score, 3 next, 4 stage, 5 is client, 6 policy match, 7 products,
# 8 en, 9 nick, 10 phone, ...
def policy_champion_set(policy_rows: list[list]) -> set[str]:
    """Policyowners with 2+ policies = referral champion."""
    from collections import Counter

    counts: Counter[str] = Counter()
    for row in policy_rows:
        if len(row) > 2:
            owner = row[2]
            key = re.sub(r"[^a-z0-9]", "", owner.lower())
            if key:
                counts[key] += 1
    return {k for k, v in counts.items() if v >= 2}


def map_approach_status(stage: str, is_client: str) -> str:
    if is_client == "Yes":
        return "Active client"
    mapping = {
        "NEW": "Not contacted",
        "L0": "First contact",
        "L1": "Meeting scheduled",
        "L2": "Quoted",
        "L3": "Negotiating",
    }
    return mapping.get((stage or "").upper(), "Not contacted")


def initial_referral_tier(is_client: str, rel_sc: int, name: str, champions: set[str]) -> str:
    key = re.sub(r"[^a-z0-9]", "", (name or "").lower())
    if is_client == "Yes" or key in champions:
        return "Champion"
    if rel_sc >= 4:
        return "High Potential"
    if rel_sc >= 3:
        return "Standard"
    return "New"


def slim_row(full: list, champions: set[str] | None = None) -> list:
    champions = champions or set()
    stage = str(full[4] or "")
    is_client = str(full[5] or "")
    try:
        rel_sc = int(full[14]) if full[14] != "" else 0
    except (TypeError, ValueError):
        rel_sc = 0
    name = str(full[8] or "")
    return [
        full[0],
        full[1],
        full[2],
        full[3],
        stage,
        is_client,
        name,
        full[9],
        full[10],
        full[11],
        full[12],
        full[13],
        rel_sc or "",
        full[15] or "",
        full[16],
        full[17],
        full[18],
        full[7],
        full[19],
        full[20],
        map_approach_status(stage, is_client),
        "",  # next touch
        "",  # birthday
        None,  # days formula
        None,  # soon formula
        initial_referral_tier(is_client, rel_sc, name, champions),
        "No",  # referral asked default
        0,  # referrals given
        "",  # referred by
        "",  # last referral date
        "",  # referral notes
        full[23],
        full[24],
        full[25],
    ]


def col_letter(key: str) -> str:
    return get_column_letter(C[key])


def row_formula_days_to_birthday(r: int) -> str:
    b = f"${col_letter('birthday')}{r}"
    return (
        f'=IF({b}="","",IF(DATE(YEAR(TODAY()),MONTH({b}),DAY({b}))>=TODAY(),'
        f"DATE(YEAR(TODAY()),MONTH({b}),DAY({b}))-TODAY(),"
        f"DATE(YEAR(TODAY())+1,MONTH({b}),DAY({b}))-TODAY()))"
    )


def row_formula_bday_soon(r: int) -> str:
    d = f"${col_letter('days_to_bday')}{r}"
    return f'=IF({d}="","",IF({d}<=30,"YES",""))'


def row_formula_ref_tier(r: int) -> str:
    cl = f"${col_letter('is_client')}{r}"
    rel = f"${col_letter('rel_sc')}{r}"
    given = f"${col_letter('ref_given')}{r}"
    return (
        f'=IF({cl}="Yes","Champion",IF({given}>=2,"Advocate",IF({given}>=1,"Referrer",'
        f'IF({rel}>=4,"High Potential",IF({rel}>=3,"Standard","New"))))))'
    )


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
        ("3", "Work from 「This Week」, 「Referral System」, or 「Birthdays」 tabs."),
        ("4", "Fill Birthday + Approach Status on 「Clients」 for automation."),
        ("", ""),
        ("Referral system", ""),
        ("•", "「Referral System」 — champions, scripts, tracking."),
        ("•", "Set Referral Asked? / Referrals Given on Clients sheet."),
        ("", ""),
        ("Birthdays", ""),
        ("•", "Enter Birthday on Clients → Days to Birthday calculates automatically."),
        ("•", "「Birthdays」 tab lists contacts with birthday within 30 days."),
        ("", ""),
        ("Tips", ""),
        ("•", "Approach Status dropdown tracks where each person is in your sales flow."),
        ("•", "Refresh: python3 import_google_sheet.py in client-base folder."),
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

    ws["A15"] = "Referral & birthdays"
    ws["A15"].font = _font(bold=True, size=12)
    ws["A16"] = "Champions (live)"
    ws["B16"] = '=COUNTIF(Clients!Z3:Z500,"Champion")'
    ws["A17"] = "Birthdays ≤30 days"
    ws["B17"] = '=COUNTIF(Clients!Y3:Y500,"YES")'
    ws["A18"] = "Referral asked (Yes)"
    ws["B18"] = '=COUNTIF(Clients!AA3:AA500,"Yes*")'
    for r in (16, 17, 18):
        ws.cell(row=r, column=2).font = _font(size=11, color=NAVY_LIGHT)

    ws["A20"] = "Go to sheet →"
    links = [
        "Referral System",
        "Birthdays",
        "Approach Funnel",
        "Clients",
        "➕ Add New Client",
        "This Week",
    ]
    for i, name in enumerate(links, 21):
        ws.cell(row=i, column=2, value=name).font = _font(bold=True, color=NAVY_LIGHT)

    set_col_widths(ws, {1: 22, 2: 42, 3: 10})


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
        "Approach Status",
        "Next Action",
        "Next Touch Date",
        "Birthday (yyyy-mm-dd)",
        "Referral Asked?",
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
    add_list_validation(ws, "C14", APPROACH_OPTIONS)
    add_list_validation(ws, "C18", REF_ASKED_OPTIONS)

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

    fr = first_in
    # Form rows: name..remarks at fr..fr+19
    formulas = [""] * len(CLIENT_HEADERS)
    formulas[C["category"] - 1] = f"$C${fr + 8}"
    formulas[C["score"] - 1] = f'=IF($C${fr + 6}="","",$C${fr + 6}+$C${fr + 7})'
    formulas[C["action"] - 1] = f"$C${fr + 11}"
    formulas[C["stage"] - 1] = f"$C${fr + 9}"
    formulas[C["name"] - 1] = f"$C${fr}"
    formulas[C["nick"] - 1] = f"$C${fr + 1}"
    formulas[C["phone"] - 1] = f"$C${fr + 2}"
    formulas[C["gender"] - 1] = f"$C${fr + 3}"
    formulas[C["age"] - 1] = f"$C${fr + 4}"
    formulas[C["relationship"] - 1] = f"$C${fr + 5}"
    formulas[C["rel_sc"] - 1] = f"$C${fr + 6}"
    formulas[C["poss"] - 1] = f"$C${fr + 7}"
    formulas[C["approach"] - 1] = f"$C${fr + 10}"
    formulas[C["next_touch"] - 1] = f"$C${fr + 12}"
    formulas[C["birthday"] - 1] = f"$C${fr + 13}"
    formulas[C["ref_asked"] - 1] = f"$C${fr + 14}"
    formulas[C["job"] - 1] = f"$C${fr + 15}"
    formulas[C["area"] - 1] = f"$C${fr + 16}"
    formulas[C["income"] - 1] = f"$C${fr + 17}"
    formulas[C["product"] - 1] = f"$C${fr + 18}"
    formulas[C["remarks"] - 1] = f"$C${fr + 19}"
    for c, fml in enumerate(formulas, 1):
        cell = ws.cell(row=paste_row, column=c)
        if fml:
            cell.value = fml if fml.startswith("=") else f"={fml}"
        cell.fill = _fill(ROW_NEW)
        cell.border = BORDER
        cell.font = _font(size=11)
    apply_client_row_formulas(ws, paste_row)

    set_col_widths(ws, {2: 26, 3: 34})
    for c in range(1, len(CLIENT_HEADERS) + 1):
        ws.column_dimensions[get_column_letter(c)].width = 13


def apply_client_row_formulas(ws, excel_row: int) -> None:
    ws.cell(row=excel_row, column=C["days_to_bday"]).value = row_formula_days_to_birthday(excel_row)
    ws.cell(row=excel_row, column=C["bday_soon"]).value = row_formula_bday_soon(excel_row)
    ws.cell(row=excel_row, column=C["ref_tier"]).value = row_formula_ref_tier(excel_row)
    ws.cell(row=excel_row, column=C["birthday"]).number_format = "yyyy-mm-dd"
    ws.cell(row=excel_row, column=C["next_touch"]).number_format = "yyyy-mm-dd"
    ws.cell(row=excel_row, column=C["ref_date"]).number_format = "yyyy-mm-dd"


def build_clients_sheet(wb: Workbook, rows: list[list], champions: set[str]) -> tuple:
    ws = wb.create_sheet("Clients")
    ws.sheet_properties.tabColor = NAVY

    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=len(CLIENT_HEADERS))
    banner = ws["A1"]
    banner.value = "Client Pipeline  |  徐語希管理組 · 龍浩賢  |  Referral + Birthday enabled"
    banner.font = _font(bold=True, size=14, color=WHITE)
    banner.fill = _fill(NAVY)
    banner.alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[1].height = 32

    header_row = 2
    for c, h in enumerate(CLIENT_HEADERS, 1):
        ws.cell(row=header_row, column=c, value=h)
    style_header_row(ws, header_row, len(CLIENT_HEADERS))

    slim = [slim_row(r, champions) for r in rows]
    data_start = 3
    for ri, row in enumerate(slim):
        excel_row = data_start + ri
        bg = ROW_ALT if ri % 2 else WHITE
        for c, val in enumerate(row, 1):
            if val is None:
                continue
            cell = ws.cell(row=excel_row, column=c, value=val if val != "" else None)
            cell.font = _font(size=11)
            cell.border = BORDER
            cell.fill = _fill(bg)
            if c == C["phone"]:
                cell.number_format = "@"
            if c in (C["score"], C["age"], C["rel_sc"], C["poss"], C["ref_given"]):
                try:
                    if val != "":
                        cell.value = int(val)
                except (TypeError, ValueError):
                    pass
        apply_client_row_formulas(ws, excel_row)
        for c in (C["action"], C["product"], C["remarks"], C["ref_notes"]):
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
            if c == C["phone"]:
                cell.number_format = "@"
        apply_client_row_formulas(ws, r)
        ws.cell(row=r, column=C["ref_asked"], value="No")
        ws.cell(row=r, column=C["approach"], value="Not contacted")

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

    # Validations
    add_list_validation(ws, f"B{data_start}:B{table_end}", "Hot,Warm,Nurture,Low,Client")
    add_list_validation(ws, f"E{data_start}:E{table_end}", "NEW,L0,L1,L2,L3")
    add_list_validation(ws, f"J{data_start}:J{table_end}", "Male,Female,Other")
    add_list_validation(ws, f"U{data_start}:U{table_end}", APPROACH_OPTIONS)
    add_list_validation(ws, f"AA{data_start}:AA{table_end}", REF_ASKED_OPTIONS)

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
    col_y = f"Y{data_start}:Y{table_end}"
    ws.conditional_formatting.add(
        col_y,
        FormulaRule(formula=[f'$Y{data_start}="YES"'], fill=_fill("FAF089")),
    )
    col_z = f"Z{data_start}:Z{table_end}"
    ws.conditional_formatting.add(
        col_z,
        FormulaRule(formula=[f'$Z{data_start}="Champion"'], fill=_fill("B2F5EA")),
    )

    widths = {
        1: 6,
        2: 10,
        3: 7,
        4: 28,
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
        15: 14,
        16: 12,
        18: 16,
        19: 24,
        21: 16,
        22: 14,
        23: 12,
        24: 10,
        25: 10,
        26: 14,
        27: 14,
        28: 8,
        31: 20,
    }
    set_col_widths(ws, widths)
    ws.row_dimensions[header_row].height = 36
    return ws, data_start, table_end, slim


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


def build_referral_system(wb: Workbook, slim: list[list], champions: set[str]) -> None:
    ws = wb.create_sheet("Referral System")
    ws.sheet_properties.tabColor = "D69E2E"

    ws.merge_cells("A1:H1")
    ws["A1"].value = "Referral System — Build your introduction pipeline"
    ws["A1"].font = _font(bold=True, size=16, color=WHITE)
    ws["A1"].fill = _fill(GOLD)
    ws["A1"].alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[1].height = 36

    ws["A3"] = "How to use"
    ws["A3"].font = _font(bold=True, size=12)
    steps = [
        "1. Ask 「Champion」 clients (green on Clients sheet) after every good service call.",
        "2. Set Referral Asked? → Yes - will refer / Yes - referred someone.",
        "3. Log name in Referred By on new prospect row + Last Referral Date.",
        "4. Thank referrer within 24 hours (message template below).",
    ]
    for i, s in enumerate(steps, 4):
        ws.merge_cells(start_row=i, start_column=1, end_row=i, end_column=8)
        ws.cell(row=i, column=1, value=s)

    ws["A9"] = "Referral champions (auto from Clients)"
    ws["A9"].font = _font(bold=True, size=12)
    ch_headers = ["Name", "Phone", "Rel Score", "Referral Tier", "Referral Asked?", "Referrals Given", "Next Action"]
    for c, h in enumerate(ch_headers, 1):
        ws.cell(row=10, column=c, value=h)
    style_header_row(ws, 10, len(ch_headers))

    def _is_champion(row: list) -> bool:
        if str(row[C["is_client"] - 1]) == "Yes":
            return True
        if str(row[C["ref_tier"] - 1]) == "Champion":
            return True
        rel = str(row[C["rel_sc"] - 1])
        return rel in ("4", "5") and rel != ""

    champ_rows = [row for row in slim if _is_champion(row)]
    champ_rows = sorted(
        champ_rows,
        key=lambda x: (-int(x[C["rel_sc"] - 1] or 0), str(x[C["name"] - 1])),
    )[:25]

    for ri, row in enumerate(champ_rows, 11):
        ws.cell(row=ri, column=1, value=row[C["name"] - 1])
        ws.cell(row=ri, column=2, value=row[C["phone"] - 1])
        ws.cell(row=ri, column=3, value=row[C["rel_sc"] - 1])
        ws.cell(row=ri, column=4, value=row[C["ref_tier"] - 1])
        ws.cell(row=ri, column=5, value=row[C["ref_asked"] - 1])
        ws.cell(row=ri, column=6, value=row[C["ref_given"] - 1])
        ws.cell(row=ri, column=7, value=row[C["action"] - 1])
        for c in range(1, 8):
            ws.cell(row=ri, column=c).border = BORDER

    script_row = 11 + len(champ_rows) + 2
    ws.cell(row=script_row, column=1, value="WhatsApp scripts (copy & edit)").font = _font(
        bold=True, size=12
    )
    scripts = [
        (
            "Ask referral",
            "多謝你信任我。想幫多啲家庭做保障——如果你朋友最近買樓、生BB或轉工，"
            "肯唔肯介紹我同佢傾15分鐘？我保證唔硬銷，你朋友唔使買都得。",
        ),
        (
            "Thank referrer",
            "多謝你介紹XX俾我！我已經聯絡咗，會好好跟進。有你介紹真係幫到我好多。",
        ),
        (
            "Birthday + referral",
            "生日快乐/生日快樂！🎂 希望新一年身體健健康康。"
            "如果身边有朋友想了解保险，随时话我知，我会照顾好你的朋友。",
        ),
    ]
    for i, (title, text) in enumerate(scripts, script_row + 1):
        ws.cell(row=i, column=1, value=title).font = _font(bold=True)
        ws.merge_cells(start_row=i, start_column=2, end_row=i, end_column=8)
        ws.cell(row=i, column=2, value=text).alignment = Alignment(wrap_text=True)
        ws.row_dimensions[i].height = 48

    ws["A" + str(script_row + 6)] = "Referral log (write each new intro)"
    ws["A" + str(script_row + 6)].font = _font(bold=True, size=12)
    log_hdr = ["Date", "Referrer", "New prospect", "Phone", "Status", "Notes"]
    log_r = script_row + 7
    for c, h in enumerate(log_hdr, 1):
        ws.cell(row=log_r, column=c, value=h)
    style_header_row(ws, log_r, len(log_hdr))
    for extra in range(15):
        r = log_r + 1 + extra
        for c in range(1, 7):
            cell = ws.cell(row=r, column=c)
            cell.fill = _fill(ROW_NEW)
            cell.border = BORDER
        ws.cell(row=r, column=1).number_format = "yyyy-mm-dd"

    set_col_widths(ws, {1: 14, 2: 14, 4: 14, 7: 32, 2: 50})


def build_birthdays(wb: Workbook, data_start: int, table_end: int) -> None:
    ws = wb.create_sheet("Birthdays")
    ws.sheet_properties.tabColor = "ED64A6"

    ws.merge_cells("A1:I1")
    ws["A1"].value = "Birthdays — next 30 days (auto from Clients sheet)"
    ws["A1"].font = _font(bold=True, size=16, color=WHITE)
    ws["A1"].fill = _fill("B83280")
    ws["A1"].alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[1].height = 34

    ws["A2"] = "Tip: Enter Birthday on Clients tab (column W). Days to Birthday updates automatically."
    ws.merge_cells("A2:I2")

    headers = [
        "Name",
        "Nickname",
        "Phone",
        "Birthday",
        "Days Left",
        "Category",
        "Referral Tier",
        "Suggested Action",
    ]
    hdr_row = 3
    for c, h in enumerate(headers, 1):
        ws.cell(row=hdr_row, column=c, value=h)
    style_header_row(ws, hdr_row, len(headers))

    # Dynamic pull: nth contact where Birthdays ≤30d? = YES
    clients = "Clients"
    for n in range(1, 41):
        r = hdr_row + n
        k = n
        name_f = (
            f'=IFERROR(INDEX({clients}!$G${data_start}:$G${table_end},'
            f"SMALL(IF({clients}!$Y${data_start}:$Y${table_end}=\"YES\","
            f"ROW({clients}!$Y${data_start}:$Y${table_end})-ROW({clients}!$G${data_start})+1),{k})),\"\")"
        )
        ws.cell(row=r, column=1, value=name_f)
        ws.cell(row=r, column=2, value=f'=IF($A{r}="","",INDEX({clients}!$H${data_start}:$H${table_end},MATCH($A{r},{clients}!$G${data_start}:$G${table_end},0)))')
        ws.cell(row=r, column=3, value=f'=IF($A{r}="","",INDEX({clients}!$I${data_start}:$I${table_end},MATCH($A{r},{clients}!$G${data_start}:$G${table_end},0)))')
        ws.cell(row=r, column=4, value=f'=IF($A{r}="","",INDEX({clients}!$W${data_start}:$W${table_end},MATCH($A{r},{clients}!$G${data_start}:$G${table_end},0)))')
        ws.cell(row=r, column=5, value=f'=IF($A{r}="","",INDEX({clients}!$X${data_start}:$X${table_end},MATCH($A{r},{clients}!$G${data_start}:$G${table_end},0)))')
        ws.cell(row=r, column=6, value=f'=IF($A{r}="","",INDEX({clients}!$B${data_start}:$B${table_end},MATCH($A{r},{clients}!$G${data_start}:$G${table_end},0)))')
        ws.cell(row=r, column=7, value=f'=IF($A{r}="","",INDEX({clients}!$Z${data_start}:$Z${table_end},MATCH($A{r},{clients}!$G${data_start}:$G${table_end},0)))')
        ws.cell(
            row=r,
            column=8,
            value=f'=IF($A{r}="","",IF($G{r}="Champion","Birthday WhatsApp + referral ask","Birthday WhatsApp only"))',
        )
        for c in range(1, 9):
            ws.cell(row=r, column=c).border = BORDER
        ws.cell(row=r, column=4).number_format = "yyyy-mm-dd"

    set_col_widths(ws, {1: 18, 3: 12, 4: 12, 8: 28})


def build_approach_funnel(wb: Workbook, data_start: int, table_end: int) -> None:
    ws = wb.create_sheet("Approach Funnel")
    ws.sheet_properties.tabColor = "3182CE"

    ws.merge_cells("A1:E1")
    ws["A1"].value = "Client Approach Status — pipeline counts"
    ws["A1"].font = _font(bold=True, size=16, color=WHITE)
    ws["A1"].fill = _fill("2B6CB0")
    ws["A1"].alignment = Alignment(horizontal="center", vertical="center")

    ws["A3"] = "Status"
    ws["B3"] = "Count"
    ws["C3"] = "% of total"
    style_header_row(ws, 3, 3)

    statuses = APPROACH_OPTIONS.split(",")
    for i, status in enumerate(statuses, 4):
        ws.cell(row=i, column=1, value=status)
        ws.cell(
            row=i,
            column=2,
            value=f'=COUNTIF(Clients!$U${data_start}:$U${table_end},A{i})',
        )
        ws.cell(
            row=i,
            column=3,
            value=f'=IF(B4=0,"",B{i}/COUNTA(Clients!$G${data_start}:$G${table_end}))',
        )
        ws.cell(row=i, column=3).number_format = "0.0%"

    ws.cell(row=4 + len(statuses), column=1, value="TOTAL with name").font = _font(bold=True)
    ws.cell(
        row=4 + len(statuses),
        column=2,
        value=f"=COUNTA(Clients!$G${data_start}:$G${table_end})",
    ).font = _font(bold=True)

    set_col_widths(ws, {1: 22, 2: 10, 3: 10})


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
        ("", ""),
        ("Referral Tier", "Who to ask"),
        ("Champion", "Client / 2+ policies — ask every quarter"),
        ("Advocate", "Gave 2+ referrals"),
        ("High Potential", "Rel score 4-5"),
        ("Standard", "Rel score 3"),
        ("New", "Build relationship first"),
    ]
    for r, row in enumerate(data, 1):
        for c, v in enumerate(row, 1):
            ws.cell(row=r, column=c, value=v)


def build_workbook(rows: list[list], policy_rows: list[list], output_path) -> None:
    wb = Workbook()
    wb.remove(wb.active)
    champions = policy_champion_set(policy_rows)

    build_guide(wb)
    build_dashboard(wb, rows)
    build_add_client(wb)
    _ws, data_start, table_end, slim = build_clients_sheet(wb, rows, champions)
    build_referral_system(wb, slim, champions)
    build_birthdays(wb, data_start, table_end)
    build_approach_funnel(wb, data_start, table_end)
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
