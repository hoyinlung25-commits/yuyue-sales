# THE MOON (XVIII) — Complete Production Pack

**Channel Series:** Major Arcana · Faith Disclosure Lofi  
**Card:** XVIII — The Moon  
**Target Duration:** 2 hours (loop)  
**Format:** 16:9 · 1920×1080 · 30fps  
**Language:** English  

---

## Brand Promise for This Episode

> *"What you cannot see in daylight waits for you in the quiet. Tonight, sit with uncertainty — and find peace in it."*

**Closing revelation:**

> *"You came with questions. Leave with trust in your own tides. Your story has already shifted."*

---

## Visual Concept

### Core Aesthetic

Cozy Tower Room × Witch Aesthetic × The Moon symbolism

A mysterious woman sits in silhouette by a gothic tower window. Outside: a luminous full moon, twin distant towers, deep starfield. Inside: amber candlelight, tarot spread, crystal ball, drifting smoke. The mood is dreamy, intuitive, and safe — not horror.

### Reference Images & Loop Videos

| Asset | File | Use |
|-------|------|-----|
| Main scene concept | `assets/the-moon/the-moon-main-scene.png` | Video background base / AI video keyframe |
| **Loop video (30s)** | `assets/the-moon/the-moon-loop-30s.mp4` | Seamless scene loop — repeat for 2hr video |
| **Loop video (15s)** | `assets/the-moon/the-moon-loop-15s.mp4` | Shorter loop variant |
| YouTube thumbnail | `assets/the-moon/the-moon-thumbnail.png` | Thumbnail base (add text in Canva/Figma) |
| Frame overlay mockup | `assets/the-moon/the-moon-frame-overlay.png` | UI border + numeral + title placement |

**Regenerate loops:** `bash scripts/build-the-moon-loop.sh`

#### Loop Video Motion Layers (built from main scene)

| Effect | Method | Cycle |
|--------|--------|-------|
| Breathing zoom | ffmpeg zoompan sin wave | 30s |
| Candle flicker | brightness oscillation (eq) | 3s + 1.77s |
| Moon glow pulse | saturation oscillation | 15s |
| Mystical smoke | PIL overlay + alpha composite | 5s tile |
| Film grain | ffmpeg noise filter | continuous |

### Color Palette

| Role | Hex | Usage |
|------|-----|-------|
| Moonlight Blue | `#1A1F3A` | Window sky, shadows |
| Ethereal Purple | `#6B4C7A` | Smoke, crystal glow |
| Amber Warm | `#C4956A` | Candlelight, skin highlights |
| Silver Mist | `#E8E0D0` | Moon glow, frame accents |
| Deep Wood | `#3D2B1F` | Furniture, bookshelves |

### Fixed Scene Elements (Do Not Change)

- Tower study room layout (bookshelves, arched window, wooden desk)
- Woman silhouette (side profile, long dark hair, knit shawl)
- Crystal ball on desk (left of center)
- 2–3 amber candles (gentle flicker loop)
- Light smoke drift (slow, bottom-up)
- Dried flowers + old books as set dressing

### Card-Specific Elements (The Moon Only)

| Element | Placement | Animation |
|---------|-----------|-----------|
| **Full moon** | Center of window, dominant | Slow pulse glow (8s cycle) |
| **Twin towers** | Distant, flanking moon | Static silhouette |
| **Moon tarot card** | Face-up on desk, lit by candle | Subtle light shimmer |
| **Wolf & dog** | Optional: faint silhouettes in window mist | Very slow fade in/out |
| **Pool reflection** | Crystal ball interior OR desk mirror | Ripple loop (12s) |
| **Crayfish** | Tiny symbol in crystal ball | Barely visible, eerie-cute |

### Frame Overlay (16:9)

```
┌─────────────────────────────────────────────────────┐
│                    XVIII                            │
│  ┌────┐                                  ┌────┐   │
│  │ 🌙 │      [ COZY TOWER ROOM SCENE ]    │ 🌙 │   │
│  │corner│     full moon · candles · smoke  │corner│  │
│  └────┘                                  └────┘   │
│                   THE MOON                          │
└─────────────────────────────────────────────────────┘
```

- **Top center:** `XVIII` — elegant serif, silver-mist color
- **Bottom center:** `THE MOON` — same font, slightly larger
- **Four corners:** Crescent moon + star motifs (identical across all 78 videos)
- **Opacity:** Frame at 85%; scene fully visible in center

---

## Loop Video — Animation Layers

Build as separate layers in After Effects / DaVinci / Canva Video:

