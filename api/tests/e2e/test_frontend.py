"""
End-to-end tests for the Diet Tracker frontend using Playwright.
"""
import pytest
import os
import re
from playwright.sync_api import expect

@pytest.fixture(scope='session')
def frontend_url():
    """URL for the frontend HTML file."""
    # frontend is at diet-tracker-app/frontend/index.html
    # This file is at diet-tracker-app/api/tests/e2e/test_frontend.py
    frontend_path = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            '..', '..', '..', 'frontend', 'index.html'
        )
    )
    assert os.path.exists(frontend_path), f"Frontend not found at {frontend_path}"
    return f'file://{frontend_path}'

def test_frontend_loads(page, frontend_url):
    """Test that the frontend page loads and contains expected elements."""
    # Capture console errors
    errors = []
    page.on('console', lambda msg: errors.append(msg) if msg.type == 'error' else None)
    
    page.goto(frontend_url)
    # Check title
    assert page.title() == 'Diet Tracker FIT - Premium'
    # Check main heading text
    heading = page.locator('h1')
    assert heading.count() == 1
    assert 'Transforma tu' in heading.inner_text()
    # Check that register and login buttons exist
    assert page.locator('button:has-text("Registrarse")').count() >= 1
    assert page.locator('button:has-text("Entrar")').count() >= 1
    # Ensure no JavaScript errors
    assert len(errors) == 0, f'JavaScript errors: {errors}'

def test_register_modal_opens(page, frontend_url):
    """Test that clicking the register button opens the modal."""
    page.goto(frontend_url)
    # Check that modal is initially hidden
    modal = page.locator('#modal-register')
    assert modal.count() == 1
    # The modal has class 'hidden' (Tailwind)
    expect(modal).to_have_class(re.compile(r"hidden"))
    # Click register button
    page.locator('button:has-text("Registrarse")').first.click()
    # Wait for modal to become visible (hidden class removed)
    expect(modal).not_to_have_class(re.compile(r"hidden"), timeout=5000)
    # Modal should be visible
    expect(modal).to_be_visible()
    # Check that modal contains some registration text
    expect(modal).to_contain_text('Crear cuenta')

def test_register_form_submission(page, frontend_url):
    """Test that the registration form submits correctly (mocked)."""
    page.goto(frontend_url)
    # Fill registration form
    page.fill('input[name="username"]', 'testuser_e2e')
    page.fill('input[name="age"]', '30')
    page.select_option('select[name="gender"]', 'male')
    page.fill('input[name="height"]', '180')
    page.fill('input[name="current_weight"]', '80')
    page.fill('input[name="goal_weight"]', '75')
    page.select_option('select[name="goal_type"]', 'lose')
    page.select_option('select[name="activity_level"]', 'moderate')
    page.select_option('select[name="meals_per_day"]', '4')
    
    # Intercept the fetch request to /api/register and respond with mock
    async def handle_route(route):
        await route.fulfill(json={
            'success': True,
            'user': {'id': 999},
            'target_calories': 2200
        })
    page.route('**/api/register', handle_route)
    
    # Click register button
    page.click('button#register-btn')
    # Wait for response (the frontend shows a success message)
    page.wait_for_selector('#register-result', state='visible', timeout=5000)
    # Ensure success message appears
    result = page.locator('#register-result')
    assert result.count() == 1
    assert 'registered' in result.inner_text().lower()

def test_login_form_submission(page, frontend_url):
    """Test login form submission."""
    page.goto(frontend_url)
    # Fill login form
    page.fill('input[name="login_username"]', 'testuser')
    # Mock the /api/login response
    async def handle_route(route):
        await route.fulfill(json={
            'success': True,
            'user': {'id': 123, 'username': 'testuser'}
        })
    page.route('**/api/login', handle_route)
    page.click('button#login-btn')
    # Wait for user info to appear
    page.wait_for_selector('#user-info', state='visible', timeout=5000)
    assert page.locator('#user-info').count() == 1

def test_plan_loading(page, frontend_url):
    """Test that weekly plan can be fetched (mocked)."""
    page.goto(frontend_url)
    # First login (mock)
    async def handle_login(route):
        await route.fulfill(json={'success': True, 'user': {'id': 123}})
    page.route('**/api/login', handle_login)
    page.fill('input[name="login_username"]', 'testuser')
    page.click('button#login-btn')
    page.wait_for_selector('#plan-section', state='visible')
    
    # Mock plan data
    async def handle_plan(route):
        await route.fulfill(json={
            'week': 10,
            'meals': [
                {
                    'day_of_week': 1,
                    'meal_type': 'desayuno',
                    'recipe_name': 'Test Recipe',
                    'calories': 300
                }
            ],
            'daily_totals': {}
        })
    page.route('**/api/plan/current*', handle_plan)
    # Trigger plan load (frontend may auto-load after login)
    # Click a reload button if exists, else just wait
    page.wait_for_timeout(1000)
    # Check that plan table appears
    assert page.locator('#plan-table').count() == 1