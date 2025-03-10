from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
import fitz  # PyMuPDF

# PDF에서 텍스트 추출하는 함수
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text("text") + "\n"
    return text

# 저장할 법률 목록 (PDF 파일명 리스트)
law_files = ["pdf/형법.pdf", "pdf/저작권법.pdf", "pdf/민법.pdf", "pdf/상법.pdf"]

# 모든 법률의 텍스트를 저장할 리스트
all_texts = []

# 각 법률 PDF에서 텍스트 추출
for law_file in law_files:
    text = extract_text_from_pdf(law_file)
    all_texts.append(text)

# 텍스트를 청크로 나누기
text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
documents = text_splitter.create_documents(all_texts)

# FAISS 벡터DB에 저장
vectorstore = FAISS.from_documents(documents, OpenAIEmbeddings())

# 벡터DB 저장 완료
vectorstore.save_local("faiss_index")
print("모든 법률 데이터가 FAISS 벡터DB에 저장 완료!")