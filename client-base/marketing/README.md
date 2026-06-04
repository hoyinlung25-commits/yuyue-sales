# Plant gift — WhatsApp poster

## Files

| File | Use |
|------|-----|
| **`plant-appointment-poster.png`** | Send this image on WhatsApp |
| `plant-appointment-poster.html` | Edit text/design, then re-export |
| `WHATSAPP_CAPTION.txt` | Copy-paste message with the image |

## What was removed (per your request)

- All **PP** branding and logos  
- All **prices** and MUJI comparisons  
- QR “scan to buy” — replaced with **WhatsApp「預約」** CTA  

## Re-export PNG after editing HTML

```bash
google-chrome --headless=new --disable-gpu --window-size=1080,1920 \
  --screenshot=plant-appointment-poster.png \
  "file://$(pwd)/plant-appointment-poster.html"
```

## Customise

Open `plant-appointment-poster.html` in a browser to preview. Change:

- Your name / team in footer  
- CTA keyword (`預約` → `植物` etc.)  
- Plant list or features  
