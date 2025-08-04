from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader("./17-ai-api/resume.pdf")
pages = loader.load_and_split()

print(f"총 페이지: {len(pages)}")
print(pages[1].page_content)