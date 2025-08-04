from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.environ.get('OPENAI_API_KEY')

client = OpenAI(api_key=api_key)

print("=== OpenAI 채팅봇 ===")
print("종료하려면 'quit' 또는 'exit'를 입력하세요.")
print("-" * 30)

while True:
    # 사용자 입력
    user_input = input("You: ")
    
    # 종료 조건
    if user_input.lower() in ['quit', 'exit', '종료']:
        print("채팅을 종료합니다.")
        break
    
    try:
        # OpenAI API 호출
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": user_input}],
            max_tokens=200
        )
        
        # AI 응답 출력
        ai_response = response.choices[0].message.content
        print(f"AI: {ai_response}")
        print()  # 빈 줄로 구분
        
    except Exception as e:
        print(f"오류 발생: {e}")
        print()