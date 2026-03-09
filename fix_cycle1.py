#!/usr/bin/env python3
"""
Fix Cycle 1: Fixes for Test Cycle 1 audit issues
1. Apply light theme redesign to 11 static pages with dark theme remnants
2. Fix 66 broken internal links
3. Ensure all pages have proper fonts
"""

import os
import re
from pathlib import Path

# CSS for light theme (from about.html and index.html)
LIGHT_THEME_CSS = """
:root {
    --white: #ffffff; --bg: #f9fafb; --bg-section: #f0f4f3; --card-bg: #ffffff;
    --border: #e2e8f0; --border-light: #eef2f1;
    --teal-900: #0f4c3a; --teal-800: #155e4a; --teal-700: #1a7a5e; --teal-600: #1f9d76; --teal-100: #e6f5f0; --teal-50: #f0faf6;
    --coral: #e8734a; --coral-dark: #d4623b; --coral-light: #fef0eb;
    --text-dark: #1a202c; --text-body: #4a5568; --text-muted: #718096; --text-light: #a0aec0;
    --font-display: 'Playfair Display', Georgia, serif;
    --font-body: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    --radius: 12px; --radius-lg: 16px; --radius-full: 9999px;
    --shadow-sm: 0 1px 3px rgba(0,0,0,0.06); --shadow-md: 0 4px 16px rgba(0,0,0,0.08);
    --max-width: 1200px;
}
* { margin: 0; padding: 0; box-sizing: border-box; }
html { scroll-behavior: smooth; }
body { font-family: var(--font-body); background: var(--white); color: var(--text-body); line-height: 1.7; -webkit-font-smoothing: antialiased; }

.site-header { position: sticky; top: 0; z-index: 100; background: rgba(255,255,255,0.96); backdrop-filter: blur(12px); border-bottom: 1px solid var(--border); padding: 0 2rem; }
.header-inner { max-width: var(--max-width); margin: 0 auto; display: flex; align-items: center; justify-content: space-between; height: 68px; }
.site-logo { display: flex; align-items: center; gap: 10px; text-decoration: none; color: var(--text-dark); }
.logo-icon { width: 36px; height: 36px; background: var(--teal-800); border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 11px; color: white; font-weight: 800; }
.logo-text { font-weight: 700; font-size: 1.15rem; color: var(--text-dark); line-height: 1.2; }
.logo-text span { color: var(--teal-700); }
.nav-links { display: flex; gap: 4px; list-style: none; align-items: center; }
.nav-links a { color: var(--text-body); text-decoration: none; padding: 8px 16px; border-radius: var(--radius-full); font-size: 0.9rem; font-weight: 500; transition: all 0.2s; }
.nav-links a:hover { color: var(--teal-800); background: var(--teal-50); }
.nav-cta { color: var(--coral) !important; font-weight: 600 !important; }
.nav-toggle { display: none; background: none; border: none; color: var(--text-dark); font-size: 1.5rem; cursor: pointer; padding: 8px; }

.page-hero { padding: 4rem 2rem 3rem; text-align: center; background: linear-gradient(180deg, var(--teal-50) 0%, var(--white) 100%); }
.page-hero h1 { font-family: var(--font-display); font-size: clamp(2rem, 4vw, 3rem); font-weight: 900; color: var(--text-dark); margin-bottom: 1rem; }
.page-hero .lead { font-size: 1.15rem; color: var(--text-muted); max-width: 700px; margin: 0 auto; }

.content { max-width: 800px; margin: 0 auto; padding: 3rem 2rem 5rem; }
.content h2 { font-family: var(--font-display); font-size: 1.6rem; font-weight: 800; color: var(--text-dark); margin: 2.5rem 0 1rem; }
.content h2:first-of-type { margin-top: 0; }
.content p { margin-bottom: 1.25rem; font-size: 1.05rem; line-height: 1.8; }
.content .highlight { background: var(--teal-50); border-left: 4px solid var(--teal-700); padding: 1.5rem 2rem; border-radius: 0 var(--radius) var(--radius) 0; margin: 2rem 0; font-size: 1.05rem; color: var(--text-dark); }

.stats-bar { display: flex; gap: 2rem; justify-content: center; flex-wrap: wrap; padding: 2rem; background: var(--bg-section); border-radius: var(--radius-lg); margin: 2rem 0; }
.stat { text-align: center; }
.stat strong { display: block; font-size: 1.8rem; color: var(--teal-800); font-weight: 800; }
.stat span { font-size: 0.85rem; color: var(--text-muted); }

.site-footer { background: #1a2332; color: #a0aec0; padding: 3rem 2rem 2rem; }
.footer-inner { max-width: var(--max-width); margin: 0 auto; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem; }
.footer-legal { font-size: 0.8rem; color: #4a5568; }
.footer-legal a { color: #718096; text-decoration: none; }
.footer-legal a:hover { color: white; }

@media (max-width: 768px) {
    .nav-links { display: none; position: fixed; top: 68px; left: 0; right: 0; background: white; flex-direction: column; padding: 1rem; border-bottom: 1px solid var(--border); z-index: 99; }
    .nav-links.active { display: flex; }
    .nav-toggle { display: block; }
    .content { padding: 2rem 1.5rem 3rem; }
    .stats-bar { flex-direction: column; gap: 1rem; }
}
"""

