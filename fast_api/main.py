from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import SessionLocal, engine
from schemas import Book

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ======================================================= User |

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_name(db, name=user.name)
    if db_user:
        raise HTTPException(status_code=400, detail="Such name already registered")
    return crud.create_user(db=db, user=user)

@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# ======================================================= Exercise |

@app.post("/create-exercise/{user_id}/", response_model=schemas.Exersice)
def create_exercise(
        user_id: int, exercise: schemas.ExersiceCreate, db: Session = Depends(get_db)
):
    return crud.create_user_exercise(db=db, exercise=exercise, user_id=user_id)

@app.get("/exercises", response_model=list[schemas.Exersice])
def read_exercises(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    exercises = crud.get_exercises(db=db, skip=skip, limit=limit)
    return exercises

# ======================================================= #

@app.get("/")
def home():
    return {"key": "Hello"}

@app.get('/{pk}')
def get_item(pk: int, sex: str, age: float = None):
    return {"key:": pk, "sex": sex, "age": age}

@app.get('/user/{pk}/items/{item}/')
def get_user_item(pk: int, item: str):
    return {"user": pk, "item": item}


@app.post('/book')
def create_book(item: Book):
    return item
