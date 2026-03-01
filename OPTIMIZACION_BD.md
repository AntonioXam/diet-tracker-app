# Optimización de Base de Datos - Diet Tracker

## Resumen

Se ha realizado un análisis del esquema de la base de datos de la aplicación Diet Tracker (tablas: users, user_profiles, weight_history, master_recipes, user_food_bank, weekly_plans) y se han identificado áreas de mejora en índices, relaciones, normalización y rendimiento de consultas.

## Esquema Actual

El esquema actual (definido en `create_tables.py`) incluye:

1. **users**: id, email (UNIQUE), password_hash, name, created_at
2. **user_profiles**: user_id (PK, FK a users), datos demográficos y de objetivos
3. **weight_history**: id, user_id (FK a users), weight_kg, week_number, recorded_at
4. **master_recipes**: id, name, meal_type, datos nutricionales, ingredients, instructions, supermarket, category
5. **user_food_bank**: id, user_id (FK a users), meal_type, recipe_id (FK a master_recipes), times_used, added_week
6. **weekly_plans**: id, user_id (FK a users), week_number, day_of_week, meal_type, selected_recipe_id (FK a master_recipes), macros

Índices existentes (según `create_tables.py`):
- `idx_users_email` ON users(email)
- `idx_profiles_user` ON user_profiles(user_id)
- `idx_weight_user` ON weight_history(user_id)
- `idx_recipes_meal` ON master_recipes(meal_type)
- `idx_foodbank_user` ON user_food_bank(user_id, meal_type)
- `idx_plans_user_week` ON weekly_plans(user_id, week_number)

## Áreas de Mejora Identificadas

### 1. Integridad Referencial

Las claves foráneas actuales no especifican acción `ON DELETE`. Se recomienda agregar `ON DELETE CASCADE` para mantener la integridad automáticamente al eliminar usuarios.

**Tablas afectadas:**
- `user_profiles` (relación 1:1 con users)
- `weight_history`
- `user_food_bank`
- `weekly_plans`

### 2. Índices Adicionales

Basado en los patrones de consulta observados en `app.py`, se requieren los siguientes índices para mejorar el rendimiento:

#### weight_history
- `(user_id, recorded_at)` → para consultas ordenadas por fecha (historial de peso)
- `(user_id, week_number)` → para consultas por semana

#### master_recipes
- `(category)` → si se filtran recetas por categoría
- `(supermarket)` → si se filtran por supermercado
- `(meal_type, id)` → para consultas que excluyen IDs específicos (ej: `NOT IN`)

#### user_food_bank
- `(recipe_id)` → para joins con master_recipes
- `(user_id, recipe_id)` → para la función `increment_recipe_usage` y búsquedas específicas

#### weekly_plans
- `(selected_recipe_id)` → para joins con master_recipes
- `(user_id, week_number, day_of_week)` → índice covering para consultas diarias

### 3. Normalización (Opcional)

Los campos `allergies` y `disliked_foods` en `user_profiles` se almacenan como TEXT (posiblemente listas separadas por comas). Si la aplicación necesita consultar o filtrar por alergias/alimentos individuales, se recomienda crear tablas separadas:

```sql
CREATE TABLE user_allergies (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id) ON DELETE CASCADE,
    allergy TEXT NOT NULL
);

CREATE TABLE user_disliked_foods (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id) ON DELETE CASCADE,
    food TEXT NOT NULL
);
```

De lo contrario, mantener el diseño actual es aceptable.

### 4. Función `increment_recipe_usage`

La función actual es correcta pero se beneficiará del índice `(user_id, recipe_id)` en `user_food_bank`. No se requiere modificación.

### 5. Estadísticas

Ejecutar `ANALYZE` periódicamente para mantener las estadísticas del optimizador actualizadas.

## Script de Optimización

Se ha generado el archivo `api/optimize_schema.sql` con todas las mejoras propuestas. El script incluye:

1. Modificación de claves foráneas con `ON DELETE CASCADE`.
2. Creación de índices adicionales (con `IF NOT EXISTS`).
3. Comentarios sobre normalización opcional.
4. Comando `ANALYZE` para todas las tablas.

## Pasos para Aplicar las Mejoras

### Opción A: Ejecutar script automáticamente (requiere permisos de service role)

1. Asegúrese de que las credenciales de Supabase estén configuradas en el archivo `.env` (SUPABASE_URL, SUPABASE_KEY).
2. Ejecute el script Python:
   ```bash
   cd api
   python3 optimize_database.py
   ```

### Opción B: Ejecutar manualmente en el SQL Editor de Supabase

1. Acceda al dashboard de Supabase > SQL Editor.
2. Copie y pegue el contenido de `api/optimize_schema.sql`.
3. Revise las sentencias (especialmente `DROP CONSTRAINT`) y ejecute.

**Nota:** El script usa `DROP CONSTRAINT IF EXISTS` para evitar errores si los nombres de las restricciones difieren. Ajuste los nombres si es necesario.

## Verificación

Después de aplicar los cambios, verifique que los índices se hayan creado correctamente:

```sql
-- Listar índices de cada tabla
SELECT tablename, indexname, indexdef 
FROM pg_indexes 
WHERE schemaname = 'public' 
ORDER BY tablename, indexname;
```

## Rendimiento Esperado

- **Consultas de historial de peso:** Mejora en ordenación por fecha.
- **Generación de planes semanales:** Mejora en joins con recetas.
- **Incremento de uso de recetas:** Actualización más rápida.
- **Consultas filtradas por categoría/supermercado:** Mejora significativa si se usan frecuentemente.

## Recomendaciones Adicionales

1. **Monitoreo:** Utilice las herramientas de monitoreo de Supabase (Logs, Query Performance) para identificar consultas lentas.
2. **Backup:** Realice un backup de la base de datos antes de aplicar cambios estructurales.
3. **Pruebas:** Ejecute las consultas críticas en un entorno de pruebas para medir la mejora.

## Archivos Generados

- `api/optimize_schema.sql`: Script SQL con todas las optimizaciones.
- `api/optimize_database.py`: Script Python para ejecutar automáticamente (requiere configuración).
- `OPTIMIZACION_BD.md`: Este informe.

## Contacto

Para cualquier duda o ajuste, consulte con el especialista de bases de datos.

---
*Última actualización: 2026-03-01*