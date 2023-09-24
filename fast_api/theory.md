# FastAPI

## Swagger
В FastAPI из коробки имеется swagger. Для перехода в swagger: `http://127.0.0.1:8000/docs`

## URL
В FastAPI url и его параметры можно жёстко валидировать по типу, указывая тайп хинт.  
То, что идёт в функцию как первый аргумент будет считаться как часть пути / endpoint url'а. А то, что идёт как следующие позиционные аргуемнты будет восприниматься как параметры.
Т.е у такой функции:
```python
@app.get('/{pk}')
def get_item(pk: int, sex: str, age: float = None):
    return {"key:": pk, "sex": sex, "age": age}
```
`http://127.0.0.1:8000/15?sex=Men&age=15` Данный url вернет json: 
```json
{
  "key:": 15,
  "sex": "Men",
  "age": 15
}
```
#### Query параметры
Для того, чтобы указать параметр Url необходимо использовать Query()  
Внутри Query есть встроенная валидация. Для того, чтобы сделать параметр обязательным используем `...`
```python
from fastapi import Query
@app.get('/book')
def get_book(q: str = Query(..., description="Search book", min_value=1)):
    return q
```
Если нужно указать дефолтное значение: `Query("default_value")`
Если нужно указать лист значений: `q: list[str] = Query(...)`

#### Path параметры
Для передачи аргументов "Path url" желательно использовать встроенный класс `Path` (Но можно и просто аргумент с тайпом как указано в примере выше)
Внутри также есть встроенная валидация и другие полезные фичи:
```python
from fastapi import Path, Query
@app.get("/book/{pk}")
def get_single_book(pk: int = Path(..., gt=1, le=20), pages: int = Query(None, gt=10, le=500)):   # Больше или равно единицы но меньше 20
    return {"pk": pk, "pages": pages}

```


## Pydantic (коротко)
Pydantic модели в FastAPI используются для валидации и сериализации моделей. В роли валидатора типа данных опять же выступает Type Hint.
По умолчанию если ожидается, например, строка, а приходит число, то оно будет сериализовано в строку и наоборот если это возможно. 
Если возращать Pydantic Model как response, она будет десиарелизована в json объект.


## Database

+ В модуле database.py инициализируем базу данных.
```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()  # От Данного класса будем наследоваться при создании моделей
```

+ Создаём models.py, где описываются модели.
> Смотреть models.py модуль



