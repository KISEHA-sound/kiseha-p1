from fastapi import FastAPI
from pydantic import BaseModel
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.memory import ConversationBufferMemory
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

# 대화 메모리 설정
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# 질문 키워드에 따라 법률 카테고리 매칭
law_categories = {
    "폭행": "형법",
    "상해": "형법",
    "사기": "형법",
    "절도": "형법",
    "이혼": "민법",
    "임대차": "민법",
    "채무": "민법",
    "계약": "민법",
    "상표권": "저작권법",
    "저작권": "저작권법",
    "노동": "근로기준법",
    "해고": "근로기준법",
    "산업재해": "근로기준법",
}

# 사용자의 질문에서 카테고리 판별
def get_law_category(query):
    for keyword, category in law_categories.items():
        if keyword in query:
            return category
    return "일반 법률"  # 기본값

# 요청 데이터 모델 정의
class QueryRequest(BaseModel):
    question: str

@app.post("/query")
async def query_law_ai(request: QueryRequest):
    start_time = time.time() # 시작 시간 측정

    query = request.question

    # 법률 검색 시 적용
    law_category = get_law_category(query)

    # FAISS에서 관련 법률 검색 (카테고리 기반 필터링)
    search_results = vectorstore.similarity_search(query, k=3, filter={"category": law_category})
    context = "\n\n".join([result.page_content for result in search_results])

    chat_history = memory.load_memory_variables({}).get("chat_history", [])

    # LLM을 이용하여 답변 생성
    prompt = f"""
    당신은 대한민국 법률 전문가이자 변호사입니다. 사용자의 법률 질문에 대해, 
    1. 정확한 법률 조항을 근거로 하고,  
    2. 법률적 해석을 덧붙이며,  
    3. 실제 변호사가 상담할 때처럼 이해하기 쉽게 설명하세요.

    ### 이전 대화 기록:
    {chat_history}

    ### 관련 법률 조항:
    {context}

    ### 사용자 질문:
    {query}

    ### 법률적 해석 및 조언:
    - 법 조항의 의미를 쉽게 풀어서 설명해 주세요.  
    - 이 사안에서 예상할 수 있는 법적 리스크와 대응 방법을 제시하세요.  
    - 피해자 또는 피의자의 입장에서 고려해야 할 사항을 알려 주세요.  
    - 변호사가 조언할 법적 절차나 대응 전략을 포함하세요. 

    ### 답변 형식 예시:
    "이 사건은 [법 조항]에 따라 [벌금 or 징역] 처벌을 받을 수 있습니다.  
    법적 입증을 위해 [증거]를 준비하는 것이 중요하며, 변호사 상담을 권장합니다."

    ### 당신의 볍률 상담 답변:
    """

    response = llm.invoke(prompt)

    # 대화 기록 업데이트 (새로운 질문과 답변 추가)
    memory.save_context({"input": query}, {"output": response.content})

    end_time = time.time() # 끝난 시간 측정
    elapsed_time = round(end_time - start_time, 2) # 실행 시간 계산 (소수점 2자리)

    return {
        "answer": response.content, # AI 응답
        "law_category": law_category,  # 적용된 법률 카테고리
        "elapsed_time": f"{elapsed_time}초" # 응답 시간  
    }