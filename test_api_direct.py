#!/usr/bin/env python3
"""
直接測試 AlphaXiv API
"""
import requests
import os

def test_alphaxiv_api():
    """直接測試 AlphaXiv API"""

    api_url = "https://api.alphaxiv.org/models/v1/deepseek/deepseek-ocr/inference"
    test_pdf = "adrenal cortex.pdf"

    if not os.path.exists(test_pdf):
        print(f"❌ 找不到測試 PDF: {test_pdf}")
        return

    print(f"🔍 測試 AlphaXiv API")
    print(f"📡 API URL: {api_url}")
    print(f"📄 測試檔案: {test_pdf}")
    print(f"📊 檔案大小: {os.path.getsize(test_pdf) / 1024 / 1024:.2f} MB\n")

    try:
        with open(test_pdf, 'rb') as f:
            files = {'file': (test_pdf, f, 'application/pdf')}

            print("🚀 發送請求...")
            response = requests.post(
                api_url,
                files=files,
                timeout=300
            )

            print(f"\n📡 HTTP 狀態碼: {response.status_code}")
            print(f"📋 回應標頭:")
            for key, value in response.headers.items():
                print(f"  {key}: {value}")

            print(f"\n📝 回應內容 (前 1000 字元):")
            print(response.text[:1000])

            if response.status_code == 200:
                try:
                    result = response.json()
                    print(f"\n✅ API 回應成功")
                    print(f"📦 回應欄位: {list(result.keys())}")

                    # 檢查常見的回應格式
                    if 'text' in result:
                        print(f"✅ 找到 'text' 欄位")
                        print(f"   長度: {len(result['text'])} 字元")
                    if 'pages' in result:
                        print(f"✅ 找到 'pages' 欄位")
                        print(f"   頁數: {len(result['pages'])}")
                    if 'content' in result:
                        print(f"✅ 找到 'content' 欄位")

                except ValueError as e:
                    print(f"⚠️  無法解析 JSON: {e}")
            else:
                print(f"\n❌ API 回應錯誤")
                print(f"錯誤訊息: {response.text}")

    except requests.Timeout:
        print("❌ 請求超時")
    except requests.ConnectionError:
        print("❌ 連接失敗，請檢查網路")
    except Exception as e:
        print(f"❌ 錯誤: {e}")

if __name__ == "__main__":
    test_alphaxiv_api()
