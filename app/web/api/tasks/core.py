import logging
from datetime import datetime, timedelta

from app.services.aws.rds_crud import create_task
from app.web.api.dependencies import get_db

USER_ID = 2


def create_reminder(
    task: str, days: int, hours: int, minutes: int, user_id: int
) -> str:
    session = get_db()

    date = datetime.now() + timedelta(days=days, hours=hours, minutes=minutes)
    logging.info(f"Creating reminder for {task} at {date}")

    if create_task(task, date, USER_ID, session):
        return f"Reminder: {task} at {date}"

    return "Failed to create reminder"
