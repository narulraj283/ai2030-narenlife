#!/usr/bin/env python3
"""
Script to fix the design and layout of ALL non-article pages across Lead the Shift website.
Adds Google Fonts import, page container wrapping, improved heading styles, and component styling.
Version 2: Improved wrapper insertion logic.
"""

import os
import re
from pathlib import Path
from typing import List, Tuple

# Configuration
GOOGLE_FONTS_IMPORT = "@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Playfair+Display:wght@700;800;900&display=swap');"

# CSS for page container
PAGE_CONTAINER_CSS = """
.page-container {
    max-width: 1000px;
    margin: 0 auto;
    padding: 2.5rem 2.5rem 3rem;
}

@media (max-width: 768px) {
    .page-container {
        padding: 1.5rem 1.25rem 2rem;
    }
}

@media (max-width: 480px) {
    .page-container {
        padding: 1rem 1rem 1.5rem;
    }
}
"""

# CSS for heading styles
HEADING_CSS = """
h1 { font-family: var(--font-display); font-size: clamp(1.8rem, 5vw, 2.5rem); font-weight: 900; color: var(--text-dark); margin-bottom: 1.5rem; }
h2 { font-family: var(--font-display); font-size: 1.5rem; font-weight: 800; color: var(--text-dark); margin-top: 2rem; margin-bottom: 1rem; }
h3 { font-family: var(--font-display); font-size: 1.25rem; font-weight: 700; color: var(--teal-800); margin-top: 1.5rem; margin-bottom: 0.75rem; }
"""

# CSS for share bar
SHARE_BAR_CSS = """
.share-bar { display: flex; gap: 0.75rem; align-items: center; margin-bottom: 1.5rem; padding: 1rem 1.25rem; background: var(--bg-section); border-radius: var(--radius); flex-wrap: wrap; }
.share-bar a, .share-bar button { display: inline-flex; align-items: center; padding: 0.5rem 1rem; background: var(--white); border: 1px solid var(--border-light); border-radius: var(--radius-full); font-size: 0.85rem; font-weight: 500; color: var(--text-body); cursor: pointer; transition: all 0.2s; text-decoration: none; }
.share-bar a:hover, .share-bar button:hover { border-color: var(--teal-700); color: var(--teal-700); background: var(--teal-50); text-decoration: none; }
"""

# CSS for entity cards
ENTITY_CARD_CSS = """
.entity-card, .article-card { background: var(--white); border: 1px solid var(--border-light); border-radius: var(--radius-lg); padding: 1.5rem; margin-bottom: 1rem; transition: all 0.2s; }
.entity-card:hover, .article-card:hover { border-color: var(--teal-500); box-shadow: var(--shadow-md); }
.entity-card a, .article-card a { text-decoration: none; }
.entity-pill, .edition-pill { display: inline-block; padding: 0.4rem 0.9rem; border: 1px solid var(--border); border-radius: var(--radius-full); font-size: 0.8rem; font-weight: 500; color: var(--text-body); text-decoration: none; transition: all 0.2s; margin: 0.25rem; }
.entity-pill:hover, .edition-pill:hover { border-color: var(--teal-700); color: var(--teal-700); background: var(--teal-50); text-decoration: none; }
"""

# CSS for filter buttons
FILTER_BTN_CSS = """
.filter-btn, .sort-btn { display: inline-flex; align-items: center; padding: 0.5rem 1rem; background: var(--white); border: 1px solid var(--border); border-radius: var(--radius-full); font-size: 0.85rem; font-weight: 500; color: var(--text-body); cursor: pointer; transition: all 0.2s; }
.filter-btn:hover, .sort-btn:hover { border-color: var(--teal-700); color: var(--teal-700); }
.filter-btn.active, .sort-btn.active { background: var(--teal-800); color: white; border-color: var(--teal-800); }
"""

