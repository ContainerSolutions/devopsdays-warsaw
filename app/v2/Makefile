IMG := gcr.io/devopsdays-warsaw-presentation/hello-world
TAG := v2
NAME := ${IMG}:${TAG}

buildpush: build push

run:
	@docker run --rm -it -p 4321:80 ${NAME}

main.go: ../v1/main.go
	sed 's/Version = "v1"/Version = "v2"/;s/ErrorRate float64 = 0.05/ErrorRate float64 = 0.5/' < ../v1/main.go > main.go

build: main.go
	@docker build -t ${NAME} .

push:
	@docker push ${NAME}

k8s.yaml:
	sed 's/Version = "v1"/Version = "v2"/;s/ErrorRate float64 = 0.05/ErrorRate float64 = 0.5/' < ../v1/main.go > main.go

deploy: k8s.yaml
	kubectl apply -f k8s.yaml
