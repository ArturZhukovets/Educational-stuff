



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
User=user
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
```
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