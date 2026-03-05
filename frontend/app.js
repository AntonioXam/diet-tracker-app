// Diet Tracker FIT - Frontend Completo
// API Base URL
const API_BASE = 'https://diet-tracker-app-chi.vercel.app/api';

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

function toggleMobileMenu() {
    const menu = document.getElementById('mobile-menu');
    menu.classList.toggle('hidden');
}

function scrollToSection(id) {
    const element = document.getElementById(id);
    if (element) {
        element.scrollIntoView({ behavior: 'smooth' });
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
    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;
    
    showToast('Iniciando sesión...', 'info');
    
    try {
        const res = await fetch(API_BASE + '/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email: email, password: password })
        });
        
        const data = await res.json();
        
        if (res.ok) {
            user = data.user;
            localStorage.setItem('user', JSON.stringify(user));
            document.getElementById('auth-modals').innerHTML = '';
            document.body.style.overflow = '';
            showToast('¡Bienvenido!', 'success');
            checkAuth();
        } else {
            showToast(data.error || 'Error al iniciar sesión', 'error');
        }
    } catch (err) {
        showToast('Error de conexión', 'error');
        console.error(err);
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
        
        if (res.ok) {
            user = data.user;
            localStorage.setItem('user', JSON.stringify(user));
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
    const email = document.getElementById('forgot-email').value;
    
    showToast('📧 Email enviado', 'success');
    document.getElementById('auth-modals').innerHTML = '';
    document.body.style.overflow = '';
}

function checkAuth() {
    const saved = localStorage.getItem('user');
    
    if (saved) {
        user = JSON.parse(saved);
        
        // Show dashboard
        document.getElementById('main-content').classList.add('hidden');
        document.getElementById('dashboard-content').classList.remove('hidden');
        
        // Update nav
        document.getElementById('nav-auth').classList.add('hidden');
        document.getElementById('nav-auth').classList.remove('flex');
        document.getElementById('nav-user').classList.remove('hidden');
        document.getElementById('nav-user').classList.add('flex');
        
        document.getElementById('user-name').textContent = user.name || user.email;
        document.getElementById('user-avatar').textContent = (user.name || 'U')[0].toUpperCase();
        
        showToast('✅ Sesión iniciada', 'success');
        
        // Load dashboard
        loadDashboard();
    } else {
        // Show landing
        document.getElementById('main-content').classList.remove('hidden');
        document.getElementById('dashboard-content').classList.add('hidden');
        
        // Update nav
        document.getElementById('nav-auth').classList.remove('hidden');
        document.getElementById('nav-auth').classList.add('flex');
        document.getElementById('nav-user').classList.add('hidden');
        document.getElementById('nav-user').classList.remove('flex');
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
    dashboard.innerHTML = `
        <div class="flex items-center justify-center min-h-[60vh]">
            <div class="text-center">
                <div class="w-16 h-16 border-4 border-purple-500 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
                <p class="font-bold dark:text-white">Cargando tu dashboard...</p>
            </div>
        </div>
    `;
    
    try {
        // Load user plan
        const userId = user.id || user.token;
        const planRes = await fetch(API_BASE + '/plan/current?user_id=' + userId, {
            headers: { 'Authorization': 'Bearer ' + user.token }
        });
        
        if (!planRes.ok) throw new Error('Error cargando plan');
        
        currentPlan = await planRes.json();
        
        // Load weight history
        const historyRes = await fetch(API_BASE + '/weight/history?user_id=' + userId, {
            headers: { 'Authorization': 'Bearer ' + user.token }
        });
        
        const history = historyRes.ok ? await historyRes.json() : [];
        
        renderDashboard(currentPlan, history);
        
    } catch (err) {
        console.error('Error loading dashboard:', err);
        showToast('Error cargando datos', 'error');
        renderDashboardError();
    }
}

function renderDashboard(plan, history) {
    const dashboard = document.getElementById('dashboard-content');
    
    const dailyCalories = plan.daily_calories || 2000;
    const currentWeight = plan.current_weight || 70;
    const goalWeight = plan.goal_weight || 65;
    
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
                        <circle cx="50" cy="50" r="45" fill="none" stroke="url(#gradient)" stroke-width="10" stroke-linecap="round" stroke-dasharray="283" stroke-dashoffset="141"/>
                        <defs>
                            <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="0%">
                                <stop offset="0%" stop-color="#a855f7"/>
                                <stop offset="100%" stop-color="#3b82f6"/>
                            </linearGradient>
                        </defs>
                    </svg>
                    <div class="absolute inset-0 flex items-center justify-center flex-col">
                        <span class="text-2xl font-black dark:text-white">0</span>
                        <span class="text-xs text-gray-500">/ ${dailyCalories}</span>
                    </div>
                </div>
                <p class="text-center text-sm text-gray-500 dark:text-gray-400">kcal consumidas</p>
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
                            <span class="font-bold dark:text-white">0g / 150g</span>
                        </div>
                        <div class="h-3 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
                            <div class="h-full bg-gradient-to-r from-red-500 to-red-600 rounded-full" style="width: 0%"></div>
                        </div>
                    </div>
                    <div>
                        <div class="flex justify-between text-sm mb-1">
                            <span class="dark:text-gray-300">Carbos</span>
                            <span class="font-bold dark:text-white">0g / 200g</span>
                        </div>
                        <div class="h-3 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
                            <div class="h-full bg-gradient-to-r from-yellow-500 to-orange-500 rounded-full" style="width: 0%"></div>
                        </div>
                    </div>
                    <div>
                        <div class="flex justify-between text-sm mb-1">
                            <span class="dark:text-gray-300">Grasas</span>
                            <span class="font-bold dark:text-white">0g / 65g</span>
                        </div>
                        <div class="h-3 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
                            <div class="h-full bg-gradient-to-r from-green-500 to-emerald-500 rounded-full" style="width: 0%"></div>
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
                    <button onclick="startOnboarding()" class="w-full glass py-3 rounded-xl font-bold dark:text-white hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors touch-target">
                        <i class="fas fa-redo mr-2"></i> Ver plan semanal
                    </button>
                </div>
            </div>
        </div>
        
        <!-- Weekly Plan Section -->
        <div class="glass-card rounded-2xl p-6 mb-8">
            <div class="flex items-center justify-between mb-6">
                <h2 class="text-xl font-black dark:text-white">📅 Plan Semanal</h2>
                <div class="flex gap-2">
                    <button onclick="changeDay(-1)" class="touch-target w-10 h-10 rounded-xl glass flex items-center justify-center dark:text-white">
                        <i class="fas fa-chevron-left"></i>
                    </button>
                    <button onclick="changeDay(1)" class="touch-target w-10 h-10 rounded-xl glass flex items-center justify-center dark:text-white">
                        <i class="fas fa-chevron-right"></i>
                    </button>
                </div>
            </div>
            
            <div class="flex gap-2 overflow-x-auto pb-4 mb-6" id="day-selector">
                ${renderDaySelector()}
            </div>
            
            <div id="meals-container" class="space-y-4">
                ${renderMealsPlaceholder()}
            </div>
        </div>
    `;
    
    // Initialize weight chart
    initWeightChart(history);
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

// ==================== ONBOARDING FLOW ====================

function startOnboarding() {
    onboardingStep = 0;
    onboardingData = {};
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
        {
            title: '¡Bienvenido a Diet Tracker FIT! 🎉',
            content: `
                <p class="text-gray-600 dark:text-gray-400 mb-6">Vamos a crear tu plan personalizado en 4 pasos simples.</p>
                <div class="grid grid-cols-2 gap-4 mb-6">
                    <div class="glass p-4 rounded-xl text-center">
                        <div class="text-3xl mb-2">📊</div>
                        <p class="text-sm font-semibold dark:text-white">Tus datos</p>
                    </div>
                    <div class="glass p-4 rounded-xl text-center">
                        <div class="text-3xl mb-2">🎯</div>
                        <p class="text-sm font-semibold dark:text-white">Tu objetivo</p>
                    </div>
                    <div class="glass p-4 rounded-xl text-center">
                        <div class="text-3xl mb-2">🏃</div>
                        <p class="text-sm font-semibold dark:text-white">Actividad</p>
                    </div>
                    <div class="glass p-4 rounded-xl text-center">
                        <div class="text-3xl mb-2">🍽️</div>
                        <p class="text-sm font-semibold dark:text-white">Tu plan</p>
                    </div>
                </div>
            `,
            button: 'Comenzar'
        },
        {
            title: 'Tus datos personales 📝',
            content: `
                <div class="grid grid-cols-2 gap-4">
                    <div>
                        <label class="block text-sm font-semibold mb-2 dark:text-gray-200">Peso (kg)</label>
                        <input type="number" id="onboarding-weight" value="${onboardingData.weight || 70}" class="w-full px-4 py-3 rounded-xl border-2 border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 dark:text-white focus:border-purple-500 focus:outline-none touch-target">
                    </div>
                    <div>
                        <label class="block text-sm font-semibold mb-2 dark:text-gray-200">Altura (cm)</label>
                        <input type="number" id="onboarding-height" value="${onboardingData.height || 170}" class="w-full px-4 py-3 rounded-xl border-2 border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 dark:text-white focus:border-purple-500 focus:outline-none touch-target">
                    </div>
                    <div>
                        <label class="block text-sm font-semibold mb-2 dark:text-gray-200">Edad</label>
                        <input type="number" id="onboarding-age" value="${onboardingData.age || 30}" class="w-full px-4 py-3 rounded-xl border-2 border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 dark:text-white focus:border-purple-500 focus:outline-none touch-target">
                    </div>
                    <div>
                        <label class="block text-sm font-semibold mb-2 dark:text-gray-200">Género</label>
                        <select id="onboarding-gender" class="w-full px-4 py-3 rounded-xl border-2 border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 dark:text-white focus:border-purple-500 focus:outline-none touch-target">
                            <option value="male" ${onboardingData.gender === 'male' ? 'selected' : ''}>Hombre</option>
                            <option value="female" ${onboardingData.gender === 'female' ? 'selected' : ''}>Mujer</option>
                        </select>
                    </div>
                </div>
            `,
            button: 'Continuar',
            prev: true
        },
        {
            title: '¿Cuál es tu objetivo? 🎯',
            content: `
                <div class="space-y-3">
                    <label class="glass p-4 rounded-xl flex items-center gap-4 cursor-pointer hover:bg-purple-50 dark:hover:bg-purple-900/20 transition-colors touch-target">
                        <input type="radio" name="goal" value="lose" ${onboardingData.goal === 'lose' ? 'checked' : ''} class="w-5 h-5">
                        <div>
                            <p class="font-bold dark:text-white">Perder peso</p>
                            <p class="text-sm text-gray-500">Quemar grasa y definir</p>
                        </div>
                    </label>
                    <label class="glass p-4 rounded-xl flex items-center gap-4 cursor-pointer hover:bg-purple-50 dark:hover:bg-purple-900/20 transition-colors touch-target">
                        <input type="radio" name="goal" value="maintain" ${onboardingData.goal === 'maintain' ? 'checked' : ''} class="w-5 h-5">
                        <div>
                            <p class="font-bold dark:text-white">Mantener peso</p>
                            <p class="text-sm text-gray-500">Estabilizar y cuidar salud</p>
                        </div>
                    </label>
                    <label class="glass p-4 rounded-xl flex items-center gap-4 cursor-pointer hover:bg-purple-50 dark:hover:bg-purple-900/20 transition-colors touch-target">
                        <input type="radio" name="goal" value="gain" ${onboardingData.goal === 'gain' ? 'checked' : ''} class="w-5 h-5">
                        <div>
                            <p class="font-bold dark:text-white">Ganar músculo</p>
                            <p class="text-sm text-gray-500">Aumentar masa muscular</p>
                        </div>
                    </label>
                </div>
            `,
            button: 'Continuar',
            prev: true
        },
        {
            title: 'Nivel de actividad 🏃',
            content: `
                <div class="space-y-3">
                    <label class="glass p-4 rounded-xl flex items-center gap-4 cursor-pointer hover:bg-purple-50 dark:hover:bg-purple-900/20 transition-colors touch-target">
                        <input type="radio" name="activity" value="sedentary" ${onboardingData.activity === 'sedentary' ? 'checked' : ''} class="w-5 h-5">
                        <div>
                            <p class="font-bold dark:text-white">Sedentario</p>
                            <p class="text-sm text-gray-500">Poco o nada de ejercicio</p>
                        </div>
                    </label>
                    <label class="glass p-4 rounded-xl flex items-center gap-4 cursor-pointer hover:bg-purple-50 dark:hover:bg-purple-900/20 transition-colors touch-target">
                        <input type="radio" name="activity" value="light" ${onboardingData.activity === 'light' ? 'checked' : ''} class="w-5 h-5">
                        <div>
                            <p class="font-bold dark:text-white">Ligero</p>
                            <p class="text-sm text-gray-500">Ejercicio 1-3 días/semana</p>
                        </div>
                    </label>
                    <label class="glass p-4 rounded-xl flex items-center gap-4 cursor-pointer hover:bg-purple-50 dark:hover:bg-purple-900/20 transition-colors touch-target">
                        <input type="radio" name="activity" value="moderate" ${onboardingData.activity === 'moderate' ? 'checked' : ''} class="w-5 h-5">
                        <div>
                            <p class="font-bold dark:text-white">Moderado</p>
                            <p class="text-sm text-gray-500">Ejercicio 3-5 días/semana</p>
                        </div>
                    </label>
                    <label class="glass p-4 rounded-xl flex items-center gap-4 cursor-pointer hover:bg-purple-50 dark:hover:bg-purple-900/20 transition-colors touch-target">
                        <input type="radio" name="activity" value="active" ${onboardingData.activity === 'active' ? 'checked' : ''} class="w-5 h-5">
                        <div>
                            <p class="font-bold dark:text-white">Activo</p>
                            <p class="text-sm text-gray-500">Ejercicio 6-7 días/semana</p>
                        </div>
                    </label>
                </div>
            `,
            button: 'Calcular mi plan',
            prev: true
        },
        {
            title: '¡Tu plan está listo! 🎉',
            content: `
                <div class="text-center">
                    <div class="w-20 h-20 bg-gradient-to-br from-green-500 to-emerald-500 rounded-full flex items-center justify-center text-4xl mx-auto mb-4">✓</div>
                    <div class="glass-card rounded-2xl p-6 mb-6">
                        <p class="text-sm text-gray-500 mb-2">Tu TMB (Tasa Metabólica Basal)</p>
                        <p class="text-4xl font-black gradient-text mb-4" id="bmr-result">--</p>
                        <p class="text-sm text-gray-500 mb-2">Tu TDEE (Gasto Energético Total)</p>
                        <p class="text-4xl font-black gradient-text mb-4" id="tdee-result">--</p>
                        <p class="text-sm text-gray-500 mb-2">Calorías diarias recomendadas</p>
                        <p class="text-5xl font-black gradient-text" id="calories-result">--</p>
                    </div>
                    <p class="text-gray-600 dark:text-gray-400">Este es el punto de partida para alcanzar tu objetivo.</p>
                </div>
            `,
            button: '¡Comenzar!',
            onShow: calculateResults
        }
    ];
    
    const step = steps[onboardingStep];
    
    container.innerHTML = `
        <div class="fade-in">
            <div class="mb-6">
                <div class="flex gap-2 mb-4">
                    ${steps.map((_, i) => `
                        <div class="h-2 flex-1 rounded-full ${i <= onboardingStep ? 'bg-purple-500' : 'bg-gray-200 dark:bg-gray-700'}"></div>
                    `).join('')}
                </div>
                <h2 class="text-2xl font-black dark:text-white">${step.title}</h2>
            </div>
            
            ${step.content}
            
            <div class="flex gap-4 mt-8">
                ${step.prev ? `
                    <button onclick="prevOnboardingStep()" class="flex-1 py-3 rounded-xl font-bold border-2 border-gray-200 dark:border-gray-700 dark:text-white hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors touch-target">
                        Atrás
                    </button>
                ` : '<div class="flex-1"></div>'}
                <button onclick="nextOnboardingStep()" class="flex-1 btn-primary text-white py-3 rounded-xl font-bold touch-target">
                    ${step.button}
                </button>
            </div>
        </div>
    `;
    
    if (step.onShow) {
        setTimeout(step.onShow, 100);
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
    saveOnboardingData();
    
    if (onboardingStep < 4) {
        onboardingStep++;
        renderOnboardingStep();
    } else {
        closeOnboarding();
        showToast('¡Plan personalizado creado!', 'success');
    }
}

function saveOnboardingData() {
    if (onboardingStep === 1) {
        onboardingData.weight = parseFloat(document.getElementById('onboarding-weight').value);
        onboardingData.height = parseFloat(document.getElementById('onboarding-height').value);
        onboardingData.age = parseFloat(document.getElementById('onboarding-age').value);
        onboardingData.gender = document.getElementById('onboarding-gender').value;
    } else if (onboardingStep === 2) {
        const goal = document.querySelector('input[name="goal"]:checked');
        if (goal) onboardingData.goal = goal.value;
    } else if (onboardingStep === 3) {
        const activity = document.querySelector('input[name="activity"]:checked');
        if (activity) onboardingData.activity = activity.value;
    }
}

function calculateResults() {
    // Calculate BMR (Mifflin-St Jeor)
    let bmr = 10 * onboardingData.weight + 6.25 * onboardingData.height - 5 * onboardingData.age;
    bmr += onboardingData.gender === 'male' ? 5 : -161;
    
    // Activity multipliers
    const activityMultipliers = {
        sedentary: 1.2,
        light: 1.375,
        moderate: 1.55,
        active: 1.725
    };
    
    const tdee = bmr * (activityMultipliers[onboardingData.activity] || 1.2);
    
    // Goal adjustments
    let calories = tdee;
    if (onboardingData.goal === 'lose') calories -= 500;
    if (onboardingData.goal === 'gain') calories += 300;
    
    document.getElementById('bmr-result').textContent = Math.round(bmr) + ' kcal';
    document.getElementById('tdee-result').textContent = Math.round(tdee) + ' kcal';
    document.getElementById('calories-result').textContent = Math.round(calories) + ' kcal';
}

// ==================== FOOD REGISTRATION ====================

function openFoodModal() {
    document.getElementById('food-modal').classList.remove('hidden');
    document.body.style.overflow = 'hidden';
    renderFoodSearch();
}

function closeFoodModal() {
    document.getElementById('food-modal').classList.add('hidden');
    document.body.style.overflow = '';
}

function renderFoodSearch() {
    const container = document.getElementById('food-content');
    
    container.innerHTML = `
        <div class="fade-in">
            <h2 class="text-2xl font-black dark:text-white mb-6">🍽️ Registrar comida</h2>
            
            <!-- Search -->
            <div class="mb-6">
                <div class="relative">
                    <input type="text" id="food-search" placeholder="Buscar alimento o receta..." 
                           class="w-full px-4 py-3 pl-12 rounded-xl border-2 border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 dark:text-white focus:border-purple-500 focus:outline-none touch-target"
                           oninput="searchFood(this.value)">
                    <i class="fas fa-search absolute left-4 top-1/2 -translate-y-1/2 text-gray-400"></i>
                </div>
            </div>
            
            <!-- Quick Add -->
            <div class="mb-6">
                <h3 class="font-bold dark:text-white mb-3">Añadir rápido</h3>
                <div class="grid grid-cols-2 sm:grid-cols-4 gap-3">
                    <button onclick="quickAdd('Desayuno', 400)" class="glass p-4 rounded-xl text-center hover:bg-purple-50 dark:hover:bg-purple-900/20 transition-colors touch-target">
                        <div class="text-2xl mb-1">🌅</div>
                        <p class="text-sm font-semibold dark:text-white">Desayuno</p>
                        <p class="text-xs text-gray-500">~400 kcal</p>
                    </button>
                    <button onclick="quickAdd('Comida', 600)" class="glass p-4 rounded-xl text-center hover:bg-purple-50 dark:hover:bg-purple-900/20 transition-colors touch-target">
                        <div class="text-2xl mb-1">☀️</div>
                        <p class="text-sm font-semibold dark:text-white">Comida</p>
                        <p class="text-xs text-gray-500">~600 kcal</p>
                    </button>
                    <button onclick="quickAdd('Merienda', 200)" class="glass p-4 rounded-xl text-center hover:bg-purple-50 dark:hover:bg-purple-900/20 transition-colors touch-target">
                        <div class="text-2xl mb-1">🍎</div>
                        <p class="text-sm font-semibold dark:text-white">Merienda</p>
                        <p class="text-xs text-gray-500">~200 kcal</p>
                    </button>
                    <button onclick="quickAdd('Cena', 500)" class="glass p-4 rounded-xl text-center hover:bg-purple-50 dark:hover:bg-purple-900/20 transition-colors touch-target">
                        <div class="text-2xl mb-1">🌙</div>
                        <p class="text-sm font-semibold dark:text-white">Cena</p>
                        <p class="text-xs text-gray-500">~500 kcal</p>
                    </button>
                </div>
            </div>
            
            <!-- Search Results -->
            <div id="food-results" class="space-y-3">
                <div class="text-center py-8 text-gray-500">
                    <i class="fas fa-search text-3xl mb-2"></i>
                    <p>Busca alimentos para ver resultados</p>
                </div>
            </div>
        </div>
    `;
}

function searchFood(query) {
    const resultsContainer = document.getElementById('food-results');
    
    if (!query || query.length < 2) {
        resultsContainer.innerHTML = `
            <div class="text-center py-8 text-gray-500">
                <i class="fas fa-search text-3xl mb-2"></i>
                <p>Busca alimentos para ver resultados</p>
            </div>
        `;
        return;
    }
    
    // Mock results (in real app, fetch from API)
    const mockFoods = [
        { name: 'Pechuga de pollo', calories: 165, protein: 31, carbs: 0, fat: 3.6 },
        { name: 'Arroz blanco', calories: 130, protein: 2.7, carbs: 28, fat: 0.3 },
        { name: 'Brócoli', calories: 34, protein: 2.8, carbs: 7, fat: 0.4 },
        { name: 'Salmón', calories: 208, protein: 20, carbs: 0, fat: 13 },
        { name: 'Huevo', calories: 155, protein: 13, carbs: 1.1, fat: 11 },
        { name: 'Avena', calories: 389, protein: 17, carbs: 66, fat: 7 },
        { name: 'Plátano', calories: 89, protein: 1.1, carbs: 23, fat: 0.3 },
        { name: 'Aguacate', calories: 160, protein: 2, carbs: 9, fat: 15 }
    ];
    
    const filtered = mockFoods.filter(f => f.name.toLowerCase().includes(query.toLowerCase()));
    
    if (filtered.length === 0) {
        resultsContainer.innerHTML = `
            <div class="text-center py-8 text-gray-500">
                <i class="fas fa-utensils text-3xl mb-2"></i>
                <p>No se encontraron resultados</p>
            </div>
        `;
        return;
    }
    
    resultsContainer.innerHTML = filtered.map(food => `
        <div class="glass-card rounded-xl p-4 flex items-center justify-between">
            <div>
                <p class="font-bold dark:text-white">${food.name}</p>
                <p class="text-sm text-gray-500">${food.calories} kcal • P: ${food.protein}g • C: ${food.carbs}g • G: ${food.fat}g</p>
            </div>
            <button onclick="addFood('${food.name}', ${food.calories})" class="btn-primary text-white px-4 py-2 rounded-xl font-bold text-sm touch-target">
                Añadir
            </button>
        </div>
    `).join('');
}

function quickAdd(meal, calories) {
    showToast(`✓ ${meal} añadido (${calories} kcal)`, 'success');
}

function addFood(name, calories) {
    showToast(`✓ ${name} añadido (${calories} kcal)`, 'success');
}

// ==================== WEIGHT MODAL ====================

function openWeightModal() {
    showToast('Función de registro de peso próximamente', 'info');
}

// ==================== SHOPPING LIST ====================

function showShoppingList() {
    showToast('Lista de compras próximamente', 'info');
}

// ==================== TOAST NOTIFICATIONS ====================

function showToast(message, type) {
    if (!type) type = 'info';
    
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');
    
    const colors = {
        success: 'from-green-500 to-emerald-600',
        error: 'from-red-500 to-rose-600',
        info: 'from-purple-500 to-blue-600'
    };
    
    const icons = {
        success: '✓',
        error: '✕',
        info: 'ℹ'
    };
    
    toast.className = `bg-gradient-to-r ${colors[type]} text-white px-6 py-3 rounded-xl shadow-lg flex items-center gap-3 slide-enter`;
    toast.innerHTML = `
        <span class="text-lg font-bold">${icons[type]}</span>
        <span class="font-medium">${message}</span>
    `;
    
    container.appendChild(toast);
    
    setTimeout(() => {
        toast.style.transition = 'opacity 0.3s';
        toast.style.opacity = '0';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}
