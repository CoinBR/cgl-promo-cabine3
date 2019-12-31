#!/bin/bash
cd "$(dirname "$0")"

if (( $EUID != 0 )); then
  docker-compose run node bash 
  exit
fi
docker-compose run -u 0 node bash 

