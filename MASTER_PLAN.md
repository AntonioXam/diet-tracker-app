# 🎯 PLAN MAESTRO - Diet Tracker App

## 📊 ESTADO ACTUAL - VERIFICACIÓN COMPLETA

### ✅ LO QUE TENEMOS:
- Frontend: Landing + Dashboard (HTML/CSS/JS)
- Backend: Flask API con 11 endpoints definidos
- Database: Supabase con 7 tablas
- Deploy: Vercel configurado

### ❌ LO QUE FALLA (Reportado por usuario):
1. ❌ Login falla / emails no se pueden resetear
2. ❌ Días de la semana mal mostrados
3. ❌ Registrar comida → no hace nada
4. ❌ Lista de la compra → falla
5. ❌ Opciones de usuario → no hacen nada
6. ❌ Imágenes no se cargan correctamente
7. ❌ Endpoints pueden no estar implementados completamente

---

## 🔍 FASE 1: AUDITORÍA COMPLETA (Día 1)

### Bot 1: **audit-backend-bot**
**TAREA:** Verificar TODOS los endpoints del backend
- [ ] Listar los 11 endpoints en api/app.py
- [ ] Verificar cada endpoint está IMPLEMENTADO (no solo definido)
- [ ] Testear cada endpoint manualmente
- [ ] Verificar conexión real a Supabase
- [ ] Checkear logs de errores

**Endpoints a verificar:**
1. POST /api/register
2. POST /api/login
3. POST /api/onboarding
4. GET /api/profile
5. POST /api/profile
6. GET /api/recipes
7. GET /api/plan
8. POST /api/plan/swap
9. GET /api/shopping-list
10. POST /api/weight
11. GET /api/stats
12. POST /api/food-log
13. GET /api/dashboard

### Bot 2: **audit-frontend-bot**
**TAREA:** Verificar frontend completo
- [ ] Revisar TODAS las llamadas fetch en app.js
- [ ] Verificar coinciden con endpoints backend
- [ ] Testear flujo completo manualmente
- [ ] Identificar botones/enlaces rotos
- [ ] Verificar manejo de errores

**Flujos a testear:**
1. Landing → Registro → Login → Dashboard
2. Onboarding completo (5 pasos)
3. Registrar comida
4. Ver plan semanal
5. Lista de la compra
6. Perfil de usuario
7. Logout

### Bot 3: **audit-database-bot**
**TAREA:** Verificar base de datos Supabase
- [ ] Conectar a Supabase directamente
- [ ] Verificar las 7 tablas existen
- [ ] Verificar RLS policies activas
- [ ] Testear queries reales
- [ ] Verificar datos seed (recetas)
- [ ] Resetear DB para testing (borrar users test)

**Tablas a verificar:**
1. user_profiles
2. master_recipes
3. weekly_plans
4. plan_meals
5. weight_logs
6. shopping_lists
7. food_logs

### Bot 4: **audit-images-bot**
**TAREA:** Verificar imágenes y recursos
- [ ] Identificar TODAS las imágenes necesarias
- [ ] Verificar URLs de imágenes (Unsplash, etc.)
- [ ] Checkear favicons
- [ ] Verificar OG images
- [ ] Buscar fuentes de imágenes gratuitas de calidad
- [ ] Crear lista de imágenes faltantes

**Imágenes necesarias:**
- Recetas (200+)
- Fondos/hero
- Iconos
- Favicons
- OG social sharing

---

## 🔧 FASE 2: ARREGLOS CRÍTICOS (Día 2-3)

### Bot 5: **fix-auth-bot**
**TAREA:** Arreglar login/registro completamente
- [ ] Implementar POST /api/register CORRECTAMENTE
- [ ] Implementar POST /api/login CORRECTAMENTE
- [ ] Implementar POST /api/recover-password
- [ ] Manejo de errores claro
- [ ] Testear con emails reales
- [ ] Resetear DB de test users

### Bot 6: **fix-dashboard-bot**
**TAREA:** Arreglar dashboard completo
- [ ] GET /api/dashboard IMPLEMENTAR si no existe
- [ ] Mostrar datos reales de usuario
- [ ] Días de semana CORRECTOS (Lunes a Domingo en español)
- [ ] Círculo de calorías funcional
- [ ] Barras de macros funcionales
- [ ] Gráfico de peso con datos reales

### Bot 7: **fix-food-logging-bot**
**TAREA:** Arreglar registro de comidas
- [ ] POST /api/food-log IMPLEMENTAR
- [ ] Buscador de recetas funcional
- [ ] Añadir comida → actualiza dashboard
- [ ] Historial de comidas del día
- [ ] Cálculo automático de macros

### Bot 8: **fix-shopping-list-bot**
**TAREA:** Arreglar lista de compra
- [ ] GET /api/shopping-list IMPLEMENTAR
- [ ] Generar lista desde plan semanal
- [ ] Marcar items como comprados
- [ ] Agrupar por supermercado
- [ ] Exportar lista (copy/paste)

### Bot 9: **fix-user-options-bot**
**TAREA:** Arreglar opciones de usuario
- [ ] Perfil de usuario funcional
- [ ] Editar perfil
- [ ] Cambiar contraseña
- [ ] Logout funciona
- [ ] Settings guardados

