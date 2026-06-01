# Axo 需求規格（繁體中文）

**品牌：** Dozeify · **吉祥物：** Axo（一隻慢性疲勞、自由靈魂的墨西哥鈍口螈）  
**哲學：** Regenerative Rest（再生式休息）— 語氣死板、溫馨、略帶疲憊，但療癒且易共鳴

---

## 一、專案需求總覽

| 項目 | 需求 |
|------|------|
| 社群 | 7 日 Instagram 上線計畫 |
| 印刷 | Printfly 服飾上架（POD） |
| 工作流程 | AI 負責大量發想與草稿；人類設計師負責修線、一致性與印刷檔 |
| 溝通語言 | 對外內容可依市場調整；**本文件為繁體中文規格** |
| 主檔格式 | 向量 SVG / Illustrator；印刷用透明底 PNG **300 DPI** |

---

## 二、繪畫風格硬性規定（目前已定）

以下為**不可擅自更改**的規格，除非品牌方書面確認。

| 項目 | 規定 |
|------|------|
| 維度 | 僅限 **平面 2D** 線稿塗色，禁止陰影、漸層、3D 立體光 |
| 輪廓線 | 墨色 `#1A1A1A`，線寬 **7px**（以 400×520 畫布為基準），圓角端點 |
| 身體填色 | 粉彩粉 `#FAD4D8`（Pastel Pink） |
| 眼睛 | **恰好兩顆**純黑圓點 `• •`，禁止大眼白、睫毛、表情符號眼 |
| 嘴巴 | 極小 **`w`**（預設）或 **`_`**（更睏）；禁止牙齒、張口橢圓 |
| 姿態 | 像人一樣 **雙腳直立**；外鰓為簡單弧線，不寫實 |
| 背景（IG） | 純白 |
| 背景（印刷） | **完全透明**，無白邊（fringe） |
| 參考調性 | 簡約 kawaii 網路漫畫（如 Ketnipz 類型的可愛、線條乾淨） |

**主提示詞（Midjourney，僅改 [動作/道具]）：**

```
A minimalist 2D line-art doodle of a cute, chubby axolotl character standing upright on two legs like a human. Solid black dot eyes, tiny w mouth, flat pale pastel pink coloring, pure white background. [Action/Prop]
```

---

## 三、繪畫風格待確認事項（需品牌方回覆）

請回答 [`docs/axo-風格問卷-zh-TW.md`](./axo-風格問卷-zh-TW.md) 中的問題。回覆後將更新至 [`docs/axo-character-sheet.md`](./axo-character-sheet.md) 並調整 SVG 資產。

---

## 四、人類設計師需求（AI Finisher）

### 職位

**2D 插畫師 /「AI 修線師」** — 不需整包代理商，一位強 freelancer 即可。

### 作品集必備

- 簡約、kawaii 四格或單格漫畫經驗  
- 手寫字或休閒手寫體排版  
- Adobe Illustrator（描線向量化）、Procreate、Photoshop（去背）

### 核心職責

1. **AI 清稿**：修掉多趾、歪線、多餘陰影，確保 100% 平面向量。  
2. **點眼執行**：強制 `• •` 與 `w`/`_` 嘴型。  
3. **對白與排版**：腳本對白融入漫畫，**手機可讀**。  
4. **Printfly 優化**：透明底、300 DPI、粉彩粉在 Bella+Canvas / Comfort Colors 上試色、無白邊。

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
| `assets/axo/axo-canonical.svg` | 標準站姿、頭像、POD 主檔 |
| `assets/axo/axo-wave.svg` | 打招呼、上線貼文 |
| `assets/axo/axo-sleepy.svg` | 休息、療癒主題 |

英文技術細節：[`docs/axo-character-sheet.md`](./axo-character-sheet.md)

---

## 七、修訂紀錄

| 日期 | 說明 |
|------|------|
| 2026-06-01 | 初版需求規格（繁中）；風格問卷待填 |
