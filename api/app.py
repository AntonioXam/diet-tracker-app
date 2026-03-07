"""
Diet Tracker API - Backend con Supabase
13 Endpoints principales con JWT auth y validación pydantic

Endpoints:
1. POST /api/onboarding - Registro y cálculo TMB/TDEE
2. GET /api/profile - Perfil del usuario
3. POST /api/profile - Actualizar perfil
4. GET /api/recipes - Lista de recetas
5. GET /api/plan - Plan semanal
6. POST /api/plan/swap - Cambiar comida del plan
7. GET /api/shopping-list - Lista de compra
8. POST /api/weight - Registrar peso
9. GET /api/stats - Estadísticas y progreso
10. POST /api/food-log - Registrar comida
11. GET /api/dashboard - Dashboard completo
12. GET /api/search-products - Buscar productos (Open Food Facts)
13. GET /api/products/:barcode - Producto por código de barras
"""
import os
import sys
import hashlib
import base64
import secrets
import time
import random
import logging
import jwt
import requests
import uuid
from datetime import datetime, timedelta
from functools import wraps
from flask import Flask, request, jsonify
from flask_cors import CORS
from supabase import create_client
from pydantic import BaseModel, Field
from typing import Optional, List

# ==================== LOGGING CONFIGURATION ====================
# Configure logging for debugging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(os.path.join(os.path.dirname(__file__), 'app.log'), mode='a')
    ]
)
logger = logging.getLogger(__name__)
logger.info("Starting Diet Tracker API...")

app = Flask(__name__)
CORS(app, origins=["*"], supports_credentials=True)

# Credenciales Supabase desde variables de entorno
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://kaomgwojvnncidyezdzj.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imthb21nd29qdm5uY2lkeWV6ZHpqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzI3MDcxNzYsImV4cCI6MjA4ODI4MzE3Nn0.Ds2ICxfiahuqt2n83dwoX9tMYGf7Xz8Jjvx6lFJc4zs")
JWT_SECRET = os.getenv("JWT_SECRET", secrets.token_hex(32))

# Initialize Supabase client with error handling
try:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    logger.info(f"Supabase client initialized successfully - URL: {SUPABASE_URL}")
except Exception as e:
    logger.error(f"Failed to initialize Supabase client: {e}")
    raise

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
    budget: Optional[str] = "medium"
    preferences: Optional[str] = ""  # Cambiado a string

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
    preferences: Optional[str] = None  # Cambiado a string
    target_calories: Optional[int] = Field(None, ge=1000, le=5000)

class WeightRequest(BaseModel):
    weight: float = Field(..., ge=30, le=300)

class FoodLogRequest(BaseModel):
    recipe_id: Optional[str] = None  # UUID - optional for manual entries
    food_name: Optional[str] = None  # For manual/Open Food Facts entries
    meal_type: str
    calories: float
    protein: float = 0
    carbs: float = 0
    fat: float = 0
    quantity: Optional[float] = 1.0  # Number of servings/units
    notes: Optional[str] = ""
    source: Optional[str] = "manual"  # 'plan', 'manual', 'openfoodfacts'
    barcode: Optional[str] = None  # For barcode-scanned products

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
    logger.debug(f"Selecting recipes for {meal_type}, target: {target_calories} cal, limit: {limit}")
    
    # Calorie range: +/- 20% of target
    min_cal = int(target_calories * 0.80)
    max_cal = int(target_calories * 1.20)
    
    try:
        # Base query for meal type
        query = supabase.table('master_recipes').select('*').eq('meal_type', meal_type)
        
        # Filter by calorie range
        query = query.gte('calories', min_cal).lte('calories', max_cal)
        
        # Execute query
        result = query.limit(limit * 2).execute()  # Get extra for filtering
        recipes = result.data or []
        logger.debug(f"Found {len(recipes)} recipes for {meal_type}")
        
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
        logger.debug(f"Returning {len(filtered[:limit])} filtered recipes for {meal_type}")
        return filtered[:limit] if filtered else recipes[:limit]
        
    except Exception as e:
        logger.error(f"Error selecting recipes for {meal_type}: {e}")
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
    logger.info("Health check requested")
    return jsonify({'status': 'ok', 'supabase_url': SUPABASE_URL})

# ==================== PRODUCT SEARCH (Open Food Facts) ====================

