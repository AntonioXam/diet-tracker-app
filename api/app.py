"""
Diet Tracker API - Backend con Supabase
11 Endpoints principales con JWT auth y validación pydantic
"""
import os
import hashlib
import base64
import secrets
import time
import random
import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask import Flask, request, jsonify
from flask_cors import CORS
from supabase import create_client
from pydantic import BaseModel, Field
from typing import Optional, List

app = Flask(__name__)
CORS(app, origins=["*"], supports_credentials=True)

# Credenciales Supabase
SUPABASE_URL = "https://kaomgwojvnncidyezdzj.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imthb21nd29qdm5uY2lkeWV6ZHpqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzI3MDcxNzYsImV4cCI6MjA4ODI4MzE3Nn0.Ds2ICxfiahuqt2n83dwoX9tMYGf7Xz8Jjvx6lFJc4zs"
JWT_SECRET = os.getenv("JWT_SECRET", secrets.token_hex(32))

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ==================== MODELOS PYDANTIC ====================

class OnboardingRequest(BaseModel):
    age: int = Field(..., ge=10, le=120)
    gender: str = Field(..., pattern="^(male|female)$")
    height: float = Field(..., ge=100, le=250)
    current_weight: float = Field(..., ge=30, le=300)
    goal_weight: float = Field(..., ge=30, le=300)
    goal_type: str = Field(..., pattern="^(lose|gain|maintain)$")
    activity_level: str = Field(..., pattern="^(sedentary|light|moderate|active|very_active)$")
    meals_per_day: int = Field(..., ge=3, le=5)
    allergies: Optional[str] = ""
    disliked_foods: Optional[str] = ""

class ProfileUpdateRequest(BaseModel):
    age: Optional[int] = Field(None, ge=10, le=120)
    gender: Optional[str] = Field(None, pattern="^(male|female)$")
    height: Optional[float] = Field(None, ge=100, le=250)
    current_weight: Optional[float] = Field(None, ge=30, le=300)
    goal_weight: Optional[float] = Field(None, ge=30, le=300)
    goal_type: Optional[str] = Field(None, pattern="^(lose|gain|maintain)$")
    activity_level: Optional[str] = Field(None, pattern="^(sedentary|light|moderate|active|very_active)$")
    meals_per_day: Optional[int] = Field(None, ge=3, le=5)
    allergies: Optional[str] = None
    disliked_foods: Optional[str] = None
    budget: Optional[str] = Field(None, pattern="^(low|medium|high)$")
    preferences: Optional[list] = None
    target_calories: Optional[int] = Field(None, ge=1000, le=5000)

class WeightRequest(BaseModel):
    weight: float = Field(..., ge=30, le=300)

class FoodLogRequest(BaseModel):
    recipe_id: str  # UUID
    meal_type: str
    calories: float
    protein: float
    carbs: float
    fat: float
    notes: Optional[str] = ""

class PlanSwapRequest(BaseModel):
    plan_id: str  # UUID
    new_recipe_id: str  # UUID

class GeneratePlanRequest(BaseModel):
    user_id: Optional[str] = None  # Optional, uses token if not provided
    target_calories: Optional[int] = None  # Uses profile if not provided
    preferences: Optional[dict] = None  # Optional preferences override

# ==================== UTILIDADES ====================

def hash_password(password: str, salt: str = None):
    if salt is None:
        salt = base64.b64encode(os.urandom(16)).decode('utf-8')
    salted_password = password + salt
    hash_obj = hashlib.sha256(salted_password.encode('utf-8'))
    return {'hash': hash_obj.hexdigest(), 'salt': salt}

def verify_password(password: str, stored_hash: str, salt: str) -> bool:
    result = hash_password(password, salt)
    return result['hash'] == stored_hash

def generate_token(user_id: int, email: str) -> str:
    payload = {
        'user_id': user_id,
        'email': email,
        'exp': datetime.utcnow() + timedelta(days=7),
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, JWT_SECRET, algorithm='HS256')

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Token requerido'}), 401
        
        try:
            if token.startswith('Bearer '):
                token = token[7:]
            payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
            request.current_user = payload
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token expirado'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Token inválido'}), 401
        
        return f(*args, **kwargs)
    return decorated

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
        deficit = min(500, max(300, (current_weight - goal_weight) * 15))
        target = max(1200, tdee - deficit)
        return target
    elif goal_type == 'gain':
        return min(tdee + 300, 3500)
    return tdee

def get_meal_types_for_count(meals_per_day: int) -> list:
    """Devuelve los tipos de comida correctos según el número seleccionado."""
    if meals_per_day == 3:
        return ['desayuno', 'comida', 'cena']
    elif meals_per_day == 4:
        return ['desayuno', 'comida', 'merienda', 'cena']
    elif meals_per_day == 5:
        return ['desayuno', 'almuerzo', 'comida', 'merienda', 'cena']
    return ['desayuno', 'comida', 'cena']

