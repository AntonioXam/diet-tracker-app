#!/usr/bin/env python3
"""
Diet Tracker API - Backend con Supabase
Productos FIT + Variedad diaria + Mercadona/Lidl
"""

import os
import json
import hashlib
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuración Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ============================================================
# RECETAS MAESTRAS FIT - Productos saludables Mercadona/Lidl
# ============================================================

MASTER_RECIPES = [
    # ==================== DESAYUNOS (15 opciones FIT) ====================
    {"name": "Tostada de espelta con aguacate y huevo poché", "meal_type": "desayuno", "calories": 340, "protein": 16, "carbs": 28, "fat": 18,
     "ingredients": "Pan de espelta Lidl (2 rebanadas), Aguacate maduro (1/2), Huevo campero L Hacendado (1), Aceite de oliva virgen extra, Pimienta negra",
     "instructions": "Tostar pan de espelta, machacar aguacate con limón y sal, hacer huevo poché 3 min", "supermarket": "mixto", "category": "salado"},
    
    {"name": "Bowl de açaí con granola y plátano", "meal_type": "desayuno", "calories": 335, "protein": 14, "carbs": 52, "fat": 10,
     "ingredients": "Puré de açaí Lidl (100g), Leche de almendras Hacendado (150ml), Granola sin azúcar Lidl (40g), Plátano (1), Fresas (50g)",
     "instructions": "Mezclar açaí con leche, congelar 30 min, topped con granola y fruta", "supermarket": "mixto", "category": "dulce"},
    
    {"name": "Bowl de quinoa con yogur griego y frutos rojos", "meal_type": "desayuno", "calories": 320, "protein": 20, "carbs": 42, "fat": 8,
     "ingredients": "Quinoa cocida Lidl (80g), Yogur griego 0% Hacendado (150g), Arándanos congelados Lidl (80g), Nueces pecan (15g), Miel de abeja",
     "instructions": "Mezclar quinoa fría con yogur, añadir frutos rojos y nueces troceadas", "supermarket": "mixto", "category": "dulce"},
    
    {"name": "Porridge de avena con proteína y plátano", "meal_type": "desayuno", "calories": 310, "protein": 24, "carbs": 45, "fat": 6,
     "ingredients": "Copos de avena finos Lidl (50g), Proteína whey vainilla Lidl (25g), Leche de almendras sin azúcar Hacendado (200ml), Plátano pequeño (1)",
     "instructions": "Cocer avena 5 min con leche, mezclar proteína con poco líquido, añadir plátano en rodajas", "supermarket": "mixto", "category": "dulce"},
    
    {"name": "Revuelto de claras con espinacas y champiñones", "meal_type": "desayuno", "calories": 280, "protein": 28, "carbs": 12, "fat": 10,
     "ingredients": "Claras de huevo Hacendado (200ml), Espinacas baby Lidl (80g), Champiñones laminados (100g), Ajo (1 diente), Aceite de oliva",
     "instructions": "Saltear champiñones con ajo, añadir espinacas 2 min, agregar claras y remover hasta cuajar", "supermarket": "mixto", "category": "salado"},
    
    {"name": "Pudín de chía con mango y coco", "meal_type": "desayuno", "calories": 295, "protein": 12, "carbs": 38, "fat": 14,
     "ingredients": "Semillas de chía Lidl (35g), Leche de coco sin azúcar Hacendado (200ml), Mango fresco (100g), Coco rallado sin azúcar (10g)",
     "instructions": "Mezclar chía con leche de coco, refrigerar 4h mínimo, añadir mango troceado", "supermarket": "mixto", "category": "dulce"},
    
    {"name": "Tortitas de avena y proteína sin azúcar", "meal_type": "desayuno", "calories": 330, "protein": 26, "carbs": 35, "fat": 9,
     "ingredients": "Avena molida Lidl (50g), Proteína whey chocolate Lidl (25g), Clara de huevo (100ml), Levadura química, Edulcorante stevia",
     "instructions": "Mezclar ingredientes, hacer tortitas en sartén antiadherente 2 min por lado", "supermarket": "mixto", "category": "dulce"},
    
    {"name": "Tostada de centeno con salmón ahumado y eneldo", "meal_type": "desayuno", "calories": 350, "protein": 22, "carbs": 24, "fat": 16,
     "ingredients": "Pan de centeno Lidl (2 rebanadas), Salmón ahumado Lidl (80g), Queso crema light Hacendado (30g), Eneldo fresco, Limón",
     "instructions": "Tostar pan, untar queso crema, colocar salmón y espolvorear eneldo", "supermarket": "lidl", "category": "salado"},
    
    {"name": "Batido verde detox con espirulina", "meal_type": "desayuno", "calories": 270, "protein": 18, "carbs": 35, "fat": 8,
     "ingredients": "Espinacas frescas (60g), Plátano verde (1/2), Manzana green (1), Proteína vegetal Lidl (20g), Espirulina en polvo Lidl (5g), Agua (250ml)",
     "instructions": "Batir todo hasta textura suave, servir inmediatamente", "supermarket": "mixto", "category": "batido"},
    
    {"name": "Bowl de requesón con granola casera y kiwi", "meal_type": "desayuno", "calories": 315, "protein": 20, "carbs": 40, "fat": 10,
     "ingredients": "Requesón batido 0% Hacendado (150g), Granola sin azúcar Lidl (40g), Kiwi maduro (2 unidades), Semillas de calabaza (10g)",
     "instructions": "Colocar requesón en bowl, añadir granola y kiwi en rodajas", "supermarket": "mixto", "category": "dulce"},
    
    {"name": "Huevos benedictinos fit con pan de kamut", "meal_type": "desayuno", "calories": 360, "protein": 24, "carbs": 26, "fat": 18,
     "ingredients": "Pan de kamut Lidl (2 rebanadas), Huevos camperos L Hacendado (2), Jamón york 97% carne Hacendado (2 lonchas), Yogur griego (50g), Mostaza Dijon",
     "instructions": "Tostar pan, colocar jamón, huevo poché, salsa de yogur con mostaza", "supermarket": "mixto", "category": "salado"},
    
    # ==================== ALMUERZOS (8 opciones FIT) ====================
    {"name": "Manzana Fuji con mantequilla de almendras", "meal_type": "almuerzo", "calories": 185, "protein": 6, "carbs": 24, "fat": 9,
     "ingredients": "Manzana Fuji (1 mediana), Mantequilla de almendras 100% Lidl (20g), Canela en polvo",
     "instructions": "Cortar manzana en gajos, untar con mantequilla de almendras y espolvorear canela", "supermarket": "lidl", "category": "snack"},
    
    {"name": "Yogur skyr con semillas de cáñamo", "meal_type": "almuerzo", "calories": 145, "protein": 18, "carbs": 10, "fat": 4,
     "ingredients": "Skyr natural Hacendado (175g), Semillas de cáñamo peladas Lidl (15g), Edulcorante eritritol",
     "instructions": "Mezclar skyr con semillas y edulcorante al gusto", "supermarket": "mixto", "category": "lácteo"},
    
    {"name": "Palitos de zanahoria con guacamole casero", "meal_type": "almuerzo", "calories": 160, "protein": 4, "carbs": 16, "fat": 10,
     "ingredients": "Zanahorias baby Lidl (150g), Aguacate maduro (1/2), Limón, Cilantro fresco, Sal marina",
     "instructions": "Cortar zanahorias, machacar aguacate con limón y cilantro, servir como dip", "supermarket": "mixto", "category": "salado"},
    
    {"name": "Barrita proteica Low Carb de chocolate", "meal_type": "almuerzo", "calories": 190, "protein": 22, "carbs": 8, "fat": 8,
     "ingredients": "Barrita protein fit Lidl (1 unidad de 45g)",
     "instructions": "Consumir directamente", "supermarket": "lidl", "category": "snack"},
    
    {"name": "Rollitos de pavo con queso fresco y pepino", "meal_type": "almuerzo", "calories": 135, "protein": 16, "carbs": 6, "fat": 5,
     "ingredients": "Pechuga de pavo en lonchas Hacendado (80g), Queso fresco 0% Hacendado (60g), Pepino (1/2), Eneldo",
     "instructions": "Extender lonchas de pavo, colocar queso y tiras de pepino, enrollar", "supermarket": "mixto", "category": "salado"},
    
    {"name": "Puñado de frutos secos mix sin tostar", "meal_type": "almuerzo", "calories": 175, "protein": 7, "carbs": 8, "fat": 14,
     "ingredients": "Mix frutos secos crudos Lidl (nueces, almendras, anacardos) (25g)",
     "instructions": "Consumir directamente", "supermarket": "lidl", "category": "snack"},
    
    {"name": "Tostada crujiente con hummus de remolacha", "meal_type": "almuerzo", "calories": 155, "protein": 7, "carbs": 20, "fat": 6,
     "ingredients": "Crispbread multicereales Lidl (2 unidades), Hummus de remolacha Hacendado (50g), Rúcula fresca",
     "instructions": "Untar hummus en crispbread, añadir rúcula fresca", "supermarket": "mixto", "category": "salado"},
    
    {"name": "Batido de proteínas con fresas y plátano", "meal_type": "almuerzo", "calories": 180, "protein": 24, "carbs": 18, "fat": 3,
     "ingredients": "Proteína whey fresa Lidl (25g), Fresas congeladas Lidl (100g), Plátano pequeño (1/2), Agua (200ml)",
     "instructions": "Batir todo hasta textura cremosa", "supermarket": "lidl", "category": "batido"},
    
    # ==================== COMIDAS (10 opciones FIT) ====================
    {"name": "Pechuga de pollo a la plancha con quinoa y brócoli", "meal_type": "comida", "calories": 445, "protein": 42, "carbs": 38, "fat": 12,
     "ingredients": "Pechuga de pollo ecológico Hacendado (160g), Quinoa tricolor Lidl (70g en crudo), Brócoli fresco (150g), Aceite de oliva virgen extra, Ajo en polvo",
     "instructions": "Cocer quinoa 12 min, hacer pollo a la plancha con especias, vapor brócoli 8 min", "supermarket": "mixto", "category": "proteina"},
    
    {"name": "Salmón al horno con boniato y espárragos", "meal_type": "comida", "calories": 485, "protein": 38, "carbs": 42, "fat": 20,
     "ingredients": "Salmón fresco Lidl (170g), Boniato mediano (180g), Espárragos verdes Lidl (150g), Limón, Romero fresco, Aceite de oliva",
     "instructions": "Hornear boniato 40 min a 200°C, salmón 12 min, espárragos 8 min con limón", "supermarket": "lidl", "category": "pescado"},
    
    {"name": "Lentejas pardinas con verduras y arroz integral", "meal_type": "comida", "calories": 425, "protein": 20, "carbs": 58, "fat": 10,
     "ingredients": "Lentejas pardinas Lidl (75g en crudo), Arroz integral Hacendado (40g), Zanahoria, Cebolla, Pimiento rojo, Laurel, Comino",
     "instructions": "Sofreír verduras, añadir lentejas y arroz, cubrir con agua, cocer 30 min", "supermarket": "mixto", "category": "legumbre"},
    
    {"name": "Pasta de garbanzos con gambas y calabacín", "meal_type": "comida", "calories": 455, "protein": 34, "carbs": 48, "fat": 14,
     "ingredients": "Pasta de garbanzos Lidl (90g en crudo), Gambas peladas Lidl (120g), Calabacín mediano (1), Ajo, Guindilla, Aceite de oliva",
     "instructions": "Cocer pasta 8 min, saltear gambas con ajo y calabacín en espiral", "supermarket": "lidl", "category": "pasta"},
    
    {"name": "Ternera magra al wok con verduras thai", "meal_type": "comida", "calories": 470, "protein": 40, "carbs": 36, "fat": 16,
     "ingredients": "Ternera magra en tiras Hacendado (160g), Mix verduras thai Lidl (200g), Salsa de soja baja en sal, Jengibre fresco, Sésamo tostado",
     "instructions": "Wok muy caliente, carne 4 min, verduras 5 min, salsa de soja y sésamo", "supermarket": "mixto", "category": "proteina"},
    
    {"name": "Bowl de garbanzos con atún y aguacate", "meal_type": "comida", "calories": 420, "protein": 28, "carbs": 42, "fat": 16,
     "ingredients": "Garbanzos cocidos Lidl (200g), Atún claro al natural Hacendado (2 latas de 52g), Aguacate (1/4), Tomates cherry, Pepino, Limón",
     "instructions": "Mezclar garbanzos con atún escurrido, añadir verduras troceadas y aguacate", "supermarket": "mixto", "category": "ensalada"},
    
    {"name": "Merluza en papillote con patata y pimientos", "meal_type": "comida", "calories": 395, "protein": 36, "carbs": 38, "fat": 10,
     "ingredients": "Merluza fresca Lidl (180g), Patata mediana (150g), Pimiento rojo y verde (1/2 cada), Cebolla, Aceite de oliva, Perejil",
     "instructions": "Papel de horno, pescado con verduras en juliana, hornear 20 min a 180°C", "supermarket": "lidl", "category": "pescado"},
    
    {"name": "Wrap integral de pollo con hummus y rúcula", "meal_type": "comida", "calories": 440, "protein": 32, "carbs": 44, "fat": 14,
     "ingredients": "Tortilla integral Lidl (1 grande de 60g), Pechuga de pollo (120g), Hummus clásico Hacendado (60g), Rúcula fresca, Tomate",
     "instructions": "Hacer pollo a la plancha, calentar tortilla, rellenar y enrollar", "supermarket": "mixto", "category": "wrap"},
    
    {"name": "Hamburguesa de pavo casera con ensalada y batata", "meal_type": "comida", "calories": 465, "protein": 38, "carbs": 40, "fat": 14,
     "ingredients": "Carne de pavo picada Hacendado (150g), Batata mediana (180g), Lechuga iceberg, Tomate, Cebolla morada, Mostaza antigua",
     "instructions": "Formar hamburguesa, plancha 5 min por lado, batata al horno 35 min", "supermarket": "mixto", "category": "proteina"},
    
    {"name": "Ensalada de espinacas con nueces y queso de cabra", "meal_type": "comida", "calories": 410, "protein": 22, "carbs": 28, "fat": 24,
     "ingredients": "Espinacas baby Lidl (100g), Queso de cabra rulo Hacendado (80g), Nueces peladas Lidl (30g), Pera conference (1/2), Vinagre de Módena",
     "instructions": "Mezclar espinacas con queso troceado, nueces y pera en gajos, aliñar", "supermarket": "mixto", "category": "ensalada"},
    
    # ==================== MERIENDAS (8 opciones FIT) ====================
    {"name": "Yogur skyr con arándanos y linaza", "meal_type": "merienda", "calories": 145, "protein": 17, "carbs": 16, "fat": 4,
     "ingredients": "Skyr natural Hacendado (175g), Arándanos frescos Lidl (80g), Semillas de linaza dorada (10g)",
     "instructions": "Mezclar skyr con arándanos y espolvorear linaza", "supermarket": "mixto", "category": "lácteo"},
    
    {"name": "Tostada de espelta con jamón serrano", "meal_type": "merienda", "calories": 175, "protein": 14, "carbs": 18, "fat": 6,
     "ingredients": "Pan de espelta Lidl (1 rebanada), Jamón serrano reserva (1 loncha de 40g), Tomate rallado",
     "instructions": "Tostar pan, rallar tomate, colocar jamón", "supermarket": "mixto", "category": "salado"},
    
    {"name": "Batido de proteínas con cacao y avellanas", "meal_type": "merienda", "calories": 165, "protein": 22, "carbs": 12, "fat": 5,
     "ingredients": "Proteína whey chocolate Lidl (25g), Cacao puro en polvo Hacendado (5g), Leche de almendras sin azúcar (200ml)",
     "instructions": "Batir todo hasta que no queden grumos", "supermarket": "mixto", "category": "batido"},
    
    {"name": "Huevos duros con pimentón y sal marina", "meal_type": "merienda", "calories": 140, "protein": 13, "carbs": 1, "fat": 9,
     "ingredients": "Huevos camperos L Hacendado (2 unidades), Pimentón de la Vera dulce, Sal marina, Orégano",
     "instructions": "Cocer huevos 10 min, enfriar, pelar y espolvorear especias", "supermarket": "mixto", "category": "proteina"},
    
    {"name": "Requesón con canela y stevia", "meal_type": "merienda", "calories": 115, "protein": 15, "carbs": 7, "fat": 3,
     "ingredients": "Requesón batido 0% Hacendado (120g), Canela de Ceilán Lidl, Stevia líquida (3-4 gotas)",
     "instructions": "Mezclar requesón con canela abundante y stevia", "supermarket": "mixto", "category": "lácteo"},
    
    {"name": "Palitos de cangrejo con bastones de pepino", "meal_type": "merienda", "calories": 95, "protein": 11, "carbs": 9, "fat": 1,
     "ingredients": "Palitos de cangrejo Lidl (100g), Pepino (1/2 mediano), Zumo de limón",
     "instructions": "Cortar pepino en bastones, acompañar con surimi desmenuzado", "supermarket": "lidl", "category": "snack"},
    
    {"name": "Onigiri de atún con alga nori", "meal_type": "merienda", "calories": 155, "protein": 12, "carbs": 24, "fat": 2,
     "ingredients": "Arroz sushi Lidl (60g cocido), Atún al natural Hacendado (1 lata pequeña), Alga nori Lidl (1 hoja), Sésamo",
     "instructions": "Formar bola de arroz con atún en el centro, envolver con nori", "supermarket": "mixto", "category": "snack"},
    
    {"name": "Taza de caldo de huesos con jengibre", "meal_type": "merienda", "calories": 85, "protein": 10, "carbs": 4, "fat": 3,
     "ingredients": "Caldo de huesos Hacendado (250ml), Jengibre fresco rallado, Cúrcuma molida, Pimienta negra",
     "instructions": "Calentar caldo, añadir jengibre y especias, servir caliente", "supermarket": "mercadona", "category": "bebida"},
    
    # ==================== CENAS (10 opciones FIT) ====================
    {"name": "Lubina al horno con menestras de verduras", "meal_type": "cena", "calories": 315, "protein": 34, "carbs": 18, "fat": 12,
     "ingredients": "Lubina fresca Lidl (200g), Menestra de verduras congelada Lidl (250g), Aceite de oliva virgen extra, Tomillo fresco, Limón",
     "instructions": "Hornear pescado 15 min a 180°C con verduras, aliñar con limón", "supermarket": "lidl", "category": "pescado"},
    
    {"name": "Tortilla de espinacas y queso feta light", "meal_type": "cena", "calories": 285, "protein": 22, "carbs": 8, "fat": 18,
     "ingredients": "Huevos camperos L Hacendado (2 grandes), Espinacas congeladas Lidl (120g), Queso feta light Hacendado (50g), Cebollino fresco",
     "instructions": "Saltear espinacas descongeladas, batir huevos con queso, hacer tortilla", "supermarket": "mixto", "category": "huevos"},
    
    {"name": "Ensalada tibia de atún rojo con judías verdes", "meal_type": "cena", "calories": 325, "protein": 32, "carbs": 14, "fat": 16,
     "ingredients": "Atún rojo fresco Lidl (140g), Judías verdes extrafinas Hacendado (150g), Tomate cherry, Aceitunas negras, Aceite de oliva",
     "instructions": "Hacer atún sellado 2 min por lado, judías al vapor 8 min, mezclar tibio", "supermarket": "mixto", "category": "ensalada"},
    
    {"name": "Sepia a la plancha con ajitos tiernos", "meal_type": "cena", "calories": 265, "protein": 34, "carbs": 10, "fat": 9,
     "ingredients": "Sepia limpia Lidl (220g), Ajitos tiernos Lidl (150g), Ajo (2 dientes), Perejil fresco, Aceite de oliva",
     "instructions": "Planchar sepia 4 min por lado, saltear ajitos con ajo laminado", "supermarket": "lidl", "category": "pescado"},
    
    {"name": "Pechuga de pavo al vapor con espárragos blancos", "meal_type": "cena", "calories": 280, "protein": 38, "carbs": 10, "fat": 8,
     "ingredients": "Pechuga de pavo Hacendado (170g), Espárragos blancos Lidl (200g), Limón, Pimienta blanca, Sal marina",
     "instructions": "Vapor pavo 15 min, espárragos 12 min, servir con limón", "supermarket": "mixto", "category": "proteina"},
    
    {"name": "Crema de calabacín y aguacate con semillas", "meal_type": "cena", "calories": 245, "protein": 10, "carbs": 18, "fat": 16,
     "ingredients": "Calabacín mediano (2), Aguacate (1/4), Puerro (1), Caldo de verduras Hacendado (300ml), Semillas de girasol (10g)",
     "instructions": "Cocer verduras 15 min, triturar con aguacate, decorar con semillas", "supermarket": "mixto", "category": "crema"},
    
    {"name": "Gambas al ajillo con champiñones portobello", "meal_type": "cena", "calories": 275, "protein": 28, "carbs": 12, "fat": 12,
     "ingredients": "Gambas peladas Lidl (150g), Champiñones portobello Hacendado (150g), Ajo (4 dientes), Guindilla, Aceite de oliva, Perejil",
     "instructions": "Saltear gambas con ajo y guindilla 3 min, añadir champiñones laminados", "supermarket": "mixto", "category": "pescado"},
    
    {"name": "Rollitos de lechuga con carne picada de ternera", "meal_type": "cena", "calories": 295, "protein": 30, "carbs": 14, "fat": 14,
     "ingredients": "Carne de ternera picada Hacendado (140g), Lechuga iceberg (4 hojas grandes), Zanahoria rallada, Cebollino, Salsa de soja",
     "instructions": "Saltear carne 6 min, rellenar hojas de lechuga como tacos", "supermarket": "mixto", "category": "proteina"},
    
    {"name": "Bacalao desalado con pisto de verduras", "meal_type": "cena", "calories": 305, "protein": 32, "carbs": 16, "fat": 12,
     "ingredients": "Bacalao desalado Lidl (160g), Calabacín (1/2), Berenjena pequeña (1/2), Pimiento rojo (1/2), Tomate triturado Hacendado (100g)",
     "instructions": "Hacer pisto 15 min, bacalao a la plancha 4 min por lado", "supermarket": "mixto", "category": "pescado"},
    
    {"name": "Sopa miso con tofu sedoso y wakame", "meal_type": "cena", "calories": 220, "protein": 14, "carbs": 18, "fat": 10,
     "ingredients": "Pasta miso Lidl (30g), Tofu sedoso Hacendado (120g), Alga wakame Lidl (5g), Cebollino, Sésamo tostado",
     "instructions": "Disolver miso en agua caliente sin hervir, añadir tofu en cubos y wakame", "supermarket": "mixto", "category": "sopa"},
]

