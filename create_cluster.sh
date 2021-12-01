gcloud config set compute/zone us-central1-c
gcloud container clusters create audioid --machine-type=e2-standard-4 --num-nodes=3

gcloud container clusters get-credentials audioid --zone us-central1-c

gcloud filestore instances create audioid \
  --zone=us-central1-c \
  --tier=standard \
  --file-share=name="audiofs",capacity=1TB \
  --network=name="default"
