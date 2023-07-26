.PHONY: build-and-push
REGION = eu-west-2
REGISTRY_ID = 823043195714
IMAGE_NAME = climate_chatbot
IMAGE_TAG = latest # always overwrite

REPO_URL = $(REGISTRY_ID).dkr.ecr.$(REGION).amazonaws.com/$(IMAGE_NAME):$(IMAGE_TAG)

build-and-push:
	$(shell aws ecr get-login-password --region $(REGION) | docker login --username AWS --password-stdin $(REPO_URL))
	docker build -t $(IMAGE_NAME) .
	docker tag $(IMAGE_NAME):$(IMAGE_TAG) $(REPO_URL)
	docker push $(REPO_URL)
