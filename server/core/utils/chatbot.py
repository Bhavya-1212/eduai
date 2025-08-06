import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted

genai.configure(api_key='AIzaSyCJ0ugpS6muT7IKj8b5INcdwqbhRWfhReQ')

def get_gemini_response(prompt):
    try:
        model = genai.GenerativeModel('models/gemini-2.0-flash')
        response = model.generate_content(prompt)
        return response.text
    except ResourceExhausted as e:
        # This handles 429 quota exceeded errors
        return "⚠️ EduBot is currently unavailable due to usage limits. Please try again later."
    except Exception as e:
        # Generic fallback
        return f"❌ EduBot encountered an error: {str(e)}"
