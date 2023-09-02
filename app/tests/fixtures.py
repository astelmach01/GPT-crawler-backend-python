from datetime import datetime

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.services.aws.models import Base, Task, User
from app.settings import settings

test_task_params = {
    "description": "test task",
    "date": datetime(2021, 1, 1, 12, 0),
    "user_id": 1,
}

test_user_params = {"name": "test user", "id": 1}


@pytest.fixture(scope="function")
def test_db_session():
    engine = create_engine(settings.get_db_url("test_user_task_db"))
    Base.metadata.create_all(engine)
    session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = session_local()

    # Insert a test user
    test_user = User(**test_user_params)
    db.add(test_user)
    db.commit()

    # insert a test task with a date of 12:30 on 1st Jan 2021
    test_date = datetime(2021, 1, 1, 12, 0)
    test_task = Task(**test_task_params)
    db.add(test_task)
    db.commit()

    yield db  # this is where the testing happens

    db.close()

    Base.metadata.drop_all(engine)
