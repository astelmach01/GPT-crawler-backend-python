from functools import wraps

from fastapi import APIRouter

from app.schemas.response import UserResponse
from app.schemas.user import User
from app.services.aws.rds import create_user, delete_user, read_user_by_id, update_user

router = APIRouter()


def user_response_decorator(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        user, log_msg = await func(*args, **kwargs)
        if not user:
            return UserResponse(success=False, reason=log_msg)
        return UserResponse(success=True, user=User(id=user.id, name=user.name))

    return wrapper


@router.post("/create_user", response_model=UserResponse)
@user_response_decorator
async def create_new_user(name: str):
    user = create_user(name)
    return user, f"User with name: {name} not created"


@router.get("/{user_id}", response_model=UserResponse)
@user_response_decorator
async def get_user(user_id: str):
    user = read_user_by_id(user_id)
    return user, f"User with id: {user_id} not found"


@router.put("/{user_id}", response_model=UserResponse)
@user_response_decorator
async def update_user_by_id(user_id: str, new_name: str):
    user = update_user(user_id, new_name)
    return user, f"User with id: {user_id} not found"


@router.delete("/{user_id}", response_model=UserResponse)
@user_response_decorator
async def delete_user_by_id(user_id: str):
    user = delete_user(user_id)
    return user, f"User with id: {user_id} not found"
