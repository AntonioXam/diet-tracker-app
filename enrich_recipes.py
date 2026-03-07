#!/usr/bin/env python3
"""
Script para enriquecer recetas con ingredientes detallados e instrucciones.
Actualiza las recetas existentes en Supabase.
"""

import json
import requests
from typing import List, Dict, Any, Optional

# Configuración de Supabase
SUPABASE_URL = "https://kaomgwojvnncidyezdzj.supabase.co"
SERVICE_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imthb21nd29qdm5uY2lkeWV6ZHpqIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MjcwNzE3NiwiZXhwIjoyMDg4MjgzMTc2fQ.g9dMyRLD6sK6WeQGywhQaTRAdfu48CG8GW8Va2gmwxk"

HEADERS = {
    "apikey": SERVICE_TOKEN,
    "Authorization": f"Bearer {SERVICE_TOKEN}",
    "Content-Type": "application/json",
    "Prefer": "return=minimal"
}

def get_existing_recipes() -> List[Dict[str, Any]]:
    """Obtener todas las recetas existentes."""
    print("📥 Obteniendo recetas existentes...")
    
    url = f"{SUPABASE_URL}/rest/v1/master_recipes"
    params = {
        "select": "id,name,description,calories,protein_g,carbs_g,fat_g,meal_type",
        "order": "name.asc"
    }
    
    response = requests.get(url, headers=HEADERS, params=params)
    
    if response.status_code == 200:
        recipes = response.json()
        print(f"✓ Encontradas {len(recipes)} recetas")
        return recipes
    else:
        print(f"✗ Error obteniendo recetas: {response.status_code}")
        print(response.text)
        return []

