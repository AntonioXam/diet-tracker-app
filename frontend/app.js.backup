// Diet Tracker App - JavaScript
// API Base URL
const API_BASE = 'https://diet-tracker-app-ten.vercel.app/api';

// Estado global
let user = null;
let currentPlan = null;
let currentDay = 1;
let weightChart = null;

// ==================== MODO OSCURO ====================

// Inicializar modo oscuro
function initDarkMode() {
  const savedTheme = localStorage.getItem('theme');
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  
  if (savedTheme === 'dark' || (!savedTheme && prefersDark)) {
    document.documentElement.classList.add('dark');
    updateDarkModeToggle('🌙');
  } else {
    document.documentElement.classList.remove('dark');
    updateDarkModeToggle('☀️');
  }
}

// Alternar modo oscuro/claro
function toggleDark() {
  const isDark = document.documentElement.classList.toggle('dark');
  localStorage.setItem('theme', isDark ? 'dark' : 'light');
  updateDarkModeToggle(isDark ? '🌙' : '☀️');
  
  // Actualizar gráfico si existe
  if (weightChart) {
    updateChartTheme();
  }
  
  // Mostrar feedback
  showToast(`Modo ${isDark ? 'oscuro' : 'claro'} activado`, 'info');
}

// Actualizar icono del toggle
function updateDarkModeToggle(icon) {
  const toggleBtn = document.querySelector('button[onclick="toggleDark()"]');
  if (toggleBtn) {
    toggleBtn.textContent = icon;
    toggleBtn.setAttribute('aria-label', icon === '🌙' ? 'Cambiar a modo claro' : 'Cambiar a modo oscuro');
  }
}

// Actualizar tema del gráfico
function updateChartTheme() {
  if (!weightChart) return;
  
  const isDark = document.documentElement.classList.contains('dark');
  const gridColor = isDark ? '#334155' : '#e2e8f0';
  const tickColor = isDark ? '#94a3b8' : '#64748b';
  const tooltipBg = isDark ? '#1e293b' : '#fff';
  const tooltipTitle = isDark ? '#f1f5f9' : '#0f172a';
  const tooltipBody = isDark ? '#cbd5e1' : '#475569';
  const borderColor = isDark ? '#475569' : '#e2e8f0';
  
  weightChart.options.plugins.tooltip.backgroundColor = tooltipBg;
  weightChart.options.plugins.tooltip.titleColor = tooltipTitle;
  weightChart.options.plugins.tooltip.bodyColor = tooltipBody;
  weightChart.options.plugins.tooltip.borderColor = borderColor;
  
  weightChart.options.scales.y.grid.color = gridColor;
  weightChart.options.scales.y.ticks.color = tickColor;
  weightChart.options.scales.x.ticks.color = tickColor;
  
  weightChart.update();
}

// ==================== AUTENTICACIÓN ====================

// Mostrar/ocultar modales
function showModal(type) {
  document.getElementById(`${type}-modal`).classList.remove('hidden');
  document.getElementById(`${type}-modal`).setAttribute('aria-hidden', 'false');
  
  // Enfocar primer campo
  setTimeout(() => {
    const firstInput = document.querySelector(`#${type}-modal input`);
    if (firstInput) firstInput.focus();
  }, 100);
}

function hideModal(type) {
  document.getElementById(`${type}-modal`).classList.add('hidden');
  document.getElementById(`${type}-modal`).setAttribute('aria-hidden', 'true');
}

