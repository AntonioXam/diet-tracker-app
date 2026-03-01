#!/usr/bin/env python3
"""Test insert profile."""

import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Datos de prueba
user_id = 5
profile_data = {
    'user_id': user_id,
    'age': 30,
    'gender': 'male',
    'height_cm': 175,
    'current_weight_kg': 80,
    'goal_weight_kg': 75,
    'goal_type': 'lose',
    'activity_level': 'moderate',
    'meals_per_day': 4,
    'allergies': '',
    'disliked_foods': ''
}

print("Intentando insertar perfil...")
try:
    result = supabase.table('user_profiles').insert(profile_data).execute()
    print(f"✅ Éxito: {result}")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()