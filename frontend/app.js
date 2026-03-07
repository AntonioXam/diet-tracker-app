// Diet Tracker FIT - Frontend Completo
// API Base URL - relativa para producción en Vercel, localhost para desarrollo
const API_BASE = window.location.hostname === 'localhost' 
    ? 'http://localhost:5000/api' 
    : '/api';

// ==================== HELPERS DE FORMATEO ====================

/**
 * Formatea un número con decimales limpios
 * @param {number} value - El valor a formatear
 * @param {number} decimals - Número de decimales (default: 1)
 * @returns {string} - Valor formateado
 */
function formatNumber(value, decimals = 1) {
    if (value === null || value === undefined || isNaN(value)) return '0';
    const num = Number(value);
    // Redondear al número de decimales especificado
    return num.toFixed(decimals).replace(/\.0$/, '');
}

/**
 * Formatea calorías (sin decimales)
 * @param {number} calories 
 * @returns {string}
 */
function formatCalories(calories) {
    if (calories === null || calories === undefined || isNaN(calories)) return '0';
    return Math.round(Number(calories)).toString();
}

/**
 * Formatea gramos (con 1 decimal, eliminando .0)
 * @param {number} grams 
 * @returns {string}
 */
function formatGrams(grams) {
    return formatNumber(grams, 1);
}

// Estado global
let user = null;
let isDark = false;
let currentPlan = null;
let currentDay = 1;
let weightChart = null;
let onboardingStep = 0;
let onboardingData = {};

// ==================== INICIALIZACIÓN ====================

document.addEventListener('DOMContentLoaded', function() {
    initDarkMode();
    checkAuth();
    renderLandingPage();
});

// ==================== MODO OSCURO ====================

function initDarkMode() {
    const savedTheme = localStorage.getItem('theme');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    
    isDark = (savedTheme === 'dark' || (!savedTheme && prefersDark));
    
    if (isDark) {
        document.documentElement.classList.add('dark');
    }
    
    updateDarkIcon();
}

function toggleDark() {
    isDark = !isDark;
    
    if (isDark) {
        document.documentElement.classList.add('dark');
    } else {
        document.documentElement.classList.remove('dark');
    }
    
    localStorage.setItem('theme', isDark ? 'dark' : 'light');
    updateDarkIcon();
    showToast('Modo ' + (isDark ? 'oscuro' : 'claro') + ' activado', 'info');
    
    // Actualizar gráfico si existe
    if (weightChart) {
        updateChartTheme();
    }
}

function updateDarkIcon() {
    const el = document.getElementById('dark-icon');
    if (el) {
        el.textContent = isDark ? '☀️' : '🌙';
    }
}

function updateChartTheme() {
    if (!weightChart) return;
    
    const gridColor = isDark ? '#334155' : '#e2e8f0';
    const tickColor = isDark ? '#94a3b8' : '#64748b';
    const tooltipBg = isDark ? '#1e293b' : '#fff';
    const tooltipTitle = isDark ? '#f1f5f9' : '#0f172a';
    const tooltipBody = isDark ? '#cbd5e1' : '#475569';
    
    weightChart.options.scales.y.grid.color = gridColor;
    weightChart.options.scales.y.ticks.color = tickColor;
    weightChart.options.scales.x.ticks.color = tickColor;
    weightChart.options.plugins.tooltip.backgroundColor = tooltipBg;
    weightChart.options.plugins.tooltip.titleColor = tooltipTitle;
    weightChart.options.plugins.tooltip.bodyColor = tooltipBody;
    
    weightChart.update();
}

// ==================== NAVEGACIÓN ====================

// Toggle landing page mobile menu
function toggleLandingMenu() {
    const menu = document.getElementById('landing-mobile-menu');
    if (menu) {
        menu.classList.toggle('hidden');
    }
}

// Toggle dashboard mobile menu
function toggleDashboardMenu() {
    const menu = document.getElementById('dashboard-mobile-menu');
    if (menu) {
        menu.classList.toggle('hidden');
    }
}

function scrollToSection(id) {
    const element = document.getElementById(id);
    if (element) {
        element.scrollIntoView({ behavior: 'smooth' });
    }
    // Close mobile menu after navigation
    const landingMenu = document.getElementById('landing-mobile-menu');
    if (landingMenu && !landingMenu.classList.contains('hidden')) {
        landingMenu.classList.add('hidden');
    }
}

// Simple page router
function showPage(page) {
    const landingContent = document.getElementById('main-content');
    const dashboardContent = document.getElementById('dashboard-content');
    const navAuth = document.getElementById('nav-auth');
    const navUser = document.getElementById('nav-user');
    const dashboardMenuBtn = document.getElementById('dashboard-menu-btn');
    const landingMobileMenu = document.getElementById('landing-mobile-menu');
    
    if (page === 'landing') {
        // Show landing page
        landingContent.classList.remove('hidden');
        dashboardContent.classList.add('hidden');
        
        // Show auth buttons, hide user info
        navAuth.classList.remove('hidden');
        navAuth.classList.add('flex');
        navUser.classList.add('hidden');
        navUser.classList.remove('flex');
        
        // Hide dashboard menu button
        dashboardMenuBtn.classList.add('hidden');
        
        // Landing menu is triggered by a separate button if needed
        landingMobileMenu.classList.add('hidden');
    } else if (page === 'dashboard') {
        // Show dashboard
        landingContent.classList.add('hidden');
        dashboardContent.classList.remove('hidden');
        
        // Hide auth buttons, show user info
        navAuth.classList.add('hidden');
        navAuth.classList.remove('flex');
        navUser.classList.remove('hidden');
        navUser.classList.add('flex');
        
        // Show dashboard menu button
        dashboardMenuBtn.classList.remove('hidden');
        
        // Hide landing mobile menu
        landingMobileMenu.classList.add('hidden');
    }
}

// ==================== RENDERIZADO LANDING PAGE ====================

function renderLandingPage() {
    const mainContent = document.getElementById('main-content');
    mainContent.innerHTML = `
        <!-- Hero Section -->
        <section id="inicio" class="min-h-[80vh] flex items-center justify-center text-center px-4 py-20">
            <div class="max-w-4xl mx-auto">
                <div class="inline-block px-4 py-2 bg-purple-100 dark:bg-purple-900/30 rounded-full text-purple-600 dark:text-purple-400 font-semibold text-sm mb-6">
                    🎯 +350 recetas saludables
                </div>
                <h1 class="text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-black mb-6 dark:text-white leading-tight">
                    Tu mejor versión <br>
                    <span class="gradient-text">comienza aquí</span>
                </h1>
                <p class="text-lg sm:text-xl text-gray-600 dark:text-gray-300 mb-8 max-w-2xl mx-auto">
                    Planificación nutricional personalizada, seguimiento de progreso y recetas deliciosas. 
                    Todo lo que necesitas para alcanzar tus objetivos de salud.
                </p>
                <div class="flex flex-col sm:flex-row gap-4 justify-center items-center">
                    <button onclick="showModal('register')" class="btn-primary text-white px-8 py-4 rounded-2xl font-bold text-lg w-full sm:w-auto touch-target">
                        🚀 Comenzar gratis
                    </button>
                    <button onclick="showModal('login')" class="glass px-8 py-4 rounded-2xl font-bold text-lg text-gray-900 dark:text-white w-full sm:w-auto touch-target hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors">
                        👤 Ya tengo cuenta
                    </button>
                </div>
                <div class="mt-12 flex items-center justify-center gap-8 text-sm text-gray-500 dark:text-gray-400">
                    <div class="flex items-center gap-2">
                        <i class="fas fa-check-circle text-green-500"></i>
                        <span>Sin tarjeta requerida</span>
                    </div>
                    <div class="flex items-center gap-2">
                        <i class="fas fa-check-circle text-green-500"></i>
                        <span>Cancela cuando quieras</span>
                    </div>
                </div>
            </div>
        </section>

        <!-- Features Section -->
        <section id="features" class="py-20 px-4 bg-white dark:bg-gray-900">
            <div class="container mx-auto max-w-6xl">
                <div class="text-center mb-16">
                    <h2 class="text-3xl sm:text-4xl md:text-5xl font-black mb-4 dark:text-white">
                        Todo lo que necesitas
                    </h2>
                    <p class="text-lg text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">
                        Herramientas poderosas diseñadas para hacer tu viaje de salud más fácil y efectivo
                    </p>
                </div>
                
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 sm:gap-8">
                    <!-- Feature 1 -->
                    <div class="glass-card rounded-2xl p-6 sm:p-8 card-hover">
                        <div class="w-14 h-14 bg-gradient-to-br from-purple-500 to-blue-500 rounded-2xl flex items-center justify-center text-3xl mb-4">
                            📊
                        </div>
                        <h3 class="text-xl font-bold mb-3 dark:text-white">Seguimiento de Calorías</h3>
                        <p class="text-gray-600 dark:text-gray-400">Control preciso de tu ingesta diaria con contador visual y metas personalizadas.</p>
                    </div>
                    
                    <!-- Feature 2 -->
                    <div class="glass-card rounded-2xl p-6 sm:p-8 card-hover">
                        <div class="w-14 h-14 bg-gradient-to-br from-green-500 to-emerald-500 rounded-2xl flex items-center justify-center text-3xl mb-4">
                            🥗
                        </div>
                        <h3 class="text-xl font-bold mb-3 dark:text-white">350+ Recetas</h3>
                        <p class="text-gray-600 dark:text-gray-400">Recetas saludables y deliciosas con información nutricional detallada.</p>
                    </div>
                    
                    <!-- Feature 3 -->
                    <div class="glass-card rounded-2xl p-6 sm:p-8 card-hover">
                        <div class="w-14 h-14 bg-gradient-to-br from-blue-500 to-cyan-500 rounded-2xl flex items-center justify-center text-3xl mb-4">
                            📈
                        </div>
                        <h3 class="text-xl font-bold mb-3 dark:text-white">Progreso de Peso</h3>
                        <p class="text-gray-600 dark:text-gray-400">Gráficos de evolución para visualizar tu transformación semana a semana.</p>
                    </div>
                    
                    <!-- Feature 4 -->
                    <div class="glass-card rounded-2xl p-6 sm:p-8 card-hover">
                        <div class="w-14 h-14 bg-gradient-to-br from-orange-500 to-red-500 rounded-2xl flex items-center justify-center text-3xl mb-4">
                            🛒
                        </div>
                        <h3 class="text-xl font-bold mb-3 dark:text-white">Lista de Compras</h3>
                        <p class="text-gray-600 dark:text-gray-400">Lista automática agrupada por supermercado para facilitar tus compras.</p>
                    </div>
                    
                    <!-- Feature 5 -->
                    <div class="glass-card rounded-2xl p-6 sm:p-8 card-hover">
                        <div class="w-14 h-14 bg-gradient-to-br from-pink-500 to-rose-500 rounded-2xl flex items-center justify-center text-3xl mb-4">
                            🎯
                        </div>
                        <h3 class="text-xl font-bold mb-3 dark:text-white">Metas Personalizadas</h3>
                        <p class="text-gray-600 dark:text-gray-400">Planes adaptados a tus objetivos: perder peso, ganar músculo o mantener.</p>
                    </div>
                    
                    <!-- Feature 6 -->
                    <div class="glass-card rounded-2xl p-6 sm:p-8 card-hover">
                        <div class="w-14 h-14 bg-gradient-to-br from-indigo-500 to-purple-500 rounded-2xl flex items-center justify-center text-3xl mb-4">
                            📱
                        </div>
                        <h3 class="text-xl font-bold mb-3 dark:text-white">100% Mobile First</h3>
                        <p class="text-gray-600 dark:text-gray-400">Diseño responsive optimizado para usar desde cualquier dispositivo.</p>
                    </div>
                </div>
            </div>
        </section>

        <!-- Beneficios Section -->
        <section id="beneficios" class="py-20 px-4">
            <div class="container mx-auto max-w-6xl">
                <div class="text-center mb-16">
                    <h2 class="text-3xl sm:text-4xl md:text-5xl font-black mb-4 dark:text-white">
                        Beneficios que marcan la diferencia
                    </h2>
                    <p class="text-lg text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">
                        Más que una app de conteo de calorías, tu compañero de transformación
                    </p>
                </div>
                
                <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
                    <div class="glass-card rounded-2xl p-8 flex gap-6 items-start">
                        <div class="w-12 h-12 bg-green-100 dark:bg-green-900/30 rounded-xl flex items-center justify-center text-2xl flex-shrink-0">
                            ⚡
                        </div>
                        <div>
                            <h3 class="text-xl font-bold mb-2 dark:text-white">Resultados Rápidos</h3>
                            <p class="text-gray-600 dark:text-gray-400">Nuestros usuarios ven resultados en las primeras 2-3 semanas con consistencia.</p>
                        </div>
                    </div>
                    
                    <div class="glass-card rounded-2xl p-8 flex gap-6 items-start">
                        <div class="w-12 h-12 bg-blue-100 dark:bg-blue-900/30 rounded-xl flex items-center justify-center text-2xl flex-shrink-0">
                            🧠
                        </div>
                        <div>
                            <h3 class="text-xl font-bold mb-2 dark:text-white">Sin Estrés</h3>
                            <p class="text-gray-600 dark:text-gray-400">Olvídate de contar manualmente. Todo automatizado y fácil de seguir.</p>
                        </div>
                    </div>
                    
                    <div class="glass-card rounded-2xl p-8 flex gap-6 items-start">
                        <div class="w-12 h-12 bg-purple-100 dark:bg-purple-900/30 rounded-xl flex items-center justify-center text-2xl flex-shrink-0">
                            🎓
                        </div>
                        <div>
                            <h3 class="text-xl font-bold mb-2 dark:text-white">Aprende a Comer</h3>
                            <p class="text-gray-600 dark:text-gray-400">Entiende tus macros y desarrolla hábitos saludables para siempre.</p>
                        </div>
                    </div>
                    
                    <div class="glass-card rounded-2xl p-8 flex gap-6 items-start">
                        <div class="w-12 h-12 bg-orange-100 dark:bg-orange-900/30 rounded-xl flex items-center justify-center text-2xl flex-shrink-0">
                            💪
                        </div>
                        <div>
                            <h3 class="text-xl font-bold mb-2 dark:text-white">Comunidad Activa</h3>
                            <p class="text-gray-600 dark:text-gray-400">Únete a miles de personas que ya están transformando su vida.</p>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- Testimonios Section -->
        <section class="py-20 px-4 bg-white dark:bg-gray-900">
            <div class="container mx-auto max-w-6xl">
                <div class="text-center mb-16">
                    <h2 class="text-3xl sm:text-4xl md:text-5xl font-black mb-4 dark:text-white">
                        Historias de éxito
                    </h2>
                    <p class="text-lg text-gray-600 dark:text-gray-400">Personas reales, resultados reales</p>
                </div>
                
                <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <div class="glass-card rounded-2xl p-6">
                        <div class="flex items-center gap-3 mb-4">
                            <div class="w-12 h-12 bg-gradient-to-br from-purple-500 to-blue-500 rounded-full flex items-center justify-center text-white font-bold">
                                M
                            </div>
                            <div>
                                <p class="font-bold dark:text-white">María G.</p>
                                <p class="text-sm text-gray-500">-8kg en 2 meses</p>
                            </div>
                        </div>
                        <p class="text-gray-600 dark:text-gray-400 italic">"La mejor inversión en mi salud. Las recetas son increíbles y el seguimiento es súper fácil."</p>
                        <div class="flex gap-1 mt-4 text-yellow-500">
                            <i class="fas fa-star"></i>
                            <i class="fas fa-star"></i>
                            <i class="fas fa-star"></i>
                            <i class="fas fa-star"></i>
                            <i class="fas fa-star"></i>
                        </div>
                    </div>
                    
                    <div class="glass-card rounded-2xl p-6">
                        <div class="flex items-center gap-3 mb-4">
                            <div class="w-12 h-12 bg-gradient-to-br from-green-500 to-emerald-500 rounded-full flex items-center justify-center text-white font-bold">
                                C
                            </div>
                            <div>
                                <p class="font-bold dark:text-white">Carlos R.</p>
                                <p class="text-sm text-gray-500">+5kg músculo en 3 meses</p>
                            </div>
                        </div>
                        <p class="text-gray-600 dark:text-gray-400 italic">"Perfecto para ganar masa muscular. Los macros están perfectamente calculados."</p>
                        <div class="flex gap-1 mt-4 text-yellow-500">
                            <i class="fas fa-star"></i>
                            <i class="fas fa-star"></i>
                            <i class="fas fa-star"></i>
                            <i class="fas fa-star"></i>
                            <i class="fas fa-star"></i>
                        </div>
                    </div>
                    
                    <div class="glass-card rounded-2xl p-6">
                        <div class="flex items-center gap-3 mb-4">
                            <div class="w-12 h-12 bg-gradient-to-br from-orange-500 to-red-500 rounded-full flex items-center justify-center text-white font-bold">
                                L
                            </div>
                            <div>
                                <p class="font-bold dark:text-white">Laura M.</p>
                                <p class="text-sm text-gray-500">-15kg en 4 meses</p>
                            </div>
                        </div>
                        <p class="text-gray-600 dark:text-gray-400 italic">"Cambió mi vida. Ahora entiendo cómo comer y mantengo mi peso sin esfuerzo."</p>
                        <div class="flex gap-1 mt-4 text-yellow-500">
                            <i class="fas fa-star"></i>
                            <i class="fas fa-star"></i>
                            <i class="fas fa-star"></i>
                            <i class="fas fa-star"></i>
                            <i class="fas fa-star"></i>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- Pricing Section -->
        <section id="pricing" class="py-20 px-4">
            <div class="container mx-auto max-w-6xl">
                <div class="text-center mb-16">
                    <h2 class="text-3xl sm:text-4xl md:text-5xl font-black mb-4 dark:text-white">
                        Planes simples y transparentes
                    </h2>
                    <p class="text-lg text-gray-600 dark:text-gray-400">Elige el plan que mejor se adapte a ti</p>
                </div>
                
                <div class="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-5xl mx-auto">
                    <!-- Free Plan -->
                    <div class="glass-card rounded-2xl p-8 border-2 border-transparent">
                        <h3 class="text-2xl font-black mb-2 dark:text-white">Gratis</h3>
                        <p class="text-gray-600 dark:text-gray-400 mb-6">Para empezar</p>
                        <div class="mb-6">
                            <span class="text-5xl font-black dark:text-white">€0</span>
                            <span class="text-gray-500">/mes</span>
                        </div>
                        <ul class="space-y-3 mb-8">
                            <li class="flex items-center gap-3">
                                <i class="fas fa-check text-green-500"></i>
                                <span class="dark:text-gray-300">Seguimiento básico</span>
                            </li>
                            <li class="flex items-center gap-3">
                                <i class="fas fa-check text-green-500"></i>
                                <span class="dark:text-gray-300">50 recetas</span>
                            </li>
                            <li class="flex items-center gap-3">
                                <i class="fas fa-check text-green-500"></i>
                                <span class="dark:text-gray-300">1 objetivo</span>
                            </li>
                        </ul>
                        <button onclick="showModal('register')" class="w-full py-3 rounded-xl font-bold border-2 border-purple-500 text-purple-500 hover:bg-purple-50 dark:hover:bg-purple-900/20 transition-colors touch-target">
                            Comenzar gratis
                        </button>
                    </div>
                    
                    <!-- Pro Plan -->
                    <div class="glass-card rounded-2xl p-8 border-2 border-purple-500 relative transform scale-105">
                        <div class="absolute -top-4 left-1/2 -translate-x-1/2 bg-gradient-to-r from-purple-500 to-blue-500 text-white px-4 py-1 rounded-full text-sm font-bold">
                            MÁS POPULAR
                        </div>
                        <h3 class="text-2xl font-black mb-2 dark:text-white">Pro</h3>
                        <p class="text-gray-600 dark:text-gray-400 mb-6">Para resultados serios</p>
                        <div class="mb-6">
                            <span class="text-5xl font-black dark:text-white">€9</span>
                            <span class="text-gray-500">/mes</span>
                        </div>
                        <ul class="space-y-3 mb-8">
                            <li class="flex items-center gap-3">
                                <i class="fas fa-check text-green-500"></i>
                                <span class="dark:text-gray-300">Todo lo de Gratis</span>
                            </li>
                            <li class="flex items-center gap-3">
                                <i class="fas fa-check text-green-500"></i>
                                <span class="dark:text-gray-300">350+ recetas</span>
                            </li>
                            <li class="flex items-center gap-3">
                                <i class="fas fa-check text-green-500"></i>
                                <span class="dark:text-gray-300">Objetivos ilimitados</span>
                            </li>
                            <li class="flex items-center gap-3">
                                <i class="fas fa-check text-green-500"></i>
                                <span class="dark:text-gray-300">Lista de compras</span>
                            </li>
                            <li class="flex items-center gap-3">
                                <i class="fas fa-check text-green-500"></i>
                                <span class="dark:text-gray-300">Soporte prioritario</span>
                            </li>
                        </ul>
                        <button onclick="showModal('register')" class="btn-primary w-full py-3 rounded-xl font-bold text-white touch-target">
                            Comenzar Pro
                        </button>
                    </div>
                    
                    <!-- Premium Plan -->
                    <div class="glass-card rounded-2xl p-8 border-2 border-transparent">
                        <h3 class="text-2xl font-black mb-2 dark:text-white">Premium</h3>
                        <p class="text-gray-600 dark:text-gray-400 mb-6">Máximo rendimiento</p>
                        <div class="mb-6">
                            <span class="text-5xl font-black dark:text-white">€19</span>
                            <span class="text-gray-500">/mes</span>
                        </div>
                        <ul class="space-y-3 mb-8">
                            <li class="flex items-center gap-3">
                                <i class="fas fa-check text-green-500"></i>
                                <span class="dark:text-gray-300">Todo lo de Pro</span>
                            </li>
                            <li class="flex items-center gap-3">
                                <i class="fas fa-check text-green-500"></i>
                                <span class="dark:text-gray-300">Coach personalizado</span>
                            </li>
                            <li class="flex items-center gap-3">
                                <i class="fas fa-check text-green-500"></i>
                                <span class="dark:text-gray-300">Planes avanzados</span>
                            </li>
                            <li class="flex items-center gap-3">
                                <i class="fas fa-check text-green-500"></i>
                                <span class="dark:text-gray-300">Comunidad VIP</span>
                            </li>
                        </ul>
                        <button onclick="showModal('register')" class="w-full py-3 rounded-xl font-bold border-2 border-purple-500 text-purple-500 hover:bg-purple-50 dark:hover:bg-purple-900/20 transition-colors touch-target">
                            Comenzar Premium
                        </button>
                    </div>
                </div>
            </div>
        </section>

        <!-- FAQ Section -->
        <section id="faq" class="py-20 px-4 bg-white dark:bg-gray-900">
            <div class="container mx-auto max-w-4xl">
                <div class="text-center mb-16">
                    <h2 class="text-3xl sm:text-4xl md:text-5xl font-black mb-4 dark:text-white">
                        Preguntas frecuentes
                    </h2>
                    <p class="text-lg text-gray-600 dark:text-gray-400">Resolvemos tus dudas</p>
                </div>
                
                <div class="space-y-4">
                    <div class="glass-card rounded-2xl overflow-hidden">
                        <button onclick="toggleFaq(this)" class="w-full px-6 py-4 text-left flex items-center justify-between dark:text-white font-semibold">
                            <span>¿Necesito experiencia previa?</span>
                            <i class="fas fa-chevron-down transition-transform"></i>
                        </button>
                        <div class="hidden px-6 pb-4 text-gray-600 dark:text-gray-400">
                            <p>¡Para nada! La app está diseñada para principiantes y expertos. El onboarding te guiará paso a paso.</p>
                        </div>
                    </div>
                    
                    <div class="glass-card rounded-2xl overflow-hidden">
                        <button onclick="toggleFaq(this)" class="w-full px-6 py-4 text-left flex items-center justify-between dark:text-white font-semibold">
                            <span>¿Puedo cancelar cuando quiera?</span>
                            <i class="fas fa-chevron-down transition-transform"></i>
                        </button>
                        <div class="hidden px-6 pb-4 text-gray-600 dark:text-gray-400">
                            <p>Sí, puedes cancelar tu suscripción en cualquier momento sin preguntas ni cargos ocultos.</p>
                        </div>
                    </div>
                    
                    <div class="glass-card rounded-2xl overflow-hidden">
                        <button onclick="toggleFaq(this)" class="w-full px-6 py-4 text-left flex items-center justify-between dark:text-white font-semibold">
                            <span>¿Las recetas son aptas para vegetarianos?</span>
                            <i class="fas fa-chevron-down transition-transform"></i>
                        </button>
                        <div class="hidden px-6 pb-4 text-gray-600 dark:text-gray-400">
                            <p>Sí, tenemos más de 100 recetas vegetarianas y veganas. Puedes filtrar por preferencias dietéticas.</p>
                        </div>
                    </div>
                    
                    <div class="glass-card rounded-2xl overflow-hidden">
                        <button onclick="toggleFaq(this)" class="w-full px-6 py-4 text-left flex items-center justify-between dark:text-white font-semibold">
                            <span>¿Funciona en móviles?</span>
                            <i class="fas fa-chevron-down transition-transform"></i>
                        </button>
                        <div class="hidden px-6 pb-4 text-gray-600 dark:text-gray-400">
                            <p>¡Sí! La app es 100% responsive y funciona perfectamente en cualquier dispositivo móvil, tablet o escritorio.</p>
                        </div>
                    </div>
                    
                    <div class="glass-card rounded-2xl overflow-hidden">
                        <button onclick="toggleFaq(this)" class="w-full px-6 py-4 text-left flex items-center justify-between dark:text-white font-semibold">
                            <span>¿Hay garantía de devolución?</span>
                            <i class="fas fa-chevron-down transition-transform"></i>
                        </button>
                        <div class="hidden px-6 pb-4 text-gray-600 dark:text-gray-400">
                            <p>Ofrecemos 14 días de garantía de devolución si no estás satisfecho con los resultados.</p>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- Footer -->
        <footer class="py-12 px-4 border-t border-gray-200 dark:border-gray-800">
            <div class="container mx-auto max-w-6xl">
                <div class="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
                    <div>
                        <div class="flex items-center gap-3 mb-4">
                            <div class="w-10 h-10 bg-gradient-to-br from-purple-500 to-blue-500 rounded-xl flex items-center justify-center text-2xl">🥗</div>
                            <span class="text-xl font-black gradient-text">Diet Tracker FIT</span>
                        </div>
                        <p class="text-gray-600 dark:text-gray-400 text-sm">
                            Tu compañero de transformación nutricional.
                        </p>
                    </div>
                    
                    <div>
                        <h4 class="font-bold mb-4 dark:text-white">Producto</h4>
                        <ul class="space-y-2 text-sm text-gray-600 dark:text-gray-400">
                            <li><a href="#features" class="hover:text-purple-500">Características</a></li>
                            <li><a href="#pricing" class="hover:text-purple-500">Precios</a></li>
                            <li><a href="#" class="hover:text-purple-500">Recetas</a></li>
                        </ul>
                    </div>
                    
                    <div>
                        <h4 class="font-bold mb-4 dark:text-white">Compañía</h4>
                        <ul class="space-y-2 text-sm text-gray-600 dark:text-gray-400">
                            <li><a href="#" class="hover:text-purple-500">Sobre nosotros</a></li>
                            <li><a href="#" class="hover:text-purple-500">Blog</a></li>
                            <li><a href="#" class="hover:text-purple-500">Contacto</a></li>
                        </ul>
                    </div>
                    
                    <div>
                        <h4 class="font-bold mb-4 dark:text-white">Legal</h4>
                        <ul class="space-y-2 text-sm text-gray-600 dark:text-gray-400">
                            <li><a href="#" class="hover:text-purple-500">Privacidad</a></li>
                            <li><a href="#" class="hover:text-purple-500">Términos</a></li>
                            <li><a href="#" class="hover:text-purple-500">Cookies</a></li>
                        </ul>
                    </div>
                </div>
                
                <div class="pt-8 border-t border-gray-200 dark:border-gray-800 flex flex-col sm:flex-row items-center justify-between gap-4">
                    <p class="text-sm text-gray-500">© 2025 Diet Tracker FIT. Todos los derechos reservados.</p>
                    <div class="flex gap-4">
                        <a href="#" class="w-10 h-10 rounded-full glass flex items-center justify-center text-gray-600 dark:text-gray-400 hover:text-purple-500 transition-colors">
                            <i class="fab fa-instagram"></i>
                        </a>
                        <a href="#" class="w-10 h-10 rounded-full glass flex items-center justify-center text-gray-600 dark:text-gray-400 hover:text-purple-500 transition-colors">
                            <i class="fab fa-twitter"></i>
                        </a>
                        <a href="#" class="w-10 h-10 rounded-full glass flex items-center justify-center text-gray-600 dark:text-gray-400 hover:text-purple-500 transition-colors">
                            <i class="fab fa-tiktok"></i>
                        </a>
                    </div>
                </div>
            </div>
        </footer>
    `;
}

