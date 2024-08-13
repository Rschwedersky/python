export DOMAIN=hub.smarthis.com.br

docker pull registry.gitlab.com/hub-smarthis/portal:manager
docker pull registry.gitlab.com/hub-smarthis/portal:nginx

docker stack deploy manager -c docker-compose-prod.yml
