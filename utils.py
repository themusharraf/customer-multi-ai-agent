import os
from dotenv import load_dotenv

def get_openai_api_key():
    """
    .env fayldan OPENAI_API_KEY ni o'qiydi.
    Agar topilmasa, xatolik qaytaradi.
    """
    # .env faylni yuklash
    load_dotenv()

    # Kalitni olish
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError("OPENAI_API_KEY topilmadi! .env faylga qo‘shing.")
    
    return api_key