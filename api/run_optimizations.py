#!/usr/bin/env python3
"""Ejecutar optimizaciones de esquema, omitiendo errores."""

import requests
import time
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
if SUPABASE_URL:
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
print(f"🔧 Encontradas {len(sql_statements)} sentencias SQL.")

success = 0
fail = 0

for i, sql in enumerate(sql_statements, 1):
    try:
        print(f"  [{i}/{len(sql_statements)}] Ejecutando...")
        preview = sql[:120] + "..." if len(sql) > 120 else sql
        print(f"    SQL: {preview}")
        
        response = requests.post(API_URL, headers=headers, json={"query": sql}, timeout=30)
        
        if response.status_code in (200, 201):
            result = response.json()
            print(f"    ✅ Éxito (status {response.status_code})")
            success += 1
        else:
            print(f"    ⚠️ Error {response.status_code}: {response.text[:150]}")
            fail += 1
        
        # Pequeña pausa
        time.sleep(0.5)
        
    except requests.exceptions.Timeout:
        print(f"    ❌ Timeout en la sentencia")
        fail += 1
    except Exception as e:
        print(f"    ❌ Excepción: {e}")
        fail += 1

print(f"\n✅ Completado: {success} exitosas, {fail} fallidas.")