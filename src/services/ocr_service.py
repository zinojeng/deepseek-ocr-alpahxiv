"""
OCR 處理服務
協調 API 呼叫和結果處理
"""

import os
import logging
from typing import Dict, Any, Optional
from datetime import datetime
from ..api.alphaxiv_client import AlphaXivClient
from ..utils.markdown_converter import MarkdownConverter

logger = logging.getLogger(__name__)


class OCRService:
    """OCR 處理服務類別"""

    def __init__(self):
        """初始化 OCR 服務"""
        self.client = AlphaXivClient()
        self.converter = MarkdownConverter()
        logger.info("OCR 服務已初始化")

    def process_document(self, file_path: str, output_dir: Optional[str] = None) -> Dict[str, Any]:
        """
        處理文件並生成 Markdown 輸出

        Args:
            file_path: 輸入 PDF 檔案路徑
            output_dir: 輸出目錄，如果未提供則使用 'outputs'

        Returns:
            包含處理結果的字典，包括：
            - success: 是否成功
            - markdown_content: Markdown 內容
            - output_file: 輸出檔案路徑
            - metadata: 處理元資料
        """
        logger.info(f"開始處理文件: {file_path}")

        try:
            # 呼叫 AlphaXiv API
            ocr_result = self.client.process_pdf(file_path)

            # 轉換為 Markdown
            markdown_content = self.converter.convert_to_markdown(ocr_result)

            # 準備輸出
            if output_dir is None:
                output_dir = 'outputs'

            os.makedirs(output_dir, exist_ok=True)

            # 生成輸出檔案名稱
            base_name = os.path.splitext(os.path.basename(file_path))[0]
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = os.path.join(output_dir, f"{base_name}_{timestamp}.md")

            # 儲存 Markdown 檔案
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(markdown_content)

            logger.info(f"文件處理完成，輸出至: {output_file}")

            return {
                'success': True,
                'markdown_content': markdown_content,
                'output_file': output_file,
                'metadata': {
                    'input_file': file_path,
                    'output_file': output_file,
                    'processed_at': datetime.now().isoformat(),
                    'content_length': len(markdown_content)
                }
            }

        except Exception as e:
            logger.error(f"文件處理失敗: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'metadata': {
                    'input_file': file_path,
                    'failed_at': datetime.now().isoformat()
                }
            }

    def process_uploaded_file(self, file_bytes: bytes, filename: str,
                            output_dir: Optional[str] = None) -> Dict[str, Any]:
        """
        處理上傳的檔案

        Args:
            file_bytes: 檔案位元組資料
            filename: 檔案名稱
            output_dir: 輸出目錄

        Returns:
            處理結果字典
        """
        logger.info(f"開始處理上傳檔案: {filename}")

        try:
            # 呼叫 AlphaXiv API
            ocr_result = self.client.process_pdf_from_bytes(file_bytes, filename)

            # 轉換為 Markdown
            markdown_content = self.converter.convert_to_markdown(ocr_result)

            # 準備輸出
            if output_dir is None:
                output_dir = 'outputs'

            os.makedirs(output_dir, exist_ok=True)

            # 生成輸出檔案名稱
            base_name = os.path.splitext(filename)[0]
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = os.path.join(output_dir, f"{base_name}_{timestamp}.md")

            # 儲存 Markdown 檔案
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(markdown_content)

            logger.info(f"檔案處理完成，輸出至: {output_file}")

            return {
                'success': True,
                'markdown_content': markdown_content,
                'output_file': output_file,
                'metadata': {
                    'input_file': filename,
                    'output_file': output_file,
                    'processed_at': datetime.now().isoformat(),
                    'content_length': len(markdown_content)
                }
            }

        except Exception as e:
            logger.error(f"檔案處理失敗: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'metadata': {
                    'input_file': filename,
                    'failed_at': datetime.now().isoformat()
                }
            }
