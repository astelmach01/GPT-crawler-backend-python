from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))


class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True)
    description = Column(Text)
    date = Column(DateTime)
    user_id = Column(Integer, ForeignKey("users.id"))
