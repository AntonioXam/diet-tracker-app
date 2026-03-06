# 📊 Auditoría de Imágenes y Recursos - Diet Tracker FIT

**Fecha:** 2026-03-05  
**Estado:** ⚠️ CRÍTICO - Múltiples imágenes rotas y recursos faltantes

---

## 1. 📋 Imágenes Necesarias (TAREA 1)

| Tipo | Cantidad | Estado |
|------|----------|--------|
| **Imágenes de recetas** | 50 (cenas.json) / 350+ (promesa frontend) | ⚠️ URLs externas, 5 rotas |
| **Hero/background images** | 0 | ❌ No existen |
| **Iconos** | Usa emojis (🥗, 📊, etc.) | ✅ Funcional |
| **Favicons** | 5 tamaños referenciados | ❌ NO existen (404) |
| **OG images (social)** | 1 referenciada | ❌ NO existe (404) |

### Estructura esperada según `site.webmanifest`:
```
/favicon-16x16.png      ❌ 404
/favicon-32x32.png      ❌ 404
/apple-touch-icon.png   ❌ 404
/icon-192.png           ❌ 404
/icon-512.png           ❌ 404
/favicon.svg            ✅ 200 (existe)
/og-image.png           ❌ 404
```

---

## 2. 🔍 Imágenes Actuales en Repo (TAREA 2)

### Archivos encontrados:
```
diet-tracker-app/frontend/
├── favicon.svg          ✅ Existe (SVG con emoji 🥗)
└── (sin más imágenes)
```

### URLs de Unsplash en `cenas.json`:
- **Total recetas:** 50
- **URLs únicas:** 20 imágenes diferentes
- **Verificación de estado:**

| URL | Estado |
|-----|--------|
| photo-1467003909585-2f8a72700288 | ✅ 200 |
| photo-1550304943-4f24f54ddde9 | ✅ 200 |
| photo-1590412497706-e98f0916f6d8 | ❌ **404** |
| photo-1519708227418-c8fd9a32b7a2 | ✅ 200 |
| photo-1626700051175-6818013e1d4f | ✅ 200 |
| photo-1476718408415-c0805d168554 | ❌ **404** |
| photo-1604908176997-125f25cc6f3d | ✅ 200 |
| photo-1574484284008-86d47dc7b505 | ❌ **404** |
| photo-1565557623262-b51c2513a641 | ✅ 200 |
| photo-1596797038530-2c107229654b | ✅ 200 |
| photo-1512058564366-18510be2db19 | ✅ 200 |
| photo-1520072959219-c595dc870360 | ✅ 200 |
| photo-1529042410759-befb1204b468 | ✅ 200 |
| photo-1529312266912-b33cf6227e24 | ❌ **404** |
| photo-1544025162-d76690b6d012 | ❌ **404** |
| photo-1546069901-ba9599a7e63c | ✅ 200 |
| photo-1547592166-23ac45744acd | ✅ 200 |
| photo-1553621042-f6e147245754 | ✅ 200 |
| photo-1555939594-58d7cb561ad1 | ✅ 200 |

### 🚨 Imágenes ROTAS (5 de 20 = 25%):
1. `photo-1590412497706-e98f0916f6d8` - Tortilla de Espinacas
2. `photo-1476718408415-c0805d168554` - (receta en cenas.json)
3. `photo-1574484284008-86d47dc7b505` - (receta en cenas.json)
4. `photo-1529312266912-b33cf6227e24` - (receta en cenas.json)
5. `photo-1544025162-d76690b6d012` - (receta en cenas.json)

---

## 3. 🌐 Fuentes de Imágenes Investigadas (TAREA 3)

