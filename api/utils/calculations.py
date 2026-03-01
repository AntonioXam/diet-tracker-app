"""Utilidades para cálculos nutricionales y metabólicos."""

def calculate_tmb(age: int, gender: str, height: float, weight: float) -> float:
    """Tasa Metabólica Basal - fórmula Mifflin-St Jeor."""
    if gender == 'male':
        tmb = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        tmb = 10 * weight + 6.25 * height - 5 * age - 161
    return tmb


def calculate_tdee(tmb: float, activity_level: str) -> float:
    """Gasto Energético Diario Total según nivel de actividad."""
    multipliers = {
        'sedentary': 1.2,
        'light': 1.375,
        'moderate': 1.55,
        'active': 1.725,
        'very_active': 1.9
    }
    return tmb * multipliers.get(activity_level, 1.2)


def calculate_target_calories(tdee: float, goal_type: str, current_weight: float, goal_weight: float) -> float:
    """Calcula calorías objetivo de forma segura y realista."""
    if goal_type == 'lose':
        # Déficit seguro: 300-500 kcal menos del TDEE
        # Nunca menos de 1200 kcal (mínimo saludable)
        deficit = min(500, max(300, (current_weight - goal_weight) * 15))
        target = max(1200, tdee - deficit)
        return target
    elif goal_type == 'gain':
        # Superávit moderado: +250-300 kcal
        return min(tdee + 300, 3500)  # Máximo 3500 kcal
    # Mantenimiento
    return tdee


def get_meal_types_for_count(meals_per_day: int) -> list[str]:
    """Devuelve los tipos de comida correctos según el número seleccionado."""
    if meals_per_day == 3:
        return ['desayuno', 'comida', 'cena']  # 3 principales
    elif meals_per_day == 4:
        return ['desayuno', 'comida', 'merienda', 'cena']  # añade merienda
    elif meals_per_day == 5:
        return ['desayuno', 'almuerzo', 'comida', 'merienda', 'cena']  # todas
    else:
        return ['desayuno', 'comida', 'cena']  # default