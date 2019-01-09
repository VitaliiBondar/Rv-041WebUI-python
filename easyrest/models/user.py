"""
This module describe data model for "users" table
"""

from sqlalchemy import (
    Column,
    Integer,
    Text,
    ForeignKey,
)
from sqlalchemy.orm import relationship

from .meta import Base


class User(Base):
    """
    The data model of "users" table
    Defines data structure of "users" table
    Relationsips:
        User->Restaurant: one to many
        User->Token: one to many
        User->UserStatus: one to one
    """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    email = Column(Text)
    password = Column(Text)
    status_id = Column(Integer, ForeignKey('user_statuses.id'))

    token = relationship("Token")
    status = relationship('UserStatus')
    restaurants = relationship('Restaurant')