// Registro
async function register() {
  const username = document.getElementById('reg-username').value.trim();
  const password = document.getElementById('reg-password').value.trim();
  const weight = parseFloat(document.getElementById('reg-weight').value);
  const height = parseInt(document.getElementById('reg-height').value);
  const age = parseInt(document.getElementById('reg-age').value);
  const activity = document.getElementById('reg-activity').value;
  const goal = document.getElementById('reg-goal').value;

  if (!username || !password || !weight || !height || !age || !activity || !goal) {
    showToast('Por favor completa todos los campos', 'error');
    return;
  }

  if (password.length < 6) {
    showToast('La contraseña debe tener al menos 6 caracteres', 'error');
    return;
  }

  try {
    const response = await fetch(`${API_BASE}/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password, weight, height, age, activity, goal })
    });

    const data = await response.json();
    
    if (response.ok) {
      // Si la API devuelve token, usarlo; si no, usar user id como token
      const token = data.token || (data.user && data.user.id ? data.user.id.toString() : null);
      user = { username, token: token, id: data.user?.id };
      localStorage.setItem('user', JSON.stringify(user));
      document.getElementById('user-avatar').textContent = username.charAt(0).toUpperCase();
      document.getElementById('user-name').textContent = username;
      
      hideModal('register');
      showToast('¡Cuenta creada con éxito!', 'success');
      loadDash();
    } else {
      showToast(data.error || 'Error en el registro', 'error');
    }
  } catch (err) {
    showToast('Error de conexión', 'error');
    console.error(err);
  }
}

// Login
async function login() {
  const username = document.getElementById('login-username').value.trim();
  const password = document.getElementById('login-password').value.trim();

  if (!username || !password) {
    showToast('Por favor completa todos los campos', 'error');
    return;
  }

  try {
    const response = await fetch(`${API_BASE}/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    });

    const data = await response.json();
    
    if (response.ok) {
      // Si la API devuelve token, usarlo; si no, usar user id como token
      const token = data.token || (data.user && data.user.id ? data.user.id.toString() : null);
      user = { username, token: token, id: data.user?.id };
      localStorage.setItem('user', JSON.stringify(user));
      document.getElementById('user-avatar').textContent = username.charAt(0).toUpperCase();
      document.getElementById('user-name').textContent = username;
      
      hideModal('login');
      showToast(`¡Bienvenido de nuevo, ${username}!`, 'success');
      loadDash();
    } else {
      showToast(data.error || 'Credenciales incorrectas', 'error');
    }
  } catch (err) {
    showToast('Error de conexión', 'error');
    console.error(err);
  }
}

// Logout
function logout() {
  user = null;
  localStorage.removeItem('user');
  document.getElementById('welcome').classList.remove('hidden');
  document.getElementById('dashboard').classList.add('hidden');
  document.getElementById('nav-auth').classList.remove('hidden');
  document.getElementById('nav-user').classList.add('hidden');
  showToast('Sesión cerrada', 'info');
}

// ==================== DASHBOARD ====================

// Cargar dashboard
async function loadDash() {
  if (!user) return;
  
  document.getElementById('welcome').classList.add('hidden');
  document.getElementById('dashboard').classList.remove('hidden');
  document.getElementById('nav-auth').classList.add('hidden');
  document.getElementById('nav-user').classList.remove('hidden');
  
  // Mostrar loader
  document.getElementById('dashboard-loader').classList.remove('hidden');
  
  try {
    // Cargar plan actual
    const userId = user.id || user.token; // user.id guardado en registro, token puede ser el id
    const planRes = await fetch(`${API_BASE}/plan/current?user_id=${userId}`, {
      headers: { 'Authorization': `Bearer ${user.token}` }
    });
    
    if (!planRes.ok) throw new Error('Error cargando plan');
    
    currentPlan = await planRes.json();
    
    // Cargar historial de peso
    const historyRes = await fetch(`${API_BASE}/weight/history?user_id=${userId}`, {
      headers: { 'Authorization': `Bearer ${user.token}` }
    });
    
    const history = historyRes.ok ? await historyRes.json() : [];
    
    // Actualizar UI
    updateDashboard(currentPlan, history);
    
    // Ocultar loader
    document.getElementById('dashboard-loader').classList.add('hidden');
    
  } catch (err) {
    console.error('Error loading dashboard:', err);
    showToast('Error cargando datos del plan', 'error');
    document.getElementById('dashboard-loader').classList.add('hidden');
  }
}

