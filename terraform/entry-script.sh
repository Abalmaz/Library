#!/bin/bash

# Install Docker
sudo yum update -y
sudo amazon-linux-extras install docker
sudo groupadd docker
sudo usermod -aG docker $USER
sudo systemctl start docker

# Install docker-compose
sudo curl -L https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
