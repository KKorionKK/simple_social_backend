from pydantic import BaseModel


class UserRegisterSchema(BaseModel):
    email: str
    nickname: str
    password: str
    profile_picture_url: str | None = None
    bio: str


class UserSchema(BaseModel):
    id: str
    email: str
    nickname: str
    profile_picture_url: str | None = None
    bio: str | None
