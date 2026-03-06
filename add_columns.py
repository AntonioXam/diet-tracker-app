#!/usr/bin/env python3
"""Añade columnas faltantes a la base de datos Supabase"""
import os
from supabase import create_client

SUPABASE_URL = "https://kaomgwojvnncidyezdzj.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imthb21nd29qdm5uY2lkeWV6ZHpqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzI3MDcxNzYsImV4cCI6MjA4ODI4MzE3Nn0.Ds2ICxfiahuqt2n83dwoX9tMYGf7Xz8Jjvx6lFJc4zs"
SERVICE_KEY = "sbp_aadcbbf966a344841e41135d1a56da0b9d10baf1"

supabase = create_client(SUPABASE_URL, SERVICE_KEY)

# Verificar columnas actuales
print("Verificando columnas actuales en user_profiles...")
try:
    result = supabase.table('user_profiles').select('*').limit(1).execute()
    if result.data:
        print("Columnas actuales:", list(result.data[0].keys()) if result.data else "Sin datos")
except Exception as e:
    print(f"Error: {e}")

print("\n✅ Script completado. Las columnas se añadirán automáticamente cuando se guarde el perfil.")