// Actualizar dashboard
function updateDashboard(plan, history) {
  // Calorías objetivo
  document.getElementById('dash-cals').textContent = plan.daily_calories.toLocaleString();
  
  // Peso actual
  const latestWeight = history.length > 0 ? history[history.length - 1].weight : plan.current_weight;
  document.getElementById('dash-weight').textContent = `${latestWeight} kg`;
  
  // Progreso (simulado)
  const progress = Math.min(Math.floor((Math.random() * 30) + 70), 100);
  document.getElementById('dash-progress').textContent = `${progress}%`;
  document.getElementById('progress-bar').style.width = `${progress}%`;
  
  // Número de semana
  const weekNum = Math.floor((new Date() - new Date(plan.created_at)) / (7 * 24 * 60 * 60 * 1000)) + 1;
  document.getElementById('week-number').textContent = weekNum;
  
  // Actualizar gráfico de peso
  updateWeightChart(history);
  
  // Cargar comidas del día actual
  loadMeals(currentDay);
}

// Actualizar gráfico de peso
function updateWeightChart(history) {
  const ctx = document.getElementById('weightChart').getContext('2d');
  
  if (weightChart) weightChart.destroy();
  
  const isDark = document.documentElement.classList.contains('dark');
  
  weightChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: history.map(h => new Date(h.created_at).toLocaleDateString('es-ES', { day: 'numeric', month: 'short' })),
      datasets: [{
        label: 'Peso (kg)',
        data: history.map(h => h.weight),
        borderColor: '#8b5cf6',
        backgroundColor: 'rgba(139, 92, 246, 0.1)',
        borderWidth: 3,
        fill: true,
        tension: 0.4,
        pointBackgroundColor: '#8b5cf6',
        pointBorderColor: '#fff',
        pointBorderWidth: 2,
        pointRadius: 5,
        pointHoverRadius: 7
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: isDark ? '#1e293b' : '#fff',
          titleColor: isDark ? '#f1f5f9' : '#0f172a',
          bodyColor: isDark ? '#cbd5e1' : '#475569',
          borderColor: isDark ? '#475569' : '#e2e8f0',
          borderWidth: 1,
          padding: 12,
          displayColors: false,
          callbacks: {
            label: (ctx) => `${ctx.parsed.y} kg`
          }
        }
      },
      scales: {
        y: {
          beginAtZero: false,
          grid: { color: isDark ? '#334155' : '#e2e8f0' },
          ticks: { color: isDark ? '#94a3b8' : '#64748b' }
        },
        x: {
          grid: { display: false },
          ticks: { color: isDark ? '#94a3b8' : '#64748b' }
        }
      }
    }
  });
}

// ==================== COMIDAS ====================

// Establecer día
function setDay(day) {
  currentDay = day;
  
  // Actualizar botones activos
  document.querySelectorAll('.day-btn').forEach((btn, idx) => {
    const isActive = idx === day - 1;
    btn.classList.toggle('gradient', isActive);
    btn.classList.toggle('text-white', isActive);
    btn.classList.toggle('scale-105', isActive);
    btn.classList.toggle('bg-white', !isActive);
    btn.classList.toggle('dark:bg-gray-800', !isActive);
    btn.classList.toggle('text-gray-700', !isActive);
    btn.classList.toggle('dark:text-gray-300', !isActive);
    btn.setAttribute('aria-pressed', isActive);
  });
  
  // Cargar comidas
  loadMeals(day);
}

// Cargar comidas del día
async function loadMeals(day) {
  if (!currentPlan || !user) return;
  
  const mealsContainer = document.getElementById('meals');
  mealsContainer.innerHTML = '<div class="text-center py-8"><div class="loading-spinner mx-auto mb-4"></div><p class="text-gray-500 dark:text-gray-400">Cargando comidas...</p></div>';
  
  try {
    // Obtener opciones de comida
    const optionsRes = await fetch(`${API_BASE}/food-bank/options`, {
      headers: { 'Authorization': `Bearer ${user.token}` }
    });
    
    if (!optionsRes.ok) throw new Error('Error cargando opciones');
    
    const options = await optionsRes.json();
    
    // Filtrar comidas para el día actual
    const dayMeals = options.filter(meal => meal.day_of_week === day);
    
    // Renderizar comidas
    renderMeals(dayMeals, mealsContainer);
    
  } catch (err) {
    console.error('Error loading meals:', err);
    mealsContainer.innerHTML = '<div class="text-center py-8 text-red-500">Error cargando las comidas</div>';
  }
}

