from dotenv import load_dotenv
load_dotenv()
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain.chains import RetrievalQA

#Loader
loader = PyPDFLoader("./17-ai-api/resume.pdf")
pages = loader.load_and_split()

#Split
text_splitter = RecursiveCharacterTextSplitter(
    # Set a really small chunk size, just to show.
    chunk_size = 300,
    chunk_overlap  = 20,
    length_function = len,
    is_separator_regex = False,
)
texts = text_splitter.split_documents(pages)

#Embedding
embeddings_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

# load it into Chroma
db = Chroma.from_documents(texts, embeddings_model)

#Question
question = "직무 관련 경험은?"

try:
    # OpenAI 사용 시도
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    retriver_from_llm = MultiQueryRetriever.from_llm(
        retriever=db.as_retriever(), llm=llm
    )
    docs = retriver_from_llm.get_relevant_documents(query=question)
    print(f"✅ MultiQuery로 찾은 문서 수: {len(docs)}")
    
    # RetrievalQA로 답변 생성
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=db.as_retriever()
    )
    result = qa_chain.run(question)
    print(f"🤖 답변: {result}")
    
except Exception as e:
    print(f"❌ OpenAI API 오류: {e}")
    print("🔍 기본 유사도 검색 사용")
    
    # 무료 대안: 기본 유사도 검색
    docs = db.similarity_search(question, k=3)
    print(f"📄 유사도 검색으로 찾은 문서 수: {len(docs)}")
    
    for i, doc in enumerate(docs):
        print(f"\n📋 문서 {i+1}:")
        print(doc.page_content[:200] + "...")

print("\n✅ 검색 완료!")