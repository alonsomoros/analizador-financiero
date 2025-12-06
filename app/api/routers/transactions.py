from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.transaction import Transaction
from app.services.classifier import classify_transaction
import pandas as pd
import io

router = APIRouter()

@router.post("/upload")
async def upload_transactions(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="El archivo debe ser un CSV")

    try:
        contents = await file.read()
        df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
        
        # Validar columnas requeridas
        required_columns = ['fecha', 'concepto', 'monto']
        if not all(col in df.columns for col in required_columns):
             raise HTTPException(status_code=400, detail=f"El CSV debe contener las columnas: {', '.join(required_columns)}")

        transactions_count = 0
        for _, row in df.iterrows():
            category = classify_transaction(row['concepto'])
            
            transaction = Transaction(
                date=pd.to_datetime(row['fecha']).date(),
                concept=row['concepto'],
                amount=float(row['monto']),
                category=category
            )
            db.add(transaction)
            transactions_count += 1
        
        db.commit()
        return {"message": f"Se han procesado exitosamente {transactions_count} transacciones"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar el archivo: {str(e)}")
