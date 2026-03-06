# 📧 CONFIGURAR EMAIL PARA RECUPERAR CONTRASEÑA

## Opción 1: Usar Supabase Auth (RECOMENDADO)

Supabase ya tiene email de recuperación integrado. Solo necesitas:

### 1. Configurar Email en Supabase:

1. Ve a: https://supabase.com/dashboard/project/kaomgwojvnncidyezdzj/auth/providers
2. Click en **Email**
3. Activa **"Enable Email Provider"**
4. Configura:
   - **From email:** noreply@tu-dominio.com (o usa el default de Supabase)
   - **From name:** Diet Tracker FIT

### 2. Habilitar Email Templates:

1. Ve a: https://supabase.com/dashboard/project/kaomgwojvnncidyezdzj/auth/templates
2. Editar template **"Recovery"**
3. Personaliza el email (opcional)

### 3. En el Frontend:

El código ya está implementado en `handleForgotPassword()`. Solo necesita:
- Que el usuario esté registrado en Supabase Auth
- El backend llamará a `supabase.auth.resetPasswordForEmail()`

---

## Opción 2: Usar tu propio SMTP

Si quieres usar tu propio servidor de email:

### 1. Configurar variables en Vercel:

```
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=tu-email@gmail.com
SMTP_PASS=tu-password-o-app-password
```

### 2. Instalar nodemailer en backend:

```bash
cd api
pip install flask-mail
```

---

## 🎯 RECOMENDACIÓN:

**Usa Supabase Auth** - Ya está integrado y es gratis hasta 50k emails/mes.

### Pasos rápidos:

1. **Ve a:** https://supabase.com/dashboard/project/kaomgwojvnncidyezdzj/auth/providers
2. **Activa Email**
3. **Guarda**
4. **Prueba** el forgot password en tu app

**¿Quieres que implemente el código para Supabase Auth?**
