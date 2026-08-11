# EP02 — 影片 Prompt（10 秒 × 3 段）

**用途：** YouTube 開場 / 故事 intro · 三段各 10 秒，CapCut 拼接成 **30 秒**  
**風格：** Vintage Hong Kong Movie · 1996 City Pop · 真人電影感  

---

## 共用 GLOBAL LOCK（三段都要貼在最前）

```text
GLOBAL LOCK — do not change across all frames:
Same fictional Hong Kong office worker man, age 28, slim build, short neat black hair,
white dress shirt with sleeves rolled to forearms, dark tie loosened, black trousers,
1990s black pager on belt, tired gentle face, natural skin texture, live-action only.
Live-action vintage Hong Kong cinema. NOT anime, NOT cartoon, NOT 3D, NOT horror.
```

---

## Part A — 前 10 秒｜錯過末班車

**故事：** 獨站空月台 → pager 閃 → 轉身離開  
**首幀參考：** `ep02_scene_02_missed_last_train.png`  
**尾幀：** 男人背對鏡頭，向月台出口方向走，步態開始移動（與 Part B 首幀銜接）

### Prompt A（貼 Flova · 10 s）

```text
GLOBAL LOCK — [貼上共用 LOCK]

SCENE:
1996 Hong Kong night, empty MTR platform after last train departed. Teal and magenta
neon ceiling tubes, wet glossy floor reflections, closed silver train doors on right,
yellow safety line. Light rain in air. City pop melancholy, film grain, shallow DOF.

ACTION — exactly 10 seconds, one shot, no cuts:
0:00–0:03  Wide hold. Man alone at platform edge, hands in pockets, facing closed
            train doors. Neon flickers softly.
0:03–0:06  Slow dolly-in (5%). He exhales, eyes drop to pager on belt — LED blinks
            once. He does not touch it.
0:06–0:10  He turns away from train, begins walking toward platform exit, camera
            slow pan following from behind-left. End frame: back view mid-stride,
            shoulders level, same shirt and pager visible.

CAMERA: slow dolly-in then slow follow pan. No shake, no whip, 24fps film blur.
LIGHTING: cool teal-magenta only. No warm door light yet.

NEGATIVE: extra people, smartphone, running, text, logo, watermark, face morph,
          clothing change, bartender, bar interior visible.
```

**Flova 設定 A：** Duration **10 s** · 16:9 · First frame = scene_02 · Final frame = 背向走動

---

## Part B — 後 10 秒｜看見 12:07 的門

**故事：** 走廊尽头琥珀光 → 側脸停步 → 向門踏一步  
**首幀：** 接 Part A 尾幀（背向走動同一男人）  
**尾幀參考：** `ep02_scene_03_door_1207.png`

### Prompt B（貼 Flova · 10 s）

```text
GLOBAL LOCK — [貼上共用 LOCK]

SCENE:
1996 Hong Kong night, MTR corridor just off the platform. Tiled walls, wet floor,
teal-magenta spill from behind. Ahead: narrow door with warm amber light leaking
through crack, rain mist in backlight. Hidden bar entrance at 12:07 mood.

ACTION — exactly 10 seconds, one shot, no cuts:
0:00–0:03  Continue from behind: same man walking mid-stride in corridor, same white
            shirt and pager. Camera follows slowly from behind.
0:03–0:06  He slows and stops. Warm amber glow from door ahead grows on his face and
            shirt edge. Shoulders relax slightly.
0:06–0:10  Cut to medium side-profile (or slow arc to side): he stares at the door,
            one slow step forward, expression from exhaustion to quiet curiosity.
            End frame: side profile, one foot forward, eyes on door, hold still.

CAMERA: slow follow then slow arc to side profile. No cuts feel like jump cut — smooth.
LIGHTING: transition cool platform neon → warm amber on face from door.

NEGATIVE: extra people, smartphone, running, text on door, logo, watermark, bartender
          visible inside, red vinyl, supernatural glow, horror, face morph, clothing change.
```

**Flova 設定 B：** Duration **10 s** · 16:9 · First frame = Part A 尾幀 export · Final frame = scene_03

---

## Part C — 第三 10 秒｜酒吧讀信

**故事：** 空吧檯前展信 → 靜讀 → 輕微動容（配《來自2026年的信》）  
**首幀參考：** `ep02_scene_04_letter_in_bar.png`（或 Part B 尾幀接「推門進入」後的第一帧）  
**尾幀：** 同一坐姿，信紙在手中，視線落在信上，表情比開頭柔和

### Prompt C（貼 Flova · 10 s）

```text
GLOBAL LOCK — [貼上共用 LOCK]

SCENE:
Inside hidden timeless bar at 12:07 AM, 1996 Hong Kong. Same office worker now seated
alone at dark polished wood bar counter. Warm amber lamp light on face, cold blue rain
on window far background softly blurred. Empty bar — no bartender, no other customers.
Black vinyl on vintage turntable softly out of focus. Colorful bottle wall bokeh.
Intimate city-pop jazzhop mood, film grain, shallow depth of field.

PROP:
Plain folded handwritten letter on bar counter, cream paper, no readable text or dates
on page (blank scribble lines only). No red vinyl close-up.

ACTION — exactly 10 seconds, one shot, no cuts:
0:00–0:03  Medium shot. He unfolds the letter with both hands, places it on counter,
            lowers eyes to read. Shoulders slightly hunched from fatigue.
0:03–0:06  Very slow dolly-in (5%). Eyes move slowly left-to-right across letter lines.
            One slow blink. Jaw softens — not crying, just quietly moved.
0:06–0:10  Hold medium-close. Fingers gently flatten paper corner. Faint exhale.
            Expression: weary but seen — as if letter knows him. End frame: still
            reading, same pose, eyes on paper, amber light unchanged.

CAMERA: slow dolly-in only, then static hold. No pan, no shake, 24fps film blur.
LIGHTING: warm amber interior dominant, soft rim from window rain cool tone.

AUDIO SYNC NOTE (for edit): paper rustle at 0:01, silence 0:03–0:08, optional soft
turntable hiss under — no voiceover in video generation.

NEGATIVE: readable letter text, date 2026 visible, bartender, Mr Seven visible, extra
          people, smartphone, red vinyl hero shot, talking mouth/lip sync speech,
          crying tears streaming, supernatural glow, horror, text overlay, logo,
          watermark, face morph, clothing change, standing up abruptly.
```

**Flova 設定 C：** Duration **10 s** · 16:9 · First frame = scene_04 · Final frame = 同姿勢讀信 close hold

---

## CapCut 拼接（30 秒 · 三段）

| 秒數 | 片段 | 聲音 |
|------|------|------|
| 0–10 | **Part A** | 地鐵環境音 + 輕 beep |
| 10–20 | **Part B** | 腳步 + 琥珀門光 |
| 20–30 | **Part C** | 信紙聲 + 《來自2026年的信》Intro 淡入 |
| 接點 | 每段 **Crossfade 0.3–0.5 秒** 或 hard cut | |

**Simple Text（可選）：**  
- 全程左上：`12:07 時空酒吧`  
- 20–30 秒左下：`《來自2026年的信》` 或 `EP02 · 錯過末班車的那一夜`

---

## 製作順序

1. 生成 **Part A** → 导出尾幀  
2. 尾幀作 **Part B** 首帧 + scene_03 尾帧参考  
3. 生成 **Part C**（可獨立用 scene_04 首帧，不必接 B 尾帧）  
4. CapCut 三段拼接 → 接專輯第一首或《來自2026年的信》

---

*Bar Twelve-O-Seven · EP02 10s × 3*
