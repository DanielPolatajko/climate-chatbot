import sys

import os

from langchain import PromptTemplate
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceHubEmbeddings

from climate_chatbot.config import config
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI, HuggingFaceHub
from langchain.chat_models import ChatOpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.schema import HumanMessage


def answer(prompt: str, llm_type: str, vector_store_name: str, k: int = 5) -> str:
    """From a question asked by the user, generate the answer based on the vectorstore.

    Args:
        prompt (str): Question asked by the user.
        vector_store_name (str): Vectorstore directory.

    Returns:
        str: Answer generated with the LLM
    """
    print(f"Start answering based on prompt: {prompt}.")
    if llm_type == "hf":
        embedding = HuggingFaceHubEmbeddings(
            repo_id=config.HUGGINGFACE_MODEL,
            task="feature-extraction",
            huggingfacehub_api_token=os.environ["HUGGING_FACE_PAT"],
        )
        llm = HuggingFaceHub(
            repo_id="google/flan-t5-xxl",
            model_kwargs={"temperature": 0.1, "max_length": 300},
            huggingfacehub_api_token=os.environ["HUGGING_FACE_PAT"],
        )
    elif llm_type == "openai":
        embedding = OpenAIEmbeddings()
        llm = ChatOpenAI(
            openai_api_key=os.environ["OPENAI_API_KEY"],
            model_name="gpt-3.5-turbo",
        )
    else:
        raise ValueError("Invalid LLM type.")
    vector_store = Chroma(
        persist_directory=vector_store_name, embedding_function=embedding
    )
    prompt_template = PromptTemplate(
        template=config.PROMPT_TEMPLATE.replace("{question}", prompt), input_variables=["context"]
    )
    doc_chain = load_qa_chain(
        llm=llm,
        chain_type="stuff",
        prompt=prompt_template,
    )

    qa = RetrievalQA(
        combine_documents_chain=doc_chain, retriever=vector_store.as_retriever(search_kwargs={"k": k})
    )

    intermediate_prompt_template = PromptTemplate(
        template=config.INTERMEDIATE_PROMPT_TEMPLATE, input_variables=["question"]
    )

    sample_answer = llm.generate(
        [[
            HumanMessage(content=intermediate_prompt_template.format(question=prompt))
        ]]
    ).generations[0][0].text

    result = qa({"query": sample_answer})

    answer = result["result"]
    print(f"The returned answer is: {answer}")
    print(f"Answering module over.")
    return answer


if __name__ == "__main__":
    llm_type = sys.argv[1]
    if llm_type == "hf":
        vector_store_name = "local_vector_store_hf"
    elif llm_type == "openai":
        vector_store_name = "local_vector_store_openai"
    else:
        raise ValueError("The first argument must be either 'openai' or 'hf'.")
    prompt = "What do I need to include in my TCFD report in the governance section?"
    answer(prompt, llm_type, vector_store_name)
