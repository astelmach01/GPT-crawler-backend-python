from functools import wraps

from fastapi import APIRouter, Depends

from app.schemas.response import UserResponse
from app.schemas.user import User
from app.services.aws.rds import create_user, delete_user, read_user_by_id, update_user

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

        return UserResponse(
            success=True, user=User(id=user.id, name=user.name), reason="Success"
        )

    return wrapper


@router.post("/create_user", response_model=UserResponse)
@user_response_decorator
async def create_new_user(name: str, session=Depends(get_db)):
    user = create_user(name, session)
    return user, f"User with name: {name} not created"


@router.get("/{user_id}", response_model=UserResponse)
@user_response_decorator
async def get_user(user_id: int, session=Depends(get_db)):
    user = read_user_by_id(user_id, session)
    return user, f"User with id: {user_id} not found"


@router.put("/{user_id}", response_model=UserResponse)
@user_response_decorator
async def update_user_by_id(user_id: int, new_name: str, session=Depends(get_db)):
    user = update_user(user_id, new_name, session)
    return user, f"User with id: {user_id} not found"


@router.delete("/{user_id}", response_model=UserResponse)
@user_response_decorator
async def delete_user_by_id(user_id: int, session=Depends(get_db)):
    user = delete_user(user_id, session)
    return user, f"User with id: {user_id} not found"
