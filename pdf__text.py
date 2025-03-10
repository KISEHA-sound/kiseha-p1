import fitz  # PyMuPDF - text로 변환

def extract_text_from_pdf(pdf_path):
    """PDF에서 텍스트를 추출하는 함수"""
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text("text") + "\n"
    return text

# 예제 실행
pdf_text = extract_text_from_pdf("pdf/형법.pdf")
print(pdf_text[:1000])  # 일부 출력 확인

__all__=["pdf_text"]