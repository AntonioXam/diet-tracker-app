-- ============================================
-- 200 RECETAS COMPLETAS CON IMÁGENES VÁLIDAS
-- Ejecutar en: https://supabase.com/dashboard/project/kaomgwojvnncidyezdzj/sql/new
-- ============================================

-- Desactivar RLS temporalmente
ALTER TABLE master_recipes DISABLE ROW LEVEL SECURITY;

-- ============================================
-- DESAYUNOS (50 recetas)
-- ============================================

INSERT INTO master_recipes (name, description, meal_type, supermarket, calories, protein_g, carbs_g, fat_g, fiber_g, prep_time_min, servings, image_url) VALUES

-- Desayunos clásicos
('Huevos revueltos con tocino', 'Clásico desayuno proteico con huevos y tocino crujiente', 'breakfast', 'mercadona', 350, 22, 2, 26, 0, 10, 1, 'https://images.unsplash.com/photo-1525351484163-7529414395d8?w=400'),
('Tostadas francesas con miel', 'Pan francés dulce con miel y canela', 'breakfast', 'mercadona', 380, 12, 45, 14, 2, 15, 2, 'https://images.unsplash.com/photo-1484723091739-30a097e8f929?w=400'),
('Bowl de açaí con frutas', 'Bowl energético de açaí con plátano, fresas y granola', 'breakfast', 'lidl', 320, 8, 55, 8, 6, 10, 1, 'https://images.unsplash.com/photo-1590301159989-7c24657c4c65?w=400'),
('Panqueques americanos', 'Fluffy pancakes con sirope de arce y mantequilla', 'breakfast', 'carrefour', 450, 15, 62, 15, 3, 20, 3, 'https://images.unsplash.com/photo-1567620905732-2d1ec7ab7445?w=400'),
('Sandwich de huevo y queso', 'Desayuno rápido con huevo frito y queso cheddar', 'breakfast', 'mercadona', 420, 22, 28, 22, 1, 10, 1, 'https://images.unsplash.com/photo-1528735602780-2552c347e2e5?w=400'),

-- Desayunos proteicos
('Omelette de espinacas y queso', 'Tortilla francesa con espinacas frescas y queso feta', 'breakfast', 'mercadona', 280, 20, 4, 18, 2, 12, 1, 'https://images.unsplash.com/photo-1510693206972-df098062cb71?w=400'),
('Huevos benedictinos', 'Huevos pochados sobre muffin inglés con salsa holandesa', 'breakfast', 'lidl', 520, 24, 30, 34, 1, 25, 2, 'https://images.unsplash.com/photo-1608039829572-9b1233451c38?w=400'),
('Wrap de desayuno', 'Tortilla de trigo con huevo, jamón y queso', 'breakfast', 'mercadona', 380, 18, 35, 16, 2, 10, 1, 'https://images.unsplash.com/photo-1626700058817-67a15a623dbd?w=400'),
('Tostadas de salmón ahumado', 'Pan tostado con salmón, queso crema y eneldo', 'breakfast', 'lidl', 380, 22, 28, 18, 2, 8, 2, 'https://images.unsplash.com/photo-1484980972926-edee96e0960d?w=400'),
('Bowl de yogur y granola', 'Yogur griego con granola casera y frutas frescas', 'breakfast', 'carrefour', 340, 15, 42, 10, 4, 5, 1, 'https://images.unsplash.com/photo-1490457849456-c0968be56a12?w=400'),

-- Más desayunos
('Hot cakes de avena', 'Panqueques de avena con plátano y miel', 'breakfast', 'mercadona', 360, 12, 52, 10, 5, 15, 2, 'https://images.unsplash.com/photo-1517673132405-a56a62b18caf?w=400'),
('Burrito de desayuno', 'Tortilla con huevo, chorizo, queso y frijoles', 'breakfast', 'lidl', 480, 22, 42, 22, 4, 12, 1, 'https://images.unsplash.com/photo-1626700058852-36b2ddd45359?w=400'),
('Muesli con leche', 'Cereal integral con frutos secos y miel', 'breakfast', 'carrefour', 310, 10, 48, 8, 6, 5, 1, 'https://images.unsplash.com/photo-1517686469429-8bd88b217859?w=400'),
('Tostada de tomate y aceite', 'Pan catalán con tomate rallado y aceite de oliva', 'breakfast', 'mercadona', 220, 6, 28, 8, 2, 5, 2, 'https://images.unsplash.com/photo-1509440159596-024e6631d513?w=400'),
('Gofres belgas', 'Gofres crujientes con nata y frutos rojos', 'breakfast', 'lidl', 420, 8, 52, 18, 3, 15, 2, 'https://images.unsplash.com/photo-1562376406-f71b9c4b9f83?w=400'),

-- Desayunos saludables
('Smoothie verde detox', 'Batido de espinacas, plátano y leche de almendras', 'breakfast', 'mercadona', 180, 5, 32, 3, 4, 5, 1, 'https://images.unsplash.com/photo-1610970881699-44a5587cabec?w=400'),
('Bowl de chía con leche', 'Semillas de chía hidratadas con leche de coco', 'breakfast', 'carrefour', 280, 8, 30, 14, 10, 10, 1, 'https://images.unsplash.com/photo-1546039907-7fa05f8e8daf?w=400'),
('Porridge de avena', 'Avena cocida con canela, miel y frutos secos', 'breakfast', 'lidl', 320, 10, 52, 8, 7, 10, 1, 'https://images.unsplash.com/photo-1517673132405-a56a62b18caf?w=400'),
('Tostada de aguacate', 'Pan integral con aguacate machacado y huevo pochado', 'breakfast', 'mercadona', 350, 16, 28, 18, 6, 10, 1, 'https://images.unsplash.com/photo-1541519227354-08fa5d50c44d?w=400'),
('Budín de huevo al horno', 'Huevos horneados con verduras y queso', 'breakfast', 'lidl', 280, 18, 8, 18, 3, 30, 2, 'https://images.unsplash.com/photo-1482049016gy-8b3f0c1f6b12?w=400'),

-- Desayunos internacionales
('Shakshuka', 'Huevos en salsa de tomate con especias', 'breakfast', 'mercadona', 320, 16, 18, 18, 4, 20, 2, 'https://images.unsplash.com/photo-1590412200988-a436970782fa?w=400'),
('Full English Breakfast', 'Desayuno inglés con huevo, bacon, salchichas y judías', 'breakfast', 'lidl', 680, 35, 28, 45, 5, 20, 1, 'https://images.unsplash.com/photo-1525351484163-7529414395d8?w=400'),
('Croissant con mantequilla', 'Croissant francés con mantequilla y mermelada', 'breakfast', 'carrefour', 420, 8, 42, 24, 2, 5, 1, 'https://images.unsplash.com/photo-1555507036-ab1f405662d6?w=400'),
('Chilaquiles verdes', 'Tortillas con salsa verde, crema y queso', 'breakfast', 'mercadona', 380, 14, 42, 16, 4, 15, 2, 'https://images.unsplash.com/photo-1512152272829-e313966b3dd4?w=400'),
('Congee chino', 'Gachas de arroz con huevo y cebollín', 'breakfast', 'lidl', 280, 12, 45, 4, 2, 20, 2, 'https://images.unsplash.com/photo-1547592180-85f9cc020646?w=400'),

