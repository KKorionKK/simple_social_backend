from dataclasses import dataclass
from api.schemas.post import PostSchemaExtended

@dataclass
class UserFeed:
    user_id: str
    feed: list[PostSchemaExtended]

    def as_json(self):
        return {
            'feed': [item.model_dump_json() for item in self.feed]
        }
