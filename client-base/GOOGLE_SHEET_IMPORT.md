# Import from Google Sheets

Your sheet:  
https://docs.google.com/spreadsheets/d/1qPNnq7tOPYX5Rk4UpiL9UaCCbEyRseC-g2-LC6itupM/edit

This environment **cannot sign in to Google**, so the link must be public **or** you export a file.

---

## Option A — Make link viewable (fastest for auto-sync)

1. Open the sheet → **Share** (top right).
2. Under **General access**, choose **Anyone with the link** → role **Viewer**.
3. Click **Done**.
4. Tell the agent to retry, or run locally:

```bash
cd client-base
curl -L "https://docs.google.com/spreadsheets/d/1qPNnq7tOPYX5Rk4UpiL9UaCCbEyRseC-g2-LC6itupM/export?format=csv&gid=0" -o google_sheet_raw.csv
python3 import_google_sheet.py
```

To import a **specific tab**, change `gid=0` to the tab’s gid (visible in the sheet URL when you click that tab).

---

## Option B — Download and upload (most private)

1. In Google Sheets: **File → Download → Microsoft Excel (.xlsx)** or **Comma Separated Values (.csv)**.
2. Save as `client-base/google_sheet_raw.xlsx` or `google_sheet_raw.csv`.
3. Run:

```bash
cd client-base && python3 import_google_sheet.py
```

This rebuilds **`client_base.xlsx`** from your sheet.

---

## Option C — Publish to web (read-only export)

1. **File → Share → Publish to web**.
2. Choose the sheet tab and **Comma-separated values (.csv)**.
3. Copy the publish link and share it with the agent.
