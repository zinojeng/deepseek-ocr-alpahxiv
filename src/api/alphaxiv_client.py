"""
AlphaXiv API 客戶端
用於與 DeepSeek OCR API 進行通訊
"""

import requests
import os
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)


class AlphaXivClient:
    """AlphaXiv DeepSeek OCR API 客戶端"""

    def __init__(self, api_url: Optional[str] = None):
        """
        初始化 AlphaXiv 客戶端

        Args:
            api_url: API 端點 URL，如果未提供則從環境變數讀取
        """
        self.api_url = api_url or os.getenv(
            'ALPHAXIV_API_URL',
            'https://api.alphaxiv.org/models/v1/deepseek/deepseek-ocr/inference'
        )
        logger.info(f"AlphaXiv 客戶端已初始化，API URL: {self.api_url}")

    def process_pdf(self, file_path: str) -> Dict[str, Any]:
        """
        處理 PDF 檔案並執行 OCR

        Args:
            file_path: PDF 檔案路徑

        Returns:
            包含 OCR 結果的字典

        Raises:
            FileNotFoundError: 如果檔案不存在
            requests.RequestException: 如果 API 請求失敗
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"檔案不存在: {file_path}")

        logger.info(f"開始處理 PDF 檔案: {file_path}")

        try:
            with open(file_path, 'rb') as f:
                files = {'file': (os.path.basename(file_path), f, 'application/pdf')}

                logger.debug(f"發送 POST 請求到: {self.api_url}")
                response = requests.post(
                    self.api_url,
                    files=files,
                    timeout=300  # 5 分鐘超時
                )

                response.raise_for_status()

                result = response.json()
                logger.info(f"PDF 處理成功: {file_path}")

                return result

        except requests.Timeout:
            logger.error(f"請求超時: {file_path}")
            raise Exception("API 請求超時，請稍後再試")

        except requests.RequestException as e:
            logger.error(f"API 請求失敗: {str(e)}")
            raise Exception(f"OCR 處理失敗: {str(e)}")

    def process_pdf_from_bytes(self, file_bytes: bytes, filename: str) -> Dict[str, Any]:
        """
        從位元組資料處理 PDF

        Args:
            file_bytes: PDF 檔案的位元組資料
            filename: 檔案名稱

        Returns:
            包含 OCR 結果的字典
        """
        logger.info(f"開始處理 PDF (從位元組): {filename}")

        try:
            files = {'file': (filename, file_bytes, 'application/pdf')}

            logger.debug(f"發送 POST 請求到: {self.api_url}")
            response = requests.post(
                self.api_url,
                files=files,
                timeout=300
            )

            response.raise_for_status()

            result = response.json()
            logger.info(f"PDF 處理成功: {filename}")

            return result

        except requests.Timeout:
            logger.error(f"請求超時: {filename}")
            raise Exception("API 請求超時，請稍後再試")

        except requests.RequestException as e:
            logger.error(f"API 請求失敗: {str(e)}")
            raise Exception(f"OCR 處理失敗: {str(e)}")