@app.route('/api/search-products', methods=['GET'])
def search_products():
    """
    Busca productos en Open Food Facts API.
    
    Parámetros:
        - query: Nombre del producto a buscar
        - barcode: Código de barras específico
        - supermarket: Filtrar por supermercado (mercadona/lidl/carrefour)
    
    Retorna productos con información nutricional.
    """
    try:
        query = request.args.get('query', '').strip()
        barcode = request.args.get('barcode', '').strip()
        supermarket = request.args.get('supermarket', '').strip().lower()
        
        # Si se proporciona barcode, buscar directamente
        if barcode:
            return search_by_barcode(barcode)
        
        # Si hay query, buscar por nombre
        if query:
            return search_by_name(query, supermarket)
        
        return jsonify({
            'products': [],
            'error': 'Proporciona un término de búsqueda (query) o código de barras (barcode)'
        }), 400
        
    except Exception as e:
        return jsonify({'error': f'Error al buscar productos: {str(e)}'}), 500


def search_by_barcode(barcode: str):
    """Busca un producto específico por su código de barras."""
    try:
        url = f"https://world.openfoodfacts.org/api/v2/product/{barcode}.json"
        response = requests.get(url, timeout=10)
        data = response.json()
        
        if data.get('status') == 1:
            product = data['product']
            nutriments = product.get('nutriments', {})
            
            return jsonify({
                'products': [{
                    'barcode': barcode,
                    'name': product.get('product_name', '') or product.get('product_name_es', ''),
                    'brands': product.get('brands', ''),
                    'categories': product.get('categories', ''),
                    'calories': nutriments.get('energy-kcal_100g', 0) or nutriments.get('energy-kcal', 0) / 10 if nutriments.get('energy-kcal') else 0,
                    'protein': nutriments.get('proteins_100g', 0),
                    'carbs': nutriments.get('carbohydrates_100g', 0),
                    'fat': nutriments.get('fat_100g', 0),
                    'fiber': nutriments.get('fiber_100g', 0),
                    'sugar': nutriments.get('sugars_100g', 0),
                    'sodium': nutriments.get('sodium_100g', 0),
                    'image_url': product.get('image_url', '') or product.get('image_front_url', ''),
                    'image_small': product.get('image_small_url', ''),
                    'quantity': product.get('quantity', ''),
                    'serving_size': product.get('serving_size', ''),
                    'ingredients': product.get('ingredients_text', ''),
                    'stores': product.get('stores', ''),
                    'countries': product.get('countries', ''),
                    'nutriscore': product.get('nutriscore_grade', ''),
                    'nova_group': product.get('nova_group', '')
                }],
                'count': 1,
                'source': 'open_food_facts'
            }), 200
        
        return jsonify({
            'products': [],
            'count': 0,
            'error': 'Producto no encontrado'
        }), 404
        
    except requests.Timeout:
        return jsonify({'error': 'Timeout al conectar con Open Food Facts'}), 504
    except requests.RequestException as e:
        return jsonify({'error': f'Error de conexión: {str(e)}'}), 502


