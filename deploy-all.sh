#!/bin/sh
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.0.4/deploy/static/provider/cloud/deploy.yaml
# kubectl apply -f webFrontend/ingress.yaml
kubectl apply -f rest/ingress.yaml

kubectl apply -f storage/pvc.yaml

kubectl apply -f rabbitmq/rabbitmq-deployment.yaml
kubectl apply -f rabbitmq/rabbitmq-service.yaml

# kubectl apply -f webFrontend/website-deployment.yaml
# kubectl apply -f webFrontend/website-service.yaml
kubectl apply -f rest/rest-deployment.yaml
kubectl apply -f rest/rest-service.yaml

kubectl apply -f cassandra/cassandra-deployment.yaml
kubectl apply -f cassandra/cassandra-service.yaml
# kubectl apply -f https://k8s.io/examples/application/cassandra/cassandra-service.yaml
# kubectl apply -f https://k8s.io/examples/application/cassandra/cassandra-statefulset.yaml

kubectl apply -f logs/logs-deployment.yaml

# sleep 180

# kubectl apply -f worker/worker-deployment.yaml






# kubectl port-forward --address 0.0.0.0 service/flask 5000:5000 &
# kubectl port-forward --address 0.0.0.0 service/redis 6379:6379 &
# kubectl port-forward --address 0.0.0.0 service/rabbitmq 5672:5672 &
# kubectl port-forward --address 0.0.0.0 service/cassandra 9042:9042
