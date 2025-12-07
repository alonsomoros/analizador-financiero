from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings
from app.core.logger import setup_logger
import time

logger = setup_logger(__name__)

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def check_db_connection(max_retries: int = 3, retry_delay: int = 2) -> bool:
    """
    Verifica la conexión a la base de datos con reintentos.
    
    Args:
        max_retries: Número máximo de reintentos
        retry_delay: Segundos entre reintentos
        
    Returns:
        True si la conexión es exitosa, False en caso contrario
    """
    for attempt in range(1, max_retries + 1):
        try:
            connection = engine.connect()
            connection.close()
            logger.info("✓ Conexión a la base de datos establecida exitosamente")
            return True
        except Exception as e:
            logger.error(f"✗ Intento {attempt}/{max_retries} - Error de conexión a la base de datos: {e}")
            if attempt < max_retries:
                logger.info(f"Reintentando en {retry_delay} segundos...")
                time.sleep(retry_delay)
            else:
                logger.critical("No se pudo establecer conexión con la base de datos después de todos los reintentos")
                return False

