# ----------------------------------------------------------------------------- start
docker-compose up

docker ps --all
docker exec -it notionsnapshot /bin/bash

# ----------------------------------------------------------------------------- stop
docker-compose down

docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)
docker rmi $(docker images -q)

yes | docker container prune
yes | docker image prune
yes | docker volume prune
yes | docker network prune
yes | docker system prune

docker ps --all
docker images
docker system df
docker volume ls
docker network ls