| Layer | Element | Loop Duration | Notes |
|-------|---------|---------------|-------|
| L1 | Background painting (static) | — | Base image |
| L2 | Candle flame flicker | 3s | 3 candles, offset timing |
| L3 | Smoke drift | 15s | Soft particle or stock overlay |
| L4 | Moon glow pulse | 8s | Opacity 70%→100%→70% |
| L5 | Clouds across moon | 20s | Very slow, subtle |
| L6 | Crystal ball swirl | 12s | Purple-blue mist inside |
| L7 | Card shimmer | 6s | Light sweep across Moon card |
| L8 | Woman micro-motion | 10s | Slow blink OR hair sway OR page turn |
| L9 | Frame overlay | Static | XVIII + THE MOON |
| L10 | Film grain (optional) | 2s | 5% opacity, adds lofi texture |

**Export:** 2-hour file = 30–60s seamless loop × repeat in editor, OR render 1 master loop and use YouTube loop / ffmpeg concat.

---

## Music Production Spec

### Mood Keywords

Dreamy · Subconscious · Ethereal · Healing · Nocturnal · Intuitive

### Technical Specs

| Parameter | Value |
|-----------|-------|
| BPM | 72–78 |
| Key | D minor or A minor |
| Time signature | 4/4 |
| Loudness target | -14 LUFS (YouTube standard) |
| Fade in | 0:00–0:30 (gentle) |
| Fade out | 1:58:00–2:00:00 |

### Instrumentation

| Layer | Instrument | Character |
|-------|------------|-----------|
| Lead | Rhodes piano | Soft, detuned, sparse melody |
| Pad | Ethereal synth pad | Wide reverb, 40% wet |
| Texture | Crystal bells (sparse) | 1 note every 8–16 bars |
| Bass | Sub bass | Very soft, felt not heard |
| Percussion | Lo-fi vinyl crackle + brushed snare | Minimal, bar 1 and 3 only |
| Ambience | Distant water lap + night crickets (quiet) | -24dB under mix |
| FX | Reverse reverb swells | Every 32 bars, subtle |

### Emotional Arc (2 hours)

| Time | Energy | Description |
|------|--------|-------------|
| 0:00–0:15 | Low → Medium | Opening ritual space; sparse piano |
| 0:15–0:45 | Medium | Pad enters; melody establishes |
| 0:45–1:30 | Medium | Full loop groove; hypnotic |
| 1:30–1:45 | Medium-Low | Strip percussion; return to piano |
| 1:45–2:00 | Low | Fade; reverse reverb; silence |

### Reference Tracks (Mood Only — Do Not Copy)

- Lofi Girl night mixes
- Ólafur Arnalds — ambient piano textures
- Amulets — ethereal pads
- Generic "moon meditation" but with **lofi beat**, not new-age cheese

---

## Audio — Voiceover Scripts

### Voice Direction

- Female voice, mid-20s to 30s
- Soft, intimate, like whispering to a friend
- Pace: ~100 words/minute (slow)
- Reverb: medium hall, 25% wet
- Volume: -18dB under music (barely above)

---

### OPENING RITUAL (0:00 – 1:30)

```
[0:00] (silence, candle crackle, 5 seconds)

[0:05]
"The Moon rises.
And everything you hid from the daylight
...waits for you here."

[0:20]
"Tonight, we sit with uncertainty.
Not to solve it.
But to find peace inside it."

[0:40]
"This is Major Arcana, card eighteen.
The Moon.
The card of dreams, intuition,
and the quiet wisdom of the dark."

[0:55]
"Light a candle, if you can.
Breathe.
Let the music begin."

[1:10]
(music fades in fully)
```

---

### CLOSING WHISPER (1:58:30 – 2:00:00)

```
[1:58:30]
(music fades to piano only)

[1:59:00]
"You came with questions.
Leave with trust in your own tides."

[1:59:30]
"The moon does not rush the night.
Neither should you."

[1:59:50]
"Your story has already shifted.
Goodnight."

[2:00:00]
(silence)
```

---

## YouTube Metadata

### Title Options (pick one)

1. `The Moon 🌙 | Healing Tarot Lofi ~ 2 Hours for Sleep, Dreams & Intuition`
2. `THE MOON · Major Arcana XVIII | Ethereal Lofi for Night Rituals`
3. `The Moon Tarot Lofi 🌙 Cozy Witch Room · 2HR Faith Disclosure`

**Recommended:** Option 1 (best SEO)

---

### Video Description

