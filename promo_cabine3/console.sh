#!/bin/bash
cd "$(dirname "$0")"

if (( $EUID != 0 )); then
  docker-compose run cabine3 bash 
  exit
fi
docker-compose run -u 0 cabine3 bash 

