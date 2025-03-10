from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-3.5-turbo")
response = llm.invoke("LangChain이란 무엇인가요?")
print(response)
