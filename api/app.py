#!/usr/bin/env python3
"""
Diet Tracker API - Backend con Supabase
Ingredientes Mercadona/Lidl - Sistema progresivo 6 opciones
"""

import os
import json
import hashlib
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuración Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ============================================================
# RECETAS MAESTRAS - Productos Hacendado/Lidl
# ============================================================

MASTER_RECIPES = [
    # DESAYUNOS (6 opciones)
    {"name": "Tostada con aguacate y huevo", "meal_type": "desayuno", "calories": 350, "protein": 15, "carbs": 30, "fat": 18,
     "ingredients": "Pan de molde integral Hacendado/Lidl (2 rebanadas), Aguacate (1/2 unidad), Huevo L Hacendado (1 unidad), Aceite de oliva virgen extra",
     "instructions": "Tostar el pan, machacar el aguacate con sal, hacer huevo poché o revuelto", "supermarket": "mixto", "category": "salado"},
    
    {"name": "Yogur con avena y frutas", "meal_type": "desayuno", "calories": 320, "protein": 18, "carbs": 45, "fat": 8,
     "ingredients": "Queso fresco batido 0% Hacendado (150g), Copos de avena Lidl (40g), Plátano (1 unidad), Miel (1 cucharada)",
     "instructions": "Mezclar queso fresco con avena, añadir plátano troceado y miel", "supermarket": "mixto", "category": "dulce"},
    
    {"name": "Batido de proteínas casero", "meal_type": "desayuno", "calories": 280, "protein": 25, "carbs": 30, "fat": 6,
     "ingredients": "Proteína whey Powerbar/Lidl (30g), Leche desnatada Hacendado (200ml), Plátano (1/2 unidad)",
     "instructions": "Batir todo hasta que quede homogéneo", "supermarket": "mixto", "category": "batido"},
    
    {"name": "Tortilla francesa con pan tostado", "meal_type": "desayuno", "calories": 340, "protein": 20, "carbs": 25, "fat": 16,
     "ingredients": "Huevos L Hacendado/Lidl (2 unidades), Pan integral de centeno Lidl (1 rebanada), Aceite de oliva (1 cucharadita)",
     "instructions": "Batir huevos con sal, hacer tortilla francesa con poco aceite", "supermarket": "mixto", "category": "salado"},
    
    {"name": "Porridge de avena con manzana", "meal_type": "desayuno", "calories": 310, "protein": 12, "carbs": 52, "fat": 7,
     "ingredients": "Copos de avena finos Lidl (50g), Leche semidesnatada Hacendado (200ml), Canela molida, Manzana Fuji",
     "instructions": "Cocer avena con leche 5 minutos, añadir canela y manzana troceada", "supermarket": "mixto", "category": "dulce"},
    
    {"name": "Requesón con frutos rojos y nueces", "meal_type": "desayuno", "calories": 290, "protein": 22, "carbs": 28, "fat": 9,
     "ingredients": "Requesón light Hacendado (150g), Fresas congeladas Lidl (100g), Nueces peladas (20g), Edulcorante",
     "instructions": "Mezclar requesón con frutos rojos y nueces troceadas", "supermarket": "mixto", "category": "dulce"},
    
    # ALMUERZOS (6 opciones)
    {"name": "Manzana con almendras", "meal_type": "almuerzo", "calories": 180, "protein": 5, "carbs": 25, "fat": 8,
     "ingredients": "Manzana Golden (1 unidad), Almendras crudas sin sal Lidl (20g)",
     "instructions": "Lavar manzana y comer con las almendras", "supermarket": "mixto", "category": "snack"},
    
    {"name": "Yogur griego natural", "meal_type": "almuerzo", "calories": 120, "protein": 15, "carbs": 8, "fat": 3,
     "ingredients": "Yogur griego natural sin azúcar Hacendado (125g)",
     "instructions": "Consumir directamente", "supermarket": "mercadona", "category": "lácteo"},
    
    {"name": "Zanahoria con hummus", "meal_type": "almuerzo", "calories": 150, "protein": 6, "carbs": 18, "fat": 7,
     "ingredients": "Zanahorias frescas (100g), Hummus clásico Hacendado (50g)",
     "instructions": "Cortar zanahorias en bastones y acompañar con hummus", "supermarket": "mixto", "category": "salado"},
    
    {"name": "Barrita proteica", "meal_type": "almuerzo", "calories": 200, "protein": 20, "carbs": 15, "fat": 6,
     "ingredients": "Barrita proteica Powerbar/Lidl (45g)",
     "instructions": "Consumir directamente", "supermarket": "mixto", "category": "snack"},
    
    {"name": "Queso fresco con nueces", "meal_type": "almuerzo", "calories": 160, "protein": 12, "carbs": 5, "fat": 11,
     "ingredients": "Queso fresco 0% Hacendado (100g), Nueces peladas Lidl (15g)",
     "instructions": "Acompañar queso con nueces troceadas", "supermarket": "mixto", "category": "lácteo"},
    
    {"name": "Pan con tomate", "meal_type": "almuerzo", "calories": 140, "protein": 5, "carbs": 22, "fat": 4,
     "ingredients": "Pan de pueblo integral Lidl (1 rebanada), Tomate de ensalada (1/2), Aceite de oliva virgen extra Hacendado, Sal",
     "instructions": "Tostar pan, rallar tomate, añadir aceite y sal", "supermarket": "mixto", "category": "salado"},
    
    # COMIDAS (6 opciones)
    {"name": "Pollo al horno con verduras", "meal_type": "comida", "calories": 450, "protein": 40, "carbs": 35, "fat": 15,
     "ingredients": "Pechuga de pollo fresca Hacendado/Lidl (150g), Patata mediana (150g), Brócoli fresco (100g), Aceite de oliva virgen extra, Sal, Pimienta",
     "instructions": "Hornear a 200°C durante 25-30 minutos con verduras cortadas", "supermarket": "mixto", "category": "proteina"},
    
    {"name": "Salmón con arroz integral", "meal_type": "comida", "calories": 480, "protein": 35, "carbs": 45, "fat": 18,
     "ingredients": "Filete de salmón fresco Lidl (150g), Arroz integral Hacendado (60g en crudo), Espárragos trigueros (100g), Limón",
     "instructions": "Cocer arroz 25 min. Hacer salmón a la plancha 4 min por lado. Saltear espárragos.", "supermarket": "mixto", "category": "pescado"},
    
    {"name": "Lentejas estofadas con verduras", "meal_type": "comida", "calories": 420, "protein": 18, "carbs": 55, "fat": 12,
     "ingredients": "Lentejas pardinas Lidl (70g en crudo), Zanahoria (1 unidad), Cebolla (1/2), Pimiento verde (1/2), Laurel",
     "instructions": "Sofreír verduras, añadir lentejas y cubrir con agua. Cocer 25-30 min.", "supermarket": "lidl", "category": "legumbre"},
    
    {"name": "Pasta integral con atún", "meal_type": "comida", "calories": 440, "protein": 30, "carbs": 50, "fat": 12,
     "ingredients": "Espaguetis integrales Lidl (80g en crudo), Atún al natural Hacendado (2 latas de 52g), Tomate triturado Hacendado (50g), Orégano",
     "instructions": "Cocer pasta. Mezclar con atún escurrido y tomate. Calentar 2 min.", "supermarket": "mixto", "category": "pasta"},
    
    {"name": "Ternera con boniato asado", "meal_type": "comida", "calories": 470, "protein": 38, "carbs": 40, "fat": 16,
     "ingredients": "Filete de ternera magra Hacendado (150g), Boniato mediano (200g), Judías verdes (100g), Aceite de oliva virgen extra",
     "instructions": "Hornear boniato 40-45 min a 200°C. Hacer ternera a la plancha. Cocer judías 10 min.", "supermarket": "mixto", "category": "proteina"},
    
    {"name": "Ensalada de garbanzos", "meal_type": "comida", "calories": 400, "protein": 20, "carbs": 48, "fat": 14,
     "ingredients": "Garbanzos cocidos Lidl (200g), Tomates cherry (100g), Pepino (1/2), Atún al natural Hacendado (1 lata), Aceitunas negras, Aceite de oliva",
     "instructions": "Mezclar todos los ingredientes en un bol y aliñar", "supermarket": "mixto", "category": "ensalada"},
    
    # MERIENDAS (6 opciones)
    {"name": "Yogur con kiwi", "meal_type": "merienda", "calories": 150, "protein": 10, "carbs": 22, "fat": 3,
     "ingredients": "Yogur natural sin azúcar Hacendado (125g), Kiwi maduro (1 unidad)",
     "instructions": "Pelar y trocear kiwi, mezclar con yogur", "supermarket": "mixto", "category": "lácteo"},
    
    {"name": "Tostada con jamón cocido", "meal_type": "merienda", "calories": 180, "protein": 15, "carbs": 18, "fat": 5,
     "ingredients": "Pan de molde integral Lidl (1 rebanada), Jamón cocido extra Hacendado (2 lonchas, 60g)",
     "instructions": "Tostar pan y colocar jamón", "supermarket": "mixto", "category": "salado"},
    
    {"name": "Batido verde", "meal_type": "merienda", "calories": 140, "protein": 3, "carbs": 32, "fat": 1,
     "ingredients": "Plátano (1/2), Fresas Lidl (100g), Agua (200ml)",
     "instructions": "Batir todo hasta textura suave", "supermarket": "mixto", "category": "batido"},
    
    {"name": "Huevos cocidos", "meal_type": "merienda", "calories": 140, "protein": 12, "carbs": 1, "fat": 10,
     "ingredients": "Huevos L Hacendado/Lidl (2 unidades), Sal",
     "instructions": "Cocer 10 minutos desde que hierve el agua", "supermarket": "mixto", "category": "proteina"},
    
    {"name": "Requesón con canela", "meal_type": "merienda", "calories": 120, "protein": 14, "carbs": 8, "fat": 4,
     "ingredients": "Requesón light Hacendado (100g), Canela molida Lidl, Edulcorante líquido",
     "instructions": "Mezclar requesón con canela y edulcorante", "supermarket": "mixto", "category": "lácteo"},
    
    {"name": "Surimi con pepino", "meal_type": "merienda", "calories": 100, "protein": 12, "carbs": 10, "fat": 1,
     "ingredients": "Palitos de cangrejo/surimi Lidl (80g), Pepino (1/2 unidad)",
     "instructions": "Cortar pepino en bastones y acompañar con surimi", "supermarket": "mixto", "category": "snack"},
    
    # CENAS (6 opciones)
    {"name": "Merluza al horno con verduras", "meal_type": "cena", "calories": 320, "protein": 30, "carbs": 20, "fat": 12,
     "ingredients": "Filete de merluza Lidl (150g), Calabacín mediano (1 unidad), Cebolla (1/2), Aceite de oliva virgen extra Hacendado",
     "instructions": "Hornear 20 min a 180°C con verduras en rodajas", "supermarket": "mixto", "category": "pescado"},
    
    {"name": "Tortilla de espinacas", "meal_type": "cena", "calories": 280, "protein": 18, "carbs": 8, "fat": 20,
     "ingredients": "Huevos L Hacendado (2 unidades), Espinacas congeladas Lidl (100g), Queso light Hacendado (1 loncha)",
     "instructions": "Hacer tortilla con espinacas salteadas y queso", "supermarket": "mixto", "category": "huevos"},
    
    {"name": "Ensalada de atún", "meal_type": "cena", "calories": 300, "protein": 28, "carbs": 15, "fat": 14,
     "ingredients": "Atún al natural Hacendado (2 latas de 52g), Lechuga iceberg (100g), Tomate (1 unidad), Maíz dulce Lidl (30g)",
     "instructions": "Mezclar todos los ingredientes y aliñar", "supermarket": "mixto", "category": "ensalada"},
    
    {"name": "Sepia a la plancha", "meal_type": "cena", "calories": 260, "protein": 32, "carbs": 10, "fat": 8,
     "ingredients": "Sepia fresca Lidl (200g), Ajo (2 dientes), Perejil fresco, Aceite de oliva virgen extra",
     "instructions": "Hacer sepia a la plancha con ajo y perejil picado", "supermarket": "mixto", "category": "pescado"},
    
    {"name": "Pavo a la plancha con espárragos", "meal_type": "cena", "calories": 290, "protein": 35, "carbs": 12, "fat": 10,
     "ingredients": "Filete de pechuga de pavo Hacendado (150g), Espárragos trigueros Lidl (150g), Limón",
     "instructions": "Hacer pavo y espárragos a la plancha, servir con limón", "supermarket": "mixto", "category": "proteina"},
    
    {"name": "Crema de calabacín", "meal_type": "cena", "calories": 240, "protein": 12, "carbs": 25, "fat": 10,
     "ingredients": "Calabacín mediano (2 unidades), Puerro (1 unidad), Queso fresco Hacendado (50g), Aceite de oliva virgen extra",
     "instructions": "Cocer verduras 15 min, triturar y añadir queso", "supermarket": "mixto", "category": "crema"},
]