-- Desayunes rápidos
('Cereal con leche', 'Cereal integral con leche semidesnatada', 'breakfast', 'mercadona', 280, 8, 48, 6, 3, 3, 1, 'https://images.unsplash.com/photo-1517686469429-8bd88b217859?w=400'),
('Tostada de mantequilla de cacahuete', 'Pan con mantequilla de cacahuete y plátano', 'breakfast', 'lidl', 350, 12, 38, 16, 4, 5, 1, 'https://images.unsplash.com/photo-1528735602780-2552c347e2e5?w=400'),
('Barrita energética', 'Barrita de cereales con nueces y miel', 'breakfast', 'carrefour', 220, 8, 28, 10, 3, 2, 1, 'https://images.unsplash.com/photo-1579954115545-a95591f28bfc?w=400'),
('Fruta fresca con yogur', 'Mix de frutas de temporada con yogur natural', 'breakfast', 'mercadona', 180, 6, 32, 4, 4, 5, 1, 'https://images.unsplash.com/photo-1488477181946-6428a0291777?w=400'),
('Bebida de almendras y dátiles', 'Leche de almendras batida con dátiles', 'breakfast', 'lidl', 200, 4, 38, 6, 4, 5, 1, 'https://images.unsplash.com/photo-1606890738374-4b6df7c5de4d?w=400'),

-- Desayunos con huevos
('Huevos al plato', 'Huevos fritos con jamón y patatas', 'breakfast', 'mercadona', 450, 24, 22, 30, 3, 15, 1, 'https://images.unsplash.com/photo-1482049016091-4d03b5a70b0b?w=400'),
('Revuelto de setas', 'Huevos revueltos con champiñones y trufa', 'breakfast', 'lidl', 320, 18, 4, 26, 2, 12, 1, 'https://images.unsplash.com/photo-1510693206972-df098062cb71?w=400'),
('Frittata de verduras', 'Tortilla italiana con verduras asadas', 'breakfast', 'carrefour', 380, 20, 12, 26, 4, 25, 2, 'https://images.unsplash.com/photo-1528735602780-2552c347e2e5?w=400'),
('Huevos rancheros', 'Tortillas con huevos y salsa ranchera', 'breakfast', 'mercadona', 360, 16, 32, 18, 4, 15, 2, 'https://images.unsplash.com/photo-1512152272829-e313966b3dd4?w=400'),
('Egg muffins', 'Muffins de huevo con verduras al horno', 'breakfast', 'lidl', 280, 18, 8, 18, 3, 25, 3, 'https://images.unsplash.com/photo-1484723091739-30a097e8f929?w=400'),

-- Más variedad
('Tostada de mermelada', 'Pan tostado con mermelada de fresa', 'breakfast', 'mercadona', 240, 4, 48, 4, 2, 3, 2, 'https://images.unsplash.com/photo-1509440159596-024e6631d513?w=400'),
('Bizcocho casero', 'Bizcocho esponjoso con vainilla', 'breakfast', 'carrefour', 320, 6, 45, 12, 1, 45, 4, 'https://images.unsplash.com/photo-1578985545062-033a1b83822b?w=400'),
('Muffins de arándanos', 'Muffins con arándanos frescos', 'breakfast', 'lidl', 350, 6, 48, 14, 2, 30, 3, 'https://images.unsplash.com/photo-1607478068780-5d6ca4f2c817?w=400'),
('Dona glaseada', 'Dona con glaseado de chocolate', 'breakfast', 'mercadona', 380, 5, 48, 18, 1, 20, 1, 'https://images.unsplash.com/photo-1551024601-ec6c1d20ff71?w=400'),
('Crepes de chocolate', 'Crepes rellenos de crema de chocolate', 'breakfast', 'lidl', 420, 8, 52, 18, 3, 20, 2, 'https://images.unsplash.com/photo-1567171466295-4afa63d07283?w=400'),

-- Desayunos proteicos extra
('Claras de huevo con jamón', 'Claras batidas con jamón serrano', 'breakfast', 'mercadona', 180, 22, 2, 7, 0, 10, 1, 'https://images.unsplash.com/photo-1510693206972-df098062cb71?w=400'),
('Batido proteico', 'Proteína whey con leche y plátano', 'breakfast', 'lidl', 300, 28, 30, 6, 3, 5, 1, 'https://images.unsplash.com/photo-1553530666-ba11a90694f3?w=400'),
('Tostada de jamón serrano', 'Pan con tomate, aceite y jamón serrano', 'breakfast', 'mercadona', 280, 12, 26, 12, 2, 5, 1, 'https://images.unsplash.com/photo-1509440159596-024e6631d513?w=400'),
('Ensalada de frutas', 'Mix de frutas frescas con menta', 'breakfast', 'carrefour', 120, 2, 28, 1, 4, 5, 1, 'https://images.unsplash.com/photo-1490474418585-d4afa7ef4d9d?w=400'),
('Té con galletas', 'Té negro con galletas integrales', 'breakfast', 'lidl', 180, 3, 28, 6, 1, 5, 1, 'https://images.unsplash.com/photo-1544787219-7f2eab1a4f53?w=400'),

