"""Servicio para operaciones de usuario."""
from typing import Dict, List, Optional, Tuple
from datetime import datetime

from supabase import Client

from utils.calculations import calculate_tmb, calculate_tdee, calculate_target_calories


class UserService:
    """Servicio para gestionar usuarios y perfiles."""
    
    def __init__(self, supabase: Client):
        self.supabase = supabase
    
    def create_user(self, username: str) -> Tuple[Optional[Dict], Optional[str]]:
        """Crea un nuevo usuario."""
        try:
            # Verificar si usuario existe
            existing = self.supabase.table('users').select('id').eq('email', username).execute()
            if existing.data and len(existing.data) > 0:
                return None, 'Nombre de usuario ya existe'
            
            # Crear usuario (email = username, name = username)
            user_result = self.supabase.table('users').insert({
                'email': username,
                'password_hash': 'no_password',
                'name': username
            }).execute()
            
            if not user_result.data:
                return None, 'Error al crear usuario'
            
            user_id = user_result.data[0]['id']
            return {'id': user_id, 'username': username}, None
        
        except Exception as e:
            return None, str(e)
    
    def create_profile(self, user_id: int, profile_data: Dict) -> Tuple[Optional[Dict], Optional[str]]:
        """Crea perfil de usuario."""
        try:
            tmb = calculate_tmb(
                profile_data['age'],
                profile_data['gender'],
                profile_data['height'],
                profile_data['current_weight']
            )
            tdee = calculate_tdee(tmb, profile_data['activity_level'])
            target_calories = calculate_target_calories(
                tdee,
                profile_data['goal_type'],
                profile_data['current_weight'],
                profile_data['goal_weight']
            )
            
            profile_result = self.supabase.table('user_profiles').insert({
                'user_id': user_id,
                'age': profile_data['age'],
                'gender': profile_data['gender'],
                'height_cm': profile_data['height'],
                'current_weight_kg': profile_data['current_weight'],
                'goal_weight_kg': profile_data['goal_weight'],
                'goal_type': profile_data['goal_type'],
                'activity_level': profile_data['activity_level'],
                'meals_per_day': profile_data['meals_per_day'],
                'allergies': profile_data.get('allergies', ''),
                'disliked_foods': profile_data.get('disliked_foods', '')
            }).execute()
            
            if not profile_result.data:
                return None, 'Error al crear perfil'
            
            # Registrar peso inicial
            week_number = datetime.now().isocalendar()[1]
            self.supabase.table('weight_history').insert({
                'user_id': user_id,
                'weight_kg': profile_data['current_weight'],
                'week_number': week_number
            }).execute()
            
            return {
                'tmb': round(tmb),
                'tdee': round(tdee),
                'target_calories': int(target_calories)
            }, None
        
        except Exception as e:
            return None, str(e)
    
    def update_profile(self, user_id: int, profile_data: Dict) -> Tuple[Optional[Dict], Optional[str]]:
        """Actualiza perfil existente."""
        try:
            # Obtener perfil actual
            current = self.supabase.table('user_profiles').select('*').eq('user_id', user_id).execute()
            if not current.data:
                return None, 'Perfil no encontrado'
            
            # Preparar datos para actualización
            update_data = {'user_id': user_id}
            for field in ['age', 'gender', 'height_cm', 'current_weight_kg', 'goal_weight_kg', 
                          'activity_level', 'meals_per_day', 'allergies', 'disliked_foods', 'goal_type']:
                if field in profile_data and profile_data[field] is not None:
                    update_data[field] = profile_data[field]
            
            # Actualizar
            self.supabase.table('user_profiles').upsert(update_data).execute()
            
            # Recalcular si cambian datos relevantes
            recalc_fields = ['current_weight_kg', 'activity_level', 'goal_weight_kg', 'goal_type', 'age', 'height_cm', 'gender']
            if any(field in profile_data for field in recalc_fields):
                profile = self.supabase.table('user_profiles').select('*').eq('user_id', user_id).execute().data[0]
                tmb = calculate_tmb(profile['age'], profile['gender'], profile['height_cm'], 
                                    profile['current_weight_kg'])
                tdee = calculate_tdee(tmb, profile['activity_level'])
                target = calculate_target_calories(tdee, profile['goal_type'], profile['current_weight_kg'], profile['goal_weight_kg'])
                
                return {
                    'recalculated': True,
                    'tmb': round(tmb),
                    'tdee': round(tdee),
                    'target_calories': int(target)
                }, None
            
            return {'recalculated': False}, None
        
        except Exception as e:
            return None, str(e)
    
    def get_profile(self, user_id: int) -> Tuple[Optional[Dict], Optional[str]]:
        """Obtiene perfil con calorías calculadas."""
        try:
            profile_result = self.supabase.table('user_profiles').select('*').eq('user_id', user_id).execute()
            if not profile_result.data:
                return None, 'Perfil no encontrado'
            
            profile = profile_result.data[0]
            
            # Calcular calorías objetivo dinámicamente
            tmb = calculate_tmb(
                profile['age'],
                profile['gender'],
                profile['height_cm'],
                profile['current_weight_kg'],
                profile['activity_level']
            )
            tdee = calculate_tdee(tmb, profile['activity_level'])
            target_calories = calculate_target_calories(
                tdee,
                profile['goal_type'],
                profile['current_weight_kg'],
                profile['goal_weight_kg']
            )
            
            profile['target_calories'] = int(target_calories)
            return profile, None
        
        except Exception as e:
            return None, str(e)
    
    def record_weight(self, user_id: int, weight: float) -> Tuple[Optional[Dict], Optional[str]]:
        """Registra nuevo peso."""
        try:
            week_number = datetime.now().isocalendar()[1]
            
            self.supabase.table('weight_history').insert({
                'user_id': user_id,
                'weight_kg': weight,
                'week_number': week_number
            }).execute()
            
            # Actualizar peso actual en perfil
            self.supabase.table('user_profiles').update({
                'current_weight_kg': weight
            }).eq('user_id', user_id).execute()
            
            # Recalcular calorías objetivo
            profile_result = self.supabase.table('user_profiles').select('*').eq('user_id', user_id).execute()
            if not profile_result.data:
                return None, 'Perfil no encontrado'
            
            profile = profile_result.data[0]
            tmb = calculate_tmb(profile['age'], profile['gender'], profile['height_cm'], weight)
            tdee = calculate_tdee(tmb, profile['activity_level'])
            target = calculate_target_calories(tdee, profile['goal_type'], weight, profile['goal_weight_kg'])
            
            return {
                'new_target_calories': int(target)
            }, None
        
        except Exception as e:
            return None, str(e)
    
    def get_weight_history(self, user_id: int, limit: int = 30) -> Tuple[Optional[List], Optional[str]]:
        """Obtiene historial de peso."""
        try:
            result = self.supabase.table('weight_history').select('created_at, weight_kg').eq('user_id', user_id).order('created_at', desc=False).limit(limit).execute()
            return result.data if result.data else [], None
        except Exception as e:
            return None, str(e)