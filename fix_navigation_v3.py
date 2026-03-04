#!/usr/bin/env python3
"""
Script to standardize navigation across all HTML pages.
More robust approach: find and update nav items individually.
"""

import os
import re
import glob

def normalize_whitespace_in_nav(content):
    """Helper to handle variable whitespace in nav patterns."""
    # This replaces any variation of spacing in nav links
    content = re.sub(r'(<li><a href="/browse/sectors\.html">Sectors</a></li>)\s*(<li><a href="/methodology\.html">Methodology</a></li>)', r'\1', content)
    return content

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

    # First, let's handle country articles with the complex pattern
    # They may have Methodology that needs to be removed, and missing Companies

    # Pattern: Sectors...Methodology...About (with any whitespace)
    if 'browse/sectors.html">Sectors' in content and 'methodology.html">Methodology' in content:
        # Find and remove methodology link
        content = re.sub(
            r'(<li><a href="/browse/sectors\.html">Sectors</a></li>)\s*<li><a href="/methodology\.html">Methodology</a></li>',
            r'\1',
            content
        )
        modified = True

    # Now ensure Companies is in the nav
    # Pattern: Countries...Sectors
    if 'browse/countries.html">Countries' in content and 'browse/sectors.html">Sectors' in content:
        # Check if Companies is missing (i.e., there's no /browse/companies in nav)
        # But be careful not to match links in breadcrumbs etc
        nav_sections = re.findall(r'<nav[^>]*>.*?</nav>', content, re.DOTALL)

        for nav_section in nav_sections:
            if '<ul class="nav-links">' in nav_section and 'browse/countries.html' in nav_section:
                if 'browse/companies.html' not in nav_section:
                    # Add Companies after Countries
                    updated_nav = re.sub(
                        r'(<li><a href="/browse/countries\.html">Countries</a></li>)\s*(<li><a href="/browse/sectors\.html">)',
                        r'\1<li><a href="/browse/companies.html">Companies</a></li>\2',
                        nav_section
                    )
                    if updated_nav != nav_section:
                        content = content.replace(nav_section, updated_nav)
                        modified = True

    # Remove Search links from all nav sections
    if '/search.html' in content:
        # Find and remove Search nav links (be specific to nav context)
        content = re.sub(
            r'<li><a href="/search\.html">Search</a></li>\s*',
            '',
            content
        )
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

    # Article files
    country_files = glob.glob(repo_root + '/articles/countries-*.html')
    company_files = glob.glob(repo_root + '/articles/companies-*.html')
    sector_files = glob.glob(repo_root + '/articles/sectors-*.html')

    files_to_fix.extend(country_files)
    files_to_fix.extend(company_files)
    files_to_fix.extend(sector_files)

    # Browse pages
    browse_files = glob.glob(repo_root + '/browse/*.html')
    browse_subdir_files = glob.glob(repo_root + '/browse/**/*.html', recursive=True)

    files_to_fix.extend(browse_files)
    files_to_fix.extend(browse_subdir_files)

    files_to_fix = list(set(files_to_fix))

    print(f"\nFound {len(files_to_fix)} HTML files to process (pass 2).")
    print("=" * 70)

    fixed_count = 0
    skipped_count = 0

    for filepath in sorted(files_to_fix):
        if fix_nav_in_file(filepath):
            rel_path = os.path.relpath(filepath, repo_root)
            print(f"✓ Fixed: {rel_path}")
            fixed_count += 1
        else:
            skipped_count += 1

    print("=" * 70)
    print(f"\nPass 2 Summary:")
    print(f"  Additional fixes: {fixed_count} files")
    print(f"  Skipped/No changes: {skipped_count} files")
    print(f"  Total processed: {len(files_to_fix)} files")

if __name__ == '__main__':
    main()
