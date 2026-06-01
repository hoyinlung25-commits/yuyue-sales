# Axo 需求規格（繁體中文）

**品牌：** Dozeify · **吉祥物：** Axo（一隻慢性疲勞、自由靈魂的墨西哥鈍口螈）  
**哲學：** Regenerative Rest（再生式休息）— 語氣死板、溫馨、略帶疲憊，但療癒且易共鳴

---

## 一、專案需求總覽

| 項目 | 需求 | 階段 |
|------|------|------|
| **社群（優先）** | 開 IG、7 日發文、互動漲粉 | **Phase 1 — 現在** |
| 印刷 | Printfly 服飾上架 | **Phase 2 — 暫停 ⏸** |
| 工作流程 | AI 發想草稿；設計師修線 + **大字手寫排版** | Phase 1 |
| 溝通語言 | 繁體中文規格為主 | — |
| 主檔格式 | 向量 SVG；IG 匯出 **1080×1350（4:5）白底** | Phase 1 |

**IG 執行手冊：** [`ig-launch-zh-TW.md`](./ig-launch-zh-TW.md) · **路線圖：** [`roadmap-zh-TW.md`](./roadmap-zh-TW.md)

---

## 二、繪畫風格硬性規定（目前已定）

以下為**不可擅自更改**的規格，除非品牌方書面確認。

| 項目 | 規定 |
|------|------|
| 維度 | 僅限 **平面 2D** 線稿塗色，禁止陰影、漸層、3D 立體光 |
| 輪廓線 | 墨色 `#1A1A1A`，線寬 **5px**（以 400×520 畫布為基準），圓角端點 |
| 身體填色 | 薰衣草粉 `#E4D4EA`（Lavender Pink） |
| 眼睛 | **恰好兩顆**純黑圓點 `• •`（**r=4.5**，更小更呆），禁止大眼白、睫毛、表情符號眼 |
| 腮紅 | **禁止** |
| 嘴巴 | 極小 **`w`**（預設）或 **`_`**（更睏）；禁止牙齒、張口橢圓 |
| 姿態 | 像人一樣 **雙腳直立**；外鰓為簡單弧線，不寫實 |
| 背景（IG） | 純白 |
| 背景（印刷） | Phase 2 才需：透明底、無白邊 |
| 參考調性 | 簡約 kawaii 網路漫畫（如 Ketnipz 類型的可愛、線條乾淨） |

**主提示詞（Midjourney，僅改 [動作/道具]）：**

```
A minimalist 2D line-art doodle of a cute, chubby axolotl character standing upright on two legs like a human. Solid black dot eyes, tiny w mouth, flat pale pastel pink coloring, pure white background. [Action/Prop]
```

---

## 三、繪畫風格（已鎖定 v2）

品牌方已於 2026-06-01 確認。完整紀錄：[`axo-style-locked-zh-TW.md`](./axo-style-locked-zh-TW.md)

問卷存檔：[`axo-風格問卷-zh-TW.md`](./axo-風格問卷-zh-TW.md)

---

## 四、人類設計師需求（AI Finisher）

### 職位

**2D 插畫師 /「AI 修線師」** — 不需整包代理商，一位強 freelancer 即可。

### 作品集必備

- 簡約、kawaii 四格或單格漫畫經驗  
- 手寫字或休閒手寫體排版  
- Adobe Illustrator（描線向量化）、Procreate、Photoshop（去背）

### 核心職責（Phase 1）

1. **AI 清稿**：修掉多趾、歪線、多餘陰影，確保 100% 平面向量。  
2. **點眼執行**：強制 `• •` 與 `w`/`_` 嘴型。  
3. **對白與排版**：毛筆手寫感、**大字**、4:5 構圖，手機可讀。  

### Phase 2 才需要

4. **Printfly 優化**（目前已暫停）

---

## 五、AI 虛擬美術指導（Brand Alchemist）

複製貼上提示詞見：[`docs/personas/brand-alchemist.md`](./personas/brand-alchemist.md)

**核心指令：**

1. 所有出圖提示詞必須包含上述 **Master Base Prompt**，僅修改 `[Action/Prop]`。  
2. 所有點子、文案、漫畫情境須通過 **Regenerative Rest** 語氣檢查。

---

## 六、現有資產清單

| 檔案 | 用途 |
|------|------|
| `assets/axo/axo-canonical.svg` | 標準站姿 v2 |
| `assets/axo/axo-doing-nothing.svg` | **Day 1 首發**（全身小圖 + 大字） |
| `assets/axo/axo-with-mug.svg` | 拿杯子（簡單手指） |
| `assets/axo/axo-wave.svg` | 打招呼 |
| `assets/axo/axo-sleepy.svg` | 休息、療癒主題 |

英文技術細節：[`docs/axo-character-sheet.md`](./axo-character-sheet.md)

---

## 七、修訂紀錄

| 日期 | 說明 |
|------|------|
| 2026-06-01 | 初版需求規格（繁中）；風格問卷待填 |
