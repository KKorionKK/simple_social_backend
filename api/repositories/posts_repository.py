from .base_repository import Repository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, and_, update
from sqlalchemy.orm import selectinload
from api.models import Post, Like, Comment
from api.schemas.post import CreatePostSchema, PostSchemaExtended
from api.services.errors import CustomErrors


class PostsRepository(Repository):
    async def create_post(self, payload: CreatePostSchema, user_id: str) -> Post:
        async with self.client() as session:
            session: AsyncSession
            model = Post.from_schema(payload, user_id)
            session.add(model)
            await session.flush()
            await session.commit()
            return model

    async def get_posts_by_user_id(self, user_id: str) -> list[Post]:
        async with self.client() as session:
            session: AsyncSession
            result = (
                (
                    await session.execute(
                        select(Post)
                        .where(Post.user_id == user_id)
                        .options(selectinload(Post.user))
                    )
                )
                .scalars()
                .fetchall()
            )
            return result

    async def get_post_by_id(self, post_id: str) -> Post | None:
        async with self.client() as session:
            session: AsyncSession
            result = (
                (
                    await session.execute(
                        select(Post)
                        .where(Post.id == post_id)
                        .options(selectinload(Post.user))
                    )
                )
                .scalars()
                .first()
            )
            return result

    async def get_post_extended(self, post_id: str) -> PostSchemaExtended:
        post = await self.get_post_by_id(post_id)
        return post.as_extended_schema()

    async def get_likes_comments_count(self, post_id: str) -> tuple[int, int]:
        async with self.client() as session:
            session: AsyncSession
            likes = len(
                (
                    await session.execute(
                        select(Like).where(
                            and_(Like.post_id == post_id, Like.comment_id == None)  # noqa: E711
                        )
                    )
                )
                .scalars()
                .fetchall()
            )  # noqa: E711
            comments = len(
                (
                    await session.execute(
                        select(Comment).where(Comment.post_id == post_id)
                    )
                )
                .scalars()
                .fetchall()
            )
            return (likes, comments)

    async def add_like_to_post(self, post_id: str, user_id: str) -> Like:
        model = Like(user_id=user_id, post_id=post_id)
        async with self.client() as session:
            session: AsyncSession
            session.add(model)
            await session.flush()
            await session.commit()
            return model

    async def delete_like(self, post_id: str, user_id: str) -> None:
        async with self.client() as session:
            session: AsyncSession
            await session.execute(
                delete(Like).where(
                    and_(Like.post_id == post_id, Like.user_id == user_id)
                )
            )
            await session.commit()

    async def check_like(self, post_id: str, user_id: str) -> bool:
        async with self.client() as session:
            session: AsyncSession
            result = (
                (
                    await session.execute(
                        select(Like).where(
                            and_(Like.user_id == user_id, Like.post_id == post_id)
                        )
                    )
                )
                .scalars()
                .first()
            )
            if result:
                return True
            return False

    async def like_post(self, post_id: str, user_id: str) -> Like:
        if await self.check_like(post_id, user_id):
            raise CustomErrors.AlreadyLiked
        else:
            return await self.add_like_to_post(post_id, user_id)

    async def get_post_likes(self, post_id: str) -> list[Like]:
        async with self.client() as session:
            session: AsyncSession
            result = (
                (await session.execute(select(Like).where(Like.post_id == post_id)))
                .scalars()
                .fetchall()
            )
            return result

    async def delete_post(self, post_id: str, user_id: str) -> Like:
        async with self.client() as session:
            session: AsyncSession
            result = (
                await session.execute(
                    delete(Post).where(
                        and_(Post.id == post_id, Post.user_id == user_id)
                    )
                )
            ).rowcount
            if result > 0:
                await session.execute(delete(Like).where(Like.post_id == post_id))
                await session.execute(delete(Comment).where(Comment.post_id == post_id))
                await session.commit()

    async def modify_post(
        self, post_id: str, payload: CreatePostSchema, user_id: str
    ) -> PostSchemaExtended:
        async with self.client() as session:
            session: AsyncSession
            await session.execute(
                update(Post)
                .where(and_(Post.id == post_id, Post.user_id == user_id))
                .values(
                    color=payload.color,
                    description=payload.description,
                    pictures_urls=payload.pictures_urls,
                )
            )
            await session.commit()
            return await self.get_post_extended(post_id)