# ============================================================
# UTILIDADES
# ============================================================

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def calculate_tmb(age, gender, height, weight, activity_level):
    """Tasa Metabólica Basal - fórmula Mifflin-St Jeor."""
    if gender == 'male':
        tmb = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        tmb = 10 * weight + 6.25 * height - 5 * age - 161
    
    multipliers = {'sedentary': 1.2, 'light': 1.375, 'moderate': 1.55, 'active': 1.725, 'very_active': 1.9}
    return round(tmb), round(tmb * multipliers.get(activity_level, 1.2))

def calculate_deficit(tdee, goal_type, current_weight, goal_weight):
    if goal_type == 'lose':
        return tdee - min(500, 300 + (current_weight - goal_weight) * 20)
    elif goal_type == 'gain':
        return tdee + 300
    return tdee

def get_week_number():
    return datetime.now().isocalendar()[1]

def seed_recipes():
    """Inserta recetas maestras si están vacías."""
    try:
        existing = supabase.table('master_recipes').select('id').execute()
        if not existing.data:
            for recipe in MASTER_RECIPES:
                supabase.table('master_recipes').insert(recipe).execute()
        print(f"✅ Recetas cargadas: {len(MASTER_RECIPES)}")
    except Exception as e:
        print(f"⚠️ Error seed recipes: {e}")

