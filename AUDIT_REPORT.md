# 🔍 AUDITORÍA COMPLETA BACKEND - Diet Tracker API

**Fecha:** 2026-03-05  
**Archivo auditado:** `/Users/servimac/.openclaw/workspace/diet-tracker-app/api/app.py`

---

## 📋 TAREA 1 - Lista completa de endpoints (13 total)

| # | Método | Ruta | Función | Implementado | try/except |
|---|--------|------|---------|--------------|------------|
| 1 | GET | `/api/health` | `health()` | ✅ Sí | ❌ No |
| 2 | POST | `/api/onboarding` | `onboarding()` | ✅ Sí | ✅ Sí |
| 3 | GET | `/api/profile` | `get_profile()` | ✅ Sí | ✅ Sí |
| 4 | POST | `/api/profile` | `update_profile()` | ✅ Sí | ✅ Sí |
| 5 | GET | `/api/recipes` | `get_recipes()` | ✅ Sí | ✅ Sí |
| 6 | GET | `/api/plan` | `get_plan()` | ✅ Sí | ✅ Sí |
| 7 | POST | `/api/plan/swap` | `swap_plan_meal()` | ✅ Sí | ✅ Sí |
| 8 | GET | `/api/shopping-list` | `get_shopping_list()` | ✅ Sí | ✅ Sí |
| 9 | POST | `/api/weight` | `register_weight()` | ✅ Sí | ✅ Sí |
| 10 | GET | `/api/stats` | `get_stats()` | ✅ Sí | ✅ Sí |
| 11 | POST | `/api/food-log` | `log_food()` | ✅ Sí | ✅ Sí |
| 12 | GET | `/api/dashboard` | `get_dashboard()` | ✅ Sí | ✅ Sí |
| 13 | POST | `/api/register` | `register()` | ✅ Sí | ✅ Sí |
| 14 | POST | `/api/login` | `login()` | ✅ Sí | ✅ Sí |
| 15 | POST | `/api/recover-password` | `recover_password()` | ✅ Sí | ✅ Sí |
| 16 | POST | `/api/reset-password` | `reset_password()` | ✅ Sí | ✅ Sí |

**Total: 16 endpoints** (no 13 como se mencionó inicialmente)

---

## 📋 TAREA 2 - Verificación de implementación real

### ✅ Endpoints correctamente implementados (con código completo):

1. **GET /api/health** - ✅ Implementado
   - Función existe con código
   - Return jsonify: ✅
   - Manejo de errores: ❌ No tiene try/except
   - Conexión Supabase: ❌ No usa

2. **POST /api/onboarding** - ✅ Implementado
   - Función existe con código completo
   - Return jsonify: ✅
   - Manejo de errores: ✅ try/except completo
   - Conexión Supabase: ✅ (users, user_profiles, weight_history)

3. **GET /api/profile** - ✅ Implementado
   - Función existe con código
   - Return jsonify: ✅
   - Manejo de errores: ✅
   - Conexión Supabase: ✅ (user_profiles)

4. **POST /api/profile** - ✅ Implementado
   - Función existe con código completo
   - Return jsonify: ✅
   - Manejo de errores: ✅
   - Conexión Supabase: ✅ (user_profiles upsert)

5. **GET /api/recipes** - ✅ Implementado
   - Función existe con código
   - Return jsonify: ✅
   - Manejo de errores: ✅
   - Conexión Supabase: ✅ (master_recipes)

6. **GET /api/plan** - ✅ Implementado
   - Función existe con código
   - Return jsonify: ✅
   - Manejo de errores: ✅
   - Conexión Supabase: ✅ (weekly_plans, master_recipes)

7. **POST /api/plan/swap** - ✅ Implementado
   - Función existe con código
   - Return jsonify: ✅
   - Manejo de errores: ✅
   - Conexión Supabase: ✅ (weekly_plans, master_recipes)

8. **GET /api/shopping-list** - ✅ Implementado
   - Función existe con código
   - Return jsonify: ✅
   - Manejo de errores: ✅
   - Conexión Supabase: ✅ (weekly_plans, master_recipes)

