from sqlalchemy.orm import mapped_column, relationship, Mapped
from sqlalchemy import String, DateTime, ForeignKey
from api.services import tools
from api.schemas.comment import CreateCommentSchema, CommentSchema

from api.services.database import Base


class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[String] = mapped_column(String, primary_key=True, default=tools.get_uuid)

    message: Mapped[String] = mapped_column(String, nullable=False)
    thread_id: Mapped[String] = mapped_column(String, nullable=True)
    reply_to: Mapped[String] = mapped_column(String, nullable=True)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(True), nullable=False, default=tools.get_dt
    )
    last_modified_at: Mapped[DateTime] = mapped_column(DateTime(True), nullable=True)

    user_id: Mapped[String] = mapped_column(
        String, ForeignKey("users.id"), nullable=False
    )
    post_id: Mapped[String] = mapped_column(
        String, ForeignKey("posts.id", ondelete="CASCADE"), nullable=False
    )

    user: Mapped["User"] = relationship("User", remote_side="User.id")  # type: ignore # noqa: F821

    post: Mapped["Post"] = relationship("Post", back_populates="comments")  # type: ignore # noqa: F821

    @classmethod
    def from_schema(cls, schema: CreateCommentSchema, user_id: str) -> "Comment":
        return Comment(
            message=schema.message,
            post_id=schema.post_id,
            user_id=user_id,
            thread_id=schema.thread_id,
            reply_to=schema.reply_to,
        )

    def as_schema(self) -> CommentSchema:
        return CommentSchema(**self.__dict__)