def search_by_name(query: str, supermarket: str = ''):
    """Busca productos por nombre con filtros opcionales."""
    try:
        # Construir URL de búsqueda
        search_url = "https://world.openfoodfacts.org/api/v2/search"
        
        # Parámetros de búsqueda
        params = {
            'search_terms': query,
            'search_simple': '1',
            'action': 'process',
            'json': '1',
            'page_size': 20,
            'fields': 'code,product_name,brands,categories,nutriments,image_url,image_small_url,quantity,serving_size,ingredients_text,stores,countries,nutriscore_grade,nova_group'
        }
        
        # Filtrar por supermercado si se especifica
        if supermarket:
            supermarket_map = {
                'mercadona': 'Mercadona',
                'lidl': 'Lidl',
                'carrefour': 'Carrefour'
            }
            if supermarket in supermarket_map:
                params['stores_tags'] = supermarket_map[supermarket]
        
        response = requests.get(search_url, params=params, timeout=15)
        data = response.json()
        
        products = []
        for product in data.get('products', []):
            nutriments = product.get('nutriments', {})
            
            # Solo incluir productos con datos nutricionales
            if nutriments.get('energy-kcal_100g') or nutriments.get('energy-kcal'):
                products.append({
                    'barcode': product.get('code', ''),
                    'name': product.get('product_name', ''),
                    'brands': product.get('brands', ''),
                    'categories': product.get('categories', ''),
                    'calories': nutriments.get('energy-kcal_100g', 0) or (nutriments.get('energy-kcal', 0) / 10 if nutriments.get('energy-kcal') else 0),
                    'protein': nutriments.get('proteins_100g', 0),
                    'carbs': nutriments.get('carbohydrates_100g', 0),
                    'fat': nutriments.get('fat_100g', 0),
                    'fiber': nutriments.get('fiber_100g', 0),
                    'sugar': nutriments.get('sugars_100g', 0),
                    'image_url': product.get('image_url', ''),
                    'image_small': product.get('image_small_url', ''),
                    'quantity': product.get('quantity', ''),
                    'stores': product.get('stores', ''),
                    'nutriscore': product.get('nutriscore_grade', '')
                })
        
        return jsonify({
            'products': products,
            'count': len(products),
            'query': query,
            'supermarket': supermarket if supermarket else 'all',
            'source': 'open_food_facts'
        }), 200
        
    except requests.Timeout:
        return jsonify({'error': 'Timeout al conectar con Open Food Facts'}), 504
    except requests.RequestException as e:
        return jsonify({'error': f'Error de conexión: {str(e)}'}), 502


@app.route('/api/products/<barcode>', methods=['GET'])
def get_product_by_barcode(barcode: str):
    """
    Obtiene información nutricional completa de un producto por código de barras.
    
    Parámetros:
        - barcode: Código de barras del producto (EAN)
    
    Retorna información nutricional detallada.
    """
    try:
        url = f"https://world.openfoodfacts.org/api/v2/product/{barcode}.json"
        response = requests.get(url, timeout=10)
        data = response.json()
        
        if data.get('status') != 1:
            return jsonify({
                'error': 'Producto no encontrado',
                'barcode': barcode
            }), 404
        
        product = data['product']
        nutriments = product.get('nutriments', {})
        
        return jsonify({
            'barcode': barcode,
            'name': product.get('product_name', '') or product.get('product_name_es', ''),
            'name_en': product.get('product_name_en', ''),
            'brands': product.get('brands', ''),
            'brand_owner': product.get('brand_owner', ''),
            'categories': product.get('categories', ''),
            'categories_tags': product.get('categories_tags', []),
            
            # Información nutricional por 100g
            'nutrition_per_100g': {
                'calories': nutriments.get('energy-kcal_100g', 0),
                'energy_kj': nutriments.get('energy-kj_100g', 0),
                'protein': nutriments.get('proteins_100g', 0),
                'carbs': nutriments.get('carbohydrates_100g', 0),
                'fat': nutriments.get('fat_100g', 0),
                'fiber': nutriments.get('fiber_100g', 0),
                'sugar': nutriments.get('sugars_100g', 0),
                'saturated_fat': nutriments.get('saturated-fat_100g', 0),
                'sodium': nutriments.get('sodium_100g', 0),
                'salt': nutriments.get('salt_100g', 0),
                'cholesterol': nutriments.get('cholesterol_100g', 0),
                'trans_fat': nutriments.get('trans-fat_100g', 0)
            },
            
            # Información por porción
            'nutrition_per_serving': {
                'calories': nutriments.get('energy-kcal_serving', 0),
                'protein': nutriments.get('proteins_serving', 0),
                'carbs': nutriments.get('carbohydrates_serving', 0),
                'fat': nutriments.get('fat_serving', 0),
                'serving_size': product.get('serving_size', '')
            },
            
            # Información del producto
            'images': {
                'front': product.get('image_url', ''),
                'front_small': product.get('image_small_url', ''),
                'ingredients': product.get('image_ingredients_url', ''),
                'nutrition': product.get('image_nutrition_url', '')
            },
            
            'quantity': product.get('quantity', ''),
            'serving_size': product.get('serving_size', ''),
            'ingredients': product.get('ingredients_text', ''),
            'ingredients_list': product.get('ingredients', []),
            'allergens': product.get('allergens', ''),
            'allergens_tags': product.get('allergens_tags', []),
            'traces': product.get('traces', ''),
            
            # Scores de calidad
            'scores': {
                'nutriscore': product.get('nutriscore_grade', ''),
                'nutriscore_score': product.get('nutriscore_score', 0),
                'nova_group': product.get('nova_group', 0),
                'eco_score': product.get('ecoscore_grade', ''),
                'eco_score_score': product.get('ecoscore_score', 0)
            },
            
            # Disponibilidad
            'stores': product.get('stores', ''),
            'countries': product.get('countries', ''),
            
            # Metadata
            'source': 'open_food_facts',
            'last_modified': product.get('last_modified_t', 0)
        }), 200
        
    except requests.Timeout:
        return jsonify({'error': 'Timeout al conectar con Open Food Facts'}), 504
    except requests.RequestException as e:
        return jsonify({'error': f'Error de conexión: {str(e)}'}), 502
    except Exception as e:
        return jsonify({'error': f'Error al obtener producto: {str(e)}'}), 500


