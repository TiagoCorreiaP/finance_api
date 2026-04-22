from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime, date

class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    phone : Optional[str] = None
    birth_date : Optional[date] = None

class UserResponse(BaseModel):
    id: int
    full_name: str
    email: str

    class Config:
        from_attributes = True

class TransactionsBase(BaseModel):
    description: str
    amount: float
    type: str
    category: str
    interest:  Optional[float] = 0.0

class TransactionCreate(TransactionsBase):
    description: str
    amount: float
    type: str
    category: str

class TransactionResponse(TransactionsBase):
    id: int
    date: datetime
    owner_id: int

    class Config:
        from_attributes = True

