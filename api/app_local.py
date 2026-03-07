"""
Diet Tracker API - Versión Local con SQLite
Para desarrollo y pruebas sin Supabase
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
from pydantic import BaseModel, Field
from typing import Optional, List
import uuid

# Base de datos local
from db_local import get_db, init_db

app = Flask(__name__)
CORS(app, origins=["*"], supports_credentials=True)

JWT_SECRET = os.getenv("JWT_SECRET", secrets.token_hex(32))

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
    disliked_foods: Optional[str] = ""
    budget: Optional[str] = "medium"
    preferences: Optional[list] = []
    target_calories: Optional[int] = None

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

class FoodLogRequest(BaseModel):
    meal_type: str
    food_name: Optional[str] = None
    recipe_id: Optional[str] = None
    calories: float
    protein: float = 0
    carbs: float = 0
    fat: float = 0
    quantity: float = 1
    source: str = "manual"
    barcode: Optional[str] = None
    notes: Optional[str] = None

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
    return jsonify({'status': 'ok', 'mode': 'local'})

@app.route('/api/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        req = RegisterRequest(**data)
        
        with get_db() as conn:
            cursor = conn.cursor()
            
            # Verificar si el email ya existe
            cursor.execute('SELECT id FROM users WHERE email = ?', (req.email,))
            if cursor.fetchone():
                return jsonify({'error': 'Email ya registrado'}), 400
            
            # Crear usuario
            user_id = str(uuid.uuid4())
            password_hash, salt = hash_password(req.password)
            
            cursor.execute('''
                INSERT INTO users (id, email, password_hash, salt, name)
                VALUES (?, ?, ?, ?, ?)
            ''', (user_id, req.email, password_hash, salt, req.name))
            
            conn.commit()
        
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
        
        with get_db() as conn:
            cursor = conn.cursor()
            
            cursor.execute('SELECT id, email, password_hash, salt, name FROM users WHERE email = ?', (req.email,))
            user = cursor.fetchone()
            
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
        
        with get_db() as conn:
            cursor = conn.cursor()
            
            # Crear o actualizar perfil
            profile_id = str(uuid.uuid4())
            cursor.execute('''
                INSERT INTO user_profiles (id, user_id, age, gender, height_cm, weight_kg, target_weight_kg, 
                    goal_type, activity_level, budget, meals_per_day, target_calories, allergies, onboarding_completed)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(user_id) DO UPDATE SET
                    age = ?, gender = ?, height_cm = ?, weight_kg = ?, target_weight_kg = ?,
                    goal_type = ?, activity_level = ?, budget = ?, meals_per_day = ?, target_calories = ?,
                    allergies = ?, onboarding_completed = ?
            ''', (
                profile_id, user_id, req.age, req.gender, req.height, req.current_weight, req.goal_weight,
                req.goal_type, req.activity_level, req.budget, req.meals_per_day, req.target_calories or 2000,
                req.allergies, True,
                req.age, req.gender, req.height, req.current_weight, req.goal_weight,
                req.goal_type, req.activity_level, req.budget, req.meals_per_day, req.target_calories or 2000,
                req.allergies, True
            ))
            
            conn.commit()
        
        return jsonify({'message': 'Onboarding completado', 'success': True})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/profile', methods=['GET'])
@token_required
def get_profile():
    user_id = request.current_user['user_id']
    
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM user_profiles WHERE user_id = ?', (user_id,))
        profile = cursor.fetchone()
        
        if not profile:
            return jsonify({'error': 'Perfil no encontrado'}), 404
        
        return jsonify(dict(profile))

@app.route('/api/profile', methods=['PUT'])
@token_required
def update_profile():
    user_id = request.current_user['user_id']
    data = request.get_json()
    
    with get_db() as conn:
        cursor = conn.cursor()
        
        updates = []
        values = []
        
        for field in ['age', 'gender', 'height_cm', 'weight_kg', 'target_weight_kg', 'goal_type', 
                      'activity_level', 'budget', 'meals_per_day', 'target_calories', 'allergies']:
            if field in data:
                updates.append(f'{field} = ?')
                values.append(data[field])
        
        if updates:
            values.append(user_id)
            cursor.execute(f'UPDATE user_profiles SET {", ".join(updates)} WHERE user_id = ?', values)
            conn.commit()
    
    return jsonify({'message': 'Perfil actualizado'})

@app.route('/api/recipes', methods=['GET'])
def get_recipes():
    meal_type = request.args.get('type', None)
    limit = request.args.get('limit', 50)
    
    with get_db() as conn:
        cursor = conn.cursor()
        
        if meal_type:
            cursor.execute('SELECT * FROM master_recipes WHERE meal_type = ? LIMIT ?', (meal_type, limit))
        else:
            cursor.execute('SELECT * FROM master_recipes LIMIT ?', (limit,))
        
        recipes = [dict(row) for row in cursor.fetchall()]
    
    return jsonify({'recipes': recipes, 'total': len(recipes)})

@app.route('/api/plan', methods=['GET'])
@token_required
def get_plan():
    user_id = request.current_user['user_id']
    
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT wp.*, mr.name, mr.meal_type 
            FROM weekly_plans wp 
            LEFT JOIN master_recipes mr ON wp.recipe_id = mr.id
            WHERE wp.user_id = ?
            ORDER BY wp.day_of_week, wp.meal_type
        ''', (user_id,))
        
        plans = [dict(row) for row in cursor.fetchall()]
    
    return jsonify({'plans': plans})

@app.route('/api/generate-plan', methods=['POST'])
@token_required
def generate_plan():
    user_id = request.current_user['user_id']
    data = request.get_json()
    
    target_calories = data.get('target_calories', 2000)
    meals_per_day = data.get('meals_per_day', 4)
    
    meal_types = ['breakfast', 'lunch', 'snack', 'dinner'][:meals_per_day]
    
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Eliminar plan anterior
        cursor.execute('DELETE FROM weekly_plans WHERE user_id = ?', (user_id,))
        
        # Generar nuevo plan
        for day in range(7):
            for meal_type in meal_types:
                cursor.execute('SELECT * FROM master_recipes WHERE meal_type = ? ORDER BY RANDOM() LIMIT 1', (meal_type,))
                recipe = cursor.fetchone()
                
                if recipe:
                    plan_id = str(uuid.uuid4())
                    cursor.execute('''
                        INSERT INTO weekly_plans (id, user_id, week_number, day_of_week, meal_type, recipe_id, calories)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    ''', (plan_id, user_id, datetime.now().isocalendar()[1], day, meal_type, recipe['id'], recipe['calories']))
        
        conn.commit()
    
    return jsonify({'message': 'Plan generado correctamente', 'success': True})

@app.route('/api/food-log', methods=['POST'])
@token_required
def log_food():
    user_id = request.current_user['user_id']
    data = request.get_json()
    
    with get_db() as conn:
        cursor = conn.cursor()
        
        log_id = str(uuid.uuid4())
        cursor.execute('''
            INSERT INTO food_logs (id, user_id, meal_type, food_name, calories, protein, carbs, fat, quantity, source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            log_id, user_id, data.get('meal_type', 'snack'), data.get('food_name', ''),
            data.get('calories', 0), data.get('protein', 0), data.get('carbs', 0), data.get('fat', 0),
            data.get('quantity', 1), data.get('source', 'manual')
        ))
        
        conn.commit()
    
    return jsonify({'message': 'Comida registrada', 'log_id': log_id})

@app.route('/api/food-log/today', methods=['GET'])
@token_required
def get_today_food():
    user_id = request.current_user['user_id']
    
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM food_logs 
            WHERE user_id = ? AND date(logged_at) = date('now')
            ORDER BY logged_at
        ''', (user_id,))
        
        logs = [dict(row) for row in cursor.fetchall()]
        
        total_calories = sum(log['calories'] for log in logs)
        total_protein = sum(log['protein'] for log in logs)
        total_carbs = sum(log['carbs'] for log in logs)
        total_fat = sum(log['fat'] for log in logs)
    
    return jsonify({
        'logs': logs,
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
    user_id = request.current_user['user_id']
    
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM shopping_items WHERE user_id = ? ORDER BY created_at', (user_id,))
        items = [dict(row) for row in cursor.fetchall()]
    
    return jsonify({'items': items})

@app.route('/api/search-products', methods=['GET'])
def search_products():
    """Busca productos en Open Food Facts"""
    import requests
    
    query = request.args.get('query', '')
    barcode = request.args.get('barcode', '')
    
    if barcode:
        # Búsqueda por código de barras
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
                        'brand': product.get('brands', ''),
                        'calories': product.get('nutriments', {}).get('energy-kcal_100g', 0),
                        'protein': product.get('nutriments', {}).get('proteins_100g', 0),
                        'carbs': product.get('nutriments', {}).get('carbohydrates_100g', 0),
                        'fat': product.get('nutriments', {}).get('fat_100g', 0),
                        'image_url': product.get('image_url', '')
                    }]
                })
        except Exception as e:
            return jsonify({'products': [], 'error': str(e)})
    
    if query:
        # Búsqueda por nombre
        url = f"https://world.openfoodfacts.org/cgi/search.pl?search_terms={query}&json=1&page_size=20"
        try:
            response = requests.get(url, timeout=10)
            data = response.json()
            products = []
            for p in data.get('products', [])[:20]:
                products.append({
                    'barcode': p.get('code', ''),
                    'name': p.get('product_name', 'Unknown'),
                    'brand': p.get('brands', ''),
                    'calories': p.get('nutriments', {}).get('energy-kcal_100g', 0),
                    'protein': p.get('nutriments', {}).get('proteins_100g', 0),
                    'carbs': p.get('nutriments', {}).get('carbohydrates_100g', 0),
                    'fat': p.get('nutriments', {}).get('fat_100g', 0),
                    'image_url': p.get('image_url', '')
                })
            return jsonify({'products': products})
        except Exception as e:
            return jsonify({'products': [], 'error': str(e)})
    
    return jsonify({'products': []})

@app.route('/api/search-food', methods=['GET'])
@token_required
def search_food():
    """Busca en recetas y productos"""
    query = request.args.get('q', '').lower()
    search_type = request.args.get('type', 'all')
    
    results = {'recipes': [], 'products': []}
    
    # Buscar en recetas locales
    if search_type in ['all', 'recipes']:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM master_recipes 
                WHERE LOWER(name) LIKE ? 
                ORDER BY name
                LIMIT 10
            ''', (f'%{query}%',))
            results['recipes'] = [dict(row) for row in cursor.fetchall()]
    
    # Buscar en Open Food Facts
    if search_type in ['all', 'products'] and len(query) >= 3:
        import requests
        url = f"https://world.openfoodfacts.org/cgi/search.pl?search_terms={query}&json=1&page_size=10"
        try:
            response = requests.get(url, timeout=10)
            data = response.json()
            for p in data.get('products', [])[:10]:
                results['products'].append({
                    'barcode': p.get('code', ''),
                    'name': p.get('product_name', 'Unknown'),
                    'brand': p.get('brands', ''),
                    'calories': p.get('nutriments', {}).get('energy-kcal_100g', 0),
                    'protein': p.get('nutriments', {}).get('proteins_100g', 0),
                    'carbs': p.get('nutriments', {}).get('carbohydrates_100g', 0),
                    'fat': p.get('nutriments', {}).get('fat_100g', 0),
                    'image_url': p.get('image_url', ''),
                    'source': 'openfoodfacts'
                })
        except Exception:
            pass
    
    return jsonify(results)

@app.route('/api/dashboard', methods=['GET'])
@token_required
def get_dashboard():
    user_id = request.current_user['user_id']
    
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Obtener perfil
        cursor.execute('SELECT * FROM user_profiles WHERE user_id = ?', (user_id,))
        profile = cursor.fetchone()
        
        # Obtener comida de hoy
        cursor.execute('''
            SELECT * FROM food_logs 
            WHERE user_id = ? AND date(logged_at) = date('now')
        ''', (user_id,))
        today_logs = [dict(row) for row in cursor.fetchall()]
        
        total_calories = sum(log['calories'] for log in today_logs)
        target_calories = profile['target_calories'] if profile else 2000
        
    return jsonify({
        'profile': dict(profile) if profile else None,
        'today': {
            'logs': today_logs,
            'total_calories': total_calories,
            'target_calories': target_calories,
            'remaining': target_calories - total_calories
        }
    })

# ==================== INICIAR ====================

if __name__ == '__main__':
    print("🚀 Diet Tracker API - Modo Local (SQLite)")
    print("📊 Base de datos: api/local.db")
    print("🌐 Servidor: http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)