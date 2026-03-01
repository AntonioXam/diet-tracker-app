"""Servicio para planes semanales."""
from typing import Dict, List, Optional, Tuple
import random
from datetime import datetime

from supabase import Client

from utils.calculations import get_meal_types_for_count


class PlanService:
    """Servicio para generar y gestionar planes semanales."""
    
    def __init__(self, supabase: Client):
        self.supabase = supabase
    
    def generate_first_week_varied(self, user_id: int, meals_per_day: int, target_calories: int) -> Tuple[Optional[List], Optional[str]]:
        """Genera la primera semana con recetas variadas."""
        try:
            # Obtener todas las recetas agrupadas por tipo de comida
            all_recipes = self.supabase.table('master_recipes').select('*').execute()
            if not all_recipes.data:
                return None, 'No hay recetas disponibles'
            
            recipes_by_meal = {}
            for recipe in all_recipes.data:
                meal_type = recipe['meal_type']
                if meal_type not in recipes_by_meal:
                    recipes_by_meal[meal_type] = []
                recipes_by_meal[meal_type].append(recipe)
            
            # Determinar tipos de comida según meals_per_day
            meal_types = get_meal_types_for_count(meals_per_day)
            
            # Generar plan para 7 días
            week_number = datetime.now().isocalendar()[1]
            plan_entries = []
            
            for day in range(7):
                for meal_type in meal_types:
                    # Filtrar recetas del tipo correspondiente
                    available = recipes_by_meal.get(meal_type, [])
                    if not available:
                        continue
                    
                    # Seleccionar receta aleatoria
                    recipe = random.choice(available)
                    
                    plan_entries.append({
                        'user_id': user_id,
                        'week_number': week_number,
                        'day_of_week': day,
                        'meal_type': meal_type,
                        'selected_recipe_id': recipe['id'],
                        'calories': recipe['calories'],
                        'protein': recipe['protein'],
                        'carbs': recipe['carbs'],
                        'fat': recipe['fat']
                    })
            
            # Insertar todas las entradas
            if plan_entries:
                self.supabase.table('weekly_plans').insert(plan_entries).execute()
            
            return plan_entries, None
        
        except Exception as e:
            return None, str(e)
    
    def get_current_plan(self, user_id: int) -> Tuple[Optional[List], Optional[str]]:
        """Obtiene el plan actual (semana actual)."""
        try:
            week_number = datetime.now().isocalendar()[1]
            result = self.supabase.table('weekly_plans').select('*').eq('user_id', user_id).eq('week_number', week_number).execute()
            return result.data if result.data else [], None
        except Exception as e:
            return None, str(e)
    
    def update_plan_entry(self, user_id: int, plan_id: int, new_recipe_id: int) -> Tuple[Optional[Dict], Optional[str]]:
        """Actualiza una entrada del plan con nueva receta."""
        try:
            # Obtener datos de la nueva receta
            recipe_result = self.supabase.table('master_recipes').select('*').eq('id', new_recipe_id).execute()
            if not recipe_result.data:
                return None, 'Receta no encontrada'
            
            recipe = recipe_result.data[0]
            
            # Actualizar entrada
            self.supabase.table('weekly_plans').update({
                'selected_recipe_id': new_recipe_id,
                'calories': recipe['calories'],
                'protein': recipe['protein'],
                'carbs': recipe['carbs'],
                'fat': recipe['fat']
            }).eq('id', plan_id).execute()
            
            # Incrementar uso en food bank
            self.supabase.table('user_food_bank').update({'times_used': 1}).eq('user_id', user_id).eq('recipe_id', new_recipe_id).execute()
            
            return {'updated': True}, None
        
        except Exception as e:
            return None, str(e)
    
    def generate_next_week_plan(self, user_id: int) -> Tuple[Optional[List], Optional[str]]:
        """Genera plan para la próxima semana basado en preferencias."""
        try:
            # Obtener perfil para conocer meals_per_day
            profile_result = self.supabase.table('user_profiles').select('meals_per_day').eq('user_id', user_id).execute()
            if not profile_result.data:
                return None, 'Perfil no encontrado'
            
            meals_per_day = profile_result.data[0]['meals_per_day']
            meal_types = get_meal_types_for_count(meals_per_day)
            
            # Obtener banco de alimentos del usuario
            food_bank_result = self.supabase.table('user_food_bank').select('recipe_id, meal_type').eq('user_id', user_id).execute()
            if not food_bank_result.data:
                return None, 'Banco de alimentos vacío'
            
            # Agrupar recetas por tipo de comida
            recipes_by_meal = {}
            for item in food_bank_result.data:
                meal_type = item['meal_type']
                if meal_type not in recipes_by_meal:
                    recipes_by_meal[meal_type] = []
                recipes_by_meal[meal_type].append(item['recipe_id'])
            
            # Obtener detalles de todas las recetas del banco
            all_recipe_ids = set()
            for ids in recipes_by_meal.values():
                all_recipe_ids.update(ids)
            
            if not all_recipe_ids:
                return None, 'Banco de alimentos vacío'
            
            recipes_result = self.supabase.table('master_recipes').select('*').in_('id', list(all_recipe_ids)).execute()
            recipes_dict = {r['id']: r for r in recipes_result.data}
            
            # Generar plan
            week_number = datetime.now().isocalendar()[1] + 1
            plan_entries = []
            
            for day in range(7):
                for meal_type in meal_types:
                    # Obtener recetas disponibles para este tipo
                    available_ids = recipes_by_meal.get(meal_type, [])
                    if not available_ids:
                        # Si no hay, buscar recetas maestras del mismo tipo
                        fallback = self.supabase.table('master_recipes').select('*').eq('meal_type', meal_type).limit(5).execute()
                        if not fallback.data:
                            continue
                        recipe = random.choice(fallback.data)
                    else:
                        # Seleccionar receta menos usada
                        usage_counts = []
                        for recipe_id in available_ids:
                            usage = self.supabase.table('user_food_bank').select('times_used').eq('user_id', user_id).eq('recipe_id', recipe_id).execute()
                            times_used = usage.data[0]['times_used'] if usage.data else 0
                            usage_counts.append((recipe_id, times_used))
                        
                        # Ordenar por menor uso
                        usage_counts.sort(key=lambda x: x[1])
                        selected_id = usage_counts[0][0]
                        recipe = recipes_dict.get(selected_id)
                        if not recipe:
                            continue
                    
                    plan_entries.append({
                        'user_id': user_id,
                        'week_number': week_number,
                        'day_of_week': day,
                        'meal_type': meal_type,
                        'selected_recipe_id': recipe['id'],
                        'calories': recipe['calories'],
                        'protein': recipe['protein'],
                        'carbs': recipe['carbs'],
                        'fat': recipe['fat']
                    })
            
            # Insertar plan
            if plan_entries:
                self.supabase.table('weekly_plans').insert(plan_entries).execute()
            
            return plan_entries, None
        
        except Exception as e:
            return None, str(e)
    
    def get_weekly_summary(self, user_id: int, week_number: int) -> Tuple[Optional[Dict], Optional[str]]:
        """Resumen nutricional de una semana."""
        try:
            result = self.supabase.table('weekly_plans').select('calories, protein, carbs, fat').eq('user_id', user_id).eq('week_number', week_number).execute()
            if not result.data:
                return None, 'Plan no encontrado'
            
            total_calories = sum(r['calories'] or 0 for r in result.data)
            total_protein = sum(r['protein'] or 0 for r in result.data)
            total_carbs = sum(r['carbs'] or 0 for r in result.data)
            total_fat = sum(r['fat'] or 0 for r in result.data)
            
            return {
                'week': week_number,
                'total_calories': total_calories,
                'total_protein': total_protein,
                'total_carbs': total_carbs,
                'total_fat': total_fat,
                'average_daily_calories': total_calories / 7,
                'average_daily_protein': total_protein / 7,
                'average_daily_carbs': total_carbs / 7,
                'average_daily_fat': total_fat / 7
            }, None
        
        except Exception as e:
            return None, str(e)