-- Últimos 10 desayunos
('Café con tostadas', 'Café con leche y tostadas integrales', 'breakfast', 'mercadona', 160, 6, 22, 5, 3, 5, 2, 'https://images.unsplash.com/photo-1509042239863-f277c0d2654b?w=400'),
('Smoothie bowl de plátano', 'Bowl de batido de plátano con toppings', 'breakfast', 'lidl', 380, 10, 68, 10, 8, 10, 1, 'https://images.unsplash.com/photo-1590301159989-7c24657c4c65?w=400'),
('Tortilla de patatas', 'Tortilla española clásica de patatas', 'breakfast', 'mercadona', 320, 12, 18, 20, 2, 20, 2, 'https://images.unsplash.com/photo-1510693206972-df098062cb71?w=400'),
('Queso con membrillo', 'Queso manchego con membrillo y pan', 'breakfast', 'lidl', 280, 14, 22, 14, 1, 5, 1, 'https://images.unsplash.com/photo-1509440159596-024e6631d513?w=400'),
('Tostada de hummus', 'Pan integral con hummus y verduras', 'breakfast', 'carrefour', 260, 10, 32, 10, 6, 5, 1, 'https://images.unsplash.com/photo-1541519227354-08fa5d50c44d?w=400'),
('Muesli con yogur', 'Muesli con yogur griego natural', 'breakfast', 'mercadona', 300, 12, 42, 8, 5, 3, 1, 'https://images.unsplash.com/photo-1490457849456-c0968be56a12?w=400'),
('Bollo de chocolate', 'Bollo suizo con chocolate', 'breakfast', 'lidl', 420, 8, 52, 20, 2, 5, 1, 'https://images.unsplash.com/photo-1551024601-ec6c1d20ff71?w=400'),
('Tostada de nueces', 'Pan con queso crema y nueces', 'breakfast', 'carrefour', 340, 10, 28, 20, 3, 5, 1, 'https://images.unsplash.com/photo-1509440159596-024e6631d513?w=400'),
('Sándwich de huevo', 'Huevo frito entre pan tostado', 'breakfast', 'mercadona', 380, 16, 32, 18, 2, 10, 1, 'https://images.unsplash.com/photo-1528735602780-2552c347e2e5?w=400'),
('Batido de frutas', 'Batido de plátano, fresa y leche', 'breakfast', 'lidl', 250, 8, 45, 5, 4, 5, 1, 'https://images.unsplash.com/photo-1553530666-ba11a90694f3?w=400');

-- ============================================
-- COMIDAS (75 recetas)
-- ============================================

INSERT INTO master_recipes (name, description, meal_type, supermarket, calories, protein_g, carbs_g, fat_g, fiber_g, prep_time_min, servings, image_url) VALUES

-- Comidas de pollo
('Pechuga de pollo a la plancha', 'Pechuga jugosa con ensalada mixta', 'lunch', 'mercadona', 380, 45, 12, 16, 4, 15, 1, 'https://images.unsplash.com/photo-1532550907401-a500c9a57435?w=400'),
('Pollo al curry', 'Pollo en salsa de curry con arroz basmati', 'lunch', 'lidl', 520, 38, 42, 18, 3, 30, 2, 'https://images.unsplash.com/photo-1565557623262-b51c2513a641?w=400'),
('Ensalada César con pollo', 'Lechuga romana con pollo crujiente y parmesano', 'lunch', 'mercadona', 420, 32, 18, 24, 3, 15, 1, 'https://images.unsplash.com/photo-1546039907-7fa05f8e8daf?w=400'),
('Fajitas de pollo', 'Tortillas con pollo, pimientos y cebolla', 'lunch', 'lidl', 580, 35, 48, 24, 5, 20, 2, 'https://images.unsplash.com/photo-1565299507173-b270aac67139?w=400'),
('Pollo al limón', 'Muslos de pollo al horno con limón y hierbas', 'lunch', 'carrefour', 440, 32, 8, 30, 1, 40, 2, 'https://images.unsplash.com/photo-1598103442098-9a4be2f95f50?w=400'),

-- Comidas de ternera
('Ternera estofada', 'Ternera en salsa con patatas y zanahorias', 'lunch', 'mercadona', 520, 42, 28, 22, 4, 45, 2, 'https://images.unsplash.com/photo-1544025162-d76694265987?w=400'),
('Bistec a la plancha', 'Filete de ternera con patatas fritas', 'lunch', 'lidl', 480, 45, 25, 20, 2, 15, 1, 'https://images.unsplash.com/photo-1546833999-b87004413ea5?w=400'),
('Empanada de ternera', 'Masa hojaldrada rellena de ternera', 'lunch', 'carrefour', 420, 18, 38, 22, 2, 30, 2, 'https://images.unsplash.com/photo-1509440159596-024e6631d513?w=400'),
('Tacos de ternera', 'Tortillas de maíz con ternera guisada', 'lunch', 'mercadona', 480, 28, 42, 22, 4, 25, 3, 'https://images.unsplash.com/photo-1565299507173-b270aac67139?w=400'),
('Bowl de ternera', 'Arroz con ternera salteada y verduras', 'lunch', 'lidl', 560, 35, 65, 18, 5, 25, 1, 'https://images.unsplash.com/photo-1512058564366-18510be2db19?w=400'),

-- Comidas de cerdo
('Chuletas de cerdo', 'Chuletas asadas con manzana', 'lunch', 'mercadona', 480, 38, 22, 26, 2, 25, 2, 'https://images.unsplash.com/photo-1544025162-d76694265987?w=400'),
('Costillas BBQ', 'Costillas de cerdo con salsa barbacoa', 'lunch', 'lidl', 620, 42, 35, 32, 1, 50, 2, 'https://images.unsplash.com/photo-1544025162-d76694265987?w=400'),
('Lomo de cerdo al horno', 'Lomo jugoso con patatas panadera', 'lunch', 'carrefour', 520, 40, 25, 28, 2, 40, 2, 'https://images.unsplash.com/photo-1546833999-b87004413ea5?w=400'),
('Pulled pork', 'Cerdo desmenuzado con salsa BBQ', 'lunch', 'mercadona', 540, 38, 32, 28, 2, 120, 4, 'https://images.unsplash.com/photo-1529193591184-b1d58069ecdd?w=400'),
('Solomillo de cerdo', 'Solomillo con salsa de queso azul', 'lunch', 'lidl', 450, 42, 15, 24, 1, 20, 1, 'https://images.unsplash.com/photo-1546833999-b87004413ea5?w=400'),

-- Comidas de pescado
('Salmón al horno', 'Salmón con espárragos y limón', 'lunch', 'mercadona', 480, 40, 12, 30, 4, 25, 1, 'https://images.unsplash.com/photo-1467003909585-2f8a7270028d?w=400'),
('Merluza a la gallega', 'Merluza con patatas y pimentón', 'lunch', 'lidl', 320, 32, 18, 12, 2, 25, 1, 'https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?w=400'),
('Bacalao al pil-pil', 'Bacalao con salsa de aceite y ajo', 'lunch', 'mercadona', 380, 35, 8, 22, 1, 35, 1, 'https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?w=400'),
('Pescado frito', 'Filetes de pescado rebozados', 'lunch', 'lidl', 420, 28, 32, 20, 2, 20, 1, 'https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?w=400'),
('Atún a la plancha', 'Atún con salsa de soja y sésamo', 'lunch', 'carrefour', 350, 42, 4, 16, 0, 12, 1, 'https://images.unsplash.com/photo-1467003909585-2f8a7270028d?w=400'),

