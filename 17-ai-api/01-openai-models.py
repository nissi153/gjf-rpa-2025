from openai import OpenAI
from dotenv import load_dotenv
import os

# pip install openai

load_dotenv()

api_key = os.environ.get('OPENAI_API_KEY')

client = OpenAI(api_key=api_key)

# 사용 가능한 모델 목록 확인
try:
    models = client.models.list()
    print("사용 가능한 모델들:")
    for model in models.data:
        # if 'gpt' in model.id:
        print(f"- {model.id}")
except Exception as e:
    print(f"모델 목록 조회 실패: {e}")