# 1. POST /api/onboarding - Calcula TMB (Mifflin-St Jeor) + TDEE
@app.route('/api/onboarding', methods=['POST'])
@token_required
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
        
        # Obtener user_id y email del token
        user_id = request.current_user['user_id']
        email = request.current_user.get('email', f'user_{user_id[:8]}@diettracker.app')
        
        # Verificar si el usuario ya tiene perfil
        existing_profile = supabase.table('user_profiles').select('*').eq('user_id', user_id).execute()
        
        if existing_profile.data and len(existing_profile.data) > 0:
            # Actualizar perfil existente
            profile_result = supabase.table('user_profiles').update({
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
                'target_calories': int(target_calories),
                'onboarding_completed': True
            }).eq('user_id', user_id).execute()
        else:
            # Crear perfil nuevo
            profile_id = str(uuid.uuid4())
            profile_result = supabase.table('user_profiles').insert({
                'id': profile_id,
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
                'target_calories': int(target_calories),
                'onboarding_completed': True
            }).execute()
        
        if not profile_result.data:
            return jsonify({'error': 'Error al guardar perfil'}), 500
        
        # Registrar peso inicial
        week_number = datetime.now().isocalendar()[1]
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
                # Ya es string, guardar directamente
                update_fields['preferences'] = value if value else ''
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
    """Genera lista de compra basada en el plan semanal con cantidades y supermercados."""
    try:
        user_id = request.current_user['user_id']
        week_number = request.args.get('week', default=datetime.now().isocalendar()[1], type=int)
        
        # Obtener plan de la semana con recetas
        plan_result = supabase.table('weekly_plans').select('*').eq('user_id', user_id).eq('week_number', week_number).execute()
        
        if not plan_result.data:
            return jsonify({
                'week_number': week_number,
                'ingredients': [],
                'grouped': {},
                'message': 'No hay plan para esta semana. Genera un plan primero.'
            }), 200
        
        # Obtener IDs únicos de recetas
        recipe_ids = list(set(entry.get('selected_recipe_id') for entry in plan_result.data if entry.get('selected_recipe_id')))
        
        if not recipe_ids:
            return jsonify({
                'week_number': week_number,
                'ingredients': [],
                'grouped': {},
                'message': 'No hay recetas en el plan'
            }), 200
        
        # Obtener recetas con ingredientes completos
        recipes_result = supabase.table('master_recipes').select('id, name, ingredients, supermarket').in_('id', recipe_ids).execute()
        recipes_dict = {r['id']: r for r in (recipes_result.data or [])}
        
        # Agrupar ingredientes por nombre y supermercado
        ingredients = {}
        for entry in plan_result.data:
            recipe_id = entry.get('selected_recipe_id')
            if not recipe_id:
                continue
            
            recipe = recipes_dict.get(recipe_id, {})
            recipe_ingredients = recipe.get('ingredients', [])
            supermarket = recipe.get('supermarket', 'generic') or 'generic'
            
            # Los ingredientes pueden ser string (formato antiguo) o lista (formato nuevo)
            if isinstance(recipe_ingredients, str):
                # Formato antiguo: string separado por comas
                ing_list = [i.strip() for i in recipe_ingredients.split(',') if i.strip()]
                for ing in ing_list:
                    name = ing.lower()
                    if name not in ingredients:
                        ingredients[name] = {
                            'name': ing,
                            'amount': 1,
                            'unit': 'unidad',
                            'supermarket': supermarket,
                            'recipes': [recipe.get('name', 'Receta')]
                        }
                    else:
                        ingredients[name]['amount'] += 1
                        if recipe.get('name') and recipe.get('name') not in ingredients[name]['recipes']:
                            ingredients[name]['recipes'].append(recipe.get('name'))
            elif isinstance(recipe_ingredients, list):
                # Formato nuevo: lista de objetos con cantidad y unidad
                for ing in recipe_ingredients:
                    if isinstance(ing, dict):
                        name = ing.get('name', '').lower()
                        if not name:
                            continue
                        
                        if name not in ingredients:
                            ingredients[name] = {
                                'name': ing.get('name', ''),
                                'amount': ing.get('amount', 1),
                                'unit': ing.get('unit', 'unidad'),
                                'supermarket': supermarket,
                                'recipes': [recipe.get('name', 'Receta')]
                            }
                        else:
                            ingredients[name]['amount'] += ing.get('amount', 1)
                            if recipe.get('name') and recipe.get('name') not in ingredients[name]['recipes']:
                                ingredients[name]['recipes'].append(recipe.get('name'))
                    elif isinstance(ing, str):
                        # Formato mixto: string dentro de lista
                        name = ing.lower()
                        if name not in ingredients:
                            ingredients[name] = {
                                'name': ing,
                                'amount': 1,
                                'unit': 'unidad',
                                'supermarket': supermarket,
                                'recipes': [recipe.get('name', 'Receta')]
                            }
                        else:
                            ingredients[name]['amount'] += 1
                            if recipe.get('name') and recipe.get('name') not in ingredients[name]['recipes']:
                                ingredients[name]['recipes'].append(recipe.get('name'))
        
        # Obtener items manuales de la lista de compras
        manual_items = supabase.table('shopping_lists').select('*').eq('user_id', user_id).execute()
        
        for item in (manual_items.data or []):
            name = item.get('ingredient', '').lower()
            if name and name not in ingredients:
                ingredients[name] = {
                    'name': item.get('ingredient', ''),
                    'amount': item.get('quantity') or 1,
                    'unit': item.get('unit') or 'unidad',
                    'supermarket': 'manual',
                    'checked': item.get('checked', False),
                    'id': item.get('id'),
                    'recipes': []
                }
        
        # Agrupar por supermercado
        grouped = {
            'mercadona': [],
            'lidl': [],
            'carrefour': [],
            'generic': [],
            'manual': []
        }
        
        for ing in ingredients.values():
            supermarket = ing.get('supermarket', 'generic')
            if supermarket in grouped:
                grouped[supermarket].append(ing)
            else:
                grouped['generic'].append(ing)
        
        return jsonify({
            'week_number': week_number,
            'ingredients': list(ingredients.values()),
            'grouped': grouped,
            'recipe_count': len(recipe_ids),
            'total_items': len(ingredients)
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Error interno: {str(e)}'}), 500


# 7.1 POST /api/shopping-list/item - Añadir item manual
@app.route('/api/shopping-list/item', methods=['POST'])
@token_required
def add_shopping_item():
    """Añade un item manual a la lista de compras."""
    try:
        user_id = request.current_user['user_id']
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'JSON requerido'}), 400
        
        name = data.get('name') or data.get('ingredient')
        amount = data.get('amount') or data.get('quantity', 1)
        unit = data.get('unit', 'unidad')
        supermarket = data.get('supermarket', 'manual')
        
        if not name:
            return jsonify({'error': 'Nombre del ingrediente requerido'}), 400
        
        # Insertar en shopping_lists
        result = supabase.table('shopping_lists').insert({
            'user_id': user_id,
            'ingredient': name,
            'quantity': str(amount),
            'unit': unit,
            'checked': False
        }).execute()
        
        if result.data:
            return jsonify({
                'message': 'Item añadido',
                'item': {
                    'id': result.data[0]['id'],
                    'name': name,
                    'amount': amount,
                    'unit': unit,
                    'supermarket': supermarket,
                    'checked': False
                }
            }), 201
        
        return jsonify({'error': 'Error al añadir item'}), 500
        
    except Exception as e:
        return jsonify({'error': f'Error interno: {str(e)}'}), 500


