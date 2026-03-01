#!/usr/bin/env python3
"""Inicializa DB en Supabase vía REST API."""
import requests
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

if not SUPABASE_URL or not SUPABASE_KEY:
    print("❌ Error: SUPABASE_URL y SUPABASE_KEY deben estar definidos en .env")
    exit(1)

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=minimal"
}

# Tablas a crear
tables = [
    """CREATE TABLE IF NOT EXISTS users (
        id BIGSERIAL PRIMARY KEY,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        name TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT NOW()
    )""",
    
    """CREATE TABLE IF NOT EXISTS user_profiles (
        user_id BIGINT PRIMARY KEY REFERENCES users(id),
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
        created_at TIMESTAMP DEFAULT NOW()
    )""",
    
    """CREATE TABLE IF NOT EXISTS weight_history (
        id BIGSERIAL PRIMARY KEY,
        user_id BIGINT REFERENCES users(id),
        weight_kg REAL NOT NULL,
        week_number INTEGER NOT NULL,
        recorded_at TIMESTAMP DEFAULT NOW()
    )""",
    
    """CREATE TABLE IF NOT EXISTS master_recipes (
        id BIGSERIAL PRIMARY KEY,
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
    )""",
    
    """CREATE TABLE IF NOT EXISTS user_food_bank (
        id BIGSERIAL PRIMARY KEY,
        user_id BIGINT REFERENCES users(id),
        meal_type TEXT NOT NULL,
        recipe_id BIGINT REFERENCES master_recipes(id),
        times_used INTEGER DEFAULT 0,
        added_week INTEGER NOT NULL
    )""",
    
    """CREATE TABLE IF NOT EXISTS weekly_plans (
        id BIGSERIAL PRIMARY KEY,
        user_id BIGINT REFERENCES users(id),
        week_number INTEGER NOT NULL,
        day_of_week INTEGER NOT NULL,
        meal_type TEXT NOT NULL,
        selected_recipe_id BIGINT REFERENCES master_recipes(id),
        calories REAL,
        protein REAL,
        carbs REAL,
        fat REAL
    )"""
]

print("🔧 Creando tablas en Supabase...")

for i, sql in enumerate(tables, 1):
    try:
        response = requests.post(
            f"{SUPABASE_URL}/rest/v1/rpc/exec_sql",
            headers=headers,
            json={"sql": sql}
        )
        if response.status_code in [200, 201, 204]:
            print(f"✅ Tabla {i}/6 creada")
        else:
            print(f"⚠️ Tabla {i}: {response.status_code} - {response.text[:100]}")
    except Exception as e:
        print(f"❌ Error tabla {i}: {e}")

print("\n✅ ¡Tablas creadas!")
