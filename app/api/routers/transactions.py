from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, func, extract
from app.db.session import get_db
from app.models.transaction import Transaction
from app.services.classifier import classify_transaction
from app.services.csv_parser import TransactionCSVParser, CSVParseError
from app.core.logger import setup_logger
from app.schemas.transaction import (
    TransactionResponse, 
    TransactionListResponse, 
    TransactionStats,
    CategoryStats,
    MonthlyStats
)
from typing import Optional, List
from datetime import date

logger = setup_logger(__name__)
router = APIRouter()

@router.post("/upload")
async def upload_transactions(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Endpoint para subir transacciones desde un archivo CSV.
    Soporta múltiples formatos automáticamente.
    """
    logger.info(f"Recibida solicitud de upload: {file.filename}")
    
    # Validar extensión
    if not file.filename.endswith('.csv'):
        logger.warning(f"Archivo rechazado: {file.filename} (no es CSV)")
        raise HTTPException(status_code=400, detail="El archivo debe ser un CSV")

    try:
        # Leer contenido del archivo
        contents = await file.read()
        logger.info(f"Archivo leído: {len(contents)} bytes")
        
        # Parsear CSV
        parser = TransactionCSVParser()
        try:
            transactions_data = parser.parse(contents)
            logger.info(f"CSV parseado exitosamente: {len(transactions_data)} transacciones encontradas")
        except CSVParseError as e:
            logger.error(f"Error al parsear CSV: {e}")
            raise HTTPException(status_code=400, detail=str(e))
        
        # Estadísticas
        stats = {
            'total': len(transactions_data),
            'processed': 0,
            'duplicates': 0,
            'errors': 0
        }
        
        # Determinar source según el formato detectado
        source = "csv_bank" if parser.detected_format == parser.BANK_FORMAT_CONFIG else "csv_simple"
        logger.info(f"Formato detectado: {source}")
        
        # Procesar cada transacción
        for idx, trans_data in enumerate(transactions_data):
            try:
                # Verificar duplicados
                existing = db.query(Transaction).filter(
                    and_(
                        Transaction.date == trans_data['date'],
                        Transaction.concept == trans_data['concept'],
                        Transaction.amount == trans_data['amount']
                    )
                ).first()
                
                if existing:
                    stats['duplicates'] += 1
                    logger.debug(f"Transacción duplicada ignorada: {trans_data['concept'][:50]} - {trans_data['amount']}€")
                    continue
                
                # Clasificar transacción
                category = classify_transaction(trans_data['concept'])
                
                # Crear nueva transacción
                transaction = Transaction(
                    date=trans_data['date'],
                    concept=trans_data['concept'],
                    amount=trans_data['amount'],
                    category=category,
                    source=source
                )
                
                db.add(transaction)
                stats['processed'] += 1
                
                logger.debug(f"Transacción {idx + 1}/{stats['total']} procesada: {trans_data['concept'][:50]} - {category}")
                
            except Exception as e:
                stats['errors'] += 1
                logger.error(f"Error al procesar transacción {idx + 1}: {e}")
                # Continuar con las demás transacciones
        
        # Commit de todas las transacciones
        try:
            db.commit()
            logger.info(f"Transacciones guardadas en base de datos: {stats['processed']} nuevas")
        except Exception as e:
            db.rollback()
            logger.error(f"Error al guardar en base de datos: {e}")
            raise HTTPException(status_code=500, detail=f"Error al guardar transacciones: {str(e)}")
        
        # Respuesta con estadísticas
        response = {
            "message": f"Procesamiento completado",
            "statistics": {
                "total_rows": stats['total'],
                "new_transactions": stats['processed'],
                "duplicates_skipped": stats['duplicates'],
                "errors": stats['errors']
            },
            "format_detected": source
        }
        
        logger.info(f"Upload completado exitosamente: {response}")
        return response

    except HTTPException:
        # Re-lanzar HTTPExceptions
        raise
    except Exception as e:
        logger.error(f"Error inesperado al procesar archivo: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error al procesar el archivo: {str(e)}")


@router.get("/transactions", response_model=TransactionListResponse)
def get_transactions(
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros a retornar"),
    start_date: Optional[date] = Query(None, description="Fecha de inicio (YYYY-MM-DD)"),
    end_date: Optional[date] = Query(None, description="Fecha de fin (YYYY-MM-DD)"),
    category: Optional[str] = Query(None, description="Filtrar por categoría"),
    min_amount: Optional[float] = Query(None, description="Monto mínimo"),
    max_amount: Optional[float] = Query(None, description="Monto máximo"),
    db: Session = Depends(get_db)
):
    """
    Obtener lista de transacciones con filtros opcionales y paginación.
    """
    logger.info(f"GET /transactions - skip={skip}, limit={limit}, filters: start_date={start_date}, end_date={end_date}, category={category}")
    
    # Construir query base
    query = db.query(Transaction)
    
    # Aplicar filtros
    if start_date:
        query = query.filter(Transaction.date >= start_date)
    if end_date:
        query = query.filter(Transaction.date <= end_date)
    if category:
        query = query.filter(Transaction.category == category)
    if min_amount is not None:
        query = query.filter(Transaction.amount >= min_amount)
    if max_amount is not None:
        query = query.filter(Transaction.amount <= max_amount)
    
    # Contar total
    total = query.count()
    
    # Aplicar ordenamiento y paginación
    transactions = query.order_by(Transaction.date.desc()).offset(skip).limit(limit).all()
    
    logger.info(f"Retornando {len(transactions)} transacciones de {total} totales")
    
    return TransactionListResponse(
        transactions=transactions,
        total=total,
        skip=skip,
        limit=limit
    )


@router.get("/transactions/stats", response_model=TransactionStats)
def get_transaction_stats(
    start_date: Optional[date] = Query(None, description="Fecha de inicio (YYYY-MM-DD)"),
    end_date: Optional[date] = Query(None, description="Fecha de fin (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    """
    Obtener estadísticas agregadas de las transacciones.
    """
    logger.info(f"GET /transactions/stats - start_date={start_date}, end_date={end_date}")
    
    # Query base
    query = db.query(Transaction)
    
    # Aplicar filtros de fecha
    if start_date:
        query = query.filter(Transaction.date >= start_date)
    if end_date:
        query = query.filter(Transaction.date <= end_date)
    
    # Totales generales
    total_transactions = query.count()
    
    # Calcular ingresos y gastos
    all_transactions = query.all()
    total_income = sum(t.amount for t in all_transactions if t.amount > 0)
    total_expenses = sum(t.amount for t in all_transactions if t.amount < 0)
    net_balance = total_income + total_expenses
    
    # Estadísticas por categoría
    category_stats_query = query.with_entities(
        Transaction.category,
        func.count(Transaction.id).label('count'),
        func.sum(Transaction.amount).label('total'),
        func.avg(Transaction.amount).label('average')
    ).group_by(Transaction.category).all()
    
    by_category = [
        CategoryStats(
            category=cat or "Sin categoría",
            count=count,
            total=round(total, 2),
            average=round(average, 2)
        )
        for cat, count, total, average in category_stats_query
    ]
    
    # Estadísticas por mes
    monthly_stats_query = query.with_entities(
        func.to_char(Transaction.date, 'YYYY-MM').label('month'),
        func.count(Transaction.id).label('count'),
        func.sum(Transaction.amount).label('total')
    ).group_by(func.to_char(Transaction.date, 'YYYY-MM')).order_by(func.to_char(Transaction.date, 'YYYY-MM')).all()
    
    by_month = [
        MonthlyStats(
            month=month,
            count=count,
            total=round(total, 2)
        )
        for month, count, total in monthly_stats_query
    ]
    
    logger.info(f"Estadísticas calculadas: {total_transactions} transacciones, {len(by_category)} categorías, {len(by_month)} meses")
    
    return TransactionStats(
        total_transactions=total_transactions,
        total_income=round(total_income, 2),
        total_expenses=round(total_expenses, 2),
        net_balance=round(net_balance, 2),
        by_category=by_category,
        by_month=by_month
    )


@router.get("/transactions/{transaction_id}", response_model=TransactionResponse)
def get_transaction(transaction_id: int, db: Session = Depends(get_db)):
    """
    Obtener una transacción específica por ID.
    """
    logger.info(f"GET /transactions/{transaction_id}")
    
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    
    if not transaction:
        logger.warning(f"Transacción {transaction_id} no encontrada")
        raise HTTPException(status_code=404, detail=f"Transacción con ID {transaction_id} no encontrada")
    
    logger.info(f"Transacción {transaction_id} encontrada: {transaction.concept[:50]}")
    return transaction


@router.delete("/transactions/{transaction_id}")
def delete_transaction(transaction_id: int, db: Session = Depends(get_db)):
    """
    Eliminar una transacción específica por ID.
    """
    logger.info(f"DELETE /transactions/{transaction_id}")
    
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    
    if not transaction:
        logger.warning(f"Transacción {transaction_id} no encontrada para eliminar")
        raise HTTPException(status_code=404, detail=f"Transacción con ID {transaction_id} no encontrada")
    
    concept = transaction.concept[:50]
    db.delete(transaction)
    db.commit()
    
    logger.info(f"Transacción {transaction_id} eliminada: {concept}")
    return {"message": f"Transacción {transaction_id} eliminada exitosamente", "deleted_id": transaction_id}


@router.delete("/transactions")
def delete_all_transactions(
    confirm: bool = Query(False, description="Debe ser 'true' para confirmar la eliminación"),
    db: Session = Depends(get_db)
):
    """
    Eliminar TODAS las transacciones. Requiere confirmación explícita.
    """
    logger.warning(f"DELETE /transactions - confirm={confirm}")
    
    if not confirm:
        raise HTTPException(
            status_code=400, 
            detail="Debe incluir el parámetro 'confirm=true' para eliminar todas las transacciones"
        )
    
    count = db.query(Transaction).count()
    db.query(Transaction).delete()
    db.commit()
    
    logger.warning(f"TODAS las transacciones eliminadas: {count} registros")
    return {"message": f"Todas las transacciones eliminadas exitosamente", "deleted_count": count}