class HTMLFixer:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.original_content = None
        self.content = None
        self.modified = False

    def read_file(self) -> bool:
        """Read the HTML file."""
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                self.original_content = f.read()
                self.content = self.original_content
            return True
        except Exception as e:
            print(f"Error reading {self.filepath}: {e}")
            return False

    def write_file(self) -> bool:
        """Write the modified HTML file."""
        if not self.modified:
            return True
        try:
            with open(self.filepath, 'w', encoding='utf-8') as f:
                f.write(self.content)
            return True
        except Exception as e:
            print(f"Error writing {self.filepath}: {e}")
            return False

    def add_google_fonts(self) -> bool:
        """Add Google Fonts import to <style> block."""
        # Check if Google Fonts is already present
        if "fonts.googleapis.com" in self.content:
            return True

        # Find the <style> tag and add import after it
        style_match = re.search(r'<style[^>]*>', self.content)
        if not style_match:
            return False

        style_end = style_match.end()

        # Insert the import after the <style> tag
        self.content = (
            self.content[:style_end] + '\n' + GOOGLE_FONTS_IMPORT + '\n' +
            self.content[style_end:]
        )
        self.modified = True
        return True

    def add_page_container_css(self) -> bool:
        """Add page container CSS to the style block."""
        # Check if already present
        if ".page-container" in self.content:
            return True

        # Find where to insert CSS - before closing </style>
        style_close = self.content.rfind('</style>')
        if style_close == -1:
            return False

        self.content = (
            self.content[:style_close] + '\n\n' + PAGE_CONTAINER_CSS + '\n' +
            self.content[style_close:]
        )
        self.modified = True
        return True

    def add_heading_css(self) -> bool:
        """Add heading styles to the style block."""
        # Check if h1 styling is already comprehensive
        if re.search(r'h1\s*\{[^}]*clamp\(1\.8rem', self.content):
            return True

        # Find where to insert CSS - before closing </style>
        style_close = self.content.rfind('</style>')
        if style_close == -1:
            return False

        self.content = (
            self.content[:style_close] + '\n\n' + HEADING_CSS + '\n' +
            self.content[style_close:]
        )
        self.modified = True
        return True

    def add_share_bar_css(self) -> bool:
        """Add share bar CSS to the style block."""
        # Check if already present
        if ".share-bar" in self.content and "gap: 0.75rem" in self.content:
            return True

        # Find where to insert CSS - before closing </style>
        style_close = self.content.rfind('</style>')
        if style_close == -1:
            return False

        self.content = (
            self.content[:style_close] + '\n\n' + SHARE_BAR_CSS + '\n' +
            self.content[style_close:]
        )
        self.modified = True
        return True

    def add_entity_card_css(self) -> bool:
        """Add entity card CSS to the style block."""
        # Check if already present
        if ".entity-card" in self.content and "gap: 1.5rem" not in self.content:
            return True

        # Find where to insert CSS - before closing </style>
        style_close = self.content.rfind('</style>')
        if style_close == -1:
            return False

        self.content = (
            self.content[:style_close] + '\n\n' + ENTITY_CARD_CSS + '\n' +
            self.content[style_close:]
        )
        self.modified = True
        return True

    def add_filter_btn_css(self) -> bool:
        """Add filter button CSS to the style block."""
        # Check if already present
        if ".filter-btn" in self.content and "border-radius: var(--radius-full)" in self.content:
            return True

        # Find where to insert CSS - before closing </style>
        style_close = self.content.rfind('</style>')
        if style_close == -1:
            return False

        self.content = (
            self.content[:style_close] + '\n\n' + FILTER_BTN_CSS + '\n' +
            self.content[style_close:]
        )
        self.modified = True
        return True

    def wrap_content_in_container(self, page_type: str = "generic") -> bool:
        """Wrap content between site-header and site-footer in a page-container div."""
        # Check if already wrapped
        if "<div class=\"page-container\">" in self.content or "article-page-container" in self.content:
            return True

        # Find the closing tag of site-header
        header_match = re.search(r'</header>\s*\n', self.content)
        if not header_match:
            return False

        # Find the opening tag of site-footer
        footer_match = re.search(r'<footer', self.content)
        if not footer_match:
            return False

        # Get positions
        header_end = header_match.end()
        footer_start = footer_match.start()

        # Check for mobile-overlay div after header and skip it if exists
        content_after_header = self.content[header_end:footer_start]

        # Look for skip-link divs, mobile-overlay divs, etc. to skip them
        skip_pattern = r'(<a[^>]*skip-link[^>]*>.*?</a>)|(<div[^>]*mobile-overlay[^>]*>.*?</div>)'
        skip_match = re.search(skip_pattern, content_after_header, re.DOTALL)

        content_start = header_end
        if skip_match:
            # Find where skip elements end
            temp_pos = skip_match.end()
            # Look for the first significant content after
            significant_match = re.search(r'(<(?:section|main|div)[^>]*>)', content_after_header[temp_pos:])
            if significant_match:
                content_start = header_end + temp_pos + significant_match.start()
            else:
                content_start = header_end + temp_pos

        # Find the position of the footer in the updated content
        footer_pos = self.content.find('<footer', content_start)

        # Trim whitespace before footer
        footer_trim_match = re.search(r'\s+<footer', self.content[content_start:footer_pos + 20])
        if footer_trim_match:
            footer_insert_pos = content_start + footer_trim_match.start()
        else:
            footer_insert_pos = footer_pos

        # Insert opening and closing container divs
        self.content = (
            self.content[:content_start] + '\n<div class="page-container">\n' +
            self.content[content_start:footer_insert_pos].rstrip() + '\n' +
            '</div>\n' +
            self.content[footer_insert_pos:]
        )

        self.modified = True
        return True