9. **POST /api/weight** - ✅ Implementado
   - Función existe con código
   - Return jsonify: ✅
   - Manejo de errores: ✅
   - Conexión Supabase: ✅ (weight_history, user_profiles)

10. **GET /api/stats** - ✅ Implementado
    - Función existe con código
    - Return jsonify: ✅
    - Manejo de errores: ✅
    - Conexión Supabase: ✅ (weight_history, user_profiles, food_logs)

11. **POST /api/food-log** - ✅ Implementado
    - Función existe con código
    - Return jsonify: ✅
    - Manejo de errores: ✅
    - Conexión Supabase: ✅ (food_logs)

12. **GET /api/dashboard** - ✅ Implementado
    - Función existe con código completo
    - Return jsonify: ✅
    - Manejo de errores: ✅
    - Conexión Supabase: ✅ (user_profiles, weekly_plans, food_logs, weight_history)

13. **POST /api/register** - ✅ Implementado
    - Función existe con código
    - Return jsonify: ✅
    - Manejo de errores: ✅
    - Conexión Supabase: ✅ (users)

14. **POST /api/login** - ✅ Implementado
    - Función existe con código
    - Return jsonify: ✅
    - Manejo de errores: ✅
    - Conexión Supabase: ✅ (users)

15. **POST /api/recover-password** - ✅ Implementado
    - Función existe con código
    - Return jsonify: ✅
    - Manejo de errores: ✅
    - Conexión Supabase: ✅ (users)

16. **POST /api/reset-password** - ✅ Implementado
    - Función existe con código
    - Return jsonify: ✅
    - Manejo de errores: ✅
    - Conexión Supabase: ✅ (users)

---

## 📋 TAREA 3 - Testeo de endpoints

**Estado del servidor:** ❌ El servidor NO está corriendo en puerto 5000

No se pudieron hacer llamadas curl porque el servidor Flask no está activo.

**Para iniciar el servidor:**
```bash
cd /Users/servimac/.openclaw/workspace/diet-tracker-app/api
python3 app.py
```

---

## 📋 TAREA 4 - Verificación de Supabase

### Credenciales verificadas: ✅ SI

```
SUPABASE_URL: https://kaomgwojvnncidyezdzj.supabase.co
SUPABASE_KEY: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9... (anon key válida)
```

### Estado de la conexión: ✅ FUNCIONA

### Tablas existentes en Supabase:

| Tabla | Estado | Notas |
|-------|--------|-------|
| `user_profiles` | ✅ Existe | Tabla vacía |
| `master_recipes` | ✅ Existe | Tabla vacía |
| `weekly_plans` | ✅ Existe | Tabla vacía |
| `food_logs` | ✅ Existe | Tabla vacía |
| `weight_logs` | ✅ Existe | Tabla vacía |
| `users` | ❌ NO EXISTE | **PROBLEMA CRÍTICO** |
| `weight_history` | ❌ NO EXISTE | **PROBLEMA CRÍTICO** |
| `plan_meals` | ❓ No verificada | Existe en schema |
| `shopping_lists` | ❓ No verificada | Existe en schema |

---

## 🚨 ERRORES ENCONTRADOS

### 1. **Tablas faltantes en Supabase** (CRÍTICO)

El código en `app.py` usa estas tablas que **NO EXISTEN**:

- **`users`** - Usada en: `/api/register`, `/api/login`, `/api/recover-password`, `/api/reset-password`, `/api/onboarding`
- **`weight_history`** - Usada en: `/api/weight`, `/api/stats`, `/api/onboarding`, `/api/dashboard`

**Impacto:** Los endpoints de auth (registro/login) y registro de peso **FALLARÁN** con error 500.

### 2. **Mismatch de nombres de columnas**

El schema real tiene columnas diferentes a las que el código espera:

| Código app.py | Schema real (supabase_schema.sql) |
|---------------|-----------------------------------|
| `current_weight_kg` | `weight_kg` |
| `goal_weight_kg` | `target_weight_kg` |
| `goal_type` | `goal` |
| `allergies` (string) | `allergies` (array TEXT[]) |
| `disliked_foods` | ❌ No existe en schema |
| `tmb` | ❌ No existe (se calcula con función) |
| `tdee` | ❌ No existe |
| `target_calories` | `daily_calories` |
| `week_number` | ❌ No existe (usa week_start/week_end) |
| `day_of_week` | ✅ Existe en plan_meals |
| `ingredients` (string) | `ingredients` (JSONB) |

### 3. **Tabla weekly_plans tiene estructura diferente**

El código espera:
- `week_number` (integer)
- `day_of_week` (integer)
- `selected_recipe_id` (integer)

El schema real tiene:
- `week_start` (DATE)
- `week_end` (DATE)
- Los meals están en tabla separada `plan_meals`

### 4. **IDs son UUID, no integers**

El schema usa `UUID` para todos los IDs, pero el código en `app.py` trata los IDs como integers en varios lugares (ej: `recipe_id: int` en Pydantic models).

---

## 📊 RESUMEN DE ESTADO

### Endpoints: 16 totales

| Estado | Count | Porcentaje |
|--------|-------|------------|
| ✅ Implementado (código completo) | 16 | 100% |
| ⚠️ Parcial (problemas de schema) | 12 | 75% |
| ❌ No funcional (tablas faltantes) | 6 | 37.5% |

### Endpoints que FALLARÁN por tablas faltantes:

1. **POST /api/register** - ❌ Tabla `users` no existe
2. **POST /api/login** - ❌ Tabla `users` no existe
3. **POST /api/recover-password** - ❌ Tabla `users` no existe
4. **POST /api/reset-password** - ❌ Tabla `users` no existe
5. **POST /api/onboarding** - ❌ Tabla `users` y `weight_history` no existen
6. **POST /api/weight** - ❌ Tabla `weight_history` no existe
7. **GET /api/stats** - ⚠️ Usa `weight_history` (fallback posible)
8. **GET /api/dashboard** - ⚠️ Usa `weight_history` (fallback posible)

### Endpoints que FALLARÁN por mismatch de columnas:

1. **GET /api/profile** - ⚠️ Columnas `current_weight_kg`, `goal_weight_kg`, `goal_type`, `tmb`, `tdee`, `target_calories`
2. **POST /api/profile** - ⚠️ Mismos problemas de columnas
3. **GET /api/plan** - ⚠️ `week_number` vs `week_start`, `selected_recipe_id`
4. **POST /api/plan/swap** - ⚠️ Mismos problemas
5. **GET /api/shopping-list** - ⚠️ `week_number` vs `week_start`
6. **GET /api/recipes** - ✅ Debería funcionar (master_recipes existe)
7. **POST /api/food-log** - ⚠️ Posibles problemas de columnas

---

## 🔧 ACCIONES RECOMENDADAS

### Prioridad 1 - Crear tablas faltantes:

```sql
-- Crear tabla users (para auth personalizado)
CREATE TABLE IF NOT EXISTS users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email TEXT UNIQUE NOT NULL,
  password_hash TEXT NOT NULL,
  name TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Crear tabla weight_history (alias compatible con el código)
CREATE TABLE IF NOT EXISTS weight_history (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  weight_kg DECIMAL(5,2) NOT NULL,
  week_number INTEGER,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
```

### Prioridad 2 - Actualizar app.py para usar nombres correctos:

Opción A: Modificar el código para usar los nombres del schema real
Opción B: Crear vistas en Supabase con los nombres que el código espera

### Prioridad 3 - Fix de tipos de datos:

- Cambiar `recipe_id: int` a `recipe_id: str` (UUID) en Pydantic models
- Actualizar validaciones para aceptar UUIDs

---

## ✅ Credenciales Supabase: VERIFICADAS (SI)

- URL: ✅ Correcta
- Anon Key: ✅ Válida
- Conexión: ✅ Funciona
- Tablas principales: ✅ 5 de 7 existen
- Tablas críticas faltantes: ❌ `users`, `weight_history`

---

**Fin del reporte de auditoría.**
