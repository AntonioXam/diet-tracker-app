# 🥗 Diet Tracker App

Aplicación web de nutrición personalizada con productos de **Mercadona y Lidl**.

## ✨ Características

- **Cuestionario inicial exhaustivo**: Edad, género, altura, peso, objetivo, actividad, alergias
- **Cálculo automático de TMB** y déficit calórico (fórmula Mifflin-St Jeor)
- **Sistema progresivo de menús**:
  - Semana 1: 1 opción por comida
  - Cada semana: +1 opción nueva (máximo 6)
  - Check-in semanal de peso obligatorio
- **Productos 100% Mercadona/Lidl**
- **Lista de la compra automática** agrupada por supermercado
- **Desglose de macros visual** (proteínas, carbohidratos, grasas)

## 🚀 Despliegue en Vercel

```bash
npx vercel deploy --prod
```

## 📁 Estructura

```
diet-tracker-app/
├── api/
│   ├── app.py          # Flask API con todas las rutas
│   └── requirements.txt
├── frontend/
│   └── index.html      # SPA con Tailwind CSS
├── vercel.json
└── README.md
```

## 🔧 API Endpoints

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/api/register` | POST | Registrar usuario |
| `/api/login` | POST | Autenticar |
| `/api/profile` | POST | Guardar perfil nutricional |
| `/api/plan/current` | GET | Obtener plan semanal |
| `/api/plan/swap` | POST | Cambiar opción de comida |
| `/api/weight/checkin` | POST | Registro semanal de peso |
| `/api/food-bank/options` | GET | Opciones del banco de comidas |
| `/api/shopping-list` | GET | Lista de la compra |
| `/api/stats` | GET | Estadísticas y progreso |

## 📊 Base de Datos

Tablas principales:
- `users` - Usuarios
- `user_profiles` - Perfiles nutricionales
- `weight_history` - Historial de peso
- `user_food_bank` - Banco de comidas (máx 6 por tipo)
- `weekly_plans` - Planes semanales
- `master_recipes` - Recetas maestras (Mercadona/Lidl)
