#!/bin/bash

kubectl apply -f db/all-secret.yaml

kubectl apply -f db/persistent-volume-file.yaml

