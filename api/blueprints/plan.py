"""Blueprint para planes semanales."""
from flask import Blueprint, request, jsonify
from supabase import create_client

from config import Config
from services.plan_service import PlanService
from services.user_service import UserService

bp = Blueprint('plan', __name__, url_prefix='/api')
supabase = create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)
plan_service = PlanService(supabase)
user_service = UserService(supabase)


@bp.route('/plan/generate-first/<int:user_id>', methods=['POST'])
def generate_first_week(user_id):
    """Genera la primera semana de planificación."""
    try:
        # Obtener perfil para target_calories y meals_per_day
        profile, error = user_service.get_profile(user_id)
        if error:
            return jsonify({'error': 'Perfil no encontrado'}), 404
        
        meals_per_day = profile['meals_per_day']
        target_calories = profile.get('target_calories', 2000)
        
        # Generar plan
        plan_entries, error = plan_service.generate_first_week_varied(user_id, meals_per_day, target_calories)
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify({
            'message': 'Plan generado para la primera semana',
            'plan_entries': plan_entries
        }), 201
    
    except Exception as e:
        return jsonify({'error': 'Error interno del servidor', 'details': str(e)}), 500


@bp.route('/plan/current/<int:user_id>', methods=['GET'])
def get_current_plan(user_id):
    """Obtiene el plan actual (semana actual)."""
    try:
        plan_entries, error = plan_service.get_current_plan(user_id)
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify(plan_entries), 200
    
    except Exception as e:
        return jsonify({'error': 'Error interno del servidor', 'details': str(e)}), 500


@bp.route('/plan/update', methods=['PUT'])
def update_plan_entry():
    """Actualiza una entrada del plan con nueva receta."""
    try:
        data = request.get_json()
        if not data or 'user_id' not in data or 'plan_id' not in data or 'new_recipe_id' not in data:
            return jsonify({'error': 'Se requieren user_id, plan_id y new_recipe_id'}), 400
        
        user_id = data['user_id']
        plan_id = data['plan_id']
        new_recipe_id = data['new_recipe_id']
        
        result, error = plan_service.update_plan_entry(user_id, plan_id, new_recipe_id)
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify({'message': 'Plan actualizado'}), 200
    
    except Exception as e:
        return jsonify({'error': 'Error interno del servidor', 'details': str(e)}), 500


@bp.route('/plan/generate-next/<int:user_id>', methods=['POST'])
def generate_next_week(user_id):
    """Genera plan para la próxima semana."""
    try:
        plan_entries, error = plan_service.generate_next_week_plan(user_id)
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify({
            'message': 'Plan generado para la próxima semana',
            'plan_entries': plan_entries
        }), 201
    
    except Exception as e:
        return jsonify({'error': 'Error interno del servidor', 'details': str(e)}), 500


@bp.route('/plan/summary/<int:user_id>', methods=['GET'])
def get_weekly_summary(user_id):
    """Obtiene resumen nutricional de una semana."""
    try:
        week_number = request.args.get('week', default=None, type=int)
        if not week_number:
            # Semana actual
            import datetime
            week_number = datetime.datetime.now().isocalendar()[1]
        
        summary, error = plan_service.get_weekly_summary(user_id, week_number)
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify(summary), 200
    
    except Exception as e:
        return jsonify({'error': 'Error interno del servidor', 'details': str(e)}), 500