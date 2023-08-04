import os

from dotenv import dotenv_values
import langchain
from langchain import PromptTemplate
from langchain.chains import ConversationalRetrievalChain
from langchain.chains.conversational_retrieval.base import (
    BaseConversationalRetrievalChain,
)
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceHubEmbeddings
from langchain.llms import HuggingFaceHub
from langchain.vectorstores import Chroma

from config import config

# TODO: move all this into app.py & manage the qa object there
_ENV = {
    **dotenv_values(".env.dev"),  # load dev env variables
    **os.environ,  # override loaded values with environment variables
}

langchain.debug = bool(_ENV.get("LANGCHAIN_DEBUG", False))


def load_qa(
    llm_type="openai",
    k=5,
    temperature=0,
) -> BaseConversationalRetrievalChain:
    if llm_type == "openai":
        vector_store_name = "local_vector_store_openai"
    elif llm_type == "hf":
        vector_store_name = "local_vector_store_hf"
    else:
        raise ValueError("Invalid LLM type.")

    if llm_type == "hf":
        llm = HuggingFaceHub(
            repo_id="google/flan-t5-xxl",
            model_kwargs={"temperature": 0.0, "max_length": 300},
            huggingfacehub_api_token=_ENV["HUGGING_FACE_PAT"],
        )
    elif llm_type == "openai":
        llm = ChatOpenAI(
            openai_api_key=_ENV["OPENAI_API_KEY"],
            model_name="gpt-3.5-turbo",
            temperature=temperature,
        )
    else:
        raise ValueError("Invalid LLM type.")

    if vector_store_name == "local_vector_store_openai":
        embedding = OpenAIEmbeddings(openai_api_key=_ENV["OPENAI_API_KEY"])
    elif vector_store_name == "local_vector_store_hf":
        embedding = HuggingFaceHubEmbeddings(
            repo_id=config.HUGGINGFACE_MODEL,
            task="feature-extraction",
            huggingfacehub_api_token=os.environ["HUGGING_FACE_PAT"],
        )
    else:
        raise ValueError("Invalid vector store name.")
    vector_store = Chroma(
        persist_directory=vector_store_name, embedding_function=embedding
    )

    prompt_template = PromptTemplate(
        template=config.PROMPT_TEMPLATE,
        input_variables=["context", "question"],
    )

    retriever = vector_store.as_retriever(
        search_type="similarity", search_kwargs={"k": k}
    )

    return ConversationalRetrievalChain.from_llm(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        combine_docs_chain_kwargs={"prompt": prompt_template},
    )
