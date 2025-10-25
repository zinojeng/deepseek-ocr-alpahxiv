#!/usr/bin/env python3
"""
完整功能測試
"""
import requests
import os
import time

def test_complete_workflow():
    """測試完整的上傳和下載流程"""

    base_url = "http://localhost:5001"
    test_pdf = "adrenal cortex.pdf"

    if not os.path.exists(test_pdf):
        print(f"❌ 找不到測試 PDF: {test_pdf}")
        return False

    print("🧪 開始完整功能測試\n")

    # 測試 1: 健康檢查
    print("1️⃣ 測試健康檢查端點...")
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            print("   ✅ 健康檢查通過")
        else:
            print(f"   ❌ 健康檢查失敗: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ 無法連接到伺服器: {e}")
        return False

    # 測試 2: 上傳 PDF
    print("\n2️⃣ 測試 PDF 上傳...")
    try:
        with open(test_pdf, 'rb') as f:
            files = {'file': (test_pdf, f, 'application/pdf')}
            response = requests.post(f"{base_url}/upload", files=files, timeout=300)

        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("   ✅ 上傳成功")
                output_file = result.get('output_file')
                markdown_content = result.get('markdown_content')
                metadata = result.get('metadata')

                print(f"   📁 輸出檔案: {output_file}")
                print(f"   📝 Markdown 長度: {len(markdown_content)} 字元")

                if metadata:
                    print(f"   ℹ️  元資料: {metadata}")

                # 測試 3: 下載檔案
                print("\n3️⃣ 測試檔案下載...")
                download_url = f"{base_url}/download/{output_file}"
                download_response = requests.get(download_url, timeout=10)

                if download_response.status_code == 200:
                    print("   ✅ 下載成功")
                    print(f"   📏 下載檔案大小: {len(download_response.content)} bytes")

                    # 驗證內容
                    if b"OCR" in download_response.content:
                        print("   ✅ 檔案內容驗證通過")
                        return True
                    else:
                        print("   ⚠️  檔案內容可能不完整")
                        return False
                else:
                    print(f"   ❌ 下載失敗: {download_response.status_code}")
                    print(f"   錯誤: {download_response.text}")
                    return False
            else:
                print(f"   ❌ 處理失敗: {result.get('error')}")
                return False
        else:
            print(f"   ❌ 上傳失敗: {response.status_code}")
            print(f"   錯誤: {response.text}")
            return False

    except requests.Timeout:
        print("   ❌ 請求超時")
        return False
    except Exception as e:
        print(f"   ❌ 錯誤: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("  DeepSeek OCR - 完整功能測試")
    print("=" * 60)

    success = test_complete_workflow()

    print("\n" + "=" * 60)
    if success:
        print("  ✅ 所有測試通過！")
    else:
        print("  ❌ 測試失敗，請檢查錯誤訊息")
    print("=" * 60)
