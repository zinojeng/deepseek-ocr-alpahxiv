"""
Markdown 轉換器
將 OCR 結果轉換為 Markdown 格式
"""

import logging
import re
from typing import Dict, Any, List

logger = logging.getLogger(__name__)


class MarkdownConverter:
    """將 OCR 結果轉換為 Markdown 格式"""

    def _enhance_figure_markup(self, text: str) -> str:
        """
        增強圖像標記，使其在 Markdown 中更清楚

        Args:
            text: 原始 OCR 文字

        Returns:
            增強後的文字
        """
        # 替換 <center>FIGURE...</center> 為更清楚的 Markdown 格式
        pattern = r'<center>(FIGURE [^<]+)</center>'

        def replace_figure(match):
            figure_text = match.group(1)
            # 分離標題和說明
            parts = figure_text.split('.', 1)
            if len(parts) == 2:
                title = parts[0].strip()
                description = parts[1].strip()
                return f"\n\n---\n\n### 📊 {title}\n\n**說明**: {description}\n\n> ⚠️ *注意: 此處為圖像位置。OCR 已提取圖像中的文字標註，但無法提供圖像的視覺結構描述。*\n\n---\n\n"
            else:
                return f"\n\n---\n\n### 📊 {figure_text}\n\n> ⚠️ *注意: 此處為圖像位置。*\n\n---\n\n"

        text = re.sub(pattern, replace_figure, text, flags=re.DOTALL)

        # 處理其他可能的圖像標記
        text = re.sub(r'<center>([^<]+)</center>', r'\n\n**\1**\n\n', text)

        return text

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
        # AlphaXiv 格式: {"data": {"ocr_text": "..."}}
        if 'data' in ocr_result:
            data = ocr_result['data']
            if 'ocr_text' in data:
                markdown_lines.append("## 提取的文字內容\n")
                # 增強圖像標記
                enhanced_text = self._enhance_figure_markup(data['ocr_text'])
                markdown_lines.append(enhanced_text)
                markdown_lines.append("\n")

                # 添加統計信息
                if 'num_pages' in data:
                    markdown_lines.append("\n---\n\n")
                    markdown_lines.append("## 📊 處理統計\n\n")
                    markdown_lines.append(f"- **總頁數**: {data['num_pages']}\n")
                    if 'num_successful' in data:
                        markdown_lines.append(f"- **成功處理**: {data['num_successful']}\n")

                    # 統計圖像數量
                    figure_count = len(re.findall(r'<center>FIGURE', data['ocr_text']))
                    if figure_count > 0:
                        markdown_lines.append(f"- **圖像數量**: {figure_count}\n")
                        markdown_lines.append(f"\n> 💡 **提示**: OCR 已提取圖像中的所有文字標註和說明，但無法描述圖像的視覺內容（如流程圖結構、關係圖等）。如需圖像內容理解，建議使用 Vision Language Model (如 GPT-4V)。\n")

            elif 'text' in data:
                markdown_lines.append("## 提取的文字內容\n")
                enhanced_text = self._enhance_figure_markup(data['text'])
                markdown_lines.append(enhanced_text)
                markdown_lines.append("\n")
            else:
                # data 欄位存在但格式不符，顯示原始內容
                markdown_lines.append("## 原始結果\n")
                markdown_lines.append("```json\n")
                import json
                markdown_lines.append(json.dumps(data, ensure_ascii=False, indent=2))
                markdown_lines.append("\n```\n")

        # 格式1: 直接包含 text 欄位
        elif 'text' in ocr_result:
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
