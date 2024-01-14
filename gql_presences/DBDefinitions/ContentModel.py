import sqlalchemy

from sqlalchemy import (
    Column,
    String,
    DateTime,
)
from sqlalchemy.dialects.postgresql import UUID
from .Base import BaseModel
from .UUID import UUIDColumn, UUIDFKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

class ContentModel(BaseModel):
    __tablename__ = "taskcontents"

    id = UUIDColumn()
    brief_des = Column(String, comment="brief description")
    detailed_des = Column(String, comment="detailed description")

    event_id = UUIDFKey(nullable=True)#Column(ForeignKey("events.id"), index=True)

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="when this entity has been created")
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="timestamp / token")
    changedby = UUIDFKey(nullable=True,comment="changed by")#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)

    # events = relationship('EventModel', back_populates='contents')
