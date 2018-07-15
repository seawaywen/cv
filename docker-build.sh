#!/bin/bash

#docker container rm cv_nginx cv_web
docker rmi memodir.azurecr.io/cv_web:0.1 memodir.azurecr.io/cv_nginx:0.1
docker rmi cv_web cv_nginx --force
docker-compose up -f docker-compose-prod.yml --build --no-start
docker tag cv_web:latest memodir.azurecr.io/cv_web:0.1
docker tag cv_nginx:latest memodir.azurecr.io/cv_nginx:0.1
docker push memodir.azurecr.io/cv_nginx:0.1
docker push memodir.azurecr.io/cv_web:0.1
kubectl delete -f kubernetes/app/app-deploy.yaml
kubectl delete -f kubernetes/app/nginx-deploy.yaml
kubectl apply -f kubernetes/app/app-deploy.yaml
kubectl apply -f kubernetes/app/nginx-deploy.yaml


