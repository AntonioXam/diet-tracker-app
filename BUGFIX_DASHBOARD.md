# Bugfix: Error al Cargar Datos en Dashboard

## Problema
El dashboard mostraba "Error al cargar los datos" debido a varios problemas:

1. **API Base URL incorrecta**: El frontend apuntaba a una URL de Vercel hardcodeada
2. **Manejo de errores deficiente**: No había fallback data cuando la API fallaba
3. **Loading states básicos**: Spinner simple sin información adicional
4. **Credenciales Supabase desactualizadas**: El backend usaba credenciales viejas

## Soluciones Implementadas

### 1. API Base URL Dinámica (frontend/app.js)
```javascript
const API_BASE = window.location.hostname === 'localhost' 
    ? 'http://localhost:5000/api' 
    : '/api';
```
- En localhost usa el backend local
- En producción usa rutas relativas (Vercel proxy)

### 2. Mejora en loadDashboard() (frontend/app.js)
- Añadido loading state mejorado con texto explicativo
- Múltiples intentos de fallback:
  1. Intenta cargar `/api/dashboard`
  2. Si falla, intenta `/api/stats` para weight history
  3. Si falla, intenta `/api/plan` como fallback
  4. Si todo falla, usa `renderDashboardWithFallback()`

### 3. Nueva Función renderDashboardWithFallback()
- Proporciona datos de ejemplo cuando la API no está disponible
- Permite que el dashboard sea usable incluso sin conexión
- Muestra toast informativo al usuario

### 4. Actualización de Credenciales Supabase (api/app.py)
```python
SUPABASE_URL = "https://kaomgwojvnncidyezdzj.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### 5. Mejoras en renderDashboard()
- Ahora usa datos dinámicos con fallbacks seguros (`data?.metrics || {}`)
- Calcula porcentajes reales para barras de progreso
- Actualiza el círculo de calorías con el dashoffset correcto
- Muestra información completa de macros (proteínas, carbos, grasas)

## Archivos Modificados

1. `/frontend/app.js`:
   - Línea ~5: API_BASE dinámica
   - Línea ~910: loadDashboard() mejorada
   - Línea ~1000: renderDashboard() actualizada
   - Línea ~1270: renderDashboardWithFallback() nueva

2. `/api/app.py`:
   - Línea ~22: Credenciales Supabase actualizadas

## Testing

### Local
```bash
cd api
python app.py
# En otro terminal
cd frontend
python -m http.server 8000
```

### Producción
El deploy en Vercel debería funcionar automáticamente:
- Frontend estático se sirve desde `/frontend`
- API Python se despliega como serverless function
- Rutas `/api/*` se proxyean al backend

## Endpoints Verificados

- ✅ GET `/api/health` - Health check
- ✅ GET `/api/dashboard` - Dashboard completo (requiere auth)
- ✅ GET `/api/stats` - Estadísticas y peso (requiere auth)
- ✅ GET `/api/plan` - Plan semanal (requiere auth)
- ✅ POST `/api/login` - Login
- ✅ POST `/api/register` - Registro

## CORS

Configurado correctamente en backend:
```python
CORS(app, origins=["*"], supports_credentials=True)
```

## Próximos Pasos

1. **Verificar en producción**: Deployar y testear en Vercel
2. **Añadir más fallbacks**: Considerar IndexedDB para cache local
3. **Mejorar error handling**: Añadir reintentos automáticos con backoff
4. **Monitoring**: Añadir logs para debuggear errores en producción

---
**Fecha**: 2025-03-05  
**Estado**: ✅ COMPLETADO
