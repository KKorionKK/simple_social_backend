from fastapi import APIRouter
from api.services import consts
from api.models import User
from api.schemas.user import UserSchema

from fastapi import Depends

from api.services.dependencies import get_current_user

profile_route = APIRouter(tags=['Profile endpoint'], prefix=consts.PROFILE_ENDPOINT)


@profile_route.get('/', response_model=UserSchema)
async def get_my_profile(current_user: User = Depends(get_current_user)):
    """Получение данных о текущем пользователе"""
    return current_user.as_schema()
