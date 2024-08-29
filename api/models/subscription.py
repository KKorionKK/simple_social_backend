from sqlalchemy.orm import mapped_column, relationship, Mapped
from sqlalchemy import String, DateTime, ForeignKey
from api.services import tools

from api.services.database import Base

from api.schemas.subscription import SubscriptionSchema


class Subscription(Base):
    __tablename__ = "subscriptions"

    id: Mapped[String] = mapped_column(String, primary_key=True, default=tools.get_uuid)

    head_id: Mapped[String] = mapped_column(
        String, ForeignKey("users.id"), nullable=False
    )  # from user
    tail_id: Mapped[String] = mapped_column(
        String, ForeignKey("users.id"), nullable=False
    )  # on user
    date: Mapped[String] = mapped_column(
        DateTime(True), nullable=False, default=tools.get_dt
    )

    head_user: Mapped["User"] = relationship("User", remote_side="User.id", primaryjoin="Subscription.head_id == User.id")  # type: ignore  # noqa: F821
    tail_user: Mapped["User"] = relationship("User", remote_side="User.id", primaryjoin="Subscription.tail_id == User.id")  # type: ignore  # noqa: F821

    def as_schema(self):
        return SubscriptionSchema(**self.__dict__)