// Toggle FAQ
function toggleFaq(button) {
    const content = button.nextElementSibling;
    const icon = button.querySelector('i');
    
    content.classList.toggle('hidden');
    icon.classList.toggle('rotate-180');
}

// ==================== MODALES DE AUTENTICACIÓN ====================

function showModal(type) {
    const container = document.getElementById('auth-modals');
    
    if (type === 'login') {
        container.innerHTML = `
            <div class="fixed inset-0 z-[100] bg-black/60 backdrop-blur-sm flex items-center justify-center p-4" onclick="hideModal(event)">
                <div class="glass-card bg-white dark:bg-gray-900 rounded-3xl max-w-md w-full p-8 relative slide-enter" onclick="event.stopPropagation()">
                    <button onclick="document.getElementById('auth-modals').innerHTML=''" class="absolute top-4 right-4 touch-target w-10 h-10 rounded-full bg-gray-100 dark:bg-gray-800 flex items-center justify-center">
                        <i class="fas fa-times"></i>
                    </button>
                    <div class="text-center mb-8">
                        <div class="w-16 h-16 bg-gradient-to-br from-purple-500 to-blue-500 rounded-2xl flex items-center justify-center text-3xl mx-auto mb-4">👋</div>
                        <h2 class="text-2xl font-black mb-2 dark:text-white">¡Bienvenido!</h2>
                        <p class="text-gray-600 dark:text-gray-400">Inicia sesión para continuar</p>
                    </div>
                    <form onsubmit="handleLogin(event)">
                        <div class="mb-4">
                            <label class="block text-sm font-semibold mb-2 dark:text-gray-200">Email</label>
                            <input type="email" id="login-email" required class="w-full px-4 py-3 rounded-xl border-2 border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 dark:text-white focus:border-purple-500 focus:outline-none touch-target">
                        </div>
                        <div class="mb-4">
                            <label class="block text-sm font-semibold mb-2 dark:text-gray-200">Contraseña</label>
                            <input type="password" id="login-password" required class="w-full px-4 py-3 rounded-xl border-2 border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 dark:text-white focus:border-purple-500 focus:outline-none touch-target">
                        </div>
                        <button type="submit" class="btn-primary w-full text-white py-3 rounded-xl font-bold text-lg touch-target">Entrar</button>
                    </form>
                    <p class="text-center mt-6 text-sm dark:text-gray-400">
                        ¿No tienes cuenta? <button onclick="showModal('register')" class="text-purple-500 font-bold hover:underline">Regístrate</button>
                    </p>
                    <p class="text-center mt-2 text-sm">
                        <button onclick="showModal('forgot')" class="text-purple-500 font-bold hover:underline text-sm">¿Olvidaste tu contraseña?</button>
                    </p>
                </div>
            </div>
        `;
    } else if (type === 'register') {
        container.innerHTML = `
            <div class="fixed inset-0 z-[100] bg-black/60 backdrop-blur-sm flex items-center justify-center p-4" onclick="hideModal(event)">
                <div class="glass-card bg-white dark:bg-gray-900 rounded-3xl max-w-md w-full p-8 relative slide-enter" onclick="event.stopPropagation()">
                    <button onclick="document.getElementById('auth-modals').innerHTML=''" class="absolute top-4 right-4 touch-target w-10 h-10 rounded-full bg-gray-100 dark:bg-gray-800 flex items-center justify-center">
                        <i class="fas fa-times"></i>
                    </button>
                    <div class="text-center mb-6">
                        <div class="w-16 h-16 bg-gradient-to-br from-purple-500 to-blue-500 rounded-2xl flex items-center justify-center text-3xl mx-auto mb-4">🎯</div>
                        <h2 class="text-2xl font-black mb-2 dark:text-white">Crea tu cuenta</h2>
                        <p class="text-gray-600 dark:text-gray-400 text-sm">Comienza tu transformación hoy</p>
                    </div>
                    <form onsubmit="handleRegister(event)">
                        <div class="mb-4">
                            <label class="block text-sm font-semibold mb-2 dark:text-gray-200">Usuario</label>
                            <input type="text" id="register-username" required class="w-full px-4 py-3 rounded-xl border-2 border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 dark:text-white focus:border-purple-500 focus:outline-none touch-target">
                        </div>
                        <div class="mb-4">
                            <label class="block text-sm font-semibold mb-2 dark:text-gray-200">Email</label>
                            <input type="email" id="register-email" required class="w-full px-4 py-3 rounded-xl border-2 border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 dark:text-white focus:border-purple-500 focus:outline-none touch-target">
                        </div>
                        <div class="mb-4">
                            <label class="block text-sm font-semibold mb-2 dark:text-gray-200">Contraseña</label>
                            <input type="password" id="register-password" required minlength="6" class="w-full px-4 py-3 rounded-xl border-2 border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 dark:text-white focus:border-purple-500 focus:outline-none touch-target">
                        </div>
                        <div class="mb-4">
                            <label class="block text-sm font-semibold mb-2 dark:text-gray-200">Confirmar contraseña</label>
                            <input type="password" id="register-confirm" required class="w-full px-4 py-3 rounded-xl border-2 border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 dark:text-white focus:border-purple-500 focus:outline-none touch-target">
                        </div>
                        <button type="submit" class="btn-primary w-full text-white py-3 rounded-xl font-bold text-lg touch-target">Crear cuenta</button>
                    </form>
                    <p class="text-center mt-6 text-sm dark:text-gray-400">
                        ¿Ya tienes cuenta? <button onclick="showModal('login')" class="text-purple-500 font-bold hover:underline">Entra</button>
                    </p>
                </div>
            </div>
        `;
    } else if (type === 'forgot') {
        container.innerHTML = `
            <div class="fixed inset-0 z-[100] bg-black/60 backdrop-blur-sm flex items-center justify-center p-4" onclick="hideModal(event)">
                <div class="glass-card bg-white dark:bg-gray-900 rounded-3xl max-w-md w-full p-8 relative slide-enter" onclick="event.stopPropagation()">
                    <button onclick="document.getElementById('auth-modals').innerHTML=''" class="absolute top-4 right-4 touch-target w-10 h-10 rounded-full bg-gray-100 dark:bg-gray-800 flex items-center justify-center">
                        <i class="fas fa-times"></i>
                    </button>
                    <div class="text-center mb-8">
                        <div class="w-16 h-16 bg-gradient-to-br from-blue-500 to-cyan-500 rounded-2xl flex items-center justify-center text-3xl mx-auto mb-4">🔑</div>
                        <h2 class="text-2xl font-black mb-2 dark:text-white">Recuperar contraseña</h2>
                        <p class="text-gray-600 dark:text-gray-400">Te enviaremos un email</p>
                    </div>
                    <form onsubmit="handleForgotPassword(event)">
                        <div class="mb-4">
                            <label class="block text-sm font-semibold mb-2 dark:text-gray-200">Email</label>
                            <input type="email" id="forgot-email" required class="w-full px-4 py-3 rounded-xl border-2 border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 dark:text-white focus:border-purple-500 focus:outline-none touch-target">
                        </div>
                        <button type="submit" class="btn-primary w-full text-white py-3 rounded-xl font-bold text-lg touch-target">Enviar email</button>
                    </form>
                    <p class="text-center mt-6 text-sm">
                        <button onclick="showModal('login')" class="text-purple-500 font-bold hover:underline">← Volver</button>
                    </p>
                </div>
            </div>
        `;
    }
    
    document.body.style.overflow = 'hidden';
}

function hideModal(event) {
    if (event && event.target !== event.currentTarget) return;
    document.getElementById('auth-modals').innerHTML = '';
    document.body.style.overflow = '';
}

// ==================== MANEJO DE AUTENTICACIÓN ====================

async function handleLogin(e) {
    e.preventDefault();
    const email = document.getElementById('login-email').value.trim().toLowerCase();
    const password = document.getElementById('login-password').value;
    
    if (!email || !password) {
        showToast('❌ Email y contraseña requeridos', 'error');
        return;
    }
    
    showToast('Iniciando sesión...', 'info');
    
    try {
        const res = await fetch(API_BASE + '/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email: email, password: password })
        });
        
        const data = await res.json();
        
        if (res.ok && data.user && data.token) {
            // Guardar usuario completo con token
            user = {
                ...data.user,
                token: data.token
            };
            localStorage.setItem('user', JSON.stringify(user));
            localStorage.setItem('token', data.token);
            
            document.getElementById('auth-modals').innerHTML = '';
            document.body.style.overflow = '';
            showToast('✅ ¡Bienvenido, ' + (user.name || user.email) + '!', 'success');
            
            // Redirigir al dashboard
            checkAuth();
        } else {
            showToast('❌ ' + (data.error || 'Email o contraseña incorrectos'), 'error');
        }
    } catch (err) {
        showToast('❌ Error de conexión. Verifica tu internet.', 'error');
        console.error('Login error:', err);
    }
}

async function handleRegister(e) {
    e.preventDefault();
    const username = document.getElementById('register-username').value;
    const email = document.getElementById('register-email').value;
    const password = document.getElementById('register-password').value;
    const confirm = document.getElementById('register-confirm').value;
    
    if (password !== confirm) {
        showToast('❌ Las contraseñas no coinciden', 'error');
        return;
    }
    
    if (password.length < 6) {
        showToast('❌ La contraseña debe tener al menos 6 caracteres', 'error');
        return;
    }
    
    showToast('Creando cuenta...', 'info');
    
    try {
        const res = await fetch(API_BASE + '/register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name: username, email: email, password: password })
        });
        
        const data = await res.json();
        
        if (res.ok && data.user && data.token) {
            // Guardar usuario completo con token (igual que en login)
            user = {
                ...data.user,
                token: data.token
            };
            localStorage.setItem('user', JSON.stringify(user));
            localStorage.setItem('token', data.token);
            
            document.getElementById('auth-modals').innerHTML = '';
            document.body.style.overflow = '';
            showToast('✅ ¡Cuenta creada! Redirigiendo...', 'success');
            setTimeout(() => {
                checkAuth();
            }, 1500);
        } else {
            showToast(data.error || 'Error al registrar', 'error');
        }
    } catch (err) {
        showToast('Error de conexión', 'error');
        console.error(err);
    }
}

async function handleForgotPassword(e) {
    e.preventDefault();
    const email = document.getElementById('forgot-email').value.trim();
    
    if (!email) {
        showToast('❌ Ingresa tu email', 'error');
        return;
    }
    
    showToast('📧 Procesando solicitud...', 'info');
    
    try {
        const res = await fetch(API_BASE + '/recover-password', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email: email })
        });
        
        const data = await res.json();
        
        if (res.ok) {
            showToast('✅ Si tu email está registrado, recibirás instrucciones', 'success');
            document.getElementById('auth-modals').innerHTML = '';
            document.body.style.overflow = '';
            // Mostrar modal de login
            setTimeout(() => showModal('login'), 1500);
        } else {
            showToast(data.error || 'Error al procesar solicitud', 'error');
        }
    } catch (err) {
        showToast('Error de conexión', 'error');
        console.error(err);
    }
}

function checkAuth() {
    const saved = localStorage.getItem('user');
    
    if (saved) {
        user = JSON.parse(saved);
        
        // Update nav user info
        document.getElementById('user-name').textContent = user.name || user.email;
        document.getElementById('user-avatar').textContent = (user.name || 'U')[0].toUpperCase();
        
        showToast('✅ Sesión iniciada', 'success');
        
        // Use router to show dashboard
        showPage('dashboard');
        
        // Load dashboard
        loadDashboard();
    } else {
        // Use router to show landing
        showPage('landing');
    }
}

function logout() {
    localStorage.removeItem('user');
    user = null;
    checkAuth();
    showToast('Sesión cerrada', 'info');
}

// ==================== DASHBOARD ====================

async function loadDashboard() {
    if (!user) return;
    
    const dashboard = document.getElementById('dashboard-content');
    
    // Loading state con spinner animado
    dashboard.innerHTML = `
        <div class="flex items-center justify-center min-h-[60vh]">
            <div class="text-center">
                <div class="w-16 h-16 border-4 border-purple-500 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
                <p class="font-bold dark:text-white text-lg">Cargando tu dashboard...</p>
                <p class="text-sm text-gray-500 dark:text-gray-400 mt-2">Obteniendo tus datos</p>
            </div>
        </div>
    `;
    
    try {
        const userId = user.id;
        const token = user.token;
        
        if (!userId || !token) {
            throw new Error('Usuario no autenticado correctamente');
        }
        
        const headers = { 
            'Authorization': 'Bearer ' + token,
            'Content-Type': 'application/json'
        };
        
        // Load dashboard data from main endpoint
        const dashboardRes = await fetch(API_BASE + '/dashboard', { headers });
        
        let dashboardData = null;
        let weightHistory = [];
        let todayLogs = [];
        
        if (dashboardRes.ok) {
            dashboardData = await dashboardRes.json();
        } else {
            console.warn('Dashboard endpoint failed, trying fallback endpoints...');
        }
        
        // Load weight history separately
        try {
            const weightRes = await fetch(API_BASE + '/stats', { headers });
            if (weightRes.ok) {
                const stats = await weightRes.json();
                weightHistory = stats.weight_history || [];
            }
        } catch (weightErr) {
            console.warn('Could not load weight history:', weightErr);
        }
        
        // Load weekly plan
        await loadWeeklyPlan();
        
        // Load today's food logs
        try {
            const foodLogRes = await fetch(API_BASE + '/food-log/today', { headers });
            if (foodLogRes.ok) {
                const foodData = await foodLogRes.json();
                todayLogs = foodData.logs || [];
            }
        } catch (foodErr) {
            console.warn('Could not load food logs:', foodErr);
        }
        
        // Use dashboard data or fallback to plan endpoint
        if (!dashboardData) {
            try {
                const planRes = await fetch(API_BASE + '/plan', { headers });
                if (planRes.ok) {
                    const plan = await planRes.json();
                    dashboardData = {
                        profile: {},
                        metrics: {
                            target_calories: 2000,
                            current_weight: 70,
                            goal_weight: 65
                        },
                        today: {
                            calories: 0,
                            protein: 0,
                            carbs: 0,
                            fat: 0
                        },
                        plan: plan
                    };
                }
            } catch (planErr) {
                console.warn('Plan endpoint also failed, using defaults');
            }
        }
        
        // Merge today's logs into dashboard data
        if (dashboardData && todayLogs.length > 0) {
            const totals = todayLogs.reduce((acc, log) => ({
                calories: acc.calories + (log.calories || 0),
                protein: acc.protein + (log.protein || 0),
                carbs: acc.carbs + (log.carbs || 0),
                fat: acc.fat + (log.fat || 0)
            }), { calories: 0, protein: 0, carbs: 0, fat: 0 });
            
            dashboardData.today = {
                ...dashboardData.today,
                ...totals,
                logs: todayLogs
            };
        }
        
        // Render with data or defaults
        renderDashboard(dashboardData, weightHistory);
        
    } catch (err) {
        console.error('Error loading dashboard:', err);
        showToast('Error cargando datos. Usando datos de ejemplo.', 'error');
        renderDashboardWithFallback();
    }
}

