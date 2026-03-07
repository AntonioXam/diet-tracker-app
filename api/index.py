"""
Diet Tracker API - Versión para Vercel Serverless
Usa memoria temporal (se reinicia con cada deploy)
"""
import os
import hashlib
import secrets
import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask import Flask, request, jsonify
from flask_cors import CORS
from pydantic import BaseModel, Field
from typing import Optional
import uuid
import json

app = Flask(__name__)
CORS(app, origins=["*"], supports_credentials=True)

JWT_SECRET = os.getenv("JWT_SECRET", secrets.token_hex(32))

# ==================== BASE DE DATOS EN MEMORIA ====================

# Usuarios: {user_id: {email, password_hash, salt, name}}
users_db = {}

# Perfiles: {user_id: {age, gender, height, weight, goal, ...}}
profiles_db = {}

# Recetas predefinidas
RECIPES = [
    {"id": "1", "name": "Tostadas con aguacate y huevo", "meal_type": "breakfast", "calories": 350, "protein": 15, "carbs": 25, "fat": 20},
    {"id": "2", "name": "Batido de proteínas con frutas", "meal_type": "breakfast", "calories": 300, "protein": 25, "carbs": 35, "fat": 5},
    {"id": "3", "name": "Tortilla de espinacas", "meal_type": "breakfast", "calories": 280, "protein": 18, "carbs": 8, "fat": 20},
    {"id": "4", "name": "Avena con frutos rojos", "meal_type": "breakfast", "calories": 320, "protein": 12, "carbs": 55, "fat": 6},
    {"id": "5", "name": "Yogur griego con granola", "meal_type": "breakfast", "calories": 290, "protein": 20, "carbs": 30, "fat": 8},
    {"id": "6", "name": "Ensalada César con pollo", "meal_type": "lunch", "calories": 450, "protein": 35, "carbs": 15, "fat": 28},
    {"id": "7", "name": "Pasta integral con verduras", "meal_type": "lunch", "calories": 400, "protein": 15, "carbs": 65, "fat": 10},
    {"id": "8", "name": "Salmón al horno con verduras", "meal_type": "lunch", "calories": 500, "protein": 40, "carbs": 20, "fat": 28},
    {"id": "9", "name": "Wraps de pavo y aguacate", "meal_type": "lunch", "calories": 380, "protein": 28, "carbs": 35, "fat": 15},
    {"id": "10", "name": "Quinoa con verduras asadas", "meal_type": "lunch", "calories": 420, "protein": 18, "carbs": 55, "fat": 14},
    {"id": "11", "name": "Pollo al curry con arroz", "meal_type": "dinner", "calories": 550, "protein": 42, "carbs": 45, "fat": 18},
    {"id": "12", "name": "Sopa de lentejas", "meal_type": "dinner", "calories": 350, "protein": 22, "carbs": 45, "fat": 8},
    {"id": "13", "name": "Filete de ternera con ensalada", "meal_type": "dinner", "calories": 600, "protein": 50, "carbs": 10, "fat": 38},
    {"id": "14", "name": "Pescado al papillote", "meal_type": "dinner", "calories": 320, "protein": 35, "carbs": 15, "fat": 12},
    {"id": "15", "name": "Revuelto de verduras", "meal_type": "dinner", "calories": 280, "protein": 15, "carbs": 12, "fat": 20},
    {"id": "16", "name": "Frutos secos", "meal_type": "snack", "calories": 180, "protein": 5, "carbs": 10, "fat": 15},
    {"id": "17", "name": "Yogur natural", "meal_type": "snack", "calories": 100, "protein": 8, "carbs": 8, "fat": 4},
    {"id": "18", "name": "Manzana con mantequilla de cacahuete", "meal_type": "snack", "calories": 200, "protein": 5, "carbs": 25, "fat": 10},
    {"id": "19", "name": "Huevo duro", "meal_type": "snack", "calories": 70, "protein": 6, "carbs": 0, "fat": 5},
    {"id": "20", "name": "Barra de proteínas", "meal_type": "snack", "calories": 220, "protein": 20, "carbs": 22, "fat": 8},
]

