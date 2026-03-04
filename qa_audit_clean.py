#!/usr/bin/env python3
"""
Comprehensive QA Audit for AI2030 Repository - CLEAN VERSION
Focus on ACTUAL issues, not intentional design elements
"""

import os
import re
import json
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse
from collections import defaultdict
import xml.etree.ElementTree as ET

# Configuration
REPO_PATH = Path("/tmp/ai2030-repo")
EXPECTED_SECTORS = 80
EXPECTED_COMPANIES = 142
EXPECTED_NAV = ["Home", "Countries", "Companies", "Sectors", "About"]
GA4_TRACKING_ID = "G-S9Z93KZ2Z2"

# These are intentionally missing (audience variations that aren't created)
INTENTIONALLY_MISSING_PATTERNS = [
    r"-employee.*\.html",
    r"-investor.*\.html",
    r"-[a-z-]+-edition\.html(?!.*ceo-edition)",  # All but CEO editions
]

report = {
    "summary": {},
    "critical": [],
    "warnings": [],
    "info": [],
    "inventory": {},
}

class HTMLLinkExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.meta_tags = {}
        self.title = ""
        self.has_ga4 = False
        self.has_schema = False
        self.text_content = ""
        self.in_script = False
        self.script_content = ""
        self.current_text = []

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == "a":
            href = attrs_dict.get("href")
            if href:
                self.links.append(href)
        elif tag == "meta":
            name = attrs_dict.get("name", "")
            property = attrs_dict.get("property", "")
            content = attrs_dict.get("content", "")
            if name:
                self.meta_tags[name] = content
            if property:
                self.meta_tags[property] = content
        elif tag == "script":
            self.in_script = True
            src = attrs_dict.get("src", "")
            if "gtag" in src or "analytics" in src:
                self.has_ga4 = True

    def handle_endtag(self, tag):
        if tag == "script":
            self.in_script = False
            if GA4_TRACKING_ID in self.script_content:
                self.has_ga4 = True
            self.script_content = ""

    def handle_data(self, data):
        if self.in_script:
            self.script_content += data
            if GA4_TRACKING_ID in self.script_content:
                self.has_ga4 = True
            if '"@context"' in self.script_content:
                self.has_schema = True
        else:
            self.current_text.append(data)

    def finalize_text(self):
        self.text_content = "".join(self.current_text)

def extract_html_content(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        parser = HTMLLinkExtractor()
        parser.feed(content)
        parser.finalize_text()

        title_match = re.search(r'<title[^>]*>([^<]+)</title>', content, re.IGNORECASE)
        parser.title = title_match.group(1) if title_match else ""

        return parser
    except Exception as e:
        return None

def get_all_html_files():
    html_files = []
    for root, dirs, files in os.walk(REPO_PATH):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['__pycache__']]
        for file in files:
            if file.endswith('.html'):
                html_files.append(Path(root) / file)
    return sorted(html_files)

def is_intentionally_missing(link):
    """Check if a link is intentionally missing"""
    for pattern in INTENTIONALLY_MISSING_PATTERNS:
        if re.search(pattern, link):
            return True
    return False

def resolve_link(link, current_file_path):
    if not link or link.startswith(('http', 'mailto:', 'tel:', '#', 'javascript:')):
        return None

    link_path = link.split('#')[0]
    if not link_path:
        return None

    if link.startswith('/'):
        full_path = REPO_PATH / link.lstrip('/')
    else:
        full_path = (current_file_path.parent / link_path).resolve()

    if full_path.exists():
        return full_path

    if not str(full_path).endswith('.html') and (full_path.with_suffix('.html')).exists():
        return full_path.with_suffix('.html')

    if full_path.is_dir() and (full_path / 'index.html').exists():
        return full_path / 'index.html'

    return None

def check_broken_links():
    """Check for ACTUAL broken links (excluding intentionally missing)"""
    html_files = get_all_html_files()
    broken = []

    for html_file in html_files:
        parser = extract_html_content(html_file)
        if not parser:
            continue

        for link in parser.links:
            if not link or link.startswith(('http', 'mailto:', 'tel:', '#', 'javascript:')):
                continue

            # Skip intentionally missing links
            if is_intentionally_missing(link):
                continue

            # Check if link resolves
            if resolve_link(link, html_file) is None:
                broken.append({
                    "file": str(html_file.relative_to(REPO_PATH)),
                    "broken_link": link,
                    "severity": "CRITICAL"
                })

    return broken

def check_seo():
    """Check SEO elements"""
    html_files = get_all_html_files()
    issues = []

    for html_file in html_files:
        parser = extract_html_content(html_file)
        if not parser:
            continue

        file_issues = []

        if not parser.title or len(parser.title) < 3:
            file_issues.append("Title too short or missing")

        if "description" not in parser.meta_tags:
            file_issues.append("Missing <meta name='description'>")

        if "og:title" not in parser.meta_tags:
            file_issues.append("Missing og:title")

        if "og:description" not in parser.meta_tags:
            file_issues.append("Missing og:description")

        if "canonical" not in parser.meta_tags:
            file_issues.append("Missing canonical URL")

        if not parser.has_ga4 and '404' not in str(html_file) and 'admin' not in str(html_file):
            file_issues.append(f"Missing GA4 tracking")

        if file_issues:
            issues.append({
                "file": str(html_file.relative_to(REPO_PATH)),
                "issues": file_issues,
                "severity": "WARNING"
            })

    return issues

