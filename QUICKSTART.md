# 快速啟動指南

## 方法一：使用啟動腳本（推薦）

最簡單的方式是使用提供的啟動腳本：

```bash
./run.sh
```

腳本會自動：
- 建立虛擬環境
- 安裝依賴套件
- 建立必要目錄
- 啟動 Flask 應用程式

## 方法二：手動啟動

### 1. 安裝依賴

```bash
pip install -r requirements.txt
```

### 2. 建立必要目錄

```bash
mkdir -p uploads outputs
```

### 3. 設定環境變數（可選）

```bash
cp .env.example .env
# 編輯 .env 檔案進行自訂設定
```

### 4. 啟動應用程式

```bash
python src/app.py
```

## 方法三：使用 Docker

### 使用 Docker Compose（推薦）

```bash
docker-compose up -d
```

### 使用 Docker

```bash
# 建立映像
docker build -t deepseek-ocr .

# 執行容器
docker run -p 5000:5000 -v $(pwd)/uploads:/app/uploads -v $(pwd)/outputs:/app/outputs deepseek-ocr
```

## 使用應用程式

1. 開啟瀏覽器訪問 `http://localhost:5000`
2. 點擊「選擇檔案」上傳 PDF
3. 點擊「開始處理」
4. 等待處理完成
5. 預覽或下載 Markdown 結果

## 執行測試

```bash
python -m pytest tests/
```

或

```bash
python -m unittest discover tests
```

## 專案結構

```
DeepSeek-OCR-alphaxiv/
├── src/                    # 原始碼
│   ├── api/               # AlphaXiv API 客戶端
│   ├── services/          # 業務邏輯服務
│   ├── utils/             # 工具函數
│   └── app.py             # Flask 主應用
├── static/                # 靜態資源
│   ├── css/              # 樣式表
│   └── js/               # JavaScript
├── templates/             # HTML 模板
├── tests/                 # 測試檔案
├── uploads/               # 上傳目錄
├── outputs/               # 輸出目錄
├── requirements.txt       # Python 依賴
├── .env.example          # 環境變數範例
├── Dockerfile            # Docker 映像
├── docker-compose.yml    # Docker Compose 設定
├── run.sh                # 啟動腳本
├── README.md             # 專案說明
└── SDD.md                # 軟體設計文件
```

## API 參考

### 上傳和處理 PDF

**端點**: `POST /upload`

**請求**: `multipart/form-data` 包含 PDF 檔案

**回應**:
```json
{
  "success": true,
  "markdown_content": "...",
  "output_file": "filename.md",
  "metadata": {
    "input_file": "input.pdf",
    "output_file": "output.md",
    "processed_at": "2025-10-25T10:00:00",
    "content_length": 1234
  }
}
```

### 下載 Markdown 檔案

**端點**: `GET /download/<filename>`

### 健康檢查

**端點**: `GET /health`

## 疑難排解

### 連接埠已被佔用

如果 5000 連接埠已被使用，可以修改 `.env` 檔案中的 `PORT` 設定：

```bash
PORT=8080
```

### 模組找不到錯誤

確保您在正確的目錄中，並且已安裝所有依賴：

```bash
pip install -r requirements.txt
```

### API 請求失敗

檢查您的網路連線，確保可以訪問 AlphaXiv API：

```bash
curl https://api.alphaxiv.org/models/v1/deepseek/deepseek-ocr/inference
```

## 下一步

- 閱讀 [README.md](README.md) 了解更多功能
- 查看 [SDD.md](SDD.md) 了解系統設計
- 瀏覽原始碼了解實作細節
