#!/usr/bin/env python3
"""
Script para ejecutar SQLs en Supabase directamente
"""
import requests
import json

# Credenciales
SUPABASE_URL = "https://kaomgwojvnncidyezdzj.supabase.co"
SUPABASE_SERVICE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imthb21nd29qdm5uY2lkeWV6ZHpqIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MjcwNzE3NiwiZXhwIjoyMDg4MjgzMTc2fQ.dBqK8FvP3qH9L5xJ2mN7oR8sT6uV0wY4zA2bC8dE9fG"

headers = {
    "apikey": SUPABASE_SERVICE_KEY,
    "Authorization": f"Bearer {SUPABASE_SERVICE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

def execute_sql(sql_content):
    """Ejecuta SQL en Supabase"""
    url = f"{SUPABASE_URL}/rest/v1/rpc/execute_sql"
    
    payload = {
        "sql": sql_content
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def main():
    print("🚀 Ejecutando SQLs en Supabase...\n")
    
    # Leer schema fix
    print("📄 Leyendo supabase_schema_fix.sql...")
    try:
        with open('/Users/servimac/.openclaw/workspace/supabase_schema_fix.sql', 'r') as f:
            schema_sql = f.read()
        print("✅ Schema fix leído\n")
    except Exception as e:
        print(f"❌ Error leyendo schema fix: {e}")
        return
    
    # Leer seed de recetas
    print("📄 Leyendo seed_recetas.sql...")
    try:
        with open('/Users/servimac/.openclaw/workspace/diet-tracker-app/seed_recetas.sql', 'r') as f:
            seed_sql = f.read()
        print("✅ Seed de recetas leído\n")
    except Exception as e:
        print(f"❌ Error leyendo seed de recetas: {e}")
        return
    
    # Ejecutar schema fix
    print("🔧 Ejecutando schema fix...")
    result = execute_sql(schema_sql)
    if result:
        print("✅ Schema fix ejecutado correctamente\n")
    else:
        print("❌ Error ejecutando schema fix\n")
    
    # Ejecutar seed de recetas
    print("🍳 Ejecutando seed de recetas...")
    result = execute_sql(seed_sql)
    if result:
        print("✅ Seed de recetas ejecutado correctamente\n")
    else:
        print("❌ Error ejecutando seed de recetas\n")
    
    # Verificar
    print("📊 Verificando...")
    verify_sql = "SELECT COUNT(*) as total FROM master_recipes;"
    result = execute_sql(verify_sql)
    if result:
        print(f"✅ Total de recetas en DB: {result}")
    
    print("\n✨ ¡Completado!")

if __name__ == "__main__":
    main()
