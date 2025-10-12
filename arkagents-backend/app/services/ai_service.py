from groq import Groq
import os
from typing import List, Dict

print("🔍 Loading Groq service...")
print(f"🔍 GROQ_API_KEY exists: {bool(os.getenv('GROQ_API_KEY'))}")

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

async def call_openai(
    system_prompt: str,
    user_message: str,
    conversation_history: List[Dict]
) -> str:
    """
    Call Groq AI to generate agent response
    """
    
    print(f"🔍 Received chat request: {user_message[:50]}...")
    
    # Build messages array
    messages = [{"role": "system", "content": system_prompt}]
    
    recent_history = conversation_history[-10:] if len(conversation_history) > 10 else conversation_history
    
    for msg in recent_history:
        messages.append({
            "role": msg["role"],
            "content": msg["message"]
        })
    
    print(f"🔍 Calling Groq with {len(messages)} messages...")
    
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",  # ← UPDATED MODEL!
            messages=messages,
            temperature=0.7,
            max_tokens=1000
        )
        
        print(f"✅ Got response from Groq!")
        return response.choices[0].message.content
        
    except Exception as e:
        print(f"❌ Groq Error: {type(e).__name__}: {str(e)}")
        raise Exception(f"Groq API error: {str(e)}")