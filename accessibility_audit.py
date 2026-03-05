#!/usr/bin/env python3
"""
Comprehensive Accessibility and Usability Audit Script
Tests a representative sample of pages for Google Search Console issues
"""

import os
import sys
import json
import re
import random
from pathlib import Path
from html.parser import HTMLParser
from typing import Dict, List, Set, Tuple
from collections import defaultdict
from datetime import datetime

# Configuration
REPO_PATH = Path('/tmp/ai2030-repo')
SAMPLE_PAGES = {
    'homepage': REPO_PATH / 'index.html',
    'about': REPO_PATH / 'about.html',
    'browse_companies': REPO_PATH / 'browse/companies.html',
    'browse_data': REPO_PATH / 'browse/data.html',
    'browse_sectors': REPO_PATH / 'browse/sectors.html',
    'briefs_index': REPO_PATH / 'briefs/index.html',
}

class AccessibilityParser(HTMLParser):
    """Parse HTML for accessibility violations"""

    def __init__(self):
        super().__init__()
        self.reset_parser()

    def reset_parser(self):
        self.in_head = False
        self.in_style = False
        self.in_body = False
        self.html_lang = None
        self.viewport_meta = False
        self.has_skip_link = False
        self.landmarks = defaultdict(int)
        self.headings = []
        self.forms = defaultdict(list)  # input_id -> labels
        self.links = []
        self.buttons = []
        self.images = []
        self.inline_css = []
        self.style_content = ""
        self.current_heading_level = 0
        self.char_count = 0
        self.file_size = 0
        self.render_blocking = []
        self.has_viewport = False
        self.current_element = None
        self.element_stack = []
        self.last_heading_level = 0
        self.heading_hierarchy_issues = []
        self.viewport_config = None

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        self.element_stack.append((tag, attrs_dict))

        if tag == 'html':
            self.html_lang = attrs_dict.get('lang')

        elif tag == 'meta':
            name = attrs_dict.get('name', '').lower()
            content = attrs_dict.get('content', '')
            if name == 'viewport':
                self.viewport_meta = True
                self.viewport_config = content
                if 'width=device-width' not in content:
                    self.has_viewport = False
                else:
                    self.has_viewport = True

        elif tag == 'head':
            self.in_head = True

        elif tag == 'body':
            self.in_body = True

        elif tag == 'style':
            self.in_style = True

        elif tag == 'script':
            src = attrs_dict.get('src', '')
            if src and not attrs_dict.get('async') and not attrs_dict.get('defer'):
                self.render_blocking.append(src)

        elif tag == 'link':
            rel = attrs_dict.get('rel', '')
            if 'stylesheet' in rel:
                href = attrs_dict.get('href', '')
                if href:
                    self.render_blocking.append(href)

        elif tag in ['main', 'nav', 'header', 'footer', 'aside']:
            role = attrs_dict.get('role', tag)
            self.landmarks[tag] += 1

        elif tag == 'a':
            href = attrs_dict.get('href', '')
            text = attrs_dict.get('title', '')
            self.links.append({
                'href': href,
                'text': text,
                'attrs': attrs_dict
            })
            # Check for "skip to content" link
            if href == '#main' or 'skip' in text.lower():
                self.has_skip_link = True

        elif tag == 'h1':
            self.headings.append((1, attrs_dict))
            self._check_heading_hierarchy(1)

        elif tag == 'h2':
            self.headings.append((2, attrs_dict))
            self._check_heading_hierarchy(2)

        elif tag == 'h3':
            self.headings.append((3, attrs_dict))
            self._check_heading_hierarchy(3)

        elif tag == 'h4':
            self.headings.append((4, attrs_dict))
            self._check_heading_hierarchy(4)

        elif tag == 'h5':
            self.headings.append((5, attrs_dict))
            self._check_heading_hierarchy(5)

        elif tag == 'h6':
            self.headings.append((6, attrs_dict))
            self._check_heading_hierarchy(6)

        elif tag == 'button':
            style = attrs_dict.get('style', '')
            self.buttons.append({
                'type': attrs_dict.get('type', 'button'),
                'style': style,
                'attrs': attrs_dict
            })

        elif tag == 'input':
            input_id = attrs_dict.get('id', '')
            input_type = attrs_dict.get('type', 'text')
            if input_type not in ['hidden', 'submit', 'reset', 'button']:
                self.forms[input_id].append({
                    'type': input_type,
                    'name': attrs_dict.get('name', ''),
                    'has_label': False
                })

        elif tag == 'label':
            label_for = attrs_dict.get('for', '')
            if label_for in self.forms:
                self.forms[label_for][0]['has_label'] = True

        elif tag == 'img':
            alt = attrs_dict.get('alt', '')
            src = attrs_dict.get('src', '')
            self.images.append({
                'src': src,
                'alt': alt,
                'role': attrs_dict.get('role', '')
            })

        elif tag == 'div' or tag == 'span':
            style = attrs_dict.get('style', '')
            if style:
                self.inline_css.append(style)

    def handle_endtag(self, tag):
        if tag == 'style':
            self.in_style = False
        if tag == 'head':
            self.in_head = False
        if tag == 'body':
            self.in_body = False
        if self.element_stack and self.element_stack[-1][0] == tag:
            self.element_stack.pop()

    def handle_data(self, data):
        self.char_count += len(data)
        if self.in_style:
            self.style_content += data

    def _check_heading_hierarchy(self, level):
        """Check for skipped heading levels"""
        if self.last_heading_level == 0:
            self.last_heading_level = level
        else:
            if level > self.last_heading_level + 1:
                self.heading_hierarchy_issues.append(
                    f"Skipped from h{self.last_heading_level} to h{level}"
                )
            self.last_heading_level = level


