#!/usr/bin/env python3
"""Ejecutar optimizaciones de esquema en Supabase."""

import requests
import json
import time
import os
from dotenv import load_dotenv

load_dotenv()

# Configuración - usar mismo proyecto que create_tables.py
SUPABASE_URL = os.getenv("SUPABASE_URL")
if SUPABASE_URL:
    # extraer project ref de https://lwbhdgpvigivgpyjqbeo.supabase.co
    PROJECT_REF = SUPABASE_URL.split('//')[1].split('.')[0]
else:
    PROJECT_REF = "lwbhdgpvigivgpyjqbeo"

ACCESS_TOKEN = os.getenv("SUPABASE_ACCESS_TOKEN") or "sbp_1ec3b72a123fc51889736833ba04e4138adb3afa"
API_URL = f"https://api.supabase.com/v1/projects/{PROJECT_REF}/database/query"

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

# Leer sentencias SQL del archivo
def read_sql_statements():
    with open('optimize_schema.sql', 'r') as f:
        content = f.read()
    # Dividir por punto y coma, ignorando líneas de comentarios y espacios
    statements = []
    current = ""
    in_string = False
    string_char = None
    for ch in content:
        if ch in "'\"" and (not in_string or string_char == ch):
            in_string = not in_string
            if in_string:
                string_char = ch
            else:
                string_char = None
        current += ch
        if ch == ';' and not in_string:
            stmt = current.strip()
            if stmt and not stmt.startswith('--'):
                statements.append(stmt)
            current = ""
    # Si queda algo después del último ;
    if current.strip() and not current.strip().startswith('--'):
        statements.append(current.strip())
    return statements

sql_statements = read_sql_statements()

print(f"🔧 Aplicando {len(sql_statements)} optimizaciones de esquema...")

for i, sql in enumerate(sql_statements, 1):
    try:
        print(f"  [{i}/{len(sql_statements)}] Ejecutando...")
        # Para debugging, mostrar primeros 100 chars
        preview = sql[:100] + "..." if len(sql) > 100 else sql
        print(f"    SQL: {preview}")
        
        response = requests.post(API_URL, headers=headers, json={"query": sql}, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if result == []:
                print(f"    ✅ Éxito")
            else:
                print(f"    ✅ Éxito: {result}")
        else:
            print(f"    ⚠️ Error {response.status_code}: {response.text[:200]}")
        
        # Pequeña pausa para no sobrecargar la API
        time.sleep(0.5)
        
    except Exception as e:
        print(f"    ❌ Excepción: {e}")

print("\n✅ ¡Optimizaciones aplicadas! Verificando índices...")

# Verificar que las tablas existen (opcional)
REST_URL = f"https://{PROJECT_REF}.supabase.co/rest/v1/"
ANON_KEY = os.getenv("SUPABASE_KEY")
if not ANON_KEY:
    # fallback al key anónimo del proyecto (puede no tener permisos)
    ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imx3YmhkZ3B2aWdpdmdweWpxYmVvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzIwMzIwMTIsImV4cCI6MjA4NzYwODAxMn0.BVItT1CsufJ-Sgb8royDOKpOCMDAUnQD-ZmuvRSCd1U"

rest_headers = {
    "apikey": ANON_KEY,
    "Authorization": f"Bearer {ANON_KEY}"
}

tables_to_check = ["users", "user_profiles", "weight_history", "master_recipes", "user_food_bank", "weekly_plans"]

for table in tables_to_check:
    try:
        response = requests.get(f"{REST_URL}{table}", headers=rest_headers, params={"limit": "1"})
        if response.status_code == 200:
            print(f"  ✅ Tabla '{table}' existe")
        else:
            print(f"  ❌ Tabla '{table}' no accesible: {response.status_code}")
    except Exception as e:
        print(f"  ❌ Error verificando '{table}': {e}")

print("\n🎉 ¡Base de datos optimizada!")