# 7.2 PUT /api/shopping-list/item/<item_id> - Actualizar item
@app.route('/api/shopping-list/item/<item_id>', methods=['PUT'])
@token_required
def update_shopping_item(item_id):
    """Actualiza un item de la lista (cantidad, checked, etc)."""
    try:
        user_id = request.current_user['user_id']
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'JSON requerido'}), 400
        
        # Verificar que el item pertenece al usuario
        existing = supabase.table('shopping_lists').select('*').eq('id', item_id).eq('user_id', user_id).execute()
        if not existing.data:
            return jsonify({'error': 'Item no encontrado'}), 404
        
        # Preparar actualización
        update_fields = {}
        if 'checked' in data:
            update_fields['checked'] = data['checked']
        if 'quantity' in data or 'amount' in data:
            update_fields['quantity'] = str(data.get('quantity') or data.get('amount'))
        if 'unit' in data:
            update_fields['unit'] = data['unit']
        if 'ingredient' in data or 'name' in data:
            update_fields['ingredient'] = data.get('ingredient') or data.get('name')
        
        if update_fields:
            result = supabase.table('shopping_lists').update(update_fields).eq('id', item_id).execute()
            return jsonify({'message': 'Item actualizado', 'item': result.data[0] if result.data else {}}), 200
        
        return jsonify({'message': 'Sin cambios'}), 200
        
    except Exception as e:
        return jsonify({'error': f'Error interno: {str(e)}'}), 500


