from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.schemas.response import TokenResponse
from app.web.api.dependencies import get_db

from .core import authenticate_user, create_access_token

router = APIRouter()


@router.post("/token", response_model=TokenResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db=Depends(get_db)):
    authenticated = await authenticate_user(form_data.username, form_data.password, db)
    if not authenticated:
        return TokenResponse(success=False, reason="Incorrect username or password")

    access_token = await create_access_token(data={"sub": form_data.username})

    return TokenResponse(
        success=True, reason="Success", access_token=access_token, token_type="bearer"
    )
