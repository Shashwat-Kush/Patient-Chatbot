# chatbot/ai_llm.py

import groq

# 1. Configure your API key here
client = groq.Groq(api_key="YOUR_GROQ_API_KEY")

# 2. A system prompt to guide the model
SYSTEM_PROMPT = (
    "You are CareBot, a friendly and professional healthcare assistant. "
    "You know the patient's upcoming appointments and current medications. "
    "Answer clearly and concisely. If you don't know, apologize and offer to connect them to a human."
)

def chat_completion(messages: list[dict]) -> str:
    """
    Synchronous call: returns the full assistant response.
    """
    resp = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
    )
    return resp.choices[0].message.content

def streaming_chat_completion(messages: list[dict]):
    """
    Synchronous generator: yields incremental deltas.
    """
    return client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        stream=True,
    )