# Planes: {user_id: [{day, meal_type, recipe_id, calories}]}
plans_db = {}

# Food logs: {user_id: [{date, meal_type, food, calories}]}
food_logs_db = {}

# ==================== MODELOS PYDANTIC ====================

class RegisterRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: str = Field(..., pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    password: str = Field(..., min_length=6, max_length=100)

class LoginRequest(BaseModel):
    email: str
    password: str

class OnboardingRequest(BaseModel):
    age: int = Field(..., ge=10, le=120)
    gender: str = Field(..., pattern="^(male|female)$")
    height: float = Field(..., ge=100, le=250)
    current_weight: float = Field(..., ge=30, le=300)
    goal_weight: float = Field(..., ge=30, le=300)
    goal_type: str = Field(..., pattern="^(lose|gain|maintain)$")
    activity_level: str = Field(..., pattern="^(sedentary|light|moderate|active|very_active)$")
    meals_per_day: int = Field(4, ge=3, le=5)
    allergies: Optional[str] = ""
    budget: Optional[str] = "medium"
    target_calories: Optional[int] = None

# ==================== FUNCIONES AUXILIARES ====================

def hash_password(password: str, salt: str = None) -> tuple:
    if salt is None:
        salt = secrets.token_hex(16)
    hashed = hashlib.sha256((password + salt).encode()).hexdigest()
    return hashed, salt

def verify_password(password: str, stored_hash: str, salt: str) -> bool:
    hashed, _ = hash_password(password, salt)
    return hashed == stored_hash

def generate_token(user_id: str, email: str) -> str:
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
        token = None
        auth_header = request.headers.get('Authorization', '')
        if auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
        
        if not token:
            return jsonify({'error': 'Token requerido'}), 401
        
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
            request.current_user = {'user_id': payload['user_id'], 'email': payload['email']}
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token expirado'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Token inválido'}), 401
        
        return f(*args, **kwargs)
    return decorated

# ==================== ENDPOINTS ====================

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'mode': 'serverless', 'users': len(users_db)})

