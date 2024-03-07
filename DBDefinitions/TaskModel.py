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

class TaskModel(BaseModel):

    __tablename__ = "tasks"

    id = UUIDColumn()
    name = Column(String, comment="name of task")
    brief_des = Column(String, comment="brief description")
    detailed_des = Column(String, comment="detailed description")
    reference = Column(String, comment="reference")
    date_of_entry = Column(DateTime, comment="time of entry")
    date_of_submission = Column(DateTime, comment="time of submission")
    date_of_fulfillment = Column(DateTime, comment="time of fulfillment")
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="timestamp / token")

    user_id = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True)
    #users = relationship("UserModel", back_populates="tasks", foreign_keys=[user_id])

    event_id = UUIDFKey(nullable=True)#Column(ForeignKey("events.id"), index=True, nullable=True)

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    changedby = UUIDFKey(nullable=True,comment="who changed this entity")#Column(ForeignKey("users.id"), index=True, nullable=True)
    createtby = UUIDFKey(nullable=True,comment="who created this entity")#Column(ForeignKey("users.id"), index=True, nullable=True)


    # nemusí být relationship