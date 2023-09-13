from pydantic import BaseModel


class User(BaseModel):
    id: int
    username: str


class UserInDB(User):
    hashed_password: str
