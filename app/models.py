from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime, timezone

class User(Base):
    __tablename__ = "users"

    id= Column(Integer, primary_key=True, index=True)
    full_name = Column(String(150))
    email = Column(String(150), unique=True, index=True)
    hashed_password = Column(String(255))

    transactions = relationship("Transaction", back_populates="owner")

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String(255))
    amount = Column(Float)

    type = Column(String(20))

    category = Column(String(50))

    interest = Column(Float, default=0.0)

    date = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="transactions")