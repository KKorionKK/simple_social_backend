from sqlalchemy.orm import mapped_column, relationship, Mapped
from sqlalchemy import String, DateTime, ForeignKey
from api.services import tools

from api.services.database import Base


class Like(Base):
    __tablename__ = "likes"

    id: Mapped[String] = mapped_column(String, primary_key=True, default=tools.get_uuid)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), default=tools.get_dt, nullable=False
    )

    user_id: Mapped[String] = mapped_column(
        String, ForeignKey("users.id"), nullable=False
    )
    post_id: Mapped[String] = mapped_column(
        String, ForeignKey("posts.id", ondelete="CASCADE"), nullable=False
    )
    comment_id: Mapped[String] = mapped_column(
        String, ForeignKey("comments.id", ondelete="CASCADE"), nullable=True
    )

    user: Mapped["User"] = relationship("User", remote_side="User.id")  # type: ignore  # noqa: F821
    post: Mapped["Post"] = relationship("Post", back_populates="likes")  # type: ignore # noqa: F821
    comment: Mapped["Comment"] = relationship("Comment", remote_side="Comment.id")  # type: ignore # noqa: F821
