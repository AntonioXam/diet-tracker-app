"""
Test script para verificar los 11 endpoints del backend
"""
import requests
import json

BASE_URL = "http://localhost:5000"

def test_endpoint(name, method, url, data=None, headers=None, expected_status=200):
    """Testea un endpoint individual."""
    print(f"\n{'='*60}")
    print(f"Testing: {name}")
    print(f"Method: {method} | URL: {url}")
    
    try:
        if method == 'GET':
            response = requests.get(url, headers=headers)
        elif method == 'POST':
            response = requests.post(url, json=data, headers=headers)
        else:
            print(f"ERROR: Método {method} no soportado")
            return False
        
        print(f"Status: {response.status_code} (expected: {expected_status})")
        
        if response.status_code == expected_status:
            print("✓ SUCCESS")
            if response.text:
                try:
                    result = response.json()
                    print(f"Response: {json.dumps(result, indent=2)[:500]}")
                except:
                    print(f"Response: {response.text[:200]}")
            return True
        else:
            print(f"✗ FAILED - Status mismatch")
            print(f"Response: {response.text[:500]}")
            return False
            
    except Exception as e:
        print(f"✗ ERROR: {str(e)}")
        return False

def run_all_tests():
    """Ejecuta todos los tests de endpoints."""
    print("\n" + "="*60)
    print("TEST DE ENDPOINTS - DIET TRACKER API")
    print("="*60)
    
    results = []
    auth_token = None
    
    # Endpoint 1: POST /api/onboarding
    onboarding_data = {
        "age": 30,
        "gender": "male",
        "height": 175,
        "current_weight": 80,
        "goal_weight": 75,
        "goal_type": "lose",
        "activity_level": "moderate",
        "meals_per_day": 4,
        "allergies": "",
        "disliked_foods": ""
    }
    
    result = test_endpoint(
        "1. POST /api/onboarding - Calcula TMB + TDEE",
        "POST", f"{BASE_URL}/api/onboarding",
        data=onboarding_data,
        expected_status=201
    )
    results.append(("Onboarding", result))
    
    if result:
        # Guardar token para tests posteriores
        try:
            response = requests.post(f"{BASE_URL}/api/onboarding", json=onboarding_data)
            if response.status_code == 201:
                auth_token = response.json().get('token')
        except:
            pass
    
    # Si no hay token, hacer login o register primero
    if not auth_token:
        print("\n⚠ No se pudo obtener token. Creando usuario de test...")
        register_data = {
            "name": "Test User",
            "email": f"test_{requests.utils.quote(str(__import__('time').time()))}@test.com",
            "password": "test123"
        }
        try:
            resp = requests.post(f"{BASE_URL}/api/register", json=register_data)
            if resp.status_code == 201:
                auth_token = resp.json().get('token')
                print(f"✓ Usuario creado, token obtenido")
        except Exception as e:
            print(f"✗ Error creando usuario: {e}")
    
    headers = {'Authorization': f'Bearer {auth_token}'} if auth_token else {}
    
    # Endpoint 2: GET /api/profile
    result = test_endpoint(
        "2. GET /api/profile - Perfil usuario",
        "GET", f"{BASE_URL}/api/profile",
        headers=headers,
        expected_status=200 if auth_token else 401
    )
    results.append(("Get Profile", result))
    
    # Endpoint 3: POST /api/profile
    profile_update = {
        "age": 31,
        "activity_level": "active"
    }
    result = test_endpoint(
        "3. POST /api/profile - Actualiza perfil",
        "POST", f"{BASE_URL}/api/profile",
        data=profile_update,
        headers=headers,
        expected_status=200 if auth_token else 401
    )
    results.append(("Update Profile", result))
    
    # Endpoint 4: GET /api/recipes
    result = test_endpoint(
        "4. GET /api/recipes - Lista recetas con filtros",
        "GET", f"{BASE_URL}/api/recipes?limit=5",
        expected_status=200
    )
    results.append(("Get Recipes", result))
    
    # Endpoint 5: GET /api/plan
    result = test_endpoint(
        "5. GET /api/plan - Plan semanal usuario",
        "GET", f"{BASE_URL}/api/plan",
        headers=headers,
        expected_status=200 if auth_token else 401
    )
    results.append(("Get Plan", result))
    
    # Endpoint 6: POST /api/plan/swap (necesita plan_id y recipe_id válidos)
    # Skip this for now as it requires existing data
    print(f"\n{'='*60}")
    print("6. POST /api/plan/swap - Cambia comida del plan")
    print("⊘ SKIPPED - Requires existing plan data")
    results.append(("Plan Swap", "SKIPPED"))
    
    # Endpoint 7: GET /api/shopping-list
    result = test_endpoint(
        "7. GET /api/shopping-list - Lista de compra",
        "GET", f"{BASE_URL}/api/shopping-list",
        headers=headers,
        expected_status=200 if auth_token else 401
    )
    results.append(("Shopping List", result))
    
    # Endpoint 8: POST /api/weight
    weight_data = {"weight": 79.5}
    result = test_endpoint(
        "8. POST /api/weight - Registra peso",
        "POST", f"{BASE_URL}/api/weight",
        data=weight_data,
        headers=headers,
        expected_status=200 if auth_token else 401
    )
    results.append(("Register Weight", result))
    
    # Endpoint 9: GET /api/stats
    result = test_endpoint(
        "9. GET /api/stats - Estadísticas/progreso",
        "GET", f"{BASE_URL}/api/stats",
        headers=headers,
        expected_status=200 if auth_token else 401
    )
    results.append(("Get Stats", result))
    
    # Endpoint 10: POST /api/food-log
    food_log_data = {
        "recipe_id": 1,
        "meal_type": "desayuno",
        "calories": 350,
        "protein": 20,
        "carbs": 40,
        "fat": 10,
        "notes": "Test log"
    }
    result = test_endpoint(
        "10. POST /api/food-log - Registra comida del día",
        "POST", f"{BASE_URL}/api/food-log",
        data=food_log_data,
        headers=headers,
        expected_status=201 if auth_token else 401
    )
    results.append(("Food Log", result))
    
    # Endpoint 11: GET /api/dashboard
    result = test_endpoint(
        "11. GET /api/dashboard - Dashboard completo",
        "GET", f"{BASE_URL}/api/dashboard",
        headers=headers,
        expected_status=200 if auth_token else 401
    )
    results.append(("Dashboard", result))
    
    # Summary
    print("\n" + "="*60)
    print("RESUMEN DE TESTS")
    print("="*60)
    
    passed = sum(1 for _, r in results if r is True)
    failed = sum(1 for _, r in results if r is False)
    skipped = sum(1 for _, r in results if r == "SKIPPED")
    
    for name, result in results:
        status = "✓" if result is True else ("✗" if result is False else "⊘")
        print(f"{status} {name}")
    
    print(f"\nTotal: {passed} passed, {failed} failed, {skipped} skipped")
    print("="*60)
    
    return passed, failed, skipped

if __name__ == '__main__':
    run_all_tests()