# ============================================================
# UTILIDADES
# ============================================================

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def calculate_tmb(age, gender, height, weight, activity_level):
    """Tasa Metabólica Basal - fórmula Mifflin-St Jeor."""
    if gender == 'male':
        tmb = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        tmb = 10 * weight + 6.25 * height - 5 * age - 161
    
    multipliers = {'sedentary': 1.2, 'light': 1.375, 'moderate': 1.55, 'active': 1.725, 'very_active': 1.9}
    return round(tmb), round(tmb * multipliers.get(activity_level, 1.2))

def calculate_deficit(tdee, goal_type, current_weight, goal_weight):
    """Calcula calorías objetivo de forma segura y realista."""
    if goal_type == 'lose':
        # Déficit seguro: 300-500 kcal menos del TDEE
        # Nunca menos de 1200 kcal (mínimo saludable)
        deficit = min(500, max(300, (current_weight - goal_weight) * 15))
        target = max(1200, tdee - deficit)
        return target
    elif goal_type == 'gain':
        # Superávit moderado: +250-300 kcal
        return min(tdee + 300, 3500)  # Máximo 3500 kcal
    # Mantenimiento
    return tdee

def get_week_number():
    return datetime.now().isocalendar()[1]

def seed_recipes():
    """Inserta recetas maestras si están vacías."""
    try:
        existing = supabase.table('master_recipes').select('id').execute()
        if not existing.data:
            for recipe in MASTER_RECIPES:
                supabase.table('master_recipes').insert(recipe).execute()
            print(f"✅ {len(MASTER_RECIPES)} recetas FIT cargadas")
        else:
            print(f"✅ {len(existing.data)} recetas ya existen")
    except Exception as e:
        print(f"⚠️ Error seed recipes: {e}")

