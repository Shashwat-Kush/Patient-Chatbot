def classify_intent(text:str) ->str:
    text_lower = text.lower()
    if "appointment" in text_lower:
        return "get_appointment"
    if any(word in text_lower for word in ["medication", "medications", "meds", "prescription", "medicine", "drugs"]):
        return "get_medications"
    return "unknown"

def get_appointment_response(patient:Patient) -> str:
    appt = patient.next_appointment
    if appt:
        return f"Your next appointment is scheduled for {appt.strftime('%Y-%m-%d %H:%M')}."
    else:
        return "You do not have any upcoming appointments scheduled."
    
def get_medications_response(patient:Patient) -> str:
    meds = patient.medications.strip()
    if meds:
        meds_list = [m.strip() for m in meds.split(",") if m.strip()]
        if meds_list:
            return f"Your current medications are: {', '.join(meds_list)}."
        else:
            return "You have no medications listed."
    else:
        return "You have no medications listed."
    
def handle_intent(text:str, patient_id:int=1)->str:
    intent = classify_intent(text)
    try:
        patient = Patient.objects.get(id=patient_id)
    except Patient.DoesNotExist:
        return "Patient not found."
    if intent == "get_appointment":
        return get_appointment_response(patient)
    elif intent == "get_medications":
        return get_medications_response(patient)
    else:
        return (
            "I’m sorry, I didn’t understand that. "
            "You can ask me about your next appointment or your medications."
        )