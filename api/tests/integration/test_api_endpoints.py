"""
Integration tests for Flask API endpoints using mocked Supabase.
"""
import json
import pytest
from unittest.mock import patch, MagicMock

def test_health_endpoint(client):
    """Test health check endpoint."""
    response = client.get('/api/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'ok'
    assert 'timestamp' in data

def test_register_success(client, mock_supabase, sample_user_data):
    """Test successful user registration."""
    # Mock Supabase responses
    mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value.data = []
    mock_supabase.table.return_value.insert.return_value.execute.return_value.data = [{'id': 123}]

    # Mock calculate_tmb and calculate_deficit? They are internal functions, we can let them run.
    # But we need to mock the seed_recipes? We'll mock the supabase calls inside generate_first_week_varied.
    # For simplicity, we'll mock the whole generate_first_week_varied function.
    with patch('app.generate_first_week_varied') as mock_generate:
        response = client.post('/api/register', json=sample_user_data)
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] == True
        assert data['user']['id'] == 123
        assert 'target_calories' in data
        mock_generate.assert_called_once()

def test_register_missing_fields(client):
    """Test registration with missing fields."""
    incomplete_data = {'username': 'test'}
    response = client.post('/api/register', json=incomplete_data)
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data

def test_register_existing_user(client, mock_supabase, sample_user_data):
    """Test registration with existing username."""
    mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value.data = [{'id': 1}]
    response = client.post('/api/register', json=sample_user_data)
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data

def test_login_success(client, mock_supabase):
    """Test successful login."""
    # First call: table('users')
    users_mock = MagicMock()
    users_mock.select.return_value.eq.return_value.execute.return_value.data = [
        {'id': 123, 'email': 'testuser', 'name': 'testuser'}
    ]
    # Second call: table('user_profiles')
    profiles_mock = MagicMock()
    profiles_mock.select.return_value.eq.return_value.execute.return_value.data = [
        {'age': 30, 'gender': 'male', 'height_cm': 180, 'current_weight_kg': 80, 'goal_weight_kg': 75,
         'goal_type': 'lose', 'activity_level': 'moderate', 'meals_per_day': 4}
    ]
    # Make table() return different mocks on consecutive calls
    mock_supabase.table.side_effect = [users_mock, profiles_mock]

    response = client.post('/api/login', json={'username': 'testuser'})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] == True
    assert data['user']['id'] == 123

def test_login_user_not_found(client, mock_supabase):
    """Test login with non-existing username."""
    mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value.data = []
    response = client.post('/api/login', json={'username': 'nonexistent'})
    assert response.status_code == 404
    data = json.loads(response.data)
    assert 'error' in data

def test_get_profile_success(client, mock_supabase):
    """Test get profile endpoint."""
    profile_data = {
        'age': 30, 'gender': 'male', 'height_cm': 180, 'current_weight_kg': 80,
        'goal_weight_kg': 75, 'goal_type': 'lose', 'activity_level': 'moderate', 'meals_per_day': 4
    }
    mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value.data = [profile_data]
    response = client.get('/api/profile/get?user_id=123')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'profile' in data
    assert data['profile']['target_calories']  # Should be added by endpoint

def test_get_profile_not_found(client, mock_supabase):
    """Test get profile when user doesn't exist."""
    mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value.data = []
    response = client.get('/api/profile/get?user_id=999')
    assert response.status_code == 404

def test_update_profile_success(client, mock_supabase):
    """Test profile update."""
    # Mock existing profile
    mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value.data = [
        {'age': 30, 'gender': 'male', 'height_cm': 180, 'current_weight_kg': 80,
         'goal_weight_kg': 75, 'activity_level': 'moderate', 'meals_per_day': 4, 'goal_type': 'lose'}
    ]
    # Mock upsert
    mock_supabase.table.return_value.upsert.return_value.execute.return_value.data = None

    update_data = {
        'user_id': 123,
        'age': 31,
        'current_weight_kg': 79
    }
    response = client.post('/api/profile/update', json=update_data)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] == True

