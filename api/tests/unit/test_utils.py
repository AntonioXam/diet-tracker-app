"""
Unit tests for utility functions in app.py.
"""
import hashlib
from datetime import datetime
from app import hash_password, calculate_tmb, calculate_deficit, get_week_number, get_meal_types_for_count

def test_hash_password():
    """Test password hashing."""
    password = 'mypassword'
    expected_hash = hashlib.sha256(password.encode()).hexdigest()
    assert hash_password(password) == expected_hash
    # Different password gives different hash
    assert hash_password('other') != expected_hash

def test_calculate_tmb_male():
    """Test TMB calculation for male."""
    tmb, tdee = calculate_tmb(age=30, gender='male', height=180, weight=80, activity_level='moderate')
    # Mifflin-St Jeor formula for male: 10*weight + 6.25*height - 5*age + 5
    expected_tmb = 10*80 + 6.25*180 - 5*30 + 5
    expected_tdee = expected_tmb * 1.55  # moderate multiplier
    assert tmb == expected_tmb
    assert tdee == expected_tdee

def test_calculate_tmb_female():
    """Test TMB calculation for female."""
    tmb, tdee = calculate_tmb(age=25, gender='female', height=165, weight=60, activity_level='light')
    expected_tmb = 10*60 + 6.25*165 - 5*25 - 161
    expected_tdee = expected_tmb * 1.375  # light multiplier
    # Function returns rounded values
    assert tmb == round(expected_tmb)
    assert tdee == round(expected_tdee)

def test_calculate_tmb_unknown_activity():
    """Test TMB calculation with unknown activity level."""
    tmb, tdee = calculate_tmb(age=30, gender='male', height=180, weight=80, activity_level='unknown')
    expected_tmb = 10*80 + 6.25*180 - 5*30 + 5
    expected_tdee = expected_tmb * 1.2  # default sedentary multiplier
    assert tdee == expected_tdee

def test_calculate_deficit_lose():
    """Test calorie deficit for weight loss with default parameters."""
    # Default loss_rate='moderate', gender='female'
    target = calculate_deficit(tdee=2500, goal_type='lose', current_weight=80, goal_weight=75)
    # deficit_per_week = 500, max_deficit = 2500*0.2 = 500, deficit = 500
    # target = 2500 - 500 = 2000, min_calories = 1200 (female), target = max(1200,2000) = 2000
    assert target == 2000
    # Ensure minimum 1200 calories (for female)
    target2 = calculate_deficit(tdee=1400, goal_type='lose', current_weight=80, goal_weight=75)
    # deficit = 500, but max_deficit = 1400*0.2 = 280, deficit = min(500,280)=280
    # target = 1400 - 280 = 1120, min_calories 1200 => target = 1200
    assert target2 == 1200
    # Test with male gender (min_calories 1500)
    target3 = calculate_deficit(tdee=1400, goal_type='lose', current_weight=80, goal_weight=75, gender='male')
    # deficit = 280, target = 1400-280=1120, min_calories 1500 => target = 1500
    assert target3 == 1500
    # Test with tmb provided
    target4 = calculate_deficit(tdee=2500, goal_type='lose', current_weight=80, goal_weight=75, tmb=1800)
    # min_calories = max(1200,1800) = 1800, target = max(1800,2000) = 2000
    assert target4 == 2000
    # Test with loss_rate='slow' (deficit 250)
    target5 = calculate_deficit(tdee=2500, goal_type='lose', current_weight=80, goal_weight=75, loss_rate='slow')
    # deficit = 250, max_deficit = 500, target = 2500-250 = 2250, min_calories 1200
    assert target5 == 2250

def test_calculate_deficit_gain():
    """Test calorie surplus for weight gain."""
    target = calculate_deficit(tdee=2500, goal_type='gain', current_weight=80, goal_weight=85)
    expected = 2500 + 300
    assert target == expected
    # Ensure max 3500 calories
    target2 = calculate_deficit(tdee=3400, goal_type='gain', current_weight=80, goal_weight=85)
    assert target2 == 3500  # 3400+300 = 3700 -> clamped to 3500
    # Edge case: tdee already above max
    target3 = calculate_deficit(tdee=3600, goal_type='gain', current_weight=80, goal_weight=85)
    assert target3 == 3500  # 3600+300 = 3900 -> clamped to 3500

def test_calculate_deficit_maintain():
    """Test calorie target for maintenance."""
    target = calculate_deficit(tdee=2500, goal_type='maintain', current_weight=80, goal_weight=80)
    assert target == 2500

def test_get_week_number():
    """Test week number extraction."""
    week = get_week_number()
    # Should be integer between 1-53
    assert isinstance(week, int)
    assert 1 <= week <= 53
    # Should match today's week number
    expected = datetime.now().isocalendar()[1]
    assert week == expected

def test_get_meal_types_for_count():
    """Test meal type mapping."""
    assert get_meal_types_for_count(3) == ['desayuno', 'comida', 'cena']
    assert get_meal_types_for_count(4) == ['desayuno', 'comida', 'merienda', 'cena']
    assert get_meal_types_for_count(5) == ['desayuno', 'almuerzo', 'comida', 'merienda', 'cena']
    assert get_meal_types_for_count(2) == ['desayuno', 'comida', 'cena']  # default
    assert get_meal_types_for_count(6) == ['desayuno', 'comida', 'cena']  # default