def distribute_macros(calories: float, goal_type: str) -> dict:
    """
    Distribuye macros según objetivo:
    - lose: 40% protein, 30% carbs, 30% fat (high protein for satiety)
    - gain: 30% protein, 45% carbs, 25% fat (more carbs for energy)
    - maintain: 30% protein, 40% carbs, 30% fat (balanced)
    
    Returns grams of protein, carbs, fat per day.
    """
    calories = max(1200, min(4000, calories))  # Safety bounds
    
    if goal_type == 'lose':
        protein_ratio, carbs_ratio, fat_ratio = 0.40, 0.30, 0.30
    elif goal_type == 'gain':
        protein_ratio, carbs_ratio, fat_ratio = 0.30, 0.45, 0.25
    else:  # maintain
        protein_ratio, carbs_ratio, fat_ratio = 0.30, 0.40, 0.30
    
    # Calculate grams (protein: 4 cal/g, carbs: 4 cal/g, fat: 9 cal/g)
    protein_g = round((calories * protein_ratio) / 4, 1)
    carbs_g = round((calories * carbs_ratio) / 4, 1)
    fat_g = round((calories * fat_ratio) / 9, 1)
    
    return {
        'protein': protein_g,
        'carbs': carbs_g,
        'fat': fat_g,
        'calories': round(calories)
    }

def distribute_meal_calories(total_calories: float, meals_per_day: int) -> dict:
    """
    Distribute calories across meals based on meals_per_day.
    Typical distribution (approximate):
    - 3 meals: Breakfast 30%, Lunch 40%, Dinner 30%
    - 4 meals: Breakfast 25%, Lunch 35%, Snack 15%, Dinner 25%
    - 5 meals: Breakfast 20%, Morning snack 10%, Lunch 30%, Afternoon snack 15%, Dinner 25%
    """
    if meals_per_day == 3:
        distribution = {'desayuno': 0.30, 'comida': 0.40, 'cena': 0.30}
    elif meals_per_day == 4:
        distribution = {'desayuno': 0.25, 'comida': 0.35, 'merienda': 0.15, 'cena': 0.25}
    elif meals_per_day == 5:
        distribution = {
            'desayuno': 0.20,
            'almuerzo': 0.10,
            'comida': 0.30,
            'merienda': 0.15,
            'cena': 0.25
        }
    else:
        # Default to 4 meals
        distribution = {'desayuno': 0.25, 'comida': 0.35, 'merienda': 0.15, 'cena': 0.25}
    
    return {
        meal: round(total_calories * ratio)
        for meal, ratio in distribution.items()
    }

def select_recipes(supabase, meal_type: str, preferences: dict, target_calories: float, limit: int = 5) -> list:
    """
    Select suitable recipes for a meal type based on preferences and calorie target.
    
    Args:
        supabase: Supabase client
        meal_type: Type of meal (desayuno, comida, cena, etc.)
        preferences: dict with allergies, disliked_foods, goal_type
        target_calories: Target calories for this meal
        limit: Max number of recipes to return
    
    Returns:
        List of suitable recipe dicts
    """
    # Calorie range: +/- 20% of target
    min_cal = target_calories * 0.80
    max_cal = target_calories * 1.20
    
    try:
        # Base query for meal type
        query = supabase.table('master_recipes').select('*').eq('meal_type', meal_type)
        
        # Filter by calorie range
        query = query.gte('calories', min_cal).lte('calories', max_cal)
        
        # Execute query
        result = query.limit(limit * 2).execute()  # Get extra for filtering
        recipes = result.data or []
        
        # Filter by allergies and disliked foods
        allergies = preferences.get('allergies', '').lower() if preferences else ''
        disliked = preferences.get('disliked_foods', '').lower() if preferences else ''
        
        filtered = []
        for recipe in recipes:
            ingredients = recipe.get('ingredients', '').lower()
            
            # Skip if contains allergens
            if allergies:
                allergen_list = [a.strip() for a in allergies.split(',') if a.strip()]
                if any(allergen in ingredients for allergen in allergen_list):
                    continue
            
            # Skip if contains disliked foods
            if disliked:
                disliked_list = [d.strip() for d in disliked.split(',') if d.strip()]
                if any(food in ingredients for food in disliked_list):
                    continue
            
            filtered.append(recipe)
            
            if len(filtered) >= limit:
                break
        
        # If not enough recipes after filtering, return what we have
        return filtered[:limit] if filtered else recipes[:limit]
        
    except Exception as e:
        print(f"Error selecting recipes: {e}")
        return []