def analyze_color_contrast(css_content: str, style_attrs: List[str]) -> List[Dict]:
    """Check for potential color contrast issues"""
    issues = []

    # Regex to find color declarations
    color_pattern = r'(?:color|background-color)\s*:\s*([#\w\s(),]+)'

    light_colors = ['white', '#fff', '#ffffff', '#f0f0f0', '#efefef']
    dark_colors = ['black', '#000', '#000000']

    for match in re.finditer(color_pattern, css_content, re.IGNORECASE):
        color = match.group(1).strip().lower()
        # Basic check for light on light or dark on dark combinations
        if any(light in color for light in light_colors):
            issues.append({
                'type': 'potential_light_color',
                'color': color
            })

    return issues


def check_css_size(css_file_path: Path) -> int:
    """Get CSS file size"""
    if css_file_path.exists():
        return css_file_path.stat().st_size
    return 0


def check_touch_targets(css_content: str) -> List[Dict]:
    """Check for potential small touch targets in CSS"""
    issues = []

    # Look for width/height declarations that might be too small
    size_pattern = r'(?:width|height|padding|min-width|min-height)\s*:\s*(\d+)(?:px)?'

    sizes = re.findall(size_pattern, css_content)
    small_sizes = [int(s) for s in sizes if int(s) < 44]

    if small_sizes:
        issues.append({
            'type': 'potentially_small_touch_targets',
            'sizes_found': sorted(set(small_sizes))
        })

    return issues


