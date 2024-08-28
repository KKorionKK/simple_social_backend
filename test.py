from api.services.database import PostgreSQLController
from api.services.postgres_manager import PGManager
from api.services.feed.feed_controller import FeedController
import asyncio
from api.manual.data_generator import run

from api.services.feed.redis_controller import RedisController

async def test():
    await PostgreSQLController().drop_db()
    await PostgreSQLController().init_db()

async def feed_test():
    user_id = 'c681641a-2980-47dd-9fb2-eb330a86ca8e'
    f = FeedController(123, PGManager.get_manager())
    # await f.new_post(12, user_id)
    await f.get_feed_for_user('89fc1d68-b15d-4569-b4bc-d8b52051ed76')


async def test_redis():
    r = RedisController()
    user_id = 'dffff446-4aae-44e6-b199-0210ed871b21'
    s = await r.get_feed(user_id)
    print(s)
    await r.r.aclose()

if __name__ == '__main__':
    # asyncio.run(feed_test())
    asyncio.run(test_redis())
    # asyncio.run(test())