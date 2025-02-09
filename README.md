# stock-price-dashboard
This project uses yahoo finance API and processes data to be shown on a dashboard

Commands for reference:

Docker commands:
- build the docker image: docker build -t stock-price-dashboard .
- run the app: docker run stock-price-dashboard
- tag the image docker image tag stock-price-dashboard saikiran9620/stock-price-dashboard:latest
- docker push ssaikiran9620/stock-price-dashboard:latest

you can find the docker image here: https://hub.docker.com/repository/docker/ssaikiran9620/stock-price-dashboard/general

Docker Compose commands:
- start all services: docker compose up
- retrigger build and start all services: docker-compose up --build -d
- remove all containers and network config: docker-compose down --volumes --remove-orphans

Kafka Commands:
- to check the message from a consumer inside kafka docker container: 
    - docker exec -it stock-stream bash
    - kafka-console-consumer --bootstrap-server stock-stream:9092 --topic stock-prices --from-beginning