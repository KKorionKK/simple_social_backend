from datetime import datetime, timezone
from uuid import uuid4


def get_dt():
    return datetime.now(timezone.utc)


def get_uuid():
    return str(uuid4())
