from .base_repository import Repository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, and_, desc, update
from api.models import Like, Comment
from api.schemas.comment import CreateCommentSchema, PostCommentsSchema, CommentUpdateSchema, CommentLikeSchema
from api.services.errors import CustomErrors
from api.services import tools

class CommentsRepository(Repository):
    async def comment_preflight(self, paylaod: CreateCommentSchema):
        if paylaod.thread_id:
            if not await self.get_comment_by_id(paylaod.thread_id):
                raise CustomErrors.GoneComment
        if paylaod.reply_to:
            if not await self.get_comment_by_id(paylaod.reply_to):
                raise CustomErrors.GoneComment

    async def get_comment_by_id(self, comment_id: str) -> Comment | None:
        async with self.client() as session:
            session: AsyncSession
            result = (await session.execute(
                select(Comment)
                .where(Comment.id==comment_id)
            )).scalars().first()
            return result
        
    async def delete_comment_by_id(self, comment_id: str, user_id: str):
        async with self.client() as session:
            session: AsyncSession
            await session.execute(
                delete(Comment)
                .where(
                    and_(
                        Comment.user_id==user_id,
                        Comment.id==comment_id
                    )
                )
            )
            await session.commit()

    
    async def modify_comment(self, payload: CommentUpdateSchema, user_id: str) -> Comment:
        async with self.client() as session:
            session: AsyncSession
            await session.execute(
                update(Comment)
                .where(
                    and_(
                        Comment.id==payload.comment_id,
                        Comment.user_id==user_id
                    )
                )
                .values(message=payload.message, last_modified_at=tools.get_dt())
            )
        return await self.get_comment_by_id(payload.comment_id)

    async def create_comment(self, user_id: str, payload: CreateCommentSchema) -> PostCommentsSchema:
        await self.comment_preflight(payload)
        model = Comment.from_schema(payload, user_id)
        async with self.client() as session:
            session: AsyncSession
            session.add(model)
            await session.commit()
        comments = await self.list_post_comments(payload.post_id)
        return PostCommentsSchema(
            comments=[item.as_schema() for item in comments]
        )
        
    
    async def list_post_comments(self, post_id: str, limit: int = 10, skip: int = 0) -> list[Comment]:
        async with self.client() as session:
            session: AsyncSession
            result = (await session.execute(
                select(Comment)
                .where(Comment.post_id==post_id)
                .order_by(desc(Comment.created_at))
                .limit(limit)
                .offset(skip)
            )).scalars().fetchall()
            return result
        
    
    async def list_thread_comments(self, thread_id: str, limit: int = 10, skip: int = 10) -> list[Comment]:
        async with self.client() as session:
            session: AsyncSession
            result = (await session.execute(
                select(Comment)
                .where(Comment.thread_id==thread_id)
                .order_by(desc(Comment.created_at))
                .limit(limit)
                .offset(skip)
            )).scalars().fetchall()
            return result

    async def add_comment_like(self, payload: CommentLikeSchema, user_id: str) -> Like:
        if await self.check_like(payload.comment_id, user_id):
            raise CustomErrors.AlreadyLiked
        model = Like(
            comment_id=payload.comment_id,
            post_id=payload.post_id,
            user_id=user_id
        )
        async with self.client() as session:
            session: AsyncSession
            session.add(model)
            await session.flush()
            await session.commit()
            return model
        

    async def check_like(self, comment_id: str, user_id: str) -> bool:
        async with self.client() as session:
            session: AsyncSession
            result = (await session.execute(
                select(Like)
                .where(
                    and_(
                        Like.user_id==user_id,
                        Like.comment_id==comment_id
                    )
                )
            )).scalars().first()
            if result:
                return True
            return False

    async def delete_comment_like(self, comment_id: str, user_id: str):
        async with self.client() as session:
            session: AsyncSession
            await session.execute(
                delete(Like)
                .where(
                    and_(
                        Like.comment_id==comment_id,
                        Like.user_id==user_id
                    )
                )
            )