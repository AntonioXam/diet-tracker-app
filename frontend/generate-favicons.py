#!/usr/bin/env python3
"""
Generate all favicons and OG image for Diet Tracker FIT
Uses Pillow to create PNGs and ICO from SVG base
"""

import os
from PIL import Image, ImageDraw, ImageFont
import math

# Output directory
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# Colors (purple/blue gradient)
PURPLE = (168, 85, 247)    # #a855f7
BLUE = (59, 130, 246)      # #3b82f6
WHITE = (255, 255, 255)
TRANSPARENT = (0, 0, 0, 0)

def create_gradient_background(width, height, color1, color2):
    """Create a purple to blue gradient background"""
    img = Image.new('RGBA', (width, height), color1 + (255,))
    pixels = img.load()
    
    for y in range(height):
        # Calculate interpolation factor (diagonal gradient)
        t = (y / height)
        r = int(color1[0] * (1 - t) + color2[0] * t)
        g = int(color1[1] * (1 - t) + color2[1] * t)
        b = int(color1[2] * (1 - t) + color2[2] * t)
        
        for x in range(width):
            # Diagonal gradient
            t2 = ((x / width) + (y / height)) / 2
            r = int(color1[0] * (1 - t2) + color2[0] * t2)
            g = int(color1[1] * (1 - t2) + color2[1] * t2)
            b = int(color1[2] * (1 - t2) + color2[2] * t2)
            pixels[x, y] = (r, g, b, 255)
    
    return img

