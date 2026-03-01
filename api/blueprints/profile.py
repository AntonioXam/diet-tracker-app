"""Blueprint para gestión de perfil y peso."""
from flask import Blueprint, request, jsonify
from supabase import create_client

from config import Config
from utils.validation import validate_profile_update, validate_weight_checkin
from services.user_service import UserService

bp = Blueprint('profile', __name__, url_prefix='/api')
supabase = create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)
user_service = UserService(supabase)


@bp.route('/profile/<int:user_id>', methods=['GET'])
def get_profile(user_id):
    """Obtiene perfil del usuario."""
    try:
        profile, error = user_service.get_profile(user_id)
        if error:
            return jsonify({'error': error}), 404
        
        return jsonify(profile), 200
    
    except Exception as e:
        return jsonify({'error': 'Error interno del servidor', 'details': str(e)}), 500


@bp.route('/profile/<int:user_id>', methods=['PUT'])
def update_profile(user_id):
    """Actualiza perfil del usuario."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        # Validar datos
        is_valid, error_msg, cleaned_data = validate_profile_update(data)
        if not is_valid:
            return jsonify({'error': error_msg}), 400
        
        # Actualizar perfil
        result, error = user_service.update_profile(user_id, cleaned_data)
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify({
            'message': 'Perfil actualizado',
            'recalculated': result.get('recalculated', False),
            'new_target_calories': result.get('target_calories'),
            'tmb': result.get('tmb'),
            'tdee': result.get('tdee')
        }), 200
    
    except Exception as e:
        return jsonify({'error': 'Error interno del servidor', 'details': str(e)}), 500


@bp.route('/weight/checkin', methods=['POST'])
def weight_checkin():
    """Registra nuevo peso."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        # Validar datos
        is_valid, error_msg, cleaned_data = validate_weight_checkin(data)
        if not is_valid:
            return jsonify({'error': error_msg}), 400
        
        user_id = cleaned_data['user_id']
        weight = cleaned_data['weight']
        
        # Registrar peso
        result, error = user_service.record_weight(user_id, weight)
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify({
            'message': 'Peso registrado',
            'new_target_calories': result['new_target_calories']
        }), 200
    
    except Exception as e:
        return jsonify({'error': 'Error interno del servidor', 'details': str(e)}), 500


@bp.route('/weight/history/<int:user_id>', methods=['GET'])
def get_weight_history(user_id):
    """Obtiene historial de peso."""
    try:
        limit = request.args.get('limit', default=30, type=int)
        
        history, error = user_service.get_weight_history(user_id, limit)
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify(history), 200
    
    except Exception as e:
        return jsonify({'error': 'Error interno del servidor', 'details': str(e)}), 500