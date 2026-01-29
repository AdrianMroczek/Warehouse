#!/bin/bash

# This script shuts down the warehouse application.

PROJECT_ID="project-208103c2-25ca-4326-ae6"
CLUSTER_NAME="warehouse-cluster"
REGION="europe-central2"

gcloud container clusters get-credentials "$CLUSTER_NAME" --region "$REGION" --project "$PROJECT_ID" || { echo "Failed to get cluster credentials"; read -p "Press [Enter]"; exit 1; }

kubectl scale deployment warehouse-app --replicas=0

IS_PRESENT=$(kubectl get service warehouse-service --ignore-not-found -o name)
if [ -n "$IS_PRESENT" ]; then
  kubectl delete service warehouse-service
fi

read -p "Press [Enter] to confirm that the application has been shut down..."