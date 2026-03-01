"""
Pytest configuration and shared fixtures for Diet Tracker API tests.
"""
import pytest
import sys
import os
from unittest.mock import MagicMock, patch

# Add the parent directory to the Python path so we can import app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def pytest_configure(config):
    """Set environment variables before any test imports."""
    os.environ['SUPABASE_URL'] = 'https://mock.supabase.co'
    os.environ['SUPABASE_KEY'] = 'mock-key'

@pytest.fixture
def mock_supabase(mocker):
    """
    Mock Supabase client and reload app module to use the mock.
    """
    # Patch create_client to return a mock
    mock_client = MagicMock()
    mocker.patch('supabase.create_client', return_value=mock_client)
    # Also patch app.supabase directly
    mocker.patch('app.supabase', new=mock_client)
    # Force reload of app module to ensure mocked supabase is used
    if 'app' in sys.modules:
        del sys.modules['app']
    import app
    # Re-apply the patch after reload (the mocker patch should persist)
    mocker.patch('app.supabase', new=mock_client)
    return mock_client

@pytest.fixture
def app(mock_supabase):
    """Flask application with mocked Supabase."""
    import app
    app.app.config['TESTING'] = True
    return app.app

@pytest.fixture
def client(app):
    """Flask test client."""
    with app.test_client() as test_client:
        yield test_client

@pytest.fixture
def sample_user_data():
    """Sample user registration data."""
    return {
        'username': 'testuser',
        'age': 30,
        'gender': 'male',
        'height': 180,
        'current_weight': 80,
        'goal_weight': 75,
        'goal_type': 'lose',
        'activity_level': 'moderate',
        'meals_per_day': 4
    }

@pytest.fixture
def sample_recipe():
    """Sample recipe data."""
    return {
        'id': 1,
        'name': 'Test Recipe',
        'meal_type': 'desayuno',
        'calories': 300,
        'protein': 20,
        'carbs': 30,
        'fat': 10,
        'ingredients': 'Ingredient 1, Ingredient 2',
        'instructions': 'Do something',
        'supermarket': 'mixto',
        'category': 'salado'
    }