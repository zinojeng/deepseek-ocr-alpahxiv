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

    def _reorganize_paragraphs_with_figures(self, text: str) -> str:
        """
        重組段落，將被圖片說明中斷的段落連接在一起

        處理邏輯：
        1. 找到所有圖片說明標記
        2. 檢查圖片說明前後的文字是否屬於同一段落
        3. 如果是，則合併段落，並將圖片說明移到段落後面

        Args:
            text: 原始 OCR 文字

        Returns:
            重組後的文字
        """
        # 先移除分頁標記
        text = re.sub(
            r'\n*<---\s*Page\s*Split\s*--->\n*',
            ' ',
            text,
            flags=re.IGNORECASE
        )

        # 找到所有圖片說明及其位置
        figure_pattern = r'(<center>FIGURE[^<]+</center>)'

        # 使用 split 保留分隔符
        parts = re.split(figure_pattern, text)

        result_parts = []
        i = 0

        while i < len(parts):
            current_part = parts[i]

            # 如果當前部分是圖片說明
            if re.match(figure_pattern, current_part):
                # 檢查前一個部分（文字）和後一個部分（文字）
                prev_text = result_parts[-1] if result_parts else ""
                next_text = parts[i + 1] if i + 1 < len(parts) else ""

                # 判斷是否需要合併段落
                should_merge = self._should_merge_paragraphs(
                    prev_text, next_text
                )

                if should_merge and result_parts and next_text:
                    # 從結果中移除前一個文字部分
                    prev_text = result_parts.pop()

                    # 清理並合併文字
                    prev_text = prev_text.rstrip()
                    next_text = next_text.lstrip()

                    # 合併段落（在中間加一個空格以確保單字不會連在一起）
                    merged_text = prev_text + ' ' + next_text

                    # 添加合併後的段落
                    result_parts.append(merged_text)
                    # 添加圖片說明
                    result_parts.append(current_part)

                    # 跳過下一個部分（因為已經合併了）
                    i += 2
                else:
                    # 不需要合併，直接添加圖片說明
                    result_parts.append(current_part)
                    i += 1
            else:
                # 普通文字部分，只有非空時才添加
                if current_part or not result_parts:
                    result_parts.append(current_part)
                i += 1

        return ''.join(result_parts)

    def _should_merge_paragraphs(
        self, prev_text: str, next_text: str
    ) -> bool:
        """
        判斷兩個文字片段是否應該合併為一個段落

        判斷標準：
        1. 前一段文字不是以句號、問號、驚嘆號結尾
        2. 後一段文字以小寫字母或「and」等連接詞開頭
        3. 前一段文字不是以換行符結尾（表示不是獨立段落）

        Args:
            prev_text: 前一段文字
            next_text: 後一段文字

        Returns:
            是否應該合併
        """
        if not prev_text or not next_text:
            return False

        # 清理空白字符以便檢查
        prev_cleaned = prev_text.strip()
        next_cleaned = next_text.strip()

        if not prev_cleaned or not next_cleaned:
            return False

        # 檢查前一段是否以句子結束標點符號結尾
        sentence_endings = [
            '.', '?', '!', '。', '？', '！', ':', '：'
        ]
        ends_with_punctuation = any(
            prev_cleaned.endswith(p) for p in sentence_endings
        )

        # 檢查後一段是否以小寫字母或連接詞開頭
        next_words = next_cleaned.split()
        next_first_word = next_words[0] if next_words else ""
        starts_with_lowercase = (
            next_first_word and next_first_word[0].islower()
        )

        # 常見的連接詞
        connecting_words = [
            'and', 'or', 'but', 'however', 'moreover', 'furthermore',
            'therefore', 'thus', 'hence', 'consequently', 'prompting',
            'resulting', 'leading', 'causing', 'which', 'that', 'who'
        ]
        starts_with_connector = (
            next_first_word.lower() in connecting_words
        )

        # 如果前一段沒有以句號結尾，且後一段以小寫或連接詞開頭，
        # 則應該合併
        should_merge = (
            (not ends_with_punctuation) or
            starts_with_lowercase or
            starts_with_connector
        )

        return should_merge

    def _enhance_figure_markup(self, text: str) -> str:
        """
        增強圖像標記，使其在 Markdown 中更清楚

        Args:
            text: 原始 OCR 文字

        Returns:
            增強後的文字
        """
        # 首先重組段落，將被圖片說明中斷的段落連接在一起
        text = self._reorganize_paragraphs_with_figures(text)

        # 替換 <center>FIGURE...</center> 為更清楚的 Markdown 格式
        pattern = r'<center>(FIGURE [^<]+)</center>'

        def replace_figure(match):
            figure_text = match.group(1)
            # 分離標題和說明
            parts = figure_text.split('.', 1)
            if len(parts) == 2:
                title = parts[0].strip()
                description = parts[1].strip()
                return (
                    f"\n\n---\n\n### 📊 {title}\n\n"
                    f"**說明**: {description}\n\n"
                    "> ⚠️ *注意: 此處為圖像位置。OCR 已提取圖像中的"
                    "文字標註，但無法提供圖像的視覺結構描述。*\n\n---\n\n"
                )
            else:
                return (
                    f"\n\n---\n\n### 📊 {figure_text}\n\n"
                    "> ⚠️ *注意: 此處為圖像位置。*\n\n---\n\n"
                )

        text = re.sub(pattern, replace_figure, text, flags=re.DOTALL)

        # 處理其他可能的圖像標記
        text = re.sub(
            r'<center>([^<]+)</center>',
            r'\n\n**\1**\n\n',
            text
        )

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
                        markdown_lines.append(
                            f"- **成功處理**: {data['num_successful']}\n"
                        )

                    # 統計圖像數量
                    figure_count = len(
                        re.findall(r'<center>FIGURE', data['ocr_text'])
                    )
                    if figure_count > 0:
                        markdown_lines.append(
                            f"- **圖像數量**: {figure_count}\n"
                        )
                        tip = (
                            "\n> 💡 **提示**: OCR 已提取圖像中的所有"
                            "文字標註和說明，但無法描述圖像的視覺內容"
                            "（如流程圖結構、關係圖等）。如需圖像內容"
                            "理解，建議使用 Vision Language Model "
                            "(如 GPT-4V)。\n"
                        )
                        markdown_lines.append(tip)

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
                markdown_lines.append(
                    json.dumps(data, ensure_ascii=False, indent=2)
                )
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
            markdown_lines.append(
                json.dumps(ocr_result, ensure_ascii=False, indent=2)
            )
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
                markdown_lines.append(
                    f"{'#' * level} {block.get('text', '')}\n"
                )

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
                row_text = " | ".join(str(cell) for cell in row)
                lines.append(f"| {row_text} |")

        return "\n".join(lines)
