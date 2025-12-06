from pydantic import BaseModel
from datetime import date
from typing import Optional

class TransactionBase(BaseModel):
    date: date
    concept: str
    amount: float
    category: Optional[str] = None

class TransactionCreate(TransactionBase):
    pass

class Transaction(TransactionBase):
    id: int

    class Config:
        from_attributes = True
