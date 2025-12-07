from app.core.logger import setup_logger

logger = setup_logger(__name__)

def classify_transaction(concept: str) -> str:
    """
    Clasifica una transacción basándose en palabras clave del concepto.
    
    Args:
        concept: Concepto/descripción de la transacción
        
    Returns:
        Categoría asignada
    """
    concept_lower = concept.lower()
    
    # Categorías con sus keywords
    categories = {
        "Comida y Supermercado": [
            "restaurante", "bar", "comida", "supermercado", "burger", "pizza",
            "mercadona", "carrefour", "lidl", "aldi", "dia", "eroski",
            "cafeteria", "cafe", "panaderia", "fruteria", "charcuteria"
        ],
        "Transporte": [
            "uber", "taxi", "cabify", "metro", "bus", "autobus", "tren", "renfe",
            "parking", "aparcamiento", "peaje", "toll", "bicing", "patinete"
        ],
        "Gasolina": [
            "gasolinera", "repsol", "cepsa", "bp", "shell", "galp", "combustible",
            "gasolina", "diesel", "carburante"
        ],
        "Ocio y Entretenimiento": [
            "cine", "teatro", "netflix", "spotify", "hbo", "disney", "amazon prime",
            "juego", "steam", "playstation", "xbox", "concierto", "museo", "gym",
            "gimnasio", "deporte"
        ],
        "Viajes y Alojamiento": [
            "vuelo", "hotel", "airbnb", "booking", "hostal", "avion", "aeropuerto",
            "ryanair", "iberia", "vueling", "easyjet"
        ],
        "Compras Online": [
            "amazon", "ebay", "aliexpress", "zalando", "asos", "shein",
            "compra internet", "paypal"
        ],
        "Salud y Farmacia": [
            "farmacia", "medico", "hospital", "clinica", "dentista", "optica",
            "seguro salud", "sanitas", "adeslas"
        ],
        "Educación": [
            "universidad", "colegio", "academia", "curso", "formacion", "libro",
            "libreria", "material escolar"
        ],
        "Servicios y Suscripciones": [
            "telefono", "movil", "internet", "luz", "agua", "gas", "electricidad",
            "vodafone", "movistar", "orange", "yoigo", "endesa", "iberdrola",
            "suscripcion", "cuota"
        ],
        "Transferencias y Cajeros": [
            "transferencia", "cajero", "retirada", "ingreso", "bizum"
        ]
    }
    
    # Buscar coincidencias
    for category, keywords in categories.items():
        if any(keyword in concept_lower for keyword in keywords):
            logger.debug(f"Transacción '{concept[:50]}...' clasificada como '{category}'")
            return category
    
    # Categoría por defecto
    logger.debug(f"Transacción '{concept[:50]}...' clasificada como 'Otros' (sin coincidencias)")
    return "Otros"

