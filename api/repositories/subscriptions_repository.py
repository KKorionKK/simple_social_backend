from .base_repository import Repository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, delete
from api.models import Subscription, User
from api.services.errors import CustomErrors

class SubscriptionsRepository(Repository):
    async def check_sub(self, head: User, tail_id: str) -> bool:
        async with self.client() as session:
            session: AsyncSession
            result: Subscription | None = (await session.execute(
                select(Subscription)
                .where(
                    and_(
                        Subscription.head_id == head.id,
                        Subscription.tail_id == tail_id
                    )
                )
            )).scalars().first()
            if result:
                return True
            return False


    async def add_sub(self, head: User, tail_id: str) -> Subscription:
        model = Subscription(head_id=head.id, tail_id=tail_id)
        async with self.client() as session:
            session: AsyncSession
            session.add(model)
            await session.flush()
            await session.commit()
            return model

    async def delete_subscription(self, head: User, tail_id: str) -> None:
        async with self.client() as session:
            session: AsyncSession
            await session.execute(
                delete(Subscription)
                .where(
                    and_(
                        Subscription.head_id == head.id,
                        Subscription.tail_id == tail_id
                    )
                )
            )
            await session.commit()

    async def subscribe_to_user(self, head: User, tail_id: str) -> Subscription:
        check_subscribed = await self.check_sub(head, tail_id)
        check_user = await self.manager.users.get_user_by_id(tail_id)
        if check_subscribed:
            raise CustomErrors.AlreadySubscribed
        if not check_user:
            raise CustomErrors.UserNotFound
        return await self.add_sub(head, tail_id)
    
    async def get_user_subscribers_count(self, user_id: str) -> Subscription:
        async with self.client() as session:
            session: AsyncSession
            await session.execute(
                select(User)
                .where()
            )
