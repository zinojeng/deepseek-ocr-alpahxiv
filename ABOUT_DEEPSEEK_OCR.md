# 關於 DeepSeek OCR

## 📖 簡介

DeepSeek OCR 是由 DeepSeek AI 開發的多模態文檔理解模型，專門用於高精度的文字識別和文檔解析。透過 AlphaXiv 提供的 API 服務，您可以輕鬆將 PDF 文檔轉換為結構化的 Markdown 格式。

## ✨ 主要特點

### 1. 高精度文字識別

- **多語言支援**: 支援中文、英文及多種語言的混合識別
- **複雜排版**: 能處理多欄位、表格、列表等複雜排版
- **數學公式**: 準確識別並轉換為 LaTeX 格式
- **特殊符號**: 支援希臘字母、數學符號、化學符號等

### 2. 圖像內容提取

DeepSeek OCR 對圖像的處理能力：

| 功能 | 支援程度 | 說明 |
|------|---------|------|
| 圖像中的文字 | ✅ 完整支援 | 提取圖表、流程圖中的所有文字標註 |
| 圖像標題 | ✅ 完整支援 | 識別圖像的標題和說明文字 |
| 圖像註解 | ✅ 完整支援 | 提取縮寫定義、圖例說明 |
| 圖像視覺結構 | ⚠️ 部分支援 | 可識別基本結構，但不提供詳細描述 |
| 圖像內容理解 | ❌ 不支援 | 無法描述圖像的語義內容 |

**範例**：

輸入：包含流程圖的 PDF 頁面

輸出：
```markdown
### 📊 FIGURE 1: System Architecture

**說明**: API Gateway, Auth Service, Database, Cache Layer, Message Queue

> ⚠️ 注意: 此處為圖像位置。OCR 已提取圖像中的文字標註，但無法提供圖像的視覺結構描述。
```

### 3. 表格識別

- 自動檢測表格結構
- 保留行列關係
- 轉換為 Markdown 表格格式
- 支援複雜表格（合併儲存格、多層表頭）

### 4. 文檔結構保留

- **標題層級**: 自動識別 H1-H6 標題
- **段落分隔**: 保持原始段落結構
- **列表項目**: 識別有序和無序列表
- **引用區塊**: 保留引文格式

## 🎯 使用場景

### 適合的場景

✅ **學術論文**: 提取論文內容、公式、參考文獻
✅ **技術文檔**: 轉換 API 文檔、技術手冊
✅ **報告文件**: 財務報告、研究報告、會議記錄
✅ **書籍掃描**: 將紙質書籍數位化
✅ **發票單據**: 提取結構化數據（配合後處理）

### 不適合的場景

❌ **圖像內容分析**: 需要理解圖表語義（建議使用 VLM）
❌ **手寫文字**: 主要針對印刷體優化
❌ **極低解析度**: 建議使用 300 DPI 以上的文檔
❌ **多媒體內容**: 無法處理音訊、影片

## 📊 性能指標

### 準確率

- **印刷體文字**: >99%
- **數學公式**: >95%
- **表格結構**: >90%
- **多語言混合**: >95%

### 處理速度

| 文檔類型 | 頁數 | 平均處理時間 |
|---------|------|-------------|
| 純文字 PDF | 10 頁 | 10-15 秒 |
| 圖文混排 | 10 頁 | 15-25 秒 |
| 複雜排版 | 10 頁 | 20-30 秒 |

*註: 實際速度取決於文檔複雜度和伺服器負載*

## 💰 成本效益

### AlphaXiv API 定價

