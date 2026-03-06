#!/usr/bin/env python3
"""
Insertar 200 recetas en Supabase via API REST
"""
import requests
import json
import re

# Credenciales de Supabase
SUPABASE_URL = "https://kaomgwojvnncidyezdzj.supabase.co"
ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imthb21nd29qdm5uY2lkeWV6ZHpqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzI3MDcxNzYsImV4cCI6MjA4ODI4MzE3Nn0.Ds2ICxfiahuqt2n83dwoX9tMYGf7Xz8Jjvx6lFJc4zs"

headers = {
    "apikey": ANON_KEY,
    "Authorization": f"Bearer {ANON_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=minimal"
}

# Leer archivo SQL
print("📖 Leyendo archivo SQL...")
with open('/Users/servimac/.openclaw/workspace/diet-tracker-app/insert_200_recipes.sql', 'r') as f:
    sql_content = f.read()

# Extraer recetas del SQL
# Formato: ('nombre', 'descripción', 'meal_type', 'supermercado', calorias, proteinas, carbs, grasa, fibra, tiempo, raciones, 'url_imagen')

pattern = r"\('([^']*)',\s*'([^']*)',\s*'([^']*)',\s*'([^']*)',\s*(\d+),\s*(\d+),\s*(\d+),\s*(\d+),\s*(\d+),\s*(\d+),\s*(\d+),\s*'([^']*)'\)"

matches = re.findall(pattern, sql_content)
print(f"📊 Recetas encontradas en SQL: {len(matches)}")

if matches:
    # Convertir a formato JSON
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
                # Intentar insertar una por una
                for recipe in batch:
                    try:
                        r = requests.post(
                            f"{SUPABASE_URL}/rest/v1/master_recipes",
                            headers=headers,
                            json=recipe
                        )
                        if r.status_code == 201:
                            total_inserted += 1
                        else:
                            print(f"      ❌ Error en '{recipe['name']}': {r.status_code}")
                    except Exception as e:
                        print(f"      ❌ Error: {e}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print(f"\n" + "=" * 60)
    print(f"📊 RESUMEN FINAL")
    print(f"=" * 60)
    print(f"   Recetas en SQL: {len(recipes)}")
    print(f"   Recetas insertadas: {total_inserted}")
    print(f"=" * 60)
else:
    print("❌ No se encontraron recetas en el archivo SQL")
    print("   Intentando con otro patrón...")
    
    # Intentar con otro patrón más flexible
    lines = sql_content.split('\n')
    recipe_lines = [l for l in lines if l.strip().startswith('(') and 'VALUES' not in l.upper()]
    print(f"   Líneas de recetas encontradas: {len(recipe_lines)}")