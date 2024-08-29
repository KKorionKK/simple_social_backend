from .database import PostgreSQLController
from api.repositories import (
    UsersRepository,
    SubscriptionsRepository,
    PostsRepository,
    CommentsRepository,
)


class PGManager:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super(PGManager, cls).__new__(cls)
        return cls.__instance

    def __init__(self, echo: bool = False) -> None:
        if not hasattr(self, "client"):
            self.client = PostgreSQLController(echo)
            self.users = UsersRepository(self.client, self)
            self.subscriptions = SubscriptionsRepository(self.client, self)
            self.posts = PostsRepository(self.client, self)
            self.comments = CommentsRepository(self.client, self)

    @staticmethod
    def get_manager() -> "PGManager":
        return PGManager()
