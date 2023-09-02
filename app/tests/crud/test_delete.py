from app.services.aws.rds_crud import delete_task, read_task_by_id

from ..fixtures import test_db_session


def test_delete_task(test_db_session):
    delete_task(session=test_db_session, task_id=1)
    deleted_task = read_task_by_id(session=test_db_session, task_id=1)
    assert deleted_task is None


# test deleting task that does not exist
def test_delete_task_not_exist(test_db_session):
    assert not delete_task(session=test_db_session, task_id=1000)
    deleted_task = read_task_by_id(session=test_db_session, task_id=1000)
    assert deleted_task is None