// Renderizar comidas
function renderMeals(meals, container) {
  if (meals.length === 0) {
    container.innerHTML = '<div class="text-center py-8 text-gray-500 dark:text-gray-400">No hay comidas programadas para hoy</div>';
    return;
  }
  
  // Agrupar por tipo de comida
  const mealsByType = {
    breakfast: meals.filter(m => m.meal_type === 'breakfast'),
    lunch: meals.filter(m => m.meal_type === 'lunch'),
    dinner: meals.filter(m => m.meal_type === 'dinner'),
    snack: meals.filter(m => m.meal_type === 'snack')
  };
  
  const mealTypes = [
    { id: 'breakfast', name: 'Desayuno', icon: '☕' },
    { id: 'lunch', name: 'Almuerzo', icon: '🍽️' },
    { id: 'dinner', name: 'Cena', icon: '🌙' },
    { id: 'snack', name: 'Snack', icon: '🍎' }
  ];
  
  let html = '';
  
  mealTypes.forEach(type => {
    const typeMeals = mealsByType[type.id];
    if (typeMeals.length === 0) return;
    
    // Calcular calorías totales para este tipo
    const totalCalories = typeMeals.reduce((sum, meal) => sum + meal.calories, 0);
    
    html += `
      <div class="glass-card rounded-3xl shadow-xl border border-white/30 dark:border-gray-700/50 overflow-hidden card-hover">
        <div class="p-6">
          <div class="flex items-center justify-between mb-4">
            <div class="flex items-center gap-3">
              <div class="w-12 h-12 gradient rounded-2xl flex items-center justify-center text-2xl shadow-lg">${type.icon}</div>
              <div>
                <h3 class="font-black text-lg text-gray-900 dark:text-white">${type.name}</h3>
                <p class="text-sm text-gray-500 dark:text-gray-400">${totalCalories} kcal total</p>
              </div>
            </div>
            <span class="text-xs font-bold bg-purple-100 dark:bg-purple-900/30 text-purple-600 dark:text-purple-400 px-3 py-1.5 rounded-full">
              ${typeMeals.length} ${typeMeals.length === 1 ? 'opción' : 'opciones'}
            </span>
          </div>
          
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            ${typeMeals.map(meal => renderMealCard(meal)).join('')}
          </div>
        </div>
      </div>
    `;
  });
  
  container.innerHTML = html || '<div class="text-center py-8 text-gray-500 dark:text-gray-400">No hay comidas programadas para hoy</div>';
}

// Renderizar tarjeta de comida
function renderMealCard(meal) {
  // Colores de placeholder basados en tipo de comida
  const placeholderColors = {
    breakfast: 'from-yellow-400 to-orange-500',
    lunch: 'from-green-400 to-teal-500',
    dinner: 'from-blue-400 to-indigo-500',
    snack: 'from-pink-400 to-rose-500'
  };
  
  const colorClass = placeholderColors[meal.meal_type] || 'from-gray-400 to-gray-600';
  
  return `
    <div class="recipe-card bg-white dark:bg-gray-800 rounded-2xl overflow-hidden border border-gray-200 dark:border-gray-700">
      <div class="relative h-40 overflow-hidden">
        ${meal.image_url ? 
          `<img src="${meal.image_url}" alt="${meal.name}" class="w-full h-full object-cover recipe-image" loading="lazy">` :
          `<div class="w-full h-full ${colorClass} bg-gradient-to-br flex items-center justify-center">
            <span class="text-4xl text-white opacity-80">${getMealIcon(meal.meal_type)}</span>
          </div>`
        }
        <div class="absolute bottom-0 left-0 right-0 image-overlay p-4">
          <span class="text-xs font-bold text-white bg-black/30 backdrop-blur-sm px-2 py-1 rounded-full">
            ${meal.calories} kcal
          </span>
        </div>
      </div>
      <div class="p-4">
        <h4 class="font-bold text-gray-900 dark:text-white mb-2 line-clamp-1">${meal.name}</h4>
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-2">
            <span class="text-xs text-gray-500 dark:text-gray-400">${meal.protein}g proteína</span>
            <span class="text-xs text-gray-500 dark:text-gray-400">•</span>
            <span class="text-xs text-gray-500 dark:text-gray-400">${meal.carbs}g carbos</span>
          </div>
          <button onclick="addToShoppingList('${meal.id}')" class="text-xs font-bold bg-accent-100 dark:bg-accent-900/30 text-accent-600 dark:text-accent-400 px-3 py-1.5 rounded-full hover:bg-accent-200 dark:hover:bg-accent-800 transition-colors">
            + Lista
          </button>
        </div>
      </div>
    </div>
  `;
}

