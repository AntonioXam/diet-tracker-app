#!/usr/bin/env python3
"""Test insert user."""

import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Datos de usuario
user_data = {
    'email': 'testuser2@example.com',
    'password_hash': 'no_password',
    'name': 'testuser2'
}

print("Intentando insertar usuario...")
try:
    result = supabase.table('users').insert(user_data).execute()
    print(f"✅ Éxito: {result}")
    if result.data:
        print(f"ID: {result.data[0]['id']}")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()