import os

from dotenv import dotenv_values
import langchain
from langchain import PromptTemplate
from langchain.chains import ConversationalRetrievalChain
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

# Open AI
llm_type = "openai"
vector_store_name = "local_vector_store_openai"
# Hugging Face
# llm_type = "hf"
# vector_store_name = "local_vector_store_hf"


k = 5
temperature = 0.0

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
vector_store = Chroma(persist_directory=vector_store_name, embedding_function=embedding)
prompt_template = PromptTemplate(
    template=config.PROMPT_TEMPLATE,
    input_variables=["context", "question"],
)

retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": k})

qa = ConversationalRetrievalChain.from_llm(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
)

chat_history = []


def answer(prompt: str) -> str:
    """From a question asked by the user, generate the answer based on the vectorstore.

    Args:
        prompt (str): Question asked by the user.

    Returns:
        str: Answer generated with the LLM
    """
    print(f"Start answering based on prompt: {prompt}.")
    print(f"Chat history: {chat_history}")

    # intermediate_prompt_template = PromptTemplate(
    #     template=config.INTERMEDIATE_PROMPT_TEMPLATE, input_variables=["question"]
    # )
    # llm_result = llm.generate(
    #     [[HumanMessage(content=intermediate_prompt_template.format(question=prompt))]]
    # )
    # sample_answer = llm_result.generations[0][0].text

    result = qa({"question": prompt, "chat_history": chat_history})

    answer = result["answer"]

    chat_history.append((prompt, answer))

    print(f"The returned answer is: {answer}")
    print(f"Answering module over.")
    return answer


if __name__ == "__main__":
    question = "What do I need to include in my TCFD report in the governance section?"
    answer(question)
