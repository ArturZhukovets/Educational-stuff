import enum

from sqlalchemy import Column, Integer, String, Enum as EnumSQL, ForeignKey
from sqlalchemy.orm import relationship

from database import Base

class ExerciseCategory(str, enum.Enum):
    LEGS = "Legs"
    BACK = "Back"
    Chest = "Chest"

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    password = Column(String)

    exercises = relationship("Exercise", back_populates="user")


class Exercise(Base):
    __tablename__ = "exercise"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    category = Column(EnumSQL(ExerciseCategory))
    user_id = Column(Integer, ForeignKey("user.id"))

    user = relationship("User", back_populates="exercises")