def audit_page(file_path: Path, page_name: str) -> Dict:
    """Audit a single HTML page"""

    results = {
        'page': page_name,
        'path': str(file_path),
        'exists': file_path.exists(),
        'file_size_kb': 0,
        'findings': {}
    }

    if not file_path.exists():
        results['findings']['error'] = f"File not found: {file_path}"
        return results

    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        html_content = f.read()

    file_size = len(html_content.encode('utf-8'))
    results['file_size_kb'] = round(file_size / 1024, 2)
    results['findings']['file_size_check'] = {
        'pass': file_size < 500 * 1024,
        'size_kb': round(file_size / 1024, 2),
        'issue': 'File exceeds 500KB' if file_size > 500 * 1024 else None
    }

    # Parse HTML
    parser = AccessibilityParser()
    try:
        parser.feed(html_content)
    except Exception as e:
        results['findings']['parse_error'] = str(e)
        return results

    # 1. ARIA Landmarks
    results['findings']['aria_landmarks'] = {
        'pass': len(parser.landmarks) > 0,
        'landmarks_found': dict(parser.landmarks),
        'issues': []
    }
    if 'nav' not in parser.landmarks:
        results['findings']['aria_landmarks']['issues'].append('Missing <nav> element')
    if 'main' not in parser.landmarks:
        results['findings']['aria_landmarks']['issues'].append('Missing <main> element')
    if 'footer' not in parser.landmarks:
        results['findings']['aria_landmarks']['issues'].append('Missing <footer> element')

    # 2. Skip Navigation Link
    results['findings']['skip_nav_link'] = {
        'pass': parser.has_skip_link,
        'issue': 'No "skip to content" link found' if not parser.has_skip_link else None
    }

    # 3. Color Contrast (basic check)
    contrast_issues = analyze_color_contrast(parser.style_content, parser.inline_css)
    results['findings']['color_contrast'] = {
        'pass': len(contrast_issues) == 0,
        'potential_issues': contrast_issues
    }

    # 4. Focus Indicators (check for outline: none)
    has_outline_none = 'outline:none' in parser.style_content or 'outline: none' in parser.style_content
    results['findings']['focus_indicators'] = {
        'pass': not has_outline_none,
        'issue': 'Found "outline: none" which removes focus indicators' if has_outline_none else None
    }

    # 5. Lang Attribute
    results['findings']['lang_attribute'] = {
        'pass': parser.html_lang == 'en',
        'lang_value': parser.html_lang,
        'issue': f'html lang attribute is "{parser.html_lang}", expected "en"' if parser.html_lang != 'en' else None
    }

    # 6. Viewport Meta
    results['findings']['viewport_meta'] = {
        'pass': parser.has_viewport,
        'has_viewport': parser.viewport_meta,
        'config': parser.viewport_config,
        'issue': 'Missing viewport meta or missing width=device-width' if not parser.has_viewport else None
    }

    # 7. Form Labels
    missing_labels = [
        input_id for input_id, forms in parser.forms.items()
        if forms and not forms[0].get('has_label', False)
    ]
    results['findings']['form_labels'] = {
        'pass': len(missing_labels) == 0,
        'total_inputs': len(parser.forms),
        'inputs_without_labels': missing_labels,
        'issue': f'{len(missing_labels)} input(s) without labels' if missing_labels else None
    }

    # 8. Link Text Quality
    bad_links = []
    for link in parser.links:
        href = link.get('href', '')
        text = link.get('text', '').lower()
        if text in ['click here', 'more', 'read more', ''] or not text:
            bad_links.append({
                'href': href,
                'text': text or '(empty)'
            })
    results['findings']['link_text_quality'] = {
        'pass': len(bad_links) == 0,
        'total_links': len(parser.links),
        'poor_links': bad_links,
        'issue': f'{len(bad_links)} link(s) with poor text' if bad_links else None
    }

    # 9. Heading Hierarchy
    results['findings']['heading_hierarchy'] = {
        'pass': len(parser.heading_hierarchy_issues) == 0,
        'total_headings': len(parser.headings),
        'issues': parser.heading_hierarchy_issues,
        'hierarchy': [(level, attrs_dict.get('id', 'N/A')) for level, attrs_dict in parser.headings[:10]]
    }

    # 10. Mobile Responsive
    fixed_width_pattern = r'width\s*:\s*\d+px'
    has_fixed_width = len(re.findall(fixed_width_pattern, parser.style_content)) > 0
    results['findings']['mobile_responsive'] = {
        'pass': parser.has_viewport and not has_fixed_width,
        'has_viewport': parser.has_viewport,
        'has_fixed_widths': has_fixed_width,
        'issue': 'Fixed width CSS or missing viewport' if (not parser.has_viewport or has_fixed_width) else None
    }

    # 11. Page Load Concerns
    results['findings']['page_load_concerns'] = {
        'pass': file_size < 500 * 1024 and len(parser.render_blocking) < 5,
        'file_size_kb': round(file_size / 1024, 2),
        'render_blocking_resources': parser.render_blocking,
        'inline_css_count': len(parser.inline_css),
        'issues': []
    }
    if file_size > 500 * 1024:
        results['findings']['page_load_concerns']['issues'].append('File size exceeds 500KB')
    if len(parser.render_blocking) >= 5:
        results['findings']['page_load_concerns']['issues'].append('Multiple render-blocking resources')

    # 12. Touch Targets
    touch_issues = check_touch_targets(parser.style_content)
    results['findings']['touch_targets'] = {
        'pass': len(touch_issues) == 0,
        'potential_issues': touch_issues,
        'issue': 'Potential small touch targets found' if touch_issues else None
    }

    # Additional: Image Alt Text
    missing_alt = [img for img in parser.images if not img['alt']]
    results['findings']['image_alt_text'] = {
        'pass': len(missing_alt) == 0,
        'total_images': len(parser.images),
        'images_without_alt': len(missing_alt),
        'issue': f'{len(missing_alt)} image(s) without alt text' if missing_alt else None
    }

    return results


