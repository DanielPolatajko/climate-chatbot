# climate-chatbot

This project is a chatbot application designed to assist with the reading of climate risk and ESG related documentation. In particular, it is useful for learning more about frameworks and protocols such as TCFD, TNFD, EU Taxonomy and GHG Protocol.

## Getting Started

1) Get a HuggingFace API key
2) Make a local directory in the project root called `local_vector_store_hf`
3) Download the TCFD recommendations PDF from their website
4) Run `poetry run python -m climate_chatbot.vector_store <path> hf` with the path to the TCFD PDF to populate the vector store with the TCFD recommendations.
5) Run `poetry run python -m climate_chatbot.chatbot hf` to watch it answer a question about transition risk.
6) Get an OpenAI API key and repeat the above, replacing `hf` with `openai` (this will cost small amounts of money, but will be quicker and probably better)

## Things to do

* Blue/green deployment
* Configure AWS sso to enable both of us to deploy 
* Terraform - use multiple workspaces
* Git access token for terraform will expire approx end of september
* ec2 status checks pass before terraform completes
* Use commit hash for docker image tag in terraform. Will require input at command line