def process_file(filepath: str, page_type: str = "generic") -> Tuple[bool, str]:
    """Process a single HTML file."""
    if not os.path.exists(filepath):
        return False, f"File not found: {filepath}"

    fixer = HTMLFixer(filepath)

    if not fixer.read_file():
        return False, f"Failed to read: {filepath}"

    # Apply fixes
    fixer.add_google_fonts()
    fixer.add_page_container_css()
    fixer.add_heading_css()

    # Add component-specific CSS
    if "share" in filepath.lower() or "browse" in filepath.lower():
        fixer.add_share_bar_css()

    if "companies" in filepath or "countries" in filepath or "sectors" in filepath:
        fixer.add_entity_card_css()
        fixer.add_filter_btn_css()

    # Wrap content in container
    if not fixer.wrap_content_in_container(page_type):
        print(f"Warning: Could not wrap content in container for {filepath}")

    if not fixer.write_file():
        return False, f"Failed to write: {filepath}"

    if fixer.modified:
        return True, f"Modified: {filepath}"
    else:
        return False, f"Already up to date: {filepath}"

def get_files_to_process() -> Tuple[List[str], dict]:
    """Get all files that need to be processed."""
    base_path = "/tmp/ai2030-repo"
    files = []
    categories = {
        "browse_listing": [],
        "browse_companies": [],
        "browse_countries": [],
        "browse_sectors": [],
        "static_pages": [],
    }

    # Browse listing pages
    listing_pages = [
        "browse/companies.html",
        "browse/countries.html",
        "browse/sectors.html",
        "browse/data.html",
        "browse/guides.html",
        "browse/action-plans.html",
    ]

    for page in listing_pages:
        filepath = os.path.join(base_path, page)
        if os.path.exists(filepath):
            files.append(filepath)
            categories["browse_listing"].append(filepath)

    # Browse entity pages
    entity_dirs = [
        "browse/companies",
        "browse/countries",
        "browse/sectors",
    ]

    for entity_dir in entity_dirs:
        dir_path = os.path.join(base_path, entity_dir)
        if os.path.isdir(dir_path):
            html_files = [f for f in os.listdir(dir_path) if f.endswith('.html')]
            for html_file in html_files:
                filepath = os.path.join(dir_path, html_file)
                files.append(filepath)
                if "companies" in entity_dir:
                    categories["browse_companies"].append(filepath)
                elif "countries" in entity_dir:
                    categories["browse_countries"].append(filepath)
                elif "sectors" in entity_dir:
                    categories["browse_sectors"].append(filepath)

    # Static pages
    static_pages = [
        "about.html",
        "methodology.html",
        "contact.html",
        "privacy.html",
        "terms.html",
        "press.html",
        "government.html",
        "updates.html",
        "search.html",
        "404.html",
        "briefs/index.html",
    ]

    for page in static_pages:
        filepath = os.path.join(base_path, page)
        if os.path.exists(filepath):
            files.append(filepath)
            categories["static_pages"].append(filepath)

    return files, categories

