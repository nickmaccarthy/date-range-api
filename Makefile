IMAGE_NAME ?= service-api-exercise
IMAGE_TAG := latest 

build:
	docker build --platform linux/amd64 -t ${IMAGE_NAME}:${IMAGE_TAG} .

run: 
	docker compose up --build
