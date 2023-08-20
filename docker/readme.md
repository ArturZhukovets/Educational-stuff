## Docker / Docker-compose example project

### Многоэтапная сборка
Многоэтапная сборка в данном случае использовалась для компиляции type script в js.  
И для соединения статики воедино. Это хорошая практика, когда необходимо получить результат от некоторых промежуточных данных, например, получить бинарник из большой кодовой базы, а затем передать этот скомпилированный бинарник в приложение.
```dockerfile
# MULTY STAGE BUILD FRONTEND
# FIRST PART - INICIALIZE js, html, css
# SECOND PART - COPY RESULT ARTEFACTS FROM FIRST STAGE TO RESULT BUILD
FROM node:17 AS BUILD

WORKDIR /app
COPY ./todo-list/package.json ./package.json
RUN npm i
COPY ./todo-list ./

RUN npm run build


FROM nginx

COPY --from=BUILD ./app/dist/index.html /nginx/static/index.html
COPY --from=BUILD ./app/dist/static/css /nginx/static/
COPY --from=BUILD ./app/dist/static/js /nginx/static/
```

***
## Реализация сборки используя отдельные контейнеры
Изначально была создана сеть `network` и `volume`
```shell
docker volume create nginx_backend
docker network create nginx_backend
```
Далее каждый из созданных контейнеров будет подключаться к этой сети и volume  

После этого отдельно был поднят каждый из контейнеров и в результате `nginx` выступал в роли фронта-конфигуратора, который  
при запросе на эндпоинты выдавал статику пользователю либо проксировал запрос на backend если выполнялся `PUT` `POST` `DELETE` `GET` для получения / изменения данных.

```shell
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
```
***

## Docker compose сборка
При сборке используя docker-compose.yml Каждый из отдельных сервисов был описан в .yml файле.

+ При поднятии `docker compose up -d` по умолчанию инициализируется свой network. Для того чтобы использовать  
существующий необходимо указать `external: true` после определения имени.  
ВАЖНО! При указании данного флага сеть уже должна существовать.
+ Также по умолчанию создаётся новый volume. Для того чтобы использовать существующий, также указать флаг `external: true`
+ При поднятии определённого сервиса если важен порядок поднятия указывается ключ `depends_on`. Также можно указать дополнительно `condition: service_healthy`.  
В этом случае сервис будет запускаться ТОЛЬКО после выполненной и успешно завершенной проверки на `healthcheck` у контейнера от которого зависит данный сервис.
+ `healthcheck` - запускает проверку в виде теста для нужного сервиса. При проведении данного теста можно убедиться, что сервис успешно поднялся и отвечает на команды.
Дополнительно используются ключи в виде interval, timeout, retries.
+ ENV прокидываются либо используя `environments` либо `env_file`. 

```yaml
version: '3.0'

services:
  db:
    image: db   # postgresql
    container_name: nginx_database
    environment:
      POSTGRES_DB: nginx_app
      POSTGRES_USER: nginx_app
      POSTGRES_PASSWORD: nginx_app
    volumes:
      - backend_nginx:/var/lib/postgresql/data
    networks:
      - backend_nginx
    restart: always
    healthcheck:
      test: ["CMD-SHELL", "pg_isready", "-U", "nginx_app"]
      interval: 5s
      timeout: 5s
      retries: 3

  backend:
    image: backend
    container_name: backend
    env_file:
      - ./backend/.env
    networks:
      - backend_nginx
    depends_on:
      db:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "--fail", "localhost:8000/test"]
      interval: 3s
      timeout: 9s
      retries: 3

  nginx:
    image: nginx
    container_name: frontend
    ports:
      - "80:80"
    networks:
      - backend_nginx
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      db:
        condition: service_healthy
      backend:
        condition: service_healthy

volumes:
  backend_nginx:
    external: true


networks:
  backend_nginx:
    external: true
```


