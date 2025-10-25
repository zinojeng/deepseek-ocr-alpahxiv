"""
OCR 服務測試
"""

import unittest
import sys
import os

# 添加父目錄到路徑
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.utils.file_validator import FileValidator
from src.utils.markdown_converter import MarkdownConverter


class TestFileValidator(unittest.TestCase):
    """測試檔案驗證器"""

    def test_allowed_file_pdf(self):
        """測試允許的 PDF 檔案"""
        self.assertTrue(FileValidator.allowed_file('test.pdf'))
        self.assertTrue(FileValidator.allowed_file('document.PDF'))

    def test_disallowed_file(self):
        """測試不允許的檔案類型"""
        self.assertFalse(FileValidator.allowed_file('test.txt'))
        self.assertFalse(FileValidator.allowed_file('image.jpg'))
        self.assertFalse(FileValidator.allowed_file('noextension'))

    def test_file_size_validation(self):
        """測試檔案大小驗證"""
        # 正常大小
        is_valid, _ = FileValidator.validate_file_size(1024 * 1024)  # 1 MB
        self.assertTrue(is_valid)

        # 過大
        is_valid, error_msg = FileValidator.validate_file_size(20 * 1024 * 1024)  # 20 MB
        self.assertFalse(is_valid)
        self.assertIn('過大', error_msg)

    def test_validate_upload(self):
        """測試完整的上傳驗證"""
        # 有效上傳
        is_valid, _ = FileValidator.validate_upload('test.pdf', 1024 * 1024)
        self.assertTrue(is_valid)

        # 無檔案名稱
        is_valid, error_msg = FileValidator.validate_upload('', 1024)
        self.assertFalse(is_valid)

        # 錯誤格式
        is_valid, error_msg = FileValidator.validate_upload('test.txt', 1024)
        self.assertFalse(is_valid)


class TestMarkdownConverter(unittest.TestCase):
    """測試 Markdown 轉換器"""

    def setUp(self):
        self.converter = MarkdownConverter()

    def test_convert_with_text_field(self):
        """測試包含 text 欄位的轉換"""
        ocr_result = {
            'text': '這是測試文字內容'
        }
        markdown = self.converter.convert_to_markdown(ocr_result)

        self.assertIn('OCR 處理結果', markdown)
        self.assertIn('這是測試文字內容', markdown)

    def test_convert_with_pages(self):
        """測試包含 pages 陣列的轉換"""
        ocr_result = {
            'pages': [
                {'text': '第一頁內容'},
                {'text': '第二頁內容'}
            ]
        }
        markdown = self.converter.convert_to_markdown(ocr_result)

        self.assertIn('第 1 頁', markdown)
        self.assertIn('第 2 頁', markdown)
        self.assertIn('第一頁內容', markdown)
        self.assertIn('第二頁內容', markdown)

    def test_convert_empty_result(self):
        """測試空結果"""
        markdown = self.converter.convert_to_markdown({})
        self.assertIn('無法從 PDF 中提取內容', markdown)

    def test_convert_with_metadata(self):
        """測試包含元資料的轉換"""
        ocr_result = {
            'text': '內容',
            'metadata': {
                'pages': 1,
                'language': 'zh-TW'
            }
        }
        markdown = self.converter.convert_to_markdown(ocr_result)

        self.assertIn('處理資訊', markdown)
        self.assertIn('pages', markdown)
        self.assertIn('language', markdown)


if __name__ == '__main__':
    unittest.main()