def main():
    """Main execution function."""
    print("=" * 80)
    print("LEAD THE SHIFT - DESIGN AND LAYOUT FIX (V2)")
    print("=" * 80)
    print()

    files, categories = get_files_to_process()

    print(f"Found {len(files)} files to process:")
    print(f"  - Browse listing pages: {len(categories['browse_listing'])}")
    print(f"  - Browse companies: {len(categories['browse_companies'])}")
    print(f"  - Browse countries: {len(categories['browse_countries'])}")
    print(f"  - Browse sectors: {len(categories['browse_sectors'])}")
    print(f"  - Static pages: {len(categories['static_pages'])}")
    print()

    results = {
        "success": 0,
        "skipped": 0,
        "failed": 0,
        "details": {}
    }

    # Process files
    for filepath in files:
        success, message = process_file(filepath)

        # Categorize result
        if "Already up to date" in message:
            results["skipped"] += 1
        elif success:
            results["success"] += 1
        else:
            results["failed"] += 1

        # Store category
        category = "other"
        if "browse/companies" in filepath and "companies.html" != os.path.basename(filepath):
            category = "browse_companies"
        elif "browse/countries" in filepath and "countries.html" != os.path.basename(filepath):
            category = "browse_countries"
        elif "browse/sectors" in filepath and "sectors.html" != os.path.basename(filepath):
            category = "browse_sectors"
        elif "browse/" in filepath:
            category = "browse_listing"
        else:
            category = "static_pages"

        if category not in results["details"]:
            results["details"][category] = []

        results["details"][category].append({
            "file": os.path.basename(filepath),
            "status": "modified" if success else ("skipped" if "Already up to date" in message else "failed"),
            "message": message
        })

    # Print results
    print()
    print("=" * 80)
    print("RESULTS")
    print("=" * 80)
    print()

    print(f"Modified: {results['success']}")
    print(f"Skipped (already up to date): {results['skipped']}")
    print(f"Failed: {results['failed']}")
    print()

    # Print detailed results by category
    category_names = {
        "browse_listing": "Browse Listing Pages",
        "browse_companies": "Browse Company Pages",
        "browse_countries": "Browse Country Pages",
        "browse_sectors": "Browse Sector Pages",
        "static_pages": "Static Pages",
    }

    for category in ["browse_listing", "browse_companies", "browse_countries", "browse_sectors", "static_pages"]:
        if category in results["details"] and results["details"][category]:
            items = results["details"][category]
            modified_count = sum(1 for item in items if item["status"] == "modified")
            skipped_count = sum(1 for item in items if item["status"] == "skipped")
            failed_count = sum(1 for item in items if item["status"] == "failed")

            print(f"{category_names[category]}: {len(items)} total")
            print(f"  Modified: {modified_count}, Skipped: {skipped_count}, Failed: {failed_count}")

    print()
    print("=" * 80)
    print(f"Total files processed: {len(files)}")
    print(f"Total modified: {results['success']}")
    print("=" * 80)

if __name__ == "__main__":
    main()
