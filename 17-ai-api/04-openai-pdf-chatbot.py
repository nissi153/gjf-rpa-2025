from dotenv import load_dotenv
import os
from openai import OpenAI
import streamlit as st

load_dotenv()
API_KEY = os.environ['OPENAI_API_KEY']

client = OpenAI(api_key=API_KEY)

# PDF 파일을 OpenAI에 업로드하는 함수
def upload_pdf_file(pdf_file):
    try:
        file_response = client.files.create(
            file=pdf_file,
            purpose="assistants"
        )
        return file_response.id
    except Exception as e:
        st.error(f"업로드 오류: {str(e)}")
        return None

# 메시지 히스토리를 session_state로 관리
if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'pdf_file_id' not in st.session_state:
    st.session_state.pdf_file_id = None

if 'pdf_file_name' not in st.session_state:
    st.session_state.pdf_file_name = None

# 페이지 제목
st.header("📄 PDF 분석 챗봇")

# PDF 파일 선택
uploaded_file = st.file_uploader(
    "PDF 파일을 선택하세요", 
    type=['pdf'],
    help="분석하고 싶은 PDF 파일을 업로드하세요"
)

# PDF 파일 업로드 처리
if uploaded_file is not None and st.session_state.pdf_file_id is None:
    if st.button("PDF 파일 업로드"):
        with st.spinner("PDF 업로드 중..."):
            file_id = upload_pdf_file(uploaded_file)
            if file_id:
                st.session_state.pdf_file_id = file_id
                st.session_state.pdf_file_name = uploaded_file.name
                st.success(f"✅ {uploaded_file.name} 업로드 완료!")
                st.rerun()

# 업로드된 PDF 정보 표시
if st.session_state.pdf_file_id:
    st.info(f"📄 업로드된 파일: {st.session_state.pdf_file_name}")
    if st.button("PDF 제거"):
        st.session_state.pdf_file_id = None
        st.session_state.pdf_file_name = None
        st.rerun()

# 기존 메시지들을 UI에 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# 입력창
prompt = st.chat_input("PDF에 대해 질문하거나 일반적인 질문을 해보세요!")
if prompt:
    # 사용자 메시지 추가 및 표시
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.write(prompt)

    # 입력 메시지 구성
    if st.session_state.pdf_file_id:
        # PDF 포함
        input_messages = [
            {"role": "system", "content": "당신은 PDF 문서를 분석하고 설명하는 전문 어시스턴트입니다. PDF 내용을 정확하고 자세하게 분석하여 사용자의 질문에 답변해주세요."},
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": prompt},
                    {"type": "input_file", "file_id": st.session_state.pdf_file_id}
                ]
            }
        ]
    else:
        # 일반 대화
        input_messages = [
            {"role": "system", "content": "당신은 도움이 되는 AI 어시스턴트입니다. 사용자의 질문에 정확하고 친절하게 답변해주세요."}
        ] + st.session_state.messages

    try:
        # OpenAI Responses API 호출
        response = client.responses.create(
            model="gpt-4o-mini",
            input=input_messages
        )
        
        # AI 답변 추출 및 표시
        assistant_message = response.output[0].content[0].text
        st.session_state.messages.append({"role": "assistant", "content": assistant_message})
        
        with st.chat_message("assistant"):
            st.write(assistant_message)
            
    except Exception as e:
        st.error(f"API 호출 오류: {str(e)}")
        
        # Chat Completions API 폴백
        try:
            fallback_messages = [
                {"role": "system", "content": "당신은 도움이 되는 AI 어시스턴트입니다. 사용자의 질문에 정확하고 친절하게 답변해주세요."}
            ] + st.session_state.messages
            
            fallback_response = client.chat.completions.create(
                model="gpt-4o",
                messages=fallback_messages,
                temperature=0.7
            )
            
            assistant_message = fallback_response.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": assistant_message})
            
            with st.chat_message("assistant"):
                st.write(assistant_message)
                st.info("💡 일반 대화 모드로 응답")
                
        except Exception as fallback_error:
            st.error(f"폴백 API도 실패: {str(fallback_error)}")

# 사이드바
with st.sidebar:
    st.header("상태")
    st.write(f"메시지: {len(st.session_state.messages)}개")
    
    if st.session_state.pdf_file_id:
        st.success("📄 PDF 업로드됨")
        st.write(f"ID: {st.session_state.pdf_file_id[:20]}...")
    else:
        st.info("📄 PDF 대기중")
    
    if st.button("대화 초기화"):
        st.session_state.messages = []
        st.session_state.pdf_file_id = None
        st.rerun()
