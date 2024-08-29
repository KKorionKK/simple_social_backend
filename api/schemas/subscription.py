from pydantic import BaseModel
from datetime import datetime


class SubscribeSchema(BaseModel):
    user_id: str


class SubscriptionSchema(BaseModel):
    id: str
    head_id: str
    tail_id: str
    date: datetime
