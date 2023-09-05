from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker

from app.services.aws.models import Base
from app.settings import settings

DB_NAME = "user_task_db"


class DatabaseSession:
    _session = None
    _engine = None

    @classmethod
    def initialize(cls):
        # query timeout of 10 seconds
        cls._engine = create_engine(settings.get_db_url(DB_NAME))

        Base.metadata.create_all(cls._engine)
        session = sessionmaker(bind=cls._engine, autoflush=True)
        cls._session = session()

    @classmethod
    def get_session(cls):
        if cls._session is None:
            cls.initialize()
        return cls._session

    @classmethod
    def close(cls):
        if cls._session:
            cls._session.close()
        if cls._engine:
            cls._engine.dispose()
