import os
import sys

from dotenv import dotenv_values
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import HuggingFaceHubEmbeddings
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma

from climate_chatbot.config import config

# TODO: move this into scripts/ and change some of the deps to dev deps
_ENV = {
    **dotenv_values(".env.dev"),  # load dev env variables
    **os.environ,  # override loaded values with environment variables
}


def add_document_to_vector_store(
    document_path: str, embedding_implementation: str, vector_store: str
) -> None:
    loader = PyPDFLoader(document_path)
    pages = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,
        chunk_overlap=200,
    )
    docs = text_splitter.split_documents(pages)

    if embedding_implementation == "openai":
        embedding = OpenAIEmbeddings(openai_api_key=_ENV["OPENAI_API_KEY"])
    else:
        embedding = HuggingFaceHubEmbeddings(
            repo_id=config.HUGGINGFACE_MODEL,
            task="feature-extraction",
            huggingfacehub_api_token=_ENV["HUGGING_FACE_PAT"],
        )
    Chroma.from_documents(
        documents=docs, embedding=embedding, persist_directory=vector_store
    )
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
