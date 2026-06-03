# Google Sheet upgrade guide

Your sheet has been restructured for clearer follow-up and priority. Use the files below to update Google Sheets.

## What improved

| Before | After |
|--------|--------|
| Duplicate columns (Relationship, Remarks ×2) | Single clean columns |
| Funnel split across L0/L1/L2/Contacted/Noted | One **Stage** column + original fields kept |
| APPT TIME mixed with names | **Next Action** column (tasks visible) |
| Hard to see who to call first | **Priority Score** + **Category** (Hot/Warm/Client…) |
| No link to policy book | **Is Policy Client** flags (e.g. Leung Wai Ki, Lung On Ki) |
| Product buried in remarks | **Product Tags** (CI, Medical, EFG, etc.) |
| Missing phones scattered | **Phone** normalized (8-digit HK) |

## Apply upgrade to Google Sheets (recommended)

1. Open your sheet:  
   https://docs.google.com/spreadsheets/d/1qPNnq7tOPYX5Rk4UpiL9UaCCbEyRseC-g2-LC6itupM/edit

2. Add a **new tab** named `Pipeline Upgraded` (do not delete the old tab yet).

3. In the repo, open **`client-base/google_sheet_upgraded.csv`**.

4. In Google Sheets: **File → Import → Upload** → select `google_sheet_upgraded.csv`.

5. Import location: **Replace current sheet** (if you created empty `Pipeline Upgraded`)  
   OR **Insert new sheet(s)**.

6. Optional — hide the old messy tab after you confirm data looks correct.

## Excel workbook (local)

**`client_base.xlsx`** sheets:

- **Dashboard** — counts (Hot / Warm / clients)
- **Pipeline Upgraded** — full cleaned list (use for Google import)
- **This Week Focus** — top priorities
- **Policies** — in-force book from screenshots
- **Lookup** — stage & category meanings
- **Archive Raw** — original download backup

## Refresh after you edit Google

```bash
cd client-base
python3 import_google_sheet.py    # download latest from Google
python3 upgrade_pipeline.py       # rebuild upgrade + Excel
```

## Optional: Google Apps Script

Copy `google_apps_script.js` into **Extensions → Apps Script** to add menu **Client Base → Sort by Priority** on the upgraded tab.