def check_file_inventory():
    """Verify file counts"""
    html_files = get_all_html_files()
    inventory = {
        "total_html_files": len(html_files),
        "countries": 0,
        "companies": 0,
        "sectors": 0,
        "browse_pages": 0,
        "root_pages": 0,
        "other": 0
    }

    for html_file in html_files:
        rel_path = str(html_file.relative_to(REPO_PATH))

        if "articles/countries-" in rel_path:
            inventory["countries"] += 1
        elif "articles/companies-" in rel_path and "employee" not in rel_path and "investor" not in rel_path:
            inventory["companies"] += 1
        elif "articles/sectors-" in rel_path:
            inventory["sectors"] += 1
        elif rel_path.startswith("browse/"):
            inventory["browse_pages"] += 1
        elif rel_path.count('/') == 0:
            inventory["root_pages"] += 1
        else:
            inventory["other"] += 1

    return inventory

def check_content_quality():
    """Check word count for sector articles"""
    issues = []
    articles_dir = REPO_PATH / "articles"

    if articles_dir.exists():
        for html_file in articles_dir.glob("sectors-*.html"):
            parser = extract_html_content(html_file)
            if not parser:
                continue

            word_count = len(parser.text_content.split())
            if word_count < 1500:
                issues.append({
                    "file": str(html_file.relative_to(REPO_PATH)),
                    "issue": f"Low word count: {word_count} words (expected 1500+)",
                    "severity": "WARNING"
                })

            # Check for placeholders
            if any(p in parser.text_content for p in ["[TODO]", "{placeholder}", "Lorem ipsum"]):
                issues.append({
                    "file": str(html_file.relative_to(REPO_PATH)),
                    "issue": "Contains placeholder text",
                    "severity": "WARNING"
                })

    return issues

def check_sitemap():
    """Verify sitemap"""
    issues = []
    sitemap_path = REPO_PATH / "sitemap.xml"

    if not sitemap_path.exists():
        issues.append({
            "file": "sitemap.xml",
            "issue": "sitemap.xml not found",
            "severity": "CRITICAL"
        })
        return issues

    try:
        tree = ET.parse(sitemap_path)
        root = tree.getroot()
        ns = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

        sitemap_urls = set()
        for url in root.findall('ns:url', ns):
            loc = url.find('ns:loc', ns)
            if loc is not None and loc.text:
                path = urlparse(loc.text).path.lstrip('/')
                sitemap_urls.add(path)

        # Check for broken URLs in sitemap
        broken_count = 0
        for url in sitemap_urls:
            if not (REPO_PATH / url).exists():
                broken_count += 1
                if broken_count <= 3:
                    issues.append({
                        "file": "sitemap.xml",
                        "issue": f"Points to missing file: {url}",
                        "severity": "CRITICAL"
                    })

        if broken_count > 3:
            issues.append({
                "file": "sitemap.xml",
                "issue": f"... and {broken_count - 3} more broken sitemap entries",
                "severity": "CRITICAL"
            })

        # Check for missing from sitemap
        html_files = get_all_html_files()
        missing_count = 0
        for html_file in html_files:
            rel_path = str(html_file.relative_to(REPO_PATH))
            if '404' not in rel_path and 'admin' not in rel_path and rel_path not in sitemap_urls:
                missing_count += 1

        if missing_count > 0:
            issues.append({
                "file": "sitemap.xml",
                "issue": f"{missing_count} existing files not in sitemap",
                "severity": "WARNING"
            })

    except Exception as e:
        issues.append({
            "file": "sitemap.xml",
            "issue": f"Error parsing: {str(e)}",
            "severity": "WARNING"
        })

    return issues

def run_audit():
    print("Running comprehensive QA audit...\n")

    print("1. Checking for broken links...")
    broken_links = check_broken_links()

    print("2. Checking SEO elements...")
    seo_issues = check_seo()

    print("3. Verifying file inventory...")
    inventory = check_file_inventory()

    print("4. Checking content quality...")
    content_issues = check_content_quality()

    print("5. Checking sitemap...")
    sitemap_issues = check_sitemap()

    # Organize issues
    all_issues = broken_links + seo_issues + content_issues + sitemap_issues

    for issue in all_issues:
        severity = issue.get("severity", "INFO")
        if severity == "CRITICAL":
            report["critical"].append(issue)
        elif severity == "WARNING":
            report["warnings"].append(issue)

    report["inventory"] = inventory
    report["summary"] = {
        "critical_issues": len(report["critical"]),
        "warnings": len(report["warnings"]),
        "total_issues": len(report["critical"]) + len(report["warnings"]),
        "files_analyzed": inventory["total_html_files"]
    }

    return report