def draw_salad_emoji(img, size_factor=0.6):
    """Draw a salad emoji on the image"""
    draw = ImageDraw.Draw(img)
    width, height = img.size
    
    # Calculate emoji size and position
    emoji_size = int(min(width, height) * size_factor)
    x = (width - emoji_size) // 2
    y = (height - emoji_size) // 2
    
    # We'll create the emoji using text
    # Try to load a font that supports emoji
    font_paths = [
        "/System/Library/Fonts/AppleColorEmoji.ttc",
        "/System/Library/Fonts/Emoji.ttc",
        "/Library/Fonts/AppleColorEmoji.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf",
    ]
    
    font = None
    for path in font_paths:
        if os.path.exists(path):
            try:
                font = ImageFont.truetype(path, emoji_size)
                break
            except:
                continue
    
    if font is None:
        # Fall back to default font
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", emoji_size)
        except:
            font = ImageFont.load_default()
    
    # Draw the salad emoji
    draw.text((x, y - emoji_size//10), "🥗", font=font, fill=WHITE, anchor="mm")
    
    return img

def create_favicon_png(size):
    """Create a single favicon PNG"""
    img = create_gradient_background(size, size, PURPLE, BLUE)
    img = draw_salad_emoji(img, size_factor=0.65)
    
    output_path = os.path.join(OUTPUT_DIR, f"favicon-{size}x{size}.png")
    img.save(output_path, "PNG")
    print(f"✅ Created: favicon-{size}x{size}.png")
    return output_path

def create_icon_png(size, filename):
    """Create an icon PNG with specific filename"""
    img = create_gradient_background(size, size, PURPLE, BLUE)
    img = draw_salad_emoji(img, size_factor=0.65)
    
    output_path = os.path.join(OUTPUT_DIR, filename)
    img.save(output_path, "PNG")
    print(f"✅ Created: {filename}")
    return output_path

def create_favicon_ico():
    """Create favicon.ico with multiple sizes using proper ICO format"""
    import struct
    import io
    
    sizes = [16, 32]
    icon_images = []
    
    for size in sizes:
        img = create_gradient_background(size, size, PURPLE, BLUE)
        img = draw_salad_emoji(img, size_factor=0.65)
        img = img.convert("RGBA")
        
        # Save to bytes as PNG (ICO can contain PNG data)
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        icon_images.append(buffer.getvalue())
    
    output_path = os.path.join(OUTPUT_DIR, "favicon.ico")
    
    # Build ICO file
    with open(output_path, 'wb') as f:
        # ICO header (6 bytes): reserved, type (1=icon), count
        f.write(struct.pack('<HHH', 0, 1, len(icon_images)))
        
        # Icon directory entries (16 bytes each)
        offset = 6 + 16 * len(icon_images)
        for i, img_data in enumerate(icon_images):
            size = sizes[i]
            w = size if size < 256 else 0
            h = size if size < 256 else 0
            # width, height, colors, reserved, planes, bpp, data size, offset
            f.write(struct.pack('<BBBBHHII', w, h, 0, 0, 1, 32, len(img_data), offset))
            offset += len(img_data)
        
        # Write image data
        for img_data in icon_images:
            f.write(img_data)
    
    print(f"✅ Created: favicon.ico (16x16, 32x32)")
    return output_path

def create_og_image():
    """Create OG image (1200x630) for social sharing"""
    width, height = 1200, 630
    
    # Create gradient background
    img = Image.new('RGBA', (width, height), PURPLE + (255,))
    pixels = img.load()
    
    # Create diagonal gradient
    for y in range(height):
        for x in range(width):
            t = ((x / width) + (y / height)) / 2
            r = int(PURPLE[0] * (1 - t) + BLUE[0] * t)
            g = int(PURPLE[1] * (1 - t) + BLUE[1] * t)
            b = int(PURPLE[2] * (1 - t) + BLUE[2] * t)
            pixels[x, y] = (r, g, b, 255)
    
    draw = ImageDraw.Draw(img)
    
    # Load fonts
    font_paths_title = [
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/HelveticaNeue.ttc",
        "/Library/Fonts/Arial.ttf",
    ]
    
    font_paths_subtitle = [
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/HelveticaNeue.ttc",
        "/Library/Fonts/Arial.ttf",
    ]
    
    title_font = None
    subtitle_font = None
    
    for path in font_paths_title:
        if os.path.exists(path):
            try:
                title_font = ImageFont.truetype(path, 72)
                break
            except:
                continue
    
    for path in font_paths_subtitle:
        if os.path.exists(path):
            try:
                subtitle_font = ImageFont.truetype(path, 42)
                break
            except:
                continue
    
    if title_font is None:
        title_font = ImageFont.load_default()
    if subtitle_font is None:
        subtitle_font = ImageFont.load_default()
    
    # Draw title
    title = "Diet Tracker FIT - Premium"
    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    title_x = (width - title_width) // 2
    title_y = height // 2 - 60
    
    # Add text shadow for better readability
    shadow_offset = 3
    draw.text((title_x + shadow_offset, title_y + shadow_offset), title, font=title_font, fill=(0, 0, 0, 100))
    draw.text((title_x, title_y), title, font=title_font, fill=WHITE)
    
    # Draw subtitle
    subtitle = "350+ recetas saludables"
    subtitle_bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
    subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
    subtitle_x = (width - subtitle_width) // 2
    subtitle_y = height // 2 + 20
    
    # Add text shadow for subtitle
    draw.text((subtitle_x + shadow_offset, subtitle_y + shadow_offset), subtitle, font=subtitle_font, fill=(0, 0, 0, 100))
    draw.text((subtitle_x, subtitle_y), subtitle, font=subtitle_font, fill=WHITE)
    
    # Draw large salad emoji
    emoji_size = 200
    emoji_x = (width - emoji_size) // 2
    emoji_y = height // 2 - 180
    
    # Try to load emoji font
    emoji_font_paths = [
        "/System/Library/Fonts/AppleColorEmoji.ttc",
        "/System/Library/Fonts/Emoji.ttc",
    ]
    
    emoji_font = None
    for path in emoji_font_paths:
        if os.path.exists(path):
            try:
                emoji_font = ImageFont.truetype(path, emoji_size)
                break
            except:
                continue
    
    if emoji_font:
        draw.text((emoji_x, emoji_y), "🥗", font=emoji_font, fill=WHITE)
    else:
        # Fallback: draw a simple circle with text
        circle_x = width // 2
        circle_y = emoji_y + emoji_size // 2
        draw.ellipse([circle_x - 100, circle_y - 100, circle_x + 100, circle_y + 100], fill=WHITE)
        draw.text((circle_x - 30, circle_y - 40), "🥗", font=ImageFont.load_default(), fill=PURPLE)
    
    output_path = os.path.join(OUTPUT_DIR, "og-image.png")
    img.save(output_path, "PNG")
    print(f"✅ Created: og-image.png (1200x630)")
    return output_path

def update_improved_favicon_svg():
    """Create an improved favicon.svg"""
    svg_content = '''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
  <defs>
    <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#a855f7;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#3b82f6;stop-opacity:1" />
    </linearGradient>
    <filter id="shadow" x="-50%" y="-50%" width="200%" height="200%">
      <feDropShadow dx="0" dy="4" stdDeviation="8" flood-opacity="0.3"/>
    </filter>
  </defs>
  
  <!-- Background circle with gradient -->
  <circle cx="256" cy="256" r="250" fill="url(#grad)" filter="url(#shadow)"/>
  
  <!-- Salad emoji centered -->
  <text x="256" y="320" font-size="280" text-anchor="middle" fill="white" font-family="Apple Color Emoji, Segoe UI Emoji, Noto Color Emoji, sans-serif" font-weight="bold">🥗</text>
</svg>
'''
    
    output_path = os.path.join(OUTPUT_DIR, "favicon.svg")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(svg_content)
    print(f"✅ Created: favicon.svg (512x512 viewBox, improved)")
    return output_path

def main():
    print("🎨 Generating favicons and OG image for Diet Tracker FIT...")
    print("=" * 60)
    
    # Create improved SVG favicon
    update_improved_favicon_svg()
    
    # Create PNG favicons
    create_favicon_png(16)
    create_favicon_png(32)
    
    # Create specific icon files
    create_icon_png(180, "apple-touch-icon.png")
    create_icon_png(192, "icon-192.png")
    create_icon_png(512, "icon-512.png")
    
    # Create ICO file
    create_favicon_ico()
    
    # Create OG image
    create_og_image()
    
    print("=" * 60)
    print("✅ All favicons and OG image generated successfully!")
    print("\nGenerated files:")
    print("  - favicon.svg (512x512 viewBox)")
    print("  - favicon-16x16.png")
    print("  - favicon-32x32.png")
    print("  - favicon.ico (16x16, 32x32)")
    print("  - apple-touch-icon.png (180x180)")
    print("  - icon-192.png (192x192)")
    print("  - icon-512.png (512x512)")
    print("  - og-image.png (1200x630)")

if __name__ == "__main__":
    main()