def test_get_current_plan(client, mock_supabase):
    """Test fetching current weekly plan."""
    # Mock get_week_number to return a fixed week
    with patch('app.get_week_number', return_value=10):
        # Mock supabase.table('weekly_plans').select('*').eq('user_id', ...).eq('week_number', ...).order('day_of_week').execute()
        weekly_result = MagicMock()
        weekly_result.data = [
            {'id': 1, 'user_id': 123, 'week_number': 10, 'day_of_week': 1, 'meal_type': 'desayuno',
             'selected_recipe_id': 1, 'calories': 300, 'protein': 20, 'carbs': 30, 'fat': 10}
        ]
        # Build chain
        weekly_mock = MagicMock()
        weekly_mock.select.return_value.eq.return_value.eq.return_value.order.return_value.execute.return_value = weekly_result

        # Mock supabase.table('master_recipes').select(...).eq('id', ...).execute()
        recipe_result = MagicMock()
        recipe_result.data = [
            {'id': 1, 'name': 'Test Recipe', 'ingredients': 'ing1', 'instructions': 'do', 'supermarket': 'mixto', 'category': 'salado', 'image_url': None}
        ]
        recipes_mock = MagicMock()
        recipes_mock.select.return_value.eq.return_value.execute.return_value = recipe_result

        # Make table() return different mocks on consecutive calls
        mock_supabase.table.side_effect = [weekly_mock, recipes_mock]

        response = client.get('/api/plan/current?user_id=123')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'week' in data
        assert 'meals' in data
        assert len(data['meals']) == 1

def test_swap_meal_success(client, mock_supabase):
    """Test swapping a meal in the plan."""
    mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value.data = [
        {'id': 1, 'name': 'New Recipe', 'calories': 350, 'protein': 25, 'carbs': 40, 'fat': 12}
    ]
    swap_data = {
        'user_id': 123,
        'day': 1,
        'meal_type': 'desayuno',
        'new_recipe_id': 2
    }
    response = client.post('/api/plan/swap', json=swap_data)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] == True

def test_weight_checkin(client, mock_supabase):
    """Test weight checkin endpoint."""
    # Mock get_week_number to return a fixed week
    with patch('app.get_week_number', return_value=10):
        # Mock data
        user_id = 123
        weight = 79.5
        meals_per_day = 4
        meal_types = ['desayuno', 'comida', 'merienda', 'cena']
        
        # 1. weight_history insert mock
        weight_history_mock = MagicMock()
        weight_history_mock.insert.return_value.execute.return_value.data = None
        
        # 2. user_profiles select mock
        profile_data = {
            'age': 30, 'gender': 'male', 'height_cm': 180, 'current_weight_kg': 80,
            'goal_weight_kg': 75, 'activity_level': 'moderate', 'meals_per_day': meals_per_day,
            'goal_type': 'lose', 'user_id': user_id
        }
        user_profiles_mock = MagicMock()
        user_profiles_mock.select.return_value.eq.return_value.execute.return_value.data = [profile_data]
        
        # 3. user_food_bank select mocks (one per meal_type)
        # Each returns 6 existing recipe_ids (so no new recipes are added)
        food_bank_mocks = []
        for _ in meal_types:
            fb_mock = MagicMock()
            fb_mock.select.return_value.eq.return_value.eq.return_value.execute.return_value.data = [
                {'recipe_id': i} for i in range(1, 7)  # 6 existing recipes
            ]
            food_bank_mocks.append(fb_mock)
        
        # 4. master_recipes select mocks (should not be called because existing_ids >= 6)
        # But we still need to mock them in case the condition fails. We'll create dummy mocks.
        master_mocks = []
        for _ in meal_types:
            mm = MagicMock()
            mm.select.return_value.eq.return_value.not_.return_value.limit.return_value.execute.return_value.data = []
            master_mocks.append(mm)
        
        # 5. user_food_bank insert mocks (should not be called)
        insert_mocks = []
        for _ in meal_types:
            im = MagicMock()
            im.insert.return_value.execute.return_value.data = None
            insert_mocks.append(im)
        
        # Build side_effect list for supabase.table calls in order:
        # weight_history, user_profiles, then for each meal_type: user_food_bank (select), (skip master_recipes and insert)
        side_effect_list = [weight_history_mock, user_profiles_mock]
        for i in range(len(meal_types)):
            side_effect_list.append(food_bank_mocks[i])
            # master_recipes and insert not called because existing_ids >= 6
        # Add extra mocks for safety (they won't be used)
        side_effect_list.extend(master_mocks)
        side_effect_list.extend(insert_mocks)
        
        mock_supabase.table.side_effect = side_effect_list
        
        checkin_data = {'user_id': user_id, 'weight': weight}
        response = client.post('/api/weight/checkin', json=checkin_data)
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] == True
        assert 'new_target_calories' in data
        # Ensure target calories is an integer
        assert isinstance(data['new_target_calories'], int)

def test_shopping_list(client, mock_supabase):
    """Test shopping list generation."""
    # Mock weekly plan
    mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value.data = [
        {'selected_recipe_id': 1}
    ]
    # Mock recipes
    mock_supabase.table.return_value.select.return_value.in_.return_value.execute.return_value.data = [
        {'ingredients': 'Ingredient 1, Ingredient 2', 'supermarket': 'mercadona'}
    ]
    response = client.get('/api/shopping-list?user_id=123')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'shopping_list' in data
    assert 'mercadona' in data['shopping_list']