import logging

from app.services.aws.dynamodb import append_task


def create_reminder(task: str, date: str):
    logging.info(f"Creating reminder for {task} at {date}")

    if append_task("Andrew Stelmach", task, date):
        return f"Reminder: {task} at {date}"

    return "Failed to create reminder"
