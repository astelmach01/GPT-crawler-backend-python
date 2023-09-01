import logging
from datetime import datetime

from app.services.aws.rds_crud import create_task
from app.web.api.dependencies import get_db


def create_reminder(task: str, date: datetime, user_id: int) -> str:
    session = get_db()
    logging.info(f"Creating reminder for {task} at {date}")

    if create_task(task, date, user_id, session):
        return f"Reminder: {task} at {date}"

    return "Failed to create reminder"
