from pydantic import BaseModel
from datetime import datetime


class CreateCommentSchema(BaseModel):
    message: str
    post_id: str
    thread_id: str | None
    reply_to: str | None


class CommentSchema(BaseModel):
    message: str
    created_at: datetime
    user_id: str
    last_modified_at: datetime | None
    thread_id: str | None
    reply_to: str | None


class PostCommentsSchema(BaseModel):
    comments: list[CommentSchema]


class CommentUpdateSchema(BaseModel):
    comment_id: str
    message: str


class CommentLikeSchema(BaseModel):
    post_id: str
    comment_id: str
