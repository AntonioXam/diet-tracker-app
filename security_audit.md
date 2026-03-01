# Auditoría de Seguridad - Diet Tracker App

Fecha: 2026-03-01
Auditor: Especialista en seguridad web

## Resumen Ejecutivo

La aplicación Diet Tracker presenta varias vulnerabilidades de seguridad críticas y mejorables. La ausencia de autenticación robusta, autorización, rate limiting y headers de seguridad expone la aplicación a riesgos significativos. A continuación se detallan los hallazgos y recomendaciones.

## 1. Autenticación y Autorización

### Hallazgos:
- **A1**: No existe autenticación por contraseña. El login solo requiere username (email), permitiendo que cualquier persona que conozca el username acceda como ese usuario.
- **A2**: No hay tokens de sesión ni cookies seguras. El estado de autenticación se maneja completamente en el frontend (localStorage) sin verificación en el backend.
- **A3**: No hay autorización a nivel de endpoints. Todos los endpoints que requieren `user_id` aceptan dicho parámetro sin verificar que corresponda al usuario autenticado. Esto permite a un usuario modificar/ver datos de cualquier otro usuario (IDOR).
- **A4**: No hay protección contra CSRF (Cross-Site Request Forgery). Como no hay tokens CSRF, un sitio malicioso podría realizar acciones en nombre del usuario.

### Recomendaciones:
- Implementar autenticación con contraseña segura (hash bcrypt).
- Introducir tokens de sesión (JWT o session cookies) y validarlos en cada request.
- Implementar middleware de autorización que verifique que el `user_id` del token coincida con el `user_id` solicitado.
- Agregar tokens CSRF si se usan cookies, o asegurar que las operaciones críticas requieran origin validation.

## 2. Protección contra Inyecciones SQL

### Hallazgos:
- **S1**: Uso de Supabase client que probablemente utiliza consultas parametrizadas. No se observa concatenación directa de strings en consultas SQL.
- **S2**: Sin embargo, no hay revisión de posibles inyecciones NoSQL o de otros vectores (Supabase es PostgreSQL, pero el cliente podría ser vulnerable si se concatenan strings).

### Recomendaciones:
- Mantener el uso de consultas parametrizadas a través del cliente Supabase.
- Evitar cualquier concatenación de strings en consultas.
- Realizar sanitización de inputs para prevenir otros tipos de inyección (ej. inyección de comandos).

## 3. Validación de Entrada

### Hallazgos:
- **V1**: Validación básica de campos requeridos y rangos en el frontend y backend.
- **V2**: No hay sanitización de HTML/JavaScript en campos de texto (alergias, nombre de recetas, etc.) lo que podría dar lugar a XSS almacenado si los datos se comparten entre usuarios.
- **V3**: No hay validación de tipos estricta en todos los endpoints (ej. `user_id` como string vs integer).

### Recomendaciones:
- Implementar sanitización de HTML en el backend (escapar caracteres especiales) o usar librerías como `bleach`.
- Validar tipos de datos y formatos (ej. email, números enteros positivos).
- Usar schemas de validación (p.ej. marshmallow, pydantic) para garantizar integridad.

## 4. Headers de Seguridad HTTP

### Hallazgos:
- **H1**: CORS configurado con `CORS(app)` (default) permitiendo cualquier origen.
- **H2**: Faltan headers de seguridad: `Strict-Transport-Security` (HSTS), `X-Content-Type-Options`, `X-Frame-Options`, `Content-Security-Policy`, `X-XSS-Protection`.
- **H3**: No se utiliza `Secure` y `HttpOnly` para cookies (no hay cookies actualmente).

### Recomendaciones:
- Restringir CORS a los dominios del frontend (ej. vercel.app, localhost).
- Agregar headers de seguridad mediante middleware de Flask (Flask-Talisman).
- Si se implementan cookies, marcarlas como `Secure`, `HttpOnly` y `SameSite=Strict`.

## 5. Manejo Seguro de Contraseñas

### Hallazgos:
- **P1**: No se utilizan contraseñas. La función `hash_password` utiliza SHA256 sin salt, lo cual es inseguro.
- **P2**: No hay política de complejidad de contraseñas.
- **P3**: No hay mecanismo de recuperación de contraseña.

### Recomendaciones:
- Implementar bcrypt o argon2 para hashing de contraseñas.
- Agregar salt único por usuario.
- Exigir contraseñas de al menos 8 caracteres con combinación de tipos.
- Implementar flujo de recuperación (restablecimiento) de contraseña.

## 6. Protección de Endpoints

### Hallazgos:
- **E1**: No hay rate limiting. Posibilidad de ataques de fuerza bruta en login/registro.
- **E2**: No hay logging de actividades sospechosas (intentos fallidos, accesos no autorizados).
- **E3**: No hay autenticación para endpoints públicos (health, etc.) – aceptable.
- **E4**: No hay versionamiento de API ni deprecation.

### Recomendaciones:
- Implementar rate limiting (ej. Flask-Limiter) para endpoints de autenticación y recursos.
- Configurar logs estructurados para eventos de seguridad.
- Considerar autenticación para endpoints que manipulan datos sensibles.
- Introducir versionamiento de API (ej. `/api/v1/`).

## 7. Otros Aspectos

### Hallazgos:
- **O1**: El archivo `.env` contiene credenciales sensibles (SUPABASE_URL, SUPABASE_KEY) y debe estar en `.gitignore`. Ya está ignorado.
- **O2**: No hay revisión de dependencias (vulnerabilidades conocidas).
- **O3**: No hay pruebas de seguridad automatizadas.

### Recomendaciones:
- Revisar dependencias con `safety` o `npm audit`.
- Integrar escaneo de seguridad en CI/CD.
- Realizar pruebas de penetración básicas.

## Plan de Acción Priorizado

1. **Crítico**: Implementar autorización (middleware) para prevenir IDOR.
2. **Alto**: Agregar autenticación con contraseña y tokens JWT.
3. **Alto**: Configurar headers de seguridad (Flask-Talisman).
4. **Medio**: Implementar rate limiting.
5. **Medio**: Sanitizar inputs y validar esquemas.
6. **Bajo**: Revisar dependencias y actualizar.

## Referencias

- OWASP Top 10 (2021)
- Flask Security Checklist
- Supabase Security Best Practices