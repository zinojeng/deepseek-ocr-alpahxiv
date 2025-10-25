"""
Markdown 轉換器
將 OCR 結果轉換為 Markdown 格式
"""

import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)


class MarkdownConverter:
    """將 OCR 結果轉換為 Markdown 格式"""

    def convert_to_markdown(self, ocr_result: Dict[str, Any]) -> str:
        """
        將 OCR 結果轉換為 Markdown

        Args:
            ocr_result: AlphaXiv API 返回的 OCR 結果

        Returns:
            Markdown 格式的字串
        """
        logger.debug("開始轉換 OCR 結果為 Markdown")

        # 檢查結果格式
        if not ocr_result:
            logger.warning("OCR 結果為空")
            return "# 處理結果\n\n無法從 PDF 中提取內容。\n"

        markdown_lines = []

        # 添加標題
        markdown_lines.append("# OCR 處理結果\n")

        # 處理不同的回應格式
        # 格式1: 直接包含 text 欄位
        if 'text' in ocr_result:
            markdown_lines.append("## 提取的文字內容\n")
            markdown_lines.append(ocr_result['text'])
            markdown_lines.append("\n")

        # 格式2: 包含 pages 陣列
        elif 'pages' in ocr_result:
            markdown_lines.append("## 文件內容\n")
            for page_num, page in enumerate(ocr_result['pages'], 1):
                markdown_lines.append(f"### 第 {page_num} 頁\n")
                if 'text' in page:
                    markdown_lines.append(page['text'])
                    markdown_lines.append("\n")

        # 格式3: 包含 content 欄位
        elif 'content' in ocr_result:
            markdown_lines.append("## 文件內容\n")
            markdown_lines.append(ocr_result['content'])
            markdown_lines.append("\n")

        # 格式4: 包含 results 陣列
        elif 'results' in ocr_result:
            markdown_lines.append("## 辨識結果\n")
            for item in ocr_result['results']:
                if isinstance(item, dict) and 'text' in item:
                    markdown_lines.append(item['text'])
                    markdown_lines.append("\n")
                elif isinstance(item, str):
                    markdown_lines.append(item)
                    markdown_lines.append("\n")

        # 如果都沒有，嘗試將整個結果轉為字串
        else:
            markdown_lines.append("## 原始結果\n")
            markdown_lines.append("```json\n")
            import json
            markdown_lines.append(json.dumps(ocr_result, ensure_ascii=False, indent=2))
            markdown_lines.append("\n```\n")

        # 添加元資料（如果有的話）
        if 'metadata' in ocr_result:
            markdown_lines.append("\n---\n")
            markdown_lines.append("## 處理資訊\n")
            metadata = ocr_result['metadata']
            for key, value in metadata.items():
                markdown_lines.append(f"- **{key}**: {value}\n")

        result = '\n'.join(markdown_lines)
        logger.debug(f"Markdown 轉換完成，長度: {len(result)} 字元")

        return result

    def format_text_blocks(self, text_blocks: List[Dict[str, Any]]) -> str:
        """
        格式化文字區塊

        Args:
            text_blocks: 文字區塊列表

        Returns:
            格式化的 Markdown 字串
        """
        markdown_lines = []

        for block in text_blocks:
            block_type = block.get('type', 'text')

            if block_type == 'heading':
                level = block.get('level', 2)
                markdown_lines.append(f"{'#' * level} {block.get('text', '')}\n")

            elif block_type == 'paragraph':
                markdown_lines.append(f"{block.get('text', '')}\n")

            elif block_type == 'list':
                items = block.get('items', [])
                for item in items:
                    markdown_lines.append(f"- {item}\n")

            elif block_type == 'code':
                markdown_lines.append("```\n")
                markdown_lines.append(block.get('text', ''))
                markdown_lines.append("\n```\n")

            elif block_type == 'table':
                # 簡單的表格處理
                markdown_lines.append(self._format_table(block))

            else:
                markdown_lines.append(f"{block.get('text', '')}\n")

            markdown_lines.append("\n")

        return '\n'.join(markdown_lines)

    def _format_table(self, table_block: Dict[str, Any]) -> str:
        """格式化表格"""
        rows = table_block.get('rows', [])
        if not rows:
            return ""

        lines = []

        # 標題行
        if 'headers' in table_block:
            headers = table_block['headers']
            lines.append("| " + " | ".join(headers) + " |")
            lines.append("| " + " | ".join(["---"] * len(headers)) + " |")

        # 資料行
        for row in rows:
            if isinstance(row, list):
                lines.append("| " + " | ".join(str(cell) for cell in row) + " |")

        return "\n".join(lines)
