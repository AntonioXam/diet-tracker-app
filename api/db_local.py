"""
Base de datos local SQLite para desarrollo y pruebas
"""
import sqlite3
import json
import os
from datetime import datetime
from contextlib import contextmanager

DB_PATH = os.path.join(os.path.dirname(__file__), 'local.db')

@contextmanager
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    """Inicializa la base de datos local"""
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Tabla de usuarios
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                salt TEXT NOT NULL,
                name TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabla de perfiles
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_profiles (
                id TEXT PRIMARY KEY,
                user_id TEXT UNIQUE NOT NULL,
                age INTEGER,
                gender TEXT,
                height_cm REAL,
                weight_kg REAL,
                target_weight_kg REAL,
                goal_type TEXT,
                activity_level TEXT,
                budget TEXT DEFAULT 'medium',
                meals_per_day INTEGER DEFAULT 4,
                target_calories INTEGER,
                preferences TEXT,
                allergies TEXT,
                onboarding_completed BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        # Tabla de recetas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS master_recipes (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                meal_type TEXT,
                calories INTEGER,
                protein REAL,
                carbs REAL,
                fat REAL,
                ingredients TEXT,
                instructions TEXT,
                tags TEXT
            )
        ''')
        
        # Tabla de planes semanales
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS weekly_plans (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                week_number INTEGER,
                day_of_week INTEGER,
                meal_type TEXT,
                recipe_id TEXT,
                calories INTEGER,
                protein REAL,
                carbs REAL,
                fat REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (recipe_id) REFERENCES master_recipes(id)
            )
        ''')
        
        # Tabla de registro de comida
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS food_logs (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                meal_type TEXT,
                food_name TEXT,
                calories INTEGER,
                protein REAL,
                carbs REAL,
                fat REAL,
                quantity REAL DEFAULT 1,
                source TEXT DEFAULT 'manual',
                logged_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        # Tabla de lista de compra
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS shopping_items (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                ingredient_name TEXT NOT NULL,
                amount REAL,
                unit TEXT,
                supermarket TEXT DEFAULT 'generic',
                checked BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        conn.commit()
        
        # Insertar recetas si no existen
        cursor.execute('SELECT COUNT(*) FROM master_recipes')
        if cursor.fetchone()[0] == 0:
            insert_recipes(cursor)
            conn.commit()

def insert_recipes(cursor):
    """Inserta recetas de ejemplo"""
    import uuid
    
    recipes = [
        # Desayunos
        {"id": str(uuid.uuid4()), "name": "Tostadas con aguacate y huevo", "meal_type": "breakfast", "calories": 350, "protein": 15, "carbs": 25, "fat": 20, "tags": "vegetarian,healthy"},
        {"id": str(uuid.uuid4()), "name": "Batido de proteínas con frutas", "meal_type": "breakfast", "calories": 300, "protein": 25, "carbs": 35, "fat": 5, "tags": "vegetarian,quick"},
        {"id": str(uuid.uuid4()), "name": "Tortilla de espinacas", "meal_type": "breakfast", "calories": 280, "protein": 18, "carbs": 8, "fat": 20, "tags": "vegetarian,keto"},
        {"id": str(uuid.uuid4()), "name": "Avena con frutos rojos", "meal_type": "breakfast", "calories": 320, "protein": 12, "carbs": 55, "fat": 6, "tags": "vegetarian,healthy"},
        {"id": str(uuid.uuid4()), "name": "Yogur griego con granola", "meal_type": "breakfast", "calories": 290, "protein": 20, "carbs": 30, "fat": 8, "tags": "vegetarian,quick"},
        
        # Comidas
        {"id": str(uuid.uuid4()), "name": "Ensalada César con pollo", "meal_type": "lunch", "calories": 450, "protein": 35, "carbs": 15, "fat": 28, "tags": "healthy,protein"},
        {"id": str(uuid.uuid4()), "name": "Pasta integral con verduras", "meal_type": "lunch", "calories": 400, "protein": 15, "carbs": 65, "fat": 10, "tags": "vegetarian,healthy"},
        {"id": str(uuid.uuid4()), "name": "Salmón al horno con verduras", "meal_type": "lunch", "calories": 500, "protein": 40, "carbs": 20, "fat": 28, "tags": "healthy,omega3"},
        {"id": str(uuid.uuid4()), "name": "Wraps de pavo y aguacate", "meal_type": "lunch", "calories": 380, "protein": 28, "carbs": 35, "fat": 15, "tags": "quick,protein"},
        {"id": str(uuid.uuid4()), "name": "Quinoa con verduras asadas", "meal_type": "lunch", "calories": 420, "protein": 18, "carbs": 55, "fat": 14, "tags": "vegetarian,vegan"},
        
        # Cenas
        {"id": str(uuid.uuid4()), "name": "Pollo al curry con arroz", "meal_type": "dinner", "calories": 550, "protein": 42, "carbs": 45, "fat": 18, "tags": "protein"},
        {"id": str(uuid.uuid4()), "name": "Sopa de lentejas", "meal_type": "dinner", "calories": 350, "protein": 22, "carbs": 45, "fat": 8, "tags": "vegetarian,vegan"},
        {"id": str(uuid.uuid4()), "name": "Filete de ternera con ensalada", "meal_type": "dinner", "calories": 600, "protein": 50, "carbs": 10, "fat": 38, "tags": "protein,keto"},
        {"id": str(uuid.uuid4()), "name": "Pescado al papillote", "meal_type": "dinner", "calories": 320, "protein": 35, "carbs": 15, "fat": 12, "tags": "healthy,quick"},
        {"id": str(uuid.uuid4()), "name": "Revuelto de verduras", "meal_type": "dinner", "calories": 280, "protein": 15, "carbs": 12, "fat": 20, "tags": "vegetarian,quick"},
        
        # Snacks
        {"id": str(uuid.uuid4()), "name": "Frutos secos", "meal_type": "snack", "calories": 180, "protein": 5, "carbs": 10, "fat": 15, "tags": "vegetarian,keto"},
        {"id": str(uuid.uuid4()), "name": "Yogur natural", "meal_type": "snack", "calories": 100, "protein": 8, "carbs": 8, "fat": 4, "tags": "vegetarian,quick"},
        {"id": str(uuid.uuid4()), "name": "Manzana con mantequilla de cacahuete", "meal_type": "snack", "calories": 200, "protein": 5, "carbs": 25, "fat": 10, "tags": "vegetarian"},
        {"id": str(uuid.uuid4()), "name": "Huevo duro", "meal_type": "snack", "calories": 70, "protein": 6, "carbs": 0, "fat": 5, "tags": "quick,keto"},
        {"id": str(uuid.uuid4()), "name": "Barra de proteínas", "meal_type": "snack", "calories": 220, "protein": 20, "carbs": 22, "fat": 8, "tags": "quick"},
    ]
    
    for recipe in recipes:
        cursor.execute('''
            INSERT INTO master_recipes (id, name, meal_type, calories, protein, carbs, fat, tags)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            recipe['id'], recipe['name'], recipe['meal_type'], recipe['calories'],
            recipe['protein'], recipe['carbs'], recipe['fat'], recipe.get('tags', '')
        ))

# Inicializar DB al importar
init_db()