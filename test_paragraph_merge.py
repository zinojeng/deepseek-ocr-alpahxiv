"""
測試段落合併功能
"""

from src.utils.markdown_converter import MarkdownConverter


def test_paragraph_merge():
    """測試被圖片說明中斷的段落能否正確合併"""

    converter = MarkdownConverter()

    # 模擬您提供的例子
    test_text = """It implicates that even slight damages in the glomerulus and renal tubule can lead to an increase in the UACR, and various mechanisms contribute to the exacerbation of albuminuria in different proportions. Its pathophysiology is likely modulated by the haemodynamics of HF and the<center>FIGURE 2 Pathophysiology of albuminuria under heart failure. (A) The components of pressure that consist of net filtration pressure. The net filtration pressure is determined by the balance of the pressure components shown as coloured arrows. (B) Pathophysiological burdens that cause glomerular damage and tubular damage resulting in albuminuria. GBM, glomerular basement membrane; P afferent, afferent artery pressure; P efferent, efferent artery pressure; RAS, renin-angiotensin system.</center>diverse underlying comorbidities present in the patient, prompting the consideration of albuminuria as a marker for cardiorenal interaction under HF."""

    print("原始文字:")
    print("=" * 80)
    print(test_text)
    print("\n" + "=" * 80 + "\n")

    # 測試重組功能
    reorganized = converter._reorganize_paragraphs_with_figures(test_text)

    print("重組後的文字:")
    print("=" * 80)
    print(reorganized)
    print("\n" + "=" * 80 + "\n")

    # 測試完整的 Markdown 轉換
    enhanced = converter._enhance_figure_markup(test_text)

    print("完整 Markdown 輸出:")
    print("=" * 80)
    print(enhanced)
    print("\n" + "=" * 80 + "\n")

    # 驗證結果
    # 1. 檢查段落是否合併
    assert "HF and the diverse" in reorganized, \
        "段落應該被合併在一起"

    # 2. 檢查圖片說明是否移到段落後面
    # 找到第一個完整段落的位置
    first_para_end = reorganized.find("under HF.")
    figure_pos = reorganized.find("<center>FIGURE")

    assert first_para_end < figure_pos, \
        "圖片說明應該在完整段落之後"

    print("✅ 所有測試通過！")
    print("\n段落成功合併，圖片說明已移至段落後方。")


if __name__ == "__main__":
    test_paragraph_merge()
