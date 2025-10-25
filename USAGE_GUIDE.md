# 使用指南

## 🚀 快速啟動

### ✅ 推薦方式：使用 run.sh

```bash
./run.sh
```

這個腳本會自動：
1. 檢查並建立虛擬環境
2. 安裝所有依賴
3. 建立必要目錄
4. 啟動應用程式在 **http://localhost:5001**

---

## 📝 端口說明

### 預設端口：5001

**為什麼是 5001 而不是 5000？**

在 macOS 上，系統的 **AirPlay Receiver** 服務預設佔用 5000 端口，因此我們改用 5001 作為預設端口。

### 使用自訂端口

如果 5001 也被佔用，您可以這樣做：

#### 選項 1：使用環境變數
```bash
source venv/bin/activate
PORT=8000 python src/app.py
```

#### 選項 2：修改 .env 檔案
```bash
echo "PORT=8000" >> .env
./run.sh
```

#### 選項 3：一次性指定
```bash
PORT=8080 ./run.sh
```

---

## 🔧 完整啟動步驟（手動）

如果您想完全了解每個步驟：

### 1. 建立虛擬環境（首次執行）
```bash
python3 -m venv venv
```

### 2. 啟用虛擬環境
```bash
source venv/bin/activate
```

您應該看到命令提示符前出現 `(venv)`：
```
(venv) user@machine:~/DeepSeek-OCR-alphaxiv$
```

### 3. 安裝依賴套件
```bash
pip install -r requirements.txt
```

### 4. 建立必要目錄
```bash
mkdir -p uploads outputs
```

### 5. 設定環境變數（可選）
```bash
cp .env.example .env
# 編輯 .env 檔案自訂設定
```

### 6. 啟動應用程式
```bash
python src/app.py
```

您應該看到：
```
2025-10-25 10:37:27,176 - api.alphaxiv_client - INFO - AlphaXiv 客戶端已初始化
2025-10-25 10:37:27,176 - services.ocr_service - INFO - OCR 服務已初始化
2025-10-25 10:37:27,176 - __main__ - INFO - 啟動 Flask 應用於 port 5001
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5001
```

---

## 🌐 使用 Web 介面

### 1. 開啟瀏覽器

訪問：**http://localhost:5001**

### 2. 上傳 PDF

- **方法 1**：點擊「選擇檔案」按鈕
- **方法 2**：直接拖放 PDF 檔案到上傳區域

### 3. 處理檔案

點擊「開始處理」按鈕，系統會：
1. 上傳 PDF 到伺服器
2. 呼叫 AlphaXiv DeepSeek OCR API
3. 將結果轉換為 Markdown
4. 顯示處理結果

### 4. 查看結果

- **預覽標籤**：渲染後的 Markdown 視圖
- **Markdown 標籤**：原始 Markdown 文字

### 5. 下載結果

點擊「下載 Markdown」按鈕，儲存 .md 檔案到本機。

---

## 📱 功能說明

### 支援的檔案格式
- **僅支援**：PDF (.pdf)
- **最大檔案大小**：16 MB

### 檔案驗證
系統會自動檢查：
- ✅ 檔案格式是否為 PDF
- ✅ 檔案大小是否在限制內
- ✅ 檔案是否可讀取

### 處理流程
```
上傳 PDF
    ↓
檔案驗證
    ↓
呼叫 AlphaXiv API
    ↓
DeepSeek OCR 處理
    ↓
轉換為 Markdown
    ↓
儲存結果
    ↓
顯示 + 下載
```

---

## 🛠 進階使用

### 批次處理（命令列）

建立一個 Python 腳本：

```python
from src.services.ocr_service import OCRService
import glob

ocr = OCRService()

# 處理資料夾中的所有 PDF
for pdf_file in glob.glob("pdfs/*.pdf"):
    print(f"處理: {pdf_file}")
    result = ocr.process_document(pdf_file)
    if result['success']:
        print(f"✅ 成功: {result['output_file']}")
    else:
        print(f"❌ 失敗: {result['error']}")
```

### API 整合

在您的專案中直接使用：

```python
from src.api.alphaxiv_client import AlphaXivClient

client = AlphaXivClient()
result = client.process_pdf("document.pdf")
print(result)
```

### 自訂 Markdown 轉換

