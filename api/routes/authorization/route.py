from fastapi import APIRouter
from api.services import consts
from .schemas import Token
from api.schemas.user import UserRegisterSchema

from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends

from api.services.authorization import AuthorizationService
from api.services.postgres_manager import PGManager

auth_route = APIRouter(prefix=consts.AUTHORIZATION_ENDPOINT, tags=['authorization'])


@auth_route.post('/token', response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], manager: PGManager = Depends(PGManager.get_manager)):
    return await AuthorizationService(manager).get_login_access_token(form_data)


@auth_route.post('/register', response_model=Token)
async def register_user(user_data: UserRegisterSchema, manager: PGManager = Depends(PGManager.get_manager)):
    return await AuthorizationService(manager).register_user(user_data)
