from datetime import datetime

from app.conftest import test_db_session
from app.services.aws.rds_crud import create_task


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


# test creating 2 tasks
def test_create_task2(test_db_session):
    new_task = {
        "description": "New Task",
        "date": datetime(2022, 1, 1, 12, 0),
        "user_id": 1,
    }
    created_task = create_task(session=test_db_session, **new_task)
    assert created_task.id is not None and created_task.id > 0
    assert created_task.description == "New Task"
    assert created_task.date == datetime(2022, 1, 1, 12, 0)

    new_task = {
        "description": "New Task2",
        "date": datetime(2023, 1, 1, 12, 0),
        "user_id": 1,
    }
    created_task = create_task(session=test_db_session, **new_task)
    assert created_task.id is not None and created_task.id > 0
    assert created_task.description == "New Task2"
    assert created_task.date == datetime(2023, 1, 1, 12, 0)