function renderDashboard(data, history) {
    const dashboard = document.getElementById('dashboard-content');
    
    // Extraer datos con fallbacks seguros
    const metrics = data?.metrics || {};
    const today = data?.today || {};
    const profile = data?.profile || {};
    const todayLogs = today?.logs || [];
    
    const dailyCalories = metrics.target_calories || 2000;
    const currentWeight = metrics.current_weight || 70;
    const goalWeight = metrics.goal_weight || 65;
    const todayCalories = today.calories || 0;
    const todayProtein = today.protein || 0;
    const todayCarbs = today.carbs || 0;
    const todayFat = today.fat || 0;
    
    // Calcular porcentajes para las barras de progreso
    const proteinGoal = 150;
    const carbsGoal = 200;
    const fatGoal = 65;
    
    const proteinPercent = Math.min(100, (todayProtein / proteinGoal) * 100);
    const carbsPercent = Math.min(100, (todayCarbs / carbsGoal) * 100);
    const fatPercent = Math.min(100, (todayFat / fatGoal) * 100);
    const caloriesPercent = Math.min(100, (todayCalories / dailyCalories) * 100);
    
    // Calcular dashoffset para el círculo de calorías (283 es la circunferencia)
    const circumference = 283;
    const dashOffset = circumference - (caloriesPercent / 100) * circumference;
    
    // Calorías restantes
    const remainingCalories = Math.max(0, dailyCalories - todayCalories);
    
    // Iconos para tipos de comida
    const mealIcons = {
        'desayuno': '🌅',
        'comida': '☀️',
        'almuerzo': '🥪',
        'merienda': '🍎',
        'cena': '🌙',
        'snack': '🥨',
        'other': '🍽️'
    };
    
    dashboard.innerHTML = `
        <!-- Welcome Header -->
        <div class="mb-8">
            <h1 class="text-2xl sm:text-3xl font-black dark:text-white mb-2">¡Hola, ${user.name || user.email}! 👋</h1>
            <p class="text-gray-600 dark:text-gray-400">Aquí está tu resumen de hoy</p>
        </div>
        
        <!-- Main Stats Grid -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6 mb-8">
            <!-- Calories Card -->
            <div class="glass-card rounded-2xl p-6">
                <div class="flex items-center justify-between mb-4">
                    <h3 class="font-bold dark:text-white">Calorías</h3>
                    <span class="text-2xl">🔥</span>
                </div>
                <div class="relative w-32 h-32 mx-auto mb-4">
                    <svg class="w-32 h-32 progress-circle" viewBox="0 0 100 100">
                        <circle cx="50" cy="50" r="45" fill="none" stroke="#e2e8f0" stroke-width="10" class="dark:stroke-gray-700"/>
                        <circle cx="50" cy="50" r="45" fill="none" stroke="url(#gradient)" stroke-width="10" stroke-linecap="round" stroke-dasharray="283" stroke-dashoffset="${dashOffset}"/>
                        <defs>
                            <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="0%">
                                <stop offset="0%" stop-color="#a855f7"/>
                                <stop offset="100%" stop-color="#3b82f6"/>
                            </linearGradient>
                        </defs>
                    </svg>
                    <div class="absolute inset-0 flex items-center justify-center flex-col">
                        <span class="text-2xl font-black dark:text-white">${formatCalories(todayCalories)}</span>
                        <span class="text-xs text-gray-500">/ ${formatCalories(dailyCalories)}</span>
                    </div>
                </div>
                <p class="text-center text-sm text-gray-500 dark:text-gray-400">Quedan <span class="font-bold gradient-text">${formatCalories(remainingCalories)}</span> kcal</p>
            </div>
            
            <!-- Macros Card -->
            <div class="glass-card rounded-2xl p-6">
                <div class="flex items-center justify-between mb-4">
                    <h3 class="font-bold dark:text-white">Macros</h3>
                    <span class="text-2xl">🥑</span>
                </div>
                <div class="space-y-4">
                    <div>
                        <div class="flex justify-between text-sm mb-1">
                            <span class="dark:text-gray-300">Proteínas</span>
                            <span class="font-bold dark:text-white">${formatGrams(todayProtein)}g / ${proteinGoal}g</span>
                        </div>
                        <div class="h-3 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
                            <div class="h-full bg-gradient-to-r from-red-500 to-red-600 rounded-full" style="width: ${proteinPercent}%"></div>
                        </div>
                    </div>
                    <div>
                        <div class="flex justify-between text-sm mb-1">
                            <span class="dark:text-gray-300">Carbos</span>
                            <span class="font-bold dark:text-white">${formatGrams(todayCarbs)}g / ${carbsGoal}g</span>
                        </div>
                        <div class="h-3 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
                            <div class="h-full bg-gradient-to-r from-yellow-500 to-orange-500 rounded-full" style="width: ${carbsPercent}%"></div>
                        </div>
                    </div>
                    <div>
                        <div class="flex justify-between text-sm mb-1">
                            <span class="dark:text-gray-300">Grasas</span>
                            <span class="font-bold dark:text-white">${formatGrams(todayFat)}g / ${fatGoal}g</span>
                        </div>
                        <div class="h-3 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
                            <div class="h-full bg-gradient-to-r from-green-500 to-emerald-500 rounded-full" style="width: ${fatPercent}%"></div>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Weight Card -->
            <div class="glass-card rounded-2xl p-6">
                <div class="flex items-center justify-between mb-4">
                    <h3 class="font-bold dark:text-white">Peso</h3>
                    <span class="text-2xl">⚖️</span>
                </div>
                <div class="text-center mb-4">
                    <p class="text-4xl font-black dark:text-white mb-1">${currentWeight}</p>
                    <p class="text-sm text-gray-500">kg actuales</p>
                    <p class="text-xs text-gray-400 mt-1">Meta: ${goalWeight} kg</p>
                </div>
                <div class="h-32">
                    <canvas id="weight-chart"></canvas>
                </div>
            </div>
            
            <!-- Actions Card -->
            <div class="glass-card rounded-2xl p-6">
                <div class="flex items-center justify-between mb-4">
                    <h3 class="font-bold dark:text-white">Acciones</h3>
                    <span class="text-2xl">⚡</span>
                </div>
                <div class="space-y-3">
                    <button onclick="openFoodModal()" class="w-full btn-primary text-white py-3 rounded-xl font-bold touch-target">
                        <i class="fas fa-utensils mr-2"></i> Registrar comida
                    </button>
                    <button onclick="openWeightModal()" class="w-full glass py-3 rounded-xl font-bold dark:text-white hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors touch-target">
                        <i class="fas fa-weight mr-2"></i> Registrar peso
                    </button>
                    <button onclick="showShoppingList()" class="w-full glass py-3 rounded-xl font-bold dark:text-white hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors touch-target">
                        <i class="fas fa-shopping-cart mr-2"></i> Lista de compras
                    </button>
                    <button onclick="showProfile()" class="w-full glass py-3 rounded-xl font-bold dark:text-white hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors touch-target">
                        <i class="fas fa-user mr-2"></i> Mi perfil
                    </button>
                    <button onclick="showSettings()" class="w-full glass py-3 rounded-xl font-bold dark:text-white hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors touch-target">
                        <i class="fas fa-cog mr-2"></i> Configuración
                    </button>
                </div>
            </div>
        </div>
        
        <!-- Today's Food Log Section -->
        <div class="glass-card rounded-2xl p-4 sm:p-6 mb-8">
            <div class="flex items-center justify-between mb-4">
                <h2 class="text-xl font-black dark:text-white">🍽️ Comidas de hoy</h2>
                <button onclick="openFoodModal()" class="btn-primary text-white px-4 py-2 rounded-xl font-bold text-sm touch-target">
                    <i class="fas fa-plus mr-2"></i> Añadir
                </button>
            </div>
            
            ${todayLogs.length > 0 ? `
                <!-- Food log entries -->
                <div class="space-y-3 mb-4">
                    ${todayLogs.map(log => `
                        <div class="glass rounded-xl p-3 flex items-center justify-between">
                            <div class="flex items-center gap-3">
                                <span class="text-xl">${mealIcons[log.meal_type] || '🍽️'}</span>
                                <div>
                                    <p class="font-medium dark:text-white text-sm">${log.food_name || log.recipe_name || 'Comida'}</p>
                                    <p class="text-xs text-gray-500">${formatCalories(log.calories)} kcal • P: ${formatGrams(log.protein)}g • C: ${formatGrams(log.carbs)}g • G: ${formatGrams(log.fat)}g</p>
                                </div>
                            </div>
                            <span class="text-xs text-gray-400 capitalize">${log.meal_type}</span>
                        </div>
                    `).join('')}
                </div>
                
                <!-- Totals -->
                <div class="glass rounded-xl p-4">
                    <div class="flex justify-between items-center">
                        <span class="font-bold dark:text-white">Total</span>
                        <span class="text-xl font-black gradient-text">${formatCalories(todayCalories)} kcal</span>
                    </div>
                    <div class="flex gap-6 mt-2 text-sm text-gray-500">
                        <span>Proteína: ${formatGrams(todayProtein)}g</span>
                        <span>Carbos: ${formatGrams(todayCarbs)}g</span>
                        <span>Grasas: ${formatGrams(todayFat)}g</span>
                    </div>
                </div>
            ` : `
                <div class="text-center py-8">
                    <div class="text-4xl mb-2">🍽️</div>
                    <p class="text-gray-500 mb-4">Aún no has registrado comidas hoy</p>
                    <button onclick="openFoodModal()" class="btn-primary text-white px-6 py-3 rounded-xl font-bold touch-target">
                        <i class="fas fa-utensils mr-2"></i> Registrar primera comida
                    </button>
                </div>
            `}
        </div>
        
        <!-- Weekly Plan Section -->
        <div class="glass-card rounded-2xl p-4 sm:p-6 mb-8">
            <div class="flex items-center justify-between mb-4">
                <h2 class="text-xl font-black dark:text-white">📅 Plan Semanal</h2>
            </div>
            
            <!-- Weekly Plan Grid -->
            <div id="plan-container" class="mb-4">
                <div class="text-center py-8">
                    <div class="w-16 h-16 border-4 border-purple-500 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
                    <p class="text-gray-500">Cargando plan...</p>
                </div>
            </div>
            
            <!-- Daily Summary -->
            <div id="daily-summary"></div>
        </div>
    `;
    
    // Initialize weight chart
    initWeightChart(history);
    
    // Render weekly plan
    renderWeeklyPlan();
    
    // Render daily summary for today
    const todayIndex = new Date().getDay();
    renderDailySummary(todayIndex === 0 ? 6 : todayIndex - 1);
}

function renderDaySelector() {
    const days = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo'];
    return days.map((day, index) => `
        <button onclick="selectDay(${index + 1})" 
                class="px-4 py-2 rounded-xl font-bold whitespace-nowrap touch-target transition-all ${currentDay === index + 1 ? 'btn-primary text-white' : 'glass dark:text-white hover:bg-gray-100 dark:hover:bg-gray-800'}">
            ${day}
        </button>
    `).join('');
}

function renderMealsPlaceholder() {
    return `
        <div class="text-center py-12">
            <div class="text-6xl mb-4">🍽️</div>
            <p class="text-gray-600 dark:text-gray-400 mb-4">Tu plan para el día ${currentDay}</p>
            <button onclick="openFoodModal()" class="btn-primary text-white px-6 py-3 rounded-xl font-bold touch-target">
                + Añadir comida
            </button>
        </div>
    `;
}

function initWeightChart(history) {
    const ctx = document.getElementById('weight-chart');
    if (!ctx) return;
    
    const isDarkMode = document.documentElement.classList.contains('dark');
    
    weightChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: history.length > 0 ? history.map(h => new Date(h.date).toLocaleDateString('es-ES', { day: 'numeric', month: 'short' })) : ['Sem 1', 'Sem 2', 'Sem 3', 'Sem 4'],
            datasets: [{
                label: 'Peso (kg)',
                data: history.length > 0 ? history.map(h => h.weight) : [70, 69.5, 69, 68.5],
                borderColor: '#a855f7',
                backgroundColor: 'rgba(168, 85, 247, 0.1)',
                tension: 0.4,
                fill: true,
                pointBackgroundColor: '#a855f7',
                pointBorderColor: '#fff',
                pointBorderWidth: 2,
                pointRadius: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: {
                    backgroundColor: isDarkMode ? '#1e293b' : '#fff',
                    titleColor: isDarkMode ? '#f1f5f9' : '#0f172a',
                    bodyColor: isDarkMode ? '#cbd5e1' : '#475569',
                    borderColor: isDarkMode ? '#475569' : '#e2e8f0',
                    borderWidth: 1
                }
            },
            scales: {
                y: {
                    beginAtZero: false,
                    grid: { color: isDarkMode ? '#334155' : '#e2e8f0' },
                    ticks: { color: isDarkMode ? '#94a3b8' : '#64748b' }
                },
                x: {
                    grid: { display: false },
                    ticks: { color: isDarkMode ? '#94a3b8' : '#64748b' }
                }
            }
        }
    });
}

function changeDay(delta) {
    currentDay += delta;
    if (currentDay < 1) currentDay = 7;
    if (currentDay > 7) currentDay = 1;
    
    const selector = document.getElementById('day-selector');
    if (selector) {
        selector.innerHTML = renderDaySelector();
    }
}

function selectDay(day) {
    currentDay = day;
    const selector = document.getElementById('day-selector');
    if (selector) {
        selector.innerHTML = renderDaySelector();
    }
}

function renderDashboardError() {
    const dashboard = document.getElementById('dashboard-content');
    dashboard.innerHTML = `
        <div class="text-center py-20">
            <div class="text-6xl mb-4">😕</div>
            <h2 class="text-2xl font-bold dark:text-white mb-4">Error al cargar datos</h2>
            <p class="text-gray-600 dark:text-gray-400 mb-6">No pudimos cargar tu plan. Por favor, intenta de nuevo.</p>
            <button onclick="loadDashboard()" class="btn-primary text-white px-6 py-3 rounded-xl font-bold touch-target">
                Reintentar
            </button>
        </div>
    `;
}

// Función de fallback con datos de ejemplo cuando la API falla
function renderDashboardWithFallback() {
    const fallbackData = {
        profile: {
            goal_type: 'lose',
            activity_level: 'moderate'
        },
        metrics: {
            tmb: 1500,
            tdee: 2000,
            target_calories: 1800,
            current_weight: 75,
            goal_weight: 68,
            weight_change: -2
        },
        today: {
            calories: 450,
            protein: 35,
            carbs: 55,
            fat: 18,
            calories_remaining: 1350
        },
        plan: {
            week_number: 10,
            entries_count: 7
        }
    };
    
    // Datos de ejemplo para el gráfico
    const fallbackHistory = [
        { weight: 77, date: new Date(Date.now() - 21 * 24 * 60 * 60 * 1000) },
        { weight: 76.2, date: new Date(Date.now() - 14 * 24 * 60 * 60 * 1000) },
        { weight: 75.5, date: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000) },
        { weight: 75, date: new Date() }
    ];
    
    showToast('Mostrando datos de ejemplo (API no disponible)', 'info');
    renderDashboard(fallbackData, fallbackHistory);
}

// ==================== WEEKLY PLAN FUNCTIONS ====================

async function loadWeeklyPlan() {
    try {
        const response = await fetch(API_BASE + '/plan', {
            headers: { 'Authorization': 'Bearer ' + user.token }
        });
        const data = await response.json();
        if (response.ok) {
            currentPlan = data;
            return data;
        }
    } catch (error) {
        console.error('Error loading plan:', error);
    }
    return null;
}

function renderWeeklyPlan() {
    const container = document.getElementById('plan-container');
    if (!container) return;
    
    if (!currentPlan || !currentPlan.days) {
        container.innerHTML = `
            <div class="text-center py-8">
                <div class="text-5xl mb-4">🍽️</div>
                <p class="text-gray-500 dark:text-gray-400 mb-4">No hay plan generado aún</p>
                <button onclick="startOnboarding()" class="btn-primary text-white px-6 py-3 rounded-xl font-bold">
                    Crear mi plan
                </button>
            </div>
        `;
        return;
    }
    
    const days = ['lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado', 'domingo'];
    const daysDisplay = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo'];
    const mealTypes = {
        'desayuno': { name: 'Desayuno', icon: '🌅', time: '7:00 - 9:00' },
        'comida': { name: 'Comida', icon: '☀️', time: '12:00 - 14:00' },
        'merienda': { name: 'Merienda', icon: '🍎', time: '16:00 - 18:00' },
        'cena': { name: 'Cena', icon: '🌙', time: '19:00 - 21:00' }
    };
    
    let html = `
        <div class="mb-4 flex items-center justify-between">
            <h3 class="text-lg font-bold dark:text-white">Tu plan nutricional</h3>
            <button onclick="regeneratePlan()" class="text-sm text-purple-500 hover:text-purple-600 font-semibold flex items-center gap-1">
                <i class="fas fa-sync-alt"></i> Regenerar plan
            </button>
        </div>
        <div class="grid grid-cols-7 gap-1 sm:gap-2 overflow-x-auto">
    `;
    
    days.forEach((day, idx) => {
        const dayMeals = currentPlan.days[day] || [];
        const dayCalories = dayMeals.reduce((sum, m) => sum + (m.calories || 0), 0);
        const dayProtein = dayMeals.reduce((sum, m) => sum + (m.protein || 0), 0);
        const dayCarbs = dayMeals.reduce((sum, m) => sum + (m.carbs || 0), 0);
        const dayFat = dayMeals.reduce((sum, m) => sum + (m.fat || 0), 0);
        
        const isToday = new Date().getDay() === (idx === 6 ? 0 : idx + 1);
        
        html += `
            <div class="glass rounded-xl p-2 sm:p-3 min-w-[100px] sm:min-w-0 ${isToday ? 'ring-2 ring-purple-500' : ''}">
                <div class="text-center mb-2">
                    <h4 class="font-bold text-sm sm:text-base dark:text-white">${daysDisplay[idx]}</h4>
                    ${isToday ? '<span class="text-xs text-purple-500 font-semibold">Hoy</span>' : ''}
                    <p class="text-xs text-gray-500">${formatCalories(dayCalories)} kcal</p>
                </div>
                <div class="space-y-1">
        `;
        
        Object.entries(mealTypes).forEach(([mealType, mealInfo]) => {
            const meal = dayMeals.find(m => (m.meal_type || m.type || '').toLowerCase() === mealType);
            const mealName = meal ? (meal.name || meal.recipe_name || 'Comida') : 'Sin asignar';
            const mealCalories = meal ? (meal.calories || 0) : 0;
            
            html += `
                <div class="text-xs p-1.5 sm:p-2 bg-white/50 dark:bg-gray-800/50 rounded hover:bg-white/80 dark:hover:bg-gray-700/50 transition-colors cursor-pointer group relative"
                     onclick="showMealDetails('${day}', '${mealType}')">
                    <p class="font-medium text-xs">${mealInfo.icon} ${mealInfo.name}</p>
                    <p class="text-gray-500 text-xs truncate">${mealCalories > 0 ? formatCalories(mealCalories) + ' kcal' : '--'}</p>
                    ${meal ? `
                        <button onclick="event.stopPropagation(); openChangeRecipeModal('${day}', '${mealType}')"
                                class="absolute -top-1 -right-1 w-5 h-5 bg-purple-500 text-white rounded-full text-xs opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center"
                                title="Cambiar receta">
                            <i class="fas fa-sync-alt text-xs"></i>
                        </button>
                    ` : ''}
                </div>
            `;
        });
        
        html += `
                </div>
                <div class="mt-2 pt-2 border-t border-gray-200 dark:border-gray-700">
                    <div class="flex justify-between text-xs text-gray-500">
                        <span>P:${formatGrams(dayProtein)}g</span>
                        <span>C:${formatGrams(dayCarbs)}g</span>
                        <span>G:${formatGrams(dayFat)}g</span>
                    </div>
                </div>
            </div>
        `;
    });
    
    html += '</div>';
    container.innerHTML = html;
}

