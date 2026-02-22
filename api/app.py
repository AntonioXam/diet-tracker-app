#!/usr/bin/env python3
"""
Diet Tracker API - Backend para generación de dietas progresivas
Ingredientes disponibles en Mercadona y Lidl - Sistema de 6 opciones máximas
"""

import os
import json
import sqlite3
from datetime import datetime, timedelta
from flask import Flask, request, jsonify, g
from flask_cors import CORS
import hashlib

app = Flask(__name__)
CORS(app)

DATABASE = os.path.join(os.path.dirname(__file__), 'diet_tracker.db')

# ============================================================
# BASE DE DATOS
# ============================================================

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    """Inicializa la base de datos con todas las tablas."""
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        name TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS user_profiles (
        user_id INTEGER PRIMARY KEY,
        age INTEGER NOT NULL,
        gender TEXT NOT NULL,
        height_cm REAL NOT NULL,
        current_weight_kg REAL NOT NULL,
        goal_weight_kg REAL NOT NULL,
        activity_level TEXT NOT NULL,
        meals_per_day INTEGER NOT NULL,
        allergies TEXT,
        disliked_foods TEXT,
        goal_type TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS weight_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        weight_kg REAL NOT NULL,
        week_number INTEGER NOT NULL,
        recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS user_food_bank (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        meal_type TEXT NOT NULL,
        recipe_id INTEGER NOT NULL,
        times_used INTEGER DEFAULT 0,
        added_week INTEGER NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS weekly_plans (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        week_number INTEGER NOT NULL,
        day_of_week INTEGER NOT NULL,
        meal_type TEXT NOT NULL,
        selected_recipe_id INTEGER NOT NULL,
        calories REAL,
        protein REAL,
        carbs REAL,
        fat REAL,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS master_recipes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        meal_type TEXT NOT NULL,
        calories REAL NOT NULL,
        protein REAL NOT NULL,
        carbs REAL NOT NULL,
        fat REAL NOT NULL,
        ingredients TEXT NOT NULL,
        instructions TEXT,
        supermarket TEXT NOT NULL,
        category TEXT NOT NULL
    )''')
    
    conn.commit()
    conn.close()

# ============================================================
# RECETAS - Ingredientes disponibles en Mercadona/Lidl
# ============================================================

MASTER_RECIPES = [
    # DESAYUNOS
    {"name": "Tostada con aguacate y huevo", "meal_type": "desayuno", "calories": 350, "protein": 15, "carbs": 30, "fat": 18,
     "ingredients": "Pan de molde integral (2 rebanadas), Aguacate (1/2 unidad), Huevo L (1 unidad), Aceite de oliva virgen extra",
     "instructions": "Tostar el pan, machacar el aguacate con sal, hacer huevo poché o revuelto", "supermarket": "mixto", "category": "salado"},
    
    {"name": "Yogur con avena y frutas", "meal_type": "desayuno", "calories": 320, "protein": 18, "carbs": 45, "fat": 8,
     "ingredients": "Queso fresco batido 0% (150g), Copos de avena (40g), Plátano (1 unidad), Miel (1 cucharada)",
     "instructions": "Mezclar queso fresco con avena, añadir plátano troceado y miel", "supermarket": "mixto", "category": "dulce"},
    
    {"name": "Batido de proteínas casero", "meal_type": "desayuno", "calories": 280, "protein": 25, "carbs": 30, "fat": 6,
     "ingredients": "Proteína de suero en polvo (30g), Leche desnatada (200ml), Plátano (1/2 unidad)",
     "instructions": "Batir todo hasta que quede homogéneo", "supermarket": "mixto", "category": "batido"},
    
    {"name": "Tortilla francesa con pan tostado", "meal_type": "desayuno", "calories": 340, "protein": 20, "carbs": 25, "fat": 16,
     "ingredients": "Huevos L (2 unidades), Pan integral de centeno (1 rebanada), Aceite de oliva (1 cucharadita)",
     "instructions": "Batir huevos con sal, hacer tortilla francesa con poco aceite", "supermarket": "mixto", "category": "salado"},
    
    {"name": "Porridge de avena con manzana", "meal_type": "desayuno", "calories": 310, "protein": 12, "carbs": 52, "fat": 7,
     "ingredients": "Copos de avena finos (50g), Leche semidesnatada (200ml), Canela molida, Manzana Fuji (1 unidad)",
     "instructions": "Cocer avena con leche 5 minutos, añadir canela y manzana troceada", "supermarket": "mixto", "category": "dulce"},
    
    {"name": "Requesón con frutos rojos y nueces", "meal_type": "desayuno", "calories": 290, "protein": 22, "carbs": 28, "fat": 9,
     "ingredients": "Requesón light (150g), Fresas congeladas (100g), Nueces peladas (20g), Edulcorante",
     "instructions": "Mezclar requesón con frutos rojos y nueces troceadas", "supermarket": "mixto", "category": "dulce"},
    
    # ALMUERZOS
    {"name": "Manzana con almendras", "meal_type": "almuerzo", "calories": 180, "protein": 5, "carbs": 25, "fat": 8,
     "ingredients": "Manzana Golden (1 unidad), Almendras crudas sin sal (20g)",
     "instructions": "Lavar manzana y comer con las almendras", "supermarket": "mixto", "category": "snack"},
    
    {"name": "Yogur griego natural", "meal_type": "almuerzo", "calories": 120, "protein": 15, "carbs": 8, "fat": 3,
     "ingredients": "Yogur griego natural sin azúcar (125g)",
     "instructions": "Consumir directamente", "supermarket": "mixto", "category": "lácteo"},
    
    {"name": "Zanahoria con hummus", "meal_type": "almuerzo", "calories": 150, "protein": 6, "carbs": 18, "fat": 7,
     "ingredients": "Zanahorias frescas (100g), Hummus clásico (50g)",
     "instructions": "Cortar zanahorias en bastones y acompañar con hummus", "supermarket": "mixto", "category": "salado"},
    
    {"name": "Barrita proteica", "meal_type": "almuerzo", "calories": 200, "protein": 20, "carbs": 15, "fat": 6,
     "ingredients": "Barrita proteica chocolate/vainilla (45g)",
     "instructions": "Consumir directamente", "supermarket": "mixto", "category": "snack"},
    
    {"name": "Queso fresco con nueces", "meal_type": "almuerzo", "calories": 160, "protein": 12, "carbs": 5, "fat": 11,
     "ingredients": "Queso fresco 0% (100g), Nueces peladas (15g)",
     "instructions": "Acompañar queso con nueces troceadas", "supermarket": "mixto", "category": "lácteo"},
    
    {"name": "Pan con tomate", "meal_type": "almuerzo", "calories": 140, "protein": 5, "carbs": 22, "fat": 4,
     "ingredients": "Pan de pueblo integral (1 rebanada), Tomate de ensalada (1/2), Aceite de oliva virgen extra, Sal",
     "instructions": "Tostar pan, rallar tomate, añadir aceite y sal", "supermarket": "mixto", "category": "salado"},
    
    # COMIDAS
    {"name": "Pollo al horno con verduras", "meal_type": "comida", "calories": 450, "protein": 40, "carbs": 35, "fat": 15,
     "ingredients": "Pechuga de pollo fresca (150g), Patata mediana (150g), Brócoli fresco (100g), Aceite de oliva, Sal, Pimienta",
     "instructions": "Hornear a 200°C durante 25-30 minutos con verduras cortadas", "supermarket": "mixto", "category": "proteina"},
    
    {"name": "Salmón con arroz integral", "meal_type": "comida", "calories": 480, "protein": 35, "carbs": 45, "fat": 18,
     "ingredients": "Filete de salmón fresco (150g), Arroz integral (60g en crudo), Espárragos trigueros (100g), Limón",
     "instructions": "Cocer arroz 25 min. Hacer salmón a la plancha 4 min por lado. Saltear espárragos.", "supermarket": "mixto", "category": "pescado"},
    
    {"name": "Lentejas estofadas con verduras", "meal_type": "comida", "calories": 420, "protein": 18, "carbs": 55, "fat": 12,
     "ingredients": "Lentejas pardinas (70g en crudo), Zanahoria (1 unidad), Cebolla (1/2), Pimiento verde (1/2), Laurel",
     "instructions": "Sofreír verduras, añadir lentejas y cubrir con agua. Cocer 25-30 min.", "supermarket": "mixto", "category": "legumbre"},
    
    {"name": "Pasta integral con atún", "meal_type": "comida", "calories": 440, "protein": 30, "carbs": 50, "fat": 12,
     "ingredients": "Espaguetis integrales (80g en crudo), Atún al natural (2 latas), Tomate triturado (50g), Orégano",
     "instructions": "Cocer pasta. Mezclar con atún escurrido y tomate. Calentar 2 min.", "supermarket": "mixto", "category": "pasta"},
    
    {"name": "Ternera con boniato asado", "meal_type": "comida", "calories": 470, "protein": 38, "carbs": 40, "fat": 16,
     "ingredients": "Filete de ternera magra (150g), Boniato mediano (200g), Judías verdes (100g), Aceite de oliva",
     "instructions": "Hornear boniato 40-45 min a 200°C. Hacer ternera a la plancha. Cocer judías 10 min.", "supermarket": "mixto", "category": "proteina"},
    
    {"name": "Ensalada de garbanzos", "meal_type": "comida", "calories": 400, "protein": 20, "carbs": 48, "fat": 14,
     "ingredients": "Garbanzos cocidos (200g), Tomates cherry (100g), Pepino (1/2), Atún al natural (1 lata), Aceitunas negras, Aceite de oliva",
     "instructions": "Mezclar todos los ingredientes en un bol y aliñar", "supermarket": "mixto", "category": "ensalada"},
    
    # MERIENDAS
    {"name": "Yogur con kiwi", "meal_type": "merienda", "calories": 150, "protein": 10, "carbs": 22, "fat": 3,
     "ingredients": "Yogur natural sin azúcar (125g), Kiwi maduro (1 unidad)",
     "instructions": "Pelar y trocear kiwi, mezclar con yogur", "supermarket": "mixto", "category": "lácteo"},
    
    {"name": "Tostada con jamón cocido", "meal_type": "merienda", "calories": 180, "protein": 15, "carbs": 18, "fat": 5,
     "ingredients": "Pan de molde integral (1 rebanada), Jamón cocido extra (2 lonchas, 60g)",
     "instructions": "Tostar pan y colocar jamón", "supermarket": "mixto", "category": "salado"},
    
    {"name": "Batido verde", "meal_type": "merienda", "calories": 140, "protein": 3, "carbs": 32, "fat": 1,
     "ingredients": "Plátano (1/2), Fresas (100g), Agua (200ml)",
     "instructions": "Batir todo hasta textura suave", "supermarket": "mixto", "category": "batido"},
    
    {"name": "Huevos cocidos", "meal_type": "merienda", "calories": 140, "protein": 12, "carbs": 1, "fat": 10,
     "ingredients": "Huevos L (2 unidades), Sal",
     "instructions": "Cocer 10 minutos desde que hierve el agua", "supermarket": "mixto", "category": "proteina"},
    
    {"name": "Requesón con canela", "meal_type": "merienda", "calories": 120, "protein": 14, "carbs": 8, "fat": 4,
     "ingredients": "Requesón light (100g), Canela molida, Edulcorante líquido",
     "instructions": "Mezclar requesón con canela y edulcorante", "supermarket": "mixto", "category": "lácteo"},
    
    {"name": "Surimi con pepino", "meal_type": "merienda", "calories": 100, "protein": 12, "carbs": 10, "fat": 1,
     "ingredients": "Palitos de cangrejo/surimi (80g), Pepino (1/2 unidad)",
     "instructions": "Cortar pepino en bastones y acompañar con surimi", "supermarket": "mixto", "category": "snack"},
    
    # CENAS
    {"name": "Merluza al horno con verduras", "meal_type": "cena", "calories": 320, "protein": 30, "carbs": 20, "fat": 12,
     "ingredients": "Filete de merluza (150g), Calabacín mediano (1 unidad), Cebolla (1/2), Aceite de oliva",
     "instructions": "Hornear 20 min a 180°C con verduras en rodajas", "supermarket": "mixto", "category": "pescado"},
    
    {"name": "Tortilla de espinacas", "meal_type": "cena", "calories": 280, "protein": 18, "carbs": 8, "fat": 20,
     "ingredients": "Huevos L (2 unidades), Espinacas frescas o congeladas (100g), Queso light (1 loncha)",
     "instructions": "Hacer tortilla con espinacas salteadas y queso", "supermarket": "mixto", "category": "huevos"},
    
    {"name": "Ensalada de atún", "meal_type": "cena", "calories": 300, "protein": 28, "carbs": 15, "fat": 14,
     "ingredients": "Atún al natural (2 latas), Lechuga iceberg (100g), Tomate (1 unidad), Maíz dulce (30g)",
     "instructions": "Mezclar todos los ingredientes y aliñar", "supermarket": "mixto", "category": "ensalada"},
    
    {"name": "Sepia a la plancha", "meal_type": "cena", "calories": 260, "protein": 32, "carbs": 10, "fat": 8,
     "ingredients": "Sepia fresca (200g), Ajo (2 dientes), Perejil fresco, Aceite de oliva",
     "instructions": "Hacer sepia a la plancha con ajo y perejil picado", "supermarket": "mixto", "category": "pescado"},
    
    {"name": "Pavo a la plancha con espárragos", "meal_type": "cena", "calories": 290, "protein": 35, "carbs": 12, "fat": 10,
     "ingredients": "Filete de pechuga de pavo (150g), Espárragos trigueros (150g), Limón",
     "instructions": "Hacer pavo y espárragos a la plancha, servir con limón", "supermarket": "mixto", "category": "proteina"},
    
    {"name": "Crema de calabacín", "meal_type": "cena", "calories": 240, "protein": 12, "carbs": 25, "fat": 10,
     "ingredients": "Calabacín mediano (2 unidades), Puerro (1 unidad), Queso fresco (50g), Aceite de oliva",
     "instructions": "Cocer verduras 15 min, triturar y añadir queso", "supermarket": "mixto", "category": "crema"},
]

def seed_recipes():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM master_recipes')
    if c.fetchone()[0] == 0:
        for recipe in MASTER_RECIPES:
            c.execute('''INSERT INTO master_recipes 
                (name, meal_type, calories, protein, carbs, fat, ingredients, instructions, supermarket, category)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                (recipe['name'], recipe['meal_type'], recipe['calories'], recipe['protein'],
                 recipe['carbs'], recipe['fat'], recipe['ingredients'], recipe['instructions'],
                 recipe['supermarket'], recipe['category']))
        conn.commit()
    conn.close()

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

# ============================================================
# API ENDPOINTS
# ============================================================

@app.route('/api/health')
def health():
    return jsonify({'status': 'ok', 'timestamp': datetime.now().isoformat()})

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    db = get_db()
    if not all(k in data for k in ('email', 'password', 'name')):
        return jsonify({'error': 'Datos incompletos'}), 400
    if db.execute('SELECT id FROM users WHERE email = ?', (data['email'],)).fetchone():
        return jsonify({'error': 'Email ya registrado'}), 400
    cursor = db.execute('INSERT INTO users (email, password_hash, name) VALUES (?, ?, ?)',
                       (data['email'], hash_password(data['password']), data['name']))
    db.commit()
    return jsonify({'success': True, 'user_id': cursor.lastrowid})

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    db = get_db()
    user = db.execute('SELECT id, name FROM users WHERE email = ? AND password_hash = ?',
                     (data.get('email'), hash_password(data.get('password', '')))).fetchone()
    if user:
        return jsonify({'success': True, 'user_id': user['id'], 'name': user['name']})
    return jsonify({'error': 'Credenciales inválidas'}), 401

@app.route('/api/profile', methods=['POST'])
def save_profile():
    data = request.json
    db = get_db()
    user_id = data.get('user_id')
    if not user_id:
        return jsonify({'error': 'user_id requerido'}), 400
    
    db.execute('''INSERT OR REPLACE INTO user_profiles 
        (user_id, age, gender, height_cm, current_weight_kg, goal_weight_kg, activity_level, meals_per_day, allergies, disliked_foods, goal_type)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
        (user_id, data['age'], data['gender'], data['height'], data['current_weight'],
         data['goal_weight'], data['activity_level'], data['meals_per_day'],
         data.get('allergies', ''), data.get('disliked_foods', ''), data['goal_type']))
    
    db.execute('INSERT INTO weight_history (user_id, weight_kg, week_number) VALUES (?, ?, ?)',
              (user_id, data['current_weight'], get_week_number()))
    db.commit()
    
    tmb, tdee = calculate_tmb(data['age'], data['gender'], data['height'], data['current_weight'], data['activity_level'])
    target = calculate_deficit(tdee, data['goal_type'], data['current_weight'], data['goal_weight'])
    generate_first_week(db, user_id, target, data['meals_per_day'])
    
    return jsonify({'success': True, 'tmb': tmb, 'tdee': tdee, 'target_calories': target})

def generate_first_week(db, user_id, target_calories, meals_per_day):
    week = get_week_number()
    meal_types = ['desayuno', 'almuerzo', 'comida', 'merienda', 'cena'][:meals_per_day]
    
    for day in range(1, 8):
        for meal_type in meal_types:
            recipe = db.execute('SELECT * FROM master_recipes WHERE meal_type = ? ORDER BY RANDOM() LIMIT 1', (meal_type,)).fetchone()
            if recipe:
                db.execute('''INSERT INTO weekly_plans 
                    (user_id, week_number, day_of_week, meal_type, selected_recipe_id, calories, protein, carbs, fat)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                    (user_id, week, day, meal_type, recipe['id'], recipe['calories'], recipe['protein'], recipe['carbs'], recipe['fat']))
                db.execute('INSERT INTO user_food_bank (user_id, meal_type, recipe_id, added_week) VALUES (?, ?, ?, ?)',
                          (user_id, meal_type, recipe['id'], week))
    db.commit()

@app.route('/api/plan/current', methods=['GET'])
def get_current_plan():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': 'user_id requerido'}), 400
    db = get_db()
    plan = db.execute('''SELECT wp.*, mr.name as recipe_name, mr.ingredients, mr.instructions, mr.supermarket, mr.category
        FROM weekly_plans wp JOIN master_recipes mr ON wp.selected_recipe_id = mr.id
        WHERE wp.user_id = ? AND wp.week_number = ? ORDER BY wp.day_of_week, wp.meal_type''',
        (user_id, get_week_number())).fetchall()
    
    daily = {}
    for row in plan:
        d = row['day_of_week']
        if d not in daily:
            daily[d] = {'calories': 0, 'protein': 0, 'carbs': 0, 'fat': 0}
        daily[d]['calories'] += row['calories'] or 0
        daily[d]['protein'] += row['protein'] or 0
        daily[d]['carbs'] += row['carbs'] or 0
        daily[d]['fat'] += row['fat'] or 0
    
    return jsonify({'week': get_week_number(), 'meals': [dict(row) for row in plan], 'daily_totals': daily})

@app.route('/api/food-bank/options', methods=['GET'])
def get_food_bank():
    user_id = request.args.get('user_id')
    meal_type = request.args.get('meal_type')
    if not user_id:
        return jsonify({'error': 'user_id requerido'}), 400
    db = get_db()
    if meal_type:
        opts = db.execute('''SELECT ufb.*, mr.name, mr.calories, mr.protein, mr.carbs, mr.fat, mr.ingredients, mr.supermarket
            FROM user_food_bank ufb JOIN master_recipes mr ON ufb.recipe_id = mr.id
            WHERE ufb.user_id = ? AND ufb.meal_type = ? ORDER BY ufb.times_used ASC''', (user_id, meal_type)).fetchall()
    else:
        opts = db.execute('''SELECT ufb.*, mr.name, mr.meal_type, mr.calories, mr.protein, mr.carbs, mr.fat
            FROM user_food_bank ufb JOIN master_recipes mr ON ufb.recipe_id = mr.id
            WHERE ufb.user_id = ? ORDER BY ufb.meal_type, ufb.times_used ASC''', (user_id,)).fetchall()
    return jsonify({'options': [dict(row) for row in opts]})

@app.route('/api/plan/swap', methods=['POST'])
def swap_meal():
    data = request.json
    db = get_db()
    recipe = db.execute('SELECT * FROM master_recipes WHERE id = ?', (data['new_recipe_id'],)).fetchone()
    if not recipe:
        return jsonify({'error': 'Receta no encontrada'}), 404
    db.execute('''UPDATE weekly_plans SET selected_recipe_id = ?, calories = ?, protein = ?, carbs = ?, fat = ?
        WHERE user_id = ? AND week_number = ? AND day_of_week = ? AND meal_type = ?''',
        (data['new_recipe_id'], recipe['calories'], recipe['protein'], recipe['carbs'], recipe['fat'],
         data['user_id'], get_week_number(), data['day'], data['meal_type']))
    db.execute('UPDATE user_food_bank SET times_used = times_used + 1 WHERE user_id = ? AND recipe_id = ?',
              (data['user_id'], data['new_recipe_id']))
    db.commit()
    return jsonify({'success': True})

@app.route('/api/weight/checkin', methods=['POST'])
def weight_checkin():
    data = request.json
    db = get_db()
    db.execute('INSERT INTO weight_history (user_id, weight_kg, week_number) VALUES (?, ?, ?)',
              (data['user_id'], data['weight'], get_week_number()))
    profile = db.execute('SELECT * FROM user_profiles WHERE user_id = ?', (data['user_id'],)).fetchone()
    if profile:
        for meal_type in ['desayuno', 'almuerzo', 'comida', 'merienda', 'cena'][:profile['meals_per_day']]:
            existing = db.execute('SELECT COUNT(*) as c FROM user_food_bank WHERE user_id = ? AND meal_type = ?',
                                 (data['user_id'], meal_type)).fetchone()['c']
            if existing < 6:
                new = db.execute('''SELECT * FROM master_recipes WHERE meal_type = ? 
                    AND id NOT IN (SELECT recipe_id FROM user_food_bank WHERE user_id = ? AND meal_type = ?)
                    ORDER BY RANDOM() LIMIT 1''', (meal_type, data['user_id'], meal_type)).fetchone()
                if new:
                    db.execute('INSERT INTO user_food_bank (user_id, meal_type, recipe_id, added_week) VALUES (?, ?, ?, ?)',
                              (data['user_id'], meal_type, new['id'], get_week_number()))
        db.commit()
        tmb, tdee = calculate_tmb(profile['age'], profile['gender'], profile['height_cm'], data['weight'], profile['activity_level'])
        return jsonify({'success': True, 'new_target_calories': calculate_deficit(tdee, profile['goal_type'], data['weight'], profile['goal_weight'])})
    return jsonify({'error': 'Perfil no encontrado'}), 404

@app.route('/api/shopping-list', methods=['GET'])
def shopping_list():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': 'user_id requerido'}), 400
    db = get_db()
    recipes = db.execute('''SELECT DISTINCT mr.ingredients, mr.supermarket FROM weekly_plans wp
        JOIN master_recipes mr ON wp.selected_recipe_id = mr.id
        WHERE wp.user_id = ? AND wp.week_number = ?''', (user_id, get_week_number())).fetchall()
    result = {'mercadona': [], 'lidl': [], 'mixto': []}
    for r in recipes:
        items = [i.strip() for i in r['ingredients'].split(',')]
        result[r['supermarket']].extend(items)
    for k in result:
        result[k] = list(set(result[k]))
    return jsonify({'shopping_list': result})

@app.route('/api/stats', methods=['GET'])
def stats():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': 'user_id requerido'}), 400
    db = get_db()
    history = db.execute('SELECT weight_kg, week_number, recorded_at FROM weight_history WHERE user_id = ? ORDER BY week_number', (user_id,)).fetchall()
    profile = db.execute('SELECT current_weight_kg, goal_weight_kg FROM user_profiles WHERE user_id = ?', (user_id,)).fetchone()
    current = history[-1]['weight_kg'] if history else profile['current_weight_kg']
    diff = profile['current_weight_kg'] - profile['goal_weight_kg']
    progress = ((profile['current_weight_kg'] - current) / diff * 100) if diff > 0 else 0
    return jsonify({'weight_history': [dict(r) for r in history], 'current_weight': current, 'goal_weight': profile['goal_weight_kg'], 'progress_percent': round(progress, 1)})

# ============================================================
# INIT
# ============================================================

if not os.path.exists(DATABASE):
    init_db()
    seed_recipes()

def handler(event, context):
    from flask import Response
    with app.app_context():
        if not os.path.exists(DATABASE):
            init_db()
            seed_recipes()
        return {'statusCode': app.full_dispatch_request().status_code, 'headers': dict(app.full_dispatch_request().headers), 'body': app.full_dispatch_request().get_data().decode('utf-8')}

if __name__ == '__main__':
    init_db()
    seed_recipes()
    app.run(debug=True, port=5000)
