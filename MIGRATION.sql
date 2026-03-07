-- ============================================
-- MIGRACIÓN: Añadir columnas a user_profiles
-- ============================================
-- Ejecutar en: https://supabase.com/dashboard/project/kaomgwojvnncidyezdzj/sql/new

-- 1. Añadir columna budget
ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS budget VARCHAR(20) DEFAULT 'medium';

-- 2. Añadir columna meals_per_day
ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS meals_per_day INTEGER DEFAULT 4;

-- 3. Añadir columna target_calories
ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS target_calories INTEGER;

-- 4. Añadir columna preferences
ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS preferences TEXT;

-- 5. Añadir columna onboarding_completed
ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS onboarding_completed BOOLEAN DEFAULT FALSE;

-- ============================================
-- MIGRACIÓN: Añadir columnas a weekly_plans
-- ============================================

-- 6. Añadir columna day_of_week (día de la semana: 0=Lunes, 6=Domingo)
ALTER TABLE weekly_plans ADD COLUMN IF NOT EXISTS day_of_week INTEGER CHECK (day_of_week BETWEEN 0 AND 6);

-- 7. Añadir columna selected_recipe_id
ALTER TABLE weekly_plans ADD COLUMN IF NOT EXISTS selected_recipe_id UUID REFERENCES master_recipes(id);

-- 8. Añadir columna calories
ALTER TABLE weekly_plans ADD COLUMN IF NOT EXISTS calories INTEGER;

-- 9. Añadir columna protein
ALTER TABLE weekly_plans ADD COLUMN IF NOT EXISTS protein DECIMAL(6,2);

-- 10. Añadir columna carbs
ALTER TABLE weekly_plans ADD COLUMN IF NOT EXISTS carbs DECIMAL(6,2);

-- 11. Añadir columna fat
ALTER TABLE weekly_plans ADD COLUMN IF NOT EXISTS fat DECIMAL(6,2);

-- 12. Añadir columna week_number
ALTER TABLE weekly_plans ADD COLUMN IF NOT EXISTS week_number INTEGER;

-- ============================================
-- MIGRACIÓN: Añadir columnas a food_logs
-- ============================================

-- 13. Añadir columna meal_type (si no existe)
ALTER TABLE food_logs ADD COLUMN IF NOT EXISTS meal_type VARCHAR(20);

-- 14. Añadir columna source
ALTER TABLE food_logs ADD COLUMN IF NOT EXISTS source VARCHAR(20) DEFAULT 'manual';

-- 15. Añadir columna barcode
ALTER TABLE food_logs ADD COLUMN IF NOT EXISTS barcode VARCHAR(50);

-- ============================================
-- VERIFICACIÓN
-- ============================================

-- Verificar columnas en user_profiles
SELECT column_name, data_type, column_default 
FROM information_schema.columns 
WHERE table_name = 'user_profiles' 
AND column_name IN ('budget', 'meals_per_day', 'target_calories', 'preferences', 'onboarding_completed')
ORDER BY column_name;

-- Verificar columnas en weekly_plans
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'weekly_plans' 
AND column_name IN ('day_of_week', 'selected_recipe_id', 'calories', 'protein', 'carbs', 'fat', 'week_number')
ORDER BY column_name;

-- Verificar columnas en food_logs
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'food_logs' 
AND column_name IN ('meal_type', 'source', 'barcode')
ORDER BY column_name;