from pydantic import BaseModel
from datetime import date
from models import ExerciseCategory

class Genre(BaseModel):
    name: str

class Book(BaseModel):
    title: str
    writer: str
    duration: str
    date: date
    summary: str
    genres: list[Genre]
    pages: int


# =========================================== Exersice

class ExersiceBase(BaseModel):
    title: str
    description: str
    category: ExerciseCategory

class ExersiceCreate(ExersiceBase):
    pass

class Exersice(ExersiceBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True

# =========================================== User

class UserBase(BaseModel):
    name: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    exercises: list[Exersice]

    class Config:
        orm_mode = True
