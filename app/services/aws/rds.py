import logging
from typing import List

import pymysql
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.settings import settings

from .models import Base  # Import models from models.py
from .models import User  # Import models from models.py
from .models import Task as TaskModel

DB_NAME = "user_task_db"

engine = create_engine(settings.get_db_url(DB_NAME))
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


# User
def create_user(name) -> User:
    logging.info(f"Creating user with name: {name}")
    new_user = User(name=name)
    session.add(new_user)
    session.commit()

    return new_user


def read_users() -> List[User] | None:
    return session.query(User).all()  # noqa


def read_user_by_id(user_id) -> User | None:
    return session.query(User).filter_by(id=user_id).first()


def update_user(user_id, new_name) -> User | None:
    user = read_user_by_id(user_id)

    if not user:
        return user

    user.name = new_name
    session.commit()

    return user


def delete_user(user_id) -> User | None:
    user = read_user_by_id(user_id)

    if not user:
        return None

    session.delete(user)
    session.commit()

    return user


# Task
def create_task(description, date, user_id) -> TaskModel:
    new_task = TaskModel(description=description, date=date, user_id=user_id)
    session.add(new_task)
    session.commit()

    return new_task


def read_tasks() -> List[TaskModel]:
    return session.query(TaskModel).all()  # noqa


def read_task_by_id(task_id) -> TaskModel | None:
    return session.query(TaskModel).filter_by(id=task_id).first()


def read_tasks_by_user_id(user_id) -> List[TaskModel]:
    return session.query(TaskModel).filter_by(user_id=user_id).all()  # noqa


def update_task(task_id, new_description, new_date) -> TaskModel | None:
    task = read_task_by_id(task_id)

    if not task:
        return None

    task.description = new_description
    task.date = new_date

    try:
        session.commit()
    except pymysql.err.IntegrityError as e:
        logging.info(f"IntegrityError: {e}")
        session.rollback()
        return None

    return task


def delete_task(task_id) -> TaskModel | None:
    task = read_task_by_id(task_id)

    if not task:
        return None

    session.delete(task)
    session.commit()

    return task