def generate_recipe_data(nombre: str, descripcion: str, meal_type: str, calories: int, protein: float) -> Dict[str, Any]:
    """Generar ingredientes e instrucciones basados en el nombre y descripción."""
    
    nombre_lower = nombre.lower()
    desc_lower = (descripcion or "").lower()
    
    # Base de datos de recetas conocidas
    recipe_database = {
        "tortilla de claras": {
            "ingredients": [
                {"name": "Claras de huevo", "amount": 4, "unit": "unidades"},
                {"name": "Espinacas frescas", "amount": 100, "unit": "g"},
                {"name": "Aceite de oliva", "amount": 1, "unit": "cucharada"},
                {"name": "Sal", "amount": 1, "unit": "pizca"},
                {"name": "Pimienta negra", "amount": 1, "unit": "pizca"}
            ],
            "instructions": "1. Batir las claras de huevo con sal y pimienta.\n2. Calentar el aceite en una sartén antiadherente.\n3. Añadir las espinacas y saltear 1 minuto.\n4. Verter las claras batidas y cocinar a fuego medio.\n5. Cuajar por ambos lados y servir caliente.",
            "tags": ["desayuno", "proteico", "bajo en calorías", "saludable"],
            "difficulty": "fácil",
            "prep_time": 10
        },
        "tortilla": {
            "ingredients": [
                {"name": "Huevos", "amount": 3, "unit": "unidades"},
                {"name": "Patatas", "amount": 300, "unit": "g"},
                {"name": "Cebolla", "amount": 0.5, "unit": "unidad"},
                {"name": "Aceite de oliva", "amount": 100, "unit": "ml"},
                {"name": "Sal", "amount": 1, "unit": "pizca"}
            ],
            "instructions": "1. Pelar y cortar las patatas en láminas finas.\n2. Pelar y picar la cebolla en juliana.\n3. Calentar el aceite y freír las patatas con la cebolla a fuego medio.\n4. Escurrir el aceite y batir los huevos con sal.\n5. Mezclar todo y cuajar en la sartén.\n6. Dar la vuelta con un plato y terminar de cuajar.",
            "tags": ["almuerzo", "cena", "español", "tradicional"],
            "difficulty": "medio",
            "prep_time": 30
        },
        "huevo": {
            "ingredients": [
                {"name": "Huevo", "amount": 2, "unit": "unidades"},
                {"name": "Aceite de oliva", "amount": 1, "unit": "cucharada"},
                {"name": "Sal", "amount": 1, "unit": "pizca"}
            ],
            "instructions": "1. Calentar el aceite en una sartén antiadherente.\n2. Romper el huevo con cuidado y añadirlo a la sartén.\n3. Cocinar hasta que la clara esté cuajada.\n4. Sazonar con sal y servir.",
            "tags": ["desayuno", "proteína", "rápido"],
            "difficulty": "fácil",
            "prep_time": 5
        },
        "tostada": {
            "ingredients": [
                {"name": "Pan integral", "amount": 2, "unit": "rebanadas"},
                {"name": "Aceite de oliva virgen extra", "amount": 1, "unit": "cucharada"},
                {"name": "Tomate maduro", "amount": 1, "unit": "unidad"},
                {"name": "Sal", "amount": 1, "unit": "pizca"}
            ],
            "instructions": "1. Tostar el pan hasta que esté dorado.\n2. Cortar el tomate por la mitad y frotar sobre el pan.\n3. Añadir aceite de oliva y sal al gusto.\n4. Servir inmediatamente.",
            "tags": ["desayuno", "mediterráneo", "vegetariano"],
            "difficulty": "fácil",
            "prep_time": 5
        },
        "avena": {
            "ingredients": [
                {"name": "Copos de avena", "amount": 50, "unit": "g"},
                {"name": "Leche o bebida vegetal", "amount": 200, "unit": "ml"},
                {"name": "Miel o edulcorante", "amount": 1, "unit": "cucharada"},
                {"name": "Frutos rojos", "amount": 30, "unit": "g"},
                {"name": "Nueces", "amount": 15, "unit": "g"}
            ],
            "instructions": "1. Calentar la leche en un cazo pequeño.\n2. Añadir los copos de avena y remover.\n3. Cocinar a fuego lento 3-5 minutos hasta espesar.\n4. Servir en un bol con frutos rojos y nueces.\n5. Añadir miel al gusto.",
            "tags": ["desayuno", "saludable", "fibra"],
            "difficulty": "fácil",
            "prep_time": 10
        },
        "yogur": {
            "ingredients": [
                {"name": "Yogur natural o griego", "amount": 150, "unit": "g"},
                {"name": "Fruta fresca", "amount": 100, "unit": "g"},
                {"name": "Miel", "amount": 1, "unit": "cucharada"},
                {"name": "Frutos secos", "amount": 15, "unit": "g"}
            ],
            "instructions": "1. Verter el yogur en un bol.\n2. Añadir la fruta troceada.\n3. Espolvorear con frutos secos.\n4. Añadir miel al gusto y servir.",
            "tags": ["desayuno", "postre", "saludable"],
            "difficulty": "fácil",
            "prep_time": 3
        },
        "ensalada": {
            "ingredients": [
                {"name": "Lechuga variada", "amount": 100, "unit": "g"},
                {"name": "Tomate cherry", "amount": 8, "unit": "unidades"},
                {"name": "Pepino", "amount": 0.5, "unit": "unidad"},
                {"name": "Cebolla roja", "amount": 0.25, "unit": "unidad"},
                {"name": "Aceite de oliva", "amount": 2, "unit": "cucharadas"},
                {"name": "Vinagre", "amount": 1, "unit": "cucharada"},
                {"name": "Sal", "amount": 1, "unit": "pizca"}
            ],
            "instructions": "1. Lavar y escurrir bien la lechuga.\n2. Cortar los tomates cherry por la mitad.\n3. Cortar el pepino en rodajas finas.\n4. Picar la cebolla en juliana fina.\n5. Mezclar todo en un bol y aliñar con aceite, vinagre y sal.",
            "tags": ["almuerzo", "cena", "ligero", "vegano"],
            "difficulty": "fácil",
            "prep_time": 10
        },
        "pasta": {
            "ingredients": [
                {"name": "Pasta", "amount": 100, "unit": "g"},
                {"name": "Salsa de tomate", "amount": 150, "unit": "g"},
                {"name": "Queso parmesano", "amount": 20, "unit": "g"},
                {"name": "Aceite de oliva", "amount": 1, "unit": "cucharada"},
                {"name": "Sal", "amount": 1, "unit": "pizca"},
                {"name": "Albahaca fresca", "amount": 5, "unit": "hojas"}
            ],
            "instructions": "1. Hervir agua con sal en una olla grande.\n2. Cocinar la pasta según el tiempo indicado en el paquete.\n3. Calentar la salsa de tomate en una sartén.\n4. Escurrir la pasta y añadir a la salsa.\n5. Remover bien y servir con queso parmesano y albahaca.",
            "tags": ["almuerzo", "cena", "carbohidratos"],
            "difficulty": "fácil",
            "prep_time": 15
        },
        "arroz": {
            "ingredients": [
                {"name": "Arroz", "amount": 100, "unit": "g"},
                {"name": "Agua", "amount": 250, "unit": "ml"},
                {"name": "Aceite de oliva", "amount": 1, "unit": "cucharada"},
                {"name": "Sal", "amount": 1, "unit": "pizca"}
            ],
            "instructions": "1. Calentar el aceite en un cazo.\n2. Añadir el arroz y tostar ligeramente 1 minuto.\n3. Verter el agua con sal.\n4. Cocinar a fuego medio-bajo hasta que absorba el agua.\n5. Apagar y reposar 5 minutos con tapa.",
            "tags": ["almuerzo", "cena", "guarnición"],
            "difficulty": "fácil",
            "prep_time": 20
        },
        "pollo": {
            "ingredients": [
                {"name": "Pechuga de pollo", "amount": 150, "unit": "g"},
                {"name": "Aceite de oliva", "amount": 2, "unit": "cucharadas"},
                {"name": "Ajo", "amount": 2, "unit": "dientes"},
                {"name": "Limón", "amount": 0.5, "unit": "unidad"},
                {"name": "Orégano", "amount": 1, "unit": "cucharadita"},
                {"name": "Sal y pimienta", "amount": 1, "unit": "al gusto"}
            ],
            "instructions": "1. Sazonar el pollo con ajo picado, orégano, sal y pimienta.\n2. Calentar el aceite en una sartén.\n3. Cocinar el pollo 5-6 minutos por lado.\n4. Añadir el zumo de limón al final.\n5. Reposar 2 minutos antes de servir.",
            "tags": ["cena", "proteína", "bajo en carbohidratos"],
            "difficulty": "medio",
            "prep_time": 15
        },
        "salmón": {
            "ingredients": [
                {"name": "Filete de salmón", "amount": 150, "unit": "g"},
                {"name": "Aceite de oliva", "amount": 1, "unit": "cucharada"},
                {"name": "Limón", "amount": 1, "unit": "unidad"},
                {"name": "Eneldo", "amount": 1, "unit": "cucharadita"},
                {"name": "Sal", "amount": 1, "unit": "pizca"}
            ],
            "instructions": "1. Precalentar el horno a 200°C.\n2. Sazonar el salmón con aceite, zumo de limón, eneldo y sal.\n3. Hornear durante 12-15 minutos.\n4. Servir con verduras al vapor o ensalada.",
            "tags": ["cena", "pescado", "omega-3", "saludable"],
            "difficulty": "medio",
            "prep_time": 20
        },
        "merluza": {
            "ingredients": [
                {"name": "Filete de merluza", "amount": 150, "unit": "g"},
                {"name": "Aceite de oliva", "amount": 2, "unit": "cucharadas"},
                {"name": "Ajo", "amount": 2, "unit": "dientes"},
                {"name": "Perejil fresco", "amount": 1, "unit": "cucharada"},
                {"name": "Vino blanco", "amount": 50, "unit": "ml"}
            ],
            "instructions": "1. Calentar el aceite con el ajo laminado.\n2. Añadir el pescado y cocinar 3 minutos por lado.\n3. Verter el vino blanco y cocinar 5 minutos más.\n4. Espolvorear con perejil picado.\n5. Servir con patatas al vapor.",
            "tags": ["cena", "pescado", "saludable"],
            "difficulty": "medio",
            "prep_time": 15
        },
        "lentejas": {
            "ingredients": [
                {"name": "Lentejas", "amount": 80, "unit": "g"},
                {"name": "Zanahoria", "amount": 1, "unit": "unidad"},
                {"name": "Cebolla", "amount": 0.5, "unit": "unidad"},
                {"name": "Ajo", "amount": 1, "unit": "diente"},
                {"name": "Laurel", "amount": 1, "unit": "hoja"},
                {"name": "Aceite de oliva", "amount": 2, "unit": "cucharadas"}
            ],
            "instructions": "1. Sofreír cebolla, ajo y zanahoria picados.\n2. Añadir las lentejas lavadas y el laurel.\n3. Cubrir con agua y cocinar 30-40 minutos.\n4. Sazonar con sal al final.\n5. Servir caliente.",
            "tags": ["almuerzo", "legumbres", "proteína vegetal"],
            "difficulty": "medio",
            "prep_time": 45
        },
        "garbanzos": {
            "ingredients": [
                {"name": "Garbanzos cocidos", "amount": 150, "unit": "g"},
                {"name": "Cebolla", "amount": 0.5, "unit": "unidad"},
                {"name": "Ajo", "amount": 2, "unit": "dientes"},
                {"name": "Pimentón dulce", "amount": 1, "unit": "cucharadita"},
                {"name": "Aceite de oliva", "amount": 2, "unit": "cucharadas"}
            ],
            "instructions": "1. Sofreír cebolla y ajo en aceite.\n2. Añadir los garbanzos escurridos.\n3. Sazonar con pimentón y sal.\n4. Cocinar 10-15 minutos a fuego lento.\n5. Servir caliente.",
            "tags": ["almuerzo", "legumbres", "proteína vegetal"],
            "difficulty": "fácil",
            "prep_time": 15
        },
        "gazpacho": {
            "ingredients": [
                {"name": "Tomate maduro", "amount": 4, "unit": "unidades"},
                {"name": "Pepino", "amount": 0.5, "unit": "unidad"},
                {"name": "Pimiento verde", "amount": 0.5, "unit": "unidad"},
                {"name": "Ajo", "amount": 1, "unit": "diente"},
                {"name": "Aceite de oliva virgen extra", "amount": 3, "unit": "cucharadas"},
                {"name": "Vinagre", "amount": 1, "unit": "cucharada"}
            ],
            "instructions": "1. Trocear todas las verduras.\n2. Triturar todo junto con el aceite y vinagre.\n3. Colar para quitar pieles.\n4. Añadir agua fría al gusto.\n5. Enfriar y servir con guarnición de verduras.",
            "tags": ["almuerzo", "verano", "frío", "vegano"],
            "difficulty": "fácil",
            "prep_time": 15
        },
        "paella": {
            "ingredients": [
                {"name": "Arroz bomba", "amount": 150, "unit": "g"},
                {"name": "Pollo troceado", "amount": 100, "unit": "g"},
                {"name": "Judía verde", "amount": 100, "unit": "g"},
                {"name": "Garrofón", "amount": 50, "unit": "g"},
                {"name": "Tomate rallado", "amount": 50, "unit": "g"},
                {"name": "Azafrán", "amount": 1, "unit": "pizca"},
                {"name": "Aceite de oliva", "amount": 3, "unit": "cucharadas"}
            ],
            "instructions": "1. Dorar el pollo en la paellera con aceite.\n2. Añadir verduras y rehogar.\n3. Incorporar el tomate y sofreír.\n4. Añadir agua, azafrán y hervir 15 minutos.\n5. Repartir el arroz en cruz y cocer a fuego fuerte 10 min.\n6. Bajar el fuego 8 minutos más y reposar 5.",
            "tags": ["almuerzo", "español", "tradicional", "domingo"],
            "difficulty": "difícil",
            "prep_time": 50
        },
        "batido": {
            "ingredients": [
                {"name": "Plátano maduro", "amount": 1, "unit": "unidad"},
                {"name": "Leche o bebida vegetal", "amount": 200, "unit": "ml"},
                {"name": "Miel", "amount": 1, "unit": "cucharada"},
                {"name": "Hielo", "amount": 3, "unit": "cubos"}
            ],
            "instructions": "1. Pelar y trocear el plátano.\n2. Añadir todos los ingredientes a la batidora.\n3. Triturar hasta conseguir una mezcla homogénea.\n4. Servir inmediatamente.",
            "tags": ["bebida", "desayuno", "energético"],
            "difficulty": "fácil",
            "prep_time": 5
        },
        "fruta": {
            "ingredients": [
                {"name": "Fruta de temporada", "amount": 200, "unit": "g"}
            ],
            "instructions": "1. Lavar y pelar la fruta según el tipo.\n2. Trocear en pedazos manejables.\n3. Servir fresca.",
            "tags": ["postre", "vegano", "saludable"],
            "difficulty": "fácil",
            "prep_time": 3
        },
        "sándwich": {
            "ingredients": [
                {"name": "Pan de molde integral", "amount": 2, "unit": "rebanadas"},
                {"name": "Jamón cocido", "amount": 50, "unit": "g"},
                {"name": "Queso en lonchas", "amount": 30, "unit": "g"},
                {"name": "Lechuga", "amount": 20, "unit": "g"},
                {"name": "Tomate", "amount": 2, "unit": "rodajas"}
            ],
            "instructions": "1. Tostar ligeramente el pan si se desea.\n2. Colocar la lechuga en una rebanada.\n3. Añadir el jamón, queso y tomate.\n4. Cerrar con la otra rebanada y servir.",
            "tags": ["almuerzo", "rápido"],
            "difficulty": "fácil",
            "prep_time": 5
        },
        "crema": {
            "ingredients": [
                {"name": "Verdura principal", "amount": 200, "unit": "g"},
                {"name": "Cebolla", "amount": 0.5, "unit": "unidad"},
                {"name": "Caldo de verduras", "amount": 300, "unit": "ml"},
                {"name": "Nata (opcional)", "amount": 50, "unit": "ml"},
                {"name": "Aceite de oliva", "amount": 2, "unit": "cucharadas"}
            ],
            "instructions": "1. Sofreír la cebolla en aceite.\n2. Añadir la verdura troceada.\n3. Cubrir con caldo y cocinar 20 minutos.\n4. Triturar hasta conseguir una crema suave.\n5. Añadir nata si se desea y servir.",
            "tags": ["almuerzo", "cena", "crema"],
            "difficulty": "medio",
            "prep_time": 30
        },
        "ternera": {
            "ingredients": [
                {"name": "Ternera para guisar", "amount": 150, "unit": "g"},
                {"name": "Cebolla", "amount": 1, "unit": "unidad"},
                {"name": "Zanahoria", "amount": 1, "unit": "unidad"},
                {"name": "Vino tinto", "amount": 100, "unit": "ml"},
                {"name": "Aceite de oliva", "amount": 2, "unit": "cucharadas"}
            ],
            "instructions": "1. Dorar la carne troceada en aceite.\n2. Añadir cebolla y zanahoria picadas.\n3. Verter el vino y dejar reducir.\n4. Cocer a fuego lento 45-60 minutos.\n5. Rectificar de sal y servir.",
            "tags": ["cena", "proteína", "tradicional"],
            "difficulty": "difícil",
            "prep_time": 60
        },
        "sopa": {
            "ingredients": [
                {"name": "Caldo de pollo", "amount": 500, "unit": "ml"},
                {"name": "Fideos finos", "amount": 50, "unit": "g"},
                {"name": "Huevo", "amount": 1, "unit": "unidad"},
                {"name": "Zanahoria", "amount": 1, "unit": "unidad"},
                {"name": "Sal", "amount": 1, "unit": "pizca"}
            ],
            "instructions": "1. Calentar el caldo en una olla.\n2. Añadir la zanahoria rallada.\n3. Incorporar los fideos y cocinar 8 minutos.\n4. Batir el huevo y añadirlo en hilo mientras se remueve.\n5. Servir caliente.",
            "tags": ["almuenzo", "cena", "reconfortante"],
            "difficulty": "fácil",
            "prep_time": 15
        },
        "postre": {
            "ingredients": [
                {"name": "Ingrediente principal", "amount": 150, "unit": "g"},
                {"name": "Azúcar o edulcorante", "amount": 30, "unit": "g"},
                {"name": "Leche o crema", "amount": 100, "unit": "ml"}
            ],
            "instructions": "1. Preparar los ingredientes según la receta específica.\n2. Mezclar bien hasta conseguir una textura homogénea.\n3. Refrigerar si es necesario.\n4. Servir frío o a temperatura ambiente.",
            "tags": ["postre"],
            "difficulty": "medio",
            "prep_time": 20
        }
    }
    
    # Buscar coincidencias por nombre
    for key, data in recipe_database.items():
        if key in nombre_lower:
            return data
    
    # Inferir por tipo de comida
    if meal_type == "breakfast":
        return {
            "ingredients": [
                {"name": "Ingrediente principal", "amount": 100, "unit": "g"},
                {"name": "Leche o yogur", "amount": 150, "unit": "ml"},
                {"name": "Fruta", "amount": 50, "unit": "g"}
            ],
            "instructions": "1. Preparar los ingredientes principales.\n2. Mezclar o cocinar según corresponda.\n3. Servir caliente o frío.",
            "tags": ["desayuno"],
            "difficulty": "fácil",
            "prep_time": 10
        }
    elif meal_type == "lunch":
        return {
            "ingredients": [
                {"name": "Ingrediente principal", "amount": 150, "unit": "g"},
                {"name": "Verduras", "amount": 100, "unit": "g"},
                {"name": "Aceite de oliva", "amount": 2, "unit": "cucharadas"},
                {"name": "Sal", "amount": 1, "unit": "pizca"}
            ],
            "instructions": "1. Preparar los ingredientes.\n2. Cocinar según el método apropiado.\n3. Sazonar y servir caliente.",
            "tags": ["almuerzo"],
            "difficulty": "medio",
            "prep_time": 25
        }
    elif meal_type == "dinner":
        return {
            "ingredients": [
                {"name": "Proteína", "amount": 150, "unit": "g"},
                {"name": "Verduras", "amount": 100, "unit": "g"},
                {"name": "Aceite de oliva", "amount": 1, "unit": "cucharada"}
            ],
            "instructions": "1. Preparar la proteína.\n2. Cocinar las verduras de acompañamiento.\n3. Emplatar y servir.",
            "tags": ["cena"],
            "difficulty": "medio",
            "prep_time": 20
        }
    
    # Valor por defecto
    return {
        "ingredients": [
            {"name": "Ingrediente principal", "amount": 150, "unit": "g"},
            {"name": "Aceite de oliva", "amount": 2, "unit": "cucharadas"},
            {"name": "Sal", "amount": 1, "unit": "al gusto"}
        ],
        "instructions": "1. Preparar los ingredientes.\n2. Cocinar según el método apropiado.\n3. Sazonar al gusto.\n4. Servir caliente.",
        "tags": ["receta"],
        "difficulty": "medio",
        "prep_time": 20
    }

