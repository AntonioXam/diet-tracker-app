# 🚀 Deploy & Monitoring Configuration

## Diet Tracker FIT - Complete Setup Guide

---

## ✅ TAREA 1 - Vercel Environment Variables

### Required Environment Variables

Configure these in your Vercel project settings (**Settings → Environment Variables**):

| Variable | Value |
|----------|-------|
| `SUPABASE_URL` | `https://kaomgwojvnncidyezdzj.supabase.co` |
| `SUPABASE_ANON_KEY` | `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imthb21nd29qdm5uY2lkeWV6ZHpqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzI3MDcxNzYsImV4cCI6MjA4ODI4MzE3Nn0.Ds2ICxfiahuqt2n83dwoX9tMYGf7Xz8Jjvx6lFJc4zs` |

### CLI Alternative

```bash
vercel env add SUPABASE_URL https://kaomgwojvnncidyezdzj.supabase.co
vercel env add SUPABASE_ANON_KEY eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imthb21nd29qdm5uY2lkeWV6ZHpqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzI3MDcxNzYsImV4cCI6MjA4ODI4MzE3Nn0.Ds2ICxfiahuqt2n83dwoX9tMYGf7Xz8Jjvx6lFJc4zs
```

---

## ✅ TAREA 2 - SEO Configuration

### Meta Tags (index.html)

- ✅ Title tag
- ✅ Meta description
- ✅ Open Graph tags (Facebook/LinkedIn)
- ✅ Twitter Card tags
- ✅ Keywords meta tag
- ✅ Robots meta tag
- ✅ Author meta tag

### Files Created

| File | Location | Purpose |
|------|----------|---------|
| `robots.txt` | `/frontend/robots.txt` | Crawler instructions |
| `sitemap.xml` | `/frontend/sitemap.xml` | Site structure for search engines |
| `favicon.svg` | `/frontend/favicon.svg` | Scalable favicon |
| `site.webmanifest` | `/frontend/site.webmanifest` | PWA configuration |

### Favicon Files Needed

Generate and place these in `/frontend/`:

```
favicon-16x16.png   (16x16px)
favicon-32x32.png   (32x32px)
apple-touch-icon.png (180x180px)
icon-192.png        (192x192px)
icon-512.png        (512x512px)
favicon.ico         (multi-size .ico)
og-image.png        (1200x630px for social sharing)
```

### Generate Favicons

