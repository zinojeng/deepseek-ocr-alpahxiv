#!/usr/bin/env python3
"""
測試 PDF 上傳功能
"""
import requests
import os

def test_upload():
    """測試上傳端點"""

    # 檢查是否有測試 PDF
    test_pdf = "adrenal cortex.pdf"

    if not os.path.exists(test_pdf):
        print(f"❌ 找不到測試 PDF: {test_pdf}")
        print("請確保當前目錄有 PDF 檔案")
        return

    print(f"📄 使用測試檔案: {test_pdf}")
    print(f"📊 檔案大小: {os.path.getsize(test_pdf) / 1024 / 1024:.2f} MB")

    # 準備上傳
    url = "http://localhost:5001/upload"

    with open(test_pdf, 'rb') as f:
        files = {'file': (test_pdf, f, 'application/pdf')}

        print(f"\n🚀 發送請求到: {url}")

        try:
            response = requests.post(url, files=files, timeout=300)

            print(f"📡 HTTP 狀態碼: {response.status_code}")
            print(f"📋 回應內容:")
            print(response.text)

            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    print("\n✅ 上傳成功！")
                    print(f"📝 Markdown 長度: {len(result.get('markdown_content', ''))} 字元")
                    print(f"📁 輸出檔案: {result.get('output_file')}")
                else:
                    print(f"\n❌ 處理失敗: {result.get('error')}")
            else:
                print(f"\n❌ 請求失敗")

        except requests.exceptions.ConnectionError:
            print("❌ 無法連接到伺服器，請確認應用程式正在運行")
        except requests.exceptions.Timeout:
            print("❌ 請求超時")
        except Exception as e:
            print(f"❌ 錯誤: {e}")

if __name__ == "__main__":
    print("🧪 DeepSeek OCR 上傳測試\n")
    test_upload()