def update_recipe(recipe_id: str, data: Dict[str, Any]) -> bool:
    """Actualizar una receta con ingredientes e instrucciones."""
    url = f"{SUPABASE_URL}/rest/v1/master_recipes?id=eq.{recipe_id}"
    
    payload = {
        "ingredients": json.dumps(data["ingredients"]),
        "instructions": data["instructions"],
        "prep_time_min": data["prep_time"]
    }
    
    response = requests.patch(url, headers=HEADERS, json=payload)
    
    return response.status_code == 204

def main():
    """Función principal para enriquecer todas las recetas."""
    print("🚀 Iniciando enriquecimiento de recetas...\n")
    
    # Obtener recetas existentes
    recipes = get_existing_recipes()
    
    if not recipes:
        print("❌ No se encontraron recetas para enriquecer")
        return
    
    # Enriquecer cada receta
    updated_count = 0
    failed_count = 0
    examples = []
    
    total = len(recipes)
    
    for i, recipe in enumerate(recipes):
        nombre = recipe.get("name", "")
        descripcion = recipe.get("description", "")
        meal_type = recipe.get("meal_type", "lunch")
        calories = recipe.get("calories", 300)
        protein = recipe.get("protein_g", 20)
        
        # Generar datos enriquecidos
        enriched_data = generate_recipe_data(nombre, descripcion, meal_type, calories, protein)
        
        # Actualizar en la base de datos
        if update_recipe(recipe["id"], enriched_data):
            updated_count += 1
            
            # Guardar ejemplos para el reporte
            if len(examples) < 5:
                examples.append({
                    "id": recipe["id"],
                    "nombre": nombre,
                    "ingredients": enriched_data["ingredients"],
                    "instructions": enriched_data["instructions"],
                    "tags": enriched_data["tags"],
                    "difficulty": enriched_data["difficulty"],
                    "prep_time": enriched_data["prep_time"]
                })
        else:
            failed_count += 1
        
        # Progreso
        if (i + 1) % 20 == 0:
            print(f"  📊 Procesadas {i + 1}/{total} recetas...")
    
    # Reporte final
    print(f"\n{'='*60}")
    print(f"✅ RECETAS ACTUALIZADAS: {updated_count}/{total}")
    if failed_count > 0:
        print(f"❌ Fallos: {failed_count}")
    print(f"{'='*60}")
    
    print("\n📝 EJEMPLOS DE RECETAS ENRIQUECIDAS:\n")
    
    for ex in examples:
        print(f"📌 {ex['nombre']}")
        print(f"   Dificultad: {ex['difficulty']} | Tiempo: {ex['prep_time']} min")
        print(f"   Tags: {', '.join(ex['tags'])}")
        print(f"   Ingredientes:")
        for ing in ex['ingredients'][:3]:
            print(f"      - {ing['amount']} {ing['unit']} de {ing['name']}")
        if len(ex['ingredients']) > 3:
            print(f"      ... y {len(ex['ingredients']) - 3} más")
        print(f"   Instrucciones (resumen): {ex['instructions'][:80]}...")
        print()
    
    print(f"\n🎉 ¡Proceso completado!")

if __name__ == "__main__":
    main()