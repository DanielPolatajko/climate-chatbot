# climate-chatbot

This project is a chatbot application designed to assist with the reading of climate risk and ESG related documentation. In particular, it is useful for learning more about frameworks and protocols such as TCFD, TNFD, EU Taxonomy and GHG Protocol.

## Getting Started

1) Get an OpenAI API key
2) Make a local directory in the project root called `local_vector_store`
3) Download the TCFD recommendations PDF from their website
4) Run `poetry run python -m climate_chatbot.vector_store` with the path to the TCFD PDF to populate the vector store with the TCFD recommendations.
5) Run `poetry run python -m climate_chatbot.chatbot` to watch it answer a question about transition risk.