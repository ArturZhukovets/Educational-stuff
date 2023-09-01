



1. Создаем сокет
`sudo vim /etc/systemd/system/gunicorn.socket`
Внутри файла сокета прописываются следующие параметры
```
[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn.sock     # section to define the socket location

[Install]
WantedBy=sockets.target     # [Install] section to make sure the socket is created at the right time
```
2. Создаём gunicorn сервис
```sudo vim /etc/systemd/system/gunicorn.service```
Внутри сервиса указываются следующие параметры:
```
[Unit]
Description=gunicorn daemon   # Описание
Requires=gunicorn.socket      # Указываем зависимость от файла-сокета
After=network.target          # Tell the init system to only start this after the networking target has been reached
```
3. Указываем следующий параметр `[Service]`
```
[Service]
User=gvensye
Group=www-data
WorkingDirectory=/home/gvensye/PycharmProjects/Educational-stuff/django_server_linux  # Рабочая директория проекта
ExecStart=/home/gvensye/.cache/pypoetry/virtualenvs/knowladge-worm-TBvfdQBi-py3.10/bin/gunicorn \    # Путь к гуникорну связывается с сокетом
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/gunicorn.sock \
          configuration.wsgi:application
          
[Install]
WantedBy=multi-user.target
```

По сути этот сервис будет сейчас слушать не порт, а сокет, созданный до этого.
4. Далее можно запустить и активировать Gunicorn socket. Эта команда создаст сокет файл в /run/gunicorn.sock в момент запуска и при загрузке системы.  
Как только появится соединение с этим сокетом - systemd автоматически запустит gunicorn.service, чтобы обрабатывать данный сокет.  
```zsh
sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket
# Created symlink /etc/systemd/system/sockets.target.wants/gunicorn.socket → /etc/systemd/system/gunicorn.socket.
```
5. Проверяем файл сокета
```zsh
sudo systemctl status gunicorn.socket
```
Получается теперь созданный конфиг сокета, после запуска создал файл сокета. Он запущен и слушает подключения к нему подобно порту на ip  (:8000)

Также можно проверить существует ли сейчас сам файл данного сокета физически: 
```zsh
file /run/gunicorn.sock
```
6. \* Проверять журнал данного сокета можно следующей командой
```zsh
sudo journalctl -u gunicorn.socket
```
На данном этапе созданы gunicorn.socket и gunicorn.service. По сути мы подключаемся к сокету, а обслуживает данный сокет созданный сервис (который в свою очередь слушает Джанго wsgi).
Как только появилось подключение к сокету - сервис начал работу. Пока подключения к сокету нет - сервис спит.

#### Тестирование активации сокета
В данный момент когда сокет только запущен (`sudo systemctl enable gunicorn.socket`), но никто ещё не подключался к нему - сокет будет деактивирован.
Проверить это можно прописав: 
```zsh
sudo systemctl status gunicorn.socket
```
```output
Output
○ gunicorn.service - gunicorn daemon
     Loaded: loaded (/etc/systemd/system/gunicorn.service; disabled; vendor preset: enabled)
     Active: inactive (dead)
TriggeredBy: ● gunicorn.socket
```
Чтобы посмотреть как работает механизм активации сокета можно, например, отправить запрос используя curl:
```zsh
curl --unix-socket /run/gunicorn.sock localhost
```
В этом примере запрос отправляется на локально поднятый сокет.

В консоли должен отобразиться респонс от localhost. Значит сокет активирован и gunicorn обслуживает соединение.
В этом можно убедится, ещё раз чекнув статус
```zsh
sudo systemctl status gunicorn
```

#### Socket reload
Если при попытке подключения возникли ошибки или проблемы. Первым делом необходимо чекнуть файл `/etc/systemd/system/gunicorn.service`  
После изменений в данном файле необходимо перезагрузить daemon, для перезагрузки данных в файле сервиса.  
Сделать это можно введя:
```zsh
sudo systemctl daemon-reload
sudo systemctl restart gunicorn
```

