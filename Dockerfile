# DeepSeek OCR Docker 映像

FROM python:3.10-slim

# 設定工作目錄
WORKDIR /app

# 安裝系統依賴
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 複製需求檔案
COPY requirements.txt .

# 安裝 Python 依賴
RUN pip install --no-cache-dir -r requirements.txt

# 複製應用程式碼
COPY . .

# 建立必要目錄
RUN mkdir -p uploads outputs

# 設定環境變數
ENV FLASK_APP=src/app.py
ENV FLASK_ENV=production
ENV PORT=8080

# 暴露端口（Zeabur 使用 PORT 環境變數）
EXPOSE 8080

# 啟動命令
CMD ["python", "run.py"]
