from api.models import Post, User, Subscription
from api.services.postgres_manager import PGManager
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, func
from sqlalchemy.orm import selectinload
from sqlalchemy.sql import text
from api.services import config
from .data import UserFeed
from .redis_controller import RedisController
from api.schemas.post import PostSchemaExtended

t = "SELECT users.id, users.nickname, COUNT(subscriptions.id) as subs FROM users" \
"JOIN subscriptions ON subscriptions.tail_id = users.id" \
"GROUP BY users.id" \
"ORDER BY subs DESC"

class FeedController:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super(FeedController, cls).__new__(cls)
        return cls.__instance

    def __init__(self, redis: RedisController, manager: PGManager) -> None:
        if not hasattr(self, 'redis'):
            self.redis: RedisController = redis
            self.manager: PGManager = manager

    async def get_subs_count(self, user: User) -> int:
        # async with self.manager.client() as session:
        #     session: AsyncSession
        #     subs_count = (await session.execute(
        #         text(f"SELECT COUNT(id) FROM subscriptions WHERE tail_id = '{user.id}'") # TODO: try select(func.count(subscriptions.id)).where*subscriptions.tail_id==user.id
        #     )).fetchone().tuple()[0]
        #     return subs_count
        async with self.manager.client() as session:
            session: AsyncSession
            subs_count = (await session.execute(
                 select(func.count(Subscription.id)).where(Subscription.tail_id==user.id)
            )).fetchone().tuple()[0]
            return subs_count
    
    async def new_post(self, post: Post, user: User) -> None:
        subs_count = await self.get_subs_count(user)
        if subs_count >= config.SUBS_COUNT_TO_CACHE:
            print(f'need redis cache for user subs, user id: {user.id}')
            # user_feed = await self.get_feed_for_user(user.id)
            # await self.redis.cache_feed(user, user_feed)
            await self.cache_feeds_for_users(user.id)

    async def get_feed(self, user_id: str, limit: int = 20, skip: int = 0) -> list | list[PostSchemaExtended]:
        cache = await self.redis.get_feed(user_id)

        if cache is not None:
            return cache
        
        return await self.get_feed_for_user(user_id, limit, skip)

    async def cache_feeds_for_users(self, tail_id: str, limit: int = 20, skip: int = 0) -> None:
        async with self.manager.client() as session:
            session: AsyncSession
            users = list((await session.execute(
                select(Subscription.head_id)
                .where(Subscription.tail_id==tail_id)
            )).scalars().fetchall())
            print(f'Caching posts for users: {users}')
            caches = []
            for user in users:
                feed = await self.get_feed_for_user(user, limit, skip)
                caches.append(feed)
            await self.redis.cache_feeds(caches)

        

    async def get_feed_for_user(self, user_id: str, limit: int = 20, skip: int = 0) -> UserFeed:
        async with self.manager.client() as session:
            session: AsyncSession
            posts = (await session.execute(
                select(Post)
                .join(Subscription, Subscription.head_id == user_id)
                .where(Post.user_id == Subscription.tail_id)
                .order_by(desc(Post.created_at))
                .limit(limit)
                .offset(skip)
                .options(selectinload(Post.likes), selectinload(Post.comments), selectinload(Post.user))
            )).scalars().fetchall()
            schemas = [post.as_extended_schema() for post in posts]
            return UserFeed(user_id, schemas)