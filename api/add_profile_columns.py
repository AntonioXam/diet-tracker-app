#!/usr/bin/env python3
"""Agregar columnas faltantes a user_profiles."""

import requests
import time

PROJECT_REF = "lwbhdgpvigivgpyjqbeo"
ACCESS_TOKEN = "sbp_1ec3b72a123fc51889736833ba04e4138adb3afa"
API_URL = f"https://api.supabase.com/v1/projects/{PROJECT_REF}/database/query"

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

# Columnas a agregar
sql_statements = [
    "ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS target_calories REAL;",
    "ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS tmb REAL;",
    "ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS tdee REAL;",
    "ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT NOW();"
]

print("🔧 Agregando columnas a user_profiles...")

for i, sql in enumerate(sql_statements, 1):
    try:
        print(f"  [{i}/{len(sql_statements)}] Ejecutando: {sql[:50]}...")
        response = requests.post(API_URL, headers=headers, json={"query": sql})
        
        if response.status_code in [200, 201]:
            result = response.json()
            if result == []:
                print(f"    ✅ Éxito")
            else:
                print(f"    ✅ Resultado: {result}")
        else:
            print(f"    ⚠️ Error {response.status_code}: {response.text[:100]}")
        
        time.sleep(0.5)
        
    except Exception as e:
        print(f"    ❌ Excepción: {e}")

print("\n🎉 ¡Esquema actualizado!")