# Header HTML (from about.html)
HEADER_HTML = """<header class="site-header">
    <div class="header-inner">
        <a href="/" class="site-logo">
            <div class="logo-icon">LTS</div>
            <div class="logo-text">Lead the <span>Shift</span></div>
        </a>
        <nav>
            <ul class="nav-links" id="navLinks">
                <li><a href="/browse/countries.html">Countries</a></li>
                <li><a href="/browse/companies.html">Companies</a></li>
                <li><a href="/browse/sectors.html">Sectors</a></li>
                <li><a href="/methodology.html">Methodology</a></li>
                <li><a href="/about.html">About</a></li>
                <li><a href="/browse/data.html" class="nav-cta">Browse All &#8595;</a></li>
            </ul>
        </nav>
        <button class="nav-toggle" aria-label="Menu" onclick="document.getElementById('navLinks').classList.toggle('active')">&#9776;</button>
    </div>
</header>"""

# Footer HTML (simplified from index.html)
FOOTER_HTML = """<footer class="site-footer">
    <div class="footer-inner">
        <a href="/" style="display:flex;align-items:center;gap:10px;text-decoration:none">
            <div style="width:32px;height:32px;background:#1a7a5e;border-radius:6px;display:flex;align-items:center;justify-content:center;font-size:10px;color:white;font-weight:800">LTS</div>
            <span style="color:white;font-weight:700;font-size:1.1rem">Lead the <span style="color:#1f9d76">Shift</span></span>
        </a>
        <p class="footer-legal">&copy; Lead the Shift. All rights reserved. | <a href="/privacy.html">Privacy</a> &bull; <a href="/terms.html">Terms</a> &bull; <a href="/contact.html">Contact</a></p>
    </div>
</footer>"""

# Fonts link
FONTS_LINK = '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Playfair+Display:wght@700;800;900&display=swap" rel="stylesheet">'

# Link mappings for broken links
LINK_FIXES = {
    # Europe CEO edition doesn't exist - remove references (21 occurrences)
    '/articles/countries-europe-europe-ceo-edition.html': None,

    # United States - old path should map to browse version
    '/browse/countries/united-states.html': '/browse/countries/us.html',

    # Government edition pages - fix naming pattern
    '/articles/countries-south-korea-south-korea-government.html': '/articles/countries-south-korea-south-korea-government-edition.html',
    '/articles/countries-poland-poland-government.html': '/articles/countries-poland-poland-government-edition.html',
    '/articles/countries-saudi-arabia-saudi-arabia-government.html': '/articles/countries-saudi-arabia-saudi-arabia-government-edition.html',
    '/articles/countries-mexico-mexico-government.html': '/articles/countries-mexico-mexico-government-edition.html',
    '/articles/countries-brazil-brazil-government.html': '/articles/countries-brazil-brazil-government-edition.html',
}

def get_header():
    """Return header HTML."""
    return HEADER_HTML

def get_footer():
    """Return footer HTML."""
    return FOOTER_HTML

def get_css():
    """Return CSS for light theme."""
    return LIGHT_THEME_CSS

def extract_content_body(html_content, filename):
    """Extract the main content body while preserving original structure."""
    # For pages with class="content", extract that
    content_match = re.search(r'<div class="content"[^>]*>(.*?)</div>\s*(?:<footer|</body)', html_content, re.DOTALL)
    if content_match:
        return '<div class="content">' + content_match.group(1) + '</div>'

    # For article pages, extract article-content
    article_match = re.search(r'<article class="article-content"[^>]*>(.*?)</article>', html_content, re.DOTALL)
    if article_match:
        return '<article class="article-content">' + article_match.group(1) + '</article>'

    # For pages with article-page wrapper
    article_page_match = re.search(r'<main class="article-page"[^>]*>(.*?)</main>', html_content, re.DOTALL)
    if article_page_match:
        return '<main class="article-page">' + article_page_match.group(1) + '</main>'

    # Fallback: find everything between last header and footer
    header_end = html_content.rfind('</header>')
    footer_start = html_content.find('<footer')
    if header_end > 0 and footer_start > header_end:
        return html_content[header_end + len('</header>'):footer_start].strip()

    return ""

