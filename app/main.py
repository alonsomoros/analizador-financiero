from fastapi import FastAPI
from app.api.routers import transactions
from app.db.session import check_db_connection, engine, Base
from app.models import transaction # Importar para que SQLAlchemy reconozca el modelo

# Crear tablas
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Analizador Financiero")

app.include_router(transactions.router, prefix="/api/v1", tags=["transactions"])

@app.on_event("startup")
def startup_event():
    check_db_connection()

@app.get("/")
def read_root():
    return {"message": "Bienvenido al Analizador Financiero"}