### 1️⃣ Unsplash (unsplash.com) ⭐ RECOMENDADO
| Característica | Detalle |
|----------------|---------|
| **Gratis** | ✅ Sí |
| **Atribución** | ⚠️ Requerida (pero no legalmente obligatoria, sí apreciada) |
| **Calidad** | ⭐⭐⭐⭐⭐ Excelente, fotos profesionales |
| **API** | ✅ Sí, REST API con límites generosos |
| **Recetas/Food** | ✅ Amplia colección (5000+ imágenes de comida) |
| **Límite API** | 50 req/hora sin key, 5000/hora con registro |

**Pros:**
- Calidad fotográfica profesional
- API bien documentada
- Sin costo para uso comercial
- URLs directas vía imgix (optimizadas)

**Contras:**
- Algunas URLs caducan (como vimos con 404s)
- Atribución recomendada

---

### 2️⃣ Pexels (pexels.com) ⭐ RECOMENDADO
| Característica | Detalle |
|----------------|---------|
| **Gratis** | ✅ Sí |
| **Atribución** | ❌ No requerida (pero apreciada) |
| **Calidad** | ⭐⭐⭐⭐ Muy buena |
| **API** | ✅ Sí, requiere API key gratis |
| **Recetas/Food** | ✅ Buena colección |
| **Límite API** | 20,000 req/mes gratis |

**Pros:**
- Sin atribución requerida
- API gratuita con buen límite
- Imágenes de calidad

**Contras:**
- Requiere registro para API
- Menos variedad que Unsplash en food

---

### 3️⃣ Pixabay (pixabay.com)
| Característica | Detalle |
|----------------|---------|
| **Gratis** | ✅ Sí |
| **Atribución** | ❌ No requerida |
| **Calidad** | ⭐⭐⭐ Variable (user-submitted) |
| **API** | ✅ Sí, 100 req/min |
| **Recetas/Food** | ✅ Colección decente |
| **Límite API** | 100 req/60 segundos |

**Pros:**
- Sin atribución
- Incluye vectores e ilustraciones
- Límite API generoso

**Contras:**
- Calidad inconsistente
- Requiere cachear 24h (términos API)
- No permite hotlinking permanente

---

### 4️⃣ Spoonacular API (spoonacular.com)
| Característica | Detalle |
|----------------|---------|
| **Gratis** | ⚠️ Plan limitado (150 req/día) |
| **Atribución** | ✅ Requerida en plan gratis |
| **Calidad** | ⭐⭐⭐⭐ Imágenes de recetas reales |
| **API** | ✅ Sí, especializada en comida |
| **Recetas/Food** | ⭐⭐⭐⭐⭐ 100,000+ recetas con imágenes |
| **Límite API** | 150 req/día (gratis), $9/mes para 5000/día |

**Pros:**
- Recetas completas con info nutricional
- Imágenes específicas por receta
- Datos estructurados

**Contras:**
- Límite muy bajo en plan gratis
- Costoso para producción
- Atribución requerida

---

### 5️⃣ Edamam API (edamam.com)
| Característica | Detalle |
|----------------|---------|
| **Gratis** | ⚠️ Plan Developer limitado |
| **Atribución** | ✅ Requerida |
| **Calidad** | ⭐⭐⭐⭐ Buena |
| **API** | ✅ Sí, nutrition + recipe |
| **Recetas/Food** | ⭐⭐⭐⭐⭐ Amplia base de datos |
| **Límite API** | 5,000 req/mes (Developer) |

**Pros:**
- Información nutricional detallada
- Recetas con imágenes
- Filtros dietéticos

**Contras:**
- Requiere aprobación para producción
- Más enfocado en nutrición que imágenes

---

## 4. 📋 Plan de Imágenes (TAREA 4)

### Escenario: 200 recetas

#### Fase 1: Urgente (1-2 días)
- [ ] **Reemplazar 5 URLs rotas** en `cenas.json`
- [ ] **Generar favicons** desde `favicon.svg`:
  - favicon-16x16.png
  - favicon-32x32.png
  - apple-touch-icon.png (180x180)
  - icon-192.png
  - icon-512.png
- [ ] **Crear OG image** (1200x630px)

