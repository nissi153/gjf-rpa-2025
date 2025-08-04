from dotenv import load_dotenv
load_dotenv()

# 최신 방식 - Warning 없음
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

chat_model = ChatOpenAI()
result = chat_model.invoke([HumanMessage(content="hi")])
print(result.content)