修改 `src/utils/markdown_converter.py` 以自訂輸出格式。

---

## 🐳 使用 Docker

### 方法 1：Docker Compose（推薦）

```bash
docker-compose up -d
```

訪問：**http://localhost:5000** （Docker 使用 5000）

停止：
```bash
docker-compose down
```

### 方法 2：Docker CLI

建立映像：
```bash
docker build -t deepseek-ocr .
```

執行容器：
```bash
docker run -d \
  -p 5001:5001 \
  -v $(pwd)/uploads:/app/uploads \
  -v $(pwd)/outputs:/app/outputs \
  --name deepseek-ocr \
  deepseek-ocr
```

查看日誌：
```bash
docker logs -f deepseek-ocr
```

停止容器：
```bash
docker stop deepseek-ocr
docker rm deepseek-ocr
```

---

## 🔍 驗證安裝

### 1. 檢查健康狀態
```bash
curl http://localhost:5001/health
```

預期輸出：
```json
{
  "status": "healthy",
  "service": "DeepSeek OCR"
}
```

### 2. 測試 API 端點
```bash
curl -X POST http://localhost:5001/upload \
  -F "file=@test.pdf"
```

### 3. 檢查日誌
應用程式啟動時會顯示詳細日誌，包括：
- AlphaXiv 客戶端初始化
- OCR 服務初始化
- Flask 應用啟動資訊

---

## ⚠️ 常見問題

### Q1: 端口被佔用怎麼辦？

**錯誤訊息**：
```
Address already in use
Port 5001 is in use by another program
```

**解決方案**：
```bash
# 使用不同端口
PORT=8000 python src/app.py

# 或找出佔用的程式並停止
lsof -ti:5001 | xargs kill -9
```

### Q2: 無法連接到 AlphaXiv API

**錯誤訊息**：
```
OCR 處理失敗: Connection error
```

**解決方案**：
1. 檢查網路連線
2. 確認 API URL 正確
3. 檢查防火牆設定

### Q3: 虛擬環境無法啟用

**在 Windows 上**：
```bash
venv\Scripts\activate
```

**在 macOS/Linux 上**：
```bash
source venv/bin/activate
```

### Q4: 檔案上傳失敗

**可能原因**：
- 檔案過大（>16 MB）
- 檔案不是 PDF 格式
- uploads 目錄沒有寫入權限

**解決方案**：
```bash
# 確保目錄存在
mkdir -p uploads outputs

# 檢查權限
ls -la uploads outputs
```

---

## 📊 效能建議

### 開發環境
- **執行緒數**：1（Flask 開發伺服器）
- **適用於**：測試、開發、小量文件

### 生產環境

使用 Gunicorn：
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5001 src.app:app
```

**參數說明**：
- `-w 4`：4 個 worker 進程
- `-b 0.0.0.0:5001`：綁定到所有介面的 5001 端口
- 建議 worker 數量：`(2 × CPU 核心數) + 1`

---

## 🔐 安全建議

### 1. 環境變數
不要在 `.env` 中儲存敏感資訊並提交到 Git

### 2. 生產部署
- 使用 HTTPS
- 設定適當的 CORS 政策
- 啟用速率限制
- 使用反向代理（Nginx）

### 3. 檔案處理
- 系統會自動清理暫存檔案
- 定期清理 uploads 和 outputs 目錄

---

## 📚 更多資源

- **SDD.md** - 軟體設計文件
- **ARCHITECTURE.md** - 系統架構說明
- **TROUBLESHOOTING.md** - 疑難排解指南
- **README.md** - 專案概述

---

## 💡 提示與技巧

### 1. 快速重啟
```bash
# 停止
Ctrl+C

# 重啟
python src/app.py
```

### 2. 背景執行
```bash
nohup python src/app.py > app.log 2>&1 &
```

### 3. 查看即時日誌
```bash
tail -f app.log
```

### 4. 效能監控
```bash
# 查看記憶體使用
ps aux | grep "python src/app.py"

# 查看端口監聽
lsof -i:5001
```

---

**祝您使用愉快！** 🎉

如有問題，請參考 [TROUBLESHOOTING.md](TROUBLESHOOTING.md) 或提交 [GitHub Issue](https://github.com/zinojeng/deepseek-ocr-alpahxiv/issues)。
