from uuid import uuid4
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Blacklist(db.Model):
    __tablename__ = "blacklist"

    id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False
    )
    email = Column(String)
    app_uuid = Column(String)
    client_ip = Column(String)
    blocked_reason = Column(String)
    created_at = Column(DateTime(timezone=True))

    def __init__(
        self,
        email: str,
        app_uuid: str,
        client_ip: str,
        blocked_reason: str = None,
    ):
        self.email = email
        self.app_uuid = app_uuid
        self.client_ip = client_ip
        self.blocked_reason = blocked_reason
        self.created_at = datetime.now(timezone.utc)
