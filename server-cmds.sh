#!/usr/bin/env bash

export IMAGE=$1
export DOCKER_USER=$2
export DOCKER_PASS=$3

echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
docker image prune
docker-compose -f docker-compose.yml up --detach
echo "success"
