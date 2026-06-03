#!/usr/bin/env python3
"""Clean and upgrade Google Sheet pipeline data → CSV + Excel."""

from __future__ import annotations

import csv
import re
from datetime import datetime
from pathlib import Path

BASE = Path(__file__).parent
RAW_CSV = BASE / "google_sheet_raw.csv"
UPGRADED_CSV = BASE / "google_sheet_upgraded.csv"
OUTPUT_XLSX = BASE / "client_base.xlsx"
POLICIES_CSV = BASE / "policies_register.csv"

OUT_HEADERS = [
    "Priority Rank",
    "Category",
    "Priority Score",
    "Next Action",
    "Stage",
    "Is Policy Client",
    "Policy Match",
    "Product Tags",
    "英文名",
    "Nick Name",
    "Phone",
    "Gender",
    "Age",
    "Relationship",
    "Rel Score (1-5)",
    "Possibility (1-5)",
    "Job",
    "Area",
    "Income",
    "Remarks",
    "Last Noted",
    "Next Appt / Follow-up",
    "L0",
    "Invited",
    "L1",
    "L2",
    "NEED",
    "Close",
    "Interest",
]


def norm_name(s: str) -> str:
    return re.sub(r"[^a-z0-9]", "", (s or "").lower())


def load_policy_names() -> set[str]:
    names = set()
    if not POLICIES_CSV.exists():
        return names
    with POLICIES_CSV.open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            names.add(norm_name(row.get("policyowner", "")))
    return names


def parse_int(s: str, default: int = 0) -> int:
    m = re.search(r"\d+", str(s or ""))
    return int(m.group()) if m else default


def normalize_phone(s: str) -> str:
    digits = re.sub(r"\D", "", s or "")
    if len(digits) == 8:
        return digits
    if len(digits) == 11 and digits.startswith("852"):
        return digits[3:]
    return digits if digits else ""


def extract_products(text: str) -> str:
    t = (text or "").upper()
    tags = []
    for key, label in [
        (r"\bCI\b|CRITICAL", "CI"),
        (r"EFG|GGG", "Savings/EFG"),
        (r"MEDICAL|MEDIC", "Medical"),
        (r"QDAP", "QDAP"),
        (r"RECRUIT", "Recruit"),
        (r"RETIRED|RETIRE", "Retirement"),
        (r"SU10|SU\+", "SU"),
        (r"IJ|INCOMEJOY", "IncomeJoy"),
        (r"FYC", "FYC"),
        (r"GI\b", "GI"),
    ]:
        if re.search(key, t):
            tags.append(label)
    return ", ".join(dict.fromkeys(tags))


def detect_stage(row_map: dict) -> str:
    """Single funnel stage from scattered columns."""
    for key in ("L2", "L1", "Invited", "L0", "Contacted", "Noted"):
        val = (row_map.get(key) or "").strip().lower()
        if val in ("l2", "l1", "l0", "l3", "invited"):
            return val.upper().replace("L3", "L3")
        if val and key in ("L2", "L1", "L0"):
            return val.upper()
    contacted = (row_map.get("Contacted") or "").strip()
    if contacted:
        return contacted.upper()
    noted = (row_map.get("Noted") or "").strip().lower()
    if noted in ("l0", "l1", "l2", "l3"):
        return noted.upper()
    return "NEW"


def category_from_score(score: int, stage: str, is_client: bool) -> str:
    if is_client:
        return "Client"
    if stage in ("L2", "L3") or score >= 8:
        return "Hot"
    if stage == "L1" or score >= 6:
        return "Warm"
    if score >= 4:
        return "Nurture"
    return "Low"


def priority_score(
    rel: int, poss: int, stage: str, has_phone: bool, has_appt: bool, is_client: bool
) -> int:
    score = rel + poss
    stage_bonus = {"L2": 3, "L3": 3, "L1": 2, "L0": 1, "INVITED": 1}.get(stage, 0)
    score += stage_bonus
    if has_phone:
        score += 1
    if has_appt:
        score += 2
    if is_client:
        score += 2
    return score