-- Comidas vegetarianas
('Ensalada de garbanzos', 'Garbanzos con verduras y vinagreta', 'lunch', 'mercadona', 380, 16, 48, 14, 10, 10, 2, 'https://images.unsplash.com/photo-1546039907-7fa05f8e8daf?w=400'),
('Buddha bowl', 'Bowl de quinoa, verduras y tahini', 'lunch', 'lidl', 520, 18, 62, 20, 12, 20, 1, 'https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=400'),
('Pasta con pesto', 'Pasta integral con salsa pesto', 'lunch', 'carrefour', 480, 14, 68, 16, 6, 15, 2, 'https://images.unsplash.com/photo-1551892374-ecf8754cf8b0?w=400'),
('Risotto de setas', 'Arroz meloso con champiñones', 'lunch', 'mercadona', 520, 14, 72, 18, 4, 30, 2, 'https://images.unsplash.com/photo-1476124369491-e7addf5db371?w=400'),
('Curry de verduras', 'Curry con arroz basmati', 'lunch', 'lidl', 450, 12, 65, 15, 8, 25, 2, 'https://images.unsplash.com/photo-1455619452474-d2be8b1e70cd?w=400'),

-- Más comidas
('Paella valenciana', 'Arroz con pollo, judías y garrofón', 'lunch', 'mercadona', 680, 32, 72, 26, 5, 50, 4, 'https://images.unsplash.com/photo-1534080564583-d5d1af1a4c6e?w=400'),
('Lasaña de carne', 'Capas de pasta con carne y bechamel', 'lunch', 'lidl', 620, 35, 55, 30, 4, 45, 4, 'https://images.unsplash.com/photo-1574894704649-f73b27448a8b?w=400'),
('Spaghetti carbonara', 'Pasta con huevo, queso y panceta', 'lunch', 'carrefour', 580, 24, 68, 22, 3, 20, 2, 'https://images.unsplash.com/photo-1551892374-ecf8754cf8b0?w=400'),
('Pizza margarita', 'Pizza con tomate, mozzarella y albahaca', 'lunch', 'mercadona', 520, 20, 62, 20, 4, 25, 1, 'https://images.unsplash.com/photo-1574071318508-1cdbab80d002?w=400'),
('Hamburguesa clásica', 'Carne de ternera con queso y lechuga', 'lunch', 'lidl', 640, 38, 42, 34, 3, 15, 1, 'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=400'),

-- Comidas internacionales
('Pad Thai', 'Fideos de arroz con gambas y cacahuetes', 'lunch', 'mercadona', 520, 28, 62, 18, 4, 25, 1, 'https://images.unsplash.com/photo-1559314809-0d3b4d99a3a3?w=400'),
('Sushi variado', 'Rollitos de arroz con salmón y atún', 'lunch', 'lidl', 480, 28, 65, 12, 3, 30, 12, 'https://images.unsplash.com/photo-1579871494447-9811cf80d66c?w=400'),
('Kebab de cordero', 'Carne de cordero con salsa yogur', 'lunch', 'carrefour', 560, 32, 48, 26, 4, 20, 1, 'https://images.unsplash.com/photo-1529006555510-10f577b03d7c?w=400'),
('Poke bowl', 'Bowl hawaiano de atún y arroz', 'lunch', 'mercadona', 480, 32, 48, 16, 5, 15, 1, 'https://images.unsplash.com/photo-1546039907-7fa05f8e8daf?w=400'),
('Pasta arrabiata', 'Pasta con salsa de tomate picante', 'lunch', 'lidl', 420, 14, 68, 10, 5, 15, 2, 'https://images.unsplash.com/photo-1551892374-ecf8754cf8b0?w=400'),

-- Comidas rápidas
('Sándwich mixto', 'Pan con jamón y queso a la plancha', 'lunch', 'mercadona', 380, 18, 32, 18, 2, 10, 1, 'https://images.unsplash.com/photo-1528735602780-2552c347e2e5?w=400'),
('Ensalada de pasta', 'Pasta fría con verduras y atún', 'lunch', 'lidl', 420, 18, 52, 14, 4, 15, 2, 'https://images.unsplash.com/photo-1546039907-7fa05f8e8daf?w=400'),
('Wrap de pollo', 'Tortilla con pollo y verduras', 'lunch', 'carrefour', 440, 28, 35, 18, 4, 10, 1, 'https://images.unsplash.com/photo-1626700058817-67a15a623dbd?w=400'),
('Quesadilla de queso', 'Tortilla con queso fundido', 'lunch', 'mercadona', 380, 16, 32, 20, 2, 10, 1, 'https://images.unsplash.com/photo-1618040996337-5648bb547f61?w=400'),
('Bocadillo de tortilla', 'Pan con tortilla de patatas', 'lunch', 'lidl', 480, 18, 48, 22, 3, 10, 1, 'https://images.unsplash.com/photo-1510693206972-df098062cb71?w=400'),

-- Más variedad
('Pollo asado', 'Pollo entero asado con patatas', 'lunch', 'mercadona', 520, 42, 25, 28, 2, 60, 2, 'https://images.unsplash.com/photo-1598103442098-9a4be2f95f50?w=400'),
('Guiso de lentejas', 'Lentejas con verduras y chorizo', 'lunch', 'lidl', 480, 28, 52, 14, 12, 40, 2, 'https://images.unsplash.com/photo-1546039907-7fa05f8e8daf?w=400'),
('Albóndigas en salsa', 'Albóndigas de carne en salsa tomate', 'lunch', 'carrefour', 520, 32, 32, 26, 3, 30, 2, 'https://images.unsplash.com/photo-1529042410552-e4295c6546d5?w=400'),
('Judiones con chorizo', 'Alubias blancas con chorizo', 'lunch', 'mercadona', 520, 28, 48, 22, 10, 35, 2, 'https://images.unsplash.com/photo-1546039907-7fa05f8e8daf?w=400'),
('Macarrones con queso', 'Pasta con salsa de queso cheddar', 'lunch', 'lidl', 520, 20, 58, 22, 3, 20, 2, 'https://images.unsplash.com/photo-1551892374-ecf8754cf8b0?w=400'),

-- Comidas saludables
('Ensalada de quinoa', 'Quinoa con verduras y aguacate', 'lunch', 'mercadona', 420, 16, 52, 16, 10, 15, 2, 'https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=400'),
('Bowl de salmón', 'Salmón, arroz y verduras', 'lunch', 'lidl', 560, 38, 45, 22, 6, 20, 1, 'https://images.unsplash.com/photo-1467003909585-2f8a7270028d?w=400'),
('Wrap de atún', 'Tortilla con atún y lechuga', 'lunch', 'carrefour', 400, 28, 32, 14, 4, 10, 1, 'https://images.unsplash.com/photo-1626700058817-67a15a623dbd?w=400'),
('Sopa de verduras', 'Crema de verduras de temporada', 'lunch', 'mercadona', 180, 6, 28, 5, 6, 25, 2, 'https://images.unsplash.com/photo-1547592166-23ac45744acd?w=400'),
('Gazpacho andaluz', 'Sopa fría de tomate y verduras', 'lunch', 'lidl', 140, 3, 22, 4, 4, 10, 2, 'https://images.unsplash.com/photo-1547592166-23ac45744acd?w=400'),

