from enum import Enum
from sqlmodel import SQLModel, Field
from typing import Optional, List
from datetime import datetime
from hashlib import sha256
import sqlalchemy as sa
from sqlalchemy.dialects.sqlite import JSON


class Review(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, default=None)
    event_id: int = Field(foreign_key='event.id')
    user_id: int = Field(foreign_key='user.id')
    rating: int = Field(sa_column=sa.Column(sa.Integer, nullable=False))
    comment: Optional[str] = Field(sa_column=sa.Column(sa.String, nullable=True))
    created_at: datetime = Field(default_factory=datetime.utcnow)


class User(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, default=None)
    hash_password: str  # хэш пароля
    role: str = Field(default='user')  # роль пользователя super_user, verify, no_verify, BAN
    email: str  # почта
    first_name: str  # имя
    last_name: str  # отчество
    surname: str  # фамилия
    date_reg: datetime = Field(default_factory=datetime.utcnow)  # дата регистрации
    temp_data: Optional[str] = Field(nullable=True)

    def verify_password(self, password: str) -> bool:
        return self.hash_password == sha256(password.encode()).hexdigest()

    def set_password(self, password: str):
        self.hash_password = sha256(password.encode()).hexdigest()


class StatusEnum(str, Enum):
    planned = 'planned'
    ended = 'ended'
    active = 'active'


class Event(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, default=None)
    title: str
    description: Optional[str]
    date: str
    time: str
    location: str
    host_id: int = Field(foreign_key='user.id')
    guests: List[int] = Field(default_factory=list, sa_column=sa.Column(JSON, default=[]))
    status: StatusEnum = Field(default='planned, ended or active')


class InvitationEnum(str, Enum):
    confirm = 'confirm'
    denied = 'denied'


class Invitation(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, default=None)
    event_id: int = Field(foreign_key='event.id')
    user_id: int = Field(foreign_key='user.id')
    status: InvitationEnum = Field(default='confirm or denied')


class Budget(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, default=None)
    event_id: int = Field(foreign_key='event.id')
    description: str
    amount: float
    date: datetime = Field(default_factory=datetime.utcnow)
    status: str = Field(default='planned')
