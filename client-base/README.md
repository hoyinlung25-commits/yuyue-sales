# Client base (yuyue-sales)

| File | Purpose |
|------|---------|
| **`client_base.xlsx`** | Main workbook (Google Sheet + policy screenshots) |
| `google_sheet_raw.csv` | Latest download from your Google Sheet |
| `policies_register.csv` | Policy book from screenshots |
| `import_google_sheet.py` | Sync sheet → Excel: `python3 import_google_sheet.py` |

## Google Sheet (live source)

https://docs.google.com/spreadsheets/d/1qPNnq7tOPYX5Rk4UpiL9UaCCbEyRseC-g2-LC6itupM/edit

## Excel sheets

| Sheet | Content |
|-------|---------|
| **Prospects & Pipeline** | Your Google Sheet (~104 contacts) |
| **Policies** | In-force book from screenshots (31 policies) |
| **How to Use** | Summary + refresh instructions |

Refresh after editing Google Sheet:

```bash
cd client-base && python3 import_google_sheet.py
```
