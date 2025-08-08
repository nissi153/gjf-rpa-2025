from dotenv import load_dotenv
load_dotenv()
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma, FAISS
# 새로운 패키지 사용 (경고 해결)
try:
    from langchain_huggingface import HuggingFaceEmbeddings
except ImportError:
    from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
import streamlit as st
import tempfile
import os
import time
from streamlit_extras.buy_me_a_coffee import button

# Buy Me a Coffee 버튼 추가
button(username="coding_gangsa", floating=True, width=221)

st.title("📄 ChatPDF")
st.write("PDF를 업로드하고 AI와 대화해보세요! ✨")

# 설정 섹션
with st.expander("⚙️ 설정 (선택사항)"):
    openai_key = st.text_input('OpenAI API Key (고급 답변용)', type="password", 
                              help="입력하지 않으면 무료 검색 모드로 작동합니다")
    
    vector_store_type = st.selectbox(
        "벡터 저장소 선택:",
        ["FAISS (빠름, 권장)", "ChromaDB (영구저장)"],
        index=0
    )
    
    embedding_model = st.selectbox(
        "임베딩 모델 선택:",
        [
            "sentence-transformers/all-MiniLM-L6-v2 (빠름, 권장)",
            "sentence-transformers/all-mpnet-base-v2 (정확함)"
        ],
        index=0
    )
    
    chunk_size = st.slider("청크 크기", 100, 500, 200)
    chunk_overlap = st.slider("청크 겹침", 0, 50, 10)

uploaded_file = st.file_uploader("📁 PDF 파일 선택", type=['pdf'])

@st.cache_data
def process_pdf(uploaded_file):
    """PDF 파일을 처리하여 텍스트 추출"""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        loader = PyPDFLoader(tmp_file.name)
        pages = loader.load_and_split()
    os.unlink(tmp_file.name)  # 임시 파일 삭제
    return pages

def create_embeddings_model(model_choice):
    """임베딩 모델 생성"""
    if "MiniLM" in model_choice:
        model_name = "sentence-transformers/all-MiniLM-L6-v2"
    else:
        model_name = "sentence-transformers/all-mpnet-base-v2"
    
    return HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )

def create_vector_store(texts, embeddings, store_type):
    """안정적인 벡터 저장소 생성"""
    try:
        if "FAISS" in store_type:
            # FAISS 사용 (빠르고 안정적)
            with st.spinner('🚀 FAISS 벡터 저장소 생성 중...'):
                start_time = time.time()
                db = FAISS.from_documents(texts, embeddings)
                end_time = time.time()
                st.success(f"✅ FAISS 생성 완료! ({end_time - start_time:.2f}초)")
                return db
        else:
            # ChromaDB 사용 (영구 저장)
            with st.spinner('💾 ChromaDB 벡터 저장소 생성 중...'):
                try:
                    start_time = time.time()
                    # 메모리에서 먼저 생성
                    db = Chroma.from_documents(texts, embeddings)
                    end_time = time.time()
                    st.success(f"✅ ChromaDB 생성 완료! ({end_time - start_time:.2f}초)")
                    return db
                except Exception as chroma_error:
                    st.warning(f"⚠️ ChromaDB 실패: {str(chroma_error)[:100]}...")
                    st.info("🔄 FAISS로 대체 생성 중...")
                    start_time = time.time()
                    db = FAISS.from_documents(texts, embeddings)
                    end_time = time.time()
                    st.success(f"✅ FAISS 대체 생성 완료! ({end_time - start_time:.2f}초)")
                    return db
                    
    except Exception as e:
        st.error(f"❌ 벡터 저장소 생성 실패: {e}")
        return None

