from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String, DateTime
from api.services import tools

from api.services.database import Base
from api.schemas.user import UserSchema


class User(Base):
    __tablename__ = "users"

    id: Mapped[String] = mapped_column(String, primary_key=True, default=tools.get_uuid)
    email: Mapped[String] = mapped_column(String, unique=True)

    nickname: Mapped[String] = mapped_column(String, nullable=False)
    bio: Mapped[String] = mapped_column(String, nullable=True)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=tools.get_dt
    )
    last_online: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=tools.get_dt
    )
    password: Mapped[String] = mapped_column(String, nullable=False)
    profile_picture_url: Mapped[String] = mapped_column(String, nullable=True)

    def as_schema(self):
        return UserSchema(
            id=self.id,
            email=self.email,
            nickname=self.nickname,
            profile_picture_url=self.profile_picture_url,
            bio=self.bio,
        )