### Настройка Nginx
Теперь gunicorn слушает сокет и на него можно даже локально отправлять запросы, используя `curl --unix-socket /run/gunicorn.sock localhost`  
Но как достучаться до сервера по http и Интернет?  
Для этого необходимо поднять nginx.  
Для начала создаём файл c конфигом в sites-available. Nginx по умолчанию слушает только sites-enable. А список всех доступных проектов можно зранить в sites-available.
```zsh
sudo nano /etc/nginx/sites-available/myproject
```
Внутри данного файла прописывается конфиг настройки сервера. Подробно здесь конфиг описываться не будет. Только то, что нужно для работы.
```text
server {
    listen 80;
    server_name 0.0.0.0;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /home/gvensye/PycharmProjects/Educational-stuff/django_server_linux;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}
```
1. Указываем, что слушаем 80 порт (listen 80;)
2. Указываем IP или доменное имя сервера (server_name 0.0.0.0)
3. Указываем, что мы игнорируем любые проблемы с `finding a favicon` (location = /favicon.ico { access_log off; log_not_found off; })
4. Указываем, что все url, начинающиеся со /static/ искать по указанному пути (location /static/)
5. Указываем, что любые другие запросы относящиеся к этой location обрабатывает `proxy_params` - файл включенный по умолчанию самим Nginx (include proxy_params;)
6. Указываем путь proxy к созданному ранее сокет файлу. (proxy_pass `http://unix:/run/gunicorn.sock;`)

Дальше необходимо сделать следующее:
+ sudo ln -s /etc/nginx/sites-available/myproject /etc/nginx/sites-enabled - Создаём линку, чтобы nginx слушал конфиг
+ sudo nginx -t   - проверяем синтаксис конфига
+ sudo systemctl restart nginx 
+ sudo ufw allow 'Nginx Full'  - Даёт доступ firewall для Nginx

После этого можно пробовать соединяться с сервером по 80 порту.

### Commands

При обновлении Джанго приложения необходимо перезапустить gunicorn
```zsh
sudo systemctl restart gunicorn
```
Если изменили сокет или служебные файлы Gunicorn, необходимо перезагрузить демон и перезапустить процесс:
```zsh
sudo systemctl daemon-reload
sudo systemctl restart gunicorn.socket gunicorn.service
```

При изменении конфига nginx, тестируем конфиг + рестарт nginx:
```zsh
sudo nginx -t && sudo systemctl restart nginx
```

Выключить gunicorn и gunicorn socket (Достаточно просто выключить сам socket т.к service зависит от сокета)
```zsh
sudo systemctl stop gunicorn # Выключит только service, но при повторном подключении через браузер - service опять начнёт свою работу
sudo systemctl stop gunicorn.socket 
```

Запустить gunicorn socket
```zsh
sudo systemctl start gunicorn.socket
```


### Troubleshooting Nginx + Full article
https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-22-04#troubleshooting-nginx-and-gunicorn

***

# Настройка Docker + gunicorn + nginx

### Docker + Docker-compose

> *Все переменные окружения, используемые внутри контейнера прописаны в файле .env.dev*

1. Создаём Dockerfile и необходимые зависимости (в этом примере создал requirements.txt)
2. Создаём docker-compose.yml
```yaml
version: '3.8'

services:
  web:
    build: ./
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - ./:/usr/src/app/
    ports:
      - "8000:8000"
    env_file:
      - ./.env.dev
    depends_on:
      db:
        condition: service_healthy

  db:
    image: postgres:15
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_USER=hello_django
      - POSTGRES_PASSWORD=hello_django
      - POSTGRES_DB=hello_django_dev
    ports:
      - "5432:5432"
      # HEALTH CHECK CONDITION
    healthcheck:
#      test: ["CMD-SHELL", "pg_isready", "-U", "hello_django", "-h", "db"]
      test: "pg_isready -h db -U hello_django"
      interval: 5s
      timeout: 5s
      retries: 3

volumes:
  postgres_data:
```
Тут необходимо обратить внимание на healthcheck. Если не указать юзера, то по дефолту подключаться к базе будет от root.  
Из-за этого в логах будет спам ошибки доступа подключения через юзера root.  
`test: ["CMD-SHELL", "pg_isready", "-U", "hello_django", "-h", "db"]` такая команда не валидна по синтаксису!
`test: [ "CMD-SHELL", "pg_isready -d $${POSTGRES_DB} -U $${POSTGRES_USER}" ]` - пример валидной команды.

