#!/bin/sh
kubectl apply -f storage/pvc.yaml

kubectl apply -f rabbitmq/rabbitmq-deployment.yaml
kubectl apply -f rabbitmq/rabbitmq-service.yaml

kubectl apply -f rest/rest-deployment.yaml

kubectl apply -f cassandra/cassandra-deployment.yaml
kubectl apply -f cassandra/cassandra-service.yaml
# kubectl apply -f https://k8s.io/examples/application/cassandra/cassandra-service.yaml
# kubectl apply -f https://k8s.io/examples/application/cassandra/cassandra-statefulset.yaml

kubectl apply -f logs/logs-deployment.yaml

sleep 120

kubectl apply -f worker/worker-deployment.yaml
kubectl expose deployment rest-server --name=rest-service \
        --type=LoadBalancer --port 8080 --target-port 5000







