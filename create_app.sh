#!/bin/bash

docker build -t xxyears:app .
docker run -d -p 5000:5000 --volume vol-db:/app/instance xxyears:app
