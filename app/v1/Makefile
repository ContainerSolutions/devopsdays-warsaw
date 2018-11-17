IMG := gcr.io/devopsdays-warsaw-presentation/hello-world
TAG := v1
NAME := ${IMG}:${TAG}

buildpush: build push

run:
	@docker run --rm -it -p 4321:80 ${NAME}

build:
	@docker build -t ${NAME} .

push:
	@docker push ${NAME}:${TAG}

deploy:
	kubectl apply -f k8s.yaml
