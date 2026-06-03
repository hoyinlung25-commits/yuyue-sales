# Client base (yuyue-sales)

| File | Purpose |
|------|---------|
| **`client_base.xlsx`** | Excel workbook — **policy screenshot data only** |
| `policies_register.csv` | Source data from your policy book screenshots |
| `build_excel.py` | Regenerate: `python3 build_excel.py` |

## Excel sheets

1. **Policies** — matches your screenshots (銷售團隊, 代理人, 權益人, 保單號碼, 基本計劃, etc.)
2. **Clients Summary** — grouped view (inforce count per client) derived from Policies only

Prospect/network PDF data has been **removed** from the workbook.

## Google Sheet

To use your Google Sheet as the source, see **`GOOGLE_SHEET_IMPORT.md`** and run `import_google_sheet.py`.
