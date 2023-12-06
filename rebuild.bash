docker rm api_ecs_monitor -f
docker build -t api_ecs_monitor .
docker run -it -dp 8000:8000 --name api_ecs_monitor -v $(pwd)/db.sqlite3:/app/db.sqlite3 api_ecs_monitor
docker logs -f api_ecs_monitor
