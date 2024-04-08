import enum
from datetime import date
from typing import Any

from sqlalchemy import (Boolean, DateTime, Enum, ForeignKey, Integer, String,
                        func)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Contact(Base):
    __tablename__ = 'contacts'
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(15), nullable=False)
    last_name: Mapped[str] = mapped_column(String(15), nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    contact_number: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    birth_date: Mapped[date] = mapped_column(nullable=False)
    additional_information: Mapped[str] = mapped_column(String(250), nullable=True)
    created_at: Mapped[date] = mapped_column(DateTime, default=func.now(), nullable=True)
    update_at: Mapped[date] = mapped_column(DateTime, default=func.now(), onupdate=func.now(), nullable=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=True)
    user: Mapped["User"] = relationship('User', backref="contacts", lazy="joined")


class Role(enum.Enum):
    admin: str = "admin"
    moderator: str = "moderator"
    user: str = "user"


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(150), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    avatar: Mapped[str] = mapped_column(String(255), nullable=True)
    refresh_token: Mapped[str] = mapped_column(String(255), nullable=True)
    created_at: Mapped[date] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[date] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
    role: Mapped[Enum] = mapped_column(Enum(Role), default=Role.user, nullable=True)
    confirmed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=True)
    reset_token: Mapped[str] = mapped_column(String, nullable=True)
