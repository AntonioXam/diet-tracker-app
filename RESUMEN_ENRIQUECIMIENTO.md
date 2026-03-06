# RESUMEN - Enriquecimiento de Base de Datos de Recetas

## 1. ESTRUCTURA ACTUAL DE master_recipes

La tabla `master_recipes` ya contiene los campos:
- `id` (UUID)
- `name` (TEXT)
- `description` (TEXT)
- `meal_type` (breakfast, lunch, dinner, snack)
- `supermarket` (mercadona, lidl, carrefour, generic)
- `calories` (INTEGER)
- `protein_g` (DECIMAL)
- `carbs_g` (DECIMAL)
- `fat_g` (DECIMAL)
- `fiber_g` (DECIMAL)
- `ingredients` (JSONB) - **Ya existe pero probablemente vacío**
- `instructions` (TEXT) - **Ya existe pero probablemente vacío**
- `prep_time_min` (INTEGER)
- `servings` (INTEGER)
- `image_url` (TEXT)
- `rating` (DECIMAL)
- `created_at` (TIMESTAMPTZ)

## 2. SQL PARA AÑADIR COLUMNAS FALTANTES

```sql
-- ============================================
-- MIGRACIÓN: Añadir campos de enriquecimiento
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

-- 5. Crear índice para ingredients (búsquedas por ingrediente)
CREATE INDEX IF NOT EXISTS idx_master_recipes_ingredients ON master_recipes USING GIN(ingredients);
```

## 3. ESTRUCTURA JSON DE INGREDIENTES

### Formato recomendado para `ingredients` (JSONB):

```json
[
  {
    "name": "Huevos",
    "quantity": 2,
    "unit": "unidades",
    "optional": false
  },
  {
    "name": "Leche desnatada",
    "quantity": 100,
    "unit": "ml",
    "optional": false
  },
  {
    "name": "Sal",
    "quantity": 1,
    "unit": "pizca",
    "optional": true
  }
]
```

### Campos del ingrediente:
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `name` | string | Nombre del ingrediente |
| `quantity` | number | Cantidad numérica |
| `unit` | string | Unidad de medida (ml, g, unidades, cucharadas, etc.) |
| `optional` | boolean | Si es opcional (por defecto: false) |

### Formato para `instructions` (TEXT):

```
Paso 1: Batir los huevos en un bol.
Paso 2: Añadir la leche y mezclar bien.
Paso 3: Cocinar en sartén a fuego medio durante 3-4 minutos.
Paso 4: Servir caliente con sal y pimienta.
```

### Formato para `tags` (TEXT[]):

```sql
ARRAY['vegetariano', 'rapido', 'sin_gluten', 'proteico']
```

**Tags disponibles:**
- **Dietéticos:** `vegano`, `vegetariano`, `sin_gluten`, `bajo_carbohidratos`, `sin_lactosa`
- **Dificultad/Tiempo:** `rapido`, `facil`, `elaborado`, `prep_overnight`
- **Occasión:** `desayuno`, `almuerzo`, `cena`, `merienda`, `tapa`
- **Salud:** `saludable`, `proteico`, `fibra`, `omega3`, `detox`, `bajo_calorias`
- **Origen:** `español`, `italiano`, `mexicano`, `asiático`, `mediterraneo`
- **Cocina:** `horno`, `plancha`, `frio`, `potaje`, `crema`, `sopa`

## 4. EJEMPLOS DE RECETAS ENRIQUECIDAS

### Ejemplo 1: Desayuno
```json
{
  "id": "bfast-001",
  "name": "Tostadas de aguacate y huevo",
  "description": "Tostadas integrales con aguacate triturado y huevo pochado",
  "meal_type": "breakfast",
  "supermarket": "mercadona",
  "calories": 320,
  "protein_g": 18,
  "carbs_g": 28,
  "fat_g": 16,
  "fiber_g": 6,
  "ingredients": [
    {"name": "Pan integral", "quantity": 2, "unit": "rebanadas"},
    {"name": "Aguacate", "quantity": 1, "unit": "unidad"},
    {"name": "Huevo", "quantity": 1, "unit": "unidad"},
    {"name": "Sal", "quantity": 1, "unit": "pizca"},
    {"name": "Pimienta negra", "quantity": 1, "unit": "pizca"},
    {"name": "Aceite de oliva", "quantity": 5, "unit": "ml"}
  ],
  "instructions": "1. Tostar el pan integral. 2. Triturar el aguacate con sal y pimienta. 3. Pochar el huevo en agua hirviendo con vinagre. 4. Untar el aguacate en el pan y colocar el huevo encima. 5. Añadir un chorrito de aceite de oliva.",
  "difficulty": "facil",
  "cost": "medio",
  "tags": ["vegetariano", "saludable", "rapido"],
  "prep_time_min": 10,
  "servings": 1
}
```