def get_random_pages(directory: Path, pattern: str, count: int) -> List[Path]:
    """Get random pages from a directory"""
    pages = list(directory.glob(pattern))
    if len(pages) <= count:
        return pages
    return random.sample(pages, count)


def generate_report(all_results: List[Dict]) -> str:
    """Generate a comprehensive audit report"""

    report = []
    report.append("=" * 80)
    report.append("ACCESSIBILITY AND USABILITY AUDIT REPORT")
    report.append("=" * 80)
    report.append(f"Generated: {datetime.now().isoformat()}")
    report.append(f"Total pages audited: {len(all_results)}\n")

    # Summary Statistics
    report.append("EXECUTIVE SUMMARY")
    report.append("-" * 80)

    issues_by_type = defaultdict(int)
    critical_issues = []

    for result in all_results:
        for check_name, check_result in result['findings'].items():
            if check_name == 'error' or check_name == 'parse_error':
                continue
            if isinstance(check_result, dict) and not check_result.get('pass', True):
                issues_by_type[check_name] += 1
                if check_result.get('issue'):
                    critical_issues.append({
                        'page': result['page'],
                        'check': check_name,
                        'issue': check_result['issue']
                    })

    report.append(f"\nIssues found by category:")
    for check_type in sorted(issues_by_type.keys()):
        count = issues_by_type[check_type]
        report.append(f"  {check_type}: {count} page(s)")

    # Detailed Results
    report.append("\n" + "=" * 80)
    report.append("DETAILED PAGE AUDITS")
    report.append("=" * 80)

    for result in all_results:
        report.append(f"\n{result['page'].upper()}")
        report.append(f"Path: {result['path']}")
        report.append(f"File Size: {result['file_size_kb']} KB")
        report.append("-" * 80)

        for check_name, check_result in result['findings'].items():
            if check_name in ['error', 'parse_error']:
                report.append(f"\nERROR: {check_result}")
                continue

            if not isinstance(check_result, dict):
                continue

            status = "PASS" if check_result.get('pass', True) else "FAIL"
            report.append(f"\n[{status}] {check_name}")

            if check_result.get('issue'):
                report.append(f"    Issue: {check_result['issue']}")

            # Custom output for each check
            if check_name == 'aria_landmarks':
                report.append(f"    Landmarks: {check_result.get('landmarks_found', {})}")
                for issue in check_result.get('issues', []):
                    report.append(f"    - {issue}")

            elif check_name == 'heading_hierarchy':
                report.append(f"    Total headings: {check_result['total_headings']}")
                if check_result['hierarchy']:
                    report.append(f"    Hierarchy sample: {check_result['hierarchy'][:5]}")
                for issue in check_result.get('issues', []):
                    report.append(f"    - {issue}")

            elif check_name == 'link_text_quality':
                report.append(f"    Total links: {check_result['total_links']}")
                if check_result['poor_links']:
                    report.append(f"    Links with poor text: {len(check_result['poor_links'])}")
                    for link in check_result['poor_links'][:3]:
                        report.append(f"      - href='{link['href']}' text='{link['text']}'")

            elif check_name == 'form_labels':
                report.append(f"    Total inputs: {check_result['total_inputs']}")
                if check_result['inputs_without_labels']:
                    report.append(f"    Inputs without labels: {len(check_result['inputs_without_labels'])}")

            elif check_name == 'page_load_concerns':
                report.append(f"    File size: {check_result['file_size_kb']} KB")
                if check_result['render_blocking_resources']:
                    report.append(f"    Render-blocking resources: {len(check_result['render_blocking_resources'])}")
                    for resource in check_result['render_blocking_resources'][:3]:
                        report.append(f"      - {resource}")

            elif check_name == 'image_alt_text':
                report.append(f"    Total images: {check_result['total_images']}")
                report.append(f"    Missing alt text: {check_result['images_without_alt']}")

            elif check_name == 'viewport_meta':
                report.append(f"    Viewport config: {check_result.get('config', 'N/A')}")

            elif check_name == 'color_contrast':
                if check_result['potential_issues']:
                    report.append(f"    Potential issues: {len(check_result['potential_issues'])}")

    # Critical Issues Summary
    if critical_issues:
        report.append("\n" + "=" * 80)
        report.append("CRITICAL ISSUES TO ADDRESS")
        report.append("=" * 80)

        issues_by_page = defaultdict(list)
        for issue in critical_issues:
            issues_by_page[issue['page']].append(issue)

        for page in sorted(issues_by_page.keys()):
            report.append(f"\n{page}:")
            for issue in issues_by_page[page]:
                report.append(f"  - {issue['check']}: {issue['issue']}")

    # Google Search Console Relevant Findings
    report.append("\n" + "=" * 80)
    report.append("GOOGLE SEARCH CONSOLE RELEVANT FINDINGS")
    report.append("=" * 80)

    gsc_issues = []
    for result in all_results:
        page = result['page']
        findings = result['findings']

        if not findings.get('lang_attribute', {}).get('pass', True):
            gsc_issues.append(f"[{page}] Missing or incorrect lang attribute")

        if not findings.get('viewport_meta', {}).get('pass', True):
            gsc_issues.append(f"[{page}] Mobile usability: Missing/incorrect viewport")

        if not findings.get('mobile_responsive', {}).get('pass', True):
            gsc_issues.append(f"[{page}] Not mobile-responsive")

        if findings.get('page_load_concerns', {}).get('file_size_kb', 0) > 500:
            gsc_issues.append(f"[{page}] Large page size ({findings['page_load_concerns']['file_size_kb']} KB)")

        if findings.get('aria_landmarks', {}).get('issues'):
            for issue in findings['aria_landmarks']['issues']:
                gsc_issues.append(f"[{page}] Accessibility: {issue}")

        if not findings.get('heading_hierarchy', {}).get('pass', True):
            gsc_issues.append(f"[{page}] Invalid heading hierarchy")

    if gsc_issues:
        for issue in sorted(set(gsc_issues)):
            report.append(f"  {issue}")
    else:
        report.append("  No critical Google Search Console issues detected")

    report.append("\n" + "=" * 80)

    return "\n".join(report)


