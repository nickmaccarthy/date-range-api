IMAGE_NAME ?= service-api-exercise
IMAGE_TAG := latest 

build:
	docker build --platform linux/amd64 -t ${IMAGE_NAME}:${IMAGE_TAG} .

run: 
	docker run -p 5001:5001 -it ${IMAGE_NAME}:${IMAGE_TAG}