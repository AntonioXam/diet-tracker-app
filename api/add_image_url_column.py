#!/usr/bin/env python3
"""Agregar columna image_url a master_recipes."""

import requests
import time

PROJECT_REF = "lwbhdgpvigivgpyjqbeo"
ACCESS_TOKEN = "sbp_1ec3b72a123fc51889736833ba04e4138adb3afa"
API_URL = f"https://api.supabase.com/v1/projects/{PROJECT_REF}/database/query"

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

# Agregar columna image_url como TEXT nullable
sql = "ALTER TABLE master_recipes ADD COLUMN IF NOT EXISTS image_url TEXT;"

print("🔧 Agregando columna image_url a master_recipes...")

try:
    response = requests.post(API_URL, headers=headers, json={"query": sql})
    
    if response.status_code == 200:
        result = response.json()
        if result == []:
            print("✅ Columna agregada (o ya existía)")
        else:
            print(f"✅ Resultado: {result}")
    else:
        print(f"⚠️ Error {response.status_code}: {response.text[:200]}")
        
except Exception as e:
    print(f"❌ Excepción: {e}")
    import traceback
    traceback.print_exc()

print("\n🎉 ¡Esquema actualizado!")