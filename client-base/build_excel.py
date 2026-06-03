#!/usr/bin/env python3
"""Build client_base.xlsx from CSV data."""

import csv
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

BASE = Path(__file__).parent
OUTPUT = BASE / "client_base.xlsx"

HEADER_FILL = PatternFill(start_color="1F4E79", end_color="1F4E79", fill_type="solid")
HEADER_FONT = Font(bold=True, color="FFFFFF", size=11)
TITLE_FONT = Font(bold=True, size=14)


def read_csv(name: str) -> tuple[list[str], list[list]]:
    path = BASE / name
    with path.open(encoding="utf-8") as f:
        rows = list(csv.reader(f))
    return rows[0], rows[1:]


def style_sheet(ws, ncols: int, nrows: int) -> None:
    for col in range(1, ncols + 1):
        cell = ws.cell(row=1, column=col)
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = f"A1:{get_column_letter(ncols)}{max(nrows, 1)}"
    for col in range(1, ncols + 1):
        letter = get_column_letter(col)
        max_len = 12
        for row in range(1, min(nrows + 1, 200)):
            val = ws.cell(row=row, column=col).value
            if val is not None:
                max_len = max(max_len, min(len(str(val)) + 2, 50))
        ws.column_dimensions[letter].width = max_len


def write_table(ws, headers: list[str], data: list[list], start_row: int = 1) -> int:
    for c, h in enumerate(headers, 1):
        ws.cell(row=start_row, column=c, value=h)
    for r, row in enumerate(data, start_row + 1):
        for c, val in enumerate(row, 1):
            ws.cell(row=r, column=c, value=val or "")
    return start_row + len(data)


def build_clients_master(wb: Workbook) -> None:
    ws = wb.active
    ws.title = "Clients Master"

    headers = [
        "Policyowner (EN)",
        "中文名",
        "Phone / WhatsApp",
        "Email",
        "Policies Inforce",
        "Product Summary",
        "Referral Tier",
        "Priority (1=urgent)",
        "Next Action",
        "Last Contact Date",
        "Next Follow-up Date",
        "Referral Asked (Y/N)",
        "Referrals Given",
        "Cross-sell: Medical",
        "Cross-sell: Other",
        "Notes",
    ]

    _, client_rows = read_csv("clients_inforce.csv")
    data = []
    for row in client_rows:
        data.append(
            [
                row[0],  # name
                "",  # chinese
                "",  # phone
                "",  # email
                row[1],
                row[2],
                row[3],
                row[4],
                row[5],
                "",
                "",
                "",
                "",
                "",
                "",
                "",
            ]
        )

    nrows = write_table(ws, headers, data)
    style_sheet(ws, len(headers), nrows)


def build_policies(wb: Workbook) -> None:
    ws = wb.create_sheet("Policies")
    headers, data = read_csv("policies_register.csv")
    extra = ["Agent", "Sales Team", "Tracking No"]
    headers = headers + extra
    data = [row + ["龍浩賢", "徐語希管理組", ""] for row in data]
    nrows = write_table(ws, headers, data)
    style_sheet(ws, len(headers), nrows)


def build_prospects(wb: Workbook) -> None:
    ws = wb.create_sheet("Prospects Network")
    headers, data = read_csv("prospects_network_top.csv")
    extra = [
        "Last Contact",
        "Next Follow-up",
        "L0",
        "Invited",
        "L1",
        "L2",
        "NEED",
        "Outcome",
    ]
    headers = headers + extra
    data = [row + [""] * len(extra) for row in data]
    nrows = write_table(ws, headers, data)
    style_sheet(ws, len(headers), nrows)


def build_weekly_actions(wb: Workbook) -> None:
    ws = wb.create_sheet("This Week Actions")
    ws["A1"] = "This Week — Priority Actions"
    ws["A1"].font = TITLE_FONT

    headers = ["Priority", "Name", "Type", "Action", "Due Date", "Done (Y/N)"]
    actions = [
        ["1", "CHEUNG TAK SIN", "Client", "Close pending INCOMEJOY policy", "", ""],
        ["1", "LUNG ON KI", "Client", "Annual review + referral ask", "", ""],
        ["1", "LUNG HO YIN", "Client", "EASY-PLUG review + referral ask", "", ""],
        ["1", "CHENG HONG WAI", "Client", "Thank-you + referral ask (3 policies)", "", ""],
        ["2", "KWOK WAI LING", "Client", "Win-back / clarify withdrawn vs inforce", "", ""],
        ["2", "LEUNG WAI KI", "Client", "Service call + referral", "", ""],
        ["2", "YU CHUN KIN", "Client", "6-month check-in + referral", "", ""],
        ["1", "鄒學蘭 Chau Hok Lan", "Prospect", "Family approach — 93380839", "", ""],
        ["1", "區家駒 Au Ka Kai", "Prospect", "Retirement/medical — 66299989", "", ""],
        ["2", "張文浩 Jackie", "Prospect", "WhatsApp protection review — 63793889", "", ""],
    ]
    nrows = write_table(ws, headers, actions, start_row=3)
    style_sheet(ws, len(headers), nrows)


def build_readme(wb: Workbook) -> None:
    ws = wb.create_sheet("How to Use", 0)
    lines = [
        ("Client Base — 龍浩賢 / 徐語希管理組", ""),
        ("", ""),
        ("Sheet guide:", ""),
        ("Clients Master", "One row per client — add 中文名, phone, follow-up dates"),
        ("Policies", "All policies from your book — one row per policy"),
        ("Prospects Network", "Warm contacts from network list — track L0→L2"),
        ("This Week Actions", "Checklist — mark Done when complete"),
        ("", ""),
        ("Updated:", "From policy book screenshots + prospect PDF"),
        ("", ""),
        ("Tips:", ""),
        ("", "Sort Clients Master by Priority for daily calls"),
        ("", "Filter Policies by policyowner to prep for reviews"),
        ("", "Do not commit real phone numbers to public repos"),
    ]
    for i, (a, b) in enumerate(lines, 1):
        ws.cell(row=i, column=1, value=a)
        ws.cell(row=i, column=2, value=b)
    ws.column_dimensions["A"].width = 22
    ws.column_dimensions["B"].width = 55
    ws["A1"].font = TITLE_FONT


def main() -> None:
    wb = Workbook()
    build_readme(wb)
    build_clients_master(wb)
    build_policies(wb)
    build_prospects(wb)
    build_weekly_actions(wb)
    wb.save(OUTPUT)
    print(f"Created {OUTPUT}")


if __name__ == "__main__":
    main()
