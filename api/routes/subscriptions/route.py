from fastapi import APIRouter
from api.services import consts
from api.models import User
from api.schemas.subscription import SubscribeSchema, SubscriptionSchema

from fastapi import Depends

from api.services.dependencies import get_current_user
from api.services.postgres_manager import PGManager

subs_route = APIRouter(
    tags=["Subscriptions endpoint"], prefix=consts.SUBSCRIPTIONS_ENDPOINT
)


@subs_route.post("/", response_model=SubscriptionSchema)
async def subscribe_to_user(
    subscribe_schema: SubscribeSchema,
    current_user: User = Depends(get_current_user),
    manager: PGManager = Depends(PGManager.get_manager),
):
    """Подписка на пользователя"""
    sub = await manager.subscriptions.subscribe_to_user(
        current_user, subscribe_schema.user_id
    )
    return sub.as_schema()


@subs_route.delete("/")
async def unsubscribe(
    unsubscribe_schema: SubscribeSchema,
    current_user: User = Depends(get_current_user),
    manager: PGManager = Depends(PGManager.get_manager),
):
    """Отписка от пользователя"""
    await manager.subscriptions.delete_subscription(
        current_user, unsubscribe_schema.user_id
    )
    return {"message": "OK"}
