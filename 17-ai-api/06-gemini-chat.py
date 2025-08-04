import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()
genai.configure(api_key=os.environ.get('GEMINI_API_KEY'))

model = genai.GenerativeModel('gemini-2.5-flash')
chat = model.start_chat(history=[])

while True:
    user_input = input("You: ")
    if user_input.lower() in ['quit', 'exit', '종료']:
        break
    
    response = chat.send_message(user_input)
    print(f"AI: {response.text}")