function renderDailySummary(dayIndex) {
    const container = document.getElementById('daily-summary');
    if (!container || !currentPlan || !currentPlan.days) return;
    
    const days = ['lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado', 'domingo'];
    const day = days[dayIndex];
    const dayMeals = currentPlan.days[day] || [];
    
    const totalCalories = dayMeals.reduce((sum, m) => sum + (m.calories || 0), 0);
    const totalProtein = dayMeals.reduce((sum, m) => sum + (m.protein || 0), 0);
    const totalCarbs = dayMeals.reduce((sum, m) => sum + (m.carbs || 0), 0);
    const totalFat = dayMeals.reduce((sum, m) => sum + (m.fat || 0), 0);
    
    const targetCalories = currentPlan.target_calories || 2000;
    const targetProtein = currentPlan.target_protein || 150;
    const targetCarbs = currentPlan.target_carbs || 200;
    const targetFat = currentPlan.target_fat || 65;
    
    const caloriesPercent = Math.min(100, (totalCalories / targetCalories) * 100);
    const proteinPercent = Math.min(100, (totalProtein / targetProtein) * 100);
    const carbsPercent = Math.min(100, (totalCarbs / targetCarbs) * 100);
    const fatPercent = Math.min(100, (totalFat / targetFat) * 100);
    
    container.innerHTML = `
        <div class="glass-card rounded-2xl p-6">
            <h3 class="text-xl font-bold dark:text-white mb-4">📊 Resumen del Día</h3>
            
            <!-- Calorías -->
            <div class="mb-6">
                <div class="flex justify-between items-center mb-2">
                    <span class="font-semibold dark:text-white">Calorías</span>
                    <span class="text-sm text-gray-500">${formatCalories(totalCalories)} / ${formatCalories(targetCalories)} kcal</span>
                </div>
                <div class="h-4 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
                    <div class="h-full bg-gradient-to-r from-purple-500 to-blue-500 rounded-full transition-all duration-500" 
                         style="width: ${caloriesPercent}%"></div>
                </div>
                <p class="text-xs text-gray-500 mt-1">${targetCalories - totalCalories > 0 ? formatCalories(targetCalories - totalCalories) + ' kcal restantes' : 'Objetivo alcanzado!'}</p>
            </div>
            
            <!-- Macros -->
            <div class="grid grid-cols-3 gap-4">
                <div>
                    <div class="flex justify-between items-center mb-1">
                        <span class="text-sm font-medium dark:text-white">Proteína</span>
                        <span class="text-xs text-gray-500">${formatGrams(totalProtein)}/${targetProtein}g</span>
                    </div>
                    <div class="h-2 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
                        <div class="h-full bg-red-500 rounded-full" style="width: ${proteinPercent}%"></div>
                    </div>
                </div>
                <div>
                    <div class="flex justify-between items-center mb-1">
                        <span class="text-sm font-medium dark:text-white">Carbos</span>
                        <span class="text-xs text-gray-500">${formatGrams(totalCarbs)}/${targetCarbs}g</span>
                    </div>
                    <div class="h-2 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
                        <div class="h-full bg-yellow-500 rounded-full" style="width: ${carbsPercent}%"></div>
                    </div>
                </div>
                <div>
                    <div class="flex justify-between items-center mb-1">
                        <span class="text-sm font-medium dark:text-white">Grasas</span>
                        <span class="text-xs text-gray-500">${formatGrams(totalFat)}/${targetFat}g</span>
                    </div>
                    <div class="h-2 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
                        <div class="h-full bg-green-500 rounded-full" style="width: ${fatPercent}%"></div>
                    </div>
                </div>
            </div>
        </div>
    `;
}

function showMealDetails(day, mealType) {
    if (!currentPlan || !currentPlan.days) return;
    
    const dayMeals = currentPlan.days[day] || [];
    const meal = dayMeals.find(m => (m.meal_type || m.type || '').toLowerCase() === mealType);
    
    if (!meal) {
        showToast('No hay detalles disponibles para esta comida', 'info');
        return;
    }
    
    const mealNames = {
        'desayuno': 'Desayuno',
        'comida': 'Comida',
        'merienda': 'Merienda',
        'cena': 'Cena'
    };
    
    const container = document.getElementById('auth-modals');
    container.innerHTML = `
        <div class="fixed inset-0 z-[100] bg-black/60 backdrop-blur-sm flex items-center justify-center p-4" onclick="closeMealDetails(event)">
            <div class="glass-card bg-white dark:bg-gray-900 rounded-3xl max-w-md w-full overflow-hidden" onclick="event.stopPropagation()">
                <div class="relative h-40 bg-gradient-to-br from-purple-500 to-blue-500 flex items-center justify-center">
                    <div class="text-6xl">${meal.image || '🍽️'}</div>
                    <button onclick="closeMealDetails()" class="absolute top-4 right-4 w-10 h-10 bg-white/20 backdrop-blur rounded-full flex items-center justify-center text-white">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
                <div class="p-6">
                    <h2 class="text-2xl font-black dark:text-white mb-2">${meal.name || meal.recipe_name || 'Comida'}</h2>
                    <p class="text-sm text-gray-500 mb-4">${mealNames[mealType] || mealType}</p>
                    
                    <div class="grid grid-cols-4 gap-3 mb-6">
                        <div class="glass rounded-xl p-3 text-center">
                            <p class="text-lg font-bold gradient-text">${formatCalories(meal.calories)}</p>
                            <p class="text-xs text-gray-500">kcal</p>
                        </div>
                        <div class="glass rounded-xl p-3 text-center">
                            <p class="text-lg font-bold text-red-500">${formatGrams(meal.protein)}g</p>
                            <p class="text-xs text-gray-500">Proteína</p>
                        </div>
                        <div class="glass rounded-xl p-3 text-center">
                            <p class="text-lg font-bold text-yellow-500">${formatGrams(meal.carbs)}g</p>
                            <p class="text-xs text-gray-500">Carbos</p>
                        </div>
                        <div class="glass rounded-xl p-3 text-center">
                            <p class="text-lg font-bold text-green-500">${formatGrams(meal.fat)}g</p>
                            <p class="text-xs text-gray-500">Grasa</p>
                        </div>
                    </div>
                    
                    ${meal.ingredients ? `
                        <div class="mb-4">
                            <h3 class="font-bold dark:text-white mb-2">Ingredientes:</h3>
                            <ul class="text-sm text-gray-600 dark:text-gray-400 space-y-1">
                                ${meal.ingredients.map(ing => `<li>• ${ing}</li>`).join('')}
                            </ul>
                        </div>
                    ` : ''}
                    
                    <div class="flex gap-3">
                        <button onclick="closeMealDetails()" class="flex-1 glass py-3 rounded-xl font-bold dark:text-white">
                            Cerrar
                        </button>
                        <button onclick="closeMealDetails(); openChangeRecipeModal('${day}', '${mealType}')" class="flex-1 btn-primary text-white py-3 rounded-xl font-bold">
                            Cambiar receta
                        </button>
                    </div>
                </div>
            </div>
        </div>
    `;
    document.body.style.overflow = 'hidden';
}

function closeMealDetails(event) {
    if (event && event.target !== event.currentTarget) return;
    document.getElementById('auth-modals').innerHTML = '';
    document.body.style.overflow = '';
}

async function openChangeRecipeModal(day, mealType) {
    showToast('Cargando recetas alternativas...', 'info');
    
    try {
        const response = await fetch(API_BASE + '/recipes?meal_type=' + mealType, {
            headers: { 'Authorization': 'Bearer ' + user.token }
        });
        
        let recipes = [];
        if (response.ok) {
            const data = await response.json();
            recipes = data.recipes || data || [];
        }
        
        // Fallback con recetas de ejemplo si no hay datos
        if (recipes.length === 0) {
            recipes = [
                { id: 1, name: 'Ensalada César', calories: 350, protein: 20, carbs: 15, fat: 22, image: '🥗' },
                { id: 2, name: 'Pechuga de pollo con arroz', calories: 450, protein: 35, carbs: 40, fat: 12, image: '🍗' },
                { id: 3, name: 'Salmón al horno', calories: 380, protein: 32, carbs: 5, fat: 24, image: '🐟' },
                { id: 4, name: 'Bowl de quinoa', calories: 420, protein: 18, carbs: 55, fat: 14, image: '🥣' },
                { id: 5, name: 'Tortilla de claras', calories: 180, protein: 22, carbs: 2, fat: 8, image: '🍳' },
                { id: 6, name: 'Yogur con frutos rojos', calories: 200, protein: 15, carbs: 25, fat: 5, image: '🫐' }
            ];
        }
        
        const container = document.getElementById('auth-modals');
        container.innerHTML = `
            <div class="fixed inset-0 z-[100] bg-black/60 backdrop-blur-sm flex items-center justify-center p-4" onclick="closeChangeRecipeModal(event)">
                <div class="glass-card bg-white dark:bg-gray-900 rounded-3xl max-w-lg w-full max-h-[80vh] overflow-hidden flex flex-col" onclick="event.stopPropagation()">
                    <div class="p-6 border-b border-gray-200 dark:border-gray-700">
                        <div class="flex items-center justify-between">
                            <h2 class="text-xl font-black dark:text-white">Cambiar Receta</h2>
                            <button onclick="closeChangeRecipeModal()" class="w-10 h-10 bg-gray-100 dark:bg-gray-800 rounded-full flex items-center justify-center">
                                <i class="fas fa-times"></i>
                            </button>
                        </div>
                        <p class="text-sm text-gray-500 mt-1">Selecciona una nueva receta para ${mealType}</p>
                    </div>
                    <div class="p-4 overflow-y-auto flex-1">
                        <div class="space-y-3">
                            ${recipes.map(recipe => `
                                <div class="glass rounded-xl p-4 flex items-center gap-4 cursor-pointer hover:bg-purple-50 dark:hover:bg-purple-900/20 transition-colors"
                                     onclick="selectRecipe('${day}', '${mealType}', ${recipe.id}, '${recipe.name}', ${recipe.calories})">
                                    <div class="text-3xl">${recipe.image || '🍽️'}</div>
                                    <div class="flex-1">
                                        <p class="font-bold dark:text-white">${recipe.name}</p>
                                        <p class="text-sm text-gray-500">${formatCalories(recipe.calories)} kcal • P: ${formatGrams(recipe.protein)}g • C: ${formatGrams(recipe.carbs)}g • G: ${formatGrams(recipe.fat)}g</p>
                                    </div>
                                    <button class="text-purple-500 hover:text-purple-600">
                                        <i class="fas fa-check-circle text-xl"></i>
                                    </button>
                                </div>
                            `).join('')}
                        </div>
                    </div>
                </div>
            </div>
        `;
        document.body.style.overflow = 'hidden';
        
    } catch (error) {
        console.error('Error loading recipes:', error);
        showToast('Error al cargar recetas', 'error');
    }
}

function closeChangeRecipeModal(event) {
    if (event && event.target !== event.currentTarget) return;
    document.getElementById('auth-modals').innerHTML = '';
    document.body.style.overflow = '';
}

async function selectRecipe(day, mealType, recipeId, recipeName, calories) {
    showToast('Actualizando plan...', 'info');
    
    try {
        const response = await fetch(API_BASE + '/plan/meal', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + user.token
            },
            body: JSON.stringify({
                day: day,
                meal_type: mealType,
                recipe_id: recipeId
            })
        });
        
        if (response.ok) {
            // Update local plan
            if (currentPlan && currentPlan.days && currentPlan.days[day]) {
                const mealIndex = currentPlan.days[day].findIndex(m => (m.meal_type || m.type || '').toLowerCase() === mealType);
                if (mealIndex !== -1) {
                    currentPlan.days[day][mealIndex] = {
                        ...currentPlan.days[day][mealIndex],
                        recipe_id: recipeId,
                        name: recipeName,
                        calories: calories
                    };
                }
            }
            
            closeChangeRecipeModal();
            renderWeeklyPlan();
            showToast('✅ Receta actualizada: ' + recipeName, 'success');
        } else {
            // Update locally even if API fails
            if (currentPlan && currentPlan.days && currentPlan.days[day]) {
                const mealIndex = currentPlan.days[day].findIndex(m => (m.meal_type || m.type || '').toLowerCase() === mealType);
                if (mealIndex !== -1) {
                    currentPlan.days[day][mealIndex] = {
                        ...currentPlan.days[day][mealIndex],
                        recipe_id: recipeId,
                        name: recipeName,
                        calories: calories
                    };
                }
            }
            
            closeChangeRecipeModal();
            renderWeeklyPlan();
            showToast('✅ Receta actualizada localmente: ' + recipeName, 'success');
        }
    } catch (error) {
        console.error('Error updating recipe:', error);
        showToast('Error al actualizar la receta', 'error');
    }
}

async function regeneratePlan() {
    if (!user || !user.token) {
        showToast('Debes iniciar sesión para regenerar el plan', 'error');
        return;
    }
    
    showToast('Regenerando plan...', 'info');
    
    try {
        const response = await fetch(API_BASE + '/generate-plan', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + user.token
            }
        });
        
        const data = await response.json();
        
        if (response.ok) {
            currentPlan = data.plan || data;
            renderWeeklyPlan();
            showToast('✅ Nuevo plan generado', 'success');
        } else {
            showToast('❌ ' + (data.error || 'Error al regenerar el plan'), 'error');
        }
    } catch (error) {
        console.error('Error regenerating plan:', error);
        showToast('Error de conexión', 'error');
    }
}

// ==================== ONBOARDING FLOW COMPLETO ====================

// Listas de preferencias y alergias
const DIETARY_PREFERENCES = [
    { id: 'vegan', name: 'Vegano', icon: '🌱' },
    { id: 'vegetarian', name: 'Vegetariano', icon: '🥗' },
    { id: 'pescatarian', name: 'Pescatariano', icon: '🐟' },
    { id: 'keto', name: 'Keto', icon: '🥑' },
    { id: 'paleo', name: 'Paleo', icon: '🍖' },
    { id: 'gluten_free', name: 'Sin gluten', icon: '🌾' },
    { id: 'lactose_free', name: 'Sin lactosa', icon: '🥛' },
    { id: 'low_carb', name: 'Bajo en carbohidratos', icon: '🍚' },
    { id: 'mediterranean', name: 'Mediterránea', icon: '🫒' }
];

const COMMON_ALLERGIES = [
    { id: 'gluten', name: 'Gluten', icon: '🌾' },
    { id: 'lactose', name: 'Lácteos', icon: '🥛' },
    { id: 'nuts', name: 'Frutos secos', icon: '🥜' },
    { id: 'shellfish', name: 'Mariscos', icon: '🦐' },
    { id: 'eggs', name: 'Huevos', icon: '🥚' },
    { id: 'soy', name: 'Soja', icon: '🫘' },
    { id: 'fish', name: 'Pescado', icon: '🐟' },
    { id: 'peanuts', name: 'Cacahuetes', icon: '🥜' }
];

const BUDGET_OPTIONS = [
    { id: 'low', name: 'Económico', desc: 'Comidas sencillas y económicas', icon: '💰' },
    { id: 'medium', name: 'Medio', desc: 'Balance entre calidad y precio', icon: '💵' },
    { id: 'high', name: 'Premium', desc: 'Ingredientes de alta calidad', icon: '💎' }
];

const MEALS_OPTIONS = [
    { id: 3, name: '3 comidas', desc: 'Desayuno, comida y cena', icon: '🍽️' },
    { id: 4, name: '4 comidas', desc: 'Desayuno, snack, comida y cena', icon: '🍱' },
    { id: 5, name: '5 comidas', desc: 'Desayuno, snack, comida, snack y cena', icon: '🥗' }
];

function startOnboarding() {
    onboardingStep = 0;
    onboardingData = {
        preferences: [],
        allergies: []
    };
    renderOnboardingStep();
    document.getElementById('onboarding-modal').classList.remove('hidden');
    document.body.style.overflow = 'hidden';
}

function closeOnboarding() {
    document.getElementById('onboarding-modal').classList.add('hidden');
    document.body.style.overflow = '';
}