# 7.3 DELETE /api/shopping-list/item/<item_id> - Eliminar item
@app.route('/api/shopping-list/item/<item_id>', methods=['DELETE'])
@token_required
def delete_shopping_item(item_id):
    """Elimina un item de la lista de compras."""
    try:
        user_id = request.current_user['user_id']
        
        # Verificar que el item pertenece al usuario
        result = supabase.table('shopping_lists').delete().eq('id', item_id).eq('user_id', user_id).execute()
        
        if result.data:
            return jsonify({'message': 'Item eliminado'}), 200
        
        return jsonify({'error': 'Item no encontrado'}), 404
        
    except Exception as e:
        return jsonify({'error': f'Error interno: {str(e)}'}), 500


# 7.4 DELETE /api/shopping-list/clear - Limpiar lista manual
@app.route('/api/shopping-list/clear', methods=['DELETE'])
@token_required
def clear_shopping_list():
    """Elimina todos los items manuales de la lista."""
    try:
        user_id = request.current_user['user_id']
        
        result = supabase.table('shopping_lists').delete().eq('user_id', user_id).execute()
        
        return jsonify({'message': 'Lista limpiada'}), 200
        
    except Exception as e:
        return jsonify({'error': f'Error interno: {str(e)}'}), 500


# 7.5 GET /api/shopping-list/export - Exportar lista
@app.route('/api/shopping-list/export', methods=['GET'])
@token_required
def export_shopping_list():
    """Exporta la lista de compras en formato texto o WhatsApp."""
    try:
        user_id = request.current_user['user_id']
        week_number = request.args.get('week', default=datetime.now().isocalendar()[1], type=int)
        format_type = request.args.get('format', 'text')  # text, whatsapp
        
        # Obtener lista completa
        plan_result = supabase.table('weekly_plans').select('*').eq('user_id', user_id).eq('week_number', week_number).execute()
        
        if not plan_result.data:
            return jsonify({'error': 'No hay plan para esta semana'}), 404
        
        recipe_ids = list(set(entry.get('selected_recipe_id') for entry in plan_result.data if entry.get('selected_recipe_id')))
        recipes_result = supabase.table('master_recipes').select('id, name, ingredients, supermarket').in_('id', recipe_ids).execute()
        recipes_dict = {r['id']: r for r in (recipes_result.data or [])}
        
        # Agrupar por supermercado
        grouped = {'mercadona': [], 'lidl': [], 'carrefour': [], 'generic': [], 'manual': []}
        
        for entry in plan_result.data:
            recipe_id = entry.get('selected_recipe_id')
            if not recipe_id:
                continue
            
            recipe = recipes_dict.get(recipe_id, {})
            supermarket = recipe.get('supermarket', 'generic') or 'generic'
            
            if supermarket not in grouped:
                supermarket = 'generic'
            
            recipe_ingredients = recipe.get('ingredients', [])
            if isinstance(recipe_ingredients, str):
                for ing in recipe_ingredients.split(','):
                    ing = ing.strip()
                    if ing:
                        grouped[supermarket].append(ing)
            elif isinstance(recipe_ingredients, list):
                for ing in recipe_ingredients:
                    if isinstance(ing, dict):
                        grouped[supermarket].append(f"{ing.get('amount', '')} {ing.get('unit', '')} {ing.get('name', '')}".strip())
                    elif isinstance(ing, str):
                        grouped[supermarket].append(ing)
        
        # Añadir items manuales
        manual_items = supabase.table('shopping_lists').select('*').eq('user_id', user_id).execute()
        for item in (manual_items.data or []):
            grouped['manual'].append(f"{item.get('quantity', '')} {item.get('unit', '')} {item.get('ingredient', '')}".strip())
        
        # Generar texto según formato
        supermarket_names = {
            'mercadona': '🛒 MERCADONA',
            'lidl': '🛒 LIDL',
            'carrefour': '🛒 CARREFOUR',
            'generic': '📦 OTROS',
            'manual': '✍️ MANUAL'
        }
        
        lines = []
        for key, items in grouped.items():
            if items:
                # Eliminar duplicados y ordenar
                unique_items = sorted(set(items))
                lines.append(f"\n{supermarket_names.get(key, key)}")
                lines.append("=" * 30)
                for item in unique_items:
                    if format_type == 'whatsapp':
                        lines.append(f"☐ {item}")
                    else:
                        lines.append(f"□ {item}")
        
        if format_type == 'whatsapp':
            header = f"🛒 *LISTA DE COMPRA - Semana {week_number}*\n\n"
            export_text = header + "\n".join(lines)
        else:
            header = f"LISTA DE COMPRA - Semana {week_number}\n"
            export_text = header + "\n".join(lines)
        
        return jsonify({
            'format': format_type,
            'text': export_text,
            'week_number': week_number,
            'total_items': sum(len(items) for items in grouped.values())
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
        log_result = supabase.table('food_logs').select('calories, protein as protein_g, carbs as carbs_g, fat as fat_g').eq('user_id', user_id).eq('week_number', week_number).execute()
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
        
        # Build food log entry
        log_entry = {
            'user_id': user_id,
            'meal_type': log_data.meal_type,
            'calories': int(log_data.calories * (log_data.quantity or 1)),
            'protein': round(log_data.protein * (log_data.quantity or 1), 2),
            'carbs': round(log_data.carbs * (log_data.quantity or 1), 2),
            'fat': round(log_data.fat * (log_data.quantity or 1), 2),
            'notes': log_data.notes or '',
            'week_number': week_number,
            'day_of_week': day_of_week,
            'logged_at': datetime.now().isoformat(),
            'source': log_data.source or 'manual',
            'quantity': log_data.quantity or 1
        }
        
        # Add optional fields
        if log_data.recipe_id:
            log_entry['recipe_id'] = log_data.recipe_id
        if log_data.food_name:
            log_entry['food_name'] = log_data.food_name
        if log_data.barcode:
            log_entry['barcode'] = log_data.barcode
        
        # Registrar food log
        result = supabase.table('food_logs').insert(log_entry).execute()
        
        return jsonify({
            'message': 'Comida registrada',
            'log_id': result.data[0]['id'] if result.data else None,
            'calories': log_entry['calories'],
            'protein': log_entry['protein'],
            'carbs': log_entry['carbs'],
            'fat': log_entry['fat'],
            'meal_type': log_data.meal_type,
            'source': log_data.source
        }), 201
        
    except Exception as e:
        return jsonify({'error': f'Error interno: {str(e)}'}), 500

# 10b. GET /api/food-log/today - Obtiene comidas del día
@app.route('/api/food-log/today', methods=['GET'])
@token_required
def get_today_food_log():
    """Obtiene todas las comidas registradas hoy."""
    try:
        user_id = request.current_user['user_id']
        week_number = datetime.now().isocalendar()[1]
        day_of_week = datetime.now().weekday()
        
        # Get today's food logs
        result = supabase.table('food_logs').select('*').eq('user_id', user_id).eq('week_number', week_number).eq('day_of_week', day_of_week).order('logged_at').execute()
        
        logs = result.data or []
        
        # Calculate totals
        total_calories = sum(log.get('calories', 0) for log in logs)
        total_protein = sum(log.get('protein', 0) for log in logs)
        total_carbs = sum(log.get('carbs', 0) for log in logs)
        total_fat = sum(log.get('fat', 0) for log in logs)
        
        # Group by meal type
        by_meal = {}
        for log in logs:
            meal = log.get('meal_type', 'other')
            if meal not in by_meal:
                by_meal[meal] = []
            by_meal[meal].append(log)
        
        return jsonify({
            'date': datetime.now().date().isoformat(),
            'logs': logs,
            'by_meal': by_meal,
            'totals': {
                'calories': total_calories,
                'protein': total_protein,
                'carbs': total_carbs,
                'fat': total_fat
            },
            'count': len(logs)
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Error interno: {str(e)}'}), 500

# 10c. DELETE /api/food-log/<id> - Elimina una comida registrada
@app.route('/api/food-log/<log_id>', methods=['DELETE'])
@token_required
def delete_food_log(log_id):
    """Elimina una comida del registro."""
    try:
        user_id = request.current_user['user_id']
        
        # Verify ownership
        check = supabase.table('food_logs').select('id').eq('id', log_id).eq('user_id', user_id).execute()
        if not check.data:
            return jsonify({'error': 'Registro no encontrado'}), 404
        
        # Delete
        supabase.table('food_logs').delete().eq('id', log_id).execute()
        
        return jsonify({'message': 'Comida eliminada del registro'}), 200
        
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

# 11b. GET /api/search-food - Busca alimentos (recetas y Open Food Facts)
@app.route('/api/search-food', methods=['GET'])
@token_required
def search_food():
    """Busca alimentos en recetas y Open Food Facts."""
    try:
        import urllib.request
        import json as json_module
        
        query = request.args.get('q', '').strip().lower()
        search_type = request.args.get('type', 'all')  # 'recipes', 'products', 'all'
        limit = request.args.get('limit', default=20, type=int)
        
        if not query or len(query) < 2:
            return jsonify({'error': 'Búsqueda muy corta (mínimo 2 caracteres)'}), 400
        
        results = {
            'recipes': [],
            'products': [],
            'total': 0
        }
        
        # Search in master_recipes
        if search_type in ['all', 'recipes']:
            try:
                recipe_result = supabase.table('master_recipes').select('id, name, calories, protein, carbs, fat, meal_type, image_url').ilike('name', f'%{query}%').limit(limit).execute()
                results['recipes'] = recipe_result.data or []
            except Exception as e:
                print(f"Error searching recipes: {e}")
        
        # Search in Open Food Facts
        if search_type in ['all', 'products']:
            try:
                # Open Food Facts API
                off_url = f"https://world.openfoodfacts.org/cgi/search.pl?search_terms={query}&json=1&page_size={min(limit, 20)}&fields=code,product_name,nutriments,image_small_url,brands,serving_size"
                
                req = urllib.request.Request(off_url, headers={'User-Agent': 'DietTrackerApp/1.0'})
                response = urllib.request.urlopen(req, timeout=10)
                off_data = json_module.loads(response.read().decode())
                
                if off_data.get('products'):
                    for product in off_data['products']:
                        nutriments = product.get('nutriments', {})
                        results['products'].append({
                            'barcode': product.get('code'),
                            'name': product.get('product_name', 'Unknown'),
                            'brand': product.get('brands', ''),
                            'image': product.get('image_small_url'),
                            'serving_size': product.get('serving_size', '100g'),
                            'calories': nutriments.get('energy-kcal_100g', nutriments.get('energy-kcal', 0)),
                            'protein': nutriments.get('proteins_100g', nutriments.get('proteins', 0)),
                            'carbs': nutriments.get('carbohydrates_100g', nutriments.get('carbohydrates', 0)),
                            'fat': nutriments.get('fat_100g', nutriments.get('fat', 0)),
                            'source': 'openfoodfacts'
                        })
            except Exception as e:
                print(f"Error searching Open Food Facts: {e}")
        
        results['total'] = len(results['recipes']) + len(results['products'])
        
        return jsonify(results), 200
        
    except Exception as e:
        return jsonify({'error': f'Error interno: {str(e)}'}), 500

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