---

## 🎨 FASE 3: PULIR UI/UX (Día 4)

### Bot 10: **ui-polish-bot**
**TAREA:** Pulir interfaz completa
- [ ] Espaciados consistentes
- [ ] Tipografía legible
- [ ] Colores contraste WCAG AA
- [ ] Animaciones suaves
- [ ] Loading states
- [ ] Mensajes de error claros
- [ ] Responsive perfecto

### Bot 11: **images-resources-bot**
**TAREA:** Imágenes y recursos
- [ ] Buscar imágenes recetas en Unsplash/Pexels
- [ ] Descargar/optimizar imágenes
- [ ] Subir a Vercel/CDN
- [ ] Actualizar DB con URLs correctas
- [ ] Generar favicons completos
- [ ] Crear OG image

**Fuentes de imágenes:**
- Unsplash (gratis, alta calidad)
- Pexels (gratis)
- Pixabay (gratis)
- Recipe images específicas

---

## 🧪 FASE 4: TESTING COMPLETO (Día 5)

### Bot 12: **qa-testing-bot**
**TAREA:** Testing exhaustivo
- [ ] Testear CADA endpoint
- [ ] Testear CADA flujo de usuario
- [ ] Testear en Chrome, Firefox, Safari
- [ ] Testear en móvil (iOS, Android)
- [ ] Testear en tablet
- [ ] Verificar consola sin errores
- [ ] Verificar network sin 404/500
- [ ] Lighthouse score >90
- [ ] Crear reporte de bugs

**Checklist de testing:**
1. Registro nuevo usuario ✅
2. Login ✅
3. Recuperar contraseña ✅
4. Onboarding 5 pasos ✅
5. Dashboard carga datos ✅
6. Registrar comida ✅
7. Ver plan semanal ✅
8. Lista de compra ✅
9. Editar perfil ✅
10. Logout ✅
11. Modo oscuro ✅
12. Responsive móvil ✅

---

## 🚀 FASE 5: DEPLOY VERIFICADO (Día 6)

### Bot 13: **deploy-verify-bot**
**TAREA:** Deploy con verificación completa
- [ ] Verificar vercel.json
- [ ] Verificar variables de entorno en Vercel
- [ ] Build sin errores
- [ ] Deploy a production
- [ ] Testear URL production
- [ ] Verificar SSL
- [ ] Checkear logs Vercel
- [ ] Performance check

**Pre-deploy checklist:**
- [ ] Todos los tests pasan
- [ ] No hay errores en consola
- [ ] Todos los endpoints responden
- [ ] Imágenes cargan
- [ ] Auth funciona
- [ ] Database conectada

---

## 📋 ENTREGABLES POR FASE:

### Fase 1 (Auditoría):
- [ ] Reporte completo de endpoints (cuáles existen, cuáles no)
- [ ] Reporte de bugs frontend
- [ ] Reporte estado database
- [ ] Lista de imágenes necesarias

### Fase 2 (Arreglos):
- [ ] Auth 100% funcional
- [ ] Dashboard 100% funcional
- [ ] Food logging 100% funcional
- [ ] Shopping list 100% funcional
- [ ] User options 100% funcionales

### Fase 3 (UI/UX):
- [ ] UI pulida y consistente
- [ ] Imágenes de calidad cargando
- [ ] Modo oscuro perfecto
- [ ] Responsive perfecto

### Fase 4 (Testing):
- [ ] Reporte de testing completo
- [ ] 0 errores en consola
- [ ] 0 errores en network
- [ ] Lighthouse >90

### Fase 5 (Deploy):
- [ ] Production deploy exitoso
- [ ] URL funcional
- [ ] Sin errores en Vercel logs

---

## ⏱️ TIMELINE ESTIMADO:

- **Día 1:** Auditoría completa (4 bots)
- **Día 2-3:** Arreglos críticos (5 bots)
- **Día 4:** UI/UX + Imágenes (2 bots)
- **Día 5:** Testing exhaustivo (1 bot)
- **Día 6:** Deploy verificado (1 bot)

**TOTAL:** 6 días para app 100% funcional

---

## 🎯 CRITERIOS DE ACEPTACIÓN:

La app se considera COMPLETA cuando:

1. ✅ Usuario puede registrarse con email real
2. ✅ Usuario puede hacer login
3. ✅ Usuario puede recuperar contraseña
4. ✅ Dashboard muestra datos reales (calorías, macros, peso)
5. ✅ Usuario puede registrar comidas
6. ✅ Usuario puede ver plan semanal (Lunes-Domingo en español)
7. ✅ Usuario puede ver lista de compra
8. ✅ Usuario puede editar perfil
9. ✅ Usuario puede hacer logout
10. ✅ Modo oscuro legible
11. ✅ Responsive en móvil
12. ✅ Sin errores en consola
13. ✅ Imágenes de recetas cargan
14. ✅ Lighthouse score >90

---

**NOTA:** NO subir NADA a production hasta que TODOS los criterios se cumplan.
Mejor tardar más pero subir app 100% funcional.