function renderOnboardingStep() {
    const container = document.getElementById('onboarding-content');
    
    const steps = [
        // PASO 1: Bienvenida
        {
            title: '¡Bienvenido a Diet Tracker FIT! 🎉',
            content: `
                <p class="text-gray-600 dark:text-gray-400 mb-6">Vamos a crear tu plan nutricional personalizado en 7 pasos simples.</p>
                <div class="grid grid-cols-2 sm:grid-cols-4 gap-4 mb-6">
                    <div class="glass p-4 rounded-xl text-center">
                        <div class="text-3xl mb-2">🎯</div>
                        <p class="text-xs font-semibold dark:text-white">Objetivo</p>
                    </div>
                    <div class="glass p-4 rounded-xl text-center">
                        <div class="text-3xl mb-2">📊</div>
                        <p class="text-xs font-semibold dark:text-white">Datos</p>
                    </div>
                    <div class="glass p-4 rounded-xl text-center">
                        <div class="text-3xl mb-2">🏃</div>
                        <p class="text-xs font-semibold dark:text-white">Actividad</p>
                    </div>
                    <div class="glass p-4 rounded-xl text-center">
                        <div class="text-3xl mb-2">🥗</div>
                        <p class="text-xs font-semibold dark:text-white">Preferencias</p>
                    </div>
                </div>
                <div class="grid grid-cols-2 sm:grid-cols-3 gap-4">
                    <div class="glass p-4 rounded-xl text-center">
                        <div class="text-3xl mb-2">⚠️</div>
                        <p class="text-xs font-semibold dark:text-white">Alergias</p>
                    </div>
                    <div class="glass p-4 rounded-xl text-center">
                        <div class="text-3xl mb-2">💰</div>
                        <p class="text-xs font-semibold dark:text-white">Presupuesto</p>
                    </div>
                    <div class="glass p-4 rounded-xl text-center col-span-2 sm:col-span-1">
                        <div class="text-3xl mb-2">🍽️</div>
                        <p class="text-xs font-semibold dark:text-white">Comidas/día</p>
                    </div>
                </div>
            `,
            button: 'Comenzar configuración'
        },
        // PASO 2: Objetivo
        {
            title: 'Paso 1: ¿Cuál es tu objetivo? 🎯',
            content: `
                <div class="space-y-3">
                    <label class="glass p-4 rounded-xl flex items-center gap-4 cursor-pointer hover:bg-purple-50 dark:hover:bg-purple-900/20 transition-colors touch-target">
                        <input type="radio" name="goal" value="lose" ${onboardingData.goal === 'lose' ? 'checked' : ''} class="w-5 h-5 accent-purple-500">
                        <div class="flex-1">
                            <p class="font-bold dark:text-white">🔥 Perder peso</p>
                            <p class="text-sm text-gray-500">Quemar grasa y reducir medidas</p>
                        </div>
                        <span class="text-2xl">📉</span>
                    </label>
                    <label class="glass p-4 rounded-xl flex items-center gap-4 cursor-pointer hover:bg-purple-50 dark:hover:bg-purple-900/20 transition-colors touch-target">
                        <input type="radio" name="goal" value="maintain" ${onboardingData.goal === 'maintain' ? 'checked' : ''} class="w-5 h-5 accent-purple-500">
                        <div class="flex-1">
                            <p class="font-bold dark:text-white">⚖️ Mantener peso</p>
                            <p class="text-sm text-gray-500">Conservar y estabilizar tu figura</p>
                        </div>
                        <span class="text-2xl">🎯</span>
                    </label>
                    <label class="glass p-4 rounded-xl flex items-center gap-4 cursor-pointer hover:bg-purple-50 dark:hover:bg-purple-900/20 transition-colors touch-target">
                        <input type="radio" name="goal" value="gain" ${onboardingData.goal === 'gain' ? 'checked' : ''} class="w-5 h-5 accent-purple-500">
                        <div class="flex-1">
                            <p class="font-bold dark:text-white">💪 Ganar músculo</p>
                            <p class="text-sm text-gray-500">Aumentar masa muscular y fuerza</p>
                        </div>
                        <span class="text-2xl">📈</span>
                    </label>
                </div>
            `,
            button: 'Continuar',
            prev: true,
            validate: () => {
                const goal = document.querySelector('input[name="goal"]:checked');
                if (!goal) {
                    showToast('❌ Por favor selecciona un objetivo', 'error');
                    return false;
                }
                return true;
            }
        },
        // PASO 3: Datos personales
        {
            title: 'Paso 2: Tus datos personales 📊',
            content: `
                <div class="grid grid-cols-2 gap-4">
                    <div>
                        <label class="block text-sm font-semibold mb-2 dark:text-gray-200">Edad</label>
                        <input type="number" id="onboarding-age" value="${onboardingData.age || 30}" min="15" max="100" 
                               class="w-full px-4 py-3 rounded-xl border-2 border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 dark:text-white focus:border-purple-500 focus:outline-none touch-target"
                               placeholder="Años">
                    </div>
                    <div>
                        <label class="block text-sm font-semibold mb-2 dark:text-gray-200">Género</label>
                        <select id="onboarding-gender" class="w-full px-4 py-3 rounded-xl border-2 border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 dark:text-white focus:border-purple-500 focus:outline-none touch-target">
                            <option value="male" ${onboardingData.gender === 'male' ? 'selected' : ''}>👨 Hombre</option>
                            <option value="female" ${onboardingData.gender === 'female' ? 'selected' : ''}>👩 Mujer</option>
                        </select>
                    </div>
                    <div>
                        <label class="block text-sm font-semibold mb-2 dark:text-gray-200">Peso actual (kg)</label>
                        <input type="number" id="onboarding-weight" value="${onboardingData.weight || 70}" min="30" max="300" step="0.1"
                               class="w-full px-4 py-3 rounded-xl border-2 border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 dark:text-white focus:border-purple-500 focus:outline-none touch-target"
                               placeholder="Ej: 70">
                    </div>
                    <div>
                        <label class="block text-sm font-semibold mb-2 dark:text-gray-200">Peso objetivo (kg)</label>
                        <input type="number" id="onboarding-goal-weight" value="${onboardingData.goal_weight || 65}" min="30" max="300" step="0.1"
                               class="w-full px-4 py-3 rounded-xl border-2 border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 dark:text-white focus:border-purple-500 focus:outline-none touch-target"
                               placeholder="Ej: 65">
                    </div>
                    <div class="col-span-2">
                        <label class="block text-sm font-semibold mb-2 dark:text-gray-200">Altura (cm)</label>
                        <input type="number" id="onboarding-height" value="${onboardingData.height || 170}" min="100" max="250"
                               class="w-full px-4 py-3 rounded-xl border-2 border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 dark:text-white focus:border-purple-500 focus:outline-none touch-target"
                               placeholder="Ej: 170">
                    </div>
                </div>
            `,
            button: 'Continuar',
            prev: true,
            validate: () => {
                const age = parseFloat(document.getElementById('onboarding-age').value);
                const weight = parseFloat(document.getElementById('onboarding-weight').value);
                const height = parseFloat(document.getElementById('onboarding-height').value);
                const goalWeight = parseFloat(document.getElementById('onboarding-goal-weight').value);
                
                if (!age || age < 15 || age > 100) {
                    showToast('❌ Edad debe estar entre 15 y 100 años', 'error');
                    return false;
                }
                if (!weight || weight < 30 || weight > 300) {
                    showToast('❌ Peso debe estar entre 30 y 300 kg', 'error');
                    return false;
                }
                if (!height || height < 100 || height > 250) {
                    showToast('❌ Altura debe estar entre 100 y 250 cm', 'error');
                    return false;
                }
                return true;
            }
        },
        // PASO 4: Actividad física
        {
            title: 'Paso 3: Nivel de actividad física 🏃',
            content: `
                <div class="space-y-3">
                    <label class="glass p-4 rounded-xl flex items-center gap-4 cursor-pointer hover:bg-purple-50 dark:hover:bg-purple-900/20 transition-colors touch-target">
                        <input type="radio" name="activity" value="sedentary" ${onboardingData.activity === 'sedentary' ? 'checked' : ''} class="w-5 h-5 accent-purple-500">
                        <div class="flex-1">
                            <p class="font-bold dark:text-white">🪑 Sedentario</p>
                            <p class="text-sm text-gray-500">Trabajo de oficina, poco ejercicio</p>
                        </div>
                    </label>
                    <label class="glass p-4 rounded-xl flex items-center gap-4 cursor-pointer hover:bg-purple-50 dark:hover:bg-purple-900/20 transition-colors touch-target">
                        <input type="radio" name="activity" value="light" ${onboardingData.activity === 'light' ? 'checked' : ''} class="w-5 h-5 accent-purple-500">
                        <div class="flex-1">
                            <p class="font-bold dark:text-white">🚶 Ligero</p>
                            <p class="text-sm text-gray-500">Ejercicio 1-3 días por semana</p>
                        </div>
                    </label>
                    <label class="glass p-4 rounded-xl flex items-center gap-4 cursor-pointer hover:bg-purple-50 dark:hover:bg-purple-900/20 transition-colors touch-target">
                        <input type="radio" name="activity" value="moderate" ${onboardingData.activity === 'moderate' ? 'checked' : ''} class="w-5 h-5 accent-purple-500">
                        <div class="flex-1">
                            <p class="font-bold dark:text-white">🏃 Moderado</p>
                            <p class="text-sm text-gray-500">Ejercicio 3-5 días por semana</p>
                        </div>
                    </label>
                    <label class="glass p-4 rounded-xl flex items-center gap-4 cursor-pointer hover:bg-purple-50 dark:hover:bg-purple-900/20 transition-colors touch-target">
                        <input type="radio" name="activity" value="active" ${onboardingData.activity === 'active' ? 'checked' : ''} class="w-5 h-5 accent-purple-500">
                        <div class="flex-1">
                            <p class="font-bold dark:text-white">💪 Activo</p>
                            <p class="text-sm text-gray-500">Ejercicio intenso 6-7 días por semana</p>
                        </div>
                    </label>
                </div>
            `,
            button: 'Continuar',
            prev: true,
            validate: () => {
                const activity = document.querySelector('input[name="activity"]:checked');
                if (!activity) {
                    showToast('❌ Por favor selecciona tu nivel de actividad', 'error');
                    return false;
                }
                return true;
            }
        },
        // PASO 5: Preferencias alimentarias
        {
            title: 'Paso 4: Preferencias alimentarias 🥗',
            content: `
                <p class="text-sm text-gray-500 mb-4">Selecciona tus preferencias dietéticas (puedes elegir varias)</p>
                <div class="grid grid-cols-2 sm:grid-cols-3 gap-3">
                    ${DIETARY_PREFERENCES.map(pref => `
                        <label class="glass p-3 rounded-xl flex items-center gap-2 cursor-pointer hover:bg-purple-50 dark:hover:bg-purple-900/20 transition-colors touch-target ${onboardingData.preferences?.includes(pref.id) ? 'bg-purple-50 dark:bg-purple-900/30 border-purple-500 border-2' : ''}">
                            <input type="checkbox" name="preference" value="${pref.id}" 
                                   ${onboardingData.preferences?.includes(pref.id) ? 'checked' : ''} 
                                   class="hidden preference-checkbox"
                                   onchange="togglePreference('${pref.id}', this)">
                            <span class="text-xl">${pref.icon}</span>
                            <span class="text-sm font-medium dark:text-white">${pref.name}</span>
                        </label>
                    `).join('')}
                </div>
                <div class="mt-4 p-3 glass rounded-xl">
                    <p class="text-sm text-gray-500 mb-2">¿Tienes alguna restricción adicional?</p>
                    <input type="text" id="onboarding-other-preferences" 
                           value="${onboardingData.other_preferences || ''}"
                           placeholder="Ej: Sin azúcar, baja en sal..."
                           class="w-full px-4 py-2 rounded-lg border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 dark:text-white focus:border-purple-500 focus:outline-none touch-target">
                </div>
            `,
            button: 'Continuar',
            prev: true
        },
        // PASO 6: Alergias
        {
            title: 'Paso 5: Alergias alimentarias ⚠️',
            content: `
                <p class="text-sm text-gray-500 mb-4">Selecciona cualquier alergia que tengas (se evitarán estos ingredientes)</p>
                <div class="grid grid-cols-2 gap-3">
                    ${COMMON_ALLERGIES.map(allergy => `
                        <label class="glass p-3 rounded-xl flex items-center gap-2 cursor-pointer hover:bg-red-50 dark:hover:bg-red-900/20 transition-colors touch-target ${onboardingData.allergies?.includes(allergy.id) ? 'bg-red-50 dark:bg-red-900/30 border-red-500 border-2' : ''}">
                            <input type="checkbox" name="allergy" value="${allergy.id}" 
                                   ${onboardingData.allergies?.includes(allergy.id) ? 'checked' : ''} 
                                   class="hidden allergy-checkbox"
                                   onchange="toggleAllergy('${allergy.id}', this)">
                            <span class="text-xl">${allergy.icon}</span>
                            <span class="text-sm font-medium dark:text-white">${allergy.name}</span>
                        </label>
                    `).join('')}
                </div>
                <div class="mt-4 p-3 glass rounded-xl">
                    <p class="text-sm text-gray-500 mb-2">¿Otras alergias?</p>
                    <input type="text" id="onboarding-other-allergies" 
                           value="${onboardingData.other_allergies || ''}"
                           placeholder="Ej: Mostaza, apio, sulfitos..."
                           class="w-full px-4 py-2 rounded-lg border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 dark:text-white focus:border-purple-500 focus:outline-none touch-target">
                </div>
            `,
            button: 'Continuar',
            prev: true
        },
        // PASO 7: Presupuesto
        {
            title: 'Paso 6: Presupuesto semanal 💰',
            content: `
                <p class="text-sm text-gray-500 mb-4">¿Cuánto quieres gastar en comida por semana?</p>
                <div class="space-y-3">
                    ${BUDGET_OPTIONS.map(budget => `
                        <label class="glass p-4 rounded-xl flex items-center gap-4 cursor-pointer hover:bg-purple-50 dark:hover:bg-purple-900/20 transition-colors touch-target ${onboardingData.budget === budget.id ? 'bg-purple-50 dark:bg-purple-900/30 border-purple-500 border-2' : ''}">
                            <input type="radio" name="budget" value="${budget.id}" 
                                   ${onboardingData.budget === budget.id ? 'checked' : ''} 
                                   class="w-5 h-5 accent-purple-500">
                            <div class="flex-1">
                                <p class="font-bold dark:text-white">${budget.icon} ${budget.name}</p>
                                <p class="text-sm text-gray-500">${budget.desc}</p>
                            </div>
                        </label>
                    `).join('')}
                </div>
            `,
            button: 'Continuar',
            prev: true,
            validate: () => {
                const budget = document.querySelector('input[name="budget"]:checked');
                if (!budget) {
                    showToast('❌ Por favor selecciona tu presupuesto', 'error');
                    return false;
                }
                return true;
            }
        },
        // PASO 8: Comidas por día
        {
            title: 'Paso 7: Comidas por día 🍽️',
            content: `
                <p class="text-sm text-gray-500 mb-4">¿Cuántas comidas principales quieres hacer al día?</p>
                <div class="space-y-3">
                    ${MEALS_OPTIONS.map(meals => `
                        <label class="glass p-4 rounded-xl flex items-center gap-4 cursor-pointer hover:bg-purple-50 dark:hover:bg-purple-900/20 transition-colors touch-target ${onboardingData.meals_per_day === meals.id ? 'bg-purple-50 dark:bg-purple-900/30 border-purple-500 border-2' : ''}">
                            <input type="radio" name="meals" value="${meals.id}" 
                                   ${onboardingData.meals_per_day === meals.id ? 'checked' : ''} 
                                   class="w-5 h-5 accent-purple-500">
                            <div class="flex-1">
                                <p class="font-bold dark:text-white">${meals.icon} ${meals.name}</p>
                                <p class="text-sm text-gray-500">${meals.desc}</p>
                            </div>
                        </label>
                    `).join('')}
                </div>
            `,
            button: 'Calcular mi plan',
            prev: true,
            validate: () => {
                const meals = document.querySelector('input[name="meals"]:checked');
                if (!meals) {
                    showToast('❌ Por favor selecciona el número de comidas', 'error');
                    return false;
                }
                return true;
            }
        },
        // PASO 9: Resultados y generación de plan
        {
            title: '¡Tu plan está listo! 🎉',
            content: `
                <div class="text-center">
                    <div class="w-20 h-20 bg-gradient-to-br from-green-500 to-emerald-500 rounded-full flex items-center justify-center text-4xl mx-auto mb-4 animate-bounce">✓</div>
                    
                    <div class="glass-card rounded-2xl p-6 mb-4">
                        <h3 class="font-bold dark:text-white mb-4">📊 Tus métricas calculadas</h3>
                        <div class="grid grid-cols-2 gap-4">
                            <div class="text-center p-3 glass rounded-xl">
                                <p class="text-xs text-gray-500 mb-1">TMB (Metabolismo Basal)</p>
                                <p class="text-2xl font-black gradient-text" id="bmr-result">--</p>
                            </div>
                            <div class="text-center p-3 glass rounded-xl">
                                <p class="text-xs text-gray-500 mb-1">TDEE (Gasto Total)</p>
                                <p class="text-2xl font-black gradient-text" id="tdee-result">--</p>
                            </div>
                        </div>
                        <div class="mt-4 text-center p-4 bg-gradient-to-r from-purple-500 to-blue-500 rounded-xl">
                            <p class="text-xs text-white/80 mb-1">Calorías diarias objetivo</p>
                            <p class="text-4xl font-black text-white" id="calories-result">--</p>
                        </div>
                    </div>
                    
                    <div id="plan-generation-status" class="text-sm text-gray-500">
                        <div class="flex items-center justify-center gap-2">
                            <div class="w-4 h-4 border-2 border-purple-500 border-t-transparent rounded-full animate-spin"></div>
                            <span>Generando tu plan personalizado...</span>
                        </div>
                    </div>
                    <div id="plan-preview" class="hidden mt-4 text-left">
                        <h4 class="font-bold dark:text-white mb-2">🍽️ Vista previa del plan:</h4>
                        <div id="plan-content" class="glass rounded-xl p-4 max-h-40 overflow-y-auto text-sm dark:text-gray-300"></div>
                    </div>
                </div>
            `,
            button: '¡Comenzar mi transformación!',
            prev: true,
            onShow: calculateAndGeneratePlan
        }
    ];
    
    const step = steps[onboardingStep];
    
    container.innerHTML = `
        <div class="fade-in">
            <div class="mb-6">
                <div class="flex gap-1 mb-4">
                    ${steps.map((_, i) => `
                        <div class="h-2 flex-1 rounded-full transition-all ${i <= onboardingStep ? 'bg-gradient-to-r from-purple-500 to-blue-500' : 'bg-gray-200 dark:bg-gray-700'}"></div>
                    `).join('')}
                </div>
                <div class="flex items-center gap-2 text-sm text-gray-500 mb-2">
                    <span>Paso ${onboardingStep} de ${steps.length - 1}</span>
                </div>
                <h2 class="text-2xl font-black dark:text-white">${step.title}</h2>
            </div>
            
            ${step.content}
            
            <div class="flex gap-4 mt-8">
                ${step.prev ? `
                    <button onclick="prevOnboardingStep()" class="flex-1 py-3 rounded-xl font-bold border-2 border-gray-200 dark:border-gray-700 dark:text-white hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors touch-target">
                        ← Atrás
                    </button>
                ` : '<div class="flex-1"></div>'}
                <button onclick="nextOnboardingStep()" class="flex-1 btn-primary text-white py-3 rounded-xl font-bold touch-target flex items-center justify-center gap-2" id="onboarding-next-btn">
                    ${step.button}
                    ${onboardingStep < steps.length - 1 ? '<i class="fas fa-arrow-right"></i>' : ''}
                </button>
            </div>
        </div>
    `;
    
    if (step.onShow) {
        setTimeout(step.onShow, 100);
    }
}

// Funciones auxiliares para checkboxes
function togglePreference(id, checkbox) {
    if (!onboardingData.preferences) onboardingData.preferences = [];
    if (checkbox.checked) {
        if (!onboardingData.preferences.includes(id)) {
            onboardingData.preferences.push(id);
        }
    } else {
        onboardingData.preferences = onboardingData.preferences.filter(p => p !== id);
    }
    // Actualizar estilo visual
    const label = checkbox.closest('label');
    if (checkbox.checked) {
        label.classList.add('bg-purple-50', 'dark:bg-purple-900/30', 'border-purple-500', 'border-2');
    } else {
        label.classList.remove('bg-purple-50', 'dark:bg-purple-900/30', 'border-purple-500', 'border-2');
    }
}

function toggleAllergy(id, checkbox) {
    if (!onboardingData.allergies) onboardingData.allergies = [];
    if (checkbox.checked) {
        if (!onboardingData.allergies.includes(id)) {
            onboardingData.allergies.push(id);
        }
    } else {
        onboardingData.allergies = onboardingData.allergies.filter(a => a !== id);
    }
    // Actualizar estilo visual
    const label = checkbox.closest('label');
    if (checkbox.checked) {
        label.classList.add('bg-red-50', 'dark:bg-red-900/30', 'border-red-500', 'border-2');
    } else {
        label.classList.remove('bg-red-50', 'dark:bg-red-900/30', 'border-red-500', 'border-2');
    }
}

function prevOnboardingStep() {
    if (onboardingStep > 0) {
        saveOnboardingData();
        onboardingStep--;
        renderOnboardingStep();
    }
}

function nextOnboardingStep() {
    // Guardar datos del paso actual
    saveOnboardingData();
    
    // Validar si existe validación
    const container = document.getElementById('onboarding-content');
    const steps = getOnboardingSteps();
    const currentStep = steps[onboardingStep];
    
    if (currentStep.validate && !currentStep.validate()) {
        return;
    }
    
    const totalSteps = steps.length - 1;
    
    if (onboardingStep < totalSteps) {
        onboardingStep++;
        renderOnboardingStep();
    } else {
        // Último paso: cerrar y mostrar dashboard
        completeOnboarding();
    }
}

// Definir los pasos del onboarding como variable global para acceso desde renderOnboardingStep y getOnboardingSteps
const ONBOARDING_STEPS = [
    // PASO 0: Bienvenida
    {
        title: '¡Bienvenido a Diet Tracker FIT! 🎉',
        content: null, // Se genera dinámicamente
        button: 'Comenzar configuración'
    },
    // PASO 1: Objetivo
    {
        title: 'Paso 1: ¿Cuál es tu objetivo? 🎯',
        validate: () => {
            const goal = document.querySelector('input[name="goal"]:checked');
            if (!goal) {
                showToast('❌ Por favor selecciona un objetivo', 'error');
                return false;
            }
            return true;
        }
    },
    // PASO 2: Datos personales
    {
        title: 'Paso 2: Tus datos personales 📊',
        validate: () => {
            const age = parseFloat(document.getElementById('onboarding-age')?.value);
            const weight = parseFloat(document.getElementById('onboarding-weight')?.value);
            const height = parseFloat(document.getElementById('onboarding-height')?.value);
            const goalWeight = parseFloat(document.getElementById('onboarding-goal-weight')?.value);
            
            if (!age || age < 15 || age > 100) {
                showToast('❌ Edad debe estar entre 15 y 100 años', 'error');
                return false;
            }
            if (!weight || weight < 30 || weight > 300) {
                showToast('❌ Peso debe estar entre 30 y 300 kg', 'error');
                return false;
            }
            if (!height || height < 100 || height > 250) {
                showToast('❌ Altura debe estar entre 100 y 250 cm', 'error');
                return false;
            }
            return true;
        }
    },
    // PASO 3: Actividad física
    {
        title: 'Paso 3: Nivel de actividad física 🏃',
        validate: () => {
            const activity = document.querySelector('input[name="activity"]:checked');
            if (!activity) {
                showToast('❌ Por favor selecciona tu nivel de actividad', 'error');
                return false;
            }
            return true;
        }
    },
    // PASO 4: Preferencias alimentarias
    {
        title: 'Paso 4: Preferencias alimentarias 🥗'
    },
    // PASO 5: Alergias
    {
        title: 'Paso 5: Alergias alimentarias ⚠️'
    },
    // PASO 6: Presupuesto
    {
        title: 'Paso 6: Presupuesto semanal 💰',
        validate: () => {
            const budget = document.querySelector('input[name="budget"]:checked');
            if (!budget) {
                showToast('❌ Por favor selecciona tu presupuesto', 'error');
                return false;
            }
            return true;
        }
    },
    // PASO 7: Comidas por día
    {
        title: 'Paso 7: Comidas por día 🍽️',
        validate: () => {
            const meals = document.querySelector('input[name="meals"]:checked');
            if (!meals) {
                showToast('❌ Por favor selecciona el número de comidas', 'error');
                return false;
            }
            return true;
        }
    },
    // PASO 8: Resultados
    {
        title: '¡Tu plan está listo! 🎉',
        onShow: 'calculateAndGeneratePlan'
    }
];

function getOnboardingSteps() {
    return ONBOARDING_STEPS;
}

function saveOnboardingData() {
    // Paso 1: Bienvenida - no hay datos
    if (onboardingStep === 1) {
        const goal = document.querySelector('input[name="goal"]:checked');
        if (goal) onboardingData.goal = goal.value;
    }
    // Paso 2: Datos personales
    else if (onboardingStep === 2) {
        onboardingData.age = parseFloat(document.getElementById('onboarding-age').value);
        onboardingData.gender = document.getElementById('onboarding-gender').value;
        onboardingData.weight = parseFloat(document.getElementById('onboarding-weight').value);
        onboardingData.height = parseFloat(document.getElementById('onboarding-height').value);
        onboardingData.goal_weight = parseFloat(document.getElementById('onboarding-goal-weight').value);
    }
    // Paso 3: Actividad
    else if (onboardingStep === 3) {
        const activity = document.querySelector('input[name="activity"]:checked');
        if (activity) onboardingData.activity = activity.value;
    }
    // Paso 4: Preferencias - ya se guardan con togglePreference
    else if (onboardingStep === 4) {
        const otherPrefs = document.getElementById('onboarding-other-preferences');
        if (otherPrefs) onboardingData.other_preferences = otherPrefs.value;
    }
    // Paso 5: Alergias - ya se guardan con toggleAllergy
    else if (onboardingStep === 5) {
        const otherAllergies = document.getElementById('onboarding-other-allergies');
        if (otherAllergies) onboardingData.other_allergies = otherAllergies.value;
    }
    // Paso 6: Presupuesto
    else if (onboardingStep === 6) {
        const budget = document.querySelector('input[name="budget"]:checked');
        if (budget) onboardingData.budget = budget.value;
    }
    // Paso 7: Comidas por día
    else if (onboardingStep === 7) {
        const meals = document.querySelector('input[name="meals"]:checked');
        if (meals) onboardingData.meals_per_day = parseInt(meals.value);
    }
}

