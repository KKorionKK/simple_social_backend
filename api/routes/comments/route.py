from fastapi import APIRouter, Path
from api.services import consts
from api.models import User
from api.schemas.comment import CreateCommentSchema, PostCommentsSchema, CommentSchema, CommentLikeSchema, CommentUpdateSchema
from typing import Annotated

from fastapi import Depends

from api.services.errors import CustomErrors
from api.services.dependencies import get_current_user
from api.services.postgres_manager import PGManager

comments_route = APIRouter(tags=['Comments endpoint'], prefix=consts.COMMENTS_ENDPOINT)

# TODO: try depends(pgmanager)
@comments_route.post('/', response_model=PostCommentsSchema)
async def create_comment(payload: CreateCommentSchema, current_user: User = Depends(get_current_user), manager: PGManager = Depends(PGManager.get_manager)):
    """Получение данных о текущем пользователе"""
    return await manager.comments.create_comment(current_user.id, payload)

@comments_route.delete('/{comment_id}')
async def delete_comment(comment_id: str, current_user: User = Depends(get_current_user), manager: PGManager = Depends(PGManager.get_manager)):
    await manager.comments.delete_comment_by_id(comment_id, current_user.id)
    return {"message": "OK"}

@comments_route.patch('/', response_model=CommentSchema)
async def modify_comment(payload: CommentUpdateSchema, current_user: User = Depends(get_current_user), manager: PGManager = Depends(PGManager.get_manager)):
    comment = await manager.comments.modify_comment(payload, current_user.id)
    if comment:
        return comment.as_schema()
    else:
        raise CustomErrors.GoneComment


@comments_route.get('/post/{post_id}', response_model=PostCommentsSchema)
async def get_post_comments(
    post_id: Annotated[str, Path(title="The ID of the post")],
    current_user: User = Depends(get_current_user),
    manager: PGManager = Depends(PGManager.get_manager)
):
    comments = await manager.comments.list_post_comments(post_id)
    return PostCommentsSchema(
        comments=[item.as_schema() for item in comments]
    )

@comments_route.get('/thread/{thread_id}', response_model=PostCommentsSchema)
async def get_thread_comments(
    thread_id: Annotated[str, Path(title="The ID of the thread")],
    current_user: User = Depends(get_current_user),
    manager: PGManager = Depends(PGManager.get_manager)
):
    comments = await manager.comments.list_thread_comments(thread_id)
    return PostCommentsSchema(
        comments=[item.as_schema() for item in comments]
    )

@comments_route.post('/like/', response_model=CommentSchema)
async def like_a_comment(
    payload: CommentLikeSchema,
    current_user: User = Depends(get_current_user),
    manager: PGManager = Depends(PGManager.get_manager)
):
    await manager.comments.add_comment_like(payload, current_user.id)
    comment = await manager.comments.get_comment_by_id(payload.comment_id)
    return comment.as_schema()



@comments_route.delete('/like/{comment_id}')
async def unlike_a_comment(
    comment_id: Annotated[str, Path(title="The ID of the comment")],
    current_user: User = Depends(get_current_user),
    manager: PGManager = Depends(PGManager.get_manager)
):
    await manager.comments.delete_comment_like(comment_id, current_user.id)
    return {"message": "OK"}