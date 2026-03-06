#!/usr/bin/env python3
"""
Verificar estado de la base de datos
"""
import requests
import json

# Credenciales de Supabase
SUPABASE_URL = "https://kaomgwojvnncidyezdzj.supabase.co"
ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imthb21nd29qdm5uY2lkeWV6ZHpqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzI3MDcxNzYsImV4cCI6MjA4ODI4MzE3Nn0.Ds2ICxfiahuqt2n83dwoX9tMYGf7Xz8Jjvx6lFJc4zs"

headers = {
    "apikey": ANON_KEY,
    "Authorization": f"Bearer {ANON_KEY}",
    "Content-Type": "application/json"
}

print("=" * 60)
print("📊 VERIFICANDO ESTADO DE LA BASE DE DATOS")
print("=" * 60)

# 1. Verificar tabla users
print("\n1️⃣ Tabla USERS:")
try:
    response = requests.get(
        f"{SUPABASE_URL}/rest/v1/users?limit=5",
        headers=headers
    )
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Usuarios: {len(data)}")
        if data:
            print(f"   Columnas: {list(data[0].keys())}")
    else:
        print(f"   ❌ Error: {response.text[:200]}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# 2. Verificar recetas
print("\n2️⃣ Tabla MASTER_RECIPES:")
try:
    response = requests.get(
        f"{SUPABASE_URL}/rest/v1/master_recipes?select=id,name,meal_type",
        headers=headers
    )
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Recetas totales: {len(data)}")
        
        # Contar por tipo
        tipos = {}
        for receta in data:
            tipo = receta.get('meal_type', 'unknown')
            tipos[tipo] = tipos.get(tipo, 0) + 1
        
        print(f"   Por tipo:")
        for tipo, count in sorted(tipos.items()):
            print(f"      - {tipo}: {count}")
    else:
        print(f"   ❌ Error: {response.text[:200]}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# 3. Verificar user_profiles
print("\n3️⃣ Tabla USER_PROFILES:")
try:
    response = requests.get(
        f"{SUPABASE_URL}/rest/v1/user_profiles?limit=5",
        headers=headers
    )
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Perfiles: {len(data)}")
    else:
        print(f"   ❌ Error: {response.text[:200]}")
except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n" + "=" * 60)
print("✅ Verificación completada")
print("=" * 60)