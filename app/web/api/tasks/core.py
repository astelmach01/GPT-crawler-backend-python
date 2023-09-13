import logging
from datetime import datetime, timedelta

from app.services.aws.rds_crud import create_task
from app.web.api.dependencies import get_db


async def create_reminder(
    task: str, days: int, hours: int, minutes: int, user_id: int, session=get_db()
) -> str:
    date = datetime.now() + timedelta(days=days, hours=hours, minutes=minutes)
    logging.info(f"Creating reminder for {task} at {date}")

    if await create_task(task, date, user_id, session):
        return f"Successfilly created reminder: {task} {days} days from now, {hours}  \
    hours from now, {minutes} minutes from now"
    return "Failed to create reminder"
