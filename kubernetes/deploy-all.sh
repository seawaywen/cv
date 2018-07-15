#!/bin/bash

kubectl apply -f db/deploy.yaml

kubectl apply -f app/nginx-deploy.yaml
kubectl apply -f app/app-deploy.yaml
