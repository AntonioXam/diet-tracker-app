"""Validación de datos de entrada."""

from typing import Dict, List, Optional, Tuple


def validate_register_data(data: Dict) -> Tuple[bool, Optional[str], Optional[Dict]]:
    """Valida datos de registro."""
    required = ['username', 'age', 'gender', 'height', 'current_weight', 'goal_weight', 'goal_type', 'activity_level', 'meals_per_day']
    
    missing = [k for k in required if k not in data]
    if missing:
        return False, f'Faltan datos: {", ".join(missing)}', None
    
    # Validar tipos
    try:
        age = int(data['age'])
        height = float(data['height'])
        current_weight = float(data['current_weight'])
        goal_weight = float(data['goal_weight'])
        meals_per_day = int(data['meals_per_day'])
    except ValueError:
        return False, 'Datos numéricos inválidos', None
    
    if age < 10 or age > 120:
        return False, 'Edad inválida (debe estar entre 10 y 120)', None
    if height < 100 or height > 250:
        return False, 'Altura inválida (debe estar entre 100 y 250 cm)', None
    if current_weight < 30 or current_weight > 300:
        return False, 'Peso actual inválido (debe estar entre 30 y 300 kg)', None
    if goal_weight < 30 or goal_weight > 300:
        return False, 'Peso objetivo inválido', None
    if meals_per_day not in [3, 4, 5]:
        return False, 'Comidas por día debe ser 3, 4 o 5', None
    if data['gender'] not in ['male', 'female']:
        return False, 'Género debe ser male o female', None
    if data['goal_type'] not in ['lose', 'gain', 'maintain']:
        return False, 'Tipo de objetivo inválido', None
    if data['activity_level'] not in ['sedentary', 'light', 'moderate', 'active', 'very_active']:
        return False, 'Nivel de actividad inválido', None
    
    # Datos limpios
    cleaned = {
        'username': str(data['username']).strip(),
        'age': age,
        'gender': data['gender'],
        'height': height,
        'current_weight': current_weight,
        'goal_weight': goal_weight,
        'goal_type': data['goal_type'],
        'activity_level': data['activity_level'],
        'meals_per_day': meals_per_day,
        'allergies': data.get('allergies', ''),
        'disliked_foods': data.get('disliked_foods', '')
    }
    
    return True, None, cleaned


def validate_profile_update(data: Dict) -> Tuple[bool, Optional[str], Optional[Dict]]:
    """Valida datos de actualización de perfil."""
    allowed_fields = ['age', 'gender', 'height', 'current_weight', 'goal_weight', 'activity_level', 'meals_per_day', 'allergies', 'disliked_foods', 'goal_type']
    
    cleaned = {}
    for field in allowed_fields:
        if field in data and data[field] is not None:
            cleaned[field] = data[field]
    
    # Validaciones específicas si están presentes
    if 'age' in cleaned:
        try:
            age = int(cleaned['age'])
            if age < 10 or age > 120:
                return False, 'Edad inválida', None
        except ValueError:
            return False, 'Edad debe ser número', None
    
    if 'height' in cleaned:
        try:
            height = float(cleaned['height'])
            if height < 100 or height > 250:
                return False, 'Altura inválida', None
        except ValueError:
            return False, 'Altura debe ser número', None
    
    if 'current_weight' in cleaned:
        try:
            weight = float(cleaned['current_weight'])
            if weight < 30 or weight > 300:
                return False, 'Peso actual inválido', None
        except ValueError:
            return False, 'Peso actual debe ser número', None
    
    if 'meals_per_day' in cleaned:
        if cleaned['meals_per_day'] not in [3, 4, 5]:
            return False, 'Comidas por día inválido', None
    
    if 'gender' in cleaned and cleaned['gender'] not in ['male', 'female']:
        return False, 'Género inválido', None
    
    if 'goal_type' in cleaned and cleaned['goal_type'] not in ['lose', 'gain', 'maintain']:
        return False, 'Tipo de objetivo inválido', None
    
    if 'activity_level' in cleaned and cleaned['activity_level'] not in ['sedentary', 'light', 'moderate', 'active', 'very_active']:
        return False, 'Nivel de actividad inválido', None
    
    return True, None, cleaned


def validate_weight_checkin(data: Dict) -> Tuple[bool, Optional[str], Optional[Dict]]:
    """Valida datos de registro de peso."""
    required = ['user_id', 'weight']
    missing = [k for k in required if k not in data]
    if missing:
        return False, f'Faltan datos: {", ".join(missing)}', None
    
    try:
        weight = float(data['weight'])
        if weight < 30 or weight > 300:
            return False, 'Peso inválido', None
    except ValueError:
        return False, 'Peso debe ser número', None
    
    cleaned = {
        'user_id': data['user_id'],
        'weight': weight
    }
    return True, None, cleaned