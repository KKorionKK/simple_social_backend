from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import timedelta, datetime, timezone
from jose import jwt, JWTError
from fastapi import Depends
from typing import Annotated
from api.services.errors import CustomErrors

from api.models import User
from api.schemas.user import UserRegisterSchema
from api.services.postgres_manager import PGManager

from api.services import config
from api.services import consts

class AuthorizationService:
    oauth2_schema = OAuth2PasswordBearer(tokenUrl=consts.API_V1 + consts.AUTHORIZATION_ENDPOINT + '/token')
    context: CryptContext = CryptContext(schemes=['bcrypt'], deprecated='auto')
    def __init__(self, manager: PGManager):
        self.pgmanager: PGManager = manager

    def __get_password_hash(self, password: str) -> str:
        return self.context.hash(password)

    def __verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.context.verify(plain_password, hashed_password)

    def __create_access_token(self, data: dict, expires_delta: timedelta = timedelta(minutes=config.SECURITY_TOKEN_EXPIRES)) -> str:
        payload = data.copy()
        expire = datetime.now(timezone.utc) + expires_delta
        payload.update({"exp": expire})
        encoded_jwt = jwt.encode(
            payload, config.SECRET, algorithm=config.ALGORITHM
        )
        return encoded_jwt
    
    async def get_current_user(self, token: Annotated[str, Depends(oauth2_schema)]) -> User:
        try:
            payload = jwt.decode(
                token, config.SECRET, algorithms=[config.ALGORITHM]
            )
            email: str | None = payload.get("sub")
            if email is None:
                raise CustomErrors.CouldNotValidateCredentials
        except JWTError:
            raise CustomErrors.CouldNotValidateCredentials
        user = await self.pgmanager.users.get_user_by_email(email)
        if user is None:
            raise CustomErrors.CouldNotValidateCredentials
        return user
    
    async def get_login_access_token(self, form_data) -> dict:
        user = await self.authenticate_user(email=form_data.username, password=form_data.password)
        if not user:
            raise CustomErrors.IncorrectCredentials
        access_token_expires = timedelta(
            minutes=config.SECURITY_TOKEN_EXPIRES
        )
        access_token = self.__create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
        
    async def authenticate_user(self, email: str, password: str) -> User | bool:
        user = await self.pgmanager.users.get_user_by_email(email)
        if not user:
            return False
        if not self.__verify_password(password, user.password):
            return False
        return user

    async def register_user(self, user_data: UserRegisterSchema) -> dict:
        register_check = await self.pgmanager.users.get_user_by_email(user_data.email)
        if register_check:
            raise CustomErrors.EmailInUse
        user_dict = user_data.model_dump()
        user_dict['password'] = self.__get_password_hash(user_dict['password'])
        user = User(**user_dict)

        await self.pgmanager.users.add_user(user)

        # access_token_expiration = timedelta(minutes=config.SECURITY_TOKEN_EXPIRES*60)
        access_token = self.__create_access_token({'sub': user_data.email})

        return {"access_token": access_token, "token_type": "bearer"}
