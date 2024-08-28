from pydantic import BaseModel
from datetime import datetime
from .user import UserSchema


class CreatePostSchema(BaseModel):
    description: str
    color: str
    pictures_urls: list[str]

class PostSchema(BaseModel):
    id: str
    description: str
    color: str
    pictures_urls: list[str]
    created_at: datetime
    user: UserSchema

class PostSchemaExtended(BaseModel):
    id: str
    description: str
    color: str
    pictures_urls: list[str]
    created_at: datetime
    user: UserSchema
    likes: int
    comments: int

class FeedSchema(BaseModel):
    items: list[PostSchema]