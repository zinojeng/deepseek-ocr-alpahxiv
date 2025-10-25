# DeepSeek OCR with AlphaXiv

使用 DeepSeek OCR 透過 AlphaXiv API 處理 PDF 文件的 Web 應用程式。

## 功能特色

- 📄 支援 PDF 文件上傳
- 🔍 使用 DeepSeek OCR 進行高精度文字識別
- 📝 自動轉換為 Markdown 格式
- 💰 成本僅為傳統 OCR 工具的十分之一
- 🌐 簡潔易用的 Web 介面

## 快速開始

### 1. 安裝依賴

```bash
pip install -r requirements.txt
```

### 2. 設定環境變數

複製 `.env.example` 為 `.env` 並設定您的配置：

```bash
cp .env.example .env
```

### 3. 建立必要目錄

```bash
mkdir -p uploads outputs
```

### 4. 啟動應用程式

```bash
python src/app.py
```

應用程式將在 `http://localhost:5001` 啟動。

> **注意**: 預設使用端口 5001，因為 macOS 的 AirPlay Receiver 通常佔用 5000 端口。如需使用其他端口，可設定環境變數：`PORT=8000 python src/app.py`

## 使用方式

1. 開啟瀏覽器訪問 `http://localhost:5001`
2. 點擊「選擇 PDF 檔案」上傳您的 PDF
3. 點擊「開始處理」
4. 等待處理完成後，可以：
   - 在線上預覽 Markdown 結果
   - 下載 .md 檔案

## API 參考

### AlphaXiv DeepSeek OCR API

```bash
curl -X POST "https://api.alphaxiv.org/models/v1/deepseek/deepseek-ocr/inference" \
  -F "file=@report.pdf"
```

更多資訊：https://www.alphaxiv.org/models/deepseek/deepseek-ocr

## 專案結構

```
.
├── src/
│   ├── api/           # API 整合模組
│   ├── services/      # 業務邏輯服務
│   ├── models/        # 資料模型
│   ├── utils/         # 工具函數
│   └── app.py         # Flask 應用主程式
├── static/
│   ├── css/           # 樣式檔案
│   └── js/            # JavaScript 檔案
├── templates/         # HTML 模板
├── tests/            # 測試檔案
├── uploads/          # 上傳檔案目錄
├── outputs/          # 輸出檔案目錄
└── SDD.md            # 軟體設計文件
```

## 技術棧

- **後端框架**: Flask 3.0
- **OCR 服務**: DeepSeek OCR via AlphaXiv API
- **前端**: HTML5, CSS3, JavaScript
- **文件格式**: Markdown

## 授權

MIT License
