from dotenv import load_dotenv
load_dotenv()

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
# 새로운 패키지 사용 (경고 해결)
try:
    from langchain_huggingface import HuggingFaceEmbeddings
    print("✅ 새로운 langchain-huggingface 패키지를 사용합니다")
except ImportError:
    from langchain_community.embeddings import HuggingFaceEmbeddings
    print("⚠️  기존 패키지를 사용합니다 (deprecated)")

from langchain_community.vectorstores import Chroma, FAISS
import os
import time

def create_vector_database(pdf_path="./17-ai-api/resume.pdf", persist_directory="./chroma_db", use_faiss=False):
    """PDF 문서를 벡터 데이터베이스에 저장하는 함수"""
    
    try:
        # PDF Loader
        print(f"📄 PDF 로딩 중: {pdf_path}")
        loader = PyPDFLoader(pdf_path)
        pages = loader.load_and_split()
        print(f"✅ {len(pages)} 페이지 로드 완료")

        # Text Split (더 가벼운 설정)
        print("🔪 텍스트 분할 중...")
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=200,  # 300 -> 200으로 축소
            chunk_overlap=10,  # 20 -> 10으로 축소
            length_function=len,
            is_separator_regex=False,
        )
        texts = text_splitter.split_documents(pages)
        print(f"✅ {len(texts)} 개의 텍스트 청크 생성")

        # Embeddings (가벼운 모델 사용)
        print("🧠 임베딩 모델 로딩 중...")
        embeddings_model = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",  # 더 가벼운 모델
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
        print("✅ 임베딩 모델 로드 완료")

        # 벡터 저장소 생성
        if use_faiss:
            print("💾 FAISS 벡터 저장소 생성 중...")
            start_time = time.time()
            db = FAISS.from_documents(texts, embeddings_model)
            end_time = time.time()
            print(f"✅ FAISS 벡터 저장소 생성 완료! 소요시간: {end_time - start_time:.2f}초")
            
            # FAISS 저장 (선택적)
            faiss_path = persist_directory.replace("chroma_db", "faiss_db")
            db.save_local(faiss_path)
            print(f"✅ FAISS 인덱스 저장 완료: {faiss_path}")
            
        else:
            print("💾 ChromaDB 벡터 저장소 생성 중...")
            
            # ChromaDB 안전한 생성 방법
            try:
                # 방법 1: 메모리에서 먼저 생성
                print("🔄 메모리에서 ChromaDB 생성 중...")
                start_time = time.time()
                db_temp = Chroma.from_documents(texts, embeddings_model)
                end_time = time.time()
                print(f"✅ 메모리 ChromaDB 생성 완료! 소요시간: {end_time - start_time:.2f}초")
                
                # 방법 2: 영구 저장소로 복사
                print(f"💾 영구 저장소로 복사 중: {persist_directory}")
                if os.path.exists(persist_directory):
                    import shutil
                    shutil.rmtree(persist_directory)
                    print("🗑️  기존 데이터베이스 삭제")
                
                start_time = time.time()
                db = Chroma.from_documents(
                    texts, 
                    embeddings_model,
                    persist_directory=persist_directory
                )
                end_time = time.time()
                print(f"✅ ChromaDB 영구 저장 완료! 소요시간: {end_time - start_time:.2f}초")
                
            except Exception as chroma_error:
                print(f"❌ ChromaDB 생성 실패: {chroma_error}")
                print("🔄 FAISS로 대체...")
                start_time = time.time()
                db = FAISS.from_documents(texts, embeddings_model)
                end_time = time.time()
                print(f"✅ FAISS 대체 생성 완료! 소요시간: {end_time - start_time:.2f}초")
        
        print(f"✅ 벡터 데이터베이스 생성 완료")
        return db, embeddings_model
        
    except Exception as e:
        print(f"❌ 전체 오류 발생: {e}")
        import traceback
        traceback.print_exc()
        return None, None

def search_documents(db, query, k=3):
    """벡터 데이터베이스에서 유사한 문서 검색"""
    if db is None:
        print("❌ 데이터베이스가 없습니다")
        return []
    
    try:
        print(f"🔍 검색 중: '{query}'")
        start_time = time.time()
        results = db.similarity_search(query, k=k)
        end_time = time.time()
        
        print(f"📋 {len(results)} 개의 관련 문서 발견! 소요시간: {end_time - start_time:.2f}초")
        for i, doc in enumerate(results, 1):
            print(f"\n--- 결과 {i} ---")
            print(f"내용: {doc.page_content[:150]}...")
            if hasattr(doc, 'metadata') and doc.metadata:
                print(f"메타데이터: {doc.metadata}")
        
        return results
    except Exception as e:
        print(f"❌ 검색 오류: {e}")
        return []

def load_existing_database(persist_directory="./chroma_db", use_faiss=False):
    """기존 벡터 데이터베이스 로드"""
    
    if use_faiss:
        faiss_path = persist_directory.replace("chroma_db", "faiss_db")
        if not os.path.exists(faiss_path):
            print(f"❌ FAISS 인덱스가 존재하지 않습니다: {faiss_path}")
            return None, None
        
        try:
            embeddings_model = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2",
                model_kwargs={'device': 'cpu'},
                encode_kwargs={'normalize_embeddings': True}
            )
            db = FAISS.load_local(faiss_path, embeddings_model, allow_dangerous_deserialization=True)
            print(f"✅ 기존 FAISS 인덱스 로드 완료: {faiss_path}")
            return db, embeddings_model
        except Exception as e:
            print(f"❌ FAISS 로드 오류: {e}")
            return None, None
    
    else:
        if not os.path.exists(persist_directory):
            print(f"❌ ChromaDB가 존재하지 않습니다: {persist_directory}")
            return None, None
        
        try:
            embeddings_model = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2",
                model_kwargs={'device': 'cpu'},
                encode_kwargs={'normalize_embeddings': True}
            )
            db = Chroma(persist_directory=persist_directory, embedding_function=embeddings_model)
            print(f"✅ 기존 ChromaDB 로드 완료: {persist_directory}")
            return db, embeddings_model
        except Exception as e:
            print(f"❌ ChromaDB 로드 오류: {e}")
            return None, None

# 메인 실행
if __name__ == "__main__":
    print("🚀 PDF 벡터 데이터베이스 시스템 시작")
    print("="*60)
    
    # FAISS 우선 시도 (더 안정적)
    print("📋 FAISS 방식으로 시도...")
    db, embeddings = create_vector_database(use_faiss=True)
    
    if db is None:
        print("🔄 ChromaDB 방식으로 재시도...")
        db, embeddings = create_vector_database(use_faiss=False)
    
    if db is not None:
        # 샘플 검색
        sample_queries = [
            "경력",
            "기술 스택", 
            "프로젝트",
            "교육"
        ]
        
        print("\n" + "="*60)
        print("🔍 샘플 검색 테스트")
        print("="*60)
        
        for query in sample_queries[:2]:  # 처음 2개만 테스트
            print(f"\n{'='*40}")
            search_documents(db, query, k=2)
            
        print("\n🎉 모든 작업 완료!")
    
    else:
        print("❌ 벡터 데이터베이스 생성에 실패했습니다.")