def generate_markdown_report(r):
    lines = []
    lines.append("# AI2030 QA Audit Report")
    lines.append("")
    lines.append("## Executive Summary")
    lines.append("")
    lines.append(f"- **Files Analyzed:** {r['summary']['files_analyzed']}")
    lines.append(f"- **Critical Issues:** {r['summary']['critical_issues']}")
    lines.append(f"- **Warnings:** {r['summary']['warnings']}")
    lines.append(f"- **Total Issues:** {r['summary']['total_issues']}")
    lines.append("")

    # Inventory check
    lines.append("## File Inventory")
    lines.append("")
    inv = r["inventory"]

    company_ok = "✓ PASS" if inv['companies'] == EXPECTED_COMPANIES else "✗ FAIL"
    sector_ok = "✓ PASS" if inv['sectors'] == EXPECTED_SECTORS else "✗ FAIL"

    lines.append(f"| Metric | Count | Expected | Status |")
    lines.append(f"|--------|-------|----------|--------|")
    lines.append(f"| Total HTML Files | {inv['total_html_files']} | - | - |")
    lines.append(f"| Country Articles | {inv['countries']} | - | - |")
    lines.append(f"| Company Articles | {inv['companies']} | {EXPECTED_COMPANIES} | {company_ok} |")
    lines.append(f"| Sector Articles | {inv['sectors']} | {EXPECTED_SECTORS} | {sector_ok} |")
    lines.append(f"| Browse Pages | {inv['browse_pages']} | - | - |")
    lines.append(f"| Root Pages | {inv['root_pages']} | - | - |")
    lines.append("")

    # Critical Issues
    if r["critical"]:
        lines.append("## Critical Issues")
        lines.append("")

        # Group by type
        broken = [i for i in r["critical"] if "broken_link" in i]
        other = [i for i in r["critical"] if "issue" in i]

        if broken:
            lines.append(f"### Broken Links ({len(broken)} issues)")
            lines.append("")
            for i in broken[:5]:
                lines.append(f"**File:** {i['file']}")
                lines.append(f"```")
                lines.append(f"{i['broken_link']}")
                lines.append(f"```")
                lines.append("")
            if len(broken) > 5:
                lines.append(f"*... and {len(broken) - 5} more broken links*")
                lines.append("")

        if other:
            lines.append(f"### Format/Structure Issues ({len(other)} issues)")
            lines.append("")
            for i in other:
                lines.append(f"- **{i['file']}** - {i['issue']}")
            lines.append("")

    # Warnings
    if r["warnings"]:
        lines.append(f"## Warnings ({len(r['warnings'])} issues)")
        lines.append("")

        # Group by category
        seo = [i for i in r["warnings"] if "issues" in i]
        other = [i for i in r["warnings"] if "issue" in i]

        if seo:
            lines.append(f"### SEO Issues ({len(seo)} files)")
            lines.append("")
            for i in seo[:3]:
                lines.append(f"**{i['file']}**")
                for iss in i.get("issues", [])[:2]:
                    lines.append(f"- {iss}")
            if len(seo) > 3:
                lines.append(f"\n*... and {len(seo) - 3} more files*")
            lines.append("")

        if other:
            lines.append(f"### Other Issues ({len(other)} issues)")
            lines.append("")
            for i in other[:5]:
                lines.append(f"- **{i['file']}** - {i['issue']}")
            if len(other) > 5:
                lines.append(f"\n*... and {len(other) - 5} more*")
            lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("**Audit Date:** 2026-03-04")
    lines.append("**Total Checks:** 5")

    return "\n".join(lines)

if __name__ == "__main__":
    audit_report = run_audit()

    # Save reports
    with open(REPO_PATH / "qa_audit_report.json", 'w') as f:
        json.dump(audit_report, f, indent=2)

    md_content = generate_markdown_report(audit_report)
    with open(REPO_PATH / "QA_REPORT.md", 'w') as f:
        f.write(md_content)

    print("\n" + "="*70)
    print("AUDIT COMPLETE")
    print("="*70)
    print(f"\nSummary:")
    print(f"  Critical Issues:  {audit_report['summary']['critical_issues']}")
    print(f"  Warnings:         {audit_report['summary']['warnings']}")
    print(f"  Total:            {audit_report['summary']['total_issues']}")
    print(f"\nInventory:")
    inv = audit_report['inventory']
    print(f"  HTML Files:       {inv['total_html_files']}")
    print(f"  Countries:        {inv['countries']}")
    print(f"  Companies:        {inv['companies']} (expected {EXPECTED_COMPANIES}) {'✓' if inv['companies'] == EXPECTED_COMPANIES else '✗'}")
    print(f"  Sectors:          {inv['sectors']} (expected {EXPECTED_SECTORS}) {'✓' if inv['sectors'] == EXPECTED_SECTORS else '✗'}")
    print(f"  Browse Pages:     {inv['browse_pages']}")
    print(f"  Root Pages:       {inv['root_pages']}")
    print(f"\nReports saved:")
    print(f"  - /tmp/ai2030-repo/QA_REPORT.md")
    print(f"  - /tmp/ai2030-repo/qa_audit_report.json")
    print("="*70)
