# groq_api.py

import os
import openai
from dotenv import load_dotenv

load_dotenv()  # Load .env file with GROQ_API_KEY

openai.api_key = os.getenv("GROQ_API_KEY")
openai.api_base = "https://api.groq.com/openai/v1"  # Groq base endpoint

def generate_groq_response(user_query, context):
    try:
        response = openai.ChatCompletion.create(
            model="mixtral-8x7b-32768",  # Fast + smart
            messages=[
                {"role": "system", "content": "You are Asha, an ethical AI assistant empowering women's careers. Provide helpful and inclusive answers."},
                {"role": "user", "content": f"User Query: {user_query}\n\nRelevant Info:\n{context}"}
            ],
            temperature=0.7
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        print(f"Groq API Error: {e}")
        return "Sorry, something went wrong with the AI engine."
