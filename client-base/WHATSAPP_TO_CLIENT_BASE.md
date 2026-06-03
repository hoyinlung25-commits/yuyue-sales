# Build your client base from WhatsApp (step-by-step)

Your WhatsApp login stays on **your** phone or computer. This project cannot read WhatsApp directly. Use this guide to move chat information into `template_clients.csv`, then share that file here for analysis.

## Step 1 — Export chats (5–15 minutes per important contact)

### Android
1. Open the chat with a **client or prospect**.
2. Tap **⋮** (menu) → **More** → **Export chat**.
3. Choose **Without media** (faster) unless you need images of policies.
4. Save the `.txt` file and repeat for your top 20–50 business chats.

### iPhone
1. Open the chat → tap the contact name at the top.
2. Scroll down → **Export Chat**.
3. Choose **Without Media** if possible.

### WhatsApp Business (optional)
Use **Labels** (e.g. `Client`, `Prospect`, `Renewal`) so you know which chats to export first.

## Step 2 — Fill the spreadsheet

Open `template_clients.csv` in Excel or Google Sheets. One row per person.

| Column | What to put |
|--------|-------------|
| `name` | As in WhatsApp |
| `phone` | Full number with country code |
| `last_contact_date` | From last message in chat |
| `relationship_stage` | `prospect` / `quoted` / `client` / `lost` / `referral_partner` |
| `products_held` | e.g. `auto`, `life`, `health` (comma-separated) |
| `products_interested` | What they asked about in chat |
| `referral_potential_score_1_5` | 5 = happy multi-product client; 1 = cold or unhappy |
| `next_action_date` | Your next follow-up |
| `next_action` | e.g. `call renewal review`, `send quote` |
| `notes` | 1–2 lines from chat (no sensitive health IDs) |

You do **not** need every column on day one. Minimum: `name`, `phone`, `last_contact_date`, `relationship_stage`, `next_action_date`, `next_action`.

## Step 3 — Upload for analysis

1. Save your filled file as `clients.csv` in this folder, **or**
2. Paste 15–30 rows (with headers) into the chat, **or**
3. Paste short excerpts from 3–5 export `.txt` files (remove personal unrelated messages).

We will then:
- Rank **referral champions**
- List **follow-ups due this week**
- Suggest **product gaps** and bundles by segment

## Privacy

- Do not commit real phone numbers to a public GitHub repo unless you intend to.
- Redact ID numbers and detailed health information in `notes`.

## Quick scan method (30 minutes)

If export is too slow, scroll your **Recent chats** and add anyone who:
- Bought or discussed insurance in the last 12 months
- Asked for a quote you never closed
- Referred someone or said they would
- Has a renewal coming up

Aim for **20 rows first**, then expand.
