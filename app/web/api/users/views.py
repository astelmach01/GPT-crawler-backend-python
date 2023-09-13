from functools import wraps

from fastapi import APIRouter, Depends

from app.schemas.response import UserResponse
from app.services.aws.rds_crud import (
    create_user,
    delete_user,
    read_user_by_id,
    update_user,
)
from app.web.api.auth.core import get_current_user, get_password_hash

from ..dependencies import get_db

router = APIRouter()


# this decorator runs the function and checks if the user is None, returning
# the appropriate response
def user_response_decorator(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        user, log_msg = await func(*args, **kwargs)
        if not user:
            return UserResponse(success=False, reason=log_msg)

        return UserResponse(success=True, user_id=user.id, reason="Success")

    return wrapper


@router.post("/create_user", response_model=UserResponse)
@user_response_decorator
async def create_new_user(
    username: str,
    password: str,
    session=Depends(get_db),
):
    hashed_password = get_password_hash(password)
    user = await create_user(username, hashed_password, session)
    return user, f"User with name: {username} already exists"


@router.get("/{user_id}", response_model=UserResponse)
@user_response_decorator
async def get_user(
    user_id: int, session=Depends(get_db), current_user=Depends(get_current_user)
):
    """Gets a user by their id.

    Args:
        user_id (int): The id of the user to get.
        session (_type_, optional): _description_. Defaults to Depends(get_db).

    Returns:
        UserResponse: The response from the server.
    """
    user = await read_user_by_id(user_id, session)
    return user, f"User with id: {user_id} not found"


@router.put("/{user_id}", response_model=UserResponse)
@user_response_decorator
async def update_user_by_id(
    user_id: int,
    new_username: str,
    session=Depends(get_db),
    current_user=Depends(get_current_user),
):
    user = await update_user(user_id, new_username, session)
    return user, f"User with id: {user_id} not found"


@router.delete("/{user_id}", response_model=UserResponse)
@user_response_decorator
async def delete_user_by_id(
    user_id: int, session=Depends(get_db), current_user=Depends(get_current_user)
):
    user = await delete_user(user_id, session)
    return user, f"User with id: {user_id} not found"