def generate_weekly_plan(supabase, user_id: str, profile: dict, target_calories: int = None) -> dict:
    """
    Generate a complete weekly meal plan for a user.
    
    Args:
        supabase: Supabase client
        user_id: User UUID
        profile: User profile dict with preferences
        target_calories: Optional override for calories
    
    Returns:
        dict with plan_id, week_number, days structure
    """
    import random
    
    # Get profile values
    meals_per_day = profile.get('meals_per_day', 4)
    goal_type = profile.get('goal', 'maintain')
    
    # Use provided calories or get from profile
    if target_calories is None:
        target_calories = profile.get('target_calories', 2000)
    
    # Calculate macros
    macros = distribute_macros(target_calories, goal_type)
    
    # Distribute calories per meal
    meal_calories = distribute_meal_calories(target_calories, meals_per_day)
    meal_types = get_meal_types_for_count(meals_per_day)
    
    # Prepare preferences
    preferences = {
        'allergies': profile.get('allergies', ''),
        'disliked_foods': profile.get('disliked_foods', ''),
        'goal_type': goal_type
    }
    
    # Get current week number
    week_number = datetime.now().isocalendar()[1]
    
    # Delete existing plan for this week
    try:
        supabase.table('weekly_plans').delete().eq('user_id', user_id).eq('week_number', week_number).execute()
    except:
        pass  # Continue even if delete fails
    
    # Generate plan for each day (7 days)
    days_of_week = ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo']
    weekly_plan = {}
    all_meals = []
    
    for day_idx, day_name in enumerate(days_of_week):
        day_meals = []
        
        for meal_type in meal_types:
            target = meal_calories.get(meal_type, target_calories / len(meal_types))
            
            # Select recipes for this meal
            recipes = select_recipes(supabase, meal_type, preferences, target, limit=10)
            
            if recipes:
                # Pick a random recipe from suitable ones
                selected_recipe = random.choice(recipes)
                
                meal_entry = {
                    'user_id': user_id,
                    'week_number': week_number,
                    'day_of_week': day_idx,
                    'meal_type': meal_type,
                    'selected_recipe_id': selected_recipe['id'],
                    'calories': selected_recipe.get('calories', target),
                    'protein': selected_recipe.get('protein', 0),
                    'carbs': selected_recipe.get('carbs', 0),
                    'fat': selected_recipe.get('fat', 0),
                    'recipe_name': selected_recipe.get('name', ''),
                    'recipe_image': selected_recipe.get('image_url', '')
                }
                
                day_meals.append(meal_entry)
                all_meals.append(meal_entry)
        
        weekly_plan[day_name] = day_meals
    
    # Batch insert all meals
    created_entries = []
    if all_meals:
        try:
            insert_result = supabase.table('weekly_plans').insert(all_meals).execute()
            created_entries = insert_result.data or []
        except Exception as e:
            print(f"Error inserting meals: {e}")
    
    return {
        'user_id': user_id,
        'week_number': week_number,
        'days': weekly_plan,
        'total_entries': len(created_entries),
        'macros_target': macros,
        'meal_calories': meal_calories
    }

# ==================== ENDPOINTS ====================

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'supabase_url': SUPABASE_URL})