#### Fase 2: Expansión (3-5 días)
- [ ] Descargar 200 imágenes de Unsplash/Pexels
- [ ] Organizar en `frontend/images/recipes/`
- [ ] Nombrar: `[categoria]-[id].webp`
- [ ] Actualizar `cenas.json` con rutas locales

#### Estructura de carpetas recomendada:
```
frontend/
├── images/
│   ├── og-image.png           (1200x630 - social)
│   ├── favicon/
│   │   ├── favicon-16x16.png
│   │   ├── favicon-32x32.png
│   │   ├── apple-touch-icon.png
│   │   ├── icon-192.png
│   │   └── icon-512.png
│   └── recipes/
│       ├── cenas-001.webp
│       ├── cenas-002.webp
│       └── ...
```

#### Actualización de DB:
```javascript
// Cambiar de URL externa a ruta local
"imagen_url": "https://images.unsplash.com/..." 
// →
"imagen_url": "/images/recipes/cenas-001.webp"
```

---

## 5. 🎯 Favicon/OG Status (TAREA 5)

### Favicon Actual:
| Recurso | Estado | Notas |
|---------|--------|-------|
| `/favicon.svg` | ✅ 200 | Existe, SVG con gradiente + emoji 🥗 |
| `/favicon-16x16.png` | ❌ 404 | **FALTA** |
| `/favicon-32x32.png` | ❌ 404 | **FALTA** |
| `/apple-touch-icon.png` | ❌ 404 | **FALTA** |
| `/icon-192.png` | ❌ 404 | **FALTA** |
| `/icon-512.png` | ❌ 404 | **FALTA** |
| `/favicon.ico` | ❌ 404 | **FALTA** |

### OG Image (Social Sharing):
| Recurso | Estado | Notas |
|---------|--------|-------|
| `/og-image.png` | ❌ 404 | **FALTA** - Twitter/FB mostrarán sin imagen |

### Tamaños requeridos:
- **Favicon:** 16x16, 32x32, 48x48 (.ico)
- **Apple Touch:** 180x180 (.png)
- **PWA:** 192x192, 512x512 (.png)
- **OG Image:** 1200x630 (.png o .jpg)

---

## 📊 Resumen Ejecutivo

### 🔴 Problemas Críticos:
1. **5 imágenes de recetas rotas (404)** - 25% de las URLs únicas
2. **Todos los favicons PNG/ICO faltan** - solo existe SVG
3. **OG image no existe** - social sharing sin imagen
4. **Dependencia de URLs externas** - riesgo de más 404s

### ✅ Lo que funciona:
- favicon.svg (pero navegadores viejos no lo soportan)
- 15 de 20 URLs de Unsplash activas
- Emojis como fallback de iconos

### 🎯 TOP 3 Fuentes Recomendadas:

| Rank | Fuente | Razón |
|------|--------|-------|
| 🥇 | **Unsplash** | Mejor calidad, API gratis, fácil integración |
| 🥈 | **Pexels** | Sin atribución requerida, buena API |
| 🥉 | **Pixabay** | Sin atribución, pero calidad variable |

### ⏱️ Tiempo Estimado:

| Tarea | Tiempo |
|-------|--------|
| Reemplazar 5 URLs rotas | 30 min |
| Generar favicons (6 tamaños) | 1 hora |
| Crear OG image | 30 min |
| Descargar 200 imágenes | 2-3 horas |
| Organizar y renombrar | 1 hora |
| Actualizar DB (cenas.json) | 1 hora |
| **TOTAL** | **~6-7 horas** |

---

## 🚀 Siguientes Pasos Recomendados

1. **INMEDIATO:** Generar favicons desde `favicon.svg`
2. **HOY:** Reemplazar 5 URLs rotas en `cenas.json`
3. **ESTA SEMANA:** Crear OG image y descargar 50 imágenes clave
4. **PRÓXIMA SEMANA:** Completar 200 imágenes y migrar a locales

---

**Generado por:** Subagent de Auditoría  
**Session:** audit-images-resources
