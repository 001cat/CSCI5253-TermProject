gcloud config set compute/zone us-central1-c
gcloud container clusters create audioid
# kubectl get nodes

gcloud container clusters get-credentials audioid --zone us-central1-c


gcloud filestore instances create audioid \
  --zone=us-central1-c \
  --tier=standard \
  --file-share=name="audiofs",capacity=1TB \
  --network=name="default"

FILESTORE_IP=`gcloud filestore instances describe audioid \
    --zone us-central1-c --format="value(networks.ipAddresses[0])"`