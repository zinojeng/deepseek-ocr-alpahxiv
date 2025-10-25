# 疑難排解指南

## 常見問題與解決方案

### 1. ImportError: attempted relative import beyond top-level package

**問題描述**:
```
ImportError: attempted relative import beyond top-level package
```

**原因**: Python 模組導入路徑問題

**解決方案**: 已修復！確保使用最新版本的程式碼。

**手動修復**（如果需要）:
- 確保在 `src/app.py` 中有 `sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))`
- 確保在 `src/services/ocr_service.py` 中使用絕對導入而非相對導入

---

### 2. ModuleNotFoundError: No module named 'flask'

**問題描述**:
```
ModuleNotFoundError: No module named 'flask'
```

**原因**: 依賴套件未安裝或未在虛擬環境中執行

**解決方案**:

#### 選項 1: 使用 run.sh 腳本（推薦）
```bash
./run.sh
```
腳本會自動處理虛擬環境和依賴安裝。

#### 選項 2: 手動啟動虛擬環境
```bash
# 啟動虛擬環境
source venv/bin/activate

# 安裝依賴
pip install -r requirements.txt

# 執行應用程式
python src/app.py
```

---

### 3. Address already in use / Port is in use

**問題描述**:
```
Address already in use
Port 5000 is in use by another program
```

**原因**: 端口 5000 已被其他程式佔用

**解決方案**:

#### 選項 1: 使用不同的端口
```bash
# 在虛擬環境中
source venv/bin/activate
PORT=5001 python src/app.py
```

#### 選項 2: 修改 .env 檔案
```bash
echo "PORT=5001" >> .env
```

#### 選項 3: 找出並停止佔用端口的程式
```bash
# macOS/Linux
lsof -ti:5000 | xargs kill -9

# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

---

### 4. 虛擬環境警告

**問題描述**:
```
WARNING: Ignoring invalid distribution -flask
```

**原因**: 虛擬環境套件安裝問題（通常不影響運行）

**解決方案**（如果影響執行）:
```bash
# 刪除虛擬環境
rm -rf venv

# 重新建立
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

### 5. 檔案上傳失敗

**問題描述**: 上傳 PDF 後出現錯誤

**可能原因和解決方案**:

#### 原因 1: 檔案過大
- **限制**: 16 MB
- **解決**: 壓縮 PDF 或分割檔案

#### 原因 2: 檔案格式不正確
- **限制**: 僅支援 .pdf 格式
- **解決**: 確認檔案副檔名為 .pdf

#### 原因 3: uploads 目錄不存在
```bash
mkdir -p uploads outputs
```

---

### 6. API 請求失敗

**問題描述**: OCR 處理時出現 API 錯誤

**可能原因和解決方案**:

#### 原因 1: 網路連線問題
```bash
# 測試 API 連線
curl https://api.alphaxiv.org/models/v1/deepseek/deepseek-ocr/inference
```

#### 原因 2: API 超時
- **解決**: 等待後重試，或檢查 PDF 檔案大小

#### 原因 3: API 配置錯誤
檢查 `.env` 檔案中的 `ALPHAXIV_API_URL` 設定

---

### 7. 靜態檔案載入失敗

**問題描述**: CSS/JS 檔案無法載入

**解決方案**:

#### 確認目錄結構
```bash
ls -la static/css/
ls -la static/js/
ls -la templates/
```

#### 確認 Flask 設定
在 `src/app.py` 中確認:
```python
app = Flask(__name__,
            template_folder='../templates',
            static_folder='../static')
```

---

### 8. 無法存取應用程式

**問題描述**: 瀏覽器無法開啟 http://localhost:5000

**解決方案**:

#### 檢查應用程式是否正在執行
```bash
# 檢查進程
ps aux | grep "python src/app.py"

# 檢查端口
lsof -i:5000
```

#### 檢查防火牆設定
確保本機防火牆允許 5000 端口

#### 嘗試使用 127.0.0.1
```
http://127.0.0.1:5000
```

---

## 啟動檢查清單

在啟動應用程式前，請確認:

- [ ] Python 3.8+ 已安裝
- [ ] 虛擬環境已建立並啟用
- [ ] 依賴套件已安裝 (`pip list | grep flask`)
- [ ] uploads 和 outputs 目錄存在
- [ ] 端口 5000 未被佔用（或使用其他端口）
- [ ] .env 檔案已建立（可選）

---

## 完整的啟動步驟

### 方法 1: 使用啟動腳本（最簡單）

```bash
chmod +x run.sh
./run.sh
```

### 方法 2: 手動啟動

```bash
# 1. 建立虛擬環境（首次執行）
python3 -m venv venv

# 2. 啟用虛擬環境
source venv/bin/activate

# 3. 安裝依賴
pip install -r requirements.txt

# 4. 建立必要目錄
mkdir -p uploads outputs

# 5. 複製環境變數檔案（可選）
cp .env.example .env

# 6. 啟動應用程式
python src/app.py
```

### 方法 3: 使用 Docker

```bash
# 使用 Docker Compose
docker-compose up -d

# 或使用 Docker
docker build -t deepseek-ocr .
docker run -p 5000:5000 deepseek-ocr
```

---

## 驗證安裝

### 1. 檢查應用程式狀態
```bash
curl http://localhost:5000/health
```

**預期輸出**:
```json
{
  "status": "healthy",
  "service": "DeepSeek OCR"
}
```

### 2. 檢查日誌
啟動應用程式時應該看到:
```
2025-10-25 10:32:36,801 - api.alphaxiv_client - INFO - AlphaXiv 客戶端已初始化
2025-10-25 10:32:36,801 - services.ocr_service - INFO - OCR 服務已初始化
2025-10-25 10:32:36,803 - __main__ - INFO - 啟動 Flask 應用於 port 5000
 * Running on http://127.0.0.1:5000
```

### 3. 測試前端
開啟瀏覽器訪問 `http://localhost:5000`，應該看到上傳介面。

---

## 除錯模式

### 啟用詳細日誌
修改 `src/app.py`:
```python
logging.basicConfig(
    level=logging.DEBUG,  # 改為 DEBUG
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### 查看完整錯誤堆疊
```bash
python src/app.py 2>&1 | tee app.log
```

---

## 效能優化

### 1. 使用 Gunicorn（生產環境）
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 src.app:app
```

### 2. 增加檔案大小限制
修改 `.env`:
```
MAX_FILE_SIZE=33554432  # 32MB
```

### 3. 調整超時設定
修改 `src/api/alphaxiv_client.py`:
```python
response = requests.post(
    self.api_url,
    files=files,
    timeout=600  # 10 分鐘
)
```

---

## 取得協助

如果以上解決方案都無法解決您的問題:

1. 查看 [GitHub Issues](https://github.com/zinojeng/deepseek-ocr-alpahxiv/issues)
2. 提交新的 Issue，包含:
   - 錯誤訊息完整內容
   - Python 版本 (`python --version`)
   - 作業系統版本
   - 執行的完整命令

---

## 系統需求

- **Python**: 3.8 或更高版本
- **RAM**: 最少 2GB，建議 4GB
- **磁碟空間**: 至少 500MB
- **網路**: 需要網際網路連線以存取 AlphaXiv API

---

## 已知限制

1. **檔案大小**: 最大 16 MB
2. **檔案格式**: 僅支援 PDF
3. **並發處理**: 開發伺服器為單執行緒
4. **API 限制**: 依 AlphaXiv 服務條款

---

**最後更新**: 2025-10-25
