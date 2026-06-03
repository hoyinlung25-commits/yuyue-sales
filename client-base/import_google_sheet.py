#!/usr/bin/env python3
"""Import Google Sheet and rebuild client_base.xlsx."""

from __future__ import annotations

import csv
import re
from pathlib import Path
from urllib.request import urlopen

from openpyxl import Workbook, load_workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

BASE = Path(__file__).parent
OUTPUT = BASE / "client_base.xlsx"
CSV_PATH = BASE / "google_sheet_raw.csv"
XLSX_PATH = BASE / "google_sheet_raw.xlsx"
POLICIES_CSV = BASE / "policies_register.csv"

SHEET_ID = "1qPNnq7tOPYX5Rk4UpiL9UaCCbEyRseC-g2-LC6itupM"
GVIZ_CSV = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=0"

HEADER_FILL = PatternFill(start_color="1F4E79", end_color="1F4E79", fill_type="solid")
HEADER_FONT = Font(bold=True, color="FFFFFF", size=11)


def fetch_google_sheet() -> None:
    print(f"Downloading {GVIZ_CSV} ...")
    with urlopen(GVIZ_CSV, timeout=60) as resp:
        data = resp.read()
    text = data.decode("utf-8")
    if text.lstrip().startswith("<!") or "Page Not Found" in text:
        raise SystemExit("Google Sheet not accessible. See GOOGLE_SHEET_IMPORT.md")
    CSV_PATH.write_text(text, encoding="utf-8")
    print(f"Saved {CSV_PATH} ({len(text.splitlines())} lines)")


def normalize_header(h: str) -> str:
    return re.sub(r"\s+", " ", h.replace("\n", " ")).strip()


def load_pipeline_rows() -> tuple[list[str], list[list]]:
    if not CSV_PATH.exists() and not XLSX_PATH.exists():
        fetch_google_sheet()

    if XLSX_PATH.exists():
        wb = load_workbook(XLSX_PATH, read_only=True, data_only=True)
        ws = wb.active
        rows = [["" if c is None else str(c) for c in row] for row in ws.iter_rows(values_only=True)]
        wb.close()
    else:
        with CSV_PATH.open(encoding="utf-8-sig") as f:
            rows = list(csv.reader(f))

    if not rows:
        raise SystemExit("Empty sheet data")

    headers = [normalize_header(h) for h in rows[0]]
    data = []
    for row in rows[1:]:
        if not any(str(c).strip() for c in row):
            continue
        padded = row + [""] * (len(headers) - len(row))
        data.append(padded[: len(headers)])
    return headers, data


def load_policies() -> tuple[list[str], list[list]] | None:
    if not POLICIES_CSV.exists():
        return None
    with POLICIES_CSV.open(encoding="utf-8") as f:
        rows = list(csv.reader(f))
    return rows[0], rows[1:]


def style_table(ws, ncols: int, nrows: int, header_row: int = 1) -> None:
    for col in range(1, ncols + 1):
        cell = ws.cell(row=header_row, column=col)
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    ws.freeze_panes = ws.cell(row=header_row + 1, column=1).coordinate
    ws.auto_filter.ref = f"A{header_row}:{get_column_letter(ncols)}{nrows}"
    ws.row_dimensions[header_row].height = 32
    for col in range(1, ncols + 1):
        letter = get_column_letter(col)
        max_len = 10
        for row in range(header_row, min(nrows + 1, 400)):
            v = ws.cell(row=row, column=col).value
            if v:
                max_len = max(max_len, min(len(str(v)) + 2, 45))
        ws.column_dimensions[letter].width = max_len


def write_sheet(wb: Workbook, title: str, headers: list[str], data: list[list]) -> None:
    ws = wb.create_sheet(title)
    for c, h in enumerate(headers, 1):
        ws.cell(row=1, column=c, value=h)
    for r, row in enumerate(data, 2):
        for c, val in enumerate(row, 1):
            v = val.strip() if isinstance(val, str) else val
            ws.cell(row=r, column=c, value=v if v != "" else None)
    style_table(ws, len(headers), len(data) + 1)


def policy_headers_bilingual() -> list[str]:
    return [
        "銷售團隊名稱",
        "代理人",
        "權益人",
        "受保人",
        "保單號碼",
        "基本計劃",
        "投保日期",
        "簽發日期",
        "保單狀態",
        "供款年期",
        "保單到期日",
        "運單號碼",
    ]


def build_readme(wb: Workbook, pipeline_rows: int, policy_rows: int) -> None:
    ws = wb.create_sheet("How to Use", 0)
    lines = [
        ("Client Base", ""),
        ("Source 1", "Google Sheet — Prospects & Pipeline"),
        ("Source 2", "Policy book screenshots — Policies tab"),
        ("", ""),
        ("Prospects & Pipeline", f"{pipeline_rows} rows (sync from Google)"),
        ("Policies", f"{policy_rows} in-force / pending rows"),
        ("", ""),
        ("Refresh:", "python3 import_google_sheet.py"),
        ("Sheet URL", f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit"),
    ]
    for i, (a, b) in enumerate(lines, 1):
        ws.cell(row=i, column=1, value=a)
        ws.cell(row=i, column=2, value=b)
    ws.column_dimensions["A"].width = 22
    ws.column_dimensions["B"].width = 60


def main() -> None:
    p_headers, p_data = load_pipeline_rows()
    policies = load_policies()

    wb = Workbook()
    wb.remove(wb.active)

    policy_count = 0
    if policies:
        ph, pd = policies
        write_sheet(wb, "Policies", policy_headers_bilingual(), pd)
        policy_count = len(pd)

    write_sheet(wb, "Prospects & Pipeline", p_headers, p_data)
    build_readme(wb, len(p_data), policy_count)

    wb.save(OUTPUT)
    print(f"Created {OUTPUT}")
    print(f"  Prospects & Pipeline: {len(p_data)} rows")
    print(f"  Policies: {policy_count} rows")


if __name__ == "__main__":
    main()