// ==================== CÁLCULO DE CALORÍAS ====================

function calculateCalories() {
    // Calcular TMB usando la fórmula Mifflin-St Jeor
    let bmr = 10 * onboardingData.weight + 6.25 * onboardingData.height - 5 * onboardingData.age;
    bmr += onboardingData.gender === 'male' ? 5 : -161;
    
    // Multiplicadores de actividad
    const activityMultipliers = {
        sedentary: 1.2,
        light: 1.375,
        moderate: 1.55,
        active: 1.725
    };
    
    const tdee = bmr * (activityMultipliers[onboardingData.activity] || 1.2);
    
    // Ajustes según objetivo
    let targetCalories = tdee;
    let deficit = 0;
    
    if (onboardingData.goal === 'lose') {
        // Déficit de 500 kcal para perder ~0.5kg por semana
        deficit = 500;
        targetCalories = tdee - deficit;
        // Mínimo seguro: no bajar de 1200 kcal (mujeres) o 1500 kcal (hombres)
        const minCalories = onboardingData.gender === 'female' ? 1200 : 1500;
        if (targetCalories < minCalories) {
            targetCalories = minCalories;
        }
    } else if (onboardingData.goal === 'gain') {
        // Superávit de 300-500 kcal para ganar músculo
        targetCalories = tdee + 400;
    }
    
    // Calcular macros
    let protein, carbs, fat;
    
    if (onboardingData.goal === 'lose') {
        // Alta proteína para preservar músculo en déficit
        protein = onboardingData.weight * 2; // 2g por kg de peso
        fat = (targetCalories * 0.25) / 9; // 25% de calorías de grasa
        carbs = (targetCalories - (protein * 4) - (fat * 9)) / 4;
    } else if (onboardingData.goal === 'gain') {
        // Moderada proteína, más carbohidratos
        protein = onboardingData.weight * 1.8;
        fat = (targetCalories * 0.25) / 9;
        carbs = (targetCalories - (protein * 4) - (fat * 9)) / 4;
    } else {
        // Mantenimiento
        protein = onboardingData.weight * 1.6;
        fat = (targetCalories * 0.3) / 9;
        carbs = (targetCalories - (protein * 4) - (fat * 9)) / 4;
    }
    
    return {
        bmr: Math.round(bmr),
        tdee: Math.round(tdee),
        targetCalories: Math.round(targetCalories),
        macros: {
            protein: Math.round(protein),
            carbs: Math.round(carbs),
            fat: Math.round(fat)
        },
        deficit: deficit
    };
}

// ==================== GENERACIÓN DE PLAN ====================

async function calculateAndGeneratePlan() {
    // Calcular calorías primero
    const calories = calculateCalories();
    
    // Mostrar resultados en el UI
    document.getElementById('bmr-result').textContent = calories.bmr + ' kcal';
    document.getElementById('tdee-result').textContent = calories.tdee + ' kcal';
    document.getElementById('calories-result').textContent = calories.targetCalories + ' kcal';
    
    // Guardar en onboardingData
    onboardingData.calculated = calories;
    
    // Intentar generar el plan con el backend
    try {
        const response = await generateMealPlan();
        
        if (response && response.success) {
            // Mostrar preview del plan
            const planPreview = document.getElementById('plan-preview');
            const planContent = document.getElementById('plan-content');
            const statusEl = document.getElementById('plan-generation-status');
            
            if (planPreview && planContent && statusEl) {
                statusEl.innerHTML = '<p class="text-green-500">✓ Plan generado correctamente</p>';
                
                // Mostrar resumen del plan
                let previewHTML = '';
                if (response.plan && response.plan.days) {
                    const firstDay = response.plan.days[0];
                    previewHTML = `
                        <p class="mb-2"><strong>Día 1:</strong></p>
                        ${firstDay.meals.map(meal => `
                            <p>${meal.type}: ${meal.name || meal.recipe_name || 'Comida'} (${meal.calories || '--'} kcal)</p>
                        `).join('')}
                    `;
                } else if (response.message) {
                    previewHTML = `<p>${response.message}</p>`;
                }
                
                planContent.innerHTML = previewHTML;
                planPreview.classList.remove('hidden');
            }
        }
    } catch (error) {
        console.log('Generación de plan en segundo plano:', error.message);
        // El plan se generará cuando el usuario tenga más datos
    }
}

async function generateMealPlan() {
    if (!user || !user.token) {
        return null;
    }
    
    try {
        const response = await fetch(API_BASE + '/generate-plan', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + user.token
            },
            body: JSON.stringify({
                goal: onboardingData.goal,
                weight: onboardingData.weight,
                height: onboardingData.height,
                age: onboardingData.age,
                gender: onboardingData.gender,
                activity_level: onboardingData.activity,
                preferences: onboardingData.preferences || [],
                allergies: onboardingData.allergies || [],
                budget: onboardingData.budget,
                meals_per_day: onboardingData.meals_per_day,
                target_calories: onboardingData.calculated?.targetCalories,
                macros: onboardingData.calculated?.macros
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            return { success: true, plan: data.plan || data, message: data.message };
        } else {
            console.log('Plan generation response:', data);
            return { success: false, error: data.error };
        }
    } catch (error) {
        console.log('Error generating plan:', error);
        return null;
    }
}

async function completeOnboarding() {
    // Guardar datos del perfil en el backend
    try {
        const token = user?.token;
        if (token) {
            const response = await fetch(API_BASE + '/profile', {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + token
                },
                body: JSON.stringify({
                    ...onboardingData,
                    onboarding_completed: true
                })
            });
            
            if (response.ok) {
                console.log('Perfil actualizado correctamente');
            }
        }
    } catch (error) {
        console.log('Error guardando perfil:', error);
    }
    
    closeOnboarding();
    showToast('✅ ¡Plan personalizado creado! Tu transformación comienza ahora.', 'success');
    
    // Reload plan after onboarding
    await loadWeeklyPlan();
    
    // Recargar dashboard para mostrar el nuevo plan
    setTimeout(() => {
        loadDashboard();
    }, 500);
}

// ==================== FOOD REGISTRATION ====================

let currentFoodSearch = null;
let selectedMealType = null;
let todayFoodLogs = [];

function openFoodModal() {
    document.getElementById('food-modal').classList.remove('hidden');
    document.body.style.overflow = 'hidden';
    renderFoodModalMain();
    loadTodayFoodLogs();
}

function closeFoodModal() {
    document.getElementById('food-modal').classList.add('hidden');
    document.body.style.overflow = '';
}

function renderFoodModalMain() {
    const container = document.getElementById('food-content');
    
    container.innerHTML = `
        <div class="fade-in">
            <h2 class="text-2xl font-black dark:text-white mb-6">🍽️ Registrar comida</h2>
            
            <!-- Opciones principales -->
            <div class="space-y-4 mb-6">
                <button onclick="showPlanMealSelection()" class="w-full glass p-6 rounded-xl flex items-center gap-4 hover:bg-green-50 dark:hover:bg-green-900/20 transition-colors touch-target">
                    <div class="w-14 h-14 bg-gradient-to-br from-green-500 to-emerald-500 rounded-xl flex items-center justify-center text-2xl">✓</div>
                    <div class="text-left flex-1">
                        <p class="font-bold dark:text-white text-lg">Comí lo del plan</p>
                        <p class="text-sm text-gray-500">Registrar una comida planificada</p>
                    </div>
                    <i class="fas fa-chevron-right text-gray-400"></i>
                </button>
                
                <button onclick="showFoodSearch()" class="w-full glass p-6 rounded-xl flex items-center gap-4 hover:bg-purple-50 dark:hover:bg-purple-900/20 transition-colors touch-target">
                    <div class="w-14 h-14 bg-gradient-to-br from-purple-500 to-blue-500 rounded-xl flex items-center justify-center text-2xl">🔍</div>
                    <div class="text-left flex-1">
                        <p class="font-bold dark:text-white text-lg">Comí otra cosa</p>
                        <p class="text-sm text-gray-500">Buscar en recetas o productos</p>
                    </div>
                    <i class="fas fa-chevron-right text-gray-400"></i>
                </button>
                
                <button onclick="showBarcodeScanner()" class="w-full glass p-6 rounded-xl flex items-center gap-4 hover:bg-orange-50 dark:hover:bg-orange-900/20 transition-colors touch-target opacity-50" disabled>
                    <div class="w-14 h-14 bg-gradient-to-br from-orange-500 to-red-500 rounded-xl flex items-center justify-center text-2xl">📷</div>
                    <div class="text-left flex-1">
                        <p class="font-bold dark:text-white text-lg">Escanear código</p>
                        <p class="text-sm text-gray-500">Próximamente</p>
                    </div>
                    <span class="text-xs bg-gray-200 dark:bg-gray-700 px-2 py-1 rounded-full">Soon</span>
                </button>
            </div>
            
            <!-- Historial del día -->
            <div class="border-t border-gray-200 dark:border-gray-700 pt-6">
                <h3 class="font-bold dark:text-white mb-4 flex items-center gap-2">
                    <span>📊</span> Historial de hoy
                </h3>
                <div id="today-log-container" class="space-y-2">
                    <div class="text-center py-4 text-gray-500">
                        <div class="animate-spin w-6 h-6 border-2 border-purple-500 border-t-transparent rounded-full mx-auto mb-2"></div>
                        <p class="text-sm">Cargando...</p>
                    </div>
                </div>
            </div>
        </div>
    `;
}

async function loadTodayFoodLogs() {
    const container = document.getElementById('today-log-container');
    if (!container) return;
    
    try {
        const token = user?.token;
        const res = await fetch(API_BASE + '/food-log/today', {
            headers: { 'Authorization': 'Bearer ' + token }
        });
        
        const data = await res.json();
        
        if (res.ok) {
            todayFoodLogs = data.logs || [];
            renderTodayLogs(data);
        } else {
            container.innerHTML = `<p class="text-center py-4 text-gray-500">Error al cargar historial</p>`;
        }
    } catch (err) {
        console.error('Error loading food logs:', err);
        container.innerHTML = `<p class="text-center py-4 text-gray-500">No hay registros todavía</p>`;
    }
}

function renderTodayLogs(data) {
    const container = document.getElementById('today-log-container');
    if (!container) return;
    
    const logs = data.logs || [];
    const totals = data.totors || {};
    
    if (logs.length === 0) {
        container.innerHTML = `
            <div class="text-center py-6 text-gray-500">
                <div class="text-4xl mb-2">🍽️</div>
                <p>Aún no has registrado comidas hoy</p>
            </div>
        `;
        return;
    }
    
    const mealIcons = {
        'desayuno': '🌅',
        'comida': '☀️',
        'almuerzo': '🥪',
        'merienda': '🍎',
        'cena': '🌙',
        'snack': '🥨',
        'other': '🍽️'
    };
    
    container.innerHTML = `
        <!-- Totales del día -->
        <div class="glass-card rounded-xl p-4 mb-4">
            <div class="flex justify-between items-center mb-2">
                <span class="text-sm text-gray-500">Total consumido</span>
                <span class="font-bold gradient-text">${formatCalories(totals.calories || 0)} kcal</span>
            </div>
            <div class="flex gap-4 text-xs text-gray-500">
                <span>P: ${formatGrams(totals.protein || 0)}g</span>
                <span>C: ${formatGrams(totals.carbs || 0)}g</span>
                <span>G: ${formatGrams(totals.fat || 0)}g</span>
            </div>
        </div>
        
        <!-- Lista de comidas -->
        ${logs.map(log => `
            <div class="glass rounded-xl p-3 flex items-center justify-between">
                <div class="flex items-center gap-3">
                    <span class="text-xl">${mealIcons[log.meal_type] || '🍽️'}</span>
                    <div>
                        <p class="font-medium dark:text-white text-sm">${log.food_name || log.recipe_name || 'Comida'}</p>
                        <p class="text-xs text-gray-500">${formatCalories(log.calories)} kcal</p>
                    </div>
                </div>
                <button onclick="deleteFoodLog('${log.id}')" class="text-red-500 hover:bg-red-50 dark:hover:bg-red-900/20 p-2 rounded-lg touch-target">
                    <i class="fas fa-trash-alt"></i>
                </button>
            </div>
        `).join('')}
    `;
}

async function deleteFoodLog(logId) {
    if (!confirm('¿Eliminar esta comida del registro?')) return;
    
    try {
        const token = user?.token;
        const res = await fetch(API_BASE + '/food-log/' + logId, {
            method: 'DELETE',
            headers: { 'Authorization': 'Bearer ' + token }
        });
        
        if (res.ok) {
            showToast('✅ Comida eliminada', 'success');
            loadTodayFoodLogs();
            loadDashboard();
        } else {
            showToast('❌ Error al eliminar', 'error');
        }
    } catch (err) {
        showToast('❌ Error de conexión', 'error');
    }
}

// ==================== PLAN MEAL SELECTION ====================

async function showPlanMealSelection() {
    const container = document.getElementById('food-content');
    
    container.innerHTML = `
        <div class="fade-in">
            <button onclick="renderFoodModalMain()" class="flex items-center gap-2 text-purple-500 font-semibold mb-4 touch-target">
                <i class="fas fa-arrow-left"></i> Volver
            </button>
            <h2 class="text-2xl font-black dark:text-white mb-2">📋 Comí lo del plan</h2>
            <p class="text-gray-500 mb-6">Selecciona qué comida del día consumiste</p>
            
            <div id="plan-meals-container" class="space-y-3">
                <div class="text-center py-8">
                    <div class="animate-spin w-8 h-8 border-4 border-purple-500 border-t-transparent rounded-full mx-auto mb-4"></div>
                    <p class="text-gray-500">Cargando tu plan...</p>
                </div>
            </div>
        </div>
    `;
    
    // Load today's plan
    try {
        const token = user?.token;
        const today = new Date().getDay();
        const dayIndex = today === 0 ? 6 : today - 1; // Sunday = 6, Monday = 0
        
        const res = await fetch(API_BASE + '/plan', {
            headers: { 'Authorization': 'Bearer ' + token }
        });
        
        const data = await res.json();
        
        if (res.ok && data.plan_entries) {
            const todayPlan = data.plan_entries.filter(entry => entry.day_of_week === dayIndex);
            renderPlanMeals(todayPlan);
        } else {
            document.getElementById('plan-meals-container').innerHTML = `
                <div class="text-center py-8">
                    <div class="text-4xl mb-4">📭</div>
                    <p class="text-gray-500 mb-4">No hay plan para hoy</p>
                    <button onclick="showFoodSearch()" class="btn-primary text-white px-6 py-2 rounded-xl font-bold touch-target">
                        Buscar otra comida
                    </button>
                </div>
            `;
        }
    } catch (err) {
        document.getElementById('plan-meals-container').innerHTML = `
            <div class="text-center py-8 text-red-500">
                <p>Error al cargar el plan</p>
            </div>
        `;
    }
}

function renderPlanMeals(meals) {
    const container = document.getElementById('plan-meals-container');
    
    if (!meals || meals.length === 0) {
        container.innerHTML = `
            <div class="text-center py-8">
                <div class="text-4xl mb-4">📭</div>
                <p class="text-gray-500 mb-4">No hay comidas planificadas para hoy</p>
                <button onclick="showFoodSearch()" class="btn-primary text-white px-6 py-2 rounded-xl font-bold touch-target">
                    Buscar otra comida
                </button>
            </div>
        `;
        return;
    }
    
    const mealIcons = {
        'desayuno': '🌅',
        'comida': '☀️',
        'almuerzo': '🥪',
        'merienda': '🍎',
        'cena': '🌙'
    };
    
    container.innerHTML = meals.map(meal => `
        <div class="glass-card rounded-xl p-4 flex items-center justify-between">
            <div class="flex items-center gap-4">
                <div class="w-12 h-12 bg-gradient-to-br from-purple-500 to-blue-500 rounded-xl flex items-center justify-center text-xl">
                    ${mealIcons[meal.meal_type] || '🍽️'}
                </div>
                <div>
                    <p class="font-bold dark:text-white">${meal.recipe_name || 'Plan meal'}</p>
                    <p class="text-sm text-gray-500 capitalize">${meal.meal_type} • ${meal.calories || '--'} kcal</p>
                </div>
            </div>
            <button onclick="confirmPlanMeal('${meal.id}', '${meal.meal_type}', '${meal.recipe_name || 'Plan meal'}', ${meal.calories || 0}, ${meal.protein || 0}, ${meal.carbs || 0}, ${meal.fat || 0})"
                    class="btn-primary text-white px-4 py-2 rounded-xl font-bold text-sm touch-target">
                Comí esto
            </button>
        </div>
    `).join('');
}

async function confirmPlanMeal(planId, mealType, name, calories, protein, carbs, fat) {
    try {
        const token = user?.token;
        const res = await fetch(API_BASE + '/food-log', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + token
            },
            body: JSON.stringify({
                recipe_id: planId,
                food_name: name,
                meal_type: mealType,
                calories: calories,
                protein: protein,
                carbs: carbs,
                fat: fat,
                source: 'plan'
            })
        });
        
        const data = await res.json();
        
        if (res.ok) {
            showToast(`✅ ${name} registrado (${formatCalories(calories)} kcal)`, 'success');
            renderFoodModalMain();
            loadDashboard();
        } else {
            showToast('❌ ' + (data.error || 'Error al registrar'), 'error');
        }
    } catch (err) {
        showToast('❌ Error de conexión', 'error');
    }
}

// ==================== FOOD SEARCH ====================

function showFoodSearch() {
    const container = document.getElementById('food-content');
    
    container.innerHTML = `
        <div class="fade-in">
            <button onclick="renderFoodModalMain()" class="flex items-center gap-2 text-purple-500 font-semibold mb-4 touch-target">
                <i class="fas fa-arrow-left"></i> Volver
            </button>
            <h2 class="text-2xl font-black dark:text-white mb-2">🔍 Buscar comida</h2>
            <p class="text-gray-500 mb-6">Busca en recetas o productos (Open Food Facts)</p>
            
            <!-- Selector de tipo de comida -->
            <div class="mb-4">
                <label class="block text-sm font-semibold mb-2 dark:text-gray-200">Tipo de comida</label>
                <div class="flex flex-wrap gap-2">
                    ${['desayuno', 'comida', 'merienda', 'cena', 'snack'].map(meal => `
                        <button onclick="selectMealType('${meal}')" 
                                class="meal-type-btn px-4 py-2 rounded-xl font-semibold text-sm touch-target transition-all ${selectedMealType === meal ? 'btn-primary text-white' : 'glass dark:text-white'}">
                            ${meal === 'desayuno' ? '🌅' : meal === 'comida' ? '☀️' : meal === 'merienda' ? '🍎' : meal === 'cena' ? '🌙' : '🥨'} ${meal.charAt(0).toUpperCase() + meal.slice(1)}
                        </button>
                    `).join('')}
                </div>
            </div>
            
            <!-- Buscador -->
            <div class="relative mb-4">
                <input type="text" id="food-search-input" 
                       placeholder="Buscar alimento o producto..." 
                       class="w-full px-4 py-3 pl-12 rounded-xl border-2 border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 dark:text-white focus:border-purple-500 focus:outline-none touch-target"
                       oninput="debounceFoodSearch(this.value)">
                <i class="fas fa-search absolute left-4 top-1/2 -translate-y-1/2 text-gray-400"></i>
            </div>
            
            <!-- Tabs -->
            <div class="flex gap-2 mb-4">
                <button onclick="setSearchType('all')" id="tab-all" class="flex-1 py-2 rounded-xl font-semibold text-sm btn-primary text-white touch-target">
                    Todos
                </button>
                <button onclick="setSearchType('recipes')" id="tab-recipes" class="flex-1 py-2 rounded-xl font-semibold text-sm glass dark:text-white touch-target">
                    🥗 Recetas
                </button>
                <button onclick="setSearchType('products')" id="tab-products" class="flex-1 py-2 rounded-xl font-semibold text-sm glass dark:text-white touch-target">
                    📦 Productos
                </button>
            </div>
            
            <!-- Resultados -->
            <div id="food-results" class="space-y-3 max-h-[50vh] overflow-y-auto">
                <div class="text-center py-8 text-gray-500">
                    <i class="fas fa-search text-3xl mb-2"></i>
                    <p>Escribe para buscar</p>
                </div>
            </div>
        </div>
    `;
}

let searchType = 'all';
let searchTimeout = null;

function selectMealType(meal) {
    selectedMealType = meal;
    document.querySelectorAll('.meal-type-btn').forEach(btn => {
        if (btn.textContent.toLowerCase().includes(meal)) {
            btn.className = 'meal-type-btn px-4 py-2 rounded-xl font-semibold text-sm touch-target transition-all btn-primary text-white';
        } else {
            btn.className = 'meal-type-btn px-4 py-2 rounded-xl font-semibold text-sm touch-target transition-all glass dark:text-white';
        }
    });
}

