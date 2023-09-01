import logging
from datetime import datetime

from fastapi import Depends
from sqlalchemy.orm import Session

from app.services.aws.rds import create_task
from app.web.api.dependencies import get_db


def create_reminder(
    task: str, date: datetime, user_id: int, session: Session = Depends(get_db)
) -> str:
    logging.info(f"Creating reminder for {task} at {date}")

    if create_task(task, date, user_id, session):
        return f"Reminder: {task} at {date}"

    return "Failed to create reminder"
