from dotenv import load_dotenv
load_dotenv()
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
import streamlit as st
import tempfile
import os
# streamlit run 16-langchain-pdf-chatbot.py
st.title(":글씨가_쓰여진_페이지: ChatPDF")
st.write("PDF를 업로드하고 질문해보세요!")
uploaded_file = st.file_uploader("PDF 파일 선택", type="pdf")
def process_pdf(uploaded_file):
    import tempfile
    import os
    try:
        tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        tmp_file.write(uploaded_file.getvalue())
        tmp_file.close()
        st.write(f"임시 파일 생성: {tmp_file.name}")
        loader = PyPDFLoader(tmp_file.name)
        st.write("PyPDFLoader 생성 완료")
        pages = loader.load_and_split()
        st.write(f"페이지 수: {len(pages)}")
        return pages
    except Exception as e:
        st.error(f"PDF 파싱 오류: {e}")
        return None
    finally:
        try:
            os.unlink(tmp_file.name)
            st.write("임시 파일 삭제 완료")
        except Exception as e:
            st.warning(f"임시 파일 삭제 오류: {e}")
if uploaded_file:
    with st.spinner('PDF 처리 중...'):
        # PDF 처리 및 벡터 DB 생성
        pages = process_pdf(uploaded_file)
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=20)
        texts = text_splitter.split_documents(pages)
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
        db = Chroma.from_documents(texts, embeddings)
    st.success(f":흰색_확인_표시: PDF 처리 완료! ({len(texts)}개 문서 조각)")
    # 질문 입력
    question = st.text_input(':말풍선: PDF에 대해 질문하세요:')
    if st.button(':로켓: 질문하기', type="primary"):
        if question:
            with st.spinner('답변 생성 중...'):
                try:
                    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
                    qa_chain = RetrievalQA.from_chain_type(llm, retriever=db.as_retriever())
                    result = qa_chain.run(question)
                    st.markdown(f"### :로봇_얼굴: 답변:\n{result}")
                except Exception as e:
                    st.error(f":x: OpenAI API 오류: {e}")
                    st.info(":돋보기: 관련 문서 검색 결과:")
                    docs = db.similarity_search(question, k=3)
                    for i, doc in enumerate(docs, 1):
                        with st.expander(f":글씨가_쓰여진_페이지: 문서 {i}"):
                            st.write(doc.page_content)
        else:
            st.warning(":경고: 질문을 입력해주세요!")
else:
    st.info(":위를_가리키는_손_모양_2: PDF 파일을 업로드하면 시작됩니다!")