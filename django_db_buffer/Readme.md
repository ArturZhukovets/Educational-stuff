# Django project with custom DB wrapper-handler "DB_Buffer"

Which allows you to wrap requests and write them to a buffer.  
Inside the buffer, a limit is set on the number of records to be saved, and if it is full, this class tries to save all records to the database.  
All the necessary code base is stored inside `db_buffer_service.buffer.py`

***

# DB initialize

```shell
docker pull postgres
```

```shell
docker run --name my-postgres --rm -e POSTGRES_PASSWORD=mysecretpassword -p 5432:5432 -d postgres
```

Or using docker-compose.yml

```shell
docker compose up -d 
```