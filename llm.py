import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def call_llm_json(prompt):
    """Calls Groq and forces a JSON object response for perfect parsing."""
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a professional B2B SaaS Account Executive. Always output strictly in JSON format."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}, 
            temperature=0.3, 
            max_tokens=2048
        )
        return response.choices[0].message.content
    except Exception as e:
        print("Groq Error:", e)
        return None