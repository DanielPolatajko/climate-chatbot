REGION = eu-west-2
REGISTRY_ID = 823043195714
IMAGE_NAME = climate-chatbot-repo
IMAGE_TAG = latest # always overwrite

REPO_URL = $(REGISTRY_ID).dkr.ecr.$(REGION).amazonaws.com/$(IMAGE_NAME):$(IMAGE_TAG)

.PHONY: run
build-and-run:
	docker build -t $(IMAGE_NAME) .
	docker run -p 8501:8501 --env-file .env.dev -v $(shell pwd):/app $(IMAGE_NAME)

.PHONY: build-and-push
build-and-push:
	$(shell aws ecr get-login-password --region $(REGION) | docker login --username AWS --password-stdin $(REPO_URL))
	docker build -t $(IMAGE_NAME) .
	docker tag $(IMAGE_NAME):$(IMAGE_TAG) $(REPO_URL)
	docker push $(REPO_URL)

.PHONY: deploy-infra
deploy-infra:
	terraform -chdir=terraform fmt
	terraform -chdir=terraform validate
	terraform -chdir=terraform apply

.PHONY: destroy-infra
destroy-infra:
	terraform -chdir=terraform destroy

.PHONY: vector-store-openai
vector-store-openai:
	poetry run python scripts/vector_store.py FINAL-2017-TCFD-Report-11052018.pdf openai

.PHONY: vector-store-hf
vector-store-hf:
	poetry run python scripts/vector_store.py FINAL-2017-TCFD-Report-11052018.pdf hf