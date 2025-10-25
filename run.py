#!/usr/bin/env python3
"""
DeepSeek OCR Application Entry Point
快速啟動腳本
"""
import sys
from pathlib import Path

# 將 src 目錄加入 Python 路徑
project_root = Path(__file__).parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

if __name__ == "__main__":
    # 導入並執行主應用程式
    from app import app, main
    main()
