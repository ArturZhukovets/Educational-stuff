#!/bin/bash
# database
sudo docker run --rm -d \
--name nginx_database \
--net=backend_nginx \
-v backend_nginx:/var/lib/postgresql/data \
-e POSTGRES_DB=nginx_app \
-e POSTGRES_USER=nginx_app \
-e POSTGRES_PASSWORD=nginx_app \
db

# backend
sudo docker run --rm -d \
--name backend \
--net=backend_nginx \
--env-file ./backend/.env \
backend

# nginx
sudo docker run --rm -d \
--name frontend \
-p 80:80 \
--net=backend_nginx \
-v $(pwd)/nginx/nginx.conf:/etc/nginx/nginx.conf:ro \
nginx
