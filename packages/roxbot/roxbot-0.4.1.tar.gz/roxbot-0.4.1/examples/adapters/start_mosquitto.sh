#!/bin/bash

docker run -d -p 1883:1883 --restart unless-stopped \
    --name mosquitto \
    registry.gitlab.com/roxautomation/images/mosquitto:latest
