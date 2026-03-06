-- ============================================
-- MIGRACIÓN: Añadir campos de enriquecimiento a master_recipes
-- Fecha: 2026-03-06
-- ============================================

-- 1. Añadir columna difficulty (dificultad)
ALTER TABLE master_recipes 
ADD COLUMN IF NOT EXISTS difficulty TEXT 
CHECK (difficulty IN ('facil', 'medio', 'dificil'))
DEFAULT 'medio';

-- 2. Añadir columna cost (coste)
ALTER TABLE master_recipes 
ADD COLUMN IF NOT EXISTS cost TEXT 
CHECK (cost IN ('barato', 'medio', 'caro'))
DEFAULT 'medio';

-- 3. Añadir columna tags (etiquetas dietéticas)
ALTER TABLE master_recipes 
ADD COLUMN IF NOT EXISTS tags TEXT[] 
DEFAULT '{}';

-- 4. Crear índice para tags (búsquedas eficientes)
CREATE INDEX IF NOT EXISTS idx_master_recipes_tags ON master_recipes USING GIN(tags);

-- 5. Añadir columna prep_time_min si no existe (ya existe, pero por si acaso)
-- ALTER TABLE master_recipes ADD COLUMN IF NOT EXISTS prep_time_min INTEGER DEFAULT 15;

-- ============================================
-- COMENTARIOS SOBRE LA ESTRUCTURA JSON DE INGREDIENTES
-- ============================================
-- 
-- Formato recomendado para ingredients (JSONB):
-- [
--   {
--     "name": "Huevos",
--     "quantity": 2,
--     "unit": "unidades",
--     "optional": false
--   },
--   {
--     "name": "Leche desnatada",
--     "quantity": 100,
--     "unit": "ml",
--     "optional": false
--   }
-- ]
--
-- Formato para instructions (TEXT):
-- Paso 1: Batir los huevos en un bol.
-- Paso 2: Añadir la leche y mezclar bien.
-- Paso 3: Cocinar en sartén a fuego medio.

-- ============================================
-- ACTUALIZACIONES DE RECETAS EXISTENTES
-- ============================================

-- Actualizar algunas recetas con valores por defecto basados en complejidad
-- Recetas con más de 500 calorías -> más probables de ser medio/difícil
-- Recetas con menos de 300 calorías -> más probables de ser fáciles

-- Marcar recetas simples como fáciles
UPDATE master_recipes 
SET difficulty = 'facil',
    tags = ARRAY['rapido', 'sencillo']
WHERE calories < 300 
AND ingredients IS NULL
AND difficulty = 'medio';

-- Marcar recetas elaboradas como difíciles
UPDATE master_recipes 
SET difficulty = 'dificil',
    tags = ARRAY['elaborado']
WHERE calories > 700 
AND ingredients IS NULL
AND difficulty = 'medio';

-- ============================================
-- VISTA ÚTIL PARA RECETAS CON INGREDIENTES
-- ============================================
CREATE OR REPLACE VIEW recipes_with_details AS
SELECT 
  id,
  name,
  description,
  meal_type,
  supermarket,
  calories,
  protein_g,
  carbs_g,
  fat_g,
  fiber_g,
  ingredients,
  instructions,
  difficulty,
  cost,
  tags,
  prep_time_min,
  servings,
  image_url,
  rating
FROM master_recipes
ORDER BY meal_type, name;

-- ============================================
-- FUNCIÓN PARA BUSCAR POR TAGS
-- ============================================
CREATE OR REPLACE FUNCTION search_recipes_by_tags(search_tags TEXT[])
RETURNS SETOF master_recipes AS $$
BEGIN
  RETURN QUERY
  SELECT * FROM master_recipes
  WHERE tags && search_tags
  ORDER BY rating DESC, name;
END;
$$ LANGUAGE plpgsql;

-- ============================================
-- FUNCIÓN PARA BUSCAR POR INGREDIENTES
-- ============================================
CREATE OR REPLACE FUNCTION search_recipes_by_ingredient(ingredient_name TEXT)
RETURNS SETOF master_recipes AS $$
BEGIN
  RETURN QUERY
  SELECT * FROM master_recipes
  WHERE ingredients::text ILIKE '%' || ingredient_name || '%'
  ORDER BY rating DESC, name;
END;
$$ LANGUAGE plpgsql;