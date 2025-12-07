import pandas as pd
import io
import re
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from app.core.logger import setup_logger

logger = setup_logger(__name__)

class CSVParseError(Exception):
    """Excepción personalizada para errores de parsing de CSV"""
    pass

class TransactionCSVParser:
    """
    Parser flexible para archivos CSV de transacciones.
    Soporta múltiples formatos:
    - Formato banco: separador ';', encoding 'latin-1', formato europeo de montos
    - Formato simple: separador ',', encoding 'utf-8', formato estándar
    """
    
    # Configuraciones de formatos soportados
    BANK_FORMAT_CONFIG = {
        'separator': ';',
        'encoding': 'latin-1',
        'skiprows': 7,
        'date_format': '%d/%m/%Y',
        'column_mapping': {
            'Fecha operación': 'date',
            'Concepto': 'concept',
            'Importe': 'amount'
        }
    }
    
    SIMPLE_FORMAT_CONFIG = {
        'separator': ',',
        'encoding': 'utf-8',
        'skiprows': 0,
        'date_format': '%Y-%m-%d',
        'column_mapping': {
            'fecha': 'date',
            'concepto': 'concept',
            'monto': 'amount'
        }
    }
    
    def __init__(self):
        self.detected_format = None
    
    def detect_format(self, content: bytes) -> Dict:
        """
        Detecta automáticamente el formato del CSV.
        
        Args:
            content: Contenido del archivo en bytes
            
        Returns:
            Configuración del formato detectado
        """
        # Intentar con formato banco primero
        try:
            df_test = pd.read_csv(
                io.BytesIO(content),
                sep=self.BANK_FORMAT_CONFIG['separator'],
                encoding=self.BANK_FORMAT_CONFIG['encoding'],
                skiprows=self.BANK_FORMAT_CONFIG['skiprows'],
                nrows=5
            )
            
            # Verificar si tiene las columnas del formato banco
            bank_columns = list(self.BANK_FORMAT_CONFIG['column_mapping'].keys())
            if any(col in df_test.columns for col in bank_columns):
                logger.info("Formato detectado: Banco (separador ';', encoding 'latin-1')")
                return self.BANK_FORMAT_CONFIG
        except Exception as e:
            logger.debug(f"No es formato banco: {e}")
        
        # Intentar con formato simple
        try:
            df_test = pd.read_csv(
                io.BytesIO(content),
                sep=self.SIMPLE_FORMAT_CONFIG['separator'],
                encoding=self.SIMPLE_FORMAT_CONFIG['encoding'],
                nrows=5
            )
            
            # Verificar si tiene las columnas del formato simple
            simple_columns = list(self.SIMPLE_FORMAT_CONFIG['column_mapping'].keys())
            if any(col in df_test.columns for col in simple_columns):
                logger.info("Formato detectado: Simple (separador ',', encoding 'utf-8')")
                return self.SIMPLE_FORMAT_CONFIG
        except Exception as e:
            logger.debug(f"No es formato simple: {e}")
        
        raise CSVParseError("No se pudo detectar el formato del CSV. Formatos soportados: banco y simple")
    
    def parse_amount(self, amount_str: str) -> float:
        """
        Parsea montos en diferentes formatos.
        Soporta: '-24,95€', '24.95', '1.234,56€', '-2,20\x80', etc.
        
        Args:
            amount_str: String con el monto
            
        Returns:
            Monto como float
        """
        if pd.isna(amount_str):
            raise ValueError("Monto vacío o nulo")
        
        # Convertir a string y limpiar
        amount_str = str(amount_str).strip()
        
        # Remover caracteres especiales de moneda (€, $, \x80, etc.)
        amount_str = re.sub(r'[€$\x80]', '', amount_str)
        
        # Remover espacios
        amount_str = amount_str.replace(' ', '')
        
        # Detectar formato europeo (coma como decimal)
        # Ejemplo: 1.234,56 -> 1234.56
        if ',' in amount_str and '.' in amount_str:
            # Formato: 1.234,56
            amount_str = amount_str.replace('.', '').replace(',', '.')
        elif ',' in amount_str:
            # Formato: 24,95
            amount_str = amount_str.replace(',', '.')
        
        try:
            return float(amount_str)
        except ValueError:
            raise ValueError(f"No se pudo convertir '{amount_str}' a número")
    
    def parse_date(self, date_str: str, date_format: str) -> datetime:
        """
        Parsea fechas en diferentes formatos.
        
        Args:
            date_str: String con la fecha
            date_format: Formato esperado (ej: '%d/%m/%Y')
            
        Returns:
            Objeto datetime
        """
        if pd.isna(date_str):
            raise ValueError("Fecha vacía o nula")
        
        date_str = str(date_str).strip()
        
        try:
            return datetime.strptime(date_str, date_format)
        except ValueError:
            # Intentar con pandas como fallback
            try:
                return pd.to_datetime(date_str)
            except Exception:
                raise ValueError(f"No se pudo parsear la fecha '{date_str}' con formato '{date_format}'")
    
    def clean_concept(self, concept: str) -> str:
        """
        Limpia y normaliza el concepto de la transacción.
        
        Args:
            concept: Concepto original
            
        Returns:
            Concepto limpio
        """
        if pd.isna(concept):
            return "Sin concepto"
        
        # Convertir a string y limpiar espacios
        concept = str(concept).strip()
        
        # Remover múltiples espacios
        concept = re.sub(r'\s+', ' ', concept)
        
        return concept
    
    def parse(self, content: bytes) -> List[Dict]:
        """
        Parsea el contenido del CSV y retorna una lista de transacciones.
        
        Args:
            content: Contenido del archivo en bytes
            
        Returns:
            Lista de diccionarios con las transacciones parseadas
            
        Raises:
            CSVParseError: Si hay un error al parsear el CSV
        """
        logger.info("Iniciando parsing de CSV")
        
        # Detectar formato
        format_config = self.detect_format(content)
        self.detected_format = format_config
        
        # Leer CSV con la configuración detectada
        try:
            df = pd.read_csv(
                io.BytesIO(content),
                sep=format_config['separator'],
                encoding=format_config['encoding'],
                skiprows=format_config['skiprows']
            )
            logger.info(f"CSV leído exitosamente. Filas: {len(df)}, Columnas: {list(df.columns)}")
        except Exception as e:
            logger.error(f"Error al leer CSV: {e}")
            raise CSVParseError(f"Error al leer el archivo CSV: {str(e)}")
        
        # Mapear columnas
        column_mapping = format_config['column_mapping']
        
        # Verificar que existan las columnas necesarias
        missing_columns = []
        for original_col in column_mapping.keys():
            if original_col not in df.columns:
                missing_columns.append(original_col)
        
        if missing_columns:
            logger.error(f"Columnas faltantes: {missing_columns}")
            raise CSVParseError(
                f"El CSV no contiene las columnas requeridas: {', '.join(missing_columns)}. "
                f"Columnas disponibles: {', '.join(df.columns)}"
            )
        
        # Parsear transacciones
        transactions = []
        errors = []
        
        for idx, row in df.iterrows():
            try:
                # Obtener valores según el mapeo
                date_col = [k for k, v in column_mapping.items() if v == 'date'][0]
                concept_col = [k for k, v in column_mapping.items() if v == 'concept'][0]
                amount_col = [k for k, v in column_mapping.items() if v == 'amount'][0]
                
                # Parsear cada campo
                date = self.parse_date(row[date_col], format_config['date_format'])
                concept = self.clean_concept(row[concept_col])
                amount = self.parse_amount(row[amount_col])
                
                transactions.append({
                    'date': date.date(),
                    'concept': concept,
                    'amount': amount
                })
                
            except Exception as e:
                error_msg = f"Fila {idx + 1}: {str(e)}"
                errors.append(error_msg)
                logger.warning(error_msg)
        
        logger.info(f"Parsing completado. Transacciones válidas: {len(transactions)}, Errores: {len(errors)}")
        
        if errors and len(transactions) == 0:
            raise CSVParseError(f"No se pudo parsear ninguna transacción. Errores: {'; '.join(errors[:5])}")
        
        return transactions
