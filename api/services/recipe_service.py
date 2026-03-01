"""Servicio para operaciones con recetas."""
from typing import Dict, List, Optional, Tuple
from datetime import datetime

from supabase import Client


class RecipeService:
    """Servicio para gestionar recetas y banco de alimentos."""
    
    def __init__(self, supabase: Client):
        self.supabase = supabase
    
    def get_recipes_by_meal_type(self, meal_type: str, limit: int = 20) -> Tuple[Optional[List], Optional[str]]:
        """Obtiene recetas por tipo de comida."""
        try:
            result = self.supabase.table('master_recipes').select('*').eq('meal_type', meal_type).limit(limit).execute()
            return result.data if result.data else [], None
        except Exception as e:
            return None, str(e)
    
    def get_all_recipes(self) -> Tuple[Optional[List], Optional[str]]:
        """Obtiene todas las recetas."""
        try:
            result = self.supabase.table('master_recipes').select('*').execute()
            return result.data if result.data else [], None
        except Exception as e:
            return None, str(e)
    
    def get_food_bank(self, user_id: int) -> Tuple[Optional[List], Optional[str]]:
        """Obtiene banco de alimentos del usuario."""
        try:
            result = self.supabase.table('user_food_bank').select('*').eq('user_id', user_id).execute()
            return result.data if result.data else [], None
        except Exception as e:
            return None, str(e)
    
    def add_to_food_bank(self, user_id: int, meal_type: str, recipe_id: int) -> Tuple[Optional[Dict], Optional[str]]:
        """Añade receta al banco de alimentos."""
        try:
            week_number = datetime.now().isocalendar()[1]
            
            # Verificar si ya existe
            existing = self.supabase.table('user_food_bank').select('id').eq('user_id', user_id).eq('recipe_id', recipe_id).execute()
            if existing.data:
                return None, 'Receta ya está en el banco'
            
            result = self.supabase.table('user_food_bank').insert({
                'user_id': user_id,
                'meal_type': meal_type,
                'recipe_id': recipe_id,
                'times_used': 0,
                'added_week': week_number
            }).execute()
            
            return result.data[0] if result.data else {}, None
        except Exception as e:
            return None, str(e)
    
    def remove_from_food_bank(self, user_id: int, recipe_id: int) -> Tuple[bool, Optional[str]]:
        """Elimina receta del banco de alimentos."""
        try:
            self.supabase.table('user_food_bank').delete().eq('user_id', user_id).eq('recipe_id', recipe_id).execute()
            return True, None
        except Exception as e:
            return False, str(e)
    
    def get_available_recipes_for_meal(self, user_id: int, meal_type: str) -> Tuple[Optional[List], Optional[str]]:
        """Obtiene recetas disponibles para un tipo de comida (del banco del usuario)."""
        try:
            result = self.supabase.table('user_food_bank').select('recipe_id').eq('user_id', user_id).eq('meal_type', meal_type).execute()
            if not result.data:
                return [], None
            
            recipe_ids = [r['recipe_id'] for r in result.data]
            recipes_result = self.supabase.table('master_recipes').select('*').in_('id', recipe_ids).execute()
            return recipes_result.data if recipes_result.data else [], None
        except Exception as e:
            return None, str(e)
    
    def increment_recipe_usage(self, user_id: int, recipe_id: int) -> Tuple[bool, Optional[str]]:
        """Incrementa el contador de uso de una receta."""
        try:
            self.supabase.table('user_food_bank').update({'times_used': 1}).eq('user_id', user_id).eq('recipe_id', recipe_id).execute()
            return True, None
        except Exception as e:
            return False, str(e)
    
    def get_popular_recipes(self, limit: int = 10) -> Tuple[Optional[List], Optional[str]]:
        """Obtiene recetas más populares por uso."""
        try:
            # Esto requiere una consulta más compleja; simplificamos: recetas con mayor times_used
            result = self.supabase.table('user_food_bank').select('recipe_id, times_used').order('times_used', desc=True).limit(limit).execute()
            if not result.data:
                return [], None
            
            # Obtener detalles de recetas
            recipe_ids = [r['recipe_id'] for r in result.data]
            recipes_result = self.supabase.table('master_recipes').select('*').in_('id', recipe_ids).execute()
            return recipes_result.data if recipes_result.data else [], None
        except Exception as e:
            return None, str(e)