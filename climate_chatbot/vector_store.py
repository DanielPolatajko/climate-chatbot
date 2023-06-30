import os
import sys

from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceHubEmbeddings
from langchain.embeddings.openai import OpenAIEmbeddings
from climate_chatbot.config import config
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter, SpacyTextSplitter
import spacy


def add_document_to_vector_store(
    document_path: str, embedding_implementation: str, vector_store: str
) -> None:
    reader = PdfReader(document_path)
    page_texts = [page.extract_text() for page in reader.pages]
    text = "".join(page_texts)

    spacy.load('en_core_web_sm')

    text_splitter = SpacyTextSplitter(
        separator="\n",
        chunk_size=1000,
    )

    chunks = text_splitter.split_text(text)

    if embedding_implementation == "openai":
        embedding = OpenAIEmbeddings()
    else:
        embedding = HuggingFaceHubEmbeddings(
            repo_id=config.HUGGINGFACE_MODEL,
            task="feature-extraction",
            huggingfacehub_api_token=os.environ["HUGGING_FACE_PAT"],
        )
    Chroma.from_texts(texts=chunks, embedding=embedding, persist_directory=vector_store)
    print(f"All documents were processed and saved in {vector_store}.")


if __name__ == "__main__":
    doc_path = sys.argv[1]
    embedding_implementation = sys.argv[2]
    if embedding_implementation == "openai":
        vector_store = "local_vector_store_openai"
    elif embedding_implementation == "hf":
        vector_store = "local_vector_store_hf"
    else:
        raise ValueError("The second argument must be either 'openai' or 'hf'.")
    add_document_to_vector_store(doc_path, embedding_implementation, vector_store)
