-- ============================================
-- INSERTAR 20 RECETAS EN SUPABASE
-- Ejecutar en: https://supabase.com/dashboard/project/kaomgwojvnncidyezdzj/sql/new
-- ============================================

-- Desactivar RLS temporalmente para insert (solo para seed inicial)
ALTER TABLE master_recipes DISABLE ROW LEVEL SECURITY;

-- Insertar DESAYUNOS (5)
INSERT INTO master_recipes (name, description, meal_type, supermarket, calories, protein_g, carbs_g, fat_g, image_url, prep_time_min, servings) VALUES
('Tortilla de claras con espinacas', 'Desayuno proteico bajo en calorías', 'breakfast', 'mercadona', 180, 20, 5, 8, 'https://images.unsplash.com/photo-1510693206972-df098062cb71?w=400', 10, 1),
('Avena con plátano y canela', 'Porridge cremoso y energético', 'breakfast', 'lidl', 320, 12, 55, 6, 'https://images.unsplash.com/photo-1517673132405-a56a62b18caf?w=400', 8, 1),
('Tostada de aguacate y huevo', 'Desayuno completo y saciante', 'breakfast', 'mercadona', 380, 18, 25, 24, 'https://images.unsplash.com/photo-1525351484163-7529414395d8?w=400', 12, 1),
('Yogur griego con frutos rojos', 'Desayuno ligero y proteico', 'breakfast', 'carrefour', 220, 18, 22, 6, 'https://images.unsplash.com/photo-1488477181946-6428a0291777?w=400', 5, 1),
('Batido de proteínas y plátano', 'Desayuno rápido post-entreno', 'breakfast', 'mercadona', 280, 25, 30, 6, 'https://images.unsplash.com/photo-1553530666-ba11a90694f3?w=400', 3, 1);

-- Insertar COMIDAS (5)
INSERT INTO master_recipes (name, description, meal_type, supermarket, calories, protein_g, carbs_g, fat_g, image_url, prep_time_min, servings) VALUES
('Pechuga de pollo a la plancha con ensalada', 'Comida clásica baja en calorías', 'lunch', 'mercadona', 420, 45, 12, 18, 'https://images.unsplash.com/photo-1532550907401-a500c9a57435?w=400', 20, 1),
('Salmón al horno con verduras', 'Comida rica en omega-3', 'lunch', 'lidl', 520, 40, 18, 32, 'https://images.unsplash.com/photo-1467003909585-2f8a7270028d?w=400', 25, 1),
('Ensalada de quinoa y garbanzos', 'Comida vegana completa', 'lunch', 'carrefour', 480, 18, 62, 16, 'https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=400', 15, 1),
('Pasta integral con pavo y tomate', 'Comida energética', 'lunch', 'mercadona', 520, 35, 68, 12, 'https://images.unsplash.com/photo-1551892374-ecf8754cf8b0?w=400', 25, 1),
('Bowl de arroz y ternera', 'Comida completa asiática', 'lunch', 'lidl', 580, 38, 72, 14, 'https://images.unsplash.com/photo-1512058564366-18510be2db19?w=400', 30, 1);

-- Insertar CENAS (5)
INSERT INTO master_recipes (name, description, meal_type, supermarket, calories, protein_g, carbs_g, fat_g, image_url, prep_time_min, servings) VALUES
('Merluza al vapor con espárragos', 'Cena ligera y digestiva', 'dinner', 'mercadona', 280, 32, 8, 12, 'https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?w=400', 20, 1),
('Tortilla francesa con ensalada', 'Cena rápida y proteica', 'dinner', 'lidl', 320, 22, 6, 22, 'https://images.unsplash.com/photo-1510693206972-df098062cb71?w=400', 12, 1),
('Crema de calabacín', 'Cena ligera reconfortante', 'dinner', 'carrefour', 180, 8, 18, 8, 'https://images.unsplash.com/photo-1547592166-23ac45744acd?w=400', 25, 1),
('Sepia a la plancha con verduras', 'Cena mediterránea', 'dinner', 'mercadona', 300, 35, 10, 14, 'https://images.unsplash.com/photo-1565557623262-b51c2513a641?w=400', 18, 1),
('Ensalada de atún y huevo', 'Cena fría y rápida', 'dinner', 'lidl', 340, 28, 8, 22, 'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=400', 10, 1);

-- Insertar MERIENDAS (5)
INSERT INTO master_recipes (name, description, meal_type, supermarket, calories, protein_g, carbs_g, fat_g, image_url, prep_time_min, servings) VALUES
('Manzana con almendras', 'Snack saludable', 'snack', 'mercadona', 180, 6, 22, 8, 'https://images.unsplash.com/photo-1568702846914-96b305d2aaeb?w=400', 3, 1),
('Barrita de proteínas casera', 'Snack proteico', 'snack', 'lidl', 220, 15, 18, 10, 'https://images.unsplash.com/photo-1579954115545-a95591f28bfc?w=400', 10, 1),
('Yogur con nueces', 'Snack saciante', 'snack', 'carrefour', 200, 12, 14, 10, 'https://images.unsplash.com/photo-1488477181946-6428a0291777?w=400', 3, 1),
('Zanahorias con hummus', 'Snack crujiente', 'snack', 'mercadona', 160, 6, 18, 8, 'https://images.unsplash.com/photo-1541519227354-08fa5d50c44d?w=400', 5, 1),
('Batido verde detox', 'Snack refrescante', 'snack', 'lidl', 140, 4, 28, 2, 'https://images.unsplash.com/photo-1610970881699-44a5587cabec?w=400', 5, 1);

-- Reactivar RLS
ALTER TABLE master_recipes ENABLE ROW LEVEL SECURITY;

-- Verificar
SELECT COUNT(*) as total_recetas FROM master_recipes;
SELECT meal_type, COUNT(*) as count FROM master_recipes GROUP BY meal_type;
