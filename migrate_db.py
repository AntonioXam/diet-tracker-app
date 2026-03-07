#!/usr/bin/env python3
"""
Script para verificar y añadir columnas faltantes a user_profiles en Supabase

IMPORTANTE: Este script verifica si las columnas existen y proporciona instrucciones
para añadirlas manualmente si no existen.

EJECUCIÓN DEL SQL:
La API REST de Supabase NO permite ejecutar DDL (ALTER TABLE).
Se debe ejecutar en el Dashboard de Supabase > SQL Editor.

Enlace directo: https://supabase.com/dashboard/project/kaomgwojvnncidyezdzj/sql/new

SQL a ejecutar:
------------------------------------------------------------
ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS budget VARCHAR(20) DEFAULT 'medium';
ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS meals_per_day INTEGER DEFAULT 4;
ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS target_calories INTEGER;
ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS preferences TEXT;
ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS onboarding_completed BOOLEAN DEFAULT FALSE;
------------------------------------------------------------
"""
import requests
import sys

# Configuración de Supabase (desde TOOLS.md)
SUPABASE_URL = "https://kaomgwojvnncidyezdzj.supabase.co"
SERVICE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imthb21nd29qdm5uY2lkeWV6ZHpqIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MjcwNzE3NiwiZXhwIjoyMDg4MjgzMTc2fQ.g9dMyRLD6sK6WeQGywhQaTRAdfu48CG8GW8Va2gmwxk"

# Token alternativo proporcionado en la tarea
PUBLISHABLE_KEY = "sbp_aadcbbf966a344841e41135d1a56da0b9d10baf1"

TARGET_COLUMNS = ['budget', 'meals_per_day', 'target_calories', 'preferences', 'onboarding_completed']

SQL_STATEMENTS = """ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS budget VARCHAR(20) DEFAULT 'medium';
ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS meals_per_day INTEGER DEFAULT 4;
ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS target_calories INTEGER;
ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS preferences TEXT;
ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS onboarding_completed BOOLEAN DEFAULT FALSE;"""


def get_headers(key: str) -> dict:
    return {
        "apikey": key,
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json"
    }


def verify_columns() -> tuple:
    """Verifica si las columnas nuevas ya existen en la tabla"""
    headers = get_headers(SERVICE_KEY)
    
    # Intentar seleccionar solo las columnas nuevas
    url = f"{SUPABASE_URL}/rest/v1/user_profiles?select=budget,meals_per_day,target_calories,preferences,onboarding_completed&limit=1"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return True, "Las columnas YA EXISTEN"
    elif response.status_code == 400:
        try:
            error = response.json()
            return False, f"Columnas NO existen: {error}"
        except:
            return False, f"Status 400 - Columnas probablemente no existen"
    else:
        return False, f"Status {response.status_code}: {response.text[:200]}"


def get_current_columns() -> list:
    """Obtiene las columnas actuales de la tabla"""
    headers = get_headers(SERVICE_KEY)
    url = f"{SUPABASE_URL}/rest/v1/user_profiles?select=*&limit=1"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        if data:
            return list(data[0].keys())
    return []


def main():
    print("=" * 70)
    print("🔍 VERIFICACIÓN DE COLUMNAS EN SUPABASE")
    print("=" * 70)
    print(f"URL: {SUPABASE_URL}")
    print(f"Tabla: user_profiles")
    print(f"Columnas objetivo: {TARGET_COLUMNS}")
    print()
    
    # Verificar estado de las columnas
    print("📊 Verificando estado actual...")
    exists, message = verify_columns()
    
    if exists:
        print(f"   ✅ {message}")
        
        # Obtener lista completa de columnas
        print("\n📋 Obteniendo estructura actual...")
        columns = get_current_columns()
        if columns:
            print(f"   Columnas en user_profiles: {columns}")
        
        missing = [c for c in TARGET_COLUMNS if c not in columns]
        if not missing:
            print("\n" + "=" * 70)
            print("🎉 ¡MIGRACIÓN COMPLETADA!")
            print("=" * 70)
            print("   Todas las columnas están presentes en la tabla user_profiles.")
            print("   No se requiere acción adicional.")
            return True
        else:
            print(f"   Faltan columnas: {missing}")
    
    print(f"   ⚠️  {message}")
    
    print("\n" + "=" * 70)
    print("⚠️  ACCIÓN MANUAL REQUERIDA")
    print("=" * 70)
    print("""
La API REST de Supabase NO permite ejecutar DDL (ALTER TABLE).
Debe ejecutar el SQL manualmente en el Dashboard de Supabase.

📌 PASOS A SEGUIR:
1. Abrir: https://supabase.com/dashboard/project/kaomgwojvnncidyezdzj/sql/new
2. Copiar y pegar el siguiente SQL:
3. Hacer clic en "Run" (▶️)

------------------------------------------------------------
""")
    print(SQL_STATEMENTS)
    print("""------------------------------------------------------------

4. Después de ejecutar, volver a correr este script para verificar:
   python3 migrate_db.py
""")
    return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)