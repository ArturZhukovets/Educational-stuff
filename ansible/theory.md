
## Initialize + run ansible ping
+ Создать и скопировать ssh ключ для ansible. Далее чтобы прокинуть его через докер на убунту сервер скопировать его в
текущую папку. (key.pub)
+ Создать и запустить сервера убунты через докер.
Build an image
```shell
sudo docker build -t ubuntu_server .
```

run ubuntu servers
```shell
sudo docker run -d --name server_1 --rm -p 2222:22  ubuntu_server
sudo docker run -d --name server_2 --rm -p 2223:22  ubuntu_server
sudo docker run -d --name server_3 --rm -p 2224:22  ubuntu_server
```

+ После этого будет поднято 3 сервера подключиться к каждому из которых можно по ssh:
```shell
ssh root@0.0.0.0 -p 2222
```

+ Установить ansible
```shell
sudo apt install ansible
```

+ Создать hosts и добавить в него хосты
```shell
touch hosts
echo <ip> >> hosts
```

+ Создать ansible.cfg
```cfg
[defaults]
inventory = ./hosts
private_key_file = ~/.ssh/ansible
host_key_checking = False
remote_user = root
```

+ Запуск ansible ping
```shell
ansible all -m ping -i hosts
```

## Ansible playbook (Создание примитивного конфига)

+ Создать `playbook_name.yml`, где будут описаны инструкции ansible в yaml формате. (В этом примере это файл `install_deps_1.yml`)
+ Запустить playbook
```shell
ansible-playbook --ask-become-pass install_deps_1.yml
```
После запуска на серверах должны обновиться зависимости `apt` и должен установиться apache 
*ВАЖНО!* В этом примере апаче не будет запущен так как докер образ собран без `systemctl`, поэтому сокет apache не будет работать.
