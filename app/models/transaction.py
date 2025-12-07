from sqlalchemy import Column, Integer, String, Float, Date, DateTime, Index
from sqlalchemy.sql import func
from app.db.session import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False, index=True)
    concept = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    category = Column(String, nullable=True, index=True)
    source = Column(String, nullable=True, default="manual")  # 'manual', 'csv_bank', 'csv_simple'
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Índice compuesto para detectar duplicados
    __table_args__ = (
        Index('idx_transaction_unique', 'date', 'concept', 'amount'),
    )

