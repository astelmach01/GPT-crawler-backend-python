from datetime import datetime

from app.services.aws.rds_crud import create_task
from app.tests.fixtures import test_db_session  # noqa


def test_create_task(test_db_session):
    new_task = {
        "description": "New Task",
        "date": datetime(2022, 1, 1, 12, 0),
        "user_id": 1,
    }
    created_task = create_task(session=test_db_session, **new_task)
    assert created_task.id is not None and created_task.id > 0
    assert created_task.description == "New Task"
    assert created_task.date == datetime(2022, 1, 1, 12, 0)
