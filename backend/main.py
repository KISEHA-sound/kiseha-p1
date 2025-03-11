from fastapi import FastAPI
from pydantic import BaseModel
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from fastapi.middleware.cors import CORSMiddleware
import time

# FastAPI 앱 생성
app = FastAPI()

# CORS 설정 (React 프론트엔드와 연결)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:3000"], # React 프론트엔드 주소
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# FAISS 벡터DB 로드
vectorstore = FAISS.load_local("faiss_index", OpenAIEmbeddings(), allow_dangerous_deserialization=True)

# OpenAI LLM 설정
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.3)

# 요청 데이터 모델 정의
class QueryRequest(BaseModel):
    question: str

@app.post("/query")
async def query_law_ai(request: QueryRequest):
    start_time = time.time() # 시작 시간 측정

    query = request.question

    # FAISS에서 관련 법률 검색
    search_results = vectorstore.similarity_search(query, k=3)
    context = "\n\n".join([result.page_content for result in search_results])

    # LLM을 이용하여 답변 생성
    prompt = f"""
    당신은 법률 전문가입니다. 사용자의 질문을 분석하고, 관련 법률 조항을 참고하여 변호사처럼 답변해 주세요.

    ### 관련 법률 조항:
    {context}

    ### 사용자 질문:
    {query}

    ### 답변 예시:
    - 이 사건은 [법 조항]에 따라 [벌금 or 징역] 처벌을 받을 수 있습니다.

    - 법적 입증을 위해 [증거]를 준비해야 합니다.
    
    - 피해자와 합의할 경우 [법적 절차]를 따를 수 있습니다.

    ### 당신의 답변:
    """

    response = llm.invoke(prompt)

    end_time = time.time() # 끝난 시간 측정
    elapsed_time = round(end_time - start_time, 2) # 실행 시간 계산 (소수점 2자리)

    return {
        "answer": response.content, # AI 응답
        "elapsed_time": f"{elapsed_time}초" # 응답 시간  
    }