import json
import requests
import os

from langchain import PromptTemplate
from langchain.embeddings import OpenAIEmbeddings

from climate_chatbot.config import config
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
def query_model(payload):
    data = json.dumps(payload)
    headers = {"Authorization": f"Bearer {os.environ['HUGGING_FACE_PAT']}"}
    response = requests.request("POST", config.HUGGING_FACE_MODEL_ENDPOINT, headers=headers, data=data)
    return json.loads(response.content.decode("utf-8"))

def answer(
    prompt: str
) -> str:
    """From a question asked by the user, generate the answer based on the vectorstore.

    Args:
        prompt (str): Question asked by the user.
        persist_directory (str): Vectorstore directory.

    Returns:
        str: Answer generated with the LLM
    """
    print(f"Start answering based on prompt: {prompt}.")
    embedding = OpenAIEmbeddings()
    vectorstore = Chroma(persist_directory=config.VECTOR_STORE, embedding_function=embedding)
    prompt_template = PromptTemplate(template=config.PROMPT_TEMPLATE, input_variables=["context", "question"])
    doc_chain = load_qa_chain(
        llm=OpenAI(
            openai_api_key=os.environ['OPENAI_API_KEY'],
            model_name="text-davinci-003",
            temperature=0,
            max_tokens=300,
        ),
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
    prompt = "What are the 4 main types of transition risk?"
    answer(prompt)