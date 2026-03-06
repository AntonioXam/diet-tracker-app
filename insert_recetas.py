#!/usr/bin/env python3
"""
Script para insertar 200 recetas en Supabase
"""
import json
from supabase import create_client

# Credenciales
SUPABASE_URL = "https://kaomgwojvnncidyezdzj.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imthb21nd29qdm5uY2lkeWV6ZHpqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzI3MDcxNzYsImV4cCI6MjA4ODI4MzE3Nn0.Ds2ICxfiahuqt2n83dwoX9tMYGf7Xz8Jjvx6lFJc4zs"

# Inicializar cliente
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Cargar recetas
with open('content/recetas_seed.json', 'r') as f:
    data = json.load(f)

recetas = data['recetas']

print(f"Insertando {len(recetas)} recetas en Supabase...")

# Insertar cada receta
inserted = 0
for receta in recetas:
    try:
        result = supabase.table('master_recipes').insert({
            'name': receta['name'],
            'description': f"Receta saludable de {receta['name']}",
            'meal_type': receta['meal_type'],
            'supermarket': receta['supermarket'],
            'calories': receta['calories'],
            'protein_g': receta['protein_g'],
            'carbs_g': receta['carbs_g'],
            'fat_g': receta['fat_g'],
            'image_url': receta['image_url'],
            'prep_time_min': 20,
            'servings': 1
        }).execute()
        
        if result.data:
            inserted += 1
            print(f"✅ {receta['name']}")
        else:
            print(f"❌ Error: {receta['name']}")
            
    except Exception as e:
        print(f"❌ Error inserting {receta['name']}: {e}")

print(f"\n✅ {inserted}/{len(recetas)} recetas insertadas correctamente")

# Verificar
count_result = supabase.table('master_recipes').select('*', count='exact').execute()
print(f"📊 Total de recetas en DB: {count_result.count}")
