#!/usr/bin/env python3
"""Prueba de importaciones."""
import sys
sys.path.insert(0, '.')

try:
    from config import Config
    print("✅ Config importado")
    
    from utils.calculations import calculate_tmb
    print("✅ Calculations importado")
    
    from utils.validation import validate_register_data
    print("✅ Validation importado")
    
    from services.user_service import UserService
    print("✅ UserService importado")
    
    from supabase import create_client
    supabase = create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)
    print("✅ Supabase conectado")
    
    print("\n✅ Todas las importaciones exitosas")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()