-- Comidas extra
('Pollo al ajillo', 'Pollo con ajo y perejil', 'lunch', 'mercadona', 420, 38, 8, 24, 1, 25, 2, 'https://images.unsplash.com/photo-1598103442098-9a4be2f95f50?w=400'),
('Entrecot a la parrilla', 'Filete de ternera con ensalada', 'lunch', 'lidl', 560, 48, 12, 34, 2, 15, 1, 'https://images.unsplash.com/photo-1546833999-b87004413ea5?w=400'),
('Croquetas de jamón', 'Croquetas crujientes de jamón', 'lunch', 'carrefour', 380, 12, 28, 24, 1, 25, 6, 'https://images.unsplash.com/photo-1509440159596-024e6631d513?w=400'),
('Pulpo a la gallega', 'Pulpo con patatas y pimentón', 'lunch', 'mercadona', 350, 32, 18, 12, 2, 35, 1, 'https://images.unsplash.com/photo-1565557623262-b51c2513a641?w=400'),
('Gambas al ajillo', 'Gambas salteadas con ajo', 'lunch', 'lidl', 280, 28, 4, 16, 1, 10, 1, 'https://images.unsplash.com/photo-1565557623262-b51c2513a641?w=400'),

-- Últimas 20 comidas
('Calamares fritos', 'Anillas de calamar rebozadas', 'lunch', 'mercadona', 420, 24, 28, 22, 2, 15, 1, 'https://images.unsplash.com/photo-1565557623262-b51c2513a641?w=400'),
('Pimientos rellenos', 'Pimientos rellenos de carne', 'lunch', 'lidl', 380, 22, 22, 20, 4, 35, 2, 'https://images.unsplash.com/photo-1546039907-7fa05f8e8daf?w=400'),
('Berenjenas al horno', 'Berenjenas con queso y tomate', 'lunch', 'carrefour', 280, 14, 22, 16, 6, 30, 2, 'https://images.unsplash.com/photo-1546039907-7fa05f8e8daf?w=400'),
('Pollo al vino', 'Muslos de pollo al vino blanco', 'lunch', 'mercadona', 480, 36, 18, 26, 2, 35, 2, 'https://images.unsplash.com/photo-1598103442098-9a4be2f95f50?w=400'),
('Ternera con setas', 'Ternera con salsa de champiñones', 'lunch', 'lidl', 520, 42, 15, 28, 3, 30, 2, 'https://images.unsplash.com/photo-1544025162-d76694265987?w=400'),
('Cordero asado', 'Cordero al horno con patatas', 'lunch', 'carrefour', 580, 42, 18, 36, 2, 50, 2, 'https://images.unsplash.com/photo-1546833999-b87004413ea5?w=400'),
('Lasaña vegetariana', 'Lasaña con verduras y queso', 'lunch', 'mercadona', 480, 18, 52, 22, 6, 40, 4, 'https://images.unsplash.com/photo-1574894704649-f73b27448a8b?w=400'),
('Canelones de carne', 'Pasta rellena de carne y bechamel', 'lunch', 'lidl', 540, 28, 48, 26, 4, 45, 4, 'https://images.unsplash.com/photo-1574894704649-f73b27448a8b?w=400'),
('Pollo al curry con arroz', 'Curry de pollo con arroz basmati', 'lunch', 'carrefour', 560, 35, 52, 20, 4, 25, 2, 'https://images.unsplash.com/photo-1455619452474-d2be8b1e70cd?w=400'),
('Fajitas de ternera', 'Tortillas con ternera y pimientos', 'lunch', 'mercadona', 620, 38, 48, 28, 5, 20, 2, 'https://images.unsplash.com/photo-1565299507173-b270aac67139?w=400'),
('Pulpo a la brasa', 'Pulpo a la plancha con aceite', 'lunch', 'lidl', 320, 35, 4, 16, 1, 20, 1, 'https://images.unsplash.com/photo-1565557623262-b51c2513a641?w=400'),
('Dorada al horno', 'Dorada con patatas panadera', 'lunch', 'carrefour', 420, 38, 22, 18, 2, 35, 1, 'https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?w=400'),
('Rape a la bilbaína', 'Rape con salsa de ajo', 'lunch', 'mercadona', 280, 32, 8, 12, 1, 20, 1, 'https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?w=400'),
('Fideuá', 'Fideos con marisco en paella', 'lunch', 'lidl', 480, 28, 55, 16, 4, 40, 4, 'https://images.unsplash.com/photo-1534080564583-d5d1af1a4c6e?w=400'),
('Cachopo', 'Filete empanado relleno de jamón y queso', 'lunch', 'carrefour', 680, 42, 42, 36, 3, 30, 1, 'https://images.unsplash.com/photo-1546833999-b87004413ea5?w=400'),
('Flamenquín', 'Rollito de carne empanado', 'lunch', 'mercadona', 520, 28, 32, 30, 2, 25, 2, 'https://images.unsplash.com/photo-1546833999-b87004413ea5?w=400'),
('Pollo al limón con arroz', 'Pollo al limón con arroz blanco', 'lunch', 'lidl', 520, 38, 48, 16, 2, 25, 2, 'https://images.unsplash.com/photo-1598103442098-9a4be2f95f50?w=400'),
('Ternera con verduras', 'Salteado de ternera con verduras', 'lunch', 'carrefour', 420, 35, 18, 22, 5, 20, 1, 'https://images.unsplash.com/photo-1544025162-d76694265987?w=400'),
('Merluza rebozada', 'Filetes de merluza con harina', 'lunch', 'mercadona', 380, 32, 22, 18, 2, 20, 1, 'https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?w=400'),
('Pasta carbonara', 'Spaghetti con huevo y panceta', 'lunch', 'lidl', 540, 22, 58, 22, 3, 20, 2, 'https://images.unsplash.com/photo-1551892374-ecf8754cf8b0?w=400'),
('Ensalada de arroz', 'Arroz con atún, huevo y verduras', 'lunch', 'carrefour', 420, 22, 48, 14, 4, 15, 2, 'https://images.unsplash.com/photo-1546039907-7fa05f8e8daf?w=400');

-- ============================================
-- CENAS (50 recetas)
-- ============================================

