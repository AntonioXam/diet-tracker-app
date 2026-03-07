-- ============================================
-- ARREGLAR TODOS LOS TIPOS Y RLS
-- ============================================

-- 1. user_profiles - Arreglar tipos FLOAT
ALTER TABLE user_profiles ALTER COLUMN height_cm TYPE FLOAT USING COALESCE(height_cm::FLOAT, 0);
ALTER TABLE user_profiles ALTER COLUMN weight_kg TYPE FLOAT USING COALESCE(weight_kg::FLOAT, 0);
ALTER TABLE user_profiles ALTER COLUMN target_weight_kg TYPE FLOAT USING COALESCE(target_weight_kg::FLOAT, 0);

-- 2. food_logs - Desactivar RLS temporalmente
ALTER TABLE food_logs DISABLE ROW LEVEL SECURITY;

-- 3. user_profiles - Desactivar RLS temporalmente
ALTER TABLE user_profiles DISABLE ROW LEVEL SECURITY;

-- 4. weekly_plans - Desactivar RLS temporalmente
ALTER TABLE weekly_plans DISABLE ROW LEVEL SECURITY;

-- 5. weight_history - Desactivar RLS temporalmente
ALTER TABLE weight_history DISABLE ROW LEVEL SECURITY;

-- Verificar
SELECT tablename, rowsecurity FROM pg_tables WHERE schemaname = 'public' AND tablename IN ('food_logs', 'user_profiles', 'weekly_plans', 'weight_history');