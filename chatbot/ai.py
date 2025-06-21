def classify_intent(text:str) ->str:
    text_lower = text.lower()
    if "appointment" in text_lower:
        return "get_appointment"
    if "medication" in text_lower or "medications" in text_lower or "meds" in text_lower or "prescription" in text_lower or "medicine" in text_lower or "drugs" in text_lower:
        return "get_medications"
    else:
        return "unknown"