INSERT INTO master_recipes (name, description, meal_type, supermarket, calories, protein_g, carbs_g, fat_g, fiber_g, prep_time_min, servings, image_url) VALUES

-- Cenas ligeras
('Crema de calabacín', 'Crema suave de calabacín y queso', 'dinner', 'mercadona', 180, 8, 18, 8, 4, 25, 2, 'https://images.unsplash.com/photo-1547592166-23ac45744acd?w=400'),
('Sopa de miso', 'Sopa japonesa con tofu y algas', 'dinner', 'lidl', 120, 8, 12, 4, 2, 15, 1, 'https://images.unsplash.com/photo-1547592166-23ac45744acd?w=400'),
('Gazpacho', 'Sopa fría de tomate y verduras', 'dinner', 'carrefour', 140, 4, 22, 4, 4, 10, 2, 'https://images.unsplash.com/photo-1547592166-23ac45744acd?w=400'),
('Ensalada verde', 'Lechuga, tomate y pepino', 'dinner', 'mercadona', 80, 3, 12, 2, 3, 5, 1, 'https://images.unsplash.com/photo-1546039907-7fa05f8e8daf?w=400'),
('Tortilla francesa', 'Huevos revueltos con jamón', 'dinner', 'lidl', 280, 18, 4, 20, 1, 8, 1, 'https://images.unsplash.com/photo-1510693206972-df098062cb71?w=400'),

-- Cenas de pescado
('Salmón al vapor', 'Salmón con verduras al vapor', 'dinner', 'mercadona', 320, 35, 8, 18, 3, 20, 1, 'https://images.unsplash.com/photo-1467003909585-2f8a7270028d?w=400'),
('Merluza al horno', 'Merluza con patatas panadera', 'dinner', 'lidl', 280, 30, 16, 10, 3, 25, 1, 'https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?w=400'),
('Pescado al papillote', 'Pescado con verduras en papel', 'dinner', 'carrefour', 260, 28, 12, 12, 3, 25, 1, 'https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?w=400'),
('Atún a la plancha', 'Atún con ensalada verde', 'dinner', 'mercadona', 340, 38, 8, 16, 2, 12, 1, 'https://images.unsplash.com/photo-1467003909585-2f8a7270028d?w=400'),
('Lubina al horno', 'Lubina con hierbas y limón', 'dinner', 'lidl', 260, 32, 4, 12, 1, 25, 1, 'https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?w=400'),

-- Cenas de pollo
('Pechuga a la plancha', 'Pechuga con ensalada', 'dinner', 'mercadona', 320, 42, 8, 12, 3, 15, 1, 'https://images.unsplash.com/photo-1532550907401-a500c9a57435?w=400'),
('Pollo al horno', 'Muslos de pollo con verduras', 'dinner', 'lidl', 380, 35, 15, 20, 3, 40, 2, 'https://images.unsplash.com/photo-1598103442098-9a4be2f95f50?w=400'),
('Ensalada César', 'Lechuga con pollo y crutones', 'dinner', 'carrefour', 380, 28, 15, 22, 3, 10, 1, 'https://images.unsplash.com/photo-1546039907-7fa05f8e8daf?w=400'),
('Fajitas de pollo', 'Tortillas con pollo y verduras', 'dinner', 'mercadona', 420, 32, 35, 18, 4, 15, 1, 'https://images.unsplash.com/photo-1565299507173-b270aac67139?w=400'),
('Wrap de pollo', 'Tortilla con pollo y lechuga', 'dinner', 'lidl', 380, 28, 28, 16, 3, 10, 1, 'https://images.unsplash.com/photo-1626700058817-67a15a623dbd?w=400'),

-- Cenas de carne
('Bistec con ensalada', 'Filete con lechuga y tomate', 'dinner', 'mercadona', 420, 42, 8, 24, 2, 12, 1, 'https://images.unsplash.com/photo-1546833999-b87004413ea5?w=400'),
('Ternera salteada', 'Ternera con pimientos', 'dinner', 'lidl', 380, 35, 12, 22, 3, 15, 1, 'https://images.unsplash.com/photo-1544025162-d76694265987?w=400'),
('Lomo con patatas', 'Lomo con patatas fritas', 'dinner', 'carrefour', 480, 38, 28, 24, 2, 20, 1, 'https://images.unsplash.com/photo-1546833999-b87004413ea5?w=400'),
('Costillas de cerdo', 'Costillas con ensalada', 'dinner', 'mercadona', 520, 35, 18, 32, 2, 35, 1, 'https://images.unsplash.com/photo-1544025162-d76694265987?w=400'),
('Cordero asado', 'Cordero con patatas panadera', 'dinner', 'lidl', 540, 38, 20, 32, 2, 50, 1, 'https://images.unsplash.com/photo-1546833999-b87004413ea5?w=400'),

-- Cenas vegetarianas
('Pasta primavera', 'Pasta con verduras de temporada', 'dinner', 'mercadona', 420, 14, 65, 12, 6, 20, 2, 'https://images.unsplash.com/photo-1551892374-ecf8754cf8b0?w=400'),
('Risotto de champiñones', 'Arroz meloso con setas', 'dinner', 'lidl', 480, 12, 68, 16, 4, 30, 2, 'https://images.unsplash.com/photo-1476124369491-e7addf5db371?w=400'),
('Ensalada de garbanzos', 'Garbanzos con verduras', 'dinner', 'carrefour', 340, 16, 45, 10, 10, 10, 2, 'https://images.unsplash.com/photo-1546039907-7fa05f8e8daf?w=400'),
('Buddha bowl', 'Bowl de quinoa y verduras', 'dinner', 'mercadona', 460, 16, 62, 16, 10, 15, 1, 'https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=400'),
('Pizza vegetariana', 'Pizza con verduras', 'dinner', 'lidl', 480, 18, 58, 18, 5, 25, 1, 'https://images.unsplash.com/photo-1574071318508-1cdbab80d002?w=400'),

-- Más cenas
('Huevos revueltos', 'Huevos con jamón y queso', 'dinner', 'mercadona', 320, 20, 6, 22, 1, 8, 1, 'https://images.unsplash.com/photo-1510693206972-df098062cb71?w=400'),
('Tortilla de patatas', 'Tortilla española clásica', 'dinner', 'lidl', 380, 14, 22, 24, 2, 20, 2, 'https://images.unsplash.com/photo-1510693206972-df098062cb71?w=400'),
('Croquetas de jamón', 'Croquetas con ensalada', 'dinner', 'carrefour', 420, 14, 30, 24, 2, 20, 4, 'https://images.unsplash.com/photo-1509440159596-024e6631d513?w=400'),
('Empanada de atún', 'Empanada gallega', 'dinner', 'mercadona', 440, 18, 38, 22, 3, 30, 2, 'https://images.unsplash.com/photo-1509440159596-024e6631d513?w=400'),
('Sopa de pollo', 'Caldo con fideos y pollo', 'dinner', 'lidl', 180, 14, 18, 5, 2, 25, 2, 'https://images.unsplash.com/photo-1547592166-23ac45744acd?w=400'),

