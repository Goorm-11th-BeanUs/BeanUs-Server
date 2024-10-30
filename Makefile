IMAGE_NAME = coffee-garbage-server
TAG = latest

build:
	docker build -t $(IMAGE_NAME):$(TAG) .

run:
	docker run -it --rm -p 8080:8080 $(IMAGE_NAME):$(TAG) /bin/bash