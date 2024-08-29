import redis.asyncio as redis
from api.services import config
from .data import UserFeed
from api.schemas.post import PostSchemaExtended
import json


class RedisController:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super(RedisController, cls).__new__(cls)
        return cls.__instance

    def __init__(self) -> None:
        if not hasattr(self, "r"):
            self.r = redis.Redis(
                host=config.REDIS_HOST,
                port=config.REDIS_PORT,
                password=config.REDIS_PASSWORD,
                username="default",
            )

    async def cache_feed(self, user_feed: UserFeed) -> None:
        dump = json.dumps(user_feed.as_json())
        await self.r.set(user_feed.user_id, dump)

    async def cache_feeds(self, user_feeds: list[UserFeed]) -> None:
        pipeline = await self.r.pipeline()
        for feed in user_feeds:
            dump = json.dumps(feed.as_json())
            pipeline.set(feed.user_id, dump)
        await pipeline.execute()

    async def get_feed(self, user_id: str) -> list[PostSchemaExtended] | None:
        raw: str = await self.r.get(user_id)
        if raw:
            data = json.loads(raw).get("feed")
            feed = [PostSchemaExtended(**json.loads(post)) for post in data]
            return feed
        return None