```
🌙 THE MOON | Major Arcana XVIII

Tonight's faith disclosure:
What you cannot see in daylight waits for you in the quiet.

▸ Card: The Moon (XVIII)
▸ Visual: Cozy tower room · full moon · twin towers · crystal ball · amber candles
▸ Music: Dreamy lofi · ethereal pads · subconscious · 72 BPM
▸ Duration: 2 hours seamless loop

—
✦ ABOUT THIS SERIES

Each video is one tarot card and one hour of healing lofi.
Not just background music — a quiet revelation.
Sit with the card. Let the music shift your inner story.

Your story will change.

—
⏱ TIMESTAMPS
0:00 — Opening Ritual
0:15 — Main Journey begins
1:58:30 — Closing Whisper

—
🔮 THE MOON — CARD MEANING (brief)

The Moon speaks of intuition, dreams, and the unknown.
It asks you to trust what you feel, even when you cannot see the path.
Fear and wonder live in the same night sky.

Tonight's revelation:
"What you fear in the dark is often what wants to heal."

—
🎧 Best for: sleep, night study, journaling, tarot meditation, anxiety relief

—
📂 PLAYLIST: Major Arcana — 22 Faith Disclosures
[Link to playlist when live]

—
#tarotlofi #themoon #majarcana #healingmusic #lofi #witchaesthetic 
#cottagecore #tarot #sleepmusic #studymusic #faithdisclosure #moonmusic
```

---

### Tags (500 char limit)

```
tarot lofi, the moon tarot, major arcana, healing lofi, sleep music, 
ethereal lofi, witch aesthetic, cozy room lofi, tarot meditation, 
moon music, intuitive music, dreamy lofi, 2 hours lofi, 
faith disclosure, spiritual lofi, night music, study music, 
cottagecore aesthetic, crystal healing music, ambient lofi
```

---

### Thumbnail Spec

**Base image:** `assets/the-moon/the-moon-thumbnail.png`

**Text overlay (add in Figma/Canva):**

| Element | Font | Color | Position |
|---------|------|-------|----------|
| THE MOON | Cormorant Garamond Bold, 72px | `#E8E0D0` | Bottom third, centered |
| healing tarot lofi | Inter Light, 28px | `#C4956A` | Below title |
| XVIII | Cormorant Garamond, 36px | `#6B4C7A` | Top left corner |

**Rules:**
- Same template for all 78 cards — only change title, numeral, accent color
- Woman silhouette always on left third
- Moon always dominant in background

---

## Faith Disclosure Copy

### One-Line Revelation (for social / community post)

> **The Moon** — *"What you fear in the dark is often what wants to heal."*

### Instagram / TikTok Caption

```
🌙 Episode XVIII — THE MOON

Tonight's disclosure:
What you cannot see in daylight waits for you in the quiet.

Sit by the window. Light a candle.
Two hours of dreamy tarot lofi for your night ritual.

Your story will change. ✦

🔗 Link in bio

#tarotlofi #themoon #witchaesthetic #healingmusic #lofi #majarcana
```

### Community Tab Post (YouTube)

```
🌙 Tonight's Card: THE MOON (XVIII)

Do you pull this card often? 
The Moon is about trusting your intuition — even when the path isn't clear.

Drop a 🌙 if you're listening tonight.
What are you sitting with in the quiet?
```

---

## Production Checklist

### Pre-Production
- [ ] Finalize main scene illustration (use concept as base)
- [ ] Design frame overlay template (reusable for 78 cards)
- [ ] Record voiceover (opening + closing)
- [ ] Compose / license 2-hour lofi track

### Production
- [ ] Animate loop layers (see Layer table above)
- [ ] Composite frame overlay
- [ ] Mix voiceover under music
- [ ] Master audio to -14 LUFS
- [ ] Render 2-hour video (H.264, 1080p)

### Post-Production
- [ ] Create thumbnail from template
- [ ] Upload with metadata (title, description, tags)
- [ ] Add to "Major Arcana" playlist
- [ ] Schedule Community post
- [ ] Pin comment with card meaning + revelation

### Quality Check
- [ ] Loop is seamless (no visible jump at repeat point)
- [ ] Voiceover audible but not dominant
- [ ] Text (XVIII / THE MOON) readable on mobile
- [ ] Thumbnail readable at small size
- [ ] No copyright issues on music

---

## File Naming Convention

```
the-moon-xviii-main-scene.png
the-moon-xviii-loop-master.mp4
the-moon-xviii-audio-master.wav
the-moon-xviii-final-2hr.mp4
the-moon-xviii-thumbnail.png
the-moon-xviii-vo-opening.wav
the-moon-xviii-vo-closing.wav
```

---

## Timeline Summary

| Timecode | Section | Content |
|----------|---------|---------|
| 0:00:00 | Black + candle crackle | 5s silence |
| 0:00:05 | Opening VO | Faith disclosure intro |
| 0:01:10 | Music in | Main lofi journey |
| 0:01:10–1:58:30 | Loop | Scene animation + music |
| 1:58:30 | Closing VO | Final revelation |
| 2:00:00 | End | Silence |

---

## Next Cards After The Moon

Recommended release order for channel launch:

1. ✅ **The Moon** (XVIII) — this pack
2. **The Star** (XVII) — hope, healing pair
3. **The High Priestess** (II) — intuition trilogy
4. **The Sun** (XIX) — contrast / uplift
5. **The World** (XXI) — series milestone

---

*Production pack v1.0 · The Moon · Major Arcana Faith Disclosure Lofi*
