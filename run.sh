#!/bin/bash

. env.sh

if [ -z "$(docker ps -aq --filter name=ma-at-volumes)" ]; then
    docker create --name ma-at-volumes -v /var/ma_at/ alpine /bin/sh
fi

docker kill --signal INT ma-at-app
docker stop -t 10 ma-at-app
docker rm -fv ma-at-app

docker run -d --name ma-at-app \
    --restart always \
    --volumes-from ma-at-volumes \
    --volumes-from swarm-data \
    -e "DATA_FILE=/var/ma_at/ma_at.json" \
    -e "DISCORD_TOKEN=${DISCORD_TOKEN}" \
    -e "STEAM_TOKEN=${STEAM_TOKEN}" \
    -e "ARK_SERVER_ID=${ARK_SERVER_ID}" \
    -e "ARK_SERVER_ADDR=${ARK_SERVER_ADDR}" \
    -e "ARK_ALERTS_CHAN_ID=${ARK_ALERTS_CHAN_ID}" \
    -e "MA_AT_DOCKER_HOST=${MA_AT_DOCKER_HOST}" \
    -e "GOOGLE_USER=${GOOGLE_USER}" \
    -e "GOOGLE_PASSWORD=${GOOGLE_PASSWORD}" \
    -e "POKEMAP_DOMAIN=${POKEMAP_DOMAIN}" \
    ma_at