if uploaded_file:
    # PDF 처리
    with st.spinner('📄 PDF 처리 중...'):
        pages = process_pdf(uploaded_file)
        
        # 텍스트 분할
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, 
            chunk_overlap=chunk_overlap,
            length_function=len,
            is_separator_regex=False
        )
        texts = text_splitter.split_documents(pages)
        
        st.info(f"📊 PDF 처리 완료: {len(pages)} 페이지 → {len(texts)} 개 청크")
    
    # 임베딩 모델 로드
    with st.spinner('🧠 임베딩 모델 로딩 중...'):
        embeddings = create_embeddings_model(embedding_model)
        st.success("✅ 임베딩 모델 로드 완료!")
    
    # 벡터 저장소 생성
    db = create_vector_store(texts, embeddings, vector_store_type)
    
    if db is not None:
        st.success(f"🎉 모든 설정 완료! ({len(texts)}개 문서 조각)")
        
        # 질문 섹션
        st.header("💬 PDF에게 질문해보세요!")
        question = st.text_input('궁금한 것을 물어보세요:', placeholder="예: 이 문서의 주요 내용은?")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            ask_button = st.button('🚀 질문하기', type="primary", use_container_width=True)
        
        with col2:
            search_only = st.button('🔍 검색만', use_container_width=True)
        
        if ask_button and question:
            with st.spinner('🤖 AI 답변 생성 중...'):
                if openai_key:
                    # OpenAI API 사용 (고급 모드)
                    try:
                        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, api_key=openai_key)
                        qa_chain = RetrievalQA.from_chain_type(
                            llm, 
                            retriever=db.as_retriever(search_kwargs={"k": 3})
                        )
                        result = qa_chain.run(question)
                        
                        st.markdown("### 🤖 AI 답변:")
                        st.markdown(result)
                        
                        # 참고 문서 표시
                        with st.expander("📚 참고한 문서들"):
                            docs = db.similarity_search(question, k=3)
                            for i, doc in enumerate(docs, 1):
                                st.markdown(f"**📄 문서 {i}:**")
                                st.text(doc.page_content[:300] + "...")
                                st.divider()
                                
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
        
        elif search_only and question:
            with st.spinner('🔍 문서 검색 중...'):
                docs = db.similarity_search(question, k=5)
                st.markdown("### 🔍 검색 결과:")
                
                for i, doc in enumerate(docs, 1):
                    with st.expander(f"📄 관련 문서 {i}", expanded=i<=2):
                        st.write(doc.page_content)
                        if hasattr(doc, 'metadata') and doc.metadata:
                            st.caption(f"출처: {doc.metadata}")
        
        elif (ask_button or search_only) and not question:
            st.warning("⚠️ 질문을 입력해주세요!")
            
        # 샘플 질문 제공
        st.markdown("### 💡 샘플 질문:")
        sample_questions = [
            "이 문서의 주요 내용을 요약해주세요",
            "핵심 키워드나 개념은 무엇인가요?",
            "중요한 날짜나 숫자가 있나요?",
            "결론이나 요점은 무엇인가요?"
        ]
        
        for i, sample in enumerate(sample_questions):
            if st.button(f"📝 {sample}", key=f"sample_{i}"):
                st.text_input('💬 PDF에 대해 질문하세요:', value=sample, key="auto_question")
    
    else:
        st.error("❌ 벡터 저장소 생성에 실패했습니다. 다른 설정을 시도해보세요.")

else:
    st.info("👆 PDF 파일을 업로드하면 시작됩니다!")
    
    # 사용법 안내
    with st.expander("📖 사용법 안내"):
        st.markdown("""
        **1단계:** PDF 파일 업로드
        - 설정에서 벡터 저장소와 임베딩 모델 선택
        - FAISS (빠름) 또는 ChromaDB (영구저장) 선택
        
        **2단계:** 질문 입력
        - 자연어로 질문 작성
        - 샘플 질문 버튼 활용
        
        **3단계:** 답변 확인
        - 🚀 질문하기: AI가 답변 생성 (OpenAI API 필요)
        - 🔍 검색만: 관련 문서만 표시 (무료)
        
        **모드:**
        - 🆓 **무료 모드**: OpenAI API 없이도 문서 검색 가능
        - 🤖 **고급 모드**: OpenAI API로 정확한 답변 생성
        
        **팁:**
        - 청크 크기가 작을수록 더 정확한 검색
        - FAISS가 더 빠르고 안정적
        - MiniLM 모델이 더 빠름
        - ☕ 오른쪽 하단 버튼으로 개발자 응원하기
        """)
    
    st.markdown("""
    ### 🌟 기능 소개:
    - 📄 **PDF 분석**: 문서를 AI가 이해할 수 있는 형태로 변환
    - 🆓 **무료 모드**: OpenAI API 없이도 문서 검색 가능
    - 🤖 **고급 모드**: OpenAI API로 정확한 답변 생성
    - ⚙️ **고급 설정**: 벡터 저장소, 임베딩 모델, 청크 크기 조정
    - ☕ **후원**: 오른쪽 하단 버튼으로 개발자 응원하기
    """) 