# 1. POST /api/onboarding - Calcula TMB (Mifflin-St Jeor) + TDEE
@app.route('/api/onboarding', methods=['POST'])
def onboarding():
    """
    Registra usuario nuevo y calcula TMB + TDEE usando fórmula Mifflin-St Jeor.
    Crea perfil completo con objetivos de calorías.
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'JSON requerido'}), 400
        
        # Validar con pydantic
        try:
            onboarding_data = OnboardingRequest(**data)
        except Exception as e:
            return jsonify({'error': f'Datos inválidos: {str(e)}'}), 400
        
        # Calcular TMB y TDEE
        tmb = calculate_tmb(
            onboarding_data.age,
            onboarding_data.gender,
            onboarding_data.height,
            onboarding_data.current_weight
        )
        tdee = calculate_tdee(tmb, onboarding_data.activity_level)
        target_calories = calculate_target_calories(
            tdee,
            onboarding_data.goal_type,
            onboarding_data.current_weight,
            onboarding_data.goal_weight
        )
        
        # Crear usuario
        email = f"user_{secrets.token_hex(8)}@diettracker.app"
        user_result = supabase.table('users').insert({
            'email': email,
            'password_hash': 'onboarding_no_password',
            'name': f'User {secrets.token_hex(4)}'
        }).execute()
        
        if not user_result.data:
            return jsonify({'error': 'Error al crear usuario'}), 500
        
        user_id = user_result.data[0]['id']
        
        # Crear perfil
        week_number = datetime.now().isocalendar()[1]
        profile_result = supabase.table('user_profiles').insert({
            'user_id': user_id,
            'age': onboarding_data.age,
            'gender': onboarding_data.gender,
            'height_cm': onboarding_data.height,
            'weight_kg': onboarding_data.current_weight,
            'target_weight_kg': onboarding_data.goal_weight,
            'goal': onboarding_data.goal_type,
            'activity_level': onboarding_data.activity_level,
            'meals_per_day': onboarding_data.meals_per_day,
            'allergies': onboarding_data.allergies or '',
            'disliked_foods': onboarding_data.disliked_foods or '',
            'tmb': round(tmb),
            'tdee': round(tdee),
            'target_calories': int(target_calories)
        }).execute()
        
        # Registrar peso inicial
        supabase.table('weight_history').insert({
            'user_id': user_id,
            'weight_kg': onboarding_data.current_weight,
            'week_number': week_number
        }).execute()
        
        # Generar token
        token = generate_token(user_id, email)
        
        return jsonify({
            'user_id': user_id,
            'tmb': round(tmb),
            'tdee': round(tdee),
            'target_calories': int(target_calories),
            'token': token,
            'profile': {
                'age': onboarding_data.age,
                'gender': onboarding_data.gender,
                'height': onboarding_data.height,
                'current_weight': onboarding_data.current_weight,
                'goal_weight': onboarding_data.goal_weight,
                'goal_type': onboarding_data.goal_type,
                'activity_level': onboarding_data.activity_level,
                'meals_per_day': onboarding_data.meals_per_day
            }
        }), 201
        
    except Exception as e:
        return jsonify({'error': f'Error interno: {str(e)}'}), 500

# 2. GET /api/profile - Perfil usuario
@app.route('/api/profile', methods=['GET'])
@token_required
def get_profile():
    """Obtiene perfil completo del usuario autenticado."""
    try:
        user_id = request.current_user['user_id']
        
        profile_result = supabase.table('user_profiles').select('*').eq('user_id', user_id).execute()
        if not profile_result.data:
            return jsonify({'error': 'Perfil no encontrado'}), 404
        
        profile = profile_result.data[0]
        
        # Recalcular valores actuales
        tmb = calculate_tmb(
            profile['age'],
            profile['gender'],
            profile['height_cm'],
            profile['weight_kg']
        )
        tdee = calculate_tdee(tmb, profile['activity_level'])
        target_calories = calculate_target_calories(
            tdee,
            profile['goal'],
            profile['weight_kg'],
            profile['target_weight_kg']
        )
        
        return jsonify({
            'user_id': user_id,
            'age': profile['age'],
            'gender': profile['gender'],
            'height': profile['height_cm'],
            'current_weight': profile['weight_kg'],
            'goal_weight': profile['target_weight_kg'],
            'goal_type': profile['goal'],
            'activity_level': profile['activity_level'],
            'meals_per_day': profile['meals_per_day'],
            'allergies': profile.get('allergies', ''),
            'disliked_foods': profile.get('disliked_foods', ''),
            'tmb': round(tmb),
            'tdee': round(tdee),
            'target_calories': int(target_calories)
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Error interno: {str(e)}'}), 500

# 3. POST /api/profile - Actualiza perfil
@app.route('/api/profile', methods=['POST'])
@token_required
def update_profile():
    """Actualiza perfil del usuario y recalcula TMB/TDEE si es necesario."""
    try:
        user_id = request.current_user['user_id']
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'JSON requerido'}), 400
        
        # Validar con pydantic
        try:
            update_data = ProfileUpdateRequest(**data)
        except Exception as e:
            return jsonify({'error': f'Datos inválidos: {str(e)}'}), 400
        
        # Obtener perfil actual
        current = supabase.table('user_profiles').select('*').eq('user_id', user_id).execute()
        if not current.data:
            return jsonify({'error': 'Perfil no encontrado'}), 404
        
        profile = current.data[0]
        
        # Preparar actualización
        update_fields = {}
        recalc_fields = ['current_weight', 'activity_level', 'goal_weight', 'goal_type', 'age', 'height', 'gender']
        needs_recalc = False
        
        for field, value in update_data.dict(exclude_none=True).items():
            if field == 'current_weight':
                update_fields['weight_kg'] = value
            elif field == 'height':
                update_fields['height_cm'] = value
            elif field == 'goal_weight':
                update_fields['target_weight_kg'] = value
            elif field == 'preferences':
                # Convertir lista a string para almacenar
                update_fields['preferences'] = ','.join(value) if value else ''
            else:
                update_fields[field] = value
            
            if field in recalc_fields:
                needs_recalc = True
        
        # Guardar target_calories si viene del frontend
        if 'target_calories' in data:
            update_fields['target_calories'] = data['target_calories']
        
        if update_fields:
            update_fields['user_id'] = user_id
            supabase.table('user_profiles').upsert(update_fields).execute()
        
        # Recalcular si es necesario
        if needs_recalc:
            updated = supabase.table('user_profiles').select('*').eq('user_id', user_id).execute().data[0]
            tmb = calculate_tmb(updated['age'], updated['gender'], updated['height_cm'], updated['weight_kg'])
            tdee = calculate_tdee(tmb, updated['activity_level'])
            target = calculate_target_calories(tdee, updated['goal'], updated['weight_kg'], updated['target_weight_kg'])
            
            return jsonify({
                'message': 'Perfil actualizado',
                'recalculated': True,
                'tmb': round(tmb),
                'tdee': round(tdee),
                'target_calories': int(target)
            }), 200
        
        return jsonify({'message': 'Perfil actualizado', 'recalculated': False}), 200
        
    except Exception as e:
        return jsonify({'error': f'Error interno: {str(e)}'}), 500

# 4. GET /api/recipes - Lista recetas con filtros
@app.route('/api/recipes', methods=['GET'])
def get_recipes():
    """Obtiene lista de recetas con filtros opcionales."""
    try:
        meal_type = request.args.get('meal_type')
        limit = request.args.get('limit', default=50, type=int)
        min_calories = request.args.get('min_calories', type=float)
        max_calories = request.args.get('max_calories', type=float)
        
        query = supabase.table('master_recipes').select('*')
        
        if meal_type:
            query = query.eq('meal_type', meal_type)
        if min_calories is not None:
            query = query.gte('calories', min_calories)
        if max_calories is not None:
            query = query.lte('calories', max_calories)
        
        query = query.limit(limit)
        result = query.execute()
        
        return jsonify({
            'recipes': result.data if result.data else [],
            'count': len(result.data) if result.data else 0
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Error interno: {str(e)}'}), 500

# 5. GET /api/plan - Plan semanal usuario
@app.route('/api/plan', methods=['GET'])
@token_required
def get_plan():
    """Obtiene plan semanal del usuario autenticado."""
    try:
        user_id = request.current_user['user_id']
        week_number = request.args.get('week', default=datetime.now().isocalendar()[1], type=int)
        
        plan_result = supabase.table('weekly_plans').select('*').eq('user_id', user_id).eq('week_number', week_number).order('day_of_week').execute()
        
        # Agrupar por día
        days = {}
        for entry in (plan_result.data or []):
            day = entry['day_of_week']
            if day not in days:
                days[day] = []
            days[day].append(entry)
        
        # Obtener detalles de recetas
        recipe_ids = set(entry['selected_recipe_id'] for entry in (plan_result.data or []))
        if recipe_ids:
            recipes_result = supabase.table('master_recipes').select('id, name, image_url').in_('id', list(recipe_ids)).execute()
            recipes_dict = {r['id']: r for r in (recipes_result.data or [])}
        else:
            recipes_dict = {}
        
        return jsonify({
            'week_number': week_number,
            'days': days,
            'plan_entries': plan_result.data or [],
            'recipes_info': recipes_dict
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Error interno: {str(e)}'}), 500

# 6. POST /api/plan/swap - Cambia comida del plan
@app.route('/api/plan/swap', methods=['POST'])
@token_required
def swap_plan_meal():
    """Cambia una comida del plan por otra receta."""
    try:
        user_id = request.current_user['user_id']
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'JSON requerido'}), 400
        
        try:
            swap_data = PlanSwapRequest(**data)
        except Exception as e:
            return jsonify({'error': f'Datos inválidos: {str(e)}'}), 400
        
        # Verificar que el plan pertenece al usuario
        plan_result = supabase.table('weekly_plans').select('*').eq('id', swap_data.plan_id).eq('user_id', user_id).execute()
        if not plan_result.data:
            return jsonify({'error': 'Plan no encontrado'}), 404
        
        # Obtener datos de la nueva receta
        recipe_result = supabase.table('master_recipes').select('*').eq('id', swap_data.new_recipe_id).execute()
        if not recipe_result.data:
            return jsonify({'error': 'Receta no encontrada'}), 404
        
        recipe = recipe_result.data[0]
        
        # Actualizar plan
        supabase.table('weekly_plans').update({
            'selected_recipe_id': swap_data.new_recipe_id,
            'calories': recipe['calories'],
            'protein': recipe['protein'],
            'carbs': recipe['carbs'],
            'fat': recipe['fat']
        }).eq('id', swap_data.plan_id).execute()
        
        return jsonify({
            'message': 'Comida actualizada',
            'new_calories': recipe['calories'],
            'new_protein': recipe['protein'],
            'new_carbs': recipe['carbs'],
            'new_fat': recipe['fat']
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Error interno: {str(e)}'}), 500

# 7. GET /api/shopping-list - Lista de compra
@app.route('/api/shopping-list', methods=['GET'])
@token_required
def get_shopping_list():
    """Genera lista de compra basada en el plan semanal."""
    try:
        user_id = request.current_user['user_id']
        week_number = request.args.get('week', default=datetime.now().isocalendar()[1], type=int)
        
        # Obtener plan de la semana
        plan_result = supabase.table('weekly_plans').select('selected_recipe_id').eq('user_id', user_id).eq('week_number', week_number).execute()
        
        if not plan_result.data:
            return jsonify({'ingredients': [], 'message': 'No hay plan para esta semana'}), 200
        
        recipe_ids = list(set(entry['selected_recipe_id'] for entry in plan_result.data))
        
        # Obtener recetas con ingredientes
        recipes_result = supabase.table('master_recipes').select('id, name, ingredients').in_('id', recipe_ids).execute()
        
        # Agrupar ingredientes
        ingredients = {}
        for recipe in (recipes_result.data or []):
            recipe_ingredients = recipe.get('ingredients', '')
            if recipe_ingredients:
                for ingredient in recipe_ingredients.split(','):
                    ingredient = ingredient.strip()
                    if ingredient:
                        ingredients[ingredient.lower()] = ingredient
        
        return jsonify({
            'week_number': week_number,
            'ingredients': list(ingredients.values()),
            'recipe_count': len(recipe_ids)
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Error interno: {str(e)}'}), 500

# 8. POST /api/weight - Registra peso
@app.route('/api/weight', methods=['POST'])
@token_required
def register_weight():
    """Registra nuevo peso del usuario."""
    try:
        user_id = request.current_user['user_id']
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'JSON requerido'}), 400
        
        try:
            weight_data = WeightRequest(**data)
        except Exception as e:
            return jsonify({'error': f'Datos inválidos: {str(e)}'}), 400
        
        week_number = datetime.now().isocalendar()[1]
        
        # Registrar peso
        supabase.table('weight_history').insert({
            'user_id': user_id,
            'weight_kg': weight_data.weight,
            'week_number': week_number
        }).execute()
        
        # Actualizar peso en perfil
        supabase.table('user_profiles').update({
            'weight_kg': weight_data.weight
        }).eq('user_id', user_id).execute()
        
        # Recalcular calorías objetivo
        profile_result = supabase.table('user_profiles').select('*').eq('user_id', user_id).execute()
        if profile_result.data:
            profile = profile_result.data[0]
            tmb = calculate_tmb(profile['age'], profile['gender'], profile['height_cm'], weight_data.weight)
            tdee = calculate_tdee(tmb, profile['activity_level'])
            target = calculate_target_calories(tdee, profile['goal'], weight_data.weight, profile['target_weight_kg'])
            
            return jsonify({
                'message': 'Peso registrado',
                'weight': weight_data.weight,
                'new_tmb': round(tmb),
                'new_tdee': round(tdee),
                'new_target_calories': int(target)
            }), 200
        
        return jsonify({'message': 'Peso registrado', 'weight': weight_data.weight}), 200
        
    except Exception as e:
        return jsonify({'error': f'Error interno: {str(e)}'}), 500

# 9. GET /api/stats - Estadísticas/progreso
@app.route('/api/stats', methods=['GET'])
@token_required
def get_stats():
    """Obtiene estadísticas y progreso del usuario."""
    try:
        user_id = request.current_user['user_id']
        
        # Historial de peso (últimas 12 semanas)
        weight_result = supabase.table('weight_history').select('weight_kg, week_number, created_at').eq('user_id', user_id).order('week_number', desc=True).limit(12).execute()
        weight_history = weight_result.data or []
        
        # Perfil actual
        profile_result = supabase.table('user_profiles').select('*').eq('user_id', user_id).execute()
        if not profile_result.data:
            return jsonify({'error': 'Perfil no encontrado'}), 404
        
        profile = profile_result.data[0]
        
        # Calcular progreso
        start_weight = weight_history[-1]['weight_kg'] if weight_history else profile['weight_kg']
        current_weight = profile['weight_kg']
        weight_change = current_weight - start_weight
        goal_progress = ((start_weight - current_weight) / (start_weight - profile['target_weight_kg']) * 100) if start_weight != profile['target_weight_kg'] else 0
        
        # Food log de esta semana
        week_number = datetime.now().isocalendar()[1]
        log_result = supabase.table('food_logs').select('calories, protein, carbs, fat').eq('user_id', user_id).gte('week_number', week_number).execute()
        logs = log_result.data or []
        
        total_calories = sum(log['calories'] or 0 for log in logs)
        avg_daily_calories = total_calories / 7 if logs else 0
        
        return jsonify({
            'current_weight': current_weight,
            'goal_weight': profile['target_weight_kg'],
            'weight_change': round(weight_change, 2),
            'goal_progress_percent': round(max(0, min(100, goal_progress)), 1),
            'weight_history': weight_history,
            'weekly_stats': {
                'total_calories': total_calories,
                'avg_daily_calories': round(avg_daily_calories, 0),
                'logs_count': len(logs)
            },
            'tmb': profile.get('tmb', 0),
            'tdee': profile.get('tdee', 0),
            'target_calories': profile.get('target_calories', 0)
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Error interno: {str(e)}'}), 500

# 10. POST /api/food-log - Registra comida del día
@app.route('/api/food-log', methods=['POST'])
@token_required
def log_food():
    """Registra comida consumida en el día."""
    try:
        user_id = request.current_user['user_id']
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'JSON requerido'}), 400
        
        try:
            log_data = FoodLogRequest(**data)
        except Exception as e:
            return jsonify({'error': f'Datos inválidos: {str(e)}'}), 400
        
        week_number = datetime.now().isocalendar()[1]
        day_of_week = datetime.now().weekday()
        
        # Registrar food log
        result = supabase.table('food_logs').insert({
            'user_id': user_id,
            'recipe_id': log_data.recipe_id,
            'meal_type': log_data.meal_type,
            'calories': log_data.calories,
            'protein': log_data.protein,
            'carbs': log_data.carbs,
            'fat': log_data.fat,
            'notes': log_data.notes or '',
            'week_number': week_number,
            'day_of_week': day_of_week,
            'logged_at': datetime.now().isoformat()
        }).execute()
        
        return jsonify({
            'message': 'Comida registrada',
            'log_id': result.data[0]['id'] if result.data else None,
            'calories': log_data.calories,
            'protein': log_data.protein,
            'carbs': log_data.carbs,
            'fat': log_data.fat
        }), 201
        
    except Exception as e:
        return jsonify({'error': f'Error interno: {str(e)}'}), 500

# 11. GET /api/dashboard - Dashboard completo
@app.route('/api/dashboard', methods=['GET'])
@token_required
def get_dashboard():
    """Obtiene dashboard completo con toda la información del usuario."""
    try:
        user_id = request.current_user['user_id']
        
        # Perfil
        profile_result = supabase.table('user_profiles').select('*').eq('user_id', user_id).execute()
        if not profile_result.data:
            return jsonify({'error': 'Perfil no encontrado'}), 404
        
        profile = profile_result.data[0]
        
        # Plan actual
        week_number = datetime.now().isocalendar()[1]
        plan_result = supabase.table('weekly_plans').select('*').eq('user_id', user_id).eq('week_number', week_number).execute()
        plan_entries = plan_result.data or []
        
        # Food log de hoy
        today_logs = supabase.table('food_logs').select('calories, protein, carbs, fat').eq('user_id', user_id).eq('week_number', week_number).eq('day_of_week', datetime.now().weekday()).execute()
        today_calories = sum(log['calories'] or 0 for log in (today_logs.data or []))
        today_protein = sum(log['protein'] or 0 for log in (today_logs.data or []))
        today_carbs = sum(log['carbs'] or 0 for log in (today_logs.data or []))
        today_fat = sum(log['fat'] or 0 for log in (today_logs.data or []))
        
        # Último peso
        weight_result = supabase.table('weight_history').select('weight_kg, created_at').eq('user_id', user_id).order('created_at', desc=True).limit(1).execute()
        last_weight = (weight_result.data or [{}])[0].get('weight_kg', profile['weight_kg'])
        
        # Progreso
        all_weights = supabase.table('weight_history').select('weight_kg').eq('user_id', user_id).order('created_at').execute()
        start_weight = (all_weights.data or [{}])[0].get('weight_kg', last_weight)
        weight_change = last_weight - start_weight
        
        return jsonify({
            'profile': {
                'age': profile['age'],
                'gender': profile['gender'],
                'goal_type': profile['goal'],
                'activity_level': profile['activity_level'],
                'meals_per_day': profile['meals_per_day']
            },
            'metrics': {
                'tmb': profile.get('tmb', 0),
                'tdee': profile.get('tdee', 0),
                'target_calories': profile.get('target_calories', 0),
                'current_weight': last_weight,
                'goal_weight': profile['target_weight_kg'],
                'weight_change': round(weight_change, 2)
            },
            'today': {
                'calories': today_calories,
                'protein': today_protein,
                'carbs': today_carbs,
                'fat': today_fat,
                'calories_remaining': max(0, profile.get('target_calories', 2000) - today_calories),
                'logs_count': len(today_logs.data or [])
            },
            'plan': {
                'week_number': week_number,
                'entries_count': len(plan_entries),
                'entries': plan_entries[:7]  # Primeros 7 para no sobrecargar
            },
            'quick_stats': {
                'adherence_percent': round((today_calories / profile.get('target_calories', 2000)) * 100, 1) if today_calories > 0 else 0,
                'days_logged': len(set((log.get('day_of_week', 0)) for log in (today_logs.data or [])))
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Error interno: {str(e)}'}), 500

# ==================== AUTH ENDPOINTS (registro/login) ====================

@app.route('/api/register', methods=['POST'])
def register():
    """Registro tradicional con email/password."""
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        
        if not all([name, email, password]):
            return jsonify({'error': 'Todos los campos son requeridos'}), 400
        
        existing = supabase.table('users').select('id').eq('email', email).execute()
        if existing.data and len(existing.data) > 0:
            return jsonify({'error': 'El email ya está registrado'}), 400
        
        hashed = hash_password(password)
        result = supabase.table('users').insert({
            'name': name, 
            'email': email,
            'password_hash': hashed['hash'],
            'salt': hashed['salt']
        }).execute()
        
        if result.data:
            user = result.data[0]
            token = generate_token(user['id'], email)
            return jsonify({
                'user': {'id': user['id'], 'name': user['name'], 'email': user['email']},
                'token': token
            }), 201
        return jsonify({'error': 'Error al crear usuario'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/login', methods=['POST'])
def login():
    """Login con email/password."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'JSON requerido'}), 400
        
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        
        if not email or not password:
            return jsonify({'error': 'Email y contraseña requeridos'}), 400
        
        result = supabase.table('users').select('*').eq('email', email).execute()
        if not result.data or len(result.data) == 0:
            return jsonify({'error': 'Usuario no encontrado'}), 401
        
        user = result.data[0]
        password_hash = user.get('password_hash', '')
        salt = user.get('salt', '')
        
        # Compatibilidad: si no hay columna salt, usar formato hash:salt
        if salt:
            stored_hash = password_hash
        elif ':' in password_hash:
            stored_hash, salt = password_hash.split(':', 1)
        else:
            return jsonify({'error': 'Formato de contraseña inválido'}), 500
        
        if not verify_password(password, stored_hash, salt):
            return jsonify({'error': 'Contraseña incorrecta'}), 401
        
        token = generate_token(user['id'], email)
        return jsonify({
            'user': {'id': user['id'], 'name': user['name'], 'email': user['email']},
            'token': token
        }), 200
    except Exception as e:
        return jsonify({'error': f'Error al iniciar sesión: {str(e)}'}), 500

