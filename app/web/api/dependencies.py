from fastapi.security import OAuth2PasswordBearer

from app.services.aws.rds import DatabaseSession

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")


def get_db():
    return DatabaseSession.get_session()
