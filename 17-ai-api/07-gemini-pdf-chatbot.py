from dotenv import load_dotenv
import os
import google.generativeai as genai
import streamlit as st
import tempfile

load_dotenv()
API_KEY = os.environ.get('GEMINI_API_KEY') or os.environ.get('GOOGLE_API_KEY')

if not API_KEY:
    st.error("❌ GEMINI_API_KEY 또는 GOOGLE_API_KEY 환경변수가 설정되지 않았습니다.")
    st.stop()

genai.configure(api_key=API_KEY)

# PDF 파일을 Gemini에 업로드하는 함수
def upload_pdf_file(pdf_file):
    try:
        # 임시 파일로 저장
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(pdf_file.getvalue())
            tmp_file_path = tmp_file.name
        
        # Gemini에 파일 업로드
        uploaded_file = genai.upload_file(tmp_file_path)
        
        # 임시 파일 삭제
        os.unlink(tmp_file_path)
        
        return uploaded_file
    except Exception as e:
        st.error(f"업로드 오류: {str(e)}")
        return None

# 메시지 히스토리를 session_state로 관리
if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'pdf_file' not in st.session_state:
    st.session_state.pdf_file = None

if 'pdf_file_name' not in st.session_state:
    st.session_state.pdf_file_name = None

# 페이지 제목
st.header("📄 Gemini PDF 분석 챗봇")

# PDF 파일 선택
uploaded_file = st.file_uploader(
    "PDF 파일을 선택하세요", 
    type=['pdf'],
    help="분석하고 싶은 PDF 파일을 업로드하세요"
)

# PDF 파일 업로드 처리
if uploaded_file is not None and st.session_state.pdf_file is None:
    if st.button("PDF 파일 업로드"):
        with st.spinner("PDF 업로드 중..."):
            uploaded_pdf = upload_pdf_file(uploaded_file)
            if uploaded_pdf:
                st.session_state.pdf_file = uploaded_pdf
                st.session_state.pdf_file_name = uploaded_file.name
                st.success(f"✅ {uploaded_file.name} 업로드 완료!")
                st.rerun()

# 업로드된 PDF 정보 표시
if st.session_state.pdf_file:
    st.info(f"📄 업로드된 파일: {st.session_state.pdf_file_name}")
    if st.button("PDF 제거"):
        # Gemini에서 파일 삭제
        try:
            genai.delete_file(st.session_state.pdf_file.name)
        except:
            pass
        st.session_state.pdf_file = None
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

    try:
        # Gemini 모델 초기화
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        # 메시지 구성
        if st.session_state.pdf_file:
            # PDF 포함하여 질문
            system_prompt = "당신은 PDF 문서를 분석하고 설명하는 전문 어시스턴트입니다. PDF 내용을 정확하고 자세하게 분석하여 사용자의 질문에 답변해주세요."
            
            # PDF와 함께 메시지 전송
            response = model.generate_content([
                system_prompt,
                st.session_state.pdf_file,
                prompt
            ])
        else:
            # 일반 대화
            # 이전 대화 히스토리를 포함한 채팅
            chat_history = []
            for msg in st.session_state.messages[:-1]:  # 마지막 메시지 제외
                if msg["role"] == "user":
                    chat_history.append(f"사용자: {msg['content']}")
                else:
                    chat_history.append(f"어시스턴트: {msg['content']}")
            
            full_prompt = "당신은 도움이 되는 AI 어시스턴트입니다. 사용자의 질문에 정확하고 친절하게 답변해주세요.\n\n"
            if chat_history:
                full_prompt += "이전 대화:\n" + "\n".join(chat_history[-6:]) + "\n\n"  # 최근 6개만
            full_prompt += f"현재 질문: {prompt}"
            
            response = model.generate_content(full_prompt)
        
        # AI 답변 추출 및 표시
        assistant_message = response.text
        st.session_state.messages.append({"role": "assistant", "content": assistant_message})
        
        with st.chat_message("assistant"):
            st.write(assistant_message)
            
    except Exception as e:
        st.error(f"API 호출 오류: {str(e)}")

# 사이드바
with st.sidebar:
    st.header("상태")
    st.write(f"메시지: {len(st.session_state.messages)}개")
    
    if st.session_state.pdf_file:
        st.success("📄 PDF 업로드됨")
        st.write(f"파일명: {st.session_state.pdf_file_name}")
    else:
        st.info("📄 PDF 대기중")
    
    if st.button("대화 초기화"):
        st.session_state.messages = []
        if st.session_state.pdf_file:
            try:
                genai.delete_file(st.session_state.pdf_file.name)
            except:
                pass
        st.session_state.pdf_file = None
        st.session_state.pdf_file_name = None
        st.rerun()

    # Gemini 모델 정보
    st.divider()
    st.info("🤖 Gemini 2.5 Flash 사용 중")
    if st.session_state.pdf_file:
        st.success("📄 PDF 분석 모드")
    else:
        st.info("💬 일반 대화 모드")