// Obtener icono por tipo de comida
function getMealIcon(mealType) {
  const icons = {
    breakfast: '☕',
    lunch: '🍽️',
    dinner: '🌙',
    snack: '🍎'
  };
  return icons[mealType] || '🍴';
}

// ==================== LISTA DE COMPRAS ====================

// Añadir a lista de compras
async function addToShoppingList(mealId) {
  if (!user) {
    showToast('Inicia sesión para usar la lista de compras', 'warning');
    return;
  }
  
  try {
    const response = await fetch(`${API_BASE}/shopping/add`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${user.token}`
      },
      body: JSON.stringify({ meal_id: mealId })
    });
    
    if (response.ok) {
      showToast('Añadido a la lista de compras', 'success');
    } else {
      showToast('Error añadiendo a la lista', 'error');
    }
  } catch (err) {
    console.error('Error adding to shopping list:', err);
    showToast('Error de conexión', 'error');
  }
}

// Mostrar lista de compras
async function showShoppingList() {
  if (!user) {
    showToast('Inicia sesión para ver tu lista', 'warning');
    return;
  }
  
  try {
    const response = await fetch(`${API_BASE}/shopping/list`, {
      headers: { 'Authorization': `Bearer ${user.token}` }
    });
    
    if (!response.ok) throw new Error('Error cargando lista');
    
    const shoppingList = await response.json();
    renderShoppingList(shoppingList);
    showModal('shopping');
    
  } catch (err) {
    console.error('Error loading shopping list:', err);
    showToast('Error cargando lista de compras', 'error');
  }
}

// Renderizar lista de compras
function renderShoppingList(list) {
  const container = document.getElementById('shopping-list-content');
  if (!container) return;
  
  if (!list || list.length === 0) {
    container.innerHTML = '<div class="text-center py-8 text-gray-500 dark:text-gray-400">Tu lista de compras está vacía</div>';
    return;
  }
  
  // Agrupar por supermercado
  const byStore = list.reduce((acc, item) => {
    const store = item.store || 'general';
    if (!acc[store]) acc[store] = [];
    acc[store].push(item);
    return acc;
  }, {});
  
  let html = '';
  
  Object.entries(byStore).forEach(([store, items]) => {
    html += `
      <div class="mb-6">
        <h4 class="font-bold text-lg text-gray-900 dark:text-white mb-3 flex items-center gap-2">
          <span class="text-xl">${getStoreIcon(store)}</span>
          ${store.charAt(0).toUpperCase() + store.slice(1)}
        </h4>
        <div class="space-y-2">
          ${items.map(item => `
            <div class="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-800 rounded-xl">
              <div class="flex items-center gap-3">
                <input type="checkbox" class="w-5 h-5 rounded border-gray-300 dark:border-gray-600" 
                       onchange="toggleShoppingItem('${item.id}', this.checked)">
                <span class="text-gray-900 dark:text-white">${item.name}</span>
              </div>
              <span class="text-sm text-gray-500 dark:text-gray-400">${item.quantity || '1 unidad'}</span>
            </div>
          `).join('')}
        </div>
      </div>
    `;
  });
  
  container.innerHTML = html;
}

// Obtener icono de supermercado
function getStoreIcon(store) {
  const icons = {
    mercadona: '🛒',
    lidl: '🏪',
    carrefour: '🛍️',
    general: '📋'
  };
  return icons[store] || '🛒';
}

// Alternar item de compra
async function toggleShoppingItem(itemId, checked) {
  try {
    const response = await fetch(`${API_BASE}/shopping/toggle`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${user.token}`
      },
      body: JSON.stringify({ item_id: itemId, checked })
    });
    
    if (!response.ok) {
      showToast('Error actualizando item', 'error');
    }
  } catch (err) {
    console.error('Error toggling shopping item:', err);
  }
}

