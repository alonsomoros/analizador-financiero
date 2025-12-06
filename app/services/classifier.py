def classify_transaction(concept: str) -> str:
    concept_lower = concept.lower()
    
    if any(keyword in concept_lower for keyword in ["restaurante", "bar", "comida", "supermercado", "burger", "pizza"]):
        return "Comida"
    elif any(keyword in concept_lower for keyword in ["cine", "teatro", "netflix", "spotify", "juego"]):
        return "Ocio"
    elif any(keyword in concept_lower for keyword in ["vuelo", "hotel", "airbnb", "tren", "uber", "taxi"]):
        return "Viajes"
    else:
        return "Otros"
