#!/bin/bash

docker volume create vol-db
docker build -t xxyears-db -f Dockerfile.db .
docker run --volume vol-db:/app/instance xxyears-db
