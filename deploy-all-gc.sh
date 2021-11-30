#!/bin/sh
kubectl expose deployment rest --name=rest-service 
        --type=LoadBalancer --port 80 --target-port 5000

kubectl apply -f storage/pvc.yaml

kubectl apply -f rabbitmq/rabbitmq-deployment.yaml
kubectl apply -f rabbitmq/rabbitmq-service.yaml

kubectl apply -f rest/rest-deployment.yaml
# kubectl apply -f rest/rest-service.yaml

kubectl apply -f cassandra/cassandra-deployment.yaml
kubectl apply -f cassandra/cassandra-service.yaml
# kubectl apply -f https://k8s.io/examples/application/cassandra/cassandra-service.yaml
# kubectl apply -f https://k8s.io/examples/application/cassandra/cassandra-statefulset.yaml

kubectl apply -f logs/logs-deployment.yaml

sleep 180

kubectl apply -f worker/worker-deployment.yaml







