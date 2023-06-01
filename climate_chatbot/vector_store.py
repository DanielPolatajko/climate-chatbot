import sys

from langchain.vectorstores import Chroma
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.embeddings.openai import OpenAIEmbeddings
from climate_chatbot.config import config
from PyPDF2 import PdfReader

def add_document_to_vector_store(document_path: str, embedding_implementation: str):
    reader = PdfReader(document_path)
    page_texts = [page.extract_text() for page in reader.pages]
    text = " ".join(page_texts)

    from langchain.text_splitter import CharacterTextSplitter
    text_splitter = CharacterTextSplitter(
        separator='\n',
        chunk_size=1300,
        chunk_overlap=0
    )

    chunks = text_splitter.split_text(text)

    if embedding_implementation == "openai":
        embedding = OpenAIEmbeddings()
    else:
        embedding = HuggingFaceEmbeddings(model_name=config.HUGGINGFACE_MODEL)
    Chroma.from_texts(
      texts=chunks,
      embedding=embedding,
      persist_directory=config.VECTOR_STORE
    )
    print(f"All documents were processed and saved in {config.VECTOR_STORE}.")


if __name__ == "__main__":
    doc_path = sys.argv[1]
    add_document_to_vector_store(doc_path, "openai")