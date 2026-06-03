#!/usr/bin/env python3
"""Import google_sheet_raw.csv or .xlsx and rebuild client_base.xlsx."""

from __future__ import annotations

import csv
from pathlib import Path

BASE = Path(__file__).parent
CSV_PATH = BASE / "google_sheet_raw.csv"
XLSX_PATH = BASE / "google_sheet_raw.xlsx"
OUTPUT = BASE / "client_base.xlsx"

HEADER_FILL_COLOR = "1F4E79"


def load_rows() -> tuple[list[str], list[list]]:
    if XLSX_PATH.exists():
        from openpyxl import load_workbook

        wb = load_workbook(XLSX_PATH, read_only=True, data_only=True)
        ws = wb.active
        rows = [["" if c is None else str(c) for c in row] for row in ws.iter_rows(values_only=True)]
        wb.close()
        if not rows:
            raise SystemExit(f"Empty workbook: {XLSX_PATH}")
        return [str(h) for h in rows[0]], [list(r) for r in rows[1:] if any(str(x).strip() for x in r)]

    if CSV_PATH.exists():
        with CSV_PATH.open(encoding="utf-8-sig") as f:
            rows = list(csv.reader(f))
        if not rows:
            raise SystemExit(f"Empty CSV: {CSV_PATH}")
        return rows[0], rows[1:]

    raise SystemExit(
        "No import file found.\n"
        f"  Place {CSV_PATH.name} or {XLSX_PATH.name} in client-base/\n"
        "  See GOOGLE_SHEET_IMPORT.md"
    )


def build_xlsx(headers: list[str], data: list[list]) -> None:
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Font, PatternFill
    from openpyxl.utils import get_column_letter

    wb = Workbook()
    ws = wb.active
    ws.title = "Data"

    fill = PatternFill(start_color=HEADER_FILL_COLOR, end_color=HEADER_FILL_COLOR, fill_type="solid")
    hfont = Font(bold=True, color="FFFFFF")

    for c, h in enumerate(headers, 1):
        cell = ws.cell(row=1, column=c, value=h)
        cell.fill = fill
        cell.font = hfont
        cell.alignment = Alignment(wrap_text=True, horizontal="center", vertical="center")

    for r, row in enumerate(data, 2):
        for c, val in enumerate(row, 1):
            ws.cell(row=r, column=c, value=val if val != "" else None)

    ws.freeze_panes = "A2"
    ncols = len(headers)
    nrows = len(data) + 1
    ws.auto_filter.ref = f"A1:{get_column_letter(ncols)}{nrows}"
    ws.row_dimensions[1].height = 28

    for col in range(1, ncols + 1):
        letter = get_column_letter(col)
        max_len = 12
        for row in range(1, min(nrows + 1, 300)):
            v = ws.cell(row=row, column=col).value
            if v:
                max_len = max(max_len, min(len(str(v)) + 2, 55))
        ws.column_dimensions[letter].width = max_len

    readme = wb.create_sheet("How to Use", 0)
    readme["A1"] = "Imported from Google Sheet"
    readme["A2"] = f"Rows: {len(data)}"
    readme["A3"] = "Regenerate: python3 import_google_sheet.py"

    wb.save(OUTPUT)
    print(f"Wrote {OUTPUT} ({len(data)} data rows, {ncols} columns)")


def main() -> None:
    headers, data = load_rows()
    build_xlsx(headers, data)


if __name__ == "__main__":
    main()
