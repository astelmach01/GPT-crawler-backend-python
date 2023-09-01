from app.services.aws.rds import DatabaseSession


def get_db():
    return DatabaseSession.get_session()
