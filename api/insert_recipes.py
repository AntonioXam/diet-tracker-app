#!/usr/bin/env python3
"""Insertar recetas maestras en Supabase."""

import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Recetas maestras (copiadas de setup_db.py)
recipes = [
    {'name': 'Tostada con aguacate y huevo', 'meal_type': 'desayuno', 'calories': 350, 'protein': 15, 'carbs': 30, 'fat': 18, 'ingredients': 'Pan de molde integral Hacendado/Lidl (2 rebanadas), Aguacate (1/2), Huevo L Hacendado (1), Aceite de oliva', 'instructions': 'Tostar pan, machacar aguacate, hacer huevo', 'supermarket': 'mixto', 'category': 'salado'},
    {'name': 'Yogur con avena y frutas', 'meal_type': 'desayuno', 'calories': 320, 'protein': 18, 'carbs': 45, 'fat': 8, 'ingredients': 'Queso fresco batido 0% Hacendado (150g), Avena Lidl (40g), Plátano, Miel', 'instructions': 'Mezclar todo en bol', 'supermarket': 'mixto', 'category': 'dulce'},
    {'name': 'Batido de proteínas', 'meal_type': 'desayuno', 'calories': 280, 'protein': 25, 'carbs': 30, 'fat': 6, 'ingredients': 'Proteína whey Powerbar/Lidl (30g), Leche desnatada Hacendado (200ml), Plátano (1/2)', 'instructions': 'Batir todo', 'supermarket': 'mixto', 'category': 'batido'},
    {'name': 'Tortilla francesa', 'meal_type': 'desayuno', 'calories': 340, 'protein': 20, 'carbs': 25, 'fat': 16, 'ingredients': 'Huevos L Hacendado (2), Pan integral Lidl (1), Aceite de oliva', 'instructions': 'Hacer tortilla francesa', 'supermarket': 'mixto', 'category': 'salado'},
    {'name': 'Porridge de avena', 'meal_type': 'desayuno', 'calories': 310, 'protein': 12, 'carbs': 52, 'fat': 7, 'ingredients': 'Avena Lidl (50g), Leche Hacendado (200ml), Canela, Manzana', 'instructions': 'Cocer 5 min con leche', 'supermarket': 'mixto', 'category': 'dulce'},
    {'name': 'Requesón con frutos rojos', 'meal_type': 'desayuno', 'calories': 290, 'protein': 22, 'carbs': 28, 'fat': 9, 'ingredients': 'Requesón light Hacendado (150g), Fresas Lidl (100g), Nueces (20g)', 'instructions': 'Mezclar todo', 'supermarket': 'mixto', 'category': 'dulce'},
    {'name': 'Manzana con almendras', 'meal_type': 'almuerzo', 'calories': 180, 'protein': 5, 'carbs': 25, 'fat': 8, 'ingredients': 'Manzana Golden, Almendras Lidl (20g)', 'instructions': 'Comer juntos', 'supermarket': 'mixto', 'category': 'snack'},
    {'name': 'Yogur griego', 'meal_type': 'almuerzo', 'calories': 120, 'protein': 15, 'carbs': 8, 'fat': 3, 'ingredients': 'Yogur griego Hacendado (125g)', 'instructions': 'Consumir directo', 'supermarket': 'mercadona', 'category': 'lácteo'},
    {'name': 'Zanahoria con hummus', 'meal_type': 'almuerzo', 'calories': 150, 'protein': 6, 'carbs': 18, 'fat': 7, 'ingredients': 'Zanahorias (100g), Hummus Hacendado (50g)', 'instructions': 'Cortar zanahorias', 'supermarket': 'mixto', 'category': 'salado'},
    {'name': 'Barrita proteica', 'meal_type': 'almuerzo', 'calories': 200, 'protein': 20, 'carbs': 15, 'fat': 6, 'ingredients': 'Barrita Powerbar/Lidl (45g)', 'instructions': 'Consumir directo', 'supermarket': 'mixto', 'category': 'snack'},
    {'name': 'Queso con nueces', 'meal_type': 'almuerzo', 'calories': 160, 'protein': 12, 'carbs': 5, 'fat': 11, 'ingredients': 'Queso 0% Hacendado (100g), Nueces Lidl (15g)', 'instructions': 'Mezclar', 'supermarket': 'mixto', 'category': 'lácteo'},
    {'name': 'Pan con tomate', 'meal_type': 'almuerzo', 'calories': 140, 'protein': 5, 'carbs': 22, 'fat': 4, 'ingredients': 'Pan Lidl (1), Tomate (1/2), Aceite Hacendado', 'instructions': 'Tostar y rallar tomate', 'supermarket': 'mixto', 'category': 'salado'},
    {'name': 'Pollo al horno', 'meal_type': 'comida', 'calories': 450, 'protein': 40, 'carbs': 35, 'fat': 15, 'ingredients': 'Pechuga pollo Hacendado (150g), Patata (150g), Brócoli (100g)', 'instructions': 'Hornear 25 min a 200°C', 'supermarket': 'mixto', 'category': 'proteina'},
    {'name': 'Salmón con arroz', 'meal_type': 'comida', 'calories': 480, 'protein': 35, 'carbs': 45, 'fat': 18, 'ingredients': 'Salmón Lidl (150g), Arroz Hacendado (60g), Espárragos', 'instructions': 'Cocer arroz, plancha salmón', 'supermarket': 'mixto', 'category': 'pescado'},
    {'name': 'Lentejas estofadas', 'meal_type': 'comida', 'calories': 420, 'protein': 18, 'carbs': 55, 'fat': 12, 'ingredients': 'Lentejas Lidl (70g), Zanahoria, Cebolla, Pimiento', 'instructions': 'Cocer 25-30 min', 'supermarket': 'lidl', 'category': 'legumbre'},
    {'name': 'Pasta con atún', 'meal_type': 'comida', 'calories': 440, 'protein': 30, 'carbs': 50, 'fat': 12, 'ingredients': 'Pasta Lidl (80g), Atún Hacendado (2 latas), Tomate', 'instructions': 'Cocer pasta y mezclar', 'supermarket': 'mixto', 'category': 'pasta'},
    {'name': 'Ternera con boniato', 'meal_type': 'comida', 'calories': 470, 'protein': 38, 'carbs': 40, 'fat': 16, 'ingredients': 'Ternera Hacendado (150g), Boniato (200g), Judías', 'instructions': 'Hornear boniato 40 min', 'supermarket': 'mixto', 'category': 'proteina'},
    {'name': 'Ensalada garbanzos', 'meal_type': 'comida', 'calories': 400, 'protein': 20, 'carbs': 48, 'fat': 14, 'ingredients': 'Garbanzos Lidl (200g), Cherry, Pepino, Atún Hacendado', 'instructions': 'Mezclar todo', 'supermarket': 'mixto', 'category': 'ensalada'},
    {'name': 'Yogur con kiwi', 'meal_type': 'merienda', 'calories': 150, 'protein': 10, 'carbs': 22, 'fat': 3, 'ingredients': 'Yogur Hacendado (125g), Kiwi (1)', 'instructions': 'Mezclar', 'supermarket': 'mixto', 'category': 'lácteo'},
    {'name': 'Tostada jamón', 'meal_type': 'merienda', 'calories': 180, 'protein': 15, 'carbs': 18, 'fat': 5, 'ingredients': 'Pan Lidl (1), Jamón Hacendado (2 lonchas)', 'instructions': 'Tostar pan', 'supermarket': 'mixto', 'category': 'salado'},
    {'name': 'Batido verde', 'meal_type': 'merienda', 'calories': 140, 'protein': 3, 'carbs': 32, 'fat': 1, 'ingredients': 'Plátano (1/2), Fresas Lidl (100g), Agua', 'instructions': 'Batir todo', 'supermarket': 'mixto', 'category': 'batido'},
    {'name': 'Huevos cocidos', 'meal_type': 'merienda', 'calories': 140, 'protein': 12, 'carbs': 1, 'fat': 10, 'ingredients': 'Huevos Hacendado (2), Sal', 'instructions': 'Cocer 10 min', 'supermarket': 'mixto', 'category': 'proteina'},
    {'name': 'Requesón canela', 'meal_type': 'merienda', 'calories': 120, 'protein': 14, 'carbs': 8, 'fat': 4, 'ingredients': 'Requesón Hacendado (100g), Canela Lidl', 'instructions': 'Mezclar', 'supermarket': 'mixto', 'category': 'lácteo'},
    {'name': 'Surimi con pepino', 'meal_type': 'merienda', 'calories': 100, 'protein': 12, 'carbs': 10, 'fat': 1, 'ingredients': 'Surimi Lidl (80g), Pepino (1/2)', 'instructions': 'Cortar pepino', 'supermarket': 'mixto', 'category': 'snack'},
    {'name': 'Merluza al horno', 'meal_type': 'cena', 'calories': 320, 'protein': 30, 'carbs': 20, 'fat': 12, 'ingredients': 'Merluza Lidl (150g), Calabacín, Cebolla', 'instructions': 'Hornear 20 min', 'supermarket': 'mixto', 'category': 'pescado'},
    {'name': 'Tortilla espinacas', 'meal_type': 'cena', 'calories': 280, 'protein': 18, 'carbs': 8, 'fat': 20, 'ingredients': 'Huevos Hacendado (2), Espinacas Lidl (100g), Queso light', 'instructions': 'Hacer tortilla', 'supermarket': 'mixto', 'category': 'huevos'},
    {'name': 'Ensalada atún', 'meal_type': 'cena', 'calories': 300, 'protein': 28, 'carbs': 15, 'fat': 14, 'ingredients': 'Atún Hacendado (2 latas), Lechuga, Tomate, Maíz Lidl', 'instructions': 'Mezclar todo', 'supermarket': 'mixto', 'category': 'ensalada'},
    {'name': 'Sepia a la plancha', 'meal_type': 'cena', 'calories': 260, 'protein': 32, 'carbs': 10, 'fat': 8, 'ingredients': 'Sepia Lidl (200g), Ajo, Perejil', 'instructions': 'Plancha con ajo', 'supermarket': 'mixto', 'category': 'pescado'},
    {'name': 'Pavo con espárragos', 'meal_type': 'cena', 'calories': 290, 'protein': 35, 'carbs': 12, 'fat': 10, 'ingredients': 'Pavo Hacendado (150g), Espárragos Lidl (150g)', 'instructions': 'Plancha ambos', 'supermarket': 'mixto', 'category': 'proteina'},
    {'name': 'Crema calabacín', 'meal_type': 'cena', 'calories': 240, 'protein': 12, 'carbs': 25, 'fat': 10, 'ingredients': 'Calabacín (2), Puerro, Queso Hacendado (50g)', 'instructions': 'Cocer y triturar', 'supermarket': 'mixto', 'category': 'crema'},
]

print(f"📦 Insertando {len(recipes)} recetas maestras...")

try:
    # Verificar si ya existen recetas
    existing = supabase.table('master_recipes').select('id').execute()
    if not existing.data:
        for recipe in recipes:
            supabase.table('master_recipes').insert(recipe).execute()
        print(f"✅ {len(recipes)} recetas insertadas")
    else:
        print(f"✅ Ya existen {len(existing.data)} recetas (no se insertan nuevas)")
except Exception as e:
    print(f"⚠️ Error insertando recetas: {e}")
    import traceback
    traceback.print_exc()

print("\n🎉 ¡Recetas listas!")