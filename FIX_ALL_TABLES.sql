-- ============================================
-- ARREGLAR TODAS LAS TABLAS
-- ============================================

-- 1. user_profiles - Añadir columnas faltantes
ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS user_id UUID REFERENCES users(id);
ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS disliked_foods TEXT;
ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS budget VARCHAR(20) DEFAULT 'medium';
ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS meals_per_day INTEGER DEFAULT 4;
ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS target_calories INTEGER;
ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS preferences TEXT;
ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS onboarding_completed BOOLEAN DEFAULT FALSE;
ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS height_cm FLOAT;
ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS weight_kg FLOAT;
ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS target_weight_kg FLOAT;
ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS goal VARCHAR(20);
ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS tmb INTEGER;
ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS tdee INTEGER;

-- 2. weekly_plans - Añadir columnas faltantes
ALTER TABLE weekly_plans ADD COLUMN IF NOT EXISTS user_id UUID REFERENCES users(id);
ALTER TABLE weekly_plans ADD COLUMN IF NOT EXISTS day_of_week INTEGER;
ALTER TABLE weekly_plans ADD COLUMN IF NOT EXISTS selected_recipe_id UUID REFERENCES master_recipes(id);
ALTER TABLE weekly_plans ADD COLUMN IF NOT EXISTS calories INTEGER;
ALTER TABLE weekly_plans ADD COLUMN IF NOT EXISTS protein DECIMAL(6,2);
ALTER TABLE weekly_plans ADD COLUMN IF NOT EXISTS carbs DECIMAL(6,2);
ALTER TABLE weekly_plans ADD COLUMN IF NOT EXISTS fat DECIMAL(6,2);
ALTER TABLE weekly_plans ADD COLUMN IF NOT EXISTS week_number INTEGER;
ALTER TABLE weekly_plans ADD COLUMN IF NOT EXISTS meal_type VARCHAR(20);
ALTER TABLE weekly_plans ADD COLUMN IF NOT EXISTS recipe_id UUID;

-- 3. food_logs - Añadir columnas faltantes
ALTER TABLE food_logs ADD COLUMN IF NOT EXISTS user_id UUID REFERENCES users(id);
ALTER TABLE food_logs ADD COLUMN IF NOT EXISTS meal_type VARCHAR(20);
ALTER TABLE food_logs ADD COLUMN IF NOT EXISTS source VARCHAR(20) DEFAULT 'manual';
ALTER TABLE food_logs ADD COLUMN IF NOT EXISTS barcode VARCHAR(50);
ALTER TABLE food_logs ADD COLUMN IF NOT EXISTS food_name VARCHAR(255);
ALTER TABLE food_logs ADD COLUMN IF NOT EXISTS recipe_id UUID;
ALTER TABLE food_logs ADD COLUMN IF NOT EXISTS calories INTEGER;
ALTER TABLE food_logs ADD COLUMN IF NOT EXISTS protein DECIMAL(6,2);
ALTER TABLE food_logs ADD COLUMN IF NOT EXISTS carbs DECIMAL(6,2);
ALTER TABLE food_logs ADD COLUMN IF NOT EXISTS fat DECIMAL(6,2);
ALTER TABLE food_logs ADD COLUMN IF NOT EXISTS quantity DECIMAL(6,2) DEFAULT 1;
ALTER TABLE food_logs ADD COLUMN IF NOT EXISTS notes TEXT;
ALTER TABLE food_logs ADD COLUMN IF NOT EXISTS week_number INTEGER;
ALTER TABLE food_logs ADD COLUMN IF NOT EXISTS day_of_week INTEGER;
ALTER TABLE food_logs ADD COLUMN IF NOT EXISTS logged_at TIMESTAMP DEFAULT NOW();

-- 4. Crear índices para mejorar rendimiento
CREATE INDEX IF NOT EXISTS idx_user_profiles_user_id ON user_profiles(user_id);
CREATE INDEX IF NOT EXISTS idx_weekly_plans_user_id ON weekly_plans(user_id);
CREATE INDEX IF NOT EXISTS idx_food_logs_user_id ON food_logs(user_id);
CREATE INDEX IF NOT EXISTS idx_food_logs_logged_at ON food_logs(logged_at);

-- 5. Verificar que las columnas existen
SELECT 'user_profiles' as tabla, column_name, data_type FROM information_schema.columns 
WHERE table_name = 'user_profiles' AND column_name IN ('user_id', 'disliked_foods', 'budget', 'meals_per_day', 'target_calories', 'preferences', 'onboarding_completed');

SELECT 'weekly_plans' as tabla, column_name, data_type FROM information_schema.columns 
WHERE table_name = 'weekly_plans' AND column_name IN ('user_id', 'day_of_week', 'selected_recipe_id', 'calories', 'protein', 'carbs', 'fat', 'week_number');

SELECT 'food_logs' as tabla, column_name, data_type FROM information_schema.columns 
WHERE table_name = 'food_logs' AND column_name IN ('user_id', 'meal_type', 'source', 'barcode', 'food_name', 'calories', 'protein', 'carbs', 'fat');