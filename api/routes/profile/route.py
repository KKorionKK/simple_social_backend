from fastapi import APIRouter, Path
from typing import Annotated
from api.services import consts
from api.models import User
from api.schemas.user import UserSchema
from api.schemas.post import FeedSchema
from api.services.errors import CustomErrors

from fastapi import Depends

from api.services.dependencies import get_current_user
from api.services.postgres_manager import PGManager

profile_route = APIRouter(tags=["Profile endpoint"], prefix=consts.PROFILE_ENDPOINT)


@profile_route.get("/", response_model=UserSchema)
async def get_my_profile(current_user: User = Depends(get_current_user)):
    """Получение данных о текущем пользователе"""
    return current_user.as_schema()


@profile_route.get("/posts", response_model=FeedSchema)
async def get_my_posts(
    current_user: User = Depends(get_current_user),
    manager: PGManager = Depends(PGManager.get_manager),
):
    posts = await manager.posts.get_posts_by_user_id(current_user.id)
    return FeedSchema(items=[item.as_schema() for item in posts])


@profile_route.get("/{user_id}", response_model=UserSchema)
async def get_user_profile(
    user_id: Annotated[str, Path(title="The ID of the user")],
    manager: PGManager = Depends(PGManager.get_manager),
):
    response = await manager.users.get_user_by_id(user_id)
    if response:
        return response.as_schema()
    raise CustomErrors.UserNotFound


@profile_route.get("/posts/{user_id}", response_model=FeedSchema)
async def get_user_posts(
    user_id: Annotated[str, Path(title="The ID of the user")],
    manager: PGManager = Depends(PGManager.get_manager),
):
    posts = await manager.posts.get_posts_by_user_id(user_id)
    return FeedSchema([item.as_schema() for item in posts])
