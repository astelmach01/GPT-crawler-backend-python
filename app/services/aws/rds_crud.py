import logging
from datetime import datetime
from functools import wraps

import sqlalchemy
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .models import Task as TaskModel
from .models import User as UserModel


def handle_db_errors(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        session = None
        for arg in args:
            if isinstance(arg, Session):
                session = arg
                break
        try:
            return await func(*args, **kwargs)
        except sqlalchemy.exc.IntegrityError as e:
            if session:
                session.rollback()
            logging.error(f"Error in DB operation: {e}")
            return None

    return wrapper


# User
@handle_db_errors
async def create_user(
    username: str, hashed_password: str, session: Session
) -> UserModel | None:
    logging.info(f"Creating user with username: {username}")
    # check if user already exists
    user = await get_user_by_username(username, session)

    if user:
        logging.info(f"User with username: {username} already exists")
        return None

    new_user = UserModel(username=username, hashed_password=hashed_password)
    session.add(new_user)
    session.commit()

    logging.info(f"User with username: {username} created successfully")

    return new_user


@handle_db_errors
async def get_user_by_username(username: str, session: Session) -> UserModel | None:
    return session.query(UserModel).filter_by(username=username).first()


@handle_db_errors
async def update_user_password(
    user_id: int, new_hashed_password: str, session: Session
) -> UserModel | None:
    user = await read_user_by_id(user_id, session)
    if not user:
        return None
    user.hashed_password = new_hashed_password
    session.add(user)
    session.commit()
    return user


@handle_db_errors
async def read_users(session: Session) -> list[UserModel]:
    return session.query(UserModel).all()


@handle_db_errors
async def read_user_by_id(user_id: int, session: Session) -> UserModel | None:
    return session.query(UserModel).filter_by(id=user_id).first()


@handle_db_errors
async def update_user(
    user_id: int, new_username: str, session: Session
) -> UserModel | None:
    user = await read_user_by_id(user_id, session)
    if not user:
        return None
    user.username = new_username
    session.add(user)
    session.commit()
    return user


@handle_db_errors
async def delete_user(user_id: int, session: Session) -> UserModel | None:
    user = await read_user_by_id(user_id, session)
    if not user:
        return None
    session.delete(user)
    session.commit()
    return user


# Task
@handle_db_errors
async def create_task(
    description: str, date: datetime, user_id: int, session: Session
) -> TaskModel | None:
    try:
        new_task = TaskModel(description=description, date=date, user_id=user_id)
        session.add(new_task)
        session.commit()
    except IntegrityError as e:
        session.rollback()
        logging.error(f"Error in DB operation: {e}")
        return None

    return new_task


@handle_db_errors
async def read_tasks(session: Session) -> list[TaskModel]:
    return session.query(TaskModel).all()


@handle_db_errors
async def read_task_by_id(task_id: int, session: Session) -> TaskModel | None:
    return session.query(TaskModel).filter_by(id=task_id).first()


@handle_db_errors
async def read_tasks_by_user_id(
    user_id: int, session: Session
) -> list[TaskModel] | None:
    logging.info(f"Reading tasks for user with id: {user_id}")
    user = await read_user_by_id(user_id, session)
    if not user:
        return None
    return session.query(TaskModel).filter_by(user_id=user_id).all()


@handle_db_errors
async def update_task(
    task_id: int,
    session: Session,
    new_description: str | None = None,
    new_date: datetime | None = None,
) -> TaskModel | None:
    logging.info(f"Updating task with id: {task_id}")
    if not new_description and not new_date:
        raise ValueError("No new data provided to update task")

    task = await read_task_by_id(task_id, session)
    if not task:
        return None

    if new_description:
        task.description = new_description

    if new_date:
        task.date = new_date

    session.add(task)
    session.commit()
    return task


@handle_db_errors
async def delete_task(task_id: int, session: Session) -> TaskModel | None:
    task = await read_task_by_id(task_id, session)
    if not task:
        return None
    session.delete(task)
    session.commit()
    return task
