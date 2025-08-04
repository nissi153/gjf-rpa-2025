import google.generativeai as genai
from dotenv import load_dotenv
import os

# pip install google-generativeai 

load_dotenv()
genai.configure(api_key=os.environ.get('GEMINI_API_KEY'))

model = genai.GenerativeModel('gemini-2.5-flash')
response = model.generate_content("안녕하세요! Gemini API 테스트입니다.")

print(response.text)