@app.route('/api/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        req = RegisterRequest(**data)
        
        # Verificar si el email ya existe
        for uid, u in users_db.items():
            if u['email'] == req.email:
                return jsonify({'error': 'Email ya registrado'}), 400
        
        # Crear usuario
        user_id = str(uuid.uuid4())
        password_hash, salt = hash_password(req.password)
        
        users_db[user_id] = {
            'id': user_id,
            'email': req.email,
            'password_hash': password_hash,
            'salt': salt,
            'name': req.name
        }
        
        token = generate_token(user_id, req.email)
        
        return jsonify({
            'message': 'Usuario registrado correctamente',
            'user': {'id': user_id, 'email': req.email, 'name': req.name},
            'token': token
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        req = LoginRequest(**data)
        
        # Buscar usuario
        user = None
        for uid, u in users_db.items():
            if u['email'] == req.email:
                user = u
                break
        
        if not user:
            return jsonify({'error': 'Credenciales inválidas'}), 401
        
        if not verify_password(req.password, user['password_hash'], user['salt']):
            return jsonify({'error': 'Credenciales inválidas'}), 401
        
        token = generate_token(user['id'], user['email'])
        
        return jsonify({
            'message': 'Login correcto',
            'user': {'id': user['id'], 'email': user['email'], 'name': user['name']},
            'token': token
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/onboarding', methods=['POST'])
@token_required
def onboarding():
    try:
        user_id = request.current_user['user_id']
        data = request.get_json()
        req = OnboardingRequest(**data)
        
        # Calcular calorías objetivo
        if not req.target_calories:
            # Fórmula Mifflin-St Jeor
            if req.gender == 'male':
                bmr = 10 * req.current_weight + 6.25 * req.height - 5 * req.age + 5
            else:
                bmr = 10 * req.current_weight + 6.25 * req.height - 5 * req.age - 161
            
            activity_multipliers = {
                'sedentary': 1.2,
                'light': 1.375,
                'moderate': 1.55,
                'active': 1.725,
                'very_active': 1.9
            }
            
            tdee = bmr * activity_multipliers.get(req.activity_level, 1.55)
            
            if req.goal_type == 'lose':
                target_calories = max(1200, int(tdee - 500))
            elif req.goal_type == 'gain':
                target_calories = int(tdee + 300)
            else:
                target_calories = int(tdee)
        else:
            target_calories = req.target_calories
        
        # Guardar perfil
        profiles_db[user_id] = {
            'age': req.age,
            'gender': req.gender,
            'height': req.height,
            'weight': req.current_weight,
            'goal_weight': req.goal_weight,
            'goal_type': req.goal_type,
            'activity_level': req.activity_level,
            'meals_per_day': req.meals_per_day,
            'budget': req.budget,
            'allergies': req.allergies,
            'target_calories': target_calories,
            'onboarding_completed': True
        }
        
        return jsonify({
            'message': 'Onboarding completado',
            'success': True,
            'target_calories': target_calories
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/profile', methods=['GET'])
@token_required
def get_profile():
    user_id = request.current_user['user_id']
    profile = profiles_db.get(user_id, {})
    return jsonify(profile)

@app.route('/api/profile', methods=['PUT'])
@token_required
def update_profile():
    user_id = request.current_user['user_id']
    data = request.get_json()
    
    if user_id not in profiles_db:
        profiles_db[user_id] = {}
    
    profiles_db[user_id].update(data)
    
    return jsonify({'message': 'Perfil actualizado', 'success': True})

@app.route('/api/recipes', methods=['GET'])
def get_recipes():
    meal_type = request.args.get('type', None)
    limit = int(request.args.get('limit', 50))
    
    if meal_type:
        recipes = [r for r in RECIPES if r['meal_type'] == meal_type][:limit]
    else:
        recipes = RECIPES[:limit]
    
    return jsonify({'recipes': recipes, 'total': len(recipes)})

@app.route('/api/plan', methods=['GET'])
@token_required
def get_plan():
    user_id = request.current_user['user_id']
    plans = plans_db.get(user_id, [])
    return jsonify({'plans': plans})

@app.route('/api/generate-plan', methods=['POST'])
@token_required
def generate_plan():
    user_id = request.current_user['user_id']
    data = request.get_json()
    
    target_calories = data.get('target_calories', 2000)
    meals_per_day = data.get('meals_per_day', 4)
    
    meal_types = ['breakfast', 'lunch', 'snack', 'dinner'][:meals_per_day]
    
    import random
    
    plans = []
    for day in range(7):
        for meal_type in meal_types:
            recipes_for_meal = [r for r in RECIPES if r['meal_type'] == meal_type]
            if recipes_for_meal:
                recipe = random.choice(recipes_for_meal)
                plans.append({
                    'day': day,
                    'meal_type': meal_type,
                    'recipe_id': recipe['id'],
                    'recipe_name': recipe['name'],
                    'calories': recipe['calories'],
                    'protein': recipe['protein'],
                    'carbs': recipe['carbs'],
                    'fat': recipe['fat']
                })
    
    plans_db[user_id] = plans
    
    return jsonify({'message': 'Plan generado correctamente', 'success': True, 'plans': plans})

@app.route('/api/food-log', methods=['POST'])
@token_required
def log_food():
    user_id = request.current_user['user_id']
    data = request.get_json()
    
    if user_id not in food_logs_db:
        food_logs_db[user_id] = []
    
    log = {
        'id': str(uuid.uuid4()),
        'meal_type': data.get('meal_type', 'snack'),
        'food_name': data.get('food_name', ''),
        'calories': data.get('calories', 0),
        'protein': data.get('protein', 0),
        'carbs': data.get('carbs', 0),
        'fat': data.get('fat', 0),
        'quantity': data.get('quantity', 1),
        'source': data.get('source', 'manual'),
        'date': datetime.now().isoformat()
    }
    
    food_logs_db[user_id].append(log)
    
    return jsonify({'message': 'Comida registrada', 'log_id': log['id'], 'success': True})

@app.route('/api/food-log/today', methods=['GET'])
@token_required
def get_today_food():
    user_id = request.current_user['user_id']
    
    logs = food_logs_db.get(user_id, [])
    today = datetime.now().date().isoformat()
    
    today_logs = [l for l in logs if l['date'].startswith(today)]
    
    total_calories = sum(l['calories'] for l in today_logs)
    total_protein = sum(l['protein'] for l in today_logs)
    total_carbs = sum(l['carbs'] for l in today_logs)
    total_fat = sum(l['fat'] for l in today_logs)
    
    return jsonify({
        'logs': today_logs,
        'totals': {
            'calories': total_calories,
            'protein': total_protein,
            'carbs': total_carbs,
            'fat': total_fat
        }
    })

@app.route('/api/shopping-list', methods=['GET'])
@token_required
def get_shopping_list():
    return jsonify({'items': []})

@app.route('/api/search-products', methods=['GET'])
def search_products():
    import requests
    
    query = request.args.get('query', '')
    barcode = request.args.get('barcode', '')
    
    if barcode:
        url = f"https://world.openfoodfacts.org/api/v2/product/{barcode}.json"
        try:
            response = requests.get(url, timeout=5)
            data = response.json()
            if data.get('status') == 1:
                product = data.get('product', {})
                return jsonify({
                    'products': [{
                        'barcode': barcode,
                        'name': product.get('product_name', 'Unknown'),
                        'calories': product.get('nutriments', {}).get('energy-kcal_100g', 0),
                        'protein': product.get('nutriments', {}).get('proteins_100g', 0),
                        'carbs': product.get('nutriments', {}).get('carbohydrates_100g', 0),
                        'fat': product.get('nutriments', {}).get('fat_100g', 0)
                    }]
                })
        except:
            pass
    
    if query:
        url = f"https://world.openfoodfacts.org/cgi/search.pl?search_terms={query}&json=1&page_size=20"
        try:
            response = requests.get(url, timeout=10)
            data = response.json()
            products = []
            for p in data.get('products', [])[:20]:
                products.append({
                    'barcode': p.get('code', ''),
                    'name': p.get('product_name', 'Unknown'),
                    'calories': p.get('nutriments', {}).get('energy-kcal_100g', 0),
                    'protein': p.get('nutriments', {}).get('proteins_100g', 0),
                    'carbs': p.get('nutriments', {}).get('carbohydrates_100g', 0),
                    'fat': p.get('nutriments', {}).get('fat_100g', 0)
                })
            return jsonify({'products': products})
        except:
            pass
    
    return jsonify({'products': []})

@app.route('/api/search-food', methods=['GET'])
@token_required
def search_food():
    query = request.args.get('q', '').lower()
    
    results = {'recipes': [], 'products': []}
    
    # Buscar en recetas
    for recipe in RECIPES:
        if query in recipe['name'].lower():
            results['recipes'].append(recipe)
    
    return jsonify(results)

@app.route('/api/dashboard', methods=['GET'])
@token_required
def get_dashboard():
    user_id = request.current_user['user_id']
    
    profile = profiles_db.get(user_id, {})
    logs = food_logs_db.get(user_id, [])
    
    today = datetime.now().date().isoformat()
    today_logs = [l for l in logs if l['date'].startswith(today)]
    
    total_calories = sum(l['calories'] for l in today_logs)
    target_calories = profile.get('target_calories', 2000)
    
    return jsonify({
        'profile': profile,
        'today': {
            'logs': today_logs,
            'total_calories': total_calories,
            'target_calories': target_calories,
            'remaining': target_calories - total_calories
        }
    })

# ==================== INICIAR ====================

# Handler para Vercel
handler = app

if __name__ == '__main__':
    print("🚀 Diet Tracker API - Modo Serverless")
    print("🌐 Servidor: http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)