def main():
    print("Starting accessibility audit...")
    print(f"Repository: {REPO_PATH}")

    all_results = []

    # Audit sample pages
    print("\n[1/4] Auditing main pages...")
    for page_name, page_path in SAMPLE_PAGES.items():
        result = audit_page(page_path, page_name)
        all_results.append(result)
        print(f"  Audited: {page_name}")

    # Audit random country articles
    print("\n[2/4] Auditing 10 random country articles...")
    country_pages = get_random_pages(
        REPO_PATH / 'browse/countries',
        '*.html',
        10
    )
    for i, page_path in enumerate(country_pages, 1):
        result = audit_page(page_path, f"country_{i}")
        all_results.append(result)
    print(f"  Audited {len(country_pages)} country pages")

    # Audit random sector articles
    print("\n[3/4] Auditing 10 random sector articles...")
    sector_pages = get_random_pages(
        REPO_PATH / 'browse/sectors',
        '*.html',
        10
    )
    for i, page_path in enumerate(sector_pages, 1):
        result = audit_page(page_path, f"sector_{i}")
        all_results.append(result)
    print(f"  Audited {len(sector_pages)} sector pages")

    # Generate report
    print("\n[4/4] Generating report...")
    report = generate_report(all_results)

    # Save report
    report_path = REPO_PATH / 'ACCESSIBILITY_AUDIT.txt'
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)

    # Save JSON results
    json_path = REPO_PATH / 'ACCESSIBILITY_AUDIT.json'
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, indent=2)

    print(f"\nReport saved to: {report_path}")
    print(f"JSON results saved to: {json_path}")
    print("\nAudit complete!")

    # Print summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    total_pages = len(all_results)
    pages_with_issues = sum(1 for r in all_results if not all(
        v.get('pass', True) for k, v in r['findings'].items()
        if isinstance(v, dict) and k != 'error'
    ))
    print(f"Pages audited: {total_pages}")
    print(f"Pages with issues: {pages_with_issues}")
    print(f"Issues-free pages: {total_pages - pages_with_issues}")


if __name__ == '__main__':
    main()
