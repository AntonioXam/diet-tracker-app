-- ============================================
-- LIMPIAR BASE DE DATOS - Borrar usuarios test
-- Ejecutar en: https://supabase.com/dashboard/project/kaomgwojvnncidyezdzj/sql/new
-- ============================================

-- 1. Borrar todos los users de la tabla users
DELETE FROM users;

-- 2. Borrar todos los user_profiles
DELETE FROM user_profiles;

-- 3. Borrar weight_history
DELETE FROM weight_history;

-- 4. Borrar food_logs
DELETE FROM food_logs;

-- 5. Borrar shopping_lists
DELETE FROM shopping_lists;

-- 6. Borrar weekly_plans
DELETE FROM weekly_plans;

-- 7. Borrar plan_meals
DELETE FROM plan_meals;

-- 8. Resetear secuencias (si aplica)
-- Verificar que está vacío
SELECT 'users' as tabla, COUNT(*) as count FROM users
UNION ALL
SELECT 'user_profiles', COUNT(*) FROM user_profiles
UNION ALL
SELECT 'weight_history', COUNT(*) FROM weight_history
UNION ALL
SELECT 'food_logs', COUNT(*) FROM food_logs
UNION ALL
SELECT 'shopping_lists', COUNT(*) FROM shopping_lists
UNION ALL
SELECT 'weekly_plans', COUNT(*) FROM weekly_plans
UNION ALL
SELECT 'plan_meals', COUNT(*) FROM plan_meals;

-- 9. Mantener master_recipes (20 recetas)
SELECT 'master_recipes', COUNT(*) FROM master_recipes;
