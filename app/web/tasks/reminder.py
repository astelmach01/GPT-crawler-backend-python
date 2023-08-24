from datetime import datetime


def create_reminder(task: str, date: str):
    time = datetime.strptime(date, "%Y-%m-%dT%H:%M")
    return f"Reminder: {task} at {time}"
