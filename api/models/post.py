from sqlalchemy.orm import mapped_column, relationship, Mapped
from sqlalchemy import String, DateTime, ForeignKey, ARRAY
from api.services import tools
from api.schemas.post import CreatePostSchema, PostSchema, PostSchemaExtended

from api.services.database import Base


class Post(Base):
    __tablename__ = 'posts'

    id: Mapped[String] = mapped_column(String, primary_key=True, default=tools.get_uuid)

    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False, default=tools.get_dt)
    description: Mapped[String] = mapped_column(String, nullable=True)
    color: Mapped[String] = mapped_column(String, nullable=False)
    pictures_urls: Mapped[ARRAY[String]] = mapped_column(ARRAY(String), nullable=False, default=list) # noqa

    user_id: Mapped[String] = mapped_column(String, ForeignKey('users.id'), nullable=False)

    user: Mapped['User'] = relationship("User", remote_side="User.id")  # type: ignore # noqa: F821
    likes: Mapped[list['Like']] = relationship(  # noqa: F821 # type: ignore
        'Like',
        back_populates='post',
        cascade='all, delete-orphan',
        passive_deletes=True
    )
    comments: Mapped[list['Comment']] = relationship(  # noqa: F821 # type: ignore
        'Comment',
        back_populates='post',
        cascade='all, delete-orphan',
        passive_deletes=True
    )

    @classmethod
    def from_schema(cls, schema: CreatePostSchema, user_id: str) -> 'Post':
        return Post(
            description=schema.description,
            color=schema.color,
            pictures_urls=schema.pictures_urls,
            user_id=user_id
        )
    
    @classmethod
    def as_feed(cls):
        # TODO
        pass

    def as_schema(self):
        return PostSchema(
            id=self.id,
            description=self.description,
            color=self.color,
            pictures_urls=self.pictures_urls,
            created_at=self.created_at,
            user=self.user.as_schema()
        )
    
    def as_extended_schema(self):
        return PostSchemaExtended(
            id=self.id,
            description=self.description,
            color=self.color,
            pictures_urls=self.pictures_urls,
            created_at=self.created_at,
            user=self.user.as_schema(),
            likes=len(self.likes),
            comments=len(self.comments)
        )

