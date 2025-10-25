#!/usr/bin/env python3
"""
檢查 pages 欄位的詳細內容
"""
import requests
import os
import json

def test_pages_detail():
    """檢查每頁的詳細內容"""

    api_url = "https://api.alphaxiv.org/models/v1/deepseek/deepseek-ocr/inference"
    test_pdf = "adrenal cortex.pdf"

    if not os.path.exists(test_pdf):
        print(f"❌ 找不到測試 PDF")
        return

    print(f"🔍 分析 API 回應中的 pages 欄位\n")

    try:
        with open(test_pdf, 'rb') as f:
            files = {'file': (test_pdf, f, 'application/pdf')}
            response = requests.post(api_url, files=files, timeout=120)

        if response.status_code == 200:
            result = response.json()
            data = result.get('data', {})

            print(f"📊 總頁數: {data.get('num_pages')}")
            print(f"✅ 成功處理: {data.get('num_successful')}")

            pages = data.get('pages', [])
            print(f"\n📄 Pages 陣列長度: {len(pages)}")
            print(f"📄 Pages 資料類型: {type(pages)}")

            if pages:
                print(f"\n--- 第 1 頁內容樣本 ---")
                page1 = pages[0]
                print(f"類型: {type(page1)}")
                print(f"長度: {len(page1) if isinstance(page1, str) else 'N/A'}")
                print(f"前 1000 字元:")
                print(page1[:1000] if isinstance(page1, str) else str(page1)[:1000])

                # 查找包含 FIGURE 的頁面
                print(f"\n🖼️  查找圖像引用...")
                for i, page in enumerate(pages):
                    if isinstance(page, str) and 'FIGURE' in page:
                        print(f"\n--- 第 {i+1} 頁包含 FIGURE ---")
                        # 提取 FIGURE 相關的行
                        lines = page.split('\n')
                        figure_context = []
                        for j, line in enumerate(lines):
                            if 'FIGURE' in line:
                                # 取前後各 5 行
                                start = max(0, j-2)
                                end = min(len(lines), j+3)
                                figure_context = lines[start:end]
                                break

                        print('\n'.join(figure_context))

                        if i >= 2:  # 只顯示前幾個
                            print("\n... (還有更多)")
                            break

            # 檢查 ocr_text 欄位
            ocr_text = data.get('ocr_text', '')
            if ocr_text:
                print(f"\n📝 ocr_text 欄位:")
                print(f"   類型: {type(ocr_text)}")
                print(f"   長度: {len(ocr_text)}")

                # 檢查是否與 pages 內容相同
                pages_combined = '\n\n<--- Page Split --->\n\n'.join(pages) if pages else ''
                if ocr_text == pages_combined:
                    print("   ℹ️  ocr_text 是所有頁面的組合")
                else:
                    print("   ℹ️  ocr_text 與 pages 不完全相同")

        else:
            print(f"❌ 請求失敗: {response.status_code}")

    except Exception as e:
        print(f"❌ 錯誤: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_pages_detail()
