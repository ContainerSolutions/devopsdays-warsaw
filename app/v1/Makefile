IMG := gcr.io/devopsdays-warsaw-presentation/hello-world
TAG := v1
NAME := ${IMG}:${TAG}

run: build
	docker run --rm -it -p 4321:80 ${NAME}

build:
	docker build -t ${NAME} .

push:
	docker push ${NAME}

deploy:
	kubectl apply -f replicaset.yaml
	kubectl apply -f service.yaml
	kubectl apply -f istio.yaml
