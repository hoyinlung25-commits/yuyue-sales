# client_base.xlsx — User guide

## Open this file

**`client_base.xlsx`** — use Excel, WPS, or Apple Numbers.

---

## Sheets (tabs)

| Tab | What it does |
|-----|----------------|
| **Start Here** | Quick instructions |
| **Dashboard** | Overview counts (Hot / Warm / Clients) |
| **➕ Add New Client** | Form to add someone new |
| **Clients** | Full list + green rows at bottom for new entries |
| **This Week** | Top priorities to call |
| **Policies** | In-force policies from your book |

---

## Add a new client (easy way)

### Method A — Green rows on **Clients** tab

1. Scroll to the bottom → light **green** rows labelled “ADD NEW CLIENTS BELOW”.
2. Type directly — use **dropdowns** for Category, Stage, Gender.
3. Press **Tab** to move across; the table expands as you add rows.

### Method B — **➕ Add New Client** form

1. Fill the **yellow** cells (name, phone, category, etc.).
2. The **green row** below updates automatically.
3. Select that entire green row → **Copy**.
4. Go to **Clients** → click first empty green row → **Paste**.

---

## Colours

| Colour | Meaning |
|--------|---------|
| Red tint | **Hot** lead — call soon |
| Green tint | **Client** — already has policy |
| Orange tint | **Warm** — book a meeting |
| Light green rows | Where to add new people |

---

## Refresh from Google Sheet

```bash
cd client-base
python3 import_google_sheet.py
```

This downloads your Google Sheet and rebuilds a fresh `client_base.xlsx`.
