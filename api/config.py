import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuración de la aplicación."""
    SUPABASE_URL = os.getenv('SUPABASE_URL')
    SUPABASE_KEY = os.getenv('SUPABASE_KEY')
    
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise ValueError("SUPABASE_URL y SUPABASE_KEY deben estar definidos en .env")
    
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'