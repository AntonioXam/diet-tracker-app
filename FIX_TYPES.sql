-- ============================================
-- ARREGLAR TIPOS DE DATOS
-- ============================================

-- 1. user_profiles - Cambiar preferences a TEXT si es array
ALTER TABLE user_profiles ALTER COLUMN preferences TYPE TEXT USING COALESCE(preferences::TEXT, '');
ALTER TABLE user_profiles ALTER COLUMN allergies TYPE TEXT USING COALESCE(allergies::TEXT, '');
ALTER TABLE user_profiles ALTER COLUMN disliked_foods TYPE TEXT USING COALESCE(disliked_foods::TEXT, '');

-- 2. food_logs - Asegurar tipos numéricos correctos
ALTER TABLE food_logs ALTER COLUMN calories TYPE INTEGER USING COALESCE(calories::INTEGER, 0);
ALTER TABLE food_logs ALTER COLUMN protein TYPE DECIMAL(6,2) USING COALESCE(protein::DECIMAL(6,2), 0);
ALTER TABLE food_logs ALTER COLUMN carbs TYPE DECIMAL(6,2) USING COALESCE(carbs::DECIMAL(6,2), 0);
ALTER TABLE food_logs ALTER COLUMN fat TYPE DECIMAL(6,2) USING COALESCE(fat::DECIMAL(6,2), 0);

-- 3. weekly_plans - Asegurar tipos correctos
ALTER TABLE weekly_plans ALTER COLUMN calories TYPE INTEGER USING COALESCE(calories::INTEGER, 0);
ALTER TABLE weekly_plans ALTER COLUMN protein TYPE DECIMAL(6,2) USING COALESCE(protein::DECIMAL(6,2), 0);
ALTER TABLE weekly_plans ALTER COLUMN carbs TYPE DECIMAL(6,2) USING COALESCE(carbs::DECIMAL(6,2), 0);
ALTER TABLE weekly_plans ALTER COLUMN fat TYPE DECIMAL(6,2) USING COALESCE(fat::DECIMAL(6,2), 0);

-- Verificar cambios
SELECT column_name, data_type FROM information_schema.columns 
WHERE table_name = 'user_profiles' AND column_name IN ('preferences', 'allergies', 'disliked_foods');

SELECT column_name, data_type FROM information_schema.columns 
WHERE table_name = 'food_logs' AND column_name IN ('calories', 'protein', 'carbs', 'fat');