function setSearchType(type) {
    searchType = type;
    ['all', 'recipes', 'products'].forEach(t => {
        const tab = document.getElementById('tab-' + t);
        if (tab) {
            if (t === type) {
                tab.className = 'flex-1 py-2 rounded-xl font-semibold text-sm btn-primary text-white touch-target';
            } else {
                tab.className = 'flex-1 py-2 rounded-xl font-semibold text-sm glass dark:text-white touch-target';
            }
        }
    });
    
    // Re-search with new type
    const input = document.getElementById('food-search-input');
    if (input && input.value.length >= 2) {
        searchFoodItems(input.value);
    }
}

function debounceFoodSearch(query) {
    clearTimeout(searchTimeout);
    searchTimeout = setTimeout(() => {
        searchFoodItems(query);
    }, 300);
}

async function searchFoodItems(query) {
    const resultsContainer = document.getElementById('food-results');
    
    if (!query || query.length < 2) {
        resultsContainer.innerHTML = `
            <div class="text-center py-8 text-gray-500">
                <i class="fas fa-search text-3xl mb-2"></i>
                <p>Escribe al menos 2 caracteres</p>
            </div>
        `;
        return;
    }
    
    resultsContainer.innerHTML = `
        <div class="text-center py-8">
            <div class="animate-spin w-8 h-8 border-4 border-purple-500 border-t-transparent rounded-full mx-auto mb-4"></div>
            <p class="text-gray-500">Buscando...</p>
        </div>
    `;
    
    try {
        const token = user?.token;
        const res = await fetch(API_BASE + '/search-food?q=' + encodeURIComponent(query) + '&type=' + searchType + '&limit=20', {
            headers: { 'Authorization': 'Bearer ' + token }
        });
        
        const data = await res.json();
        
        if (res.ok) {
            renderFoodResults(data);
        } else {
            resultsContainer.innerHTML = `
                <div class="text-center py-8 text-red-500">
                    <p>${data.error || 'Error al buscar'}</p>
                </div>
            `;
        }
    } catch (err) {
        console.error('Search error:', err);
        resultsContainer.innerHTML = `
            <div class="text-center py-8 text-red-500">
                <p>Error de conexión</p>
            </div>
        `;
    }
}

function renderFoodResults(data) {
    const container = document.getElementById('food-results');
    const recipes = data.recipes || [];
    const products = data.products || [];
    
    if (recipes.length === 0 && products.length === 0) {
        container.innerHTML = `
            <div class="text-center py-8 text-gray-500">
                <div class="text-4xl mb-2">🔍</div>
                <p>No se encontraron resultados</p>
            </div>
        `;
        return;
    }
    
    let html = '';
    
    // Recetas
    if (recipes.length > 0) {
        html += `<h4 class="font-bold dark:text-white text-sm mb-2">🥗 Recetas</h4>`;
        html += recipes.map(recipe => `
            <div class="glass-card rounded-xl p-4 flex items-center justify-between">
                <div class="flex-1">
                    <p class="font-bold dark:text-white">${recipe.name}</p>
                    <p class="text-sm text-gray-500">${formatCalories(recipe.calories)} kcal • P: ${formatGrams(recipe.protein)}g • C: ${formatGrams(recipe.carbs)}g • G: ${formatGrams(recipe.fat)}g</p>
                    ${recipe.meal_type ? `<span class="text-xs bg-purple-100 dark:bg-purple-900/30 text-purple-600 dark:text-purple-400 px-2 py-0.5 rounded-full capitalize">${recipe.meal_type}</span>` : ''}
                </div>
                <button onclick="showAddFoodModal('${recipe.id}', '${recipe.name.replace(/'/g, "\\'")}', ${recipe.calories || 0}, ${recipe.protein || 0}, ${recipe.carbs || 0}, ${recipe.fat || 0}, 'recipe')"
                        class="btn-primary text-white px-4 py-2 rounded-xl font-bold text-sm touch-target ml-3">
                    Añadir
                </button>
            </div>
        `).join('');
    }
    
    // Productos Open Food Facts
    if (products.length > 0) {
        html += `<h4 class="font-bold dark:text-white text-sm mb-2 mt-4">📦 Productos (Open Food Facts)</h4>`;
        html += products.map(product => `
            <div class="glass-card rounded-xl p-4 flex items-center justify-between">
                <div class="flex items-center gap-3 flex-1">
                    ${product.image ? `<img src="${product.image}" alt="${product.name}" class="w-12 h-12 rounded-lg object-cover">` : '<div class="w-12 h-12 bg-gray-200 dark:bg-gray-700 rounded-lg flex items-center justify-center text-xl">📦</div>'}
                    <div class="flex-1">
                        <p class="font-bold dark:text-white text-sm">${product.name || 'Unknown'}</p>
                        <p class="text-xs text-gray-500">${product.brand || ''} • ${formatCalories(product.calories || 0)} kcal/100g</p>
                    </div>
                </div>
                <button onclick="showAddFoodModal('${product.barcode || ''}', '${(product.name || 'Product').replace(/'/g, "\\'")}', ${product.calories || 0}, ${product.protein || 0}, ${product.carbs || 0}, ${product.fat || 0}, 'product', '${product.serving_size || '100g'}')"
                        class="btn-primary text-white px-4 py-2 rounded-xl font-bold text-sm touch-target ml-3">
                    Añadir
                </button>
            </div>
        `).join('');
    }
    
    container.innerHTML = html;
}

function showAddFoodModal(id, name, calories, protein, carbs, fat, type, servingSize = null) {
    if (!selectedMealType) {
        showToast('⚠️ Selecciona el tipo de comida primero', 'warning');
        return;
    }
    
    const container = document.getElementById('auth-modals');
    container.innerHTML = `
        <div class="fixed inset-0 z-[100] bg-black/60 backdrop-blur-sm flex items-center justify-center p-4" onclick="closeAddFoodModal(event)">
            <div class="glass-card bg-white dark:bg-gray-900 rounded-3xl max-w-md w-full p-6" onclick="event.stopPropagation()">
                <h3 class="text-xl font-bold dark:text-white mb-4">Añadir ${name}</h3>
                
                <div class="glass rounded-xl p-4 mb-4">
                    <p class="text-sm text-gray-500 mb-2">Info nutricional ${servingSize ? `(por ${servingSize})` : '(por ración)'}</p>
                    <div class="flex justify-around text-center">
                        <div>
                            <p class="text-xl font-black gradient-text">${formatCalories(calories)}</p>
                            <p class="text-xs text-gray-500">kcal</p>
                        </div>
                        <div>
                            <p class="text-lg font-bold dark:text-white">${formatGrams(protein)}g</p>
                            <p class="text-xs text-gray-500">Proteína</p>
                        </div>
                        <div>
                            <p class="text-lg font-bold dark:text-white">${formatGrams(carbs)}g</p>
                            <p class="text-xs text-gray-500">Carbos</p>
                        </div>
                        <div>
                            <p class="text-lg font-bold dark:text-white">${formatGrams(fat)}g</p>
                            <p class="text-xs text-gray-500">Grasa</p>
                        </div>
                    </div>
                </div>
                
                <div class="mb-4">
                    <label class="block text-sm font-semibold mb-2 dark:text-gray-200">Cantidad</label>
                    <div class="flex items-center gap-3">
                        <button onclick="adjustQuantity(-0.5)" class="w-10 h-10 glass rounded-xl font-bold dark:text-white touch-target">-</button>
                        <input type="number" id="food-quantity" value="1" min="0.5" max="10" step="0.5"
                               class="flex-1 px-4 py-2 rounded-xl border-2 border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 dark:text-white text-center font-bold touch-target">
                        <button onclick="adjustQuantity(0.5)" class="w-10 h-10 glass rounded-xl font-bold dark:text-white touch-target">+</button>
                    </div>
                    <p class="text-xs text-gray-500 mt-1 text-center" id="quantity-preview">${servingSize || '1 ración'}</p>
                </div>
                
                <div class="glass rounded-xl p-4 mb-4">
                    <div class="flex justify-between">
                        <span class="text-gray-500">Total:</span>
                        <span class="font-bold gradient-text" id="total-calories">${formatCalories(calories)} kcal</span>
                    </div>
                </div>
                
                <div class="flex gap-3">
                    <button onclick="closeAddFoodModal()" class="flex-1 glass py-3 rounded-xl font-bold dark:text-white touch-target">
                        Cancelar
                    </button>
                    <button onclick="confirmAddFood('${id}', '${name.replace(/'/g, "\\'")}', ${calories}, ${protein}, ${carbs}, ${fat}, '${type}')"
                            class="flex-1 btn-primary text-white py-3 rounded-xl font-bold touch-target">
                        Confirmar
                    </button>
                </div>
            </div>
        </div>
    `;
    
    // Setup quantity change listener
    const qtyInput = document.getElementById('food-quantity');
    if (qtyInput) {
        qtyInput.addEventListener('input', () => updateTotalCalories(calories));
    }
}

function adjustQuantity(delta) {
    const input = document.getElementById('food-quantity');
    if (input) {
        let value = parseFloat(input.value) || 1;
        value = Math.max(0.5, Math.min(10, value + delta));
        input.value = value;
        input.dispatchEvent(new Event('input'));
    }
}

function updateTotalCalories(baseCalories) {
    const qty = parseFloat(document.getElementById('food-quantity').value) || 1;
    const totalEl = document.getElementById('total-calories');
    if (totalEl) {
        totalEl.textContent = formatCalories(baseCalories * qty) + ' kcal';
    }
}

function closeAddFoodModal(event) {
    if (event && event.target !== event.currentTarget) return;
    document.getElementById('auth-modals').innerHTML = '';
}

async function confirmAddFood(id, name, calories, protein, carbs, fat, type) {
    const quantity = parseFloat(document.getElementById('food-quantity').value) || 1;
    
    try {
        const token = user?.token;
        const payload = {
            food_name: name,
            meal_type: selectedMealType || 'other',
            calories: calories,
            protein: protein,
            carbs: carbs,
            fat: fat,
            quantity: quantity,
            source: type === 'recipe' ? 'manual' : 'openfoodfacts'
        };
        
        if (type === 'recipe') {
            payload.recipe_id = id;
        } else if (type === 'product') {
            payload.barcode = id;
        }
        
        const res = await fetch(API_BASE + '/food-log', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + token
            },
            body: JSON.stringify(payload)
        });
        
        const data = await res.json();
        
        if (res.ok) {
            closeAddFoodModal();
            showToast(`✅ ${name} añadido (${formatCalories(calories * quantity)} kcal)`, 'success');
            renderFoodModalMain();
            loadDashboard();
        } else {
            showToast('❌ ' + (data.error || 'Error al registrar'), 'error');
        }
    } catch (err) {
        showToast('❌ Error de conexión', 'error');
    }
}

function showBarcodeScanner() {
    showToast('📷 Escáner de códigos próximamente', 'info');
}

// ==================== WEIGHT MODAL ====================

function openWeightModal() {
    const container = document.getElementById('auth-modals');
    container.innerHTML = `
        <div class="fixed inset-0 z-[100] bg-black/60 backdrop-blur-sm flex items-center justify-center p-4" onclick="closeWeightModal(event)">
            <div class="glass-card bg-white dark:bg-gray-900 rounded-3xl max-w-md w-full p-8 relative slide-enter" onclick="event.stopPropagation()">
                <button onclick="closeWeightModal()" class="absolute top-4 right-4 touch-target w-10 h-10 rounded-full bg-gray-100 dark:bg-gray-800 flex items-center justify-center">
                    <i class="fas fa-times"></i>
                </button>
                <div class="text-center mb-8">
                    <div class="w-16 h-16 bg-gradient-to-br from-green-500 to-emerald-500 rounded-2xl flex items-center justify-center text-3xl mx-auto mb-4">⚖️</div>
                    <h2 class="text-2xl font-black mb-2 dark:text-white">Registrar peso</h2>
                    <p class="text-gray-600 dark:text-gray-400">Actualiza tu peso actual</p>
                </div>
                <form onsubmit="handleWeightSubmit(event)">
                    <div class="mb-6">
                        <label class="block text-sm font-semibold mb-2 dark:text-gray-200">Peso (kg)</label>
                        <input type="number" id="weight-input" step="0.1" min="30" max="300" required 
                               class="w-full px-4 py-3 rounded-xl border-2 border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 dark:text-white focus:border-green-500 focus:outline-none touch-target">
                    </div>
                    <button type="submit" class="btn-primary w-full text-white py-3 rounded-xl font-bold text-lg touch-target">
                        Guardar peso
                    </button>
                </form>
            </div>
        </div>
    `;
    document.body.style.overflow = 'hidden';
}

function closeWeightModal(event) {
    if (event && event.target !== event.currentTarget) return;
    document.getElementById('auth-modals').innerHTML = '';
    document.body.style.overflow = '';
}

async function handleWeightSubmit(e) {
    e.preventDefault();
    const weight = parseFloat(document.getElementById('weight-input').value);
    
    if (!weight || weight < 30 || weight > 300) {
        showToast('❌ Peso inválido (30-300 kg)', 'error');
        return;
    }
    
    showToast('Registrando peso...', 'info');
    
    try {
        const token = user.token;
        const res = await fetch(API_BASE + '/weight', {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + token
            },
            body: JSON.stringify({ weight: weight })
        });
        
        const data = await res.json();
        
        if (res.ok) {
            closeWeightModal();
            showToast('✅ Peso registrado: ' + weight + ' kg', 'success');
            // Reload dashboard to show updated data
            loadDashboard();
        } else {
            showToast('❌ ' + (data.error || 'Error al registrar peso'), 'error');
        }
    } catch (err) {
        showToast('❌ Error de conexión', 'error');
        console.error('Weight error:', err);
    }
}

// ==================== SHOPPING LIST ====================

let shoppingListData = null;

async function showShoppingList() {
    // Verificar que el usuario está logueado
    if (!user || !user.token) {
        showToast('❌ Debes iniciar sesión para ver la lista de compras', 'error');
        showModal('login');
        return;
    }
    
    showToast('Cargando lista de compras...', 'info');
    
    try {
        const token = user.token;
        const res = await fetch(API_BASE + '/shopping-list', {
            headers: { 
                'Authorization': 'Bearer ' + token
            }
        });
        
        const data = await res.json();
        
        if (res.ok) {
            shoppingListData = data;
            renderShoppingListUI(data);
        } else {
            showToast('❌ ' + (data.error || 'Error al cargar lista'), 'error');
        }
    } catch (err) {
        showToast('❌ Error de conexión', 'error');
        console.error('Shopping list error:', err);
    }
}

function renderShoppingListUI(data) {
    const container = document.getElementById('auth-modals');
    const grouped = data.grouped || {};
    const totalItems = data.total_items || 0;
    
    const supermarketIcons = {
        'mercadona': '🟢',
        'lidl': '🔵',
        'carrefour': '🔴',
        'generic': '📦',
        'manual': '✍️'
    };
    
    const supermarketColors = {
        'mercadona': 'from-green-500 to-emerald-600',
        'lidl': 'from-blue-500 to-blue-600',
        'carrefour': 'from-red-500 to-red-600',
        'generic': 'from-gray-500 to-gray-600',
        'manual': 'from-purple-500 to-purple-600'
    };
    
    container.innerHTML = `
        <div class="fixed inset-0 z-[100] bg-black/60 backdrop-blur-sm flex items-center justify-center p-4" onclick="closeShoppingList(event)">
            <div class="glass-card bg-white dark:bg-gray-900 rounded-3xl max-w-3xl w-full max-h-[90vh] overflow-hidden flex flex-col" onclick="event.stopPropagation()">
                <!-- Header -->
                <div class="p-4 sm:p-6 border-b border-gray-200 dark:border-gray-700">
                    <div class="flex items-center justify-between">
                        <div class="flex items-center gap-3">
                            <div class="w-12 h-12 bg-gradient-to-br from-orange-500 to-red-500 rounded-xl flex items-center justify-center text-2xl">🛒</div>
                            <div>
                                <h2 class="text-xl font-black dark:text-white">Lista de Compras</h2>
                                <p class="text-sm text-gray-500">Semana ${data.week_number || '--'} • ${totalItems} ingredientes</p>
                            </div>
                        </div>
                        <button onclick="closeShoppingList()" class="touch-target w-10 h-10 rounded-full bg-gray-100 dark:bg-gray-800 flex items-center justify-center">
                            <i class="fas fa-times"></i>
                        </button>
                    </div>
                    
                    <!-- Action buttons -->
                    <div class="flex gap-2 mt-4 overflow-x-auto pb-2">
                        <button onclick="showAddItemModal()" class="flex-shrink-0 btn-primary text-white px-4 py-2 rounded-xl font-bold text-sm touch-target flex items-center gap-2">
                            <i class="fas fa-plus"></i> Añadir
                        </button>
                        <button onclick="exportList('text')" class="flex-shrink-0 glass px-4 py-2 rounded-xl font-bold text-sm dark:text-white touch-target flex items-center gap-2">
                            <i class="fas fa-copy"></i> Copiar
                        </button>
                        <button onclick="exportList('whatsapp')" class="flex-shrink-0 glass px-4 py-2 rounded-xl font-bold text-sm dark:text-white touch-target flex items-center gap-2">
                            <i class="fab fa-whatsapp"></i> WhatsApp
                        </button>
                        <button onclick="confirmClearList()" class="flex-shrink-0 glass px-4 py-2 rounded-xl font-bold text-sm text-red-500 touch-target flex items-center gap-2">
                            <i class="fas fa-trash"></i> Limpiar
                        </button>
                    </div>
                </div>
                
                <!-- Content -->
                <div class="flex-1 overflow-y-auto p-4 sm:p-6">
                    ${totalItems === 0 ? `
                        <div class="text-center py-12">
                            <div class="text-6xl mb-4">🛒</div>
                            <p class="text-gray-600 dark:text-gray-400 mb-4">No hay ingredientes para esta semana</p>
                            <p class="text-sm text-gray-500">Genera un plan semanal primero</p>
                        </div>
                    ` : `
                        <div class="space-y-6">
                            ${Object.entries(grouped).filter(([_, items]) => items.length > 0).map(([supermarket, items]) => `
                                <div class="glass rounded-2xl overflow-hidden">
                                    <div class="bg-gradient-to-r ${supermarketColors[supermarket] || 'from-gray-500 to-gray-600'} px-4 py-3 flex items-center justify-between">
                                        <div class="flex items-center gap-2 text-white">
                                            <span class="text-xl">${supermarketIcons[supermarket] || '📦'}</span>
                                            <span class="font-bold capitalize">${supermarket}</span>
                                        </div>
                                        <span class="bg-white/20 px-2 py-1 rounded-lg text-sm text-white font-medium">${items.length} items</span>
                                    </div>
                                    <ul class="divide-y divide-gray-100 dark:divide-gray-800">
                                        ${items.map((item, idx) => `
                                            <li class="flex items-center gap-3 p-4 hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors" data-item-idx="${idx}" data-supermarket="${supermarket}">
                                                <input type="checkbox" 
                                                       id="item-${supermarket}-${idx}"
                                                       ${item.checked ? 'checked' : ''}
                                                       onchange="toggleItemChecked('${supermarket}', ${idx}, this.checked)"
                                                       class="w-5 h-5 rounded border-gray-300 text-purple-500 focus:ring-purple-500 cursor-pointer">
                                                <label for="item-${supermarket}-${idx}" class="flex-1 cursor-pointer">
                                                    <span class="dark:text-white ${item.checked ? 'line-through text-gray-400' : ''}">${item.name || item}</span>
                                                    ${item.amount && item.unit ? `<span class="text-sm text-gray-500 ml-2">(${item.amount} ${item.unit})</span>` : ''}
                                                    ${item.recipes && item.recipes.length > 0 ? `<span class="block text-xs text-gray-400 mt-1">📌 ${item.recipes.join(', ')}</span>` : ''}
                                                </label>
                                                ${item.id ? `
                                                    <button onclick="deleteShoppingItem('${item.id}')" class="text-red-400 hover:text-red-600 p-2 touch-target">
                                                        <i class="fas fa-trash text-sm"></i>
                                                    </button>
                                                ` : ''}
                                            </li>
                                        `).join('')}
                                    </ul>
                                </div>
                            `).join('')}
                        </div>
                    `}
                </div>
                
                <!-- Footer summary -->
                ${totalItems > 0 ? `
                    <div class="p-4 border-t border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800/50">
                        <div class="flex justify-between text-sm text-gray-600 dark:text-gray-400">
                            <span>Total ingredientes: ${totalItems}</span>
                            <span>Recetas: ${data.recipe_count || 0}</span>
                        </div>
                    </div>
                ` : ''}
            </div>
        </div>
    `;
    document.body.style.overflow = 'hidden';
}

function closeShoppingList(event) {
    if (event && event.target !== event.currentTarget) return;
    document.getElementById('auth-modals').innerHTML = '';
    document.body.style.overflow = '';
}

