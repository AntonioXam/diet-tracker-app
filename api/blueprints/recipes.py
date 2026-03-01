"""Blueprint para recetas y banco de alimentos."""
from flask import Blueprint, request, jsonify
from supabase import create_client

from config import Config
from services.recipe_service import RecipeService

bp = Blueprint('recipes', __name__, url_prefix='/api')
supabase = create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)
recipe_service = RecipeService(supabase)


@bp.route('/recipes', methods=['GET'])
def get_all_recipes():
    """Obtiene todas las recetas."""
    try:
        recipes, error = recipe_service.get_all_recipes()
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify(recipes), 200
    
    except Exception as e:
        return jsonify({'error': 'Error interno del servidor', 'details': str(e)}), 500


@bp.route('/recipes/meal/<meal_type>', methods=['GET'])
def get_recipes_by_meal_type(meal_type):
    """Obtiene recetas por tipo de comida."""
    try:
        limit = request.args.get('limit', default=20, type=int)
        
        recipes, error = recipe_service.get_recipes_by_meal_type(meal_type, limit)
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify(recipes), 200
    
    except Exception as e:
        return jsonify({'error': 'Error interno del servidor', 'details': str(e)}), 500


@bp.route('/food-bank/<int:user_id>', methods=['GET'])
def get_food_bank(user_id):
    """Obtiene banco de alimentos del usuario."""
    try:
        food_bank, error = recipe_service.get_food_bank(user_id)
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify(food_bank), 200
    
    except Exception as e:
        return jsonify({'error': 'Error interno del servidor', 'details': str(e)}), 500


@bp.route('/food-bank/add', methods=['POST'])
def add_to_food_bank():
    """Añade receta al banco de alimentos."""
    try:
        data = request.get_json()
        if not data or 'user_id' not in data or 'recipe_id' not in data or 'meal_type' not in data:
            return jsonify({'error': 'Se requieren user_id, recipe_id y meal_type'}), 400
        
        user_id = data['user_id']
        recipe_id = data['recipe_id']
        meal_type = data['meal_type']
        
        result, error = recipe_service.add_to_food_bank(user_id, meal_type, recipe_id)
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify({
            'message': 'Receta añadida al banco',
            'food_bank_entry': result
        }), 201
    
    except Exception as e:
        return jsonify({'error': 'Error interno del servidor', 'details': str(e)}), 500


@bp.route('/food-bank/remove', methods=['DELETE'])
def remove_from_food_bank():
    """Elimina receta del banco de alimentos."""
    try:
        data = request.get_json()
        if not data or 'user_id' not in data or 'recipe_id' not in data:
            return jsonify({'error': 'Se requieren user_id y recipe_id'}), 400
        
        user_id = data['user_id']
        recipe_id = data['recipe_id']
        
        success, error = recipe_service.remove_from_food_bank(user_id, recipe_id)
        if error or not success:
            return jsonify({'error': error or 'Error eliminando receta'}), 400
        
        return jsonify({'message': 'Receta eliminada del banco'}), 200
    
    except Exception as e:
        return jsonify({'error': 'Error interno del servidor', 'details': str(e)}), 500


@bp.route('/food-bank/available/<int:user_id>/<meal_type>', methods=['GET'])
def get_available_recipes(user_id, meal_type):
    """Obtiene recetas disponibles del banco para un tipo de comida."""
    try:
        recipes, error = recipe_service.get_available_recipes_for_meal(user_id, meal_type)
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify(recipes), 200
    
    except Exception as e:
        return jsonify({'error': 'Error interno del servidor', 'details': str(e)}), 500


@bp.route('/recipes/popular', methods=['GET'])
def get_popular_recipes():
    """Obtiene recetas más populares."""
    try:
        limit = request.args.get('limit', default=10, type=int)
        
        recipes, error = recipe_service.get_popular_recipes(limit)
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify(recipes), 200
    
    except Exception as e:
        return jsonify({'error': 'Error interno del servidor', 'details': str(e)}), 500