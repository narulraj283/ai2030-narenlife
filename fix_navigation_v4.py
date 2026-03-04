#!/usr/bin/env python3
"""
Script to standardize navigation across all HTML pages.
Pass 4: Handle sector articles with absolute URLs
"""

import os
import re
import glob

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

    # Handle sector articles with absolute URLs https://ai2030.io/
    # Old: Home, Countries, Companies, Sectors, Search
    if 'https://ai2030.io/' in content:
        # Remove Search link
        content = re.sub(
            r'<li><a href="https://ai2030\.io/search">Search</a></li>\s*',
            '',
            content
        )
        # Ensure About link is there (some might be missing it)
        if 'https://ai2030.io/about' not in content:
            # Add About at the end
            content = re.sub(
                r'(<li><a href="https://ai2030\.io/sectors">Sectors</a></li>)',
                r'\1<li><a href="https://ai2030.io/about">About</a></li>',
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

    print("Scanning repository for sector articles (pass 4)...")

    # Sector articles
    sector_files = glob.glob(repo_root + '/articles/sectors-*.html')
    files_to_fix.extend(sector_files)

    files_to_fix = list(set(files_to_fix))

    print(f"\nFound {len(files_to_fix)} sector files to process.")
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
    print(f"\nPass 4 Summary:")
    print(f"  Additional fixes: {fixed_count} files")
    print(f"  Skipped/No changes: {skipped_count} files")

if __name__ == '__main__':
    main()
