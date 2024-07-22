from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime


class UserResponse(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    surname: str
    date_reg: datetime

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    email: EmailStr = Field(default='Email')  # почта
    first_name: str = Field(default='Имя')  # имя
    last_name: str = Field(default='Отчество')  # отчество
    surname: str = Field(default='Фамилия')  # фамилия
    password: str = Field(default='Password')
    complete_password: str = Field(default='Confirm the password')


class GetUser(BaseModel):
    email: EmailStr = Field(default='Email')  # почта
    first_name: str = Field(default='Имя')  # имя
    last_name: str = Field(default='Отчество')  # отчество
    surname: str = Field(default='Фамилия')  # фамилия


class UserUpdate(BaseModel):
    email: EmailStr = Field(default='Email')
    first_name: str = Field(default=None)
    last_name: str = Field(default=None)
    surname: str = Field(default=None)


class CreateNewPassword(BaseModel):
    email: EmailStr = Field(default='Email')
    password: str = Field(default='Password')
    complete_password: str = Field(default='Confirm the password')


class StatusEnum(str, Enum):
    planned = 'planned'
    ended = 'ended'
    active = 'active'


class AddEvent(BaseModel):
    title: str = Field(default='Напишите что-нибудь')
    description: Optional[str]
    date: str
    time: str
    location: str
    status: StatusEnum = Field(default='planned, ended or active')


class GetEvent(BaseModel):
    id: int
    title: str = Field(default='Напишите что-нибудь')
    description: Optional[str]
    date: str
    time: str
    location: str
    host_id: int
    status: str

    class Config:
        from_attributes = True


class EventUpdate(BaseModel):
    id: int
    description: Optional[str]
    date: str
    time: str
    location: str
    status: StatusEnum = Field(default='planned, ended or active')


class GetEventWithGuests(BaseModel):
    event: GetEvent
    guests: List[UserResponse]


class BudgetCreate(BaseModel):
    description: str
    amount: float


class ReviewCreate(BaseModel):
    event_id: int
    rating: int = Field(default='Rate from 1 to 5', ge=1, le=5)
    comment: Optional[str]


class ReviewResponse(BaseModel):
    id: int
    event_id: int
    user_id: int
    rating: int
    comment: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True