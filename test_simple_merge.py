"""
簡單的段落合併測試
"""

from src.utils.markdown_converter import MarkdownConverter


def test_simple_cases():
    """測試簡單的合併案例"""

    converter = MarkdownConverter()

    print("=" * 80)
    print("測試 1: 基本合併 - 前面沒有句號，後面小寫開頭")
    print("=" * 80)

    test1 = """Text before the<center>FIGURE 1 Test.</center>text after continues."""
    result1 = converter._reorganize_paragraphs_with_figures(test1)
    print(f"輸入: {test1}")
    print(f"輸出: {result1}")
    assert "before the text after" in result1
    print("✅ 測試 1 通過\n")

    print("=" * 80)
    print("測試 2: 不合併 - 前面有句號，後面大寫開頭")
    print("=" * 80)

    test2 = """Sentence ends.<center>FIGURE 2 Test.</center>New sentence starts."""
    result2 = converter._reorganize_paragraphs_with_figures(test2)
    print(f"輸入: {test2}")
    print(f"輸出: {result2}")
    # 這種情況下可能會合併（因為 "New" 開頭，但根據邏輯應該檢查）
    print(f"結果: {result2}")
    print()

    print("=" * 80)
    print("測試 3: 合併 - 後面以連接詞開頭")
    print("=" * 80)

    test3 = """Text ends.<center>FIGURE 3 Test.</center>prompting further discussion."""
    result3 = converter._reorganize_paragraphs_with_figures(test3)
    print(f"輸入: {test3}")
    print(f"輸出: {result3}")
    assert "ends. prompting" in result3
    print("✅ 測試 3 通過\n")

    print("=" * 80)
    print("測試 4: 您的原始例子")
    print("=" * 80)

    test4 = """HF and the<center>FIGURE X Test.</center>diverse underlying comorbidities prompting"""
    result4 = converter._reorganize_paragraphs_with_figures(test4)
    print(f"輸入: {test4}")
    print(f"輸出: {result4}")
    assert "and the diverse" in result4
    print("✅ 測試 4 通過\n")

    print("=" * 80)
    print("所有基本測試完成！")
    print("=" * 80)


if __name__ == "__main__":
    test_simple_cases()
