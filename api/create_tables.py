#!/usr/bin/env python3
"""Crear tablas en Supabase usando la API de SQL."""

import requests
import json
import time

# Configuración
PROJECT_REF = "lwbhdgpvigivgpyjqbeo"
ACCESS_TOKEN = "sbp_1ec3b72a123fc51889736833ba04e4138adb3afa"
API_URL = f"https://api.supabase.com/v1/projects/{PROJECT_REF}/database/query"

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

# Sentencias SQL (extraídas de setup_db.py)
sql_statements = [
    # 1. Tabla users
    """CREATE TABLE IF NOT EXISTS users (
        id BIGSERIAL PRIMARY KEY,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        name TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT NOW()
    )""",
    
    # 2. Tabla user_profiles
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
    
    # 3. Tabla weight_history
    """CREATE TABLE IF NOT EXISTS weight_history (
        id BIGSERIAL PRIMARY KEY,
        user_id BIGINT REFERENCES users(id),
        weight_kg REAL NOT NULL,
        week_number INTEGER NOT NULL,
        recorded_at TIMESTAMP DEFAULT NOW()
    )""",
    
    # 4. Tabla master_recipes
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
    
    # 5. Tabla user_food_bank
    """CREATE TABLE IF NOT EXISTS user_food_bank (
        id BIGSERIAL PRIMARY KEY,
        user_id BIGINT REFERENCES users(id),
        meal_type TEXT NOT NULL,
        recipe_id BIGINT REFERENCES master_recipes(id),
        times_used INTEGER DEFAULT 0,
        added_week INTEGER NOT NULL
    )""",
    
    # 6. Tabla weekly_plans
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
    )""",
    
    # 7. Función para incrementar uso de receta
    """CREATE OR REPLACE FUNCTION increment_recipe_usage(p_user_id BIGINT, p_recipe_id BIGINT)
    RETURNS void AS $$
    BEGIN
        UPDATE user_food_bank 
        SET times_used = times_used + 1 
        WHERE user_id = p_user_id AND recipe_id = p_recipe_id;
    END;
    $$ LANGUAGE plpgsql""",
    
    # 8. Índices para mejorar rendimiento
    """CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)""",
    """CREATE INDEX IF NOT EXISTS idx_profiles_user ON user_profiles(user_id)""",
    """CREATE INDEX IF NOT EXISTS idx_weight_user ON weight_history(user_id)""",
    """CREATE INDEX IF NOT EXISTS idx_recipes_meal ON master_recipes(meal_type)""",
    """CREATE INDEX IF NOT EXISTS idx_foodbank_user ON user_food_bank(user_id, meal_type)""",
    """CREATE INDEX IF NOT EXISTS idx_plans_user_week ON weekly_plans(user_id, week_number)"""
]

print("🔧 Creando tablas en Supabase usando API de SQL...")

for i, sql in enumerate(sql_statements, 1):
    try:
        print(f"  [{i}/{len(sql_statements)}] Ejecutando...")
        response = requests.post(API_URL, headers=headers, json={"query": sql})
        
        if response.status_code == 200:
            result = response.json()
            if result == []:
                print(f"    ✅ Éxito")
            else:
                print(f"    ✅ Éxito: {result}")
        else:
            print(f"    ⚠️ Error {response.status_code}: {response.text[:100]}")
        
        # Pequeña pausa para no sobrecargar la API
        time.sleep(0.5)
        
    except Exception as e:
        print(f"    ❌ Excepción: {e}")

print("\n✅ ¡Tablas creadas! Verificando...")

# Verificar que las tablas existen
REST_URL = f"https://{PROJECT_REF}.supabase.co/rest/v1/"
ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imx3YmhkZ3B2aWdpdmdweWpxYmVvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzIwMzIwMTIsImV4cCI6MjA4NzYwODAxMn0.BVItT1CsufJ-Sgb8royDOKpOCMDAUnQD-ZmuvRSCd1U"

rest_headers = {
    "apikey": ANON_KEY,
    "Authorization": f"Bearer {ANON_KEY}"
}

tables_to_check = ["users", "user_profiles", "weight_history", "master_recipes", "user_food_bank", "weekly_plans"]

for table in tables_to_check:
    try:
        response = requests.get(f"{REST_URL}{table}", headers=rest_headers, params={"limit": "1"})
        if response.status_code == 200:
            print(f"  ✅ Tabla '{table}' existe")
        else:
            print(f"  ❌ Tabla '{table}' no accesible: {response.status_code}")
    except Exception as e:
        print(f"  ❌ Error verificando '{table}': {e}")

print("\n🎉 ¡Base de datos configurada!")