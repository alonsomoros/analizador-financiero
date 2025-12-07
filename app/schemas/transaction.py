from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional, List

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

class TransactionResponse(BaseModel):
    """Respuesta completa de una transacción con todos los campos"""
    id: int
    date: date
    concept: str
    amount: float
    category: Optional[str] = None
    source: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class TransactionListResponse(BaseModel):
    """Respuesta paginada de transacciones"""
    transactions: List[TransactionResponse]
    total: int
    skip: int
    limit: int

class CategoryStats(BaseModel):
    """Estadísticas por categoría"""
    category: str
    count: int
    total: float
    average: float

class MonthlyStats(BaseModel):
    """Estadísticas mensuales"""
    month: str  # Formato: YYYY-MM
    count: int
    total: float

class TransactionStats(BaseModel):
    """Estadísticas generales de transacciones"""
    total_transactions: int
    total_income: float
    total_expenses: float
    net_balance: float
    by_category: List[CategoryStats]
    by_month: List[MonthlyStats]
