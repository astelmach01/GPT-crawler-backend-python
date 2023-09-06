from datetime import datetime

from app.services.aws.rds_crud import create_task, delete_task, read_task_by_id


def test_delete_task(test_db_session):  # noqa
    delete_task(session=test_db_session, task_id=1)
    deleted_task = read_task_by_id(session=test_db_session, task_id=1)
    assert deleted_task is None


# test deleting task that does not exist
def test_delete_task_not_exist(test_db_session):
    assert not delete_task(session=test_db_session, task_id=1000)
    deleted_task = read_task_by_id(session=test_db_session, task_id=1000)
    assert deleted_task is None


# test adding a task, then deleting it
def test_delete_task2(test_db_session):
    new_task = {
        "description": "New Task",
        "date": datetime(2022, 1, 1, 12, 0),
        "user_id": 1,
    }
    created_task = create_task(session=test_db_session, **new_task)
    assert created_task.id is not None and created_task.id > 0
    assert created_task.description == "New Task"
    assert created_task.date == datetime(2022, 1, 1, 12, 0)

    delete_task(session=test_db_session, task_id=1)
    deleted_task = read_task_by_id(session=test_db_session, task_id=1)
    assert deleted_task is None