def fix_page_theme(filepath):
    """Apply light theme to a page with dark theme."""
    print(f"  Fixing theme for {os.path.basename(filepath)}...")

    with open(filepath, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Extract original content
    body_content = extract_content_body(html_content, filepath)

    # Extract title from original
    title_match = re.search(r'<title>([^<]+)</title>', html_content)
    title = title_match.group(1) if title_match else "Lead the Shift"

    # Check for GA tag
    has_ga = 'googletagmanager.com/gtag/js' in html_content

    # Reconstruct with light theme
    new_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-S9Z93KZ2Z2"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag("js",new Date());gtag("config","G-S9Z93KZ2Z2");</script>
<title>{title}</title>
{FONTS_LINK}
<style>
{get_css()}
</style>
</head>
<body>

{get_header()}

{body_content}

{get_footer()}

</body>
</html>
"""

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_html)

    return True

def fix_broken_links(filepath):
    """Fix broken internal links in a file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content
    fixes_made = []

    for broken_link, correct_link in LINK_FIXES.items():
        # Handle quoted links
        pattern = re.escape(broken_link)

        if correct_link is None:
            # Remove the broken link entirely - find the surrounding container and remove it
            # For Europe CEO edition links which appear in specific containers
            if 'countries-europe-europe-ceo-edition' in broken_link:
                # Remove the entire related-report container
                container_pattern = r'<a href="[^"]*countries-europe-europe-ceo-edition[^"]*"[^>]*>[^<]*(?:<div[^>]*>[^<]*</div>)*[^<]*</a>'
                matches = re.findall(container_pattern, content, re.DOTALL)
                for match in matches:
                    content = content.replace(match, '')
                    fixes_made.append(f"Removed broken Europe CEO link (1 occurrence)")
        else:
            # Replace with correct link
            new_content = re.sub(f'href=["\']({pattern})["\']', f'href="{correct_link}"', content)
            if new_content != content:
                count = len(re.findall(pattern, content))
                content = new_content
                fixes_made.append(f"Fixed {broken_link} -> {correct_link} ({count} occurrences)")

    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return fixes_made

    return []

def main():
    """Main fix script."""
    os.chdir('/tmp/ai2030-repo')

    print("Starting Fix Cycle 1...")
    print()

    # Pages to fix with light theme
    pages_to_fix = [
        'privacy.html',
        'terms.html',
        'press.html',
        'government.html',
        'methodology.html',
        'contact.html',
        '404.html',
        'updates.html',
        'search.html',
        'browse/action-plans.html',
        'browse/guides.html',
    ]

    print("=== ISSUE 1: Fixing Dark Theme Remnants ===")
    theme_fixes = 0
    for page in pages_to_fix:
        filepath = Path(page)
        if filepath.exists():
            try:
                fix_page_theme(str(filepath))
                theme_fixes += 1
            except Exception as e:
                print(f"  ERROR fixing {page}: {e}")
        else:
            print(f"  SKIPPED {page}: File not found")

    print(f"Successfully fixed {theme_fixes}/{len(pages_to_fix)} pages")
    print()

    # Fix broken links across all files
    print("=== ISSUE 2: Fixing Broken Internal Links ===")

    total_link_fixes = 0
    all_html_files = list(Path('.').rglob('*.html'))

    for html_file in all_html_files:
        # Skip script files and generated files
        if 'batch' in str(html_file) or 'rewrite' in str(html_file) or 'qa_audit' in str(html_file):
            continue

        fixes = fix_broken_links(str(html_file))
        if fixes:
            total_link_fixes += len(fixes)
            print(f"{html_file}:")
            for fix in fixes:
                print(f"  - {fix}")

    print()
    print(f"Fixed {total_link_fixes} broken link issues across all files")
    print()

    print("=== ISSUE 3: Checking Google Fonts ===")
    fonts_check = 0
    for page in pages_to_fix:
        filepath = Path(page)
        if filepath.exists():
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            if 'fonts.googleapis.com' in content and 'Inter' in content and 'Playfair' in content:
                fonts_check += 1

    print(f"Google Fonts link verified in {fonts_check}/{len(pages_to_fix)} fixed pages")
    print()

    print("=== SUMMARY ===")
    print(f"Pages with light theme applied: {theme_fixes}")
    print(f"Broken link fixes applied: {total_link_fixes}")
    print(f"Pages with correct fonts: {fonts_check}")
    print()
    print("Fix Cycle 1 Complete!")

if __name__ == '__main__':
    main()
