# Diet Tracker FIT - Frontend

Aplicación web moderna para seguimiento de dieta con modo oscuro, diseño responsive y experiencia de usuario mejorada.

## 🚀 Características Implementadas

### 1. **Modo Oscuro Completo**
- ✅ Toggle persistente en localStorage
- ✅ Variables CSS para colores (modo claro/oscuro)
- ✅ Transiciones suaves entre modos
- ✅ Compatibilidad con preferencias del sistema
- ✅ Gráficos que se adaptan al tema

### 2. **Mejoras Visuales**
- ✅ Diseño moderno con gradientes y efectos glassmorphism
- ✅ Tipografía Inter mejorada
- ✅ Espaciado y consistencia visual
- ✅ Tarjetas de recetas con imágenes de la API
- ✅ Placeholders con colores por tipo de comida
- ✅ Efectos hover y micro-interacciones

### 3. **Responsive Design**
- ✅ Mobile-first approach
- ✅ Adaptación a tablet y escritorio
- ✅ Navegación optimizada para móviles
- ✅ Grids flexibles

### 4. **Experiencia de Usuario**
- ✅ Dashboard con estadísticas claras
- ✅ Progreso semanal visual
- ✅ Distribución de calorías por comidas
- ✅ Navegación por días intuitiva
- ✅ Feedback visual con toasts
- ✅ Estados de carga animados

### 5. **Integración con API**
- ✅ Conexión con API de Vercel
- ✅ Imágenes de recetas desde `image_url`
- ✅ Cálculo de calorías actualizado
- ✅ Lista de compras por supermercado

## 🛠️ Estructura de Archivos

```
frontend/
├── index.html          # HTML principal
├── styles.css          # Estilos CSS con variables
├── app.js              # Lógica JavaScript
├── README.md           # Esta documentación
└── CHANGELOG.md        # Historial de cambios
```

## 🎨 Variables CSS

El sistema de diseño usa variables CSS para colores:

```css
:root {
  /* Modo claro */
  --color-bg-primary: #ffffff;
  --color-text-primary: #0f172a;
  /* ... */
}

.dark {
  /* Modo oscuro */
  --color-bg-primary: #0f172a;
  --color-text-primary: #f1f5f9;
  /* ... */
}
```

## 📱 Breakpoints Responsive

- **Mobile**: < 640px
- **Tablet**: 640px - 1024px  
- **Desktop**: > 1024px

## 🎯 Funcionalidades Principales

### Autenticación
- Registro con datos personales
- Login persistente
- Avatar personalizado

### Dashboard
- Calorías objetivo diarias
- Peso actual y progreso
- Gráfico de evolución de peso
- Distribución de calorías por comidas

### Plan Diario
- Navegación por días de la semana
- Tarjetas de recetas con imágenes
- Información nutricional detallada
- Añadir a lista de compras

### Lista de Compras
- Agrupada por supermercado
- Checkboxes para marcar comprados
- Copiar al portapapeles
- Limpiar lista

## 🔧 Tecnologías Utilizadas

- **HTML5** con semántica mejorada
- **CSS3** con variables y animaciones
- **JavaScript Vanilla** (sin frameworks)
- **Tailwind CSS** para utilidades
- **Chart.js** para gráficos
- **Google Fonts** (Inter)

## 🚀 Instalación y Uso

1. Clonar el repositorio
2. Abrir `index.html` en un navegador moderno
3. La aplicación se conecta automáticamente a la API en Vercel

## 📈 Mejoras Futuras

- [ ] Notificaciones push
- [ ] Exportar datos a PDF
- [ ] Compartir progreso en redes
- [ ] Modo offline
- [ ] Integración con wearables

## 🎨 Paleta de Colores

### Modo Claro
- Primario: Gradiente púrpura (#667eea → #764ba2)
- Secundario: Azul (#3b82f6)
- Fondo: Gradiente suave (indigo → pink)

### Modo Oscuro
- Primario: Gradiente púrpura oscuro
- Fondo: Gradiente gris oscuro
- Texto: Blanco/gris claro

## 📱 Accesibilidad

- ✅ Navegación por teclado
- ✅ Etiquetas ARIA
- ✅ Contraste adecuado
- ✅ Textos alternativos
- ✅ Focus visible

## 🔒 Seguridad

- Tokens almacenados en localStorage
- Validación de formularios
- Sanitización de inputs
- CORS configurado en API

## 📊 Performance

- ✅ Imágenes lazy loading
- ✅ CSS optimizado
- ✅ JavaScript modular
- ✅ Cache de localStorage
- ✅ Animaciones CSS (no JS)

---

**Desarrollado con ❤️ para Diet Tracker FIT**