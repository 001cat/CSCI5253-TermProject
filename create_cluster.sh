gcloud config set compute/zone us-central1-c
gcloud container clusters create audioid
# kubectl get nodes

gcloud container clusters get-credentials audioid --zone us-central1-c