# ============================================================
# API ENDPOINTS
# ============================================================

@app.route('/api/health')
def health():
    return jsonify({'status': 'ok', 'timestamp': datetime.now().isoformat()})

@app.route('/api/register', methods=['POST'])
def register():
    try:
        data = request.json
        if not all(k in data for k in ('email', 'password', 'name')):
            return jsonify({'error': 'Datos incompletos'}), 400
        
        existing = supabase.table('users').select('id').eq('email', data['email']).execute()
        if existing.data:
            return jsonify({'error': 'Email ya registrado'}), 400
        
        result = supabase.table('users').insert({
            'email': data['email'],
            'password_hash': hash_password(data['password']),
            'name': data['name']
        }).execute()
        
        return jsonify({'success': True, 'user_id': result.data[0]['id']})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.json
        result = supabase.table('users').select('id, name').eq('email', data.get('email')).eq('password_hash', hash_password(data.get('password', ''))).execute()
        
        if result.data:
            return jsonify({'success': True, 'user_id': result.data[0]['id'], 'name': result.data[0]['name']})
        return jsonify({'error': 'Credenciales inválidas'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/profile', methods=['POST'])
def save_profile():
    try:
        data = request.json
        user_id = data.get('user_id')
        if not user_id:
            return jsonify({'error': 'user_id requerido'}), 400
        
        # Guardar perfil
        supabase.table('user_profiles').upsert({
            'user_id': user_id,
            'age': data['age'],
            'gender': data['gender'],
            'height_cm': data['height'],
            'current_weight_kg': data['current_weight'],
            'goal_weight_kg': data['goal_weight'],
            'activity_level': data['activity_level'],
            'meals_per_day': data['meals_per_day'],
            'allergies': data.get('allergies', ''),
            'disliked_foods': data.get('disliked_foods', ''),
            'goal_type': data['goal_type'],
            'target_calories': data.get('target_calories_override')  # Opcional: override manual
        }).execute()
        
        # Guardar peso inicial
        supabase.table('weight_history').insert({
            'user_id': user_id,
            'weight_kg': data['current_weight'],
            'week_number': get_week_number()
        }).execute()
        
        # Calcular calorías
        tmb, tdee = calculate_tmb(data['age'], data['gender'], data['height'], data['current_weight'], data['activity_level'])
        target = calculate_deficit(tdee, data['goal_type'], data['current_weight'], data['goal_weight'])
        
        # Generar primera semana CON VARIEDAD DIARIA
        generate_first_week_varied(user_id, target, data['meals_per_day'])
        
        return jsonify({'success': True, 'tmb': tmb, 'tdee': tdee, 'target_calories': int(target)})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/profile/update', methods=['POST'])
def update_profile():
    """Permite EDITAR el perfil después de creado."""
    try:
        data = request.json
        user_id = data.get('user_id')
        if not user_id:
            return jsonify({'error': 'user_id requerido'}), 400
        
        # Obtener perfil actual
        current = supabase.table('user_profiles').select('*').eq('user_id', user_id).execute()
        if not current.data:
            return jsonify({'error': 'Perfil no encontrado'}), 404
        
        current_profile = current.data[0]
        
        # Actualizar solo los campos proporcionados
        update_data = {'user_id': user_id}
        for field in ['age', 'gender', 'height_cm', 'current_weight_kg', 'goal_weight_kg', 
                      'activity_level', 'meals_per_day', 'allergies', 'disliked_foods', 'goal_type']:
            if field in data and data[field] is not None:
                update_data[field] = data[field]
        
        supabase.table('user_profiles').upsert(update_data).execute()
        
        # Si cambian datos de peso/actividad, recalcular calorías
        if any(k in data for k in ['current_weight_kg', 'activity_level', 'goal_weight_kg', 'goal_type', 'age', 'height_cm', 'gender']):
            profile = supabase.table('user_profiles').select('*').eq('user_id', user_id).execute().data[0]
            tmb, tdee = calculate_tmb(profile['age'], profile['gender'], profile['height_cm'], 
                                      profile['current_weight_kg'], profile['activity_level'])
            target = calculate_deficit(tdee, profile['goal_type'], profile['current_weight_kg'], profile['goal_weight_kg'])
            
            return jsonify({'success': True, 'recalculated': True, 'tmb': tmb, 'tdee': tdee, 'target_calories': int(target)})
        
        return jsonify({'success': True, 'recalculated': False})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/profile/get', methods=['GET'])
def get_profile():
    """Obtiene el perfil del usuario."""
    try:
        user_id = request.args.get('user_id')
        if not user_id:
            return jsonify({'error': 'user_id requerido'}), 400
        
        profile = supabase.table('user_profiles').select('*').eq('user_id', user_id).execute()
        if not profile.data:
            return jsonify({'error': 'Perfil no encontrado'}), 404
        
        return jsonify({'profile': profile.data[0]})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def get_meal_types_for_count(meals_per_day):
    """Devuelve los tipos de comida correctos según el número seleccionado."""
    if meals_per_day == 3:
        return ['desayuno', 'comida', 'cena']  # 3 principales
    elif meals_per_day == 4:
        return ['desayuno', 'comida', 'merienda', 'cena']  # añade merienda
    elif meals_per_day == 5:
        return ['desayuno', 'almuerzo', 'comida', 'merienda', 'cena']  # todas
    else:
        return ['desayuno', 'comida', 'cena']  # default

def generate_first_week_varied(user_id, target_calories, meals_per_day):
    """Genera la primera semana CON VARIEDAD - cada día diferente."""
    import random
    week = get_week_number()
    meal_types = get_meal_types_for_count(meals_per_day)
    
    # Obtener todas las recetas por tipo de comida
    recipes_by_type = {}
    for meal_type in meal_types:
        result = supabase.table('master_recipes').select('*').eq('meal_type', meal_type).execute()
        recipes_by_type[meal_type] = result.data or []
    
    used_recipes = {mt: [] for mt in meal_types}  # Tracking de recetas usadas esta semana
    
    for day in range(1, 8):  # 7 días
        for meal_type in meal_types:
            available = [r for r in recipes_by_type[meal_type] if r['id'] not in used_recipes[meal_type]]
            
            # Si se agotan, resetear y permitir repetir
            if not available:
                available = recipes_by_type[meal_type]
                used_recipes[meal_type] = []
            
            # Seleccionar aleatoria
            recipe = random.choice(available)
            used_recipes[meal_type].append(recipe['id'])
            
            # Insertar en plan semanal
            supabase.table('weekly_plans').insert({
                'user_id': user_id,
                'week_number': week,
                'day_of_week': day,
                'meal_type': meal_type,
                'selected_recipe_id': recipe['id'],
                'calories': recipe['calories'],
                'protein': recipe['protein'],
                'carbs': recipe['carbs'],
                'fat': recipe['fat']
            }).execute()
            
            # Añadir al banco de comidas
            supabase.table('user_food_bank').insert({
                'user_id': user_id,
                'meal_type': meal_type,
                'recipe_id': recipe['id'],
                'added_week': week
            }).execute()

@app.route('/api/plan/current', methods=['GET'])
def get_current_plan():
    try:
        user_id = request.args.get('user_id')
        if not user_id:
            return jsonify({'error': 'user_id requerido'}), 400
        
        week = get_week_number()
        
        # Obtener plan semanal
        result = supabase.table('weekly_plans').select('*').eq('user_id', user_id).eq('week_number', week).order('day_of_week').execute()
        
        # Calcular totales diarios y obtener recetas
        daily = {}
        meals = []
        for row in result.data:
            # Obtener detalles de la receta
            recipe_result = supabase.table('master_recipes').select('id, name, ingredients, instructions, supermarket, category, image_url').eq('id', row['selected_recipe_id']).execute()
            recipe = recipe_result.data[0] if recipe_result.data else {}
            
            meal = {
                'id': row['id'],
                'day_of_week': row['day_of_week'],
                'meal_type': row['meal_type'],
                'recipe_id': row['selected_recipe_id'],
                'recipe_name': recipe.get('name', ''),
                'ingredients': recipe.get('ingredients', ''),
                'instructions': recipe.get('instructions', ''),
                'supermarket': recipe.get('supermarket', ''),
                'image_url': recipe.get('image_url', None),
                'calories': row['calories'],
                'protein': row['protein'],
                'carbs': row['carbs'],
                'fat': row['fat']
            }
            meals.append(meal)
            
            d = row['day_of_week']
            if d not in daily:
                daily[d] = {'calories': 0, 'protein': 0, 'carbs': 0, 'fat': 0}
            daily[d]['calories'] += row['calories'] or 0
            daily[d]['protein'] += row['protein'] or 0
            daily[d]['carbs'] += row['carbs'] or 0
            daily[d]['fat'] += row['fat'] or 0
        
        return jsonify({'week': week, 'meals': meals, 'daily_totals': daily})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/food-bank/options', methods=['GET'])
def get_food_bank():
    try:
        user_id = request.args.get('user_id')
        meal_type = request.args.get('meal_type')
        if not user_id:
            return jsonify({'error': 'user_id requerido'}), 400
        
        query = supabase.table('user_food_bank').select('*').eq('user_id', user_id)
        
        if meal_type:
            query = query.eq('meal_type', meal_type)
        
        result = query.execute()
        
        options = []
        for row in result.data:
            recipe_result = supabase.table('master_recipes').select('id, name, meal_type, calories, protein, carbs, fat, ingredients, supermarket, image_url').eq('id', row['recipe_id']).execute()
            recipe = recipe_result.data[0] if recipe_result.data else {}
            
            options.append({
                'id': row['id'],
                'recipe_id': row['recipe_id'],
                'meal_type': row['meal_type'],
                'times_used': row['times_used'],
                'added_week': row['added_week'],
                'name': recipe.get('name', ''),
                'calories': recipe.get('calories', 0),
                'protein': recipe.get('protein', 0),
                'carbs': recipe.get('carbs', 0),
                'fat': recipe.get('fat', 0),
                'ingredients': recipe.get('ingredients', ''),
                'supermarket': recipe.get('supermarket', ''),
                'image_url': recipe.get('image_url', None)
            })
        
        return jsonify({'options': options})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/plan/swap', methods=['POST'])
def swap_meal():
    try:
        data = request.json
        recipe = supabase.table('master_recipes').select('*').eq('id', data['new_recipe_id']).execute()
        if not recipe.data:
            return jsonify({'error': 'Receta no encontrada'}), 404
        
        recipe = recipe.data[0]
        week = get_week_number()
        
        supabase.table('weekly_plans').update({
            'selected_recipe_id': data['new_recipe_id'],
            'calories': recipe['calories'],
            'protein': recipe['protein'],
            'carbs': recipe['carbs'],
            'fat': recipe['fat']
        }).eq('user_id', data['user_id']).eq('week_number', week).eq('day_of_week', data['day']).eq('meal_type', data['meal_type']).execute()
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/plan/regenerate', methods=['POST'])
def regenerate_plan():
    """Genera un NUEVO plan semanal con recetas diferentes."""
    try:
        data = request.json
        user_id = data.get('user_id')
        if not user_id:
            return jsonify({'error': 'user_id requerido'}), 400
        
        week = get_week_number()
        
        # Obtener perfil del usuario
        profile = supabase.table('user_profiles').select('*').eq('user_id', user_id).execute()
        if not profile.data:
            return jsonify({'error': 'Perfil no encontrado'}), 404
        
        profile = profile.data[0]
        meals_per_day = profile['meals_per_day']
        
        # Eliminar plan actual de esta semana
        supabase.table('weekly_plans').delete().eq('user_id', user_id).eq('week_number', week).execute()
        
        # Generar nuevo plan con variedad
        generate_first_week_varied(user_id, 2000, meals_per_day)  # Las calorías ya están en cada receta
        
        return jsonify({'success': True, 'message': 'Plan regenerado con nuevas recetas'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/plan/export', methods=['GET'])
def export_plan():
    """Exporta el plan semanal en formato texto para copiar."""
    try:
        user_id = request.args.get('user_id')
        if not user_id:
            return jsonify({'error': 'user_id requerido'}), 400
        
        week = get_week_number()
        result = supabase.table('weekly_plans').select('*').eq('user_id', user_id).eq('week_number', week).order('day_of_week').execute()
        
        days = {1: 'Lunes', 2: 'Martes', 3: 'Miércoles', 4: 'Jueves', 5: 'Viernes', 6: 'Sábado', 7: 'Domingo'}
        meal_types = {'desayuno': 'Desayuno', 'almuerzo': 'Almuerzo', 'comida': 'Comida', 'merienda': 'Merienda', 'cena': 'Cena'}
        
        output = f"📅 PLAN SEMANAL - Semana {week}\n\n"
        
        for day in range(1, 8):
            day_meals = [m for m in result.data if m['day_of_week'] == day]
            output += f"--- {days.get(day, f'Día {day}')} ---\n"
            
            for meal in day_meals:
                recipe = supabase.table('master_recipes').select('name').eq('id', meal['selected_recipe_id']).execute()
                recipe_name = recipe.data[0]['name'] if recipe.data else 'Sin nombre'
                output += f"  {meal_types.get(meal['meal_type'], meal['meal_type'])}: {recipe_name}\n"
            
            output += "\n"
        
        return jsonify({'export': output})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/weight/history', methods=['GET'])
def get_weight_history():
    """Retorna historial de peso del usuario (últimos 30 días)."""
    try:
        user_id = request.args.get('user_id')
        if not user_id:
            return jsonify({'error': 'user_id requerido'}), 400
        
        from datetime import datetime, timedelta
        thirty_days_ago = (datetime.now() - timedelta(days=30)).isoformat()
        
        result = supabase.table('weight_history').select('created_at, weight_kg').eq('user_id', user_id).gte('created_at', thirty_days_ago).order('created_at', desc=False).execute()
        
        history = [{'created_at': h['created_at'], 'weight': h['weight_kg']} for h in result.data]
        
        return jsonify({'history': history})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/weight/checkin', methods=['POST'])
def weight_checkin():
    try:
        data = request.json
        week = get_week_number()
        
        supabase.table('weight_history').insert({
            'user_id': data['user_id'],
            'weight_kg': data['weight'],
            'week_number': week
        }).execute()
        
        profile = supabase.table('user_profiles').select('*').eq('user_id', data['user_id']).execute()
        if not profile.data:
            return jsonify({'error': 'Perfil no encontrado'}), 404
        
        profile = profile.data[0]
        
        # Añadir NUEVAS opciones (hasta 6 por tipo) - USAR LÓGICA CORRECTA
        meal_types = get_meal_types_for_count(profile['meals_per_day'])
        
        for meal_type in meal_types:
            existing = supabase.table('user_food_bank').select('recipe_id').eq('user_id', data['user_id']).eq('meal_type', meal_type).execute()
            existing_ids = [r['recipe_id'] for r in existing.data]
            
            if len(existing_ids) < 6:
                # Obtener receta NO usada de este tipo
                new_recipe = supabase.table('master_recipes').select('*').eq('meal_type', meal_type).not_.in_('id', existing_ids).limit(1).execute()
                
                if new_recipe.data:
                    supabase.table('user_food_bank').insert({
                        'user_id': data['user_id'],
                        'meal_type': meal_type,
                        'recipe_id': new_recipe.data[0]['id'],
                        'added_week': week
                    }).execute()
        
        # Recalcular calorías
        tmb, tdee = calculate_tmb(profile['age'], profile['gender'], profile['height_cm'], data['weight'], profile['activity_level'])
        target = calculate_deficit(tdee, profile['goal_type'], data['weight'], profile['goal_weight_kg'])
        
        return jsonify({'success': True, 'new_target_calories': int(target)})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/shopping-list', methods=['GET'])
def shopping_list():
    try:
        user_id = request.args.get('user_id')
        if not user_id:
            return jsonify({'error': 'user_id requerido'}), 400
        
        week = get_week_number()
        result = supabase.table('weekly_plans').select('selected_recipe_id').eq('user_id', user_id).eq('week_number', week).execute()
        
        recipe_ids = [r['selected_recipe_id'] for r in result.data]
        recipes = supabase.table('master_recipes').select('ingredients, supermarket').in_('id', recipe_ids).execute()
        
        shopping = {'mercadona': [], 'lidl': [], 'mixto': []}
        for r in recipes.data:
            items = [i.strip() for i in r['ingredients'].split(',')]
            supermarket = r.get('supermarket', 'mixto')
            if supermarket not in shopping:
                shopping[supermarket] = []
            shopping[supermarket].extend(items)
        
        for k in shopping:
            shopping[k] = list(set(shopping[k]))
        
        return jsonify({'shopping_list': shopping})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def stats():
    try:
        user_id = request.args.get('user_id')
        if not user_id:
            return jsonify({'error': 'user_id requerido'}), 400
        
        history = supabase.table('weight_history').select('weight_kg, week_number, recorded_at').eq('user_id', user_id).order('week_number').execute()
        profile = supabase.table('user_profiles').select('current_weight_kg, goal_weight_kg').eq('user_id', user_id).execute()
        
        if not profile.data:
            return jsonify({'error': 'Perfil no encontrado'}), 404
        
        profile = profile.data[0]
        current = history.data[-1]['weight_kg'] if history.data else profile['current_weight_kg']
        diff = profile['current_weight_kg'] - profile['goal_weight_kg']
        progress = ((profile['current_weight_kg'] - current) / diff * 100) if diff > 0 else 0
        
        return jsonify({
            'weight_history': history.data,
            'current_weight': current,
            'goal_weight': profile['goal_weight_kg'],
            'progress_percent': round(progress, 1)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============================================================
# INIT
# ============================================================

try:
    seed_recipes()
except Exception as e:
    print(f"⚠️ Error inicializando recetas: {e}")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
