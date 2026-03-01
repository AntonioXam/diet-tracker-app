#!/usr/bin/env python3
"""Verificar tablas existentes."""
import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

supabase = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY'))

tables = ['users', 'user_profiles', 'weight_history', 'master_recipes', 'user_food_bank', 'weekly_plans']

for table in tables:
    try:
        result = supabase.table(table).select('*', count='exact').limit(1).execute()
        count = getattr(result, 'count', len(result.data))
        print(f"{table}: {count} filas")
    except Exception as e:
        print(f"{table}: ERROR - {e}")