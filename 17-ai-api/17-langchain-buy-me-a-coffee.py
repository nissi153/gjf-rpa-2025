# Streamlit Cloud 배포시에만 필요 (로컬 실행시 주석 처리)
# __import__('pysqlite3')
# import sys
# sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

# pip install streamlit_extra`s

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
import streamlit as st
import tempfile
import os
from streamlit_extras.buy_me_a_coffee import button

button(username="coding_gangsa", floating=True, width=221)

st.title("📄 ChatPDF")
st.write("PDF를 업로드하고 AI와 대화해보세요! ✨")

# 설정 섹션
with st.expander("⚙️ 설정 (선택사항)"):
    openai_key = st.text_input('OpenAI API Key (고급 답변용)', type="password", 
                              help="입력하지 않으면 무료 검색 모드로 작동합니다")

uploaded_file = st.file_uploader("📁 PDF 파일 선택", type=['pdf'])

def process_pdf(uploaded_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        loader = PyPDFLoader(tmp_file.name)
        pages = loader.load_and_split()
    os.unlink(tmp_file.name)
    return pages

if uploaded_file:
    with st.spinner('📄 PDF 처리 중...'):
        # PDF 처리 및 벡터 DB 생성
        pages = process_pdf(uploaded_file)
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=20)
        texts = text_splitter.split_documents(pages)
        
        # 무료 임베딩 사용 (HuggingFace)
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
        db = Chroma.from_documents(texts, embeddings)
        
    st.success(f"✅ PDF 처리 완료! ({len(texts)}개 문서 조각)")
    
    # 질문 섹션
    st.header("💬 PDF에게 질문해보세요!")
    question = st.text_input('궁금한 것을 물어보세요:', placeholder="예: 이 문서의 주요 내용은?")
    
    if st.button('🚀 질문하기', type="primary"):
        if question:
            with st.spinner('🤖 답변 생성 중...'):
                if openai_key:
                    # OpenAI API 사용 (고급 모드)
                    try:
                        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, api_key=openai_key)
                        qa_chain = RetrievalQA.from_chain_type(llm, retriever=db.as_retriever())
                        result = qa_chain.run(question)
                        st.markdown(f"### 🤖 AI 답변:\n{result}")
                    except Exception as e:
                        st.error(f"❌ OpenAI API 오류: {e}")
                        st.info("🔍 무료 검색 모드로 전환합니다...")
                        docs = db.similarity_search(question, k=3)
                        for i, doc in enumerate(docs, 1):
                            with st.expander(f"📄 관련 문서 {i}"):
                                st.write(doc.page_content)
                else:
                    # 무료 검색 모드
                    st.info("🆓 무료 검색 모드 (OpenAI API 키 없음)")
                    docs = db.similarity_search(question, k=3)
                    for i, doc in enumerate(docs, 1):
                        with st.expander(f"📄 관련 문서 {i}"):
                            st.write(doc.page_content)
        else:
            st.warning("⚠️ 질문을 입력해주세요!")
else:
    st.info("👆 PDF 파일을 업로드하면 시작됩니다!")
    st.markdown("""
    ### 🌟 기능 소개:
    - 📄 **PDF 분석**: 문서를 AI가 이해할 수 있는 형태로 변환
    - 🆓 **무료 모드**: OpenAI API 없이도 문서 검색 가능
    - 🤖 **고급 모드**: OpenAI API로 정확한 답변 생성
    - ☕ **후원**: 오른쪽 하단 버튼으로 개발자 응원하기
    """)