@app.route('/api/recover-password', methods=['POST'])
def recover_password():
    """Solicita recuperación de contraseña por email."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'JSON requerido'}), 400
        
        email = data.get('email', '').strip().lower()
        if not email:
            return jsonify({'error': 'Email requerido'}), 400
        
        # Verificar que el usuario existe
        result = supabase.table('users').select('id, email, name').eq('email', email).execute()
        if not result.data or len(result.data) == 0:
            # Por seguridad, no revelamos si el email existe o no
            return jsonify({'message': 'Si el email está registrado, recibirás instrucciones'}), 200
        
        user = result.data[0]
        
        # Generar token de recuperación (válido por 1 hora)
        reset_token = generate_token(user['id'], email)
        reset_payload = {
            'user_id': user['id'],
            'email': email,
            'type': 'password_reset',
            'exp': datetime.utcnow() + timedelta(hours=1),
            'iat': datetime.utcnow()
        }
        reset_token = jwt.encode(reset_payload, JWT_SECRET, algorithm='HS256')
        
        # En producción: enviar email con enlace de recuperación
        # reset_link = f"https://diet-tracker-app-chi.vercel.app/reset-password?token={reset_token}"
        # TODO: Integrar con servicio de email (SendGrid, Resend, etc.)
        
        # Por ahora, devolvemos el token para testing (solo en desarrollo)
        return jsonify({
            'message': 'Si el email está registrado, recibirás instrucciones',
            'reset_token': reset_token,  # Remover en producción
            'user_email': email  # Remover en producción
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Error al procesar recuperación: {str(e)}'}), 500

@app.route('/api/reset-password', methods=['POST'])
def reset_password():
    """Resetea contraseña con token válido."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'JSON requerido'}), 400
        
        token = data.get('token', '')
        new_password = data.get('password', '')
        
        if not token or not new_password:
            return jsonify({'error': 'Token y nueva contraseña requeridos'}), 400
        
        if len(new_password) < 6:
            return jsonify({'error': 'La contraseña debe tener al menos 6 caracteres'}), 400
        
        # Verificar token
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
            if payload.get('type') != 'password_reset':
                return jsonify({'error': 'Token inválido'}), 400
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token expirado'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Token inválido'}), 401
        
        user_id = payload['user_id']
        
        # Hashear nueva contraseña
        hashed = hash_password(new_password)
        
        # Actualizar en DB
        result = supabase.table('users').update({
            'password_hash': f"{hashed['hash']}:{hashed['salt']}"
        }).eq('id', user_id).execute()
        
        if not result.data:
            return jsonify({'error': 'Error al actualizar contraseña'}), 500
        
        return jsonify({'message': 'Contraseña actualizada correctamente'}), 200
        
    except Exception as e:
        return jsonify({'error': f'Error al resetear contraseña: {str(e)}'}), 500

