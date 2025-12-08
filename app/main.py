from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routers import transactions
from app.db.session import check_db_connection, engine, Base
from app.models import transaction # Importar para que SQLAlchemy reconozca el modelo

# Crear tablas
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Analizador Financiero")

# Configurar CORS para permitir requests desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # URL del frontend Vite
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos HTTP
    allow_headers=["*"],  # Permitir todos los headers
)

app.include_router(transactions.router, prefix="/api/v1", tags=["transactions"])

@app.on_event("startup")
def startup_event():
    check_db_connection()

@app.get("/")
def read_root():
    return {"message": "Bienvenido al Analizador Financiero"}
