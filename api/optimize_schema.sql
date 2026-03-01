-- Optimizaciones para la base de datos Diet Tracker
-- Incluye índices adicionales, integridad referencial y mejoras de rendimiento

-- 1. Agregar ON DELETE CASCADE a las claves foráneas para mantener integridad
-- Nota: Esto podría eliminar datos existentes si hay inconsistencias, asegúrese de hacer backup.

-- user_profiles ya tiene PRIMARY KEY que referencia users(id). Agregar ON DELETE CASCADE.
ALTER TABLE user_profiles DROP CONSTRAINT IF EXISTS user_profiles_user_id_fkey;
ALTER TABLE user_profiles ADD CONSTRAINT user_profiles_user_id_fkey 
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;

-- weight_history
ALTER TABLE weight_history DROP CONSTRAINT IF EXISTS weight_history_user_id_fkey;
ALTER TABLE weight_history ADD CONSTRAINT weight_history_user_id_fkey 
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;

-- user_food_bank (dos claves foráneas)
ALTER TABLE user_food_bank DROP CONSTRAINT IF EXISTS user_food_bank_user_id_fkey;
ALTER TABLE user_food_bank ADD CONSTRAINT user_food_bank_user_id_fkey 
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;

ALTER TABLE user_food_bank DROP CONSTRAINT IF EXISTS user_food_bank_recipe_id_fkey;
ALTER TABLE user_food_bank ADD CONSTRAINT user_food_bank_recipe_id_fkey 
    FOREIGN KEY (recipe_id) REFERENCES master_recipes(id) ON DELETE CASCADE;

-- weekly_plans (dos claves foráneas)
ALTER TABLE weekly_plans DROP CONSTRAINT IF EXISTS weekly_plans_user_id_fkey;
ALTER TABLE weekly_plans ADD CONSTRAINT weekly_plans_user_id_fkey 
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;

ALTER TABLE weekly_plans DROP CONSTRAINT IF EXISTS weekly_plans_selected_recipe_id_fkey;
ALTER TABLE weekly_plans ADD CONSTRAINT weekly_plans_selected_recipe_id_fkey 
    FOREIGN KEY (selected_recipe_id) REFERENCES master_recipes(id) ON DELETE CASCADE;

-- 2. Índices adicionales para mejorar rendimiento de consultas

-- weight_history: índice para consultas ordenadas por fecha y por semana
CREATE INDEX IF NOT EXISTS idx_weight_user_created ON weight_history(user_id, recorded_at);
CREATE INDEX IF NOT EXISTS idx_weight_user_week ON weight_history(user_id, week_number);

-- master_recipes: índices para category y supermarket si se filtran frecuentemente
CREATE INDEX IF NOT EXISTS idx_recipes_category ON master_recipes(category);
CREATE INDEX IF NOT EXISTS idx_recipes_supermarket ON master_recipes(supermarket);
-- Índice compuesto para búsquedas por meal_type y exclusión por id
CREATE INDEX IF NOT EXISTS idx_recipes_meal_id ON master_recipes(meal_type, id);

-- user_food_bank: índice para la función increment_recipe_usage y joins por recipe_id
CREATE INDEX IF NOT EXISTS idx_foodbank_user_recipe ON user_food_bank(user_id, recipe_id);
CREATE INDEX IF NOT EXISTS idx_foodbank_recipe ON user_food_bank(recipe_id);

-- weekly_plans: índice covering para consultas comunes (user, week, day)
CREATE INDEX IF NOT EXISTS idx_plans_user_week_day ON weekly_plans(user_id, week_number, day_of_week);
-- Índice para selected_recipe_id (clave foránea)
CREATE INDEX IF NOT EXISTS idx_plans_selected_recipe ON weekly_plans(selected_recipe_id);

-- 3. La función increment_recipe_usage ya existe. Se mantiene igual.
-- Se ha agregado el índice idx_foodbank_user_recipe para acelerar la actualización.

-- 4. Posible normalización: crear tabla de alergias y alimentos no deseados
-- Opcional: si se necesita consultar individualmente, descomentar.
/*
CREATE TABLE IF NOT EXISTS user_allergies (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id) ON DELETE CASCADE,
    allergy TEXT NOT NULL
);
CREATE INDEX idx_user_allergies_user ON user_allergies(user_id);

CREATE TABLE IF NOT EXISTS user_disliked_foods (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id) ON DELETE CASCADE,
    food TEXT NOT NULL
);
CREATE INDEX idx_user_disliked_user ON user_disliked_foods(user_id);
*/

-- 5. Estadísticas y mantenimiento
-- Actualizar estadísticas para el optimizador de consultas
ANALYZE users;
ANALYZE user_profiles;
ANALYZE weight_history;
ANALYZE master_recipes;
ANALYZE user_food_bank;
ANALYZE weekly_plans;

-- Fin de optimizaciones