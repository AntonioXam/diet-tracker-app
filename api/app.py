#!/usr/bin/env python3
"""
Diet Tracker API - Backend para generación de dietas progresivas
Productos Mercadona/Lidl - Sistema de 6 opciones máximas
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
    
    # Tabla de usuarios
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            name TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Perfil nutricional del usuario (onboarding)
    c.execute('''
        CREATE TABLE IF NOT EXISTS user_profiles (
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
        )
    ''')
    
    # Historial de peso semanal
    c.execute('''
        CREATE TABLE IF NOT EXISTS weight_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            weight_kg REAL NOT NULL,
            week_number INTEGER NOT NULL,
            recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    # Banco de comidas del usuario (máximo 6 opciones por tipo)
    c.execute('''
        CREATE TABLE IF NOT EXISTS user_food_bank (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            meal_type TEXT NOT NULL,
            recipe_id INTEGER NOT NULL,
            times_used INTEGER DEFAULT 0,
            added_week INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    # Plan semanal actual del usuario
    c.execute('''
        CREATE TABLE IF NOT EXISTS weekly_plans (
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
        )
    ''')
    
    # Recetas maestras (productos Mercadona/Lidl)
    c.execute('''
        CREATE TABLE IF NOT EXISTS master_recipes (
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
        )
    ''')
    
    conn.commit()
    conn.close()

# ============================================================
# RECETAS MAESTRAS - Productos Mercadona/Lidl
# ============================================================

MASTER_RECIPES = [
    # DESAYUNOS
    {"name": "Tostada con aguacate y huevo", "meal_type": "desayuno", "calories": 350, "protein": 15, "carbs": 30, "fat": 18, 
     "ingredients": "Pan integral Lidl (2 rebanadas), Aguacate Mercadona (1/2), Huevo Lidl (1 unidad)", 
     "instructions": "Tostar el pan, machacar el aguacate, hacer huevo poché o revuelto", "supermarket": "mixto", "category": "salado"},
    
    {"name": "Yogur con avena y frutas", "meal_type": "desayuno", "calories": 320, "protein": 18, "carbs": 45, "fat": 8,
     "ingredients": "Queso fresco batido Mercadona (150g), Avena Lidl (40g), Plátano (1 unidad), Miel Lidl (1 cucharada)",
     "instructions": "Mezclar todo en un bol", "supermarket": "mixto", "category": "dulce"},
    
    {"name": "Batido de proteínas", "meal_type": "desayuno", "calories": 280, "protein": 25, "carbs": 30, "fat": 6,
     "ingredients": "Proteína whey Lidl (1 scoop), Leche desnatada Mercadona (200ml), Plátano (1/2)",
     "instructions": "Batir todo hasta que quede suave", "supermarket": "mixto", "category": "batido"},
    
    {"name": "Tortilla francesa con pan", "meal_type": "desayuno", "calories": 340, "protein": 20, "carbs": 25, "fat": 16,
     "ingredients": "Huevos Lidl (2 unidades), Pan integral Lidl (1 rebanada), Aceite de oliva Mercadona (5ml)",
     "instructions": "Hacer tortilla francesa con poco aceite", "supermarket": "mixto", "category": "salado"},
    
    {"name": "Porridge de avena", "meal_type": "desayuno", "calories": 310, "protein": 12, "carbs": 52, "fat": 7,
     "ingredients": "Avena Lidl (50g), Leche desnatada Mercadona (200ml), Canela Lidl, Manzana (1 unidad)",
     "instructions": "Cocer avena con leche 5 minutos, añadir canela y manzana troceada", "supermarket": "mixto", "category": "dulce"},
    
    {"name": "Requesón con frutos rojos", "meal_type": "desayuno", "calories": 290, "protein": 22, "carbs": 28, "fat": 9,
     "ingredients": "Requesón Mercadona (150g), Fresas congeladas Lidl (100g), Nueces Lidl (20g)",
     "instructions": "Mezclar requesón con frutos rojos y nueces", "supermarket": "mixto", "category": "dulce"},
    
    # ALMUERZOS (media mañana)
    {"name": "Fruta con frutos secos", "meal_type": "almuerzo", "calories": 180, "protein": 5, "carbs": 25, "fat": 8,
     "ingredients": "Manzana (1 unidad), Almendras Lidl (20g)", "instructions": "Comer la fruta con las almendras", 
     "supermarket": "mixto", "category": "snack"},
    
    {"name": "Yogur proteico", "meal_type": "almuerzo", "calories": 120, "protein": 15, "carbs": 10, "fat": 2,
     "ingredients": "Yogur proteico Mercadona (1 unidad)", "instructions": "Consumir directamente", 
     "supermarket": "mercadona", "category": "lácteo"},
    
    {"name": "Bastones de zanahoria con hummus", "meal_type": "almuerzo", "calories": 150, "protein": 6, "carbs": 18, "fat": 7,
     "ingredients": "Zanahorias Lidl (100g), Hummus Mercadona (50g)", "instructions": "Cortar zanahorias y acompañar con hummus",
     "supermarket": "mixto", "category": "salado"},
    
    {"name": "Barrita de proteínas", "meal_type": "almuerzo", "calories": 200, "protein": 20, "carbs": 15, "fat": 6,
     "ingredients": "Barrita proteica Lidl (1 unidad)", "instructions": "Consumir directamente",
     "supermarket": "lidl", "category": "snack"},
    
    {"name": "Queso fresco con nueces", "meal_type": "almuerzo", "calories": 160, "protein": 12, "carbs": 5, "fat": 11,
     "ingredients": "Queso fresco Mercadona (100g), Nueces Lidl (15g)", "instructions": "Acompañar queso con nueces",
     "supermarket": "mixto", "category": "lácteo"},
    
    {"name": "Tostada integral con tomate", "meal_type": "almuerzo", "calories": 140, "protein": 5, "carbs": 22, "fat": 4,
     "ingredients": "Pan integral Lidl (1 rebanada), Tomate natural (1/2), Aceite de oliva (5ml)",
     "instructions": "Tostar pan, rallar tomate y añadir aceite", "supermarket": "mixto", "category": "salado"},
    
    # COMIDAS
    {"name": "Pollo al horno con verduras", "meal_type": "comida", "calories": 450, "protein": 40, "carbs": 35, "fat": 15,
     "ingredients": "Pechuga pollo Mercadona (150g), Patata Lidl (150g), Brócoli Mercadona (100g), Aceite de oliva (10ml)",
     "instructions": "Hornear pollo con patata y brócoli 25 min a 200°C", "supermarket": "mixto", "category": "proteina"},
    
    {"name": "Salmón con arroz integral", "meal_type": "comida", "calories": 480, "protein": 35, "carbs": 45, "fat": 18,
     "ingredients": "Salmón Lidl (150g), Arroz integral Mercadona (60g en crudo), Espárragos (100g)",
     "instructions": "Cocer arroz, hacer salmón a la plancha con espárragos", "supermarket": "mixto", "category": "pescado"},
    
    {"name": "Lentejas con verduras", "meal_type": "comida", "calories": 420, "protein": 18, "carbs": 55, "fat": 12,
     "ingredients": "Lentejas cocidas Lidl (200g), Zanahoria (1 unidad), Cebolla (1/2), Pimiento (1/2)",
     "instructions": "Sofreír verduras, añadir lentejas y cocinar 15 min", "supermarket": "lidl", "category": "legumbre"},
    
    {"name": "Pasta integral con atún", "meal_type": "comida", "calories": 440, "protein": 30, "carbs": 50, "fat": 12,
     "ingredients": "Pasta integral Lidl (80g en crudo), Atún al natural Mercadona (2 latas), Tomate frito Lidl (50g)",
     "instructions": "Cocer pasta, mezclar con atún y tomate", "supermarket": "mixto", "category": "pasta"},
    
    {"name": "Ternera con boniato", "meal_type": "comida", "calories": 470, "protein": 38, "carbs": 40, "fat": 16,
     "ingredients": "Filete ternera Mercadona (150g), Boniato Lidl (200g), Judías verdes (100g)",
     "instructions": "Hacer ternera a la plancha, hornear boniato y cocer judías", "supermarket": "mixto", "category": "proteina"},
    
    {"name": "Ensalada de garbanzos", "meal_type": "comida", "calories": 400, "protein": 20, "carbs": 48, "fat": 14,
     "ingredients": "Garbanzos cocidos Lidl (200g), Tomate cherry (100g), Pepino (1/2), Atún (1 lata), Aceite de oliva (10ml)",
     "instructions": "Mezclar todos los ingredientes en un bol", "supermarket": "lidl", "category": "ensalada"},
    
    # MERIENDAS
    {"name": "Yogur con fruta", "meal_type": "merienda", "calories": 150, "protein": 10, "carbs": 22, "fat": 3,
     "ingredients": "Yogur natural Mercadona (1 unidad), Kiwi (1 unidad)", "instructions": "Mezclar yogur con kiwi troceado",
     "supermarket": "mixto", "category": "lácteo"},
    
    {"name": "Tostada con jamón", "meal_type": "merienda", "calories": 180, "protein": 15, "carbs": 18, "fat": 5,
     "ingredients": "Pan integral Lidl (1 rebanada), Jamón york Mercadona (2 lonchas)",
     "instructions": "Tostar pan y poner jamón", "supermarket": "mixto", "category": "salado"},
    
    {"name": "Batido de frutas", "meal_type": "merienda", "calories": 140, "protein": 3, "carbs": 32, "fat": 1,
     "ingredients": "Plátano (1/2), Fresas Lidl (100g), Agua (200ml)", "instructions": "Batir todo hasta que quede suave",
     "supermarket": "mixto", "category": "batido"},
    
    {"name": "Huevo duro", "meal_type": "merienda", "calories": 140, "protein": 12, "carbs": 1, "fat": 10,
     "ingredients": "Huevo Lidl (2 unidades)", "instructions": "Cocer huevos 10 minutos", "supermarket": "lidl", "category": "proteina"},
    
    {"name": "Requesón con canela", "meal_type": "merienda", "calories": 120, "protein": 14, "carbs": 8, "fat": 4,
     "ingredients": "Requesón Mercadona (100g), Canela Lidl, Stevia", "instructions": "Mezclar requesón con canela y endulzante",
     "supermarket": "mixto", "category": "lácteo"},
    
    {"name": "Palitos de cangrejo", "meal_type": "merienda", "calories": 100, "protein": 12, "carbs": 10, "fat": 1,
     "ingredients": "Palitos cangrejo Lidl (8 unidades), Pepino (1/2)", "instructions": "Acompañar palitos con pepino en bastones",
     "supermarket": "lidl", "category": "snack"},
    
    # CENAS
    {"name": "Merluza al horno con verduras", "meal_type": "cena", "calories": 320, "protein": 30, "carbs": 20, "fat": 12,
     "ingredients": "Merluza Mercadona (150g), Calabacín (1 unidad), Cebolla (1/2), Aceite de oliva (10ml)",
     "instructions": "Hornear merluza con verduras 20 min a 180°C", "supermarket": "mixto", "category": "pescado"},
    
    {"name": "Tortilla de espinacas", "meal_type": "cena", "calories": 280, "protein": 18, "carbs": 8, "fat": 20,
     "ingredients": "Huevos Lidl (2 unidades), Espinacas congeladas Lidl (100g), Queso light Mercadona (1 loncha)",
     "instructions": "Hacer tortilla con espinacas y queso", "supermarket": "mixto", "category": "huevos"},
    
    {"name": "Ensalada de atún", "meal_type": "cena", "calories": 300, "protein": 28, "carbs": 15, "fat": 14,
     "ingredients": "Atún al natural Mercadona (2 latas), Lechuga (100g), Tomate (1 unidad), Maíz Lidl (30g)",
     "instructions": "Mezclar todos los ingredientes", "supermarket": "mixto", "category": "ensalada"},
    
    {"name": "Sepia a la plancha", "meal_type": "cena", "calories": 260, "protein": 32, "carbs": 10, "fat": 8,
     "ingredients": "Sepia Lidl (200g), Ajo (2 dientes), Perejil, Aceite de oliva (10ml)",
     "instructions": "Hacer sepia a la plancha con ajo y perejil", "supermarket": "lidl", "category": "pescado"},
    
    {"name": "Pavo con espárragos", "meal_type": "cena", "calories": 290, "protein": 35, "carbs": 12, "fat": 10,
     "ingredients": "Filete pavo Mercadona (150g), Espárragos trigueros Lidl (150g), Limón",
     "instructions": "Hacer pavo a la plancha con espárragos salteados", "supermarket": "mixto", "category": "proteina"},
    
    {"name": "Crema de calabacín", "meal_type": "cena", "calories": 240, "protein": 12, "carbs": 25, "fat": 10,
     "ingredients": "Calabacín (2 unidades), Puerro (1 unidad), Queso fresco Mercadona (50g), Aceite de oliva (10ml)",
     "instructions": "Cocer verduras, triturar y añadir queso", "supermarket": "mixto", "category": "crema"},
]

def seed_recipes():
    """Inserta recetas maestras si la tabla está vacía."""
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM master_recipes')
    if c.fetchone()[0] == 0:
        for recipe in MASTER_RECIPES:
            c.execute('''
                INSERT INTO master_recipes (name, meal_type, calories, protein, carbs, fat, ingredients, instructions, supermarket, category)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (recipe['name'], recipe['meal_type'], recipe['calories'], recipe['protein'], 
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
    """Calcula Tasa Metabólica Basal con fórmula Mifflin-St Jeor."""
    if gender == 'male':
        tmb = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        tmb = 10 * weight + 6.25 * height - 5 * age - 161
    
    # Multiplicador por actividad
    activity_multipliers = {
        'sedentary': 1.2,
        'light': 1.375,
        'moderate': 1.55,
        'active': 1.725,
        'very_active': 1.9
    }
    
    tdee = tmb * activity_multipliers.get(activity_level, 1.2)
    return round(tmb), round(tdee)

def calculate_deficit(tdee, goal_type, current_weight, goal_weight):
    """Calcula déficit calórico según objetivo."""
    if goal_type == 'lose':
        # Déficit de 300-500 calorías según diferencia de peso
        weight_diff = current_weight - goal_weight
        deficit = min(500, 300 + (weight_diff * 20))
        return tdee - deficit
    elif goal_type == 'gain':
        return tdee + 300
    else:  # maintain
        return tdee

def get_week_number():
    """Obtiene número de semana actual desde inicio de año."""
    return datetime.now().isocalendar()[1]

# ============================================================
# RUTAS API
# ============================================================

@app.route('/api/health')
def health():
    return jsonify({'status': 'ok', 'timestamp': datetime.now().isoformat()})

@app.route('/api/register', methods=['POST'])
def register():
    """Registra un nuevo usuario."""
    data = request.json
    db = get_db()
    
    if not all(k in data for k in ('email', 'password', 'name')):
        return jsonify({'error': 'Datos incompletos'}), 400
    
    # Verificar si existe
    existing = db.execute('SELECT id FROM users WHERE email = ?', (data['email'],)).fetchone()
    if existing:
        return jsonify({'error': 'Email ya registrado'}), 400
    
    # Crear usuario
    password_hash = hash_password(data['password'])
    cursor = db.execute('INSERT INTO users (email, password_hash, name) VALUES (?, ?, ?)',
                       (data['email'], password_hash, data['name']))
    db.commit()
    
    return jsonify({'success': True, 'user_id': cursor.lastrowid})

@app.route('/api/login', methods=['POST'])
def login():
    """Autentica usuario."""
    data = request.json
    db = get_db()
    
    password_hash = hash_password(data.get('password', ''))
    user = db.execute('SELECT id, name FROM users WHERE email = ? AND password_hash = ?',
                     (data.get('email'), password_hash)).fetchone()
    
    if user:
        return jsonify({'success': True, 'user_id': user['id'], 'name': user['name']})
    return jsonify({'error': 'Credenciales inválidas'}), 401

@app.route('/api/profile', methods=['POST'])
def save_profile():
    """Guarda perfil nutricional del usuario (onboarding)."""
    data = request.json
    db = get_db()
    user_id = data.get('user_id')
    
    if not user_id:
        return jsonify({'error': 'user_id requerido'}), 400
    
    # Guardar perfil
    db.execute('''
        INSERT OR REPLACE INTO user_profiles 
        (user_id, age, gender, height_cm, current_weight_kg, goal_weight_kg, 
         activity_level, meals_per_day, allergies, disliked_foods, goal_type)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (user_id, data['age'], data['gender'], data['height'], data['current_weight'],
          data['goal_weight'], data['activity_level'], data['meals_per_day'],
          data.get('allergies', ''), data.get('disliked_foods', ''), data['goal_type']))
    
    # Guardar peso inicial en historial
    week = get_week_number()
    db.execute('INSERT INTO weight_history (user_id, weight_kg, week_number) VALUES (?, ?, ?)',
              (user_id, data['current_weight'], week))
    db.commit()
    
    # Calcular calorías objetivo
    tmb, tdee = calculate_tmb(data['age'], data['gender'], data['height'], 
                              data['current_weight'], data['activity_level'])
    target_calories = calculate_deficit(tdee, data['goal_type'], 
                                        data['current_weight'], data['goal_weight'])
    
    # Generar primera semana de dieta
    generate_first_week(db, user_id, target_calories, data['meals_per_day'])
    
    return jsonify({'success': True, 'tmb': tmb, 'tdee': tdee, 'target_calories': target_calories})

def generate_first_week(db, user_id, target_calories, meals_per_day):
    """Genera la primera semana con 1 opción por comida."""
    week = get_week_number()
    meal_types = ['desayuno', 'almuerzo', 'comida', 'merienda', 'cena'][:meals_per_day]
    
    for day in range(1, 8):  # 7 días
        for meal_type in meal_types:
            # Seleccionar receta aleatoria del tipo
            recipe = db.execute('''
                SELECT * FROM master_recipes WHERE meal_type = ? ORDER BY RANDOM() LIMIT 1
            ''', (meal_type,)).fetchone()
            
            if recipe:
                db.execute('''
                    INSERT INTO weekly_plans (user_id, week_number, day_of_week, meal_type, 
                                             selected_recipe_id, calories, protein, carbs, fat)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (user_id, week, day, meal_type, recipe['id'], 
                      recipe['calories'], recipe['protein'], recipe['carbs'], recipe['fat']))
                
                # Añadir al banco de comidas del usuario
                db.execute('''
                    INSERT INTO user_food_bank (user_id, meal_type, recipe_id, added_week)
                    VALUES (?, ?, ?, ?)
                ''', (user_id, meal_type, recipe['id'], week))
    
    db.commit()

@app.route('/api/plan/current', methods=['GET'])
def get_current_plan():
    """Obtiene plan semanal actual del usuario."""
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': 'user_id requerido'}), 400
    
    db = get_db()
    week = get_week_number()
    
    plan = db.execute('''
        SELECT wp.*, mr.name as recipe_name, mr.ingredients, mr.instructions, 
               mr.supermarket, mr.category
        FROM weekly_plans wp
        JOIN master_recipes mr ON wp.selected_recipe_id = mr.id
        WHERE wp.user_id = ? AND wp.week_number = ?
        ORDER BY wp.day_of_week, wp.meal_type
    ''', (user_id, week)).fetchall()
    
    # Calcular totales diarios
    daily_totals = {}
    for row in plan:
        day = row['day_of_week']
        if day not in daily_totals:
            daily_totals[day] = {'calories': 0, 'protein': 0, 'carbs': 0, 'fat': 0}
        daily_totals[day]['calories'] += row['calories'] or 0
        daily_totals[day]['protein'] += row['protein'] or 0
        daily_totals[day]['carbs'] += row['carbs'] or 0
        daily_totals[day]['fat'] += row['fat'] or 0
    
    return jsonify({
        'week': week,
        'meals': [dict(row) for row in plan],
        'daily_totals': daily_totals
    })

@app.route('/api/food-bank/options', methods=['GET'])
def get_food_bank_options():
    """Obtiene opciones disponibles en el banco de comidas del usuario."""
    user_id = request.args.get('user_id')
    meal_type = request.args.get('meal_type')
    if not user_id:
        return jsonify({'error': 'user_id requerido'}), 400
    
    db = get_db()
    
    if meal_type:
        options = db.execute('''
            SELECT ufb.*, mr.name, mr.calories, mr.protein, mr.carbs, mr.fat, 
                   mr.ingredients, mr.supermarket
            FROM user_food_bank ufb
            JOIN master_recipes mr ON ufb.recipe_id = mr.id
            WHERE ufb.user_id = ? AND ufb.meal_type = ?
            ORDER BY ufb.times_used ASC
        ''', (user_id, meal_type)).fetchall()
    else:
        options = db.execute('''
            SELECT ufb.*, mr.name, mr.meal_type, mr.calories, mr.protein, mr.carbs, mr.fat
            FROM user_food_bank ufb
            JOIN master_recipes mr ON ufb.recipe_id = mr.id
            WHERE ufb.user_id = ?
            ORDER BY ufb.meal_type, ufb.times_used ASC
        ''', (user_id,)).fetchall()
    
    return jsonify({'options': [dict(row) for row in options]})

@app.route('/api/plan/swap', methods=['POST'])
def swap_meal_option():
    """Cambia una comida por otra opción del banco."""
    data = request.json
    db = get_db()
    user_id = data.get('user_id')
    
    if not all(k in data for k in ('day', 'meal_type', 'new_recipe_id')):
        return jsonify({'error': 'Datos incompletos'}), 400
    
    week = get_week_number()
    
    # Obtener nueva receta
    recipe = db.execute('SELECT * FROM master_recipes WHERE id = ?', 
                       (data['new_recipe_id'],)).fetchone()
    if not recipe:
        return jsonify({'error': 'Receta no encontrada'}), 404
    
    # Actualizar plan
    db.execute('''
        UPDATE weekly_plans 
        SET selected_recipe_id = ?, calories = ?, protein = ?, carbs = ?, fat = ?
        WHERE user_id = ? AND week_number = ? AND day_of_week = ? AND meal_type = ?
    ''', (data['new_recipe_id'], recipe['calories'], recipe['protein'], 
          recipe['carbs'], recipe['fat'], user_id, week, data['day'], data['meal_type']))
    
    # Actualizar contador de uso
    db.execute('''
        UPDATE user_food_bank 
        SET times_used = times_used + 1 
        WHERE user_id = ? AND recipe_id = ?
    ''', (user_id, data['new_recipe_id']))
    
    db.commit()
    return jsonify({'success': True})

@app.route('/api/weight/checkin', methods=['POST'])
def weight_checkin():
    """Registro semanal de peso para desbloquear nueva semana."""
    data = request.json
    db = get_db()
    user_id = data.get('user_id')
    new_weight = data.get('weight')
    
    if not user_id or not new_weight:
        return jsonify({'error': 'Datos incompletos'}), 400
    
    week = get_week_number()
    
    # Guardar peso
    db.execute('INSERT INTO weight_history (user_id, weight_kg, week_number) VALUES (?, ?, ?)',
              (user_id, new_weight, week))
    
    # Obtener perfil para recalcular
    profile = db.execute('SELECT * FROM user_profiles WHERE user_id = ?', (user_id,)).fetchone()
    
    if profile:
        # Recalcular calorías con nuevo peso
        tmb, tdee = calculate_tmb(profile['age'], profile['gender'], profile['height_cm'],
                                  new_weight, profile['activity_level'])
        target_calories = calculate_deficit(tdee, profile['goal_type'],
                                           new_weight, profile['goal_weight'])
        
        # Añadir NUEVA opción a cada tipo de comida (sistema progresivo)
        meal_types = ['desayuno', 'almuerzo', 'comida', 'merienda', 'cena'][:profile['meals_per_day']]
        
        for meal_type in meal_types:
            # Verificar cuántas opciones tiene ya (máximo 6)
            existing = db.execute('''
                SELECT COUNT(*) as count FROM user_food_bank 
                WHERE user_id = ? AND meal_type = ?
            ''', (user_id, meal_type)).fetchone()['count']
            
            if existing < 6:
                # Añadir nueva receta aleatoria
                new_recipe = db.execute('''
                    SELECT * FROM master_recipes WHERE meal_type = ? 
                    AND id NOT IN (SELECT recipe_id FROM user_food_bank WHERE user_id = ? AND meal_type = ?)
                    ORDER BY RANDOM() LIMIT 1
                ''', (meal_type, user_id, meal_type)).fetchone()
                
                if new_recipe:
                    db.execute('''
                        INSERT INTO user_food_bank (user_id, meal_type, recipe_id, added_week)
                        VALUES (?, ?, ?, ?)
                    ''', (user_id, meal_type, new_recipe['id'], week))
        
        db.commit()
        
        return jsonify({
            'success': True,
            'new_target_calories': target_calories,
            'new_options_added': True
        })
    
    return jsonify({'error': 'Perfil no encontrado'}), 404

@app.route('/api/shopping-list', methods=['GET'])
def get_shopping_list():
    """Genera lista de la compra consolidada."""
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': 'user_id requerido'}), 400
    
    db = get_db()
    week = get_week_number()
    
    # Obtener todas las recetas de la semana
    recipes = db.execute('''
        SELECT DISTINCT mr.ingredients, mr.supermarket
        FROM weekly_plans wp
        JOIN master_recipes mr ON wp.selected_recipe_id = mr.id
        WHERE wp.user_id = ? AND wp.week_number = ?
    ''', (user_id, week)).fetchall()
    
    # Agrupar por supermercado
    shopping_list = {'mercadona': [], 'lidl': [], 'mixto': []}
    for recipe in recipes:
        ingredients = recipe['ingredients'].split(', ')
        supermarket = recipe['supermarket']
        if supermarket not in shopping_list:
            shopping_list[supermarket] = []
        shopping_list[supermarket].extend(ingredients)
    
    # Eliminar duplicados
    for key in shopping_list:
        shopping_list[key] = list(set(shopping_list[key]))
    
    return jsonify({'shopping_list': shopping_list})

@app.route('/api/stats', methods=['GET'])
def get_user_stats():
    """Obtiene estadísticas del usuario."""
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': 'user_id requerido'}), 400
    
    db = get_db()
    
    # Historial de peso
    weight_history = db.execute('''
        SELECT weight_kg, week_number, recorded_at 
        FROM weight_history 
        WHERE user_id = ? 
        ORDER BY week_number
    ''', (user_id,)).fetchall()
    
    # Progreso
    profile = db.execute('SELECT current_weight_kg, goal_weight_kg FROM user_profiles WHERE user_id = ?', 
                        (user_id,)).fetchone()
    
    current = weight_history[-1]['weight_kg'] if weight_history else profile['current_weight_kg']
    goal = profile['goal_weight_kg']
    progress = ((profile['current_weight_kg'] - current) / (profile['current_weight_kg'] - goal)) * 100
    
    return jsonify({
        'weight_history': [dict(row) for row in weight_history],
        'current_weight': current,
        'goal_weight': goal,
        'progress_percent': round(progress, 1)
    })

# ============================================================
# INICIALIZACIÓN
# ============================================================

# Inicializar DB al importar
if not os.path.exists(DATABASE):
    init_db()
    seed_recipes()

def handler(event, context):
    """Handler para Vercel serverless."""
    from flask import Response
    with app.app_context():
        if not os.path.exists(DATABASE):
            init_db()
            seed_recipes()
        response = app.full_dispatch_request()
        return {
            'statusCode': response.status_code,
            'headers': dict(response.headers),
            'body': response.get_data().decode('utf-8')
        }

if __name__ == '__main__':
    init_db()
    seed_recipes()
    app.run(debug=True, port=5000)
