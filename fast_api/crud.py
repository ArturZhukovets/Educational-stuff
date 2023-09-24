from sqlalchemy.orm import Session
from models import User, Exercise
from schemas import UserCreate, ExersiceCreate


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_name(db: Session, name: str):
    return db.query(User).filter(User.name == name).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()

def create_user(db: Session, user: UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = User(name=user.name, password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_exercises(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Exercise).offset(skip).limit(limit).all()

def create_user_exercise(db: Session, exercise: ExersiceCreate, user_id: int) -> Exercise:
    db_exercise = Exercise(**exercise.dict(), user_id=user_id)
    db.add(db_exercise)
    db.commit()
    db.refresh(db_exercise)
    return db_exercise