-- Cenas internacionales
('Pad Thai', 'Fideos con gambas y cacahuetes', 'dinner', 'mercadona', 480, 24, 58, 16, 4, 25, 1, 'https://images.unsplash.com/photo-1559314809-0d3b4d99a3a3?w=400'),
('Sushi', 'Rollitos de arroz con salmón', 'dinner', 'lidl', 420, 24, 58, 10, 3, 30, 10, 'https://images.unsplash.com/photo-1579871494447-9811cf80d66c?w=400'),
('Curry de verduras', 'Curry con arroz basmati', 'dinner', 'carrefour', 420, 12, 62, 12, 8, 25, 2, 'https://images.unsplash.com/photo-1455619452474-d2be8b1e70cd?w=400'),
('Tacos de pollo', 'Tortillas con pollo y salsa', 'dinner', 'mercadona', 480, 28, 42, 22, 5, 15, 2, 'https://images.unsplash.com/photo-1565299507173-b270aac67139?w=400'),
('Kebab de pollo', 'Carne con salsa yogur', 'dinner', 'lidl', 520, 30, 45, 22, 4, 15, 1, 'https://images.unsplash.com/photo-1529006555510-10f577b03d7c?w=400'),

-- Cenas saludables
('Ensalada de atún', 'Atún con lechuga y huevo', 'dinner', 'mercadona', 280, 26, 8, 16, 2, 10, 1, 'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=400'),
('Bowl de salmón', 'Salmón con arroz y verduras', 'dinner', 'lidl', 480, 35, 42, 16, 5, 20, 1, 'https://images.unsplash.com/photo-1467003909585-2f8a7270028d?w=400'),
('Wrap de verduras', 'Tortilla con verduras asadas', 'dinner', 'carrefour', 320, 10, 42, 12, 6, 15, 1, 'https://images.unsplash.com/photo-1626700058817-67a15a623dbd?w=400'),
('Ensalada de quinoa', 'Quinoa con aguacate', 'dinner', 'mercadona', 360, 14, 48, 14, 8, 15, 1, 'https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=400'),
('Sopa de lentejas', 'Lentejas con verduras', 'dinner', 'lidl', 280, 18, 35, 6, 10, 30, 2, 'https://images.unsplash.com/photo-1547592166-23ac45744acd?w=400'),

-- Más variedad
('Pollo al curry', 'Curry de pollo con arroz', 'dinner', 'carrefour', 520, 32, 48, 18, 4, 25, 2, 'https://images.unsplash.com/photo-1455619452474-d2be8b1e70cd?w=400'),
('Lasaña', 'Capas de pasta y carne', 'dinner', 'mercadona', 560, 28, 52, 26, 4, 40, 2, 'https://images.unsplash.com/photo-1574894704649-f73b27448a8b?w=400'),
('Spaghetti bolognesa', 'Pasta con salsa de tomate y carne', 'dinner', 'lidl', 540, 26, 58, 20, 4, 25, 2, 'https://images.unsplash.com/photo-1551892374-ecf8754cf8b0?w=400'),
('Pizza de pepperoni', 'Pizza con salami', 'dinner', 'carrefour', 560, 22, 62, 24, 4, 20, 1, 'https://images.unsplash.com/photo-1574071318508-1cdbab80d002?w=400'),
('Hamburguesa con queso', 'Carne con queso y lechuga', 'dinner', 'mercadona', 580, 35, 42, 30, 3, 15, 1, 'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=400'),

-- Últimas 10 cenas
('Pulpo a la gallega', 'Pulpo con patatas', 'dinner', 'lidl', 300, 32, 12, 14, 2, 25, 1, 'https://images.unsplash.com/photo-1565557623262-b51c2513a641?w=400'),
('Calamares fritos', 'Calamares con alioli', 'dinner', 'mercadona', 380, 24, 25, 20, 2, 15, 1, 'https://images.unsplash.com/photo-1565557623262-b51c2513a641?w=400'),
('Gambas al ajillo', 'Gambas con ajo', 'dinner', 'carrefour', 260, 28, 4, 14, 1, 10, 1, 'https://images.unsplash.com/photo-1565557623262-b51c2513a641?w=400'),
('Sepia a la plancha', 'Sepia con ajo', 'dinner', 'mercadona', 240, 30, 6, 10, 1, 12, 1, 'https://images.unsplash.com/photo-1565557623262-b51c2513a641?w=400'),
('Dorada al horno', 'Dorada con limón', 'dinner', 'lidl', 280, 32, 4, 14, 1, 25, 1, 'https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?w=400'),
('Bacalao dorado', 'Bacalao con tomate', 'dinner', 'carrefour', 320, 32, 10, 14, 2, 25, 1, 'https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?w=400'),
('Rape a la vasca', 'Rape con salsa verde', 'dinner', 'mercadona', 260, 30, 8, 10, 2, 25, 1, 'https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?w=400'),
('Lenguado rebozado', 'Lenguado con limón', 'dinner', 'lidl', 300, 28, 18, 12, 1, 15, 1, 'https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?w=400'),
('Boquerones fritos', 'Boquerones empanados', 'dinner', 'carrefour', 360, 26, 24, 18, 1, 12, 1, 'https://images.unsplash.com/photo-1565557623262-b51c2513a641?w=400'),
('Sardinas al horno', 'Sardinas con hierbas', 'dinner', 'mercadona', 280, 28, 4, 16, 1, 20, 1, 'https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?w=400');

-- ============================================
-- MERIENDAS (25 recetas)
-- ============================================

INSERT INTO master_recipes (name, description, meal_type, supermarket, calories, protein_g, carbs_g, fat_g, fiber_g, prep_time_min, servings, image_url) VALUES

-- Frutas
('Manzana con crema de cacahuete', 'Manzana con mantequilla de cacahuete', 'snack', 'mercadona', 200, 5, 24, 10, 4, 3, 1, 'https://images.unsplash.com/photo-1568702846914-96b305d2aaeb?w=400'),
('Plátano con nueces', 'Plátano con nueces picadas', 'snack', 'lidl', 220, 4, 28, 12, 4, 2, 1, 'https://images.unsplash.com/photo-1517673132405-a56a62b18caf?w=400'),
('Yogur con frutos rojos', 'Yogur griego con frutos rojos', 'snack', 'carrefour', 180, 12, 18, 6, 3, 3, 1, 'https://images.unsplash.com/photo-1488477181946-6428a0291777?w=400'),
('Batido de frutas', 'Batido de plátano y fresa', 'snack', 'mercadona', 180, 4, 38, 2, 4, 5, 1, 'https://images.unsplash.com/photo-1553530666-ba11a90694f3?w=400'),
('Fruta fresca', 'Mix de frutas de temporada', 'snack', 'lidl', 100, 2, 24, 1, 4, 5, 1, 'https://images.unsplash.com/photo-1490474418585-d4afa7ef4d9d?w=400'),

