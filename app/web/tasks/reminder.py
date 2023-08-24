import logging
from datetime import datetime


def create_reminder(task: str, date: str):
    logging.info(f"Creating reminder for {task} at {date}")
    time = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    return f"Reminder: {task} at {time}"
