-- Arreglar user_profiles
ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS user_id UUID REFERENCES users(id);
ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS disliked_foods TEXT;
ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS budget VARCHAR(20) DEFAULT 'medium';
ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS meals_per_day INTEGER DEFAULT 4;
ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS target_calories INTEGER;
ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS preferences TEXT;
ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS onboarding_completed BOOLEAN DEFAULT FALSE;

-- Arreglar weekly_plans
ALTER TABLE weekly_plans ADD COLUMN IF NOT EXISTS user_id UUID REFERENCES users(id);
ALTER TABLE weekly_plans ADD COLUMN IF NOT EXISTS day_of_week INTEGER;
ALTER TABLE weekly_plans ADD COLUMN IF NOT EXISTS selected_recipe_id UUID REFERENCES master_recipes(id);
ALTER TABLE weekly_plans ADD COLUMN IF NOT EXISTS calories INTEGER;
ALTER TABLE weekly_plans ADD COLUMN IF NOT EXISTS protein DECIMAL(6,2);
ALTER TABLE weekly_plans ADD COLUMN IF NOT EXISTS carbs DECIMAL(6,2);
ALTER TABLE weekly_plans ADD COLUMN IF NOT EXISTS fat DECIMAL(6,2);
ALTER TABLE weekly_plans ADD COLUMN IF NOT EXISTS week_number INTEGER;

-- Arreglar food_logs
ALTER TABLE food_logs ADD COLUMN IF NOT EXISTS user_id UUID REFERENCES users(id);
ALTER TABLE food_logs ADD COLUMN IF NOT EXISTS meal_type VARCHAR(20);
ALTER TABLE food_logs ADD COLUMN IF NOT EXISTS source VARCHAR(20) DEFAULT 'manual';
ALTER TABLE food_logs ADD COLUMN IF NOT EXISTS barcode VARCHAR(50);