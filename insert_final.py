#!/usr/bin/env python3
"""
Insertar 200 recetas usando Service Role Key JWT
"""
import requests
import re

# Service Role Key JWT (bypass RLS)
SUPABASE_URL = "https://kaomgwojvnncidyezdzj.supabase.co"
SERVICE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imthb21nd29qdm5uY2lkeWV6ZHpqIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MjcwNzE3NiwiZXhwIjoyMDg4MjgzMTc2fQ.g9dMyRLD6sK6WeQGywhQaTRAdfu48CG8GW8Va2gmwxk"

headers = {
    "apikey": SERVICE_KEY,
    "Authorization": f"Bearer {SERVICE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=minimal"
}

# Leer archivo SQL
print("📖 Leyendo archivo SQL...")
with open('/Users/servimac/.openclaw/workspace/diet-tracker-app/insert_200_recipes.sql', 'r') as f:
    sql_content = f.read()

# Extraer recetas
pattern = r"\('([^']*)',\s*'([^']*)',\s*'([^']*)',\s*'([^']*)',\s*(\d+),\s*(\d+),\s*(\d+),\s*(\d+),\s*(\d+),\s*(\d+),\s*(\d+),\s*'([^']*)'\)"
matches = re.findall(pattern, sql_content)
print(f"📊 Recetas encontradas: {len(matches)}")

if matches:
    recipes = []
    for m in matches:
        recipe = {
            "name": m[0],
            "description": m[1],
            "meal_type": m[2],
            "supermarket": m[3],
            "calories": int(m[4]),
            "protein_g": int(m[5]),
            "carbs_g": int(m[6]),
            "fat_g": int(m[7]),
            "fiber_g": int(m[8]),
            "prep_time_min": int(m[9]),
            "servings": int(m[10]),
            "image_url": m[11]
        }
        recipes.append(recipe)
    
    print(f"✅ Recetas procesadas: {len(recipes)}")
    
    # Insertar en lotes de 50
    batch_size = 50
    total_inserted = 0
    
    for i in range(0, len(recipes), batch_size):
        batch = recipes[i:i+batch_size]
        print(f"\n🔄 Insertando lote {i//batch_size + 1}/{(len(recipes) + batch_size - 1)//batch_size} ({len(batch)} recetas)...")
        
        try:
            response = requests.post(
                f"{SUPABASE_URL}/rest/v1/master_recipes",
                headers=headers,
                json=batch
            )
            
            if response.status_code == 201:
                total_inserted += len(batch)
                print(f"   ✅ Insertadas {len(batch)} recetas (total: {total_inserted})")
            else:
                print(f"   ❌ Error {response.status_code}: {response.text[:200]}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    # Verificar total
    print("\n📊 Verificando total de recetas...")
    response = requests.get(
        f"{SUPABASE_URL}/rest/v1/master_recipes?select=id",
        headers={"apikey": SERVICE_KEY, "Authorization": f"Bearer {SERVICE_KEY}"}
    )
    total_in_db = len(response.json())
    
    print(f"\n" + "=" * 60)
    print(f"📊 RESUMEN FINAL")
    print(f"=" * 60)
    print(f"   Recetas en SQL: {len(recipes)}")
    print(f"   Recetas insertadas: {total_inserted}")
    print(f"   Total en DB: {total_in_db}")
    print(f"=" * 60)