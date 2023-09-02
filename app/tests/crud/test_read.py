from app.services.aws.rds_crud import read_tasks_by_user_id

from ..fixtures import test_db_session


def test_get_user_tasks(test_db_session):
    user_tasks = read_tasks_by_user_id(session=test_db_session, user_id=1)
    assert len(user_tasks) == 1
    assert user_tasks[0].description == "test task"


# test reading tasks for a user that doesn't exist
def test_get_user_tasks_no_user(test_db_session):
    user_tasks = read_tasks_by_user_id(session=test_db_session, user_id=2)
    assert len(user_tasks) == 0