3. Создаём `entrypoint.sh`. Файл, для запуска миграций при поднятии контейнера с приложением.
```bash
#!/bin/sh
if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while !nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python manage.py flush --no-input
python manage.py migrate

exec "$@"
```

4. Добавить в Dockerfile команду запуска через entrypoint `ENTRYPOINT ["/usr/src/app/entrypoint.sh"]`.


### Gunicorn

1. Добавим docker-compose.prod.yml файл, в котором будет использоваться runcommand запускающая сервер через gunicorn. `command: gunicorn configuration.wsgi:application --bind 0.0.0.0:8000`  
2. Добавить в requirements.txt `gunicorn==21.2.0`
3. Пробуем запустить новый docker-compose `docker compose up -d --build`

### Nginx
0. Для дальнейшей конфигурации будет использоваться prod и dev конфигурация. А именно: docker-compose.prod / dev, Dockerfile.prod / Dockerfile, entrypoint.prod.sh / entrypoint.sh  
Dockerfile.prod собирается теперь в два этапа (Builder + Final). В docker-compose.yml.prod указать, что сборка билдится именно из Dockerfile.prod

1. Добавим сервис nginx в docker-compose.prod.yml
```yaml
nginx:
  build: ./nginx
  ports:
    - 1337:80
  depends_on:
    - web
```
2. В конфиг nginx.conf добавляем конфиг для nginx сервера
```nginx configuration pro
upstream hello_django {
    server web:8000;
}

server {

    listen 80;

    location / {
        proxy_pass http://hello_django;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;
        proxy_redirect off;
    }

}
```
3. Убираем проброску портов в docker-compose.prod.yml. Сейчас будет доступен 8000 порт Django прилажения только внутри докер сервисов. С локальной машины достучаться до этого порта уже не получится
```yaml
services:
  web:
    build:
      context: ./
      dockerfile: Dockerfile.prod
    command: gunicorn configuration.wsgi:application --bind 0.0.0.0:8000
    expose:
      - 8000
    env_file:
      - ./.env.prod
    depends_on:
      db:
        condition: service_healthy
```

### Static

1. Обновим settings.py:
```python
STATIC_ROOT = BASE_DIR / "staticfiles"
```
Теперь каждый запрос по адресу /static/ будет обслуживаться папкой `django_server_linux/staticfiles`
2. В `docker-compose.prod.yml` Добавить `volume` со статикой
```yaml
  - static_volume:/home/app/web/staticfiles
```
> В моём билде в entrypoint.sh есть команда по собиранию статики каждый раз, когда поднимается образ. Это можно делать мануально.  Соответсвенно всякий раз статик файлы будут перезаписываться в моём случае.
3. Далее необходимо обновить nginx конфиг, указав, куда отправлять все запросы на адрес `/static/`
```nginx
location /static/ {
        alias /home/app/web/staticfiles/;
    }
```
4. Последнее, начиная с Django 4.0. При попытке проверить prod сборку заходим на localhost:1337/admin должны подключиться дефолтные Django admin стили.  
Если после ввода логина и пароля ругается на CSRF_TRUSTED_ORIGINS, необходимо добавить в settings.py url с которого обращаемся на сайт.
```python
import os
# CSRF_TRUSTED_ORIGINS = ["http://localhost:1337", ]
CSRF_TRUSTED_ORIGINS = os.environ.get("CSRF_TRUSTED_ORIGINS").split()
```
5. Запускаем финальный тест. Убеждаемся, что внутри проекта создалась папка staticfiles. Если нет - создаём её мануально. 

### Media
