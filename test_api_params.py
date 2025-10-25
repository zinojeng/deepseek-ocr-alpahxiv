#!/usr/bin/env python3
"""
測試 AlphaXiv API 參數
研究如何啟用圖像解析
"""
import requests
import os
import json

def test_with_params():
    """測試不同的 API 參數組合"""

    api_url = "https://api.alphaxiv.org/models/v1/deepseek/deepseek-ocr/inference"
    test_pdf = "adrenal cortex.pdf"

    if not os.path.exists(test_pdf):
        print(f"❌ 找不到測試 PDF: {test_pdf}")
        return

    print(f"🔍 測試 AlphaXiv API 參數")
    print(f"📡 API URL: {api_url}\n")

    # 測試配置
    test_configs = [
        {
            "name": "基本請求（無參數）",
            "data": None,
            "files_only": True
        },
        {
            "name": "添加 prompt 參數（grounding）",
            "data": {"prompt": "<|grounding|>Convert the document to markdown."},
            "files_only": False
        },
        {
            "name": "添加 prompt 參數（parse figure）",
            "data": {"prompt": "Parse the figure."},
            "files_only": False
        },
        {
            "name": "添加完整參數",
            "data": {
                "prompt": "<|grounding|>Convert the document to markdown.",
                "base_size": 1024,
                "crop_mode": True
            },
            "files_only": False
        }
    ]

    for i, config in enumerate(test_configs, 1):
        print(f"\n{'='*60}")
        print(f"測試 {i}: {config['name']}")
        print(f"{'='*60}")

        try:
            with open(test_pdf, 'rb') as f:
                files = {'file': (test_pdf, f, 'application/pdf')}

                if config['files_only']:
                    # 只發送文件
                    print("📤 發送: 僅文件")
                    response = requests.post(api_url, files=files, timeout=60)
                else:
                    # 發送文件 + 數據
                    print(f"📤 發送: 文件 + 參數")
                    print(f"   參數: {json.dumps(config['data'], indent=2)}")
                    response = requests.post(
                        api_url,
                        files=files,
                        data=config['data'],
                        timeout=60
                    )

            print(f"\n📡 HTTP 狀態碼: {response.status_code}")

            if response.status_code == 200:
                try:
                    result = response.json()
                    print(f"✅ 請求成功")

                    # 檢查回應結構
                    if 'data' in result:
                        data = result['data']
                        if 'ocr_text' in data:
                            text = data['ocr_text']
                            print(f"📝 OCR 文字長度: {len(text)} 字元")

                            # 檢查是否有圖像描述
                            if 'FIGURE' in text[:2000]:
                                # 檢查圖像是否有詳細描述
                                figure_lines = [line for line in text.split('\n') if 'FIGURE' in line]
                                print(f"\n🖼️  發現圖像引用: {len(figure_lines)} 個")
                                for line in figure_lines[:3]:
                                    print(f"   - {line[:100]}")

                                # 檢查是否只是佔位符
                                if all('?' in line or 'center' in line.lower() for line in figure_lines):
                                    print("   ⚠️  似乎只有圖像佔位符，沒有實際解析")
                                else:
                                    print("   ✅ 可能包含圖像內容解析")

                        # 顯示額外的欄位
                        other_fields = [k for k in data.keys() if k != 'ocr_text']
                        if other_fields:
                            print(f"\n📦 其他欄位: {other_fields}")
                            for field in other_fields:
                                print(f"   - {field}: {str(data[field])[:100]}")

                    print(f"\n📋 完整回應鍵值: {list(result.keys())}")

                except ValueError as e:
                    print(f"⚠️  無法解析 JSON: {e}")
                    print(f"回應內容 (前 500 字元): {response.text[:500]}")
            else:
                print(f"❌ 請求失敗")
                print(f"錯誤: {response.text[:500]}")

        except requests.Timeout:
            print("❌ 請求超時")
        except Exception as e:
            print(f"❌ 錯誤: {e}")

    print(f"\n{'='*60}")
    print("測試完成")
    print(f"{'='*60}")

if __name__ == "__main__":
    test_with_params()
