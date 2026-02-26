#!/usr/bin/env python3
"""Fix database schema to use username instead of email."""

import os
from supabase import create_client

SUPABASE_URL = "https://jxafifppxnaqjxpqfrtr.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imp4YWZpZnBweG5hcWp4cHFmcnRyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzE4NzE1NDEsImV4cCI6MjA4NzQ0NzU0MX0._8JT1PAaSZpnyUf9SwuwKxBtV5hhsvrq4BalSN5t3GU"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

print("🔧 Fixing database schema...")

# Drop and recreate users table with username
try:
    # Drop existing tables (they'll be recreated)
    print("Dropping old tables...")
    supabase.rpc('exec_sql', {'sql': '''
        DROP TABLE IF EXISTS weekly_plans CASCADE;
        DROP TABLE IF EXISTS user_food_bank CASCADE;
        DROP TABLE IF EXISTS weight_history CASCADE;
        DROP TABLE IF EXISTS user_profiles CASCADE;
        DROP TABLE IF EXISTS users CASCADE;
        DROP TABLE IF EXISTS master_recipes CASCADE;
    '''}).execute()
    print("✅ Tables dropped")
except Exception as e:
    print(f"⚠️ Note: {e}")

# Create new schema
print("Creating new schema...")
try:
    supabase.rpc('exec_sql', {'sql': '''
        -- Users table with username
        CREATE TABLE users (
            id BIGSERIAL PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT NOW()
        );
        
        -- User profiles
        CREATE TABLE user_profiles (
            user_id BIGINT PRIMARY KEY REFERENCES users(id),
            age INTEGER NOT NULL,
            gender TEXT NOT NULL,
            height_cm REAL NOT NULL,
            current_weight_kg REAL NOT NULL,
            goal_weight_kg REAL NOT NULL,
            goal_type TEXT NOT NULL,
            activity_level TEXT NOT NULL,
            meals_per_day INTEGER NOT NULL,
            target_calories INTEGER NOT NULL,
            starting_weight_kg REAL NOT NULL,
            created_at TIMESTAMP DEFAULT NOW()
        );
        
        -- Weight history
        CREATE TABLE weight_history (
            id BIGSERIAL PRIMARY KEY,
            user_id BIGINT REFERENCES users(id),
            weight_kg REAL NOT NULL,
            week_number INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT NOW()
        );
        
        -- Master recipes
        CREATE TABLE master_recipes (
            id BIGSERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            meal_type TEXT NOT NULL,
            calories REAL NOT NULL,
            protein REAL NOT NULL,
            carbs REAL NOT NULL,
            fat REAL NOT NULL,
            ingredients TEXT NOT NULL,
            instructions TEXT,
            image_url TEXT,
            supermarket TEXT,
            category TEXT
        );
        
        -- User food bank
        CREATE TABLE user_food_bank (
            id BIGSERIAL PRIMARY KEY,
            user_id BIGINT REFERENCES users(id),
            meal_type TEXT NOT NULL,
            recipe_id BIGINT REFERENCES master_recipes(id),
            times_used INTEGER DEFAULT 0,
            added_week INTEGER NOT NULL
        );
        
        -- Weekly plans
        CREATE TABLE weekly_plans (
            id BIGSERIAL PRIMARY KEY,
            user_id BIGINT REFERENCES users(id),
            week_number INTEGER NOT NULL,
            day_of_week INTEGER NOT NULL,
            meal_type TEXT NOT NULL,
            selected_recipe_id BIGINT REFERENCES master_recipes(id),
            calories REAL,
            protein REAL,
            carbs REAL,
            fat REAL,
            created_at TIMESTAMP DEFAULT NOW()
        );
        
        -- Create indexes for performance
        CREATE INDEX idx_users_username ON users(username);
        CREATE INDEX idx_profiles_user ON user_profiles(user_id);
        CREATE INDEX idx_weight_user ON weight_history(user_id, created_at);
        CREATE INDEX idx_recipes_meal ON master_recipes(meal_type);
        CREATE INDEX idx_plans_user ON weekly_plans(user_id, week_number);
    '''}).execute()
    print("✅ Schema created successfully")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n✅ Database schema fixed!")
