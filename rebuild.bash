docker rm api_ecs_monitor -f
docker build -t api_ecs_monitor .
docker run -it -dp 8000:8000 --name api_ecs_monitor api_ecs_monitor
docker logs -f api_ecs_monitor
