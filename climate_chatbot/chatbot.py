import sys

import os

from langchain import PromptTemplate
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceHubEmbeddings

from climate_chatbot.config import config
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI, HuggingFaceHub
from langchain.chains.question_answering import load_qa_chain

def answer(
    prompt: str,
    llm_type: str,
) -> str:
    """From a question asked by the user, generate the answer based on the vectorstore.

    Args:
        prompt (str): Question asked by the user.
        persist_directory (str): Vectorstore directory.

    Returns:
        str: Answer generated with the LLM
    """
    print(f"Start answering based on prompt: {prompt}.")
    if llm_type == "hf":
        embedding = HuggingFaceHubEmbeddings(
            repo_id="sentence-transformers/all-mpnet-base-v2",
            task="feature-extraction",
            huggingfacehub_api_token=os.environ['HUGGING_FACE_PAT'],
        )
        llm = HuggingFaceHub(
            repo_id=config.HUGGINGFACE_MODEL,
            model_kwargs={"temperature": 0, "max_tokens": 300},
            huggingfacehub_api_token=os.environ['HUGGING_FACE_PAT'],
        )
    elif llm_type == "openai":
        embedding = OpenAIEmbeddings()
        llm = OpenAI(
            openai_api_key=os.environ['OPENAI_API_KEY'],
            model_name="text-davinci-003",
            temperature=0,
            max_tokens=300,
        )
    else:
        raise ValueError("Invalid LLM type.")
    vectorstore = Chroma(persist_directory=config.VECTOR_STORE, embedding_function=embedding)
    prompt_template = PromptTemplate(template=config.PROMPT_TEMPLATE, input_variables=["context", "question"])
    doc_chain = load_qa_chain(
        llm=llm,
        chain_type="stuff",
        prompt=prompt_template,
    )

    qa = RetrievalQA(
        combine_documents_chain=doc_chain,
        retriever=vectorstore.as_retriever()
    )
    result = qa({"query": prompt})
    answer = result["result"]
    print(f"The returned answer is: {answer}")
    print(f"Answering module over.")
    return answer


if __name__ == "__main__":
    llm_type = sys.argv[1]
    if llm_type == "hf":
        os.environ['VECTOR_STORE'] = "local_vector_store_hf"
    elif llm_type == "openai":
        os.environ['VECTOR_STORE'] = "local_vector_store_openai"
    else:
        raise ValueError("The first argument must be either 'openai' or 'hf'.")
    prompt = "What are some examples of policy-related transition risks?"
    answer(prompt, llm_type)