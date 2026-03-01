# Mejoras en la Lógica de Negocio - Diet Tracker

## Resumen

Se han implementado mejoras significativas en los algoritmos de nutrición y lógica de negocio de la aplicación Diet Tracker. Los cambios buscan hacer las recomendaciones más personalizadas, precisas y seguras para el usuario.

## Mejoras Implementadas

### 1. Cálculo de Calorías Mejorado

**Fórmulas ampliadas:**
- `calculate_tmb` ahora soporta tres fórmulas:
  - Mifflin-St Jeor (default)
  - Harris-Benedict (revisada)
  - Katch-McArdle (si se proporciona porcentaje de grasa corporal)
- Parámetros opcionales: `body_fat_percentage`, `formula`

**Cálculo de déficit/superávit mejorado:**
- `calculate_deficit` ahora incluye:
  - Tasa de pérdida de peso configurable (`slow`, `moderate`, `aggressive`)
  - Límite seguro: déficit máximo del 20% del TDEE
  - Mínimos saludables por género (1200 kcal mujeres, 1500 hombres)
  - Consideración del TMB para evitar caer por debajo del metabolismo basal
- Todos los llamados a esta función fueron actualizados para pasar `tmb` y `gender`

### 2. Distribución Calórica por Tipo de Comida

Nueva función `get_calorie_distribution`:
- Distribuye las calorías diarias objetivo entre los tipos de comida según el número de comidas por día
- Porcentajes basados en recomendaciones dietéticas:
  - 3 comidas: desayuno 30%, comida 40%, cena 30%
  - 4 comidas: desayuno 30%, comida 35%, merienda 10%, cena 25%
  - 5 comidas: desayuno 25%, almuerzo 10%, comida 35%, merienda 10%, cena 20%

### 3. Generación de Plan Semanal Inteligente

`generate_first_week_varied` mejorada:
- **Filtrado por alergias y alimentos desagradables:** compara ingredientes de las recetas con las listas del perfil
- **Distribución calórica:** selecciona recetas que se acerquen a las calorías objetivo por tipo de comida
- **Selección greedy:** ordena recetas disponibles por proximidad calórica, no aleatoria pura
- **Gestión del banco de comidas:** incrementa `times_used` en lugar de insertar duplicados

### 4. Sistema de Recomendación en Banco de Comidas

`get_food_bank` mejorada:
- Calcula score de recomendación para cada opción:
  - **Uso:** prioriza recetas menos utilizadas (`times_used`)
  - **Calorías:** prioriza proximidad a las calorías objetivo del tipo de comida
- Score combinado (60% uso, 40% calorías)
- **Filtrado de seguridad:** verifica ingredientes contra alergias y preferencias
- **Ordenamiento:** devuelve opciones ordenadas del mejor al peor score

### 5. Corrección de Bugs

- `regenerate_plan` ahora usa las calorías objetivo del perfil en lugar de 2000 fijos
- Todas las llamadas a `calculate_deficit` actualizadas con parámetros requeridos
- Manejo de `times_used` en banco de comidas (incremento en lugar de duplicados)

## Cambios en la Base de Datos

No se requieren cambios en el esquema de base de datos existente. Se aprovechan campos ya existentes:
- `allergies` y `disliked_foods` en `user_profiles`
- `times_used` en `user_food_bank` (ya existía pero no se actualizaba correctamente)

## Próximas Mejoras Sugeridas

1. **Sistema de recomendación avanzado:** incorporar aprendizaje por refuerzo basado en ratings del usuario
2. **Balance de macronutrientes:** calcular distribución óptima de proteínas, carbohidratos y grasas según objetivo
3. **Planificación de porciones:** ajustar tamaño de porción para cumplir calorías objetivo exactas
4. **Lista de compra inteligente:** deduplicación semántica de ingredientes y sumatoria de cantidades
5. **Predicción de progreso:** estimar fecha de llegada al objetivo basado en tasa de pérdida histórica
6. **Integración con wearables:** importar actividad física para ajustar TDEE dinámicamente

## Archivos Modificados

- `api/app.py`: todas las funciones mencionadas
- Se creó copia de seguridad `api/app.py.backup`

## Validación

Se recomienda realizar pruebas exhaustivas con:
1. Usuarios con alergias y preferencias
2. Diferentes objetivos (pérdida, ganancia, mantenimiento)
3. Varios niveles de actividad física
4. Diferentes números de comidas diarias

Las mejoras mantienen compatibilidad con la API existente; no se rompen endpoints actuales.