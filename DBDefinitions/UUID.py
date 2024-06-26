from uuid import uuid4, UUID
from sqlalchemy import Column, Uuid
uuid = uuid4

def UUIDColumn():
    return Column(Uuid, primary_key=True, comment="primary key", default=uuid)

def UUIDFKey(comment=None, nullable=True, **kwargs):
    return Column(Uuid, index=True, comment=comment, nullable=nullable, **kwargs)
# id = Column(UUID(as_uuid=True), primary_key=True, server_default=sqlalchemy.text("uuid_generate_v4()"),)