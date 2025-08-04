from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

chat_model = ChatOpenAI(model="gpt-4o-mini")

content = "여름"

# invoke 방식으로 더 자세한 정보 확인
result = chat_model.invoke([HumanMessage(content=content + "에 대한 시를 써줘")])

print("=== 시 내용 ===")
print(result.content)

print("\n=== 메타데이터 ===")
print(f"모델: {result.response_metadata.get('model_name', 'gpt-4o-mini')}")
print(f"토큰 사용량: {result.response_metadata.get('token_usage', '정보 없음')}")
print(f"응답 ID: {result.id}")

print("\n=== 전체 응답 객체 ===")
print(f"타입: {type(result)}")