def read_raw_rows() -> list[dict]:
    with RAW_CSV.open(encoding="utf-8-sig") as f:
        rows = list(csv.reader(f))
    if len(rows) < 2:
        return []
    headers = [re.sub(r"\s+", " ", h.replace("\n", " ")).strip() for h in rows[0]]

    def col_idx(name_part: str) -> int | None:
        for i, h in enumerate(headers):
            if name_part.lower() in h.lower():
                return i
        return None

    idx = {
        "appt": 0,
        "en": col_idx("英文名") or 1,
        "nick": col_idx("Nick") or 2,
        "phone": col_idx("Contact") or 3,
        "gender": col_idx("Gender") or 4,
        "age": col_idx("Age") or 5,
        "rel": col_idx("Relationship") if col_idx("Relationship") != col_idx("Relationship (1-5)") else 6,
        "rel_score": col_idx("Relationship (1-5)") or col_idx("(1-5)") or 7,
        "poss": col_idx("Possibility") or 8,
        "job": col_idx("Job") or 9,
        "area": col_idx("Location") or 10,
        "income": col_idx("Income") or 11,
        "remarks": col_idx("Remarks") if headers.count("Remarks") == 1 else 13,
        "contacted": col_idx("Contacted") or 14,
        "noted": col_idx("Noted") or 15,
        "l0": col_idx("L0") or 16,
        "inv": col_idx("Invited") or 17,
        "l1": col_idx("L1") or 18,
        "l2": col_idx("L2") or 19,
        "need": col_idx("NEED") or 20,
        "close": col_idx("Close") or 21,
        "interest": col_idx("Interest") or 22,
    }

    records = []
    for raw in rows[1:]:
        if not any(str(c).strip() for c in raw):
            continue

        def g(i: int | None) -> str:
            if i is None or i >= len(raw):
                return ""
            return str(raw[i]).strip()

        row_map = {
            "APPT TIME": g(idx["appt"]),
            "英文名": g(idx["en"]),
            "Nick Name": g(idx["nick"]),
            "Contact": g(idx["phone"]),
            "Gender": g(idx["gender"]),
            "Age": g(idx["age"]),
            "Relationship": g(idx["rel"]),
            "Relationship (1-5)": g(idx["rel_score"]),
            "Possibility": g(idx["poss"]),
            "Job": g(idx["job"]),
            "Job Location": g(idx["area"]),
            "Income": g(idx["income"]),
            "Remarks": g(idx["remarks"]),
            "Contacted": g(idx["contacted"]),
            "Noted": g(idx["noted"]),
            "L0": g(idx["l0"]),
            "Invited": g(idx["inv"]),
            "L1": g(idx["l1"]),
            "L2": g(idx["l2"]),
            "NEED": g(idx["need"]),
            "Close": g(idx["close"]),
            "Interest": g(idx["interest"]),
        }
        records.append(row_map)
    return records


