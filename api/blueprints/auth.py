"""Blueprint para autenticación y registro."""
from flask import Blueprint, request, jsonify
from supabase import create_client

from config import Config
from utils.validation import validate_register_data
from services.user_service import UserService

bp = Blueprint('auth', __name__, url_prefix='/api')
supabase = create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)
user_service = UserService(supabase)


@bp.route('/register', methods=['POST'])
def register():
    """Registra un nuevo usuario y crea su perfil."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        # Validar datos
        is_valid, error_msg, cleaned_data = validate_register_data(data)
        if not is_valid:
            return jsonify({'error': error_msg}), 400
        
        # Crear usuario
        user_result, error = user_service.create_user(cleaned_data['username'])
        if error:
            return jsonify({'error': error}), 400
        
        user_id = user_result['id']
        
        # Crear perfil
        profile_result, error = user_service.create_profile(user_id, cleaned_data)
        if error:
            # Intentar eliminar usuario creado (rollback parcial)
            supabase.table('users').delete().eq('id', user_id).execute()
            return jsonify({'error': error}), 400
        
        return jsonify({
            'message': 'Usuario registrado correctamente',
            'user_id': user_id,
            'username': cleaned_data['username'],
            'target_calories': profile_result['target_calories'],
            'tmb': profile_result['tmb'],
            'tdee': profile_result['tdee']
        }), 201
    
    except Exception as e:
        return jsonify({'error': 'Error interno del servidor', 'details': str(e)}), 500


@bp.route('/login', methods=['POST'])
def login():
    """Login simplificado - verifica que el usuario exista."""
    try:
        data = request.get_json()
        if not data or 'username' not in data:
            return jsonify({'error': 'Se requiere username'}), 400
        
        username = data['username'].strip()
        
        # Buscar usuario
        result = supabase.table('users').select('id, name').eq('email', username).execute()
        if not result.data:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        
        user = result.data[0]
        return jsonify({
            'message': 'Login exitoso',
            'user_id': user['id'],
            'username': username
        }), 200
    
    except Exception as e:
        return jsonify({'error': 'Error interno del servidor', 'details': str(e)}), 500