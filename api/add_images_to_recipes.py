#!/usr/bin/env python3
"""Agregar imágenes a recetas maestras usando fakeimg.pl placeholder."""

import os
from supabase import create_client
from dotenv import load_dotenv
import urllib.parse

load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Obtener todas las recetas
print("📋 Obteniendo recetas...")
result = supabase.table('master_recipes').select('id, name, meal_type').execute()
recipes = result.data
print(f"✅ {len(recipes)} recetas encontradas")

# Colores por tipo de comida
color_map = {
    'desayuno': 'FFB347',  # naranja claro
    'comida': '4CAF50',    # verde
    'cena': '2196F3'       # azul
}

updated = 0
for recipe in recipes:
    recipe_id = recipe['id']
    name = recipe['name']
    meal_type = recipe['meal_type']
    
    # Crear texto para imagen (limitar longitud)
    text = urllib.parse.quote(name[:30])
    color = color_map.get(meal_type, '6A5ACD')
    
    # URL de placeholder con fakeimg.pl (400x300, color de fondo, texto blanco)
    image_url = f"https://fakeimg.pl/400x300/{color}/FFFFFF/?font_size=20&text={text}"
    
    print(f"  🖼️ {recipe_id}: {name} -> {image_url[:60]}...")
    
    # Actualizar receta
    try:
        supabase.table('master_recipes').update({'image_url': image_url}).eq('id', recipe_id).execute()
        updated += 1
    except Exception as e:
        print(f"    ❌ Error actualizando receta {recipe_id}: {e}")

print(f"\n🎉 {updated} recetas actualizadas con imágenes.")