# 🖼️ Image Optimization Guide

## Current Status

The app currently uses emoji icons (🥗, 📊, etc.) which are lightweight and don't require optimization.

## When Adding Images

### 1. Convert to Modern Formats

Use **WebP** or **AVIF** for best compression:

```bash
# Using ImageMagick
convert input.png output.webp

# Using squoosh-cli
npx @squoosh/cli input.png --webp '{quality: 80}'
```

### 2. Generate Multiple Sizes

For responsive images:

```bash
# Generate srcset sizes
convert input.png -resize 480w output-480.webp
convert input.png -resize 800w output-800.webp
convert input.png -resize 1200w output-1200.webp
```

### 3. Implement Lazy Loading

Add to your HTML:

```html
<img 
    src="image.webp" 
    alt="Description"
    loading="lazy"
    decoding="async"
    width="800"
    height="600"
>
```

### 4. Use Vercel Image Optimization

```html
<!-- Vercel will auto-optimize -->
<img src="/images/recipe.jpg" alt="Recipe" />
```

Vercel automatically:
- Converts to WebP/AVIF
- Resizes based on device
- Caches at edge locations

## Recommended Image Locations

```
frontend/
├── images/
│   ├── og-image.png (1200x630 - social sharing)
│   ├── favicon/
│   │   ├── favicon-16x16.png
│   │   ├── favicon-32x32.png
│   │   ├── apple-touch-icon.png (180x180)
│   │   ├── icon-192.png
│   │   └── icon-512.png
│   ├── recipes/
│   │   └── [recipe-id].webp
│   └── heroes/
│       └── hero-banner.webp
```

## Tools

- **[Squoosh](https://squoosh.app/)** - Online image optimizer
- **[TinyPNG](https://tinypng.com/)** - PNG compression
- **[ImageOptim](https://imageoptim.com/)** - Mac app for optimization
- **[RealFaviconGenerator](https://realfavicongenerator.net/)** - Favicon generator

## Performance Impact

| Format | Size (example) | Quality |
|--------|---------------|---------|
| PNG | 500 KB | Good |
| JPEG | 200 KB | Good |
| WebP | 100 KB | Same/Better |
| AVIF | 70 KB | Same/Better |

**Target:** All images under 100 KB where possible.

## Lighthouse Image Audit Checks

- [ ] Images use modern formats (WebP/AVIF)
- [ ] Images are properly sized
- [ ] Lazy loading enabled for offscreen images
- [ ] Aspect ratio is explicit (width/height attributes)
- [ ] Alt text is present for accessibility