function showAddItemModal() {
    const container = document.getElementById('auth-modals');
    const existingContent = container.innerHTML;
    
    container.innerHTML = `
        <div class="fixed inset-0 z-[110] bg-black/60 backdrop-blur-sm flex items-center justify-center p-4">
            <div class="glass-card bg-white dark:bg-gray-900 rounded-3xl max-w-md w-full p-6 slide-enter">
                <div class="flex items-center justify-between mb-6">
                    <h3 class="text-xl font-black dark:text-white">Añadir ingrediente</h3>
                    <button onclick="renderShoppingListUI(shoppingListData)" class="touch-target w-10 h-10 rounded-full bg-gray-100 dark:bg-gray-800 flex items-center justify-center">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
                <form onsubmit="addShoppingItem(event)">
                    <div class="space-y-4">
                        <div>
                            <label class="block text-sm font-semibold mb-2 dark:text-gray-200">Ingrediente *</label>
                            <input type="text" id="new-item-name" required placeholder="Ej: Leche entera"
                                   class="w-full px-4 py-3 rounded-xl border-2 border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 dark:text-white focus:border-purple-500 focus:outline-none touch-target">
                        </div>
                        <div class="grid grid-cols-2 gap-4">
                            <div>
                                <label class="block text-sm font-semibold mb-2 dark:text-gray-200">Cantidad</label>
                                <input type="number" id="new-item-amount" placeholder="1" min="0.1" step="0.1"
                                       class="w-full px-4 py-3 rounded-xl border-2 border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 dark:text-white focus:border-purple-500 focus:outline-none touch-target">
                            </div>
                            <div>
                                <label class="block text-sm font-semibold mb-2 dark:text-gray-200">Unidad</label>
                                <select id="new-item-unit" class="w-full px-4 py-3 rounded-xl border-2 border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 dark:text-white focus:border-purple-500 focus:outline-none touch-target">
                                    <option value="unidad">unidad</option>
                                    <option value="kg">kg</option>
                                    <option value="g">g</option>
                                    <option value="l">litro</option>
                                    <option value="ml">ml</option>
                                    <option value="docena">docena</option>
                                    <option value="bote">bote</option>
                                    <option value="lata">lata</option>
                                    <option value="paquete">paquete</option>
                                </select>
                            </div>
                        </div>
                        <div>
                            <label class="block text-sm font-semibold mb-2 dark:text-gray-200">Supermercado</label>
                            <select id="new-item-supermarket" class="w-full px-4 py-3 rounded-xl border-2 border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 dark:text-white focus:border-purple-500 focus:outline-none touch-target">
                                <option value="manual">Manual</option>
                                <option value="mercadona">Mercadona</option>
                                <option value="lidl">Lidl</option>
                                <option value="carrefour">Carrefour</option>
                                <option value="generic">Otros</option>
                            </select>
                        </div>
                    </div>
                    <div class="flex gap-3 mt-6">
                        <button type="button" onclick="renderShoppingListUI(shoppingListData)" class="flex-1 py-3 rounded-xl font-bold border-2 border-gray-200 dark:border-gray-700 dark:text-white touch-target">
                            Cancelar
                        </button>
                        <button type="submit" class="flex-1 btn-primary text-white py-3 rounded-xl font-bold touch-target">
                            Añadir
                        </button>
                    </div>
                </form>
            </div>
        </div>
    `;
}

async function addShoppingItem(e) {
    e.preventDefault();
    
    const name = document.getElementById('new-item-name').value.trim();
    const amount = document.getElementById('new-item-amount').value || 1;
    const unit = document.getElementById('new-item-unit').value;
    const supermarket = document.getElementById('new-item-supermarket').value;
    
    if (!name) {
        showToast('❌ Ingresa el nombre del ingrediente', 'error');
        return;
    }
    
    showToast('Añadiendo...', 'info');
    
    try {
        const token = user.token;
        const res = await fetch(API_BASE + '/shopping-list/item', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + token
            },
            body: JSON.stringify({
                name: name,
                amount: parseFloat(amount),
                unit: unit,
                supermarket: supermarket
            })
        });
        
        const data = await res.json();
        
        if (res.ok) {
            showToast('✅ Ingrediente añadido', 'success');
            // Reload list
            showShoppingList();
        } else {
            showToast('❌ ' + (data.error || 'Error al añadir'), 'error');
        }
    } catch (err) {
        showToast('❌ Error de conexión', 'error');
        console.error('Add item error:', err);
    }
}

function toggleItemChecked(supermarket, idx, checked) {
    // Visual feedback
    const item = document.querySelector(`[data-item-idx="${idx}"][data-supermarket="${supermarket}"] label span`);
    if (item) {
        if (checked) {
            item.classList.add('line-through', 'text-gray-400');
        } else {
            item.classList.remove('line-through', 'text-gray-400');
        }
    }
    
    // If has ID, update in backend
    const items = shoppingListData?.grouped?.[supermarket] || [];
    if (items[idx] && items[idx].id) {
        updateShoppingItem(items[idx].id, { checked: checked });
    }
}

async function updateShoppingItem(itemId, updates) {
    try {
        const token = user.token;
        await fetch(API_BASE + '/shopping-list/item/' + itemId, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + token
            },
            body: JSON.stringify(updates)
        });
    } catch (err) {
        console.error('Update item error:', err);
    }
}

async function deleteShoppingItem(itemId) {
    if (!confirm('¿Eliminar este ingrediente?')) return;
    
    showToast('Eliminando...', 'info');
    
    try {
        const token = user.token;
        const res = await fetch(API_BASE + '/shopping-list/item/' + itemId, {
            method: 'DELETE',
            headers: {
                'Authorization': 'Bearer ' + token
            }
        });
        
        if (res.ok) {
            showToast('✅ Ingrediente eliminado', 'success');
            showShoppingList();
        } else {
            const data = await res.json();
            showToast('❌ ' + (data.error || 'Error al eliminar'), 'error');
        }
    } catch (err) {
        showToast('❌ Error de conexión', 'error');
        console.error('Delete item error:', err);
    }
}

function confirmClearList() {
    if (!confirm('¿Eliminar todos los ingredientes manuales de la lista?')) return;
    clearShoppingList();
}

async function clearShoppingList() {
    showToast('Limpiando lista...', 'info');
    
    try {
        const token = user.token;
        const res = await fetch(API_BASE + '/shopping-list/clear', {
            method: 'DELETE',
            headers: {
                'Authorization': 'Bearer ' + token
            }
        });
        
        if (res.ok) {
            showToast('✅ Lista limpiada', 'success');
            showShoppingList();
        } else {
            const data = await res.json();
            showToast('❌ ' + (data.error || 'Error al limpiar'), 'error');
        }
    } catch (err) {
        showToast('❌ Error de conexión', 'error');
        console.error('Clear list error:', err);
    }
}

async function exportList(format) {
    showToast('Generando lista...', 'info');
    
    try {
        const token = user.token;
        const res = await fetch(API_BASE + '/shopping-list/export?format=' + format, {
            headers: {
                'Authorization': 'Bearer ' + token
            }
        });
        
        const data = await res.json();
        
        if (res.ok) {
            // Copy to clipboard
            await navigator.clipboard.writeText(data.text);
            
            if (format === 'whatsapp') {
                showToast('✅ Lista copiada (formato WhatsApp)', 'success');
            } else {
                showToast('✅ Lista copiada al portapapeles', 'success');
            }
        } else {
            showToast('❌ ' + (data.error || 'Error al exportar'), 'error');
        }
    } catch (err) {
        showToast('❌ Error de conexión', 'error');
        console.error('Export list error:', err);
    }
}

function printShoppingList() {
    window.print();
}

// ==================== PROFILE PAGE ====================

async function showProfile() {
    // Verificar que el usuario está logueado
    if (!user || !user.token) {
        showToast('❌ Debes iniciar sesión para ver tu perfil', 'error');
        showModal('login');
        return;
    }
    
    showToast('Cargando perfil...', 'info');
    
    try {
        const token = user.token;
        const res = await fetch(API_BASE + '/profile', {
            headers: { 
                'Authorization': 'Bearer ' + token
            }
        });
        
        const data = await res.json();
        
        if (res.ok) {
            const container = document.getElementById('auth-modals');
            container.innerHTML = `
                <div class="fixed inset-0 z-[100] bg-black/60 backdrop-blur-sm flex items-center justify-center p-4" onclick="closeProfile(event)">
                    <div class="glass-card bg-white dark:bg-gray-900 rounded-3xl max-w-2xl w-full max-h-[80vh] overflow-hidden flex flex-col" onclick="event.stopPropagation()">
                        <div class="p-6 border-b border-gray-200 dark:border-gray-700 flex items-center justify-between">
                            <div class="flex items-center gap-3">
                                <div class="w-12 h-12 bg-gradient-to-br from-purple-500 to-blue-500 rounded-full flex items-center justify-center text-xl font-bold text-white">
                                    ${(user.name || 'U')[0].toUpperCase()}
                                </div>
                                <div>
                                    <h2 class="text-xl font-black dark:text-white">Mi Perfil</h2>
                                    <p class="text-sm text-gray-500">${user.email}</p>
                                </div>
                            </div>
                            <button onclick="closeProfile()" class="touch-target w-10 h-10 rounded-full bg-gray-100 dark:bg-gray-800 flex items-center justify-center">
                                <i class="fas fa-times"></i>
                            </button>
                        </div>
                        <div class="p-6 overflow-y-auto flex-1">
                            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-6">
                                <div class="glass rounded-xl p-4">
                                    <p class="text-sm text-gray-500 mb-1">Edad</p>
                                    <p class="text-2xl font-black dark:text-white">${data.age || '--'}</p>
                                </div>
                                <div class="glass rounded-xl p-4">
                                    <p class="text-sm text-gray-500 mb-1">Género</p>
                                    <p class="text-2xl font-black dark:text-white">${data.gender ? (data.gender === 'male' ? 'Hombre' : 'Mujer') : '--'}</p>
                                </div>
                                <div class="glass rounded-xl p-4">
                                    <p class="text-sm text-gray-500 mb-1">Altura</p>
                                    <p class="text-2xl font-black dark:text-white">${data.height || '--'} cm</p>
                                </div>
                                <div class="glass rounded-xl p-4">
                                    <p class="text-sm text-gray-500 mb-1">Peso actual</p>
                                    <p class="text-2xl font-black dark:text-white">${data.current_weight || '--'} kg</p>
                                </div>
                                <div class="glass rounded-xl p-4">
                                    <p class="text-sm text-gray-500 mb-1">Peso objetivo</p>
                                    <p class="text-2xl font-black dark:text-white">${data.goal_weight || '--'} kg</p>
                                </div>
                                <div class="glass rounded-xl p-4">
                                    <p class="text-sm text-gray-500 mb-1">Objetivo</p>
                                    <p class="text-lg font-bold dark:text-white">${data.goal_type ? (data.goal_type === 'lose' ? 'Perder peso' : data.goal_type === 'gain' ? 'Ganar músculo' : 'Mantener') : '--'}</p>
                                </div>
                                <div class="glass rounded-xl p-4">
                                    <p class="text-sm text-gray-500 mb-1">Actividad</p>
                                    <p class="text-lg font-bold dark:text-white">${data.activity_level ? data.activity_level.replace('_', ' ') : '--'}</p>
                                </div>
                                <div class="glass rounded-xl p-4">
                                    <p class="text-sm text-gray-500 mb-1">Comidas/día</p>
                                    <p class="text-2xl font-black dark:text-white">${data.meals_per_day || '--'}</p>
                                </div>
                            </div>
                            
                            <div class="glass-card rounded-xl p-4 mb-4">
                                <h3 class="font-bold dark:text-white mb-3">📊 Métricas</h3>
                                <div class="grid grid-cols-3 gap-4">
                                    <div class="text-center">
                                        <p class="text-xs text-gray-500 mb-1">TMB</p>
                                        <p class="text-lg font-black gradient-text">${data.tmb || '--'} kcal</p>
                                    </div>
                                    <div class="text-center">
                                        <p class="text-xs text-gray-500 mb-1">TDEE</p>
                                        <p class="text-lg font-black gradient-text">${data.tdee || '--'} kcal</p>
                                    </div>
                                    <div class="text-center">
                                        <p class="text-xs text-gray-500 mb-1">Objetivo</p>
                                        <p class="text-lg font-black gradient-text">${data.target_calories || '--'} kcal</p>
                                    </div>
                                </div>
                            </div>
                            
                            ${(data.allergies || data.disliked_foods) ? `
                                <div class="glass-card rounded-xl p-4">
                                    <h3 class="font-bold dark:text-white mb-3">⚠️ Preferencias</h3>
                                    ${data.allergies ? `<p class="text-sm dark:text-gray-300 mb-2"><strong>Alergias:</strong> ${data.allergies}</p>` : ''}
                                    ${data.disliked_foods ? `<p class="text-sm dark:text-gray-300"><strong>Comidas que no me gustan:</strong> ${data.disliked_foods}</p>` : ''}
                                </div>
                            ` : ''}
                        </div>
                        <div class="p-4 border-t border-gray-200 dark:border-gray-700">
                            <button onclick="closeProfile()" class="w-full btn-primary text-white py-3 rounded-xl font-bold touch-target">
                                Cerrar
                            </button>
                        </div>
                    </div>
                </div>
            `;
            document.body.style.overflow = 'hidden';
        } else {
            showToast('❌ ' + (data.error || 'Error al cargar perfil'), 'error');
        }
    } catch (err) {
        showToast('❌ Error de conexión', 'error');
        console.error('Profile error:', err);
    }
}

function closeProfile(event) {
    if (event && event.target !== event.currentTarget) return;
    document.getElementById('auth-modals').innerHTML = '';
    document.body.style.overflow = '';
}

// ==================== SETTINGS PAGE ====================

function showSettings() {
    const container = document.getElementById('auth-modals');
    container.innerHTML = `
        <div class="fixed inset-0 z-[100] bg-black/60 backdrop-blur-sm flex items-center justify-center p-4" onclick="closeSettings(event)">
            <div class="glass-card bg-white dark:bg-gray-900 rounded-3xl max-w-md w-full" onclick="event.stopPropagation()">
                <div class="p-6 border-b border-gray-200 dark:border-gray-700 flex items-center justify-between">
                    <div class="flex items-center gap-3">
                        <div class="w-12 h-12 bg-gradient-to-br from-gray-500 to-gray-700 rounded-xl flex items-center justify-center text-2xl">⚙️</div>
                        <div>
                            <h2 class="text-xl font-black dark:text-white">Configuración</h2>
                            <p class="text-sm text-gray-500">Preferencias de la app</p>
                        </div>
                    </div>
                    <button onclick="closeSettings()" class="touch-target w-10 h-10 rounded-full bg-gray-100 dark:bg-gray-800 flex items-center justify-center">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
                <div class="p-6 space-y-4">
                    <button onclick="toggleDark(); closeSettings()" class="w-full glass p-4 rounded-xl flex items-center justify-between touch-target">
                        <div class="flex items-center gap-3">
                            <span class="text-2xl">${isDark ? '☀️' : '🌙'}</span>
                            <div class="text-left">
                                <p class="font-bold dark:text-white">Modo oscuro</p>
                                <p class="text-sm text-gray-500">${isDark ? 'Activado' : 'Desactivado'}</p>
                            </div>
                        </div>
                        <div class="w-12 h-6 bg-gray-300 dark:bg-purple-500 rounded-full relative transition-colors">
                            <div class="w-5 h-5 bg-white rounded-full absolute top-0.5 ${isDark ? 'right-0.5' : 'left-0.5'} transition-all"></div>
                        </div>
                    </button>
                    
                    <button onclick="showProfile(); closeSettings()" class="w-full glass p-4 rounded-xl flex items-center gap-3 touch-target">
                        <span class="text-2xl">👤</span>
                        <div class="text-left">
                            <p class="font-bold dark:text-white">Mi perfil</p>
                            <p class="text-sm text-gray-500">Ver mis datos y métricas</p>
                        </div>
                    </button>
                    
                    <button onclick="exportData()" class="w-full glass p-4 rounded-xl flex items-center gap-3 touch-target">
                        <span class="text-2xl">📥</span>
                        <div class="text-left">
                            <p class="font-bold dark:text-white">Exportar datos</p>
                            <p class="text-sm text-gray-500">Descargar mi progreso</p>
                        </div>
                    </button>
                    
                    <div class="border-t border-gray-200 dark:border-gray-700 pt-4">
                        <button onclick="logout(); closeSettings()" class="w-full glass p-4 rounded-xl flex items-center gap-3 touch-target hover:bg-red-50 dark:hover:bg-red-900/20 transition-colors">
                            <span class="text-2xl">🚪</span>
                            <div class="text-left">
                                <p class="font-bold text-red-500">Cerrar sesión</p>
                                <p class="text-sm text-gray-500">Salir de tu cuenta</p>
                            </div>
                        </button>
                    </div>
                </div>
            </div>
        </div>
    `;
    document.body.style.overflow = 'hidden';
}

function closeSettings(event) {
    if (event && event.target !== event.currentTarget) return;
    document.getElementById('auth-modals').innerHTML = '';
    document.body.style.overflow = '';
}

function exportData() {
    showToast('📥 Preparando exportación...', 'info');
    // TODO: Implement data export
    setTimeout(() => {
        showToast('✅ Datos exportados (próximamente)', 'success');
    }, 1000);
}

// ==================== TOAST NOTIFICATIONS MEJORADOS ====================

function showToast(message, type = 'info', duration = 3000) {
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');
    
    const config = {
        success: { 
            icon: '✓', 
            class: 'toast-success',
            ariaLabel: 'Éxito'
        },
        error: { 
            icon: '✕', 
            class: 'toast-error',
            ariaLabel: 'Error'
        },
        info: { 
            icon: 'ℹ', 
            class: 'toast-info',
            ariaLabel: 'Información'
        },
        warning: { 
            icon: '⚠', 
            class: 'toast-warning',
            ariaLabel: 'Advertencia'
        }
    };
    
    const toastConfig = config[type] || config.info;
    
    toast.className = `toast ${toastConfig.class} slide-up`;
    toast.setAttribute('role', 'alert');
    toast.setAttribute('aria-live', 'polite');
    toast.innerHTML = `
        <span class="text-xl font-bold" aria-hidden="true">${toastConfig.icon}</span>
        <span class="font-medium flex-1">${message}</span>
        <button onclick="this.parentElement.remove()" class="touch-target w-8 h-8 rounded-lg hover:bg-black/10 flex items-center justify-center" aria-label="Cerrar notificación">
            <i class="fas fa-times text-sm"></i>
        </button>
    `;
    
    container.appendChild(toast);
    
    // Auto-remove after duration
    const timeoutId = setTimeout(() => {
        toast.style.transition = 'opacity 0.3s, transform 0.3s';
        toast.style.opacity = '0';
        toast.style.transform = 'translateX(100%)';
        setTimeout(() => toast.remove(), 300);
    }, duration);
    
    // Store timeout for manual cleanup if needed
    toast.dataset.timeoutId = timeoutId;
    
    // Limit toasts to max 5 visible
    const toasts = container.querySelectorAll('.toast');
    if (toasts.length > 5) {
        const oldest = toasts[0];
        clearTimeout(oldest.dataset.timeoutId);
        oldest.remove();
    }
}

// ==================== LOADING SKELETONS ====================

function showSkeleton(containerId, type = 'card', count = 3) {
    const container = document.getElementById(containerId);
    if (!container) return;
    
    let skeletonHTML = '';
    
    switch(type) {
        case 'card':
            skeletonHTML = Array(count).fill(`
                <div class="glass-card rounded-2xl p-6">
                    <div class="flex items-center gap-4 mb-4">
                        <div class="skeleton skeleton-circle"></div>
                        <div class="flex-1">
                            <div class="skeleton skeleton-title"></div>
                        </div>
                    </div>
                    <div class="space-y-2">
                        <div class="skeleton skeleton-text"></div>
                        <div class="skeleton skeleton-text"></div>
                        <div class="skeleton skeleton-text" style="width: 60%"></div>
                    </div>
                </div>
            `).join('');
            break;
        case 'list':
            skeletonHTML = Array(count).fill(`
                <div class="glass-card rounded-xl p-4 flex items-center gap-4">
                    <div class="skeleton skeleton-circle"></div>
                    <div class="flex-1">
                        <div class="skeleton skeleton-title" style="height: 1rem; width: 80%"></div>
                        <div class="skeleton skeleton-text" style="height: 0.75rem; width: 60%"></div>
                    </div>
                </div>
            `).join('');
            break;
        case 'table':
            skeletonHTML = `
                <div class="glass-card rounded-2xl overflow-hidden">
                    <div class="p-4 border-b border-gray-200 dark:border-gray-700">
                        <div class="skeleton skeleton-title"></div>
                    </div>
                    ${Array(count).fill(`
                        <div class="p-4 border-b border-gray-200 dark:border-gray-700 flex gap-4">
                            <div class="skeleton skeleton-text flex-1"></div>
                            <div class="skeleton skeleton-text flex-1"></div>
                            <div class="skeleton skeleton-text flex-1"></div>
                        </div>
                    `).join('')}
                </div>
            `;
            break;
        default:
            skeletonHTML = `<div class="skeleton skeleton-card"></div>`;
    }
    
    container.innerHTML = skeletonHTML;
}

function hideSkeleton(containerId) {
    const container = document.getElementById(containerId);
    if (container) {
        container.querySelectorAll('.skeleton').forEach(el => el.remove());
    }
}

// ==================== LOADING OVERLAY ====================

function showLoadingOverlay(message = 'Cargando...') {
    const overlay = document.getElementById('loading-overlay');
    if (overlay) {
        overlay.querySelector('p').textContent = message;
        overlay.classList.remove('hidden');
        document.body.style.overflow = 'hidden';
    }
}

function hideLoadingOverlay() {
    const overlay = document.getElementById('loading-overlay');
    if (overlay) {
        overlay.classList.add('hidden');
        document.body.style.overflow = '';
    }
}
