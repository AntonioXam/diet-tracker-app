#!/usr/bin/env python3
"""
Ejecutar SQLs en Supabase para arreglar la app
"""
import requests
import json

# Credenciales de Supabase
SUPABASE_URL = "https://kaomgwojvnncidyezdzj.supabase.co"
SERVICE_TOKEN = "sbp_aadcbbf966a344841e41135d1a56da0b9d10baf1"

headers = {
    "apikey": SERVICE_TOKEN,
    "Authorization": f"Bearer {SERVICE_TOKEN}",
    "Content-Type": "application/json"
}

# SQL a ejecutar
sqls = [
    # 1. Añadir columna salt a users
    "ALTER TABLE users ADD COLUMN IF NOT EXISTS salt TEXT;",
    
    # 2. Añadir columna name a users (por si acaso)
    "ALTER TABLE users ADD COLUMN IF NOT EXISTS name TEXT;",
    
    # 3. Verificar estructura
    "SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'users' ORDER BY ordinal_position;"
]

def execute_sql_via_endpoint():
    """Intentar ejecutar SQL via endpoint alternativo"""
    print("🔄 Intentando ejecutar SQLs...")
    
    # Verificar conexión
    print("\n1️⃣ Verificando conexión a Supabase...")
    try:
        response = requests.get(f"{SUPABASE_URL}/rest/v1/", headers=headers)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Conexión OK")
        else:
            print(f"   ❌ Error: {response.text}")
    except Exception as e:
        print(f"   ❌ Error de conexión: {e}")
        return
    
    # Verificar tabla users
    print("\n2️⃣ Verificando tabla users...")
    try:
        response = requests.get(
            f"{SUPABASE_URL}/rest/v1/users?limit=1",
            headers=headers
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Tabla users accesible")
            print(f"   Registros: {len(data)}")
        else:
            print(f"   ❌ Error: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Verificar recetas
    print("\n3️⃣ Verificando recetas...")
    try:
        response = requests.get(
            f"{SUPABASE_URL}/rest/v1/master_recipes?select=count",
            headers={**headers, "Prefer": "count=exact"}
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            # Obtener todas las recetas para contar
            response = requests.get(
                f"{SUPABASE_URL}/rest/v1/master_recipes?select=id",
                headers=headers
            )
            data = response.json()
            count = len(data)
            print(f"   ✅ Recetas encontradas: {count}")
        else:
            print(f"   ❌ Error: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

if __name__ == "__main__":
    print("=" * 60)
    print("🔧 FIX DIET TRACKER APP")
    print("=" * 60)
    execute_sql_via_endpoint()
    print("\n" + "=" * 60)
    print("✅ Verificación completada")
    print("=" * 60)