Use [RealFaviconGenerator](https://realfavicongenerator.net/) or similar tool with the SVG favicon as base.

### Sitemap Submission

After deploy, submit sitemap to:
- [Google Search Console](https://search.google.com/search-console)
- [Bing Webmaster Tools](https://www.bing.com/webmasters)

---

## ✅ TAREA 3 - Monitoring

### Google Analytics

**Status:** ⚠️ **NEEDS CONFIGURATION**

Replace `G-XXXXXXXXXX` with your actual GA4 Measurement ID:

1. Go to [Google Analytics](https://analytics.google.com/)
2. Create property for "Diet Tracker FIT"
3. Get Measurement ID (format: `G-XXXXXXXXXX`)
4. Update `index.html` lines 38-43

```html
<script async src="https://www.googletagmanager.com/gtag/js?id=G-YOUR_ACTUAL_ID"></script>
<script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'G-YOUR_ACTUAL_ID');
</script>
```

### Sentry Error Tracking

**Status:** ⚠️ **NEEDS CONFIGURATION**

Replace the DSN in `index.html` lines 46-59:

1. Go to [Sentry.io](https://sentry.io/)
2. Create new project (JavaScript)
3. Copy your DSN
4. Update the `Sentry.init()` configuration

```javascript
Sentry.init({
    dsn: "https://YOUR_ACTUAL_DSN@o0.ingest.sentry.io/0",
    // ... rest of config
});
```

### What's Tracked

- **JavaScript errors** (automatic)
- **Performance metrics** (tracing enabled)
- **Session replays** (10% sample rate, 100% on errors)
- **Page views** (via Google Analytics)
- **User interactions** (custom events can be added)

---

## ✅ TAREA 4 - Performance Optimization

### Caching Strategy (vercel.json)

| Asset Type | Cache Duration |
|------------|----------------|
| Images (jpg, jpeg, png, gif, webp, svg, ico) | 1 year (immutable) |
| CSS/JS files | 1 year (immutable) |
| robots.txt, sitemap.xml, favicons | 1 day |
| HTML pages | Default (no cache header) |

### Image Optimization

**Recommendations:**

1. **Convert to WebP/AVIF** - Use modern formats
2. **Lazy loading** - Add `loading="lazy"` to images
3. **Responsive images** - Use `srcset` for different sizes
4. **Compress** - Use tools like TinyPNG, Squoosh

**Example implementation:**

```html
<img 
    src="image.webp" 
    srcset="image-480.webp 480w, image-800.webp 800w, image-1200.webp 1200w"
    sizes="(max-width: 600px) 480px, (max-width: 900px) 800px, 1200px"
    alt="Description"
    loading="lazy"
    width="1200"
    height="800"
>
```

### Vercel Optimizations

- ✅ Automatic image optimization via `@vercel/static`
- ✅ Edge caching (region: iad1)
- ✅ HTTP/2 enabled by default
- ✅ Automatic Brotli compression
- ✅ Security headers configured

### Security Headers

```
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Referrer-Policy: strict-origin-when-cross-origin
```

---

## 📊 Post-Deploy Checklist

### Immediate Actions

- [ ] Add actual Google Analytics ID
- [ ] Add actual Sentry DSN
- [ ] Generate and upload favicon files
- [ ] Create og-image.png for social sharing
- [ ] Test in Vercel preview deployment

### After First Deploy

- [ ] Submit sitemap to Google Search Console
- [ ] Submit sitemap to Bing Webmaster Tools
- [ ] Verify domain in Google Analytics
- [ ] Set up Sentry alerts for errors
- [ ] Test error tracking (trigger test error)
- [ ] Verify analytics events in GA4
- [ ] Run Lighthouse audit
- [ ] Test on mobile devices
- [ ] Check Core Web Vitals

### Ongoing Monitoring

- [ ] Review Sentry error dashboard weekly
- [ ] Check GA4 traffic reports weekly
- [ ] Monitor Vercel analytics for performance
- [ ] Update sitemap when adding new pages
- [ ] Review and optimize slow endpoints

---

## 🔧 Commands

### Local Testing

```bash
cd diet-tracker-app
python -m http.server 8000
# Visit http://localhost:8000/frontend/
```

### Vercel CLI

```bash
# Install
npm i -g vercel

# Login
vercel login

# Deploy preview
vercel

# Deploy to production
vercel --prod
```

### Environment Variables Check

```bash
vercel env ls
```

---

## 📈 Performance Targets

| Metric | Target | Current |
|--------|--------|---------|
| LCP (Largest Contentful Paint) | < 2.5s | TBD |
| FID (First Input Delay) | < 100ms | TBD |
| CLS (Cumulative Layout Shift) | < 0.1 | TBD |
| Performance Score | > 90 | TBD |

Run Lighthouse after deploy to measure actual values.

---

## 🆘 Troubleshooting

### Environment Variables Not Working

1. Check variable names match exactly (case-sensitive)
2. Redeploy after adding new env vars
3. Verify in Vercel dashboard → Settings → Environment Variables

### Analytics Not Tracking

1. Check browser console for errors
2. Verify GA4 Measurement ID is correct
3. Use Google Tag Assistant extension
4. Check real-time reports in GA4

### Sentry Not Capturing Errors

1. Verify DSN is correct
2. Check browser console for Sentry initialization
3. Trigger a test error: `throw new Error('Test Sentry error')`
4. Check Sentry project → Issues

### Caching Issues

1. Hard refresh (Ctrl+Shift+R / Cmd+Shift+R)
2. Check Response Headers in DevTools
3. Purge cache in Vercel dashboard if needed

---

**Last Updated:** 2025-03-05  
**Project:** Diet Tracker FIT  
**Deploy URL:** https://diet-tracker-app-chi.vercel.app
