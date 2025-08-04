from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# pip install langchain_text_splitters

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

print(texts[0])