#!/usr/bin/env python3
"""
Script to standardize navigation across all HTML pages in the repository.
Updates nav links to: Home, Countries, Companies, Sectors, About
Removes: Methodology, Search
"""

import os
import re
import glob
from pathlib import Path

# Target navigation pattern (consistent across all pages)
CORRECT_NAV = '<li><a href="/">Home</a></li><li><a href="/browse/countries.html">Countries</a></li><li><a href="/browse/companies.html">Companies</a></li><li><a href="/browse/sectors.html">Sectors</a></li><li><a href="/about.html">About</a></li>'

# Patterns to look for - we need to handle multiple variations
# Pattern 1: Country articles (minified with no spaces)
PATTERN_COUNTRY = r'<li><a href="/">Home</a></li><li><a href="/browse/countries\.html">Countries</a></li><li><a href="/browse/sectors\.html">Sectors</a></li><li><a href="/methodology\.html">Methodology</a></li><li><a href="/about\.html">About</a></li>'

# Pattern 2: Company articles with new style (already has Companies)
PATTERN_COMPANY_NEW = r'<li><a href="/">Home</a></li><li><a href="/browse/countries\.html">Countries</a></li><li><a href="/browse/companies\.html">Companies</a></li><li><a href="/browse/sectors\.html">Sectors</a></li><li><a href="/search\.html">Search</a></li><li><a href="/about\.html">About</a></li>'

# Pattern 3: Sector articles similar to company articles
PATTERN_SECTOR = r'<li><a href="/">Home</a></li><li><a href="/browse/countries\.html">Countries</a></li><li><a href="/browse/companies\.html">Companies</a></li><li><a href="/browse/sectors\.html">Sectors</a></li><li><a href="/search\.html">Search</a></li><li><a href="/about\.html">About</a></li>'

# Pattern 4: About.html with Search
PATTERN_ABOUT = r'<li><a href="/">Home</a></li><li><a href="/browse/countries\.html">Countries</a></li><li><a href="/browse/companies\.html">Companies</a></li><li><a href="/browse/sectors\.html">Sectors</a></li><li><a href="/search\.html">Search</a></li><li><a href="/about\.html" class="active">About</a></li>'

# Pattern 5: Index with Search
PATTERN_INDEX = r'<li><a href="/" class="active">Home</a></li><li><a href="/browse/countries\.html">Countries</a></li><li><a href="/browse/companies\.html">Companies</a></li><li><a href="/browse/sectors\.html">Sectors</a></li><li><a href="/search\.html">Search</a></li><li><a href="/about\.html">About</a></li>'

def fix_nav_in_file(filepath):
    """Fix navigation in a single HTML file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"ERROR reading {filepath}: {e}")
        return False

    original_content = content

    # Try each pattern and replace accordingly
    # Country articles
    if re.search(PATTERN_COUNTRY, content):
        content = re.sub(PATTERN_COUNTRY, CORRECT_NAV, content)
        print(f"✓ Fixed country article: {filepath}")

    # About page - preserve "active" class on About link
    elif re.search(PATTERN_ABOUT, content):
        correct_nav_about = '<li><a href="/">Home</a></li><li><a href="/browse/countries.html">Countries</a></li><li><a href="/browse/companies.html">Companies</a></li><li><a href="/browse/sectors.html">Sectors</a></li><li><a href="/about.html" class="active">About</a></li>'
        content = re.sub(PATTERN_ABOUT, correct_nav_about, content)
        print(f"✓ Fixed about page: {filepath}")

    # Index page - preserve "active" class on Home link
    elif re.search(PATTERN_INDEX, content):
        correct_nav_index = '<li><a href="/" class="active">Home</a></li><li><a href="/browse/countries.html">Countries</a></li><li><a href="/browse/companies.html">Companies</a></li><li><a href="/browse/sectors.html">Sectors</a></li><li><a href="/about.html">About</a></li>'
        content = re.sub(PATTERN_INDEX, correct_nav_index, content)
        print(f"✓ Fixed index page: {filepath}")

    # Company/Sector articles with Search
    elif re.search(PATTERN_COMPANY_NEW, content):
        content = re.sub(PATTERN_COMPANY_NEW, CORRECT_NAV, content)
        print(f"✓ Fixed company/sector article: {filepath}")

    else:
        # Fallback: look for any nav-links pattern and try generic replacement
        # Look for nav pattern with flexible spacing
        nav_pattern = r'<li><a href="/">Home</a></li>.*?<li><a href="/about\.html">About</a></li>'
        if re.search(nav_pattern, content, re.DOTALL):
            # This is tricky - only do if we can be fairly sure
            # For now, skip these files and report them
            print(f"⚠ Skipped (non-standard format): {filepath}")
            return False
        else:
            print(f"⚠ No nav pattern found: {filepath}")
            return False

    # Only write if content changed
    if content != original_content:
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        except Exception as e:
            print(f"ERROR writing {filepath}: {e}")
            return False

    return False

def main():
    repo_root = '/tmp/ai2030-repo'
    files_to_fix = []

    # Find all HTML files
    print("Scanning repository for HTML files...")

    # Root level pages
    root_pages = [
        '/index.html',
        '/about.html',
        '/methodology.html',
        '/404.html',
        '/admin.html',
        '/press.html',
        '/government.html',
        '/updates.html'
    ]

    for page in root_pages:
        full_path = repo_root + page
        if os.path.exists(full_path):
            files_to_fix.append(full_path)

    # Country articles
    country_files = glob.glob(repo_root + '/articles/countries-*.html')
    files_to_fix.extend(country_files)

    # Company articles
    company_files = glob.glob(repo_root + '/articles/companies-*.html')
    files_to_fix.extend(company_files)

    # Sector articles
    sector_files = glob.glob(repo_root + '/articles/sectors-*.html')
    files_to_fix.extend(sector_files)

    # Browse pages (all levels)
    browse_files = glob.glob(repo_root + '/browse/*.html')
    files_to_fix.extend(browse_files)

    browse_subdir_files = glob.glob(repo_root + '/browse/**/*.html', recursive=True)
    files_to_fix.extend(browse_subdir_files)

    files_to_fix = list(set(files_to_fix))  # Remove duplicates

    print(f"\nFound {len(files_to_fix)} HTML files to process.")
    print("=" * 70)

    fixed_count = 0
    skipped_count = 0

    for filepath in sorted(files_to_fix):
        if fix_nav_in_file(filepath):
            fixed_count += 1
        else:
            skipped_count += 1

    print("=" * 70)
    print(f"\nSummary:")
    print(f"  Fixed: {fixed_count} files")
    print(f"  Skipped/No changes: {skipped_count} files")
    print(f"  Total processed: {len(files_to_fix)} files")

if __name__ == '__main__':
    main()
