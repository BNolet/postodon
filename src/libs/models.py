import json

import uuid
from datetime import datetime, UTC
from typing import List, Optional
from sqlalchemy import ForeignKey, String, DateTime, Index, Boolean, Integer
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship
from flask_login import UserMixin

Base = declarative_base()

class RowToDict:
    @property
    def dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}
    
class DictToRow:
    def __init__(self, **kwargs):
        existing_field_names = {column.name for column in self.__table__.columns}
        for key, value in kwargs.items():
            if key in existing_field_names:
                value = json.dumps(value) if key == 'meta' else value
                setattr(self, key, value)

class ObjectBase(Base, RowToDict, DictToRow):
    __abstract__ = True

class User(ObjectBase, UserMixin):
    __tablename__ = "user_account"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email: Mapped[str] = mapped_column(String(320), nullable=False)
    username: Mapped[str] = mapped_column(String(64), nullable=False)
    display_name: Mapped[Optional[str]] = mapped_column(String(64), default=None)
    password: Mapped[str] = mapped_column(String(128), nullable=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    posts = relationship('Post', back_populates='author', cascade='all, delete-orphan')

    def __repr__(self) -> str:
        return f"""User(
        id={self.id!r},
        email={self.email},
        name={self.username!r}, 
        fullname={self.display_name!r},
        is_admin={self.is_admin})"""
    
class Post(ObjectBase):
    __tablename__ = "post"

    id: Mapped[str] = mapped_column(String(36),primary_key=True, default=lambda: str(uuid.uuid4()), nullable=False)
    content: Mapped[str] = mapped_column(String(600), nullable=False)
    date_created: Mapped[DateTime] = mapped_column(DateTime, nullable=False, default=datetime.now(UTC))
    date_posted: Mapped[DateTime] = mapped_column(DateTime)
    recurring: Mapped[Boolean] = mapped_column(Boolean, nullable=False, default=False)
    created_by: Mapped[User] = mapped_column(ForeignKey("user_account.id"), nullable=False)

    author = relationship('User', back_populates='posts')

    __table_args__ = (
        Index('idx_user_posts', 'created_by'),
    )

    def __repr__(self) -> str:
        return f"""User=(
        id={self.id!r}, 
        content={self.content!r}, 
        date_created={self.date_created!r}),
        date_posted={self.date_posted!r},
        created_by={self.created_by!r})"""
    
class Social(ObjectBase):
    __tablename__ = "social"

    id: Mapped[str] = mapped_column(String(36),primary_key=True, default=lambda: str(uuid.uuid4()), nullable=False)
    username: Mapped[str] = mapped_column(String(283), nullable=False)
    access_token: Mapped[str] = mapped_column(String(60), nullable=False)
    instance_domain: Mapped[str] = mapped_column(String(253), nullable=False)
    instance_user_id: Mapped[str] = mapped_column(String(16), nullable=False)
    user_id: Mapped[User] = mapped_column(ForeignKey("user_account.id"), nullable=False)

class Instance(ObjectBase):
    __tablename__ = "instance"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), nullable=False)
    domain: Mapped[str] = mapped_column(String(253), nullable=False)
    client_id: Mapped[str] = mapped_column(String(64), nullable=False)
    client_secret: Mapped[str] = mapped_column(String(64), nullable=False)
    

class Version(ObjectBase):
    __tablename__ = "version"

    id: Mapped[str] = mapped_column(String(36),primary_key=True, default=lambda: str(uuid.uuid4()), nullable=False)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(UTC), nullable=False)
    major: Mapped[int] = mapped_column(Integer, nullable=False)
    minor: Mapped[int] = mapped_column(Integer, nullable=False)
    patch: Mapped[int] = mapped_column(Integer, nullable=False)