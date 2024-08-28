from fastapi import APIRouter

from api.routes.profile import profile_route
from api.routes.authorization import auth_route
from api.routes.subscriptions import subs_route
from api.routes.posts import posts_route
from api.routes.comments import comments_route

api_router = APIRouter(prefix='/v1')
api_router.include_router(profile_route)
api_router.include_router(auth_route)
api_router.include_router(subs_route)
api_router.include_router(posts_route)
api_router.include_router(comments_route)