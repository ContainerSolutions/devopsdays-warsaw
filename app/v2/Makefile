IMG := gcr.io/devopsdays-warsaw-presentation/hello-world
TAG := v2
NAME := ${IMG}:${TAG}

main.go: ../v1/main.go
	sed 's/Version = "v1"/Version = "v2"/;s/ErrorRate float64 = 0.10/ErrorRate float64 = 0.5/' < ../v1/main.go > main.go

Dockerfile: ../v1/Dockerfile
	cp ../v1/Dockerfile .

build: main.go Dockerfile
	@docker build -t ${NAME} .

push:
	@docker push ${NAME}

replicaset.yaml:
	sed 's/version: v1/version: v2/;s/hello-world:v1/hello-world:v2/' < ../v1/replicaset.yaml > replicaset.yaml

deploy_5_percent: replicaset.yaml
	kubectl apply -f replicaset.yaml
	kubectl apply -f istio-try-5-percent.yaml

check:
	watch ../check_status.py v1 v2

abort: replicaset.yaml
	kubectl apply -f ../v1/istio.yaml
	kubectl delete -f replicaset.yaml
