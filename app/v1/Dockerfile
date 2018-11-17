FROM golang:1.11 AS builder
WORKDIR /go/src/github.com/ContainerSolutions/docker-hello-world/
COPY main.go .
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o main .

FROM alpine:latest
EXPOSE 80
RUN apk --no-cache add ca-certificates
WORKDIR /root/
COPY --from=builder /go/src/github.com/ContainerSolutions/docker-hello-world/main .
CMD ["./main"]