### Ejemplo 2: Comida
```json
{
  "id": "lunch-001",
  "name": "Ensalada César con pollo",
  "description": "Lechuga romana con pollo a la plancha y salsa César",
  "meal_type": "lunch",
  "supermarket": "mercadona",
  "calories": 450,
  "protein_g": 35,
  "carbs_g": 15,
  "fat_g": 28,
  "fiber_g": 4,
  "ingredients": [
    {"name": "Pechuga de pollo", "quantity": 150, "unit": "g"},
    {"name": "Lechuga romana", "quantity": 150, "unit": "g"},
    {"name": "Parmesano", "quantity": 30, "unit": "g"},
    {"name": "Crutones", "quantity": 30, "unit": "g"},
    {"name": "Salsa César", "quantity": 30, "unit": "ml"}
  ],
  "instructions": "1. Hacer pollo a la plancha y cortar en tiras. 2. Lavar y cortar lechuga. 3. Mezclar con salsa, queso y crutones.",
  "difficulty": "facil",
  "cost": "medio",
  "tags": ["proteico", "fresco", "clásico"],
  "prep_time_min": 15,
  "servings": 1
}
```

### Ejemplo 3: Cena
```json
{
  "id": "dinner-001",
  "name": "Salmón al horno con espárragos",
  "description": "Filete de salmón con espárragos verdes",
  "meal_type": "dinner",
  "supermarket": "mercadona",
  "calories": 480,
  "protein_g": 35,
  "carbs_g": 12,
  "fat_g": 32,
  "fiber_g": 4,
  "ingredients": [
    {"name": "Salmón", "quantity": 160, "unit": "g"},
    {"name": "Espárragos", "quantity": 150, "unit": "g"},
    {"name": "Limón", "quantity": 0.5, "unit": "unidad"},
    {"name": "Aceite", "quantity": 15, "unit": "ml"},
    {"name": "Eneldo", "quantity": 1, "unit": "cucharadita"}
  ],
  "instructions": "1. Colocar salmón en bandeja con espárragos. 2. Aliñar con aceite y limón. 3. Hornear 18 minutos a 200C.",
  "difficulty": "facil",
  "cost": "caro",
  "tags": ["pescado", "omega3", "saludable", "bajo_carbohidratos"],
  "prep_time_min": 20,
  "servings": 1
}
```

### Ejemplo 4: Merienda
```json
{
  "id": "snack-001",
  "name": "Yogur con nueces",
  "description": "Yogur griego con nueces",
  "meal_type": "snack",
  "supermarket": "mercadona",
  "calories": 240,
  "protein_g": 15,
  "carbs_g": 12,
  "fat_g": 16,
  "fiber_g": 2,
  "ingredients": [
    {"name": "Yogur griego", "quantity": 150, "unit": "g"},
    {"name": "Nueces", "quantity": 25, "unit": "g"}
  ],
  "instructions": "1. Servir yogur. 2. Añadir nueces picadas.",
  "difficulty": "facil",
  "cost": "barato",
  "tags": ["proteico", "omega3", "rapido"],
  "prep_time_min": 2,
  "servings": 1
}
```

## 5. RESUMEN DE ARCHIVOS CREADOS

### Archivos de migración SQL:
- `migrations/001_add_recipe_fields.sql` - SQL para añadir columnas y funciones

### Archivos CSV con recetas enriquecidas:
- `data/enriched_recipes.csv` - **50 desayunos** con ingredientes completos
- `data/enriched_recipes_lunch.csv` - **75 comidas** con ingredientes completos
- `data/enriched_recipes_dinner.csv` - **50 cenas** con ingredientes completos
- `data/enriched_recipes_snacks.csv` - **25 meriendas** con ingredientes completos

### Total: **200 recetas enriquecidas**

## 6. ESTADÍSTICAS DE RECETAS POR TIPO

| Tipo | Cantidad | Dificultad Principal | Coste Principal |
|------|----------|---------------------|-----------------|
| Desayuno | 50 | Facil (80%) | Medio (50%) |
| Comida | 75 | Facil-Medio (70%) | Medio (55%) |
| Cena | 50 | Facil (65%) | Medio (45%) |
| Merienda | 25 | Facil (100%) | Barato (60%) |

## 7. PRÓXIMOS PASOS RECOMENDADOS

1. **Ejecutar migración SQL** en Supabase
2. **Importar CSVs** a la base de datos
3. **Actualizar recetas existentes** con los nuevos campos
4. **Crear índices** para búsquedas eficientes
5. **Implementar funciones de búsqueda** por ingredientes y tags