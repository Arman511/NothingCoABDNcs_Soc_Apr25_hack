REPOSITORY_OWNER=arman511
IMAGE_NAME=nothingcoabdncs_soc_apr25_hack
TAG=latest

build:
	docker build -t $(REPOSITORY_OWNER)/$(IMAGE_NAME):$(TAG) .

push: build
	docker push $(REPOSITORY_OWNER)/$(IMAGE_NAME):$(TAG)

all: build push