// ==================== REGISTRO DE PESO ====================

// Registrar peso
async function registerWeight() {
  const weightInput = document.getElementById('weight-input');
  const weight = parseFloat(weightInput.value);
  
  if (!weight || weight < 30 || weight > 300) {
    showToast('Por favor ingresa un peso válido (30-300 kg)', 'error');
    weightInput.classList.add('error-shake');
    setTimeout(() => weightInput.classList.remove('error-shake'), 500);
    return;
  }
  
  try {
    const response = await fetch(`${API_BASE}/weight/checkin`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${user.token}`
      },
      body: JSON.stringify({ weight })
    });
    
    if (response.ok) {
      showToast(`Peso registrado: ${weight} kg`, 'success');
      weightInput.value = '';
      hideModal('edit');
      loadDash(); // Recargar dashboard para actualizar gráfico
    } else {
      showToast('Error registrando peso', 'error');
    }
  } catch (err) {
    console.error('Error registering weight:', err);
    showToast('Error de conexión', 'error');
  }
}

// ==================== NOTIFICACIONES ====================

// Mostrar notificación toast
function showToast(message, type = 'info') {
  const container = document.getElementById('toast-container');
  const toast = document.createElement('div');
  
  const types = {
    success: { bg: 'bg-green-500', icon: '✅' },
    error: { bg: 'bg-red-500', icon: '❌' },
    warning: { bg: 'bg-yellow-500', icon: '⚠️' },
    info: { bg: 'bg-blue-500', icon: 'ℹ️' }
  };
  
  const config = types[type] || types.info;
  
  toast.className = `${config.bg} text-white px-5 py-3 rounded-2xl shadow-2xl font-bold flex items-center gap-3 animate-slide-up max-w-sm toast`;
  toast.innerHTML = `
    <span class="text-xl">${config.icon}</span>
    <span>${message}</span>
    <button onclick="this.parentElement.remove()" class="ml-auto text-white/80 hover:text-white text-lg" aria-label="Cerrar">×</button>
  `;
  
  container.appendChild(toast);
  
  // Auto-remover después de 5 segundos
  setTimeout(() => {
    if (toast.parentElement) {
      toast.remove();
    }
  }, 5000);
}

// ==================== INICIALIZACIÓN ====================

// Inicializar aplicación
function initApp() {
  // Inicializar modo oscuro
  initDarkMode();
  
  // Cargar usuario si existe
  const saved = localStorage.getItem('user');
  if (saved) {
    try {
      user = JSON.parse(saved);
      document.getElementById('user-avatar').textContent = user.username.charAt(0).toUpperCase();
      document.getElementById('user-name').textContent = user.username;
      loadDash();
    } catch (err) {
      console.error('Error loading saved user:', err);
      localStorage.removeItem('user');
    }
  }
  
  // Configurar listeners para tecla Escape
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      ['login', 'register', 'edit', 'options', 'shopping'].forEach(hideModal);
    }
  });
  
  // Configurar año actual en footer
  document.getElementById('current-year').textContent = new Date().getFullYear();
}

// Iniciar cuando el DOM esté listo
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initApp);
} else {
  initApp();
}