def transform(records: list[dict], policy_names: set[str]) -> list[list]:
    out = []
    for r in records:
        en = r.get("英文名", "")
        nick = r.get("Nick Name", "")
        phone = normalize_phone(r.get("Contact", ""))
        rel_s = parse_int(r.get("Relationship (1-5)", ""), 0)
        poss = parse_int(r.get("Possibility", ""), 0)
        stage = detect_stage(r)
        appt = r.get("APPT TIME", "")
        remarks = r.get("Remarks", "")
        noted = r.get("Noted", "")

        nn = norm_name(en)
        # Fuzzy match: e.g. Yu Chun Kit → YU CHUN KIN, Ng Ki Yi → NG KA YI
        is_client = nn in policy_names
        if not is_client and len(nn) >= 6:
            for pn in policy_names:
                if len(pn) >= 6 and nn[:6] == pn[:6]:
                    is_client = True
                    break
                if nn in pn or pn in nn:
                    is_client = True
                    break
        policy_match = ""
        if is_client:
            for pn in policy_names:
                if nn and (nn == pn or (len(nn) > 5 and (nn in pn or pn in nn))):
                    policy_match = pn.upper()
                    break

        score = priority_score(rel_s, poss, stage, bool(phone), bool(appt), is_client)
        cat = category_from_score(score, stage, is_client)
        products = extract_products(f"{remarks} {appt} {r.get('Interest','')}")

        out.append(
            [
                0,  # rank filled later
                cat,
                score,
                appt or noted or "",
                stage,
                "Yes" if is_client else "",
                policy_match,
                products,
                en,
                nick,
                phone,
                r.get("Gender", ""),
                r.get("Age", ""),
                r.get("Relationship", ""),
                rel_s or "",
                poss or "",
                r.get("Job", ""),
                r.get("Job Location", ""),
                r.get("Income", ""),
                remarks,
                noted if noted and noted.lower() not in ("l0", "l1", "l2") else "",
                noted if noted.lower() in ("l0", "l1", "l2", "l3") else r.get("Contacted", ""),
                r.get("L0", ""),
                r.get("Invited", ""),
                r.get("L1", ""),
                r.get("L2", ""),
                r.get("NEED", ""),
                r.get("Close", ""),
                r.get("Interest", ""),
            ]
        )

    out.sort(key=lambda x: (-x[2], x[3] == "", x[8]))
    for i, row in enumerate(out, 1):
        row[0] = i
    return out


def write_upgraded_csv(rows: list[list]) -> None:
    with UPGRADED_CSV.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(OUT_HEADERS)
        w.writerows(rows)