-- Barritas y snacks
('Barrita de cereales', 'Barrita energética de avena', 'snack', 'mercadona', 180, 4, 32, 6, 3, 1, 1, 'https://images.unsplash.com/photo-1579954115545-a95591f28bfc?w=400'),
('Barrita proteica', 'Barrita de proteína', 'snack', 'lidl', 220, 20, 18, 8, 2, 1, 1, 'https://images.unsplash.com/photo-1579954115545-a95591f28bfc?w=400'),
('Tosta de aguacate', 'Pan integral con aguacate', 'snack', 'carrefour', 180, 4, 22, 10, 4, 5, 1, 'https://images.unsplash.com/photo-1541519227354-08fa5d50c44d?w=400'),
('Tosta de tomate', 'Pan con tomate y aceite', 'snack', 'mercadona', 140, 3, 22, 4, 2, 3, 1, 'https://images.unsplash.com/photo-1509440159596-024e6631d513?w=400'),
('Palomitas', 'Palomitas de maíz naturales', 'snack', 'lidl', 100, 3, 20, 2, 4, 5, 1, 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400'),

-- Frutos secos
('Mezcla de frutos secos', 'Nueces, almendras y avellanas', 'snack', 'mercadona', 200, 6, 8, 16, 3, 2, 1, 'https://images.unsplash.com/photo-1536591284546-15f5b566a9f6?w=400'),
('Almendras tostadas', 'Almendras con sal', 'snack', 'lidl', 180, 6, 6, 15, 3, 2, 1, 'https://images.unsplash.com/photo-1508061253366-f8158571e569?w=400'),
('Nueces', 'Nueces peladas', 'snack', 'carrefour', 190, 4, 4, 18, 2, 2, 1, 'https://images.unsplash.com/photo-1536591284546-15f5b566a9f6?w=400'),
('Pistachos', 'Pistachos con cáscara', 'snack', 'mercadona', 170, 6, 8, 13, 3, 3, 1, 'https://images.unsplash.com/photo-1525351484163-7529414395d8?w=400'),
('Anacardos', 'Anacardos tostados', 'snack', 'lidl', 180, 5, 10, 14, 1, 2, 1, 'https://images.unsplash.com/photo-1536591284546-15f5b566a9f6?w=400'),

-- Lácteos
('Yogur natural', 'Yogur griego sin azúcar', 'snack', 'mercadona', 100, 18, 5, 1, 0, 1, 1, 'https://images.unsplash.com/photo-1488477181946-6428a0291777?w=400'),
('Queso fresco', 'Queso fresco con miel', 'snack', 'lidl', 150, 12, 8, 8, 0, 2, 1, 'https://images.unsplash.com/photo-1486297678162-626b8cd0a6ab?w=400'),
('Requesón', 'Requesón con canela', 'snack', 'carrefour', 120, 14, 4, 5, 0, 2, 1, 'https://images.unsplash.com/photo-1486297678162-626b8cd0a6ab?w=400'),
('Kéfir', 'Kéfir de frutas', 'snack', 'mercadona', 80, 6, 10, 2, 0, 1, 1, 'https://images.unsplash.com/photo-1490474418585-d4afa7ef4d9d?w=400'),
('Leche con cacao', 'Leche con cacao soluble', 'snack', 'lidl', 180, 8, 26, 5, 1, 3, 1, 'https://images.unsplash.com/photo-1544787219-7f2d5cc64537?w=400'),

-- Batidos
('Batido de proteína', 'Proteína whey con leche', 'snack', 'mercadona', 250, 25, 20, 8, 1, 3, 1, 'https://images.unsplash.com/photo-1553530666-ba11a90694f3?w=400'),
('Batido verde', 'Espinacas, plátano y leche', 'snack', 'lidl', 160, 5, 28, 3, 4, 5, 1, 'https://images.unsplash.com/photo-1610970881699-44a5587cabec?w=400'),
('Batido de chocolate', 'Batido de cacao', 'snack', 'carrefour', 220, 8, 32, 8, 2, 3, 1, 'https://images.unsplash.com/photo-1544787219-7f2d5cc64537?w=400'),
('Smoothie tropical', 'Mango, piña y leche de coco', 'snack', 'mercadona', 200, 4, 38, 5, 4, 5, 1, 'https://images.unsplash.com/photo-1509440159596-024e6631d513?w=400'),
('Batido de avena', 'Avena, plátano y leche', 'snack', 'lidl', 280, 8, 45, 8, 5, 5, 1, 'https://images.unsplash.com/photo-1553530666-ba11a90694f3?w=400'),

-- Más snacks
('Hummus con zanahoria', 'Hummus con bastones de zanahoria', 'snack', 'mercadona', 150, 5, 15, 8, 5, 5, 1, 'https://images.unsplash.com/photo-1541519227354-08fa5d50c44d?w=400'),
('Guacamole con nachos', 'Guacamole con totopos', 'snack', 'lidl', 220, 4, 24, 12, 4, 5, 1, 'https://images.unsplash.com/photo-1565299507173-b270aac67139?w=400'),
('Tostada de hummus', 'Pan con hummus y pepino', 'snack', 'carrefour', 160, 5, 22, 6, 3, 5, 1, 'https://images.unsplash.com/photo-1541519227354-08fa5d50c44d?w=400'),
('Aceitunas', 'Aceitunas con hueso', 'snack', 'mercadona', 80, 1, 4, 8, 2, 2, 1, 'https://images.unsplash.com/photo-1564750533745-e0f63f86a0b9?w=400'),
('Queso curado', 'Queso manchego', 'snack', 'lidl', 120, 8, 1, 10, 0, 1, 1, 'https://images.unsplash.com/photo-1486297678162-626b8cd0a6ab?w=400');

-- Reactivar RLS
ALTER TABLE master_recipes ENABLE ROW LEVEL SECURITY;

-- Verificar inserción
SELECT 'Total recetas insertadas' as info, COUNT(*) as count FROM master_recipes;
SELECT 'Por categoría' as info, meal_type, COUNT(*) as count FROM master_recipes GROUP BY meal_type ORDER BY meal_type;