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
    brief_des = Column(String)
    detailed_des = Column(String)

    event_id = UUIDFKey(nullable=True)#Column(ForeignKey("events.id"), index=True)

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)

    # events = relationship('EventModel', back_populates='contents')
