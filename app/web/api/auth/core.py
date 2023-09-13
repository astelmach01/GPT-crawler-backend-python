from datetime import datetime, timedelta

from fastapi import Depends
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.schemas.user import User
from app.services.aws.rds_crud import get_user_by_username
from app.settings import settings
from app.web.api.dependencies import get_db, oauth2_scheme

ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")


async def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


async def get_password_hash(password) -> str:
    return pwd_context.hash(password)


async def authenticate_user(
    username: str, password: str, db: Session = Depends(get_db)
) -> bool:
    """Authenticates a user in the db.

    Args:
        username (str): The username of the user to authenticate.
        password (str): The password of the user to authenticate.
        db (Session, optional): _description_. Defaults to Depends(get_db).

    Returns:
        bool: True if the user is authenticated, False otherwise.
    """
    user = await get_user_by_username(username, db)

    if not user:
        return False

    return await verify_password(password, user.hashed_password)


async def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> User | None:
    """Gets the current user from the token.

    Args:
        token (str, optional): The token to get the user from.
        Defaults to Dependsoauth2_scheme).
        db (Session, optional): The db session. Defaults to Depends(get_db).

    Returns:
        User: The user object.
    """
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return None
    except jwt.PyJWTError:
        return None

    user = await get_user_by_username(username, db)
    if user is None:
        return None
    return User(id=user.id, username=user.username)