# ============================================================
# API ENDPOINTS
# ============================================================

@app.route('/api/health')
def health():
    return jsonify({'status': 'ok', 'timestamp': datetime.now().isoformat()})

@app.route('/api/register', methods=['POST'])
def register():
    try:
        data = request.json
        if not all(k in data for k in ('email', 'password', 'name')):
            return jsonify({'error': 'Datos incompletos'}), 400
        
        # Verificar si existe
        existing = supabase.table('users').select('id').eq('email', data['email']).execute()
        if existing.data:
            return jsonify({'error': 'Email ya registrado'}), 400
        
        # Crear usuario
        result = supabase.table('users').insert({
            'email': data['email'],
            'password_hash': hash_password(data['password']),
            'name': data['name']
        }).execute()
        
        return jsonify({'success': True, 'user_id': result.data[0]['id']})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.json
        result = supabase.table('users').select('id, name').eq('email', data.get('email')).eq('password_hash', hash_password(data.get('password', ''))).execute()
        
        if result.data:
            return jsonify({'success': True, 'user_id': result.data[0]['id'], 'name': result.data[0]['name']})
        return jsonify({'error': 'Credenciales inválidas'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/profile', methods=['POST'])
def save_profile():
    try:
        data = request.json
        user_id = data.get('user_id')
        if not user_id:
            return jsonify({'error': 'user_id requerido'}), 400
        
        # Guardar perfil
        supabase.table('user_profiles').upsert({
            'user_id': user_id,
            'age': data['age'],
            'gender': data['gender'],
            'height_cm': data['height'],
            'current_weight_kg': data['current_weight'],
            'goal_weight_kg': data['goal_weight'],
            'activity_level': data['activity_level'],
            'meals_per_day': data['meals_per_day'],
            'allergies': data.get('allergies', ''),
            'disliked_foods': data.get('disliked_foods', ''),
            'goal_type': data['goal_type']
        }).execute()
        
        # Guardar peso inicial
        supabase.table('weight_history').insert({
            'user_id': user_id,
            'weight_kg': data['current_weight'],
            'week_number': get_week_number()
        }).execute()
        
        # Calcular calorías
        tmb, tdee = calculate_tmb(data['age'], data['gender'], data['height'], data['current_weight'], data['activity_level'])
        target = calculate_deficit(tdee, data['goal_type'], data['current_weight'], data['goal_weight'])
        
        # Generar primera semana
        generate_first_week(user_id, target, data['meals_per_day'])
        
        return jsonify({'success': True, 'tmb': tmb, 'tdee': tdee, 'target_calories': int(target)})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def generate_first_week(user_id, target_calories, meals_per_day):
    """Genera la primera semana con 1 opción por comida."""
    week = get_week_number()
    meal_types = ['desayuno', 'almuerzo', 'comida', 'merienda', 'cena'][:meals_per_day]
    
    for day in range(1, 8):
        for meal_type in meal_types:
            # Obtener receta aleatoria
            recipe_result = supabase.table('master_recipes').select('*').eq('meal_type', meal_type).order('id', desc=False).limit(1).execute()
            if recipe_result.data:
                recipe = recipe_result.data[0]
                
                # Insertar en plan semanal
                supabase.table('weekly_plans').insert({
                    'user_id': user_id,
                    'week_number': week,
                    'day_of_week': day,
                    'meal_type': meal_type,
                    'selected_recipe_id': recipe['id'],
                    'calories': recipe['calories'],
                    'protein': recipe['protein'],
                    'carbs': recipe['carbs'],
                    'fat': recipe['fat']
                }).execute()
                
                # Añadir al banco de comidas
                supabase.table('user_food_bank').insert({
                    'user_id': user_id,
                    'meal_type': meal_type,
                    'recipe_id': recipe['id'],
                    'added_week': week
                }).execute()

@app.route('/api/plan/current', methods=['GET'])
def get_current_plan():
    try:
        user_id = request.args.get('user_id')
        if not user_id:
            return jsonify({'error': 'user_id requerido'}), 400
        
        week = get_week_number()
        
        # Obtener plan con detalles de recetas
        result = supabase.table('weekly_plans').select('''
            *,
            master_recipes!inner(
                id, name, ingredients, instructions, supermarket, category
            )
        ''').eq('user_id', user_id).eq('week_number', week).eq('master_recipes.id', 'weekly_plans.selected_recipe_id').execute()
        
        # Calcular totales diarios
        daily = {}
        meals = []
        for row in result.data:
            recipe = row.get('master_recipes', {})
            meal = {
                'id': row['id'],
                'day_of_week': row['day_of_week'],
                'meal_type': row['meal_type'],
                'recipe_id': row['selected_recipe_id'],
                'recipe_name': recipe.get('name', ''),
                'ingredients': recipe.get('ingredients', ''),
                'instructions': recipe.get('instructions', ''),
                'supermarket': recipe.get('supermarket', ''),
                'calories': row['calories'],
                'protein': row['protein'],
                'carbs': row['carbs'],
                'fat': row['fat']
            }
            meals.append(meal)
            
            d = row['day_of_week']
            if d not in daily:
                daily[d] = {'calories': 0, 'protein': 0, 'carbs': 0, 'fat': 0}
            daily[d]['calories'] += row['calories'] or 0
            daily[d]['protein'] += row['protein'] or 0
            daily[d]['carbs'] += row['carbs'] or 0
            daily[d]['fat'] += row['fat'] or 0
        
        return jsonify({'week': week, 'meals': meals, 'daily_totals': daily})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/food-bank/options', methods=['GET'])
def get_food_bank():
    try:
        user_id = request.args.get('user_id')
        meal_type = request.args.get('meal_type')
        if not user_id:
            return jsonify({'error': 'user_id requerido'}), 400
        
        query = supabase.table('user_food_bank').select('''
            *,
            master_recipes!inner(
                id, name, meal_type, calories, protein, carbs, fat, ingredients, supermarket
            )
        ''').eq('user_id', user_id)
        
        if meal_type:
            query = query.eq('meal_type', meal_type)
        
        result = query.execute()
        
        options = []
        for row in result.data:
            recipe = row.get('master_recipes', {})
            options.append({
                'id': row['id'],
                'recipe_id': row['recipe_id'],
                'meal_type': row['meal_type'],
                'times_used': row['times_used'],
                'added_week': row['added_week'],
                'name': recipe.get('name', ''),
                'calories': recipe.get('calories', 0),
                'protein': recipe.get('protein', 0),
                'carbs': recipe.get('carbs', 0),
                'fat': recipe.get('fat', 0),
                'ingredients': recipe.get('ingredients', ''),
                'supermarket': recipe.get('supermarket', '')
            })
        
        return jsonify({'options': options})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/plan/swap', methods=['POST'])
def swap_meal():
    try:
        data = request.json
        recipe = supabase.table('master_recipes').select('*').eq('id', data['new_recipe_id']).execute()
        if not recipe.data:
            return jsonify({'error': 'Receta no encontrada'}), 404
        
        recipe = recipe.data[0]
        week = get_week_number()
        
        # Actualizar plan
        supabase.table('weekly_plans').update({
            'selected_recipe_id': data['new_recipe_id'],
            'calories': recipe['calories'],
            'protein': recipe['protein'],
            'carbs': recipe['carbs'],
            'fat': recipe['fat']
        }).eq('user_id', data['user_id']).eq('week_number', week).eq('day_of_week', data['day']).eq('meal_type', data['meal_type']).execute()
        
        # Actualizar contador de uso
        supabase.rpc('increment_recipe_usage', {'p_user_id': data['user_id'], 'p_recipe_id': data['new_recipe_id']}).execute()
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/weight/checkin', methods=['POST'])
def weight_checkin():
    try:
        data = request.json
        week = get_week_number()
        
        # Guardar peso
        supabase.table('weight_history').insert({
            'user_id': data['user_id'],
            'weight_kg': data['weight'],
            'week_number': week
        }).execute()
        
        # Obtener perfil
        profile = supabase.table('user_profiles').select('*').eq('user_id', data['user_id']).execute()
        if not profile.data:
            return jsonify({'error': 'Perfil no encontrado'}), 404
        
        profile = profile.data[0]
        
        # Añadir nueva opción por cada tipo de comida (máximo 6)
        meal_types = ['desayuno', 'almuerzo', 'comida', 'merienda', 'cena'][:profile['meals_per_day']]
        
        for meal_type in meal_types:
            # Contar opciones existentes
            existing = supabase.table('user_food_bank').select('id').eq('user_id', data['user_id']).eq('meal_type', meal_type).execute()
            
            if len(existing.data) < 6:
                # Obtener receta no usada de este tipo
                new_recipe = supabase.table('master_recipes').select('*').eq('meal_type', meal_type).not_.in_('id', [r['recipe_id'] for r in supabase.table('user_food_bank').select('recipe_id').eq('user_id', data['user_id']).eq('meal_type', meal_type).execute().data]).limit(1).execute()
                
                if new_recipe.data:
                    supabase.table('user_food_bank').insert({
                        'user_id': data['user_id'],
                        'meal_type': meal_type,
                        'recipe_id': new_recipe.data[0]['id'],
                        'added_week': week
                    }).execute()
        
        # Recalcular calorías
        tmb, tdee = calculate_tmb(profile['age'], profile['gender'], profile['height_cm'], data['weight'], profile['activity_level'])
        target = calculate_deficit(tdee, profile['goal_type'], data['weight'], profile['goal_weight_kg'])
        
        return jsonify({'success': True, 'new_target_calories': int(target)})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/shopping-list', methods=['GET'])
def shopping_list():
    try:
        user_id = request.args.get('user_id')
        if not user_id:
            return jsonify({'error': 'user_id requerido'}), 400
        
        week = get_week_number()
        result = supabase.table('weekly_plans').select('selected_recipe_id').eq('user_id', user_id).eq('week_number', week).execute()
        
        recipe_ids = [r['selected_recipe_id'] for r in result.data]
        recipes = supabase.table('master_recipes').select('ingredients, supermarket').in_('id', recipe_ids).execute()
        
        shopping = {'mercadona': [], 'lidl': [], 'mixto': []}
        for r in recipes.data:
            items = [i.strip() for i in r['ingredients'].split(',')]
            supermarket = r.get('supermarket', 'mixto')
            if supermarket not in shopping:
                shopping[supermarket] = []
            shopping[supermarket].extend(items)
        
        for k in shopping:
            shopping[k] = list(set(shopping[k]))
        
        return jsonify({'shopping_list': shopping})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def stats():
    try:
        user_id = request.args.get('user_id')
        if not user_id:
            return jsonify({'error': 'user_id requerido'}), 400
        
        history = supabase.table('weight_history').select('weight_kg, week_number, recorded_at').eq('user_id', user_id).order('week_number').execute()
        profile = supabase.table('user_profiles').select('current_weight_kg, goal_weight_kg').eq('user_id', user_id).execute()
        
        if not profile.data:
            return jsonify({'error': 'Perfil no encontrado'}), 404
        
        profile = profile.data[0]
        current = history.data[-1]['weight_kg'] if history.data else profile['current_weight_kg']
        diff = profile['current_weight_kg'] - profile['goal_weight_kg']
        progress = ((profile['current_weight_kg'] - current) / diff * 100) if diff > 0 else 0
        
        return jsonify({
            'weight_history': history.data,
            'current_weight': current,
            'goal_weight': profile['goal_weight_kg'],
            'progress_percent': round(progress, 1)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============================================================
# INIT
# ============================================================

# Seed recipes al iniciar
try:
    seed_recipes()
except Exception as e:
    print(f"⚠️ Error inicializando recetas: {e}")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
