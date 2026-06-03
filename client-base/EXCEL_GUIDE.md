# client_base.xlsx — User guide

## Sheets

| Tab | Purpose |
|-----|---------|
| **Start Here** | Instructions |
| **Dashboard** | KPIs + live referral/birthday counts |
| **➕ Add New Client** | Form with referral & birthday fields |
| **Clients** | Master list (all functions) |
| **Referral System** | Champions, scripts, referral log |
| **Birthdays** | Auto-list birthdays within 30 days |
| **Approach Funnel** | Count by approach status |
| **This Week** | Priority calls |
| **Policies** | In-force policies |

---

## Referral system

On **Clients** sheet:

| Column | Use |
|--------|-----|
| **Referral Tier** | Auto: Champion / High Potential / Standard (updates when Referrals Given changes) |
| **Referral Asked?** | Dropdown: No → Yes - will refer → Yes - referred someone |
| **Referrals Given** | Number of people they introduced |
| **Referred By** | Who introduced this prospect |
| **Last Referral Date** | When you received the intro |
| **Referral Notes** | Free text |

**Referral System** tab:

- Top **champions** to call first  
- **WhatsApp scripts** (Cantonese)  
- **Referral log** — write each new introduction  

---

## Customer birthdays

1. On **Clients**, enter **Birthday** (column W) — use date format `1990-05-15` or Excel date picker.  
2. **Days to Birthday** (column X) calculates automatically.  
3. **Birthday ≤30d?** shows **YES** when within 30 days.  
4. Open **Birthdays** tab — names appear automatically (may need Excel to recalculate: press `F9`).

**Suggested action** on Birthdays tab: Champion → birthday + referral ask; others → birthday message only.

---

## Client approach status

| Column | Use |
|--------|-----|
| **Approach Status** | Dropdown: Not contacted → Meeting → Quoted → Active client → Lost |
| **Next Touch Date** | Your next follow-up date |

**Approach Funnel** tab shows how many people are at each stage (live `COUNTIF` formulas).

---

## Add new client

1. **➕ Add New Client** — fill yellow cells (including birthday & approach status).  
2. Copy the green row → paste into **Clients** (green rows at bottom).  

---

## Refresh data

```bash
cd client-base && python3 import_google_sheet.py
```
