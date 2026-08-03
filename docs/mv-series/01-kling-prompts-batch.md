# 《沒有狼的村莊》Kling 批次包（可直接貼上）

## 全域設定
- 模式：Image-to-Video（強烈建議）
- 畫幅：9:16
- 時長：每鏡 4–5 秒
- Motion：0.3–0.5（故事書感）
- CFG／創意度：中低（保角色）

## Negative（每鏡共用）
```text
photorealistic, live action, modern clothing, smartphones, cars, text artifacts, extra fingers, deformed face, morphing face, horror gore, explicit violence, blood, jump scare, 3D CGI plastic skin, watermark, logo, burned-in subtitles
```

## Style Anchor（每鏡結尾追加｜暗黑哥特 2D 卡通）
```text
dark gothic 2D cartoon illustration, adult fairytale animation style, thick ink outlines, flat cel shading with large black shadow shapes, limited desaturated palette, cold ash blue and charcoal, grim storybook cartoon, paper grain, NOT children's watercolor, NOT Disney, NOT cute anime, NOT photorealistic
```

---

## 定裝圖（先做）

### REF_OLD_MAN
```text
Character sheet, front and three-quarter view, elderly storyteller, deep wrinkles, kind knowing eyes, long silver beard, dark wool cloak with fur collar, thick yellowed fairytale book, fireplace amber light, storybook animation
```

### REF_ELIA
```text
Character sheet, 12-year-old girl Elia, freckles, large observant eyes, handmade winter coat, red wool scarf, brown hair loose braid, sketchbook and charcoal pencil, innocent brave expression, consistent facial features, storybook animation
```

### REF_VILLAGE
```text
Wide matte painting of White Hollow, tiny snowy wooden houses surrounded by dense dark forest, chimney smoke, fearful quiet atmosphere, Nordic winter folklore, storybook animation
```

### REF_FOREST
```text
Magical winter forest, bioluminescent flowers, gentle deer and foxes, moonlight on snow, peaceful sacred mood, no wolves, painterly fantasy storybook
```

### REF_STELE
```text
Ancient mossy stone stele in forest clearing, carved words partially hidden by moss, moonlight rim light, mysterious revelation, storybook animation
```

### REF_SKETCHBOOK
```text
Open sketchbook on snow, hand-drawn villagers casting wolf-shaped shadows, poetic tragic symbolism, storybook animation
```

---

## 分鏡 Prompt（16 鏡完整版）

### S01_BOOK
```text
Close-up open yellowed fairytale book, fireplace light flickering on pages, snow outside frosted window, slow push-in, quiet magical mood
```

### S02_NARRATOR
```text
Elderly storyteller with silver beard looks to camera, gentle knowing smile, thick book in hands, fireplace warm light, cold blue window behind, soft eye contact, slow push-in
```

### S03_VILLAGE
```text
Wide establishing shot snowy village White Hollow surrounded by dark forest, chimney smoke, slow lateral drift, fearful quiet atmosphere
```

### S04_WARNING
```text
Dim wooden cottage, parents whispering to child near candle, frost on window, worried faces, slow push-in on child's eyes, tense but not gory
```

### S05_NO_WOLF
```text
Empty winter forest path, untouched snow, no footprints, wind moving pine branches, soft fog, slow forward move, eerie quiet absence
```

### S06_MISSING
```text
Snowy village square dusk, abandoned small shoe near ajar wooden door, villagers whispering in silhouette, high-angle slow descend, symbolic
```

### S07_ELIA
```text
Elia freckles red scarf sketching at frosty window, hopeful gaze toward forest, charcoal tree drawings, tender close-up, consistent face, soft daylight
```

### S08_ENTER_FOREST
```text
Elia walking deeper into magical winter forest, deer and fox calm, glowing flowers on snow, side-tracking follow camera, wonder and innocence, no wolves
```

### S09_STELE
```text
Elia kneeling at ancient mossy stele, wiping moss, moonlight reveal, awe and shock, slow push-in wide to inscription area, leave text blank for post captions
```

### S10_LAUGHTER
```text
Village hall, Elia speaking urgently, villagers uneasy laughter spreading face by face, fear as mockery, slow pan across crowd, emotional tension
```

### S11_SCAPEGOAT
```text
Symbolic montage: shadows whispering, fingers pointing at Elia, distant square crowd around small figure, stones only in far background, non-graphic tragedy, desaturated cold colors
```

### S12_QUESTION
```text
Close-up Elia tears looking upward, snow on red scarf, heartbreaking stillness, slow push-in to eyes, emotional climax
```

### S13_ESCAPE
```text
Night forest, Elia walking into moonlight, deer calm, birds still, silver-blue light, sanctuary after cruelty, slow dolly out
```

### S14_BOOK_SHADOWS
```text
Open sketchbook on snow, portraits of villagers with wolf-shaped shadows, poetic horror symbolism no gore, slow tilt down then gentle push-in
```

### S15_RUINS
```text
Abandoned snowy village years later, empty moonlit streets, broken shutters, no beasts, haunting wind, slow forward tracking, melancholic
```

### S16_MORAL
```text
Elderly storyteller closing fairytale book, candle flame extinguishing, final wise sorrowful gaze to camera, warm light dying to darkness, fade to black
```

---

## 8 鏡極簡版（最省錢）
使用：S02 → S03 → S07 → S08 → S09 → S11 → S14 → S16  
總長目標：约 45–55 秒（每鏡可拉到 5–6 秒）＋旁白補敘事。

---

## 旁白（繁中・Shorts 精簡版）

```text
每個童話都說：要提防森林裡的狼。
但如果……根本沒有狼呢？

White Hollow 的孩子，都聽著狼的故事長大。
沒有人見過狼。可每年，總有人消失。

女孩 Elia 走進森林，只看見鹿、狐狸，與發光的花。
石碑寫著：狼早已離開。留下來的，只有人。

她把真相告訴村莊。
村民卻笑了——因為害怕。
他們說：她就是狼。

她問：「如果沒有狼，你們害怕的是什麼？」
沒有人回答。

後來，人們只找到她的畫冊。
每一個村民的影子，都是狼。

很多年後，荒村里仍有人喊：狼來了。
街上卻只有月光。

狼，從來沒有住在森林裡。
牠，一直住在人心裡。
```

## 旁白（English・optional）

```text
Every fairytale warns us of wolves in the woods.
But what if there were never any wolves?

In White Hollow, children grew up on that story.
No one ever saw a wolf. Yet every year, someone vanished.

Elia walked into the forest and found only deer, foxes, and glowing flowers.
A stone said: The wolves left long ago. Only humans remained.

She told the village the truth.
They laughed — not from joy, but from fear.
Then they named her the wolf.

She asked, “If there are no wolves… what are you afraid of?”
No one answered.

Later they found only her sketchbook.
Every villager cast a wolf for a shadow.

Years after, empty streets still cried, “The wolf is here!”
But there was only moonlight.

The wolf never lived in the forest.
It lived in the human heart.
```
