#!/usr/bin/env python3
"""
Verify all favicons and OG image are correctly created and accessible
"""

import os
from PIL import Image

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# Expected files with their required dimensions
EXPECTED_FILES = {
    'favicon.svg': {'type': 'svg', 'viewBox': '512x512'},
    'favicon-16x16.png': {'type': 'png', 'size': (16, 16)},
    'favicon-32x32.png': {'type': 'png', 'size': (32, 32)},
    'favicon.ico': {'type': 'ico', 'sizes': [(16, 16), (32, 32)]},
    'apple-touch-icon.png': {'type': 'png', 'size': (180, 180)},
    'icon-192.png': {'type': 'png', 'size': (192, 192)},
    'icon-512.png': {'type': 'png', 'size': (512, 512)},
    'og-image.png': {'type': 'png', 'size': (1200, 630)},
}

# Expected HTML tags
EXPECTED_HTML_TAGS = [
    '<link rel="icon" type="image/svg+xml" href="/favicon.svg">',
    '<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">',
    '<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">',
    '<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">',
    '<link rel="icon" type="image/x-icon" href="/favicon.ico">',
    '<link rel="icon" type="image/png" sizes="192x192" href="/icon-192.png">',
    '<link rel="icon" type="image/png" sizes="512x512" href="/icon-512.png">',
    '<meta property="og:image" content="',
]

def verify_files():
    """Verify all image files exist and have correct dimensions"""
    print("=" * 70)
    print("🔍 VERIFYING FAVICONS AND OG IMAGE")
    print("=" * 70)
    
    all_ok = True
    results = {}
    
    for filename, specs in EXPECTED_FILES.items():
        filepath = os.path.join(OUTPUT_DIR, filename)
        
        if not os.path.exists(filepath):
            print(f"❌ {filename}: FILE NOT FOUND")
            results[filename] = {'status': 'missing', 'error': 'File not found'}
            all_ok = False
            continue
        
        file_size = os.path.getsize(filepath)
        
        try:
            if specs['type'] == 'svg':
                # Verify SVG
                with open(filepath, 'r') as f:
                    content = f.read()
                    if 'viewBox="0 0 512 512"' in content or "viewBox='0 0 512 512'" in content:
                        print(f"✅ {filename}: SVG with 512x512 viewBox ({file_size} bytes)")
                        results[filename] = {'status': 'ok', 'size': file_size, 'type': 'svg'}
                    else:
                        print(f"⚠️  {filename}: SVG found but viewBox might be incorrect ({file_size} bytes)")
                        results[filename] = {'status': 'warning', 'size': file_size, 'type': 'svg'}
                
            elif specs['type'] == 'png':
                # Verify PNG dimensions
                img = Image.open(filepath)
                if img.size == specs['size']:
                    print(f"✅ {filename}: {img.size[0]}x{img.size[1]} ({file_size} bytes)")
                    results[filename] = {'status': 'ok', 'size': file_size, 'dimensions': img.size, 'type': 'png'}
                else:
                    print(f"❌ {filename}: Wrong size {img.size[0]}x{img.size[1]} (expected {specs['size'][0]}x{specs['size'][1]})")
                    results[filename] = {'status': 'error', 'size': file_size, 'dimensions': img.size, 'expected': specs['size'], 'type': 'png'}
                    all_ok = False
                
            elif specs['type'] == 'ico':
                # Verify ICO has multiple sizes
                import subprocess
                result = subprocess.run(['file', filepath], capture_output=True, text=True)
                file_info = result.stdout.strip()
                
                # Check if it contains both 16x16 and 32x32
                has_16 = '16x16' in file_info
                has_32 = '32x32' in file_info
                
                if has_16 and has_32:
                    print(f"✅ {filename}: Multi-size ICO (16x16, 32x32) ({file_size} bytes)")
                    results[filename] = {'status': 'ok', 'size': file_size, 'type': 'ico', 'info': file_info}
                else:
                    print(f"⚠️  {filename}: ICO might be missing sizes ({file_size} bytes)")
                    print(f"    File info: {file_info}")
                    results[filename] = {'status': 'warning', 'size': file_size, 'type': 'ico', 'info': file_info}
        
        except Exception as e:
            print(f"❌ {filename}: Error - {e}")
            results[filename] = {'status': 'error', 'error': str(e)}
            all_ok = False
    
    return all_ok, results

def verify_html():
    """Verify index.html contains all required favicon tags"""
    print("\n" + "=" * 70)
    print("🔍 VERIFYING HTML TAGS")
    print("=" * 70)
    
    html_path = os.path.join(OUTPUT_DIR, 'index.html')
    
    if not os.path.exists(html_path):
        print(f"❌ index.html: FILE NOT FOUND")
        return False, []
    
    with open(html_path, 'r') as f:
        html_content = f.read()
    
    all_ok = True
    found_tags = []
    
    for tag in EXPECTED_HTML_TAGS:
        # For og:image, just check if the meta tag exists
        if 'og:image' in tag:
            if 'og:image' in html_content:
                print(f"✅ OG Image meta tag found")
                found_tags.append('og:image')
            else:
                print(f"❌ OG Image meta tag NOT found")
                all_ok = False
        else:
            if tag in html_content:
                print(f"✅ {tag.strip()}")
                found_tags.append(tag)
            else:
                print(f"❌ MISSING: {tag.strip()}")
                all_ok = False
    
    return all_ok, found_tags

def generate_report():
    """Generate a summary report"""
    print("\n" + "=" * 70)
    print("📊 SUMMARY REPORT")
    print("=" * 70)
    
    files_ok, files_results = verify_files()
    html_ok, found_tags = verify_html()
    
    print("\n" + "-" * 70)
    print("FILES STATUS:")
    print("-" * 70)
    
    for filename, result in files_results.items():
        status_icon = "✅" if result['status'] == 'ok' else ("⚠️" if result['status'] == 'warning' else "❌")
        print(f"{status_icon} {filename}: {result['status'].upper()}")
    
    print("\n" + "-" * 70)
    print("HTML TAGS STATUS:")
    print("-" * 70)
    print(f"✅ Found {len(found_tags)} required tags")
    
    print("\n" + "=" * 70)
    if files_ok and html_ok:
        print("✅ ALL CHECKS PASSED!")
    else:
        print("⚠️  SOME CHECKS FAILED - Review the output above")
    print("=" * 70)
    
    return files_ok and html_ok

if __name__ == "__main__":
    success = generate_report()
    exit(0 if success else 1)
