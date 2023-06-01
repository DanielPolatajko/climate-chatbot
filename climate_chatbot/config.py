from pydantic import BaseModel, Field


class Config(BaseModel):

    HUGGINGFACE_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
    HUGGINGFACE_MODEL_ENDPOINT = f"https://api-inference.huggingface.co/models/{HUGGINGFACE_MODEL}"
    VECTOR_STORE = Field(default="local_vector_store", env="VECTOR_STORE")

    PROMPT_TEMPLATE = """You are a Bot assistant answering any questions about documents.
    You are given a question and a set of documents.
    If the user's question requires you to provide specific information from the documents, give your answer based only on the examples provided below. DON'T generate an answer that is NOT written in the provided examples.
    If you don't find the answer to the user's question with the examples provided to you below, answer that you didn't find the answer in the documentation and propose him to rephrase his query with more details.
    Use bullet points if you have to make a list, only if necessary.

    QUESTION: {question}

    DOCUMENTS:
    =========
    {context}
    =========
    Finish by proposing your help for anything else.
    """

    NUMBER_CANDIDATE_ANSWERS = 5


config = Config()