def build_excel(rows: list[list], policy_rows: list[list]) -> None:
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Font, PatternFill
    from openpyxl.utils import get_column_letter
    from openpyxl.worksheet.datavalidation import DataValidation

    wb = Workbook()
    wb.remove(wb.active)
    fill = PatternFill(start_color="1F4E79", end_color="1F4E79", fill_type="solid")
    hfont = Font(bold=True, color="FFFFFF", size=11)

    def write(ws, headers, data, start=1):
        for c, h in enumerate(headers, 1):
            cell = ws.cell(row=start, column=c, value=h)
            cell.fill = fill
            cell.font = hfont
        for r, row in enumerate(data, start + 1):
            for c, val in enumerate(row, 1):
                ws.cell(row=r, column=c, value=val if val != "" else None)
        ws.freeze_panes = ws.cell(row=start + 1, column=1).coordinate
        nrows = start + len(data)
        ws.auto_filter.ref = f"A{start}:{get_column_letter(len(headers))}{nrows}"
        return nrows

    # Dashboard
    dash = wb.create_sheet("Dashboard", 0)
    hot = sum(1 for r in rows if r[1] == "Hot")
    warm = sum(1 for r in rows if r[1] == "Warm")
    clients = sum(1 for r in rows if r[1] == "Client")
    with_appt = sum(1 for r in rows if r[3])
    l1l2 = sum(1 for r in rows if r[4] in ("L1", "L2", "L3"))
    dash["A1"] = "Pipeline Dashboard"
    dash["A1"].font = Font(bold=True, size=16)
    stats = [
        ("Total contacts", len(rows)),
        ("Hot", hot),
        ("Warm", warm),
        ("Policy clients in list", clients),
        ("Has next action written", with_appt),
        ("Stage L1/L2/L3", l1l2),
        ("Updated", datetime.now().strftime("%Y-%m-%d %H:%M")),
        ("Google Sheet", f"https://docs.google.com/spreadsheets/d/1qPNnq7tOPYX5Rk4UpiL9UaCCbEyRseC-g2-LC6itupM/edit"),
    ]
    for i, (k, v) in enumerate(stats, 3):
        dash.cell(row=i, column=1, value=k)
        dash.cell(row=i, column=2, value=v)
    dash.column_dimensions["A"].width = 28
    dash.column_dimensions["B"].width = 50

    # Pipeline Upgraded
    pipe = wb.create_sheet("Pipeline Upgraded")
    write(pipe, OUT_HEADERS, rows)

    # This Week
    week = wb.create_sheet("This Week Focus")
    week_headers = OUT_HEADERS[:12]
    week_data = [
        r[:12] for r in rows if r[1] in ("Hot", "Client") or (r[3] and r[1] != "Low")
    ][:25]
    write(week, week_headers, week_data)

    # Policies
    if policy_rows:
        pol = wb.create_sheet("Policies")
        ph = [
            "銷售團隊",
            "代理人",
            "權益人",
            "受保人",
            "保單號碼",
            "基本計劃",
            "投保日期",
            "簽發日期",
            "狀態",
            "供款年期",
            "到期日",
            "運單號碼",
        ]
        write(pol, ph, policy_rows)

    # Lookup
    lk = wb.create_sheet("Lookup")
    lk["A1"] = "Stage"
    lk["B1"] = "Meaning"
    stages = [
        ("NEW", "Not yet contacted / no stage set"),
        ("L0", "Lead — initial contact"),
        ("L1", "Meeting / needs analysis"),
        ("L2", "Quote / follow-up"),
        ("L3", "Closing"),
        ("Client", "Already has in-force policy"),
    ]
    for i, (a, b) in enumerate(stages, 2):
        lk.cell(row=i, column=1, value=a)
        lk.cell(row=i, column=2, value=b)
    lk["D1"] = "Category"
    lk["E1"] = "Action"
    cats = [
        ("Hot", "Call this week"),
        ("Warm", "WhatsApp + book L1"),
        ("Client", "Service + referral"),
        ("Nurture", "Monthly touch"),
        ("Low", "Batch message only"),
    ]
    for i, (a, b) in enumerate(cats, 2):
        lk.cell(row=i, column=4, value=a)
        lk.cell(row=i, column=5, value=b)

    # Validation on Pipeline
    dv = DataValidation(
        type="list",
        formula1='"Hot,Warm,Nurture,Low,Client"',
        allow_blank=True,
    )
    dv.add(f"B2:B500")
    pipe.add_data_validation(dv)
    dv2 = DataValidation(type="list", formula1='"NEW,L0,L1,L2,L3,Client"', allow_blank=True)
    dv2.add(f"E2:E500")
    pipe.add_data_validation(dv2)

    # Raw archive
    if RAW_CSV.exists():
        with RAW_CSV.open(encoding="utf-8-sig") as f:
            raw = list(csv.reader(f))
        arch = wb.create_sheet("Archive Raw")
        if raw:
            write(arch, [re.sub(r"\s+", " ", h)[:40] for h in raw[0]], raw[1:])

    readme = wb.create_sheet("How to Use")
    lines = [
        ("Upgraded client base", ""),
        ("Pipeline Upgraded", "Clean columns + priority score — import to Google"),
        ("This Week Focus", "Top 25 actions"),
        ("google_sheet_upgraded.csv", "Upload to Google: File → Import → Replace sheet"),
        ("Refresh", "python3 upgrade_pipeline.py"),
    ]
    for i, (a, b) in enumerate(lines, 1):
        readme.cell(row=i, column=1, value=a)
        readme.cell(row=i, column=2, value=b)

    wb.save(OUTPUT_XLSX)


def main() -> None:
    if not RAW_CSV.exists():
        from import_google_sheet import fetch_google_sheet

        fetch_google_sheet()

    policy_names = load_policy_names()
    records = read_raw_rows()
    rows = transform(records, policy_names)
    write_upgraded_csv(rows)

    policy_data = []
    if POLICIES_CSV.exists():
        with POLICIES_CSV.open(encoding="utf-8") as f:
            policy_data = list(csv.reader(f))[1:]

    build_excel(rows, policy_data)
    print(f"Upgraded {len(rows)} contacts → {UPGRADED_CSV.name}, {OUTPUT_XLSX.name}")


if __name__ == "__main__":
    main()
