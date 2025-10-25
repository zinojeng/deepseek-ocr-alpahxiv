# 段落合併功能說明

## 功能概述

此功能解決了 OCR 處理過程中，圖片說明會中斷段落文字的問題。當圖片說明插入在段落中間時，系統會自動識別並將被中斷的段落重新合併，然後將圖片說明移到完整段落的後面。

## 問題背景

在處理包含圖片的 PDF 文件時，OCR 可能會產生以下格式的輸出：

```
這段本文上段...and the<center>FIGURE 2 ...</center>diverse underlying...
```

這會導致原本連續的段落被圖片說明中斷，影響閱讀體驗。

## 解決方案

### 自動段落重組

系統會分析圖片說明前後的文字，根據以下規則判斷是否需要合併：

#### 合併條件

段落會在以下情況下被合併：

1. **前一段沒有以句號結尾**
   - 例如：`"HF and the"` → 沒有句號，應該繼續

2. **後一段以小寫字母開頭**
   - 例如：`"diverse underlying..."` → 以小寫開頭，表示是同一句的延續

3. **後一段以連接詞開頭**
   - 支援的連接詞包括：
     - and, or, but
     - however, moreover, furthermore
     - therefore, thus, hence, consequently
     - prompting, resulting, leading, causing
     - which, that, who

#### 不合併的情況

當遇到以下情況時，段落不會合併：

1. **前一段以句號結尾，且後一段以大寫字母開頭**
   - 例如：`"Sentence ends."` + `"New sentence starts."` → 保持分開

2. **前後文字為空**
   - 如果圖片說明前後沒有文字，則不進行合併

## 處理流程

```
原始文字:
"Text before and the<center>FIGURE 1 ...</center>prompting the discussion."

↓ 步驟 1: 識別圖片說明
前文: "Text before and the"
圖片: "<center>FIGURE 1 ...</center>"
後文: "prompting the discussion."

↓ 步驟 2: 分析合併條件
- 前文沒有句號結尾 ✓
- 後文以連接詞 "prompting" 開頭 ✓
→ 應該合併

↓ 步驟 3: 重組文字
"Text before and the prompting the discussion.<center>FIGURE 1 ...</center>"

↓ 步驟 4: 轉換為 Markdown
"Text before and the prompting the discussion.

---

### 📊 FIGURE 1 ...

..."
```

## 使用範例

### 範例 1：基本合併

**輸入：**
```
Its pathophysiology is likely modulated by the haemodynamics of HF and the<center>FIGURE 2 Pathophysiology of albuminuria under heart failure. ...</center>diverse underlying comorbidities present in the patient, prompting the consideration of albuminuria as a marker for cardiorenal interaction under HF.
```

**輸出：**
```
Its pathophysiology is likely modulated by the haemodynamics of HF and the diverse underlying comorbidities present in the patient, prompting the consideration of albuminuria as a marker for cardiorenal interaction under HF.

---

### 📊 FIGURE 2 Pathophysiology of albuminuria under heart failure

**說明**: ...
```

### 範例 2：不合併（獨立句子）

**輸入：**
```
The first sentence ends here.<center>FIGURE 1 Test.</center>A completely new sentence starts.
```

**輸出：**
```
The first sentence ends here.

---

### 📊 FIGURE 1 Test

...

A completely new sentence starts.
```

## 技術實現

### 核心函數

1. **`_reorganize_paragraphs_with_figures(text: str) -> str`**
   - 主要的重組函數
   - 使用正則表達式分割文字和圖片說明
   - 迭代處理每個部分並判斷是否合併

2. **`_should_merge_paragraphs(prev_text: str, next_text: str) -> bool`**
   - 判斷函數
   - 分析前後文字的標點和首字母
   - 檢查連接詞

### 相關文件

- 主要實現：[src/utils/markdown_converter.py](src/utils/markdown_converter.py)
- 測試文件：
  - [test_paragraph_merge.py](test_paragraph_merge.py) - 基本功能測試
  - [test_simple_merge.py](test_simple_merge.py) - 簡單案例測試

## 測試結果

所有測試案例均已通過：

- ✅ 基本段落合併
- ✅ 連接詞識別
- ✅ 句號判斷
- ✅ 小寫字母開頭處理
- ✅ 獨立句子保持分開

## 兼容性

此功能：
- 不影響現有的 OCR 處理流程
- 自動應用於所有新的 OCR 處理
- 符合 PEP 8 編碼規範
- 已通過所有測試案例

## 注意事項

1. 此功能基於英文文法規則設計，對中文文本可能需要額外調整
2. 連接詞列表可以根據需要擴展
3. 如果遇到特殊格式，可能需要手動調整

## 作者

Claude (Anthropic)

## 版本歷史

- v1.0.0 (2025-10-26) - 初始實現
  - 實現基本段落合併功能
  - 添加連接詞識別
  - 完成測試案例