# 12. POST /api/generate-plan - Genera plan semanal automático
@app.route('/api/generate-plan', methods=['POST'])
@token_required
def generate_plan():
    """
    Genera un plan semanal de comidas automático basado en preferencias y calorías objetivo.
    
    Input (opcional):
        - user_id: Si no se proporciona, usa el del token
        - target_calories: Si no se proporciona, usa el del perfil
        - preferences: Override de preferencias (allergies, disliked_foods)
    
    Output:
        - Plan semanal completo (7 días x N comidas)
        - Macros objetivo distribuidas
        - IDs de recetas seleccionadas
    """
    try:
        user_id = request.current_user['user_id']
        data = request.get_json() or {}
        
        # Validate input if provided
        try:
            request_data = GeneratePlanRequest(**data) if data else GeneratePlanRequest()
        except Exception as e:
            return jsonify({'error': f'Datos inválidos: {str(e)}'}), 400
        
        # Override user_id if provided (for admin use)
        effective_user_id = request_data.user_id or user_id
        
        # Get user profile
        profile_result = supabase.table('user_profiles').select('*').eq('user_id', effective_user_id).execute()
        if not profile_result.data:
            return jsonify({'error': 'Perfil no encontrado. Completa el onboarding primero.'}), 404
        
        profile = profile_result.data[0]
        
        # Get target calories
        target_calories = request_data.target_calories or profile.get('target_calories', 2000)
        
        # Override preferences if provided
        if request_data.preferences:
            profile['allergies'] = request_data.preferences.get('allergies', profile.get('allergies', ''))
            profile['disliked_foods'] = request_data.preferences.get('disliked_foods', profile.get('disliked_foods', ''))
            profile['goal'] = request_data.preferences.get('goal_type', profile.get('goal', 'maintain'))
        
        # Generate the weekly plan
        plan = generate_weekly_plan(supabase, effective_user_id, profile, target_calories)
        
        # Calculate daily totals for verification
        meals_per_day = profile.get('meals_per_day', 4)
        meal_types = get_meal_types_for_count(meals_per_day)
        
        daily_totals = {
            'calories': sum(m.get('calories', 0) for m in plan['days'].get('lunes', [])),
            'protein': sum(m.get('protein', 0) for m in plan['days'].get('lunes', [])),
            'carbs': sum(m.get('carbs', 0) for m in plan['days'].get('lunes', [])),
            'fat': sum(m.get('fat', 0) for m in plan['days'].get('lunes', []))
        }
        
        return jsonify({
            'success': True,
            'message': 'Plan semanal generado correctamente',
            'user_id': effective_user_id,
            'week_number': plan['week_number'],
            'target_calories': target_calories,
            'macros_target': plan['macros_target'],
            'meal_distribution': plan['meal_calories'],
            'days': plan['days'],
            'summary': {
                'total_entries': plan['total_entries'],
                'meals_per_day': meals_per_day,
                'estimated_daily_calories': daily_totals['calories'],
                'estimated_daily_macros': {
                    'protein': daily_totals['protein'],
                    'carbs': daily_totals['carbs'],
                    'fat': daily_totals['fat']
                }
            }
        }), 201
        
    except Exception as e:
        return jsonify({'error': f'Error al generar plan: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