根據 [AlphaXiv 官網](https://www.alphaxiv.org/models/deepseek/deepseek-ocr)：

- **API 配額**: 每小時 15,000 次請求
- **費率限制**: RateLimit-Policy: 15000;w=3600
- **成本**: 約為傳統 OCR 工具的 **1/10**

### 與其他方案比較

| 方案 | 精度 | 速度 | 成本 | 多語言 |
|------|------|------|------|--------|
| DeepSeek OCR | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ✅ |
| Tesseract | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ✅ |
| Adobe Acrobat | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ✅ |
| Google Vision | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ✅ |
| AWS Textract | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ✅ |

## 🔧 技術規格

### 支援的格式

- **輸入格式**: PDF
- **輸出格式**: Markdown, JSON
- **圖像支援**: PNG, JPEG (內嵌於 PDF)
- **最大檔案大小**: 建議 ≤ 100 MB

### API 規格

```
端點: https://api.alphaxiv.org/models/v1/deepseek/deepseek-ocr/inference
方法: POST
Content-Type: multipart/form-data
```

**請求**:
```bash
curl -X POST "https://api.alphaxiv.org/models/v1/deepseek/deepseek-ocr/inference" \
  -F "file=@document.pdf"
```

**回應格式**:
```json
{
  "data": {
    "ocr_text": "識別的文字內容...",
    "pages": ["頁面1內容", "頁面2內容"],
    "num_pages": 23,
    "num_successful": 23
  }
}
```

### 解析度建議

- **最佳**: 300 DPI
- **可接受**: 150-300 DPI
- **不建議**: < 150 DPI

## 🚀 最佳實踐

### 1. 文檔預處理

✅ **DO**:
- 確保 PDF 文字清晰可讀
- 使用高解析度掃描（≥ 300 DPI）
- 保持文檔正向（不要旋轉）
- 移除浮水印和背景噪點

❌ **DON'T**:
- 使用過度壓縮的 PDF
- 掃描時傾斜或扭曲
- 包含過多手寫註解

### 2. 結果後處理

處理 OCR 結果時建議：

```python
# 1. 清理多餘空白
text = re.sub(r'\n{3,}', '\n\n', ocr_text)

# 2. 修正常見錯誤
text = text.replace('０', '0')  # 全形轉半形

# 3. 提取結構化數據
figures = re.findall(r'FIGURE \d+[:\-](.+)', text)
```

### 3. 錯誤處理

```python
try:
    result = ocr_service.process_document(pdf_path)
    if result['success']:
        markdown = result['markdown_content']
    else:
        # 處理失敗情況
        logger.error(f"OCR 失敗: {result['error']}")
except Exception as e:
    # 網路錯誤、超時等
    logger.exception("處理文檔時發生錯誤")
```

## 📚 延伸閱讀

- **AlphaXiv 官網**: https://www.alphaxiv.org/models/deepseek/deepseek-ocr
- **DeepSeek GitHub**: https://github.com/deepseek-ai/DeepSeek-OCR
- **技術論文**: [待補充]
- **API 文檔**: https://www.alphaxiv.org/docs

## ❓ 常見問題

### Q1: 為什麼圖像只顯示標題和說明？

**A**: DeepSeek OCR 是文字識別工具，只能提取圖像中的**文字**，無法理解圖像的**視覺內容**。如需圖像內容描述，請使用 Vision Language Model (如 GPT-4V)。

### Q2: 處理大型 PDF 需要多長時間？

**A**: 一般每頁需要 1-3 秒，100 頁的 PDF 約需 2-5 分鐘。建議分批處理超大文檔。

### Q3: 支援哪些語言？

**A**: 支援中文（繁/簡）、英文、日文、韓文等主流語言，以及多語言混合文檔。

### Q4: 識別率不理想怎麼辦？

**A**:
1. 檢查原始 PDF 解析度
2. 確認文字清晰度
3. 嘗試重新掃描（如果是掃描件）
4. 使用 PDF 編輯工具增強對比度

### Q5: API 有使用限制嗎？

**A**: 根據 AlphaXiv，每小時限制 15,000 次請求。超過限制可能需要等待或升級方案。

### Q6: 可以處理加密的 PDF 嗎？

**A**: 不支援。請先解除 PDF 加密再上傳。

## 🤝 貢獻

如果您發現 OCR 結果的問題或有改進建議，歡迎：

1. 提交 Issue: https://github.com/zinojeng/deepseek-ocr-alpahxiv/issues
2. 分享使用案例
3. 提供問題 PDF 樣本（注意隱私）

## 📄 授權

DeepSeek OCR 模型由 DeepSeek AI 開發，通過 AlphaXiv 提供 API 服務。
本專案使用 MIT License。
