#!/usr/bin/env python3
"""
Script to standardize navigation across all HTML pages in the repository.
Updates nav links to: Home, Countries, Companies, Sectors, About
Removes: Methodology, Search
Handles multiple nav formats (minified and formatted)
"""

import os
import re
import glob
from pathlib import Path

def fix_nav_in_file(filepath):
    """Fix navigation in a single HTML file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"ERROR reading {filepath}: {e}")
        return False

    original_content = content
    modified = False

    # Pattern 1: Minified nav (no spaces between li tags) - Country articles
    # Old: Home, Countries, Sectors, Methodology, About
    minified_country = r'<li><a href="/">Home</a></li><li><a href="/browse/countries\.html">Countries</a></li><li><a href="/browse/sectors\.html">Sectors</a></li><li><a href="/methodology\.html">Methodology</a></li><li><a href="/about\.html">About</a></li>'
    minified_correct = '<li><a href="/">Home</a></li><li><a href="/browse/countries.html">Countries</a></li><li><a href="/browse/companies.html">Companies</a></li><li><a href="/browse/sectors.html">Sectors</a></li><li><a href="/about.html">About</a></li>'

    if re.search(minified_country, content):
        content = re.sub(minified_country, minified_correct, content)
        modified = True

    # Pattern 2: Minified nav with Search (company/sector articles)
    # Old: Home, Countries, Companies, Sectors, Search, About
    minified_search = r'<li><a href="/">Home</a></li><li><a href="/browse/countries\.html">Countries</a></li><li><a href="/browse/companies\.html">Companies</a></li><li><a href="/browse/sectors\.html">Sectors</a></li><li><a href="/search\.html">Search</a></li><li><a href="/about\.html">About</a></li>'
    minified_correct_nosearch = '<li><a href="/">Home</a></li><li><a href="/browse/countries.html">Countries</a></li><li><a href="/browse/companies.html">Companies</a></li><li><a href="/browse/sectors.html">Sectors</a></li><li><a href="/about.html">About</a></li>'

    if re.search(minified_search, content):
        content = re.sub(minified_search, minified_correct_nosearch, content)
        modified = True

    # Pattern 3: Formatted nav with Search (most company articles)
    # Look for formatted nav structure
    formatted_search = r'<nav class="nav-links">\s*<li><a href="/">Home</a></li>\s*<li><a href="/browse/countries\.html">Countries</a></li>\s*<li><a href="/browse/companies\.html">Companies</a></li>\s*<li><a href="/browse/sectors\.html">Sectors</a></li>\s*<li><a href="/search\.html">Search</a></li>\s*<li><a href="/about\.html">About</a></li>\s*</nav>'
    formatted_correct = '''<nav class="nav-links">
                <li><a href="/">Home</a></li>
                <li><a href="/browse/countries.html">Countries</a></li>
                <li><a href="/browse/companies.html">Companies</a></li>
                <li><a href="/browse/sectors.html">Sectors</a></li>
                <li><a href="/about.html">About</a></li>
            </nav>'''

    if re.search(formatted_search, content):
        content = re.sub(formatted_search, formatted_correct, content)
        modified = True

    # Pattern 4: Minified nav with active class on About
    minified_about_search = r'<li><a href="/">Home</a></li><li><a href="/browse/countries\.html">Countries</a></li><li><a href="/browse/companies\.html">Companies</a></li><li><a href="/browse/sectors\.html">Sectors</a></li><li><a href="/search\.html">Search</a></li><li><a href="/about\.html" class="active">About</a></li>'
    minified_about_correct = '<li><a href="/">Home</a></li><li><a href="/browse/countries.html">Countries</a></li><li><a href="/browse/companies.html">Companies</a></li><li><a href="/browse/sectors.html">Sectors</a></li><li><a href="/about.html" class="active">About</a></li>'

    if re.search(minified_about_search, content):
        content = re.sub(minified_about_search, minified_about_correct, content)
        modified = True

    # Pattern 5: Minified nav with active class on Home
    minified_home_search = r'<li><a href="/" class="active">Home</a></li><li><a href="/browse/countries\.html">Countries</a></li><li><a href="/browse/companies\.html">Companies</a></li><li><a href="/browse/sectors\.html">Sectors</a></li><li><a href="/search\.html">Search</a></li><li><a href="/about\.html">About</a></li>'
    minified_home_correct = '<li><a href="/" class="active">Home</a></li><li><a href="/browse/countries.html">Countries</a></li><li><a href="/browse/companies.html">Companies</a></li><li><a href="/browse/sectors.html">Sectors</a></li><li><a href="/about.html">About</a></li>'

    if re.search(minified_home_search, content):
        content = re.sub(minified_home_search, minified_home_correct, content)
        modified = True

    # Pattern 6: Browse pages might have different structures - look for any nav with Search
    # and remove it, or update list items
    if re.search(r'<li><a href="/search\.html">Search</a></li>', content):
        content = re.sub(r'<li><a href="/search\.html">Search</a></li>\s*', '', content)
        modified = True

    # Pattern 7: Check for old methodology links in nav and remove them
    if re.search(r'<li><a href="/methodology\.html">Methodology</a></li>', content):
        content = re.sub(r'<li><a href="/methodology\.html">Methodology</a></li>\s*', '', content)
        modified = True

    # Only write if content changed
    if modified and content != original_content:
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
            print(f"✓ Fixed: {os.path.basename(filepath)}")
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
