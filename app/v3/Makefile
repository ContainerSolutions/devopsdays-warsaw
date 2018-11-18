IMG := gcr.io/devopsdays-warsaw-presentation/hello-world
TAG := v3
NAME := ${IMG}:${TAG}

main.go: ../v1/main.go
	sed 's/Version = "v1"/Version = "v2"/;s/ErrorRate float64 = 0.10/ErrorRate float64 = 0.01/' < ../v1/main.go > main.go

Dockerfile: ../v1/Dockerfile
	cp ../v1/Dockerfile .

build: main.go Dockerfile
	@docker build -t ${NAME} .

push:
	@docker push ${NAME}

replicaset.yaml:
	sed 's/version: v1/version: v3/;s/hello-world:v1/hello-world:v3/;s/hello-world-v1/hello-world-v3/' < ../v1/replicaset.yaml > replicaset.yaml

deploy_5_percent: replicaset.yaml
	kubectl apply -f replicaset.yaml
	kubectl apply -f istio-try-5-percent.yaml

deploy_50_percent: replicaset.yaml
	kubectl apply -f istio-try-50-percent.yaml

deploy_100_percent: replicaset.yaml
	kubectl apply -f istio-100-percent.yaml
	kubectl delete -f ../v1/replicaset.yaml

check:
	watch ../check_status.py v1 v3
