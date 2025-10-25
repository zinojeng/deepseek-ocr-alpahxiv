"""
檔案驗證工具
"""

import os
import logging
from typing import Tuple

logger = logging.getLogger(__name__)


class FileValidator:
    """檔案驗證類別"""

    ALLOWED_EXTENSIONS = {'pdf'}
    # 從環境變數讀取最大檔案大小，預設 100 MB
    MAX_FILE_SIZE = int(os.getenv('MAX_FILE_SIZE', 100 * 1024 * 1024))

    @staticmethod
    def allowed_file(filename: str) -> bool:
        """
        檢查檔案副檔名是否允許

        Args:
            filename: 檔案名稱

        Returns:
            True 如果允許，否則 False
        """
        if '.' not in filename:
            return False

        extension = filename.rsplit('.', 1)[1].lower()
        is_allowed = extension in FileValidator.ALLOWED_EXTENSIONS

        logger.debug(f"檔案 {filename} 副檔名檢查: {is_allowed}")
        return is_allowed

    @staticmethod
    def validate_file_size(file_size: int) -> Tuple[bool, str]:
        """
        驗證檔案大小

        Args:
            file_size: 檔案大小（位元組）

        Returns:
            (是否有效, 錯誤訊息)
        """
        if file_size > FileValidator.MAX_FILE_SIZE:
            size_mb = file_size / (1024 * 1024)
            max_mb = FileValidator.MAX_FILE_SIZE / (1024 * 1024)
            error_msg = f"檔案過大 ({size_mb:.2f} MB)，最大允許 {max_mb} MB"
            logger.warning(error_msg)
            return False, error_msg

        return True, ""

    @staticmethod
    def validate_upload(filename: str, file_size: int) -> Tuple[bool, str]:
        """
        驗證上傳的檔案

        Args:
            filename: 檔案名稱
            file_size: 檔案大小

        Returns:
            (是否有效, 錯誤訊息)
        """
        # 檢查檔案名稱
        if not filename:
            return False, "未提供檔案"

        # 檢查副檔名
        if not FileValidator.allowed_file(filename):
            return False, f"不支援的檔案格式，僅支援: {', '.join(FileValidator.ALLOWED_EXTENSIONS)}"

        # 檢查檔案大小
        is_valid, error_msg = FileValidator.validate_file_size(file_size)
        if not is_valid:
            return False, error_msg

        logger.info(f"檔案驗證通過: {filename}")
        return True, ""
