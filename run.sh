#!/bin/bash

# DeepSeek OCR 啟動腳本

echo "🚀 啟動 DeepSeek OCR 應用程式..."

# 檢查 Python 版本
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python 版本: $python_version"

# 建立虛擬環境（如果不存在）
if [ ! -d "venv" ]; then
    echo "📦 建立虛擬環境..."
    python3 -m venv venv
fi

# 啟用虛擬環境
echo "🔧 啟用虛擬環境..."
source venv/bin/activate

# 安裝依賴
echo "📚 安裝依賴套件..."
pip install -r requirements.txt

# 建立必要目錄
echo "📁 建立必要目錄..."
mkdir -p uploads outputs

# 複製環境變數檔案（如果不存在）
if [ ! -f ".env" ]; then
    echo "⚙️  建立 .env 檔案..."
    cp .env.example .env
    echo "請編輯 .env 檔案設定您的配置"
fi

# 啟動應用程式
echo "✨ 啟動 Flask 應用程式..."
echo "應用程式將在 http://localhost:5000 啟動"
echo "按 Ctrl+C 停止應用程式"
echo ""

python src/app.py
