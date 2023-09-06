from sqlalchemy import create_engine, pool
from sqlalchemy.orm import sessionmaker

from app.services.aws.models import Base
from app.settings import settings

DB_NAME = "user_task_db"


class DatabaseSession:
    _engine = None

    @classmethod
    def initialize(cls):
        if cls._engine is None:
            cls._engine = create_engine(
                settings.get_db_url(DB_NAME),
                poolclass=pool.QueuePool,
                pool_size=5,
                pool_pre_ping=True,
                max_overflow=10,
            )
            Base.metadata.create_all(cls._engine)

    @classmethod
    def get_session(cls):
        cls.initialize()
        session = sessionmaker(bind=cls._engine, autoflush=True)
        return session()

    @classmethod
    def close(cls, session):
        if session:
            session.close()
