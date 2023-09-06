from datetime import datetime

from app.conftest import test_task_params
from app.services.aws.rds_crud import read_task_by_id, update_task


def test_update_task(test_db_session):
    updated_data = {
        "task_id": 1,
        "new_description": "Updated Task",
        "new_date": datetime(2022, 1, 2, 12, 0),
    }
    updated_task_1 = update_task(**updated_data, session=test_db_session)

    updated_task_2 = read_task_by_id(session=test_db_session, task_id=1)

    assert updated_task_1.description == "Updated Task"
    assert updated_task_1.date == datetime(2022, 1, 2, 12, 0)
    assert updated_task_2.description == "Updated Task"
    assert updated_task_2.date == datetime(2022, 1, 2, 12, 0)
    assert updated_task_1 == updated_task_2


# test update task with no new date
def test_update_task_no_new_date(test_db_session):
    updated_data = {
        "task_id": 1,
        "new_description": "Updated Task",
    }
    updated_task_1 = update_task(**updated_data, session=test_db_session)

    updated_task_2 = read_task_by_id(session=test_db_session, task_id=1)

    assert updated_task_1.description == "Updated Task"
    assert updated_task_1.date == test_task_params["date"]
    assert updated_task_2.description == "Updated Task"
    assert updated_task_2.date == test_task_params["date"]
    assert updated_task_1 == updated_task_2


# test update task with no new description
def test_update_task_no_new_description(test_db_session):
    updated_data = {
        "task_id": 1,
        "new_date": datetime(2022, 1, 2, 12, 45),
    }
    updated_task_1 = update_task(**updated_data, session=test_db_session)

    updated_task_2 = read_task_by_id(session=test_db_session, task_id=1)

    assert updated_task_1.description == test_task_params["description"]
    assert updated_task_1.date == datetime(2022, 1, 2, 12, 45)
    assert updated_task_2.description == test_task_params["description"]
    assert updated_task_2.date == datetime(2022, 1, 2, 12, 45)
    assert updated_task_1 == updated_task_2


# test update task with no new description or date
# this should raise a value error
def test_update_task_no_new_description_or_date(test_db_session):
    updated_data = {
        "task_id": 1,
    }
    try:
        update_task(**updated_data, session=test_db_session)
    except ValueError:
        pass
    else:
        assert False, "Expected ValueError"

    updated_task_2 = read_task_by_id(session=test_db_session, task_id=1)

    assert updated_task_2.description == test_task_params["description"]
    assert updated_task_2.date == test_task_params["date"]
