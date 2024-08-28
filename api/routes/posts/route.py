from fastapi import APIRouter, Path
from api.services import consts
from api.models import User
from api.schemas.post import FeedSchema, CreatePostSchema
from typing import Annotated

from fastapi import Depends

from api.services.dependencies import get_current_user, get_feed_controller
from api.services.postgres_manager import PGManager
from api.services.feed.feed_controller import FeedController

posts_route = APIRouter(tags=['Posts endpoint'], prefix=consts.POSTS_ENDPOINT)


@posts_route.post('/', response_model=FeedSchema)
async def create_new_post(
    payload: CreatePostSchema, 
    current_user: User = Depends(get_current_user),
    manager: PGManager = Depends(PGManager.get_manager),
    feed_controller: FeedController = Depends(get_feed_controller)
    ):
    """Получение данных о текущем пользователе"""
    post = await manager.posts.create_post(payload, current_user.id)
    posts = await manager.posts.get_posts_by_user_id(current_user.id)
    feed = FeedSchema(items=[item.as_schema() for item in posts])
    await feed_controller.new_post(post, current_user)
    return feed

@posts_route.get('/{post_id}')
async def get_post(
    post_id: Annotated[str, Path(title="The ID of the post")],
    current_user: User = Depends(get_current_user),
    manager: PGManager = Depends(PGManager.get_manager)
):
    return await manager.posts.get_post_extended(post_id)

@posts_route.delete('/{post_id}')
async def delete_post(
    post_id: Annotated[str, Path(title="The ID of the post")],
    current_user: User = Depends(get_current_user),
    manager: PGManager = Depends(PGManager.get_manager)
):
    await manager.posts.delete_post(post_id, current_user.id)


@posts_route.patch('/{post_id}')
async def update_post(
    post_id: Annotated[str, Path(title="The ID of the post")],
    payload: CreatePostSchema,
    current_user: User = Depends(get_current_user),
    manager: PGManager = Depends(PGManager.get_manager)
):
    await manager.posts.modify_post(post_id, payload, current_user.id)

@posts_route.post('/like/{post_id}')
async def like_a_post(
    post_id: Annotated[str, Path(title="The ID of the post")],
    current_user: User = Depends(get_current_user),
    manager: PGManager = Depends(PGManager.get_manager)
):
    await manager.posts.like_post(post_id, current_user.id)
    return {"message": "OK"}


@posts_route.delete('/like/{post_id}')
async def unlike_a_post(
    post_id: Annotated[str, Path(title="The ID of the post")],
    current_user: User = Depends(get_current_user),
    manager: PGManager = Depends(PGManager.get_manager)
):
    await manager.posts.delete_like(post_id, current_user.id)
    return {"message": "OK"}