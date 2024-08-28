from .authorization import AuthorizationService
from .postgres_manager import PGManager
from fastapi import Depends
from .feed.feed_controller import FeedController
from .feed.redis_controller import RedisController

def get_auth_service():
    return AuthorizationService(PGManager.get_manager())

async def get_current_user(token: str = Depends(AuthorizationService.oauth2_schema), auth_service: AuthorizationService = Depends(get_auth_service)):
    return await auth_service.get_current_user(token)


def get_redis():
    return RedisController()

def get_feed_controller():
    redis = get_redis()
    manager = PGManager.get_manager()
    return FeedController(redis, manager)