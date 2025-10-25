# 部署指南

## Zeabur 部署

### 快速部署

1. **前往 Zeabur**
   - 訪問 https://zeabur.com
   - 使用 GitHub 帳號登入

2. **創建新專案**
   - 點擊 "Create Project"
   - 選擇 "Deploy from GitHub"
   - 選擇此 repository: `deepseek-ocr-alpahxiv`

3. **配置環境變數**（可選）

   在 Zeabur 專案設置中添加以下環境變數：

   ```env
   # Flask 配置
   FLASK_ENV=production
   SECRET_KEY=your-production-secret-key-here

   # 文件大小限制（bytes）
   MAX_FILE_SIZE=16777216

   # AlphaXiv API（如需自訂）
   ALPHAXIV_API_URL=https://api.alphaxiv.org/models/v1/deepseek/deepseek-ocr/inference
   ```

4. **部署**
   - Zeabur 會自動檢測 Dockerfile
   - 自動構建和部署應用程式
   - 完成後會獲得一個公開 URL

### 環境變數說明

| 變數名 | 必填 | 預設值 | 說明 |
|--------|------|--------|------|
| `PORT` | ❌ | 8080 | 應用程式端口（Zeabur 自動設置） |
| `FLASK_ENV` | ❌ | production | Flask 環境模式 |
| `SECRET_KEY` | ⚠️ | dev-secret-key | 用於 session 加密（生產環境建議設置） |
| `MAX_FILE_SIZE` | ❌ | 16777216 | 最大上傳檔案大小（16MB） |
| `ALPHAXIV_API_URL` | ❌ | AlphaXiv OCR 端點 | DeepSeek OCR API URL |

### 生成安全的 SECRET_KEY

```python
import secrets
print(secrets.token_urlsafe(32))
```

或使用命令行：

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 注意事項

1. **文件儲存**
   - Zeabur 的檔案系統是暫時性的
   - 上傳的檔案會在容器重啟後消失
   - 輸出的 Markdown 檔案建議即時下載

2. **記憶體限制**
   - 注意 PDF 檔案大小（預設上限 16MB）
   - 大型 PDF 可能需要較長處理時間

3. **API 限制**
   - AlphaXiv API 有使用限制（每小時 15000 次）
   - 請參考：https://www.alphaxiv.org/models/deepseek/deepseek-ocr

## 其他部署平台

### Docker 部署

```bash
# 構建映像
docker build -t deepseek-ocr .

# 運行容器
docker run -p 8080:8080 \
  -e FLASK_ENV=production \
  -e SECRET_KEY=your-secret-key \
  deepseek-ocr
```

### Docker Compose 部署

```bash
docker-compose up -d
```

### 手動部署

```bash
# 安裝依賴
pip install -r requirements.txt

# 設置環境變數
export FLASK_ENV=production
export PORT=8080
export SECRET_KEY=your-secret-key

# 啟動應用
python run.py
```

## 驗證部署

部署完成後，訪問以下端點驗證：

- **健康檢查**: `https://your-domain.zeabur.app/health`
- **首頁**: `https://your-domain.zeabur.app/`

應該會看到：
```json
{
  "status": "healthy",
  "service": "DeepSeek OCR"
}
```

## 故障排除

### 應用無法啟動

1. 檢查環境變數是否正確設置
2. 查看 Zeabur 的構建日誌
3. 確認 Python 版本兼容（需要 Python 3.10+）

### 文件上傳失敗

1. 檢查檔案大小是否超過限制
2. 確認檔案格式為 PDF
3. 查看應用程式日誌

### API 請求失敗

1. 檢查 AlphaXiv API 狀態
2. 確認網路連接正常
3. 檢查 API URL 是否正確

## 監控和日誌

在 Zeabur 控制台可以查看：

- **即時日誌**: 應用程式運行日誌
- **指標**: CPU、記憶體使用情況
- **請求**: HTTP 請求統計

## 更新部署

當您推送更新到 GitHub 時：

1. Zeabur 會自動檢測更新
2. 觸發重新構建
3. 自動部署新版本

或手動在 Zeabur 控制台觸發重新部署。

## 成本估算

Zeabur 提供：
- **免費方案**: 適合個人使用和測試
- **付費方案**: 根據使用量計費

詳情請參考：https://zeabur.com/pricing

## 支援

- **Zeabur 文檔**: https://zeabur.com/docs
- **專案 Issues**: https://github.com/zinojeng/deepseek-ocr-alpahxiv/issues
- **AlphaXiv 文檔**: https://www.alphaxiv.org/models/deepseek/deepseek-ocr
