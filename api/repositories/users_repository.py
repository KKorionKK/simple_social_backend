from .base_repository import Repository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from api.models import User

class UsersRepository(Repository):
    async def get_user_by_email(self, email: str) -> User | None:
        async with self.client() as session:
            session: AsyncSession
            result = (await session.execute(
                select(User)
                .where(User.email == email)
            )).scalars().first()
            return result
        
    async def add_user(self, user: User) -> User:
        async with self.client() as session:
            session: AsyncSession
            session.add(user)
            await session.commit()
            return user
        
    async def get_user_by_id(self, user_id: User) -> User | None:
        async with self.client() as session:
            session: AsyncSession
            result = (await session.execute(
                select(User)
                .where(User.id == user_id)
            )).scalars().first()
            return result

