import logging
from datetime import datetime
from typing import List, Type

from sqlalchemy.orm import Session

from .models import Task as TaskModel
from .models import User as UserModel  # Import models from models.py


# User
def create_user(name: str, session: Session) -> UserModel:
    logging.info(f"Creating user with name: {name}")
    new_user = UserModel(name=name)
    session.add(new_user)
    session.commit()
    return new_user


def read_users(session: Session) -> list[UserModel]:
    return session.query(UserModel).all()


def read_user_by_id(user_id: int, session: Session) -> UserModel | None:
    return session.query(UserModel).filter_by(id=user_id).first()


def update_user(user_id: int, new_name: str, session: Session) -> UserModel | None:
    user = read_user_by_id(user_id, session)
    if not user:
        return None
    user.name = new_name
    session.commit()
    return user


def delete_user(user_id: int, session: Session) -> UserModel | None:
    user = read_user_by_id(user_id, session)
    if not user:
        return None
    session.delete(user)
    session.commit()
    return user


# Task
def create_task(
    description: str, date: datetime, user_id: int, session: Session
) -> TaskModel:
    new_task = TaskModel(description=description, date=date, user_id=user_id)
    session.add(new_task)
    session.commit()
    return new_task


def read_tasks(session: Session) -> list[TaskModel]:
    return session.query(TaskModel).all()


def read_task_by_id(task_id: int, session: Session) -> TaskModel | None:
    return session.query(TaskModel).filter_by(id=task_id).first()


def read_tasks_by_user_id(user_id: int, session: Session) -> list[TaskModel]:
    return session.query(TaskModel).filter_by(user_id=user_id).all()


def update_task(
    task_id: int, new_description: str, new_date: datetime, session: Session
) -> TaskModel | None:
    task = read_task_by_id(task_id, session)
    if not task:
        return None
    task.description = new_description
    task.date = new_date
    session.commit()
    return task


def delete_task(task_id: int, session: Session) -> TaskModel | None:
    task = read_task_by_id(task_id, session)
    if not task:
        return None
    session.delete(task)
    session.commit()
    return task
