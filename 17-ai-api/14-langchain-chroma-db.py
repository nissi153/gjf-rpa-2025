from dotenv import load_dotenv
load_dotenv()
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# pip install langchain_huggingface

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

print( db )