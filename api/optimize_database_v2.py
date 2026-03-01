#!/usr/bin/env python3
"""Ejecutar optimizaciones de esquema en Supabase usando SQL API."""

import requests
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

def read_sql_statements():
    with open('optimize_schema.sql', 'r') as f:
        content = f.read()
    # Remove comments (-- until end of line)
    lines = content.split('\n')
    cleaned_lines = []
    for line in lines:
        # Remove inline comments
        idx = line.find('--')
        if idx >= 0:
            line = line[:idx]
        cleaned_lines.append(line)
    content = '\n'.join(cleaned_lines)
    # Split by semicolon
    statements = [stmt.strip() for stmt in content.split(';') if stmt.strip()]
    return statements

sql_statements = read_sql_statements()
print(f"🔧 Encontradas {len(sql_statements)} sentencias SQL para ejecutar.")

for i, sql in enumerate(sql_statements, 1):
    try:
        print(f"  [{i}/{len(sql_statements)}] Ejecutando...")
        preview = sql[:150] + "..." if len(sql) > 150 else sql
        print(f"    SQL: {preview}")
        
        response = requests.post(API_URL, headers=headers, json={"query": sql}, timeout=30)
        
        if response.status_code in (200, 201):
            result = response.json()
            if result == [] or (isinstance(result, list) and len(result) == 0):
                print(f"    ✅ Éxito")
            else:
                print(f"    ✅ Éxito: {result}")
        else:
            print(f"    ⚠️ Error {response.status_code}: {response.text[:200]}")
        
        # Pequeña pausa para no sobrecargar la API
        time.sleep(0.5)
        
    except requests.exceptions.Timeout:
        print(f"    ❌ Timeout en la sentencia")
    except Exception as e:
        print(f"    ❌ Excepción: {e}")

print("\n✅ ¡Optimizaciones aplicadas!")