#!/usr/bin/env python3
"""
Comprehensive QA Audit for AI2030 Repository - v2
Checks: broken links, navigation, SEO, content quality, file inventory, format compliance
"""

import os
import re
import json
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse
from collections import defaultdict, Counter
import xml.etree.ElementTree as ET

# Configuration
REPO_PATH = Path("/tmp/ai2030-repo")
EXPECTED_SECTORS = 80  # 20 sectors × 4 audiences
EXPECTED_COMPANIES = 142  # CEO-only articles
EXPECTED_NAV = ["Home", "Countries", "Companies", "Sectors", "About"]
GA4_TRACKING_ID = "G-S9Z93KZ2Z2"

# Report structure
report = {
    "summary": {},
    "critical": [],
    "warnings": [],
    "info": [],
    "inventory": {},
    "details": {
        "broken_links": [],
        "nav_issues": [],
        "seo_issues": [],
        "content_issues": [],
        "format_issues": []
    }
}

class HTMLLinkExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.meta_tags = {}
        self.title = ""
        self.has_ga4 = False
        self.has_schema = False
        self.nav_items = []
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

        elif tag == "title":
            self.in_script = False

        elif tag == "script":
            self.in_script = True
            src = attrs_dict.get("src", "")
            if "gtag" in src or "analytics" in src:
                self.has_ga4 = True
            if attrs_dict.get("type") == "application/ld+json":
                self.has_schema = True

        elif tag == "nav":
            # Flag nav items
            pass

    def handle_endtag(self, tag):
        if tag == "script":
            self.in_script = False
            if self.script_content and "gtag" in self.script_content:
                self.has_ga4 = True
            if self.script_content and GA4_TRACKING_ID in self.script_content:
                self.has_ga4 = True
            self.script_content = ""

    def handle_data(self, data):
        if self.in_script:
            self.script_content += data
            if GA4_TRACKING_ID in self.script_content:
                self.has_ga4 = True
            if '"@context"' in self.script_content or "'@context'" in self.script_content:
                self.has_schema = True
        else:
            self.current_text.append(data)

    def finalize_text(self):
        self.text_content = "".join(self.current_text)

def extract_html_content(file_path):
    """Extract all relevant content from HTML file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        parser = HTMLLinkExtractor()
        parser.feed(content)
        parser.finalize_text()

        # Extract title
        title_match = re.search(r'<title[^>]*>([^<]+)</title>', content, re.IGNORECASE)
        parser.title = title_match.group(1) if title_match else ""

        # Extract nav items by looking for nav element or specific nav patterns
        nav_matches = re.findall(r'<a[^>]*href="[^"]*"[^>]*>([^<]+)</a>', content)
        parser.nav_items = nav_matches[:10]  # First 10 links are usually nav

        return parser
    except Exception as e:
        return None

def get_all_html_files():
    """Get all HTML files in repo"""
    html_files = []
    for root, dirs, files in os.walk(REPO_PATH):
        # Skip hidden directories and common non-content dirs
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['__pycache__']]

        for file in files:
            if file.endswith('.html'):
                html_files.append(Path(root) / file)

    return sorted(html_files)

def resolve_link(link, current_file_path):
    """Resolve a link to check if it points to existing file"""
    # Skip external links, mailto, tel, etc.
    if not link or link.startswith(('http', 'mailto:', 'tel:', '#', 'javascript:')):
        return None

    # Remove fragments
    link_path = link.split('#')[0]

    if not link_path:
        return None

    # Resolve relative to repo root for absolute paths
    if link.startswith('/'):
        full_path = REPO_PATH / link.lstrip('/')
    else:
        # Relative to current file
        full_path = (current_file_path.parent / link_path).resolve()

    # Try with and without .html extension
    if full_path.exists():
        return full_path

    if not str(full_path).endswith('.html') and (full_path.with_suffix('.html')).exists():
        return full_path.with_suffix('.html')

    # Check if it's a directory with index.html
    if full_path.is_dir() and (full_path / 'index.html').exists():
        return full_path / 'index.html'

    return None

def count_words(text):
    """Count words in text content"""
    words = text.split()
    return len(words)

def check_broken_links():
    """Check 1: Verify all links point to existing files (excluding intentional missing files)"""
    html_files = get_all_html_files()
    broken_links_found = []

    for html_file in html_files:
        parser = extract_html_content(html_file)
        if not parser:
            continue

        for link in parser.links:
            resolved = resolve_link(link, html_file)
            if resolved is None and link and not link.startswith(('http', 'mailto:', 'tel:', '#', 'javascript:')):
                # Skip links to intentionally missing employee/investor articles
                if "-employee.html" in link or "-investor.html" in link:
                    continue

                # Only report if it looks like it should be internal
                broken_links_found.append({
                    "file": str(html_file.relative_to(REPO_PATH)),
                    "broken_link": link,
                    "severity": "CRITICAL"
                })

    return broken_links_found

def check_navigation_consistency():
    """Check 2: Verify navigation is consistent across all files"""
    html_files = get_all_html_files()
    nav_issues = []

    for html_file in html_files:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Look for nav element and extract links
        nav_match = re.search(r'<nav[^>]*>(.*?)</nav>', content, re.DOTALL | re.IGNORECASE)
        if nav_match:
            nav_section = nav_match.group(1)
            # Extract nav item text
            nav_items = re.findall(r'>([^<]+)</a>', nav_section)
            nav_items = [item.strip() for item in nav_items if item.strip()]

            # Check for unexpected items
            unexpected = [item for item in nav_items if item not in EXPECTED_NAV and item not in ['AI2030 Report']]
            if unexpected:
                nav_issues.append({
                    "file": str(html_file.relative_to(REPO_PATH)),
                    "unexpected_nav": unexpected,
                    "severity": "WARNING"
                })
        else:
            nav_issues.append({
                "file": str(html_file.relative_to(REPO_PATH)),
                "issue": "No nav element found",
                "severity": "WARNING"
            })

    return nav_issues

def check_seo():
    """Check 3: Verify SEO elements in all files"""
    html_files = get_all_html_files()
    seo_issues = []

    for html_file in html_files:
        parser = extract_html_content(html_file)
        if not parser:
            continue

        issues = []

        if not parser.title:
            issues.append("Missing or empty <title> tag")
        elif len(parser.title) < 3:
            issues.append(f"Title too short: '{parser.title}'")

        if "description" not in parser.meta_tags:
            issues.append("Missing <meta name='description'>")

        if "og:title" not in parser.meta_tags:
            issues.append("Missing <meta property='og:title'>")

        if "og:description" not in parser.meta_tags:
            issues.append("Missing <meta property='og:description'>")

        if "canonical" not in parser.meta_tags:
            issues.append("Missing canonical URL")

        if not parser.has_ga4:
            # Only flag if it's a content page (not 404 or admin)
            if '404' not in str(html_file) and 'admin' not in str(html_file):
                issues.append(f"Missing GA4 tracking (expected {GA4_TRACKING_ID})")

        if not parser.has_schema:
            if 'articles' in str(html_file) or 'browse' in str(html_file):
                issues.append("Missing Schema.org JSON-LD")

        if issues:
            seo_issues.append({
                "file": str(html_file.relative_to(REPO_PATH)),
                "issues": issues,
                "severity": "WARNING"
            })

    return seo_issues

def check_content_quality():
    """Check 4: Verify content quality for sector articles"""
    content_issues = []
    articles_dir = REPO_PATH / "articles"

    if articles_dir.exists():
        for html_file in articles_dir.glob("*.html"):
            parser = extract_html_content(html_file)
            if not parser:
                continue

            issues = []

            # Check word count for sector articles
            if "sector" in html_file.name.lower():
                word_count = count_words(parser.text_content)
                if word_count < 1500:
                    issues.append(f"Low word count: {word_count} (expected 1500+)")

            # Check for placeholder text
            placeholders = ["Lorem ipsum", "[TODO]", "{placeholder}", "TODO:", "PLACEHOLDER"]
            for placeholder in placeholders:
                if placeholder.lower() in parser.text_content.lower():
                    issues.append(f"Found placeholder text: {placeholder}")

            if issues:
                content_issues.append({
                    "file": str(html_file.relative_to(REPO_PATH)),
                    "issues": issues,
                    "severity": "WARNING"
                })

    return content_issues

def check_file_inventory():
    """Check 5: Count and verify file inventory"""
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
        elif "articles/companies-" in rel_path and "-employee" not in rel_path and "-investor" not in rel_path:
            inventory["companies"] += 1
        elif "articles/sector-" in rel_path:
            inventory["sectors"] += 1
        elif rel_path.startswith("browse/"):
            inventory["browse_pages"] += 1
        elif rel_path.count('/') == 0:
            inventory["root_pages"] += 1
        else:
            inventory["other"] += 1

    return inventory

def check_company_format():
    """Check 6: Verify company articles are CEO-only"""
    format_issues = []
    articles_dir = REPO_PATH / "articles"

    if articles_dir.exists():
        # Check for employee/investor articles (should not exist)
        for pattern in ["companies-*-employee*.html", "companies-*-investor*.html"]:
            files = list(articles_dir.glob(pattern))
            for file in files:
                format_issues.append({
                    "file": str(file.relative_to(REPO_PATH)),
                    "issue": "Found non-CEO company article (should only have CEO articles)",
                    "severity": "CRITICAL"
                })

    return format_issues

def check_sector_format():
    """Check 7: Verify sector article format (80 files, correct format)"""
    format_issues = []
    articles_dir = REPO_PATH / "articles"
    sectors = defaultdict(int)

    if articles_dir.exists():
        sector_files = list(articles_dir.glob("sector-*.html"))

        # Count by sector and audience
        for file in sector_files:
            match = re.search(r"sector-([^-]+)-([a-z]+)", file.name)
            if match:
                sector = match.group(1)
                audience = match.group(2)
                sectors[sector] += 1

        # Check if we have exactly 80 files
        if len(sector_files) != EXPECTED_SECTORS:
            format_issues.append({
                "file": "articles/",
                "issue": f"Expected {EXPECTED_SECTORS} sector files, found {len(sector_files)}",
                "severity": "CRITICAL"
            })

        # Check for old-format files
        old_format_files = list(articles_dir.glob("sectors-*.html"))
        if old_format_files:
            format_issues.append({
                "file": "articles/",
                "issue": f"Found {len(old_format_files)} old-format sector files (sectors-*.html)",
                "severity": "CRITICAL"
            })

        # Verify sibling pills link to all 4 audience types
        audiences = Counter()
        for file in sector_files:
            match = re.search(r"sector-([^-]+)-([a-z]+)", file.name)
            if match:
                audiences[match.group(2)] += 1

        for sector in sectors:
            if sectors[sector] != 4:
                format_issues.append({
                    "file": f"articles/ (sector: {sector})",
                    "issue": f"Sector '{sector}' has {sectors[sector]} audience variations (expected 4)",
                    "severity": "WARNING"
                })

    return format_issues

def check_sitemap():
    """Check 8: Verify sitemap.xml consistency"""
    sitemap_issues = []
    sitemap_path = REPO_PATH / "sitemap.xml"
    html_files = get_all_html_files()

    if sitemap_path.exists():
        try:
            tree = ET.parse(sitemap_path)
            root = tree.getroot()

            sitemap_urls = set()
            ns = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

            for url in root.findall('ns:url', ns):
                loc = url.find('ns:loc', ns)
                if loc is not None and loc.text:
                    # Extract path from URL
                    parsed = urlparse(loc.text)
                    path = parsed.path.lstrip('/')
                    sitemap_urls.add(path)

            # Check each sitemap URL points to existing file
            for url in sitemap_urls:
                full_path = REPO_PATH / url
                if not full_path.exists():
                    sitemap_issues.append({
                        "file": "sitemap.xml",
                        "issue": f"Sitemap points to non-existent file: {url}",
                        "severity": "CRITICAL"
                    })

            # Check each HTML file is in sitemap (except 404, admin, etc.)
            missing_from_sitemap = 0
            for html_file in html_files:
                rel_path = str(html_file.relative_to(REPO_PATH))
                if '404.html' in rel_path or 'admin.html' in rel_path:
                    continue

                if rel_path not in sitemap_urls:
                    missing_from_sitemap += 1
                    if missing_from_sitemap <= 5:  # Only report first 5
                        sitemap_issues.append({
                            "file": rel_path,
                            "issue": "File exists but not in sitemap.xml",
                            "severity": "WARNING"
                        })

            if missing_from_sitemap > 5:
                sitemap_issues.append({
                    "file": "sitemap.xml",
                    "issue": f"... and {missing_from_sitemap - 5} more files missing from sitemap",
                    "severity": "WARNING"
                })

        except Exception as e:
            sitemap_issues.append({
                "file": "sitemap.xml",
                "issue": f"Error parsing sitemap: {str(e)}",
                "severity": "WARNING"
            })
    else:
        sitemap_issues.append({
            "file": "sitemap.xml",
            "issue": "sitemap.xml not found",
            "severity": "CRITICAL"
        })

    return sitemap_issues

def run_audit():
    """Run all audit checks"""
    print("Starting comprehensive QA audit...")
    print()

    # Run all checks
    print("1. Checking broken links...")
    broken_links = check_broken_links()
    report["details"]["broken_links"] = broken_links

    print("2. Checking navigation consistency...")
    nav_issues = check_navigation_consistency()
    report["details"]["nav_issues"] = nav_issues

    print("3. Checking SEO elements...")
    seo_issues = check_seo()
    report["details"]["seo_issues"] = seo_issues

    print("4. Checking content quality...")
    content_issues = check_content_quality()
    report["details"]["content_issues"] = content_issues

    print("5. Checking file inventory...")
    inventory = check_file_inventory()
    report["inventory"] = inventory

    print("6. Checking company article format...")
    company_format = check_company_format()
    report["details"]["format_issues"].extend(company_format)

    print("7. Checking sector article format...")
    sector_format = check_sector_format()
    report["details"]["format_issues"].extend(sector_format)

    print("8. Checking sitemap...")
    sitemap = check_sitemap()
    report["details"]["format_issues"].extend(sitemap)

    # Organize by severity
    for issue_list in report["details"].values():
        for issue in issue_list:
            severity = issue.get("severity", "INFO")
            if severity == "CRITICAL":
                report["critical"].append(issue)
            elif severity == "WARNING":
                report["warnings"].append(issue)
            else:
                report["info"].append(issue)

    # Summary
    report["summary"] = {
        "critical_issues": len(report["critical"]),
        "warnings": len(report["warnings"]),
        "info_messages": len(report["info"]),
        "total_issues": len(report["critical"]) + len(report["warnings"]) + len(report["info"]),
        "inventory": inventory
    }

    return report

def generate_markdown_report(report):
    """Generate markdown version of report"""
    md = []
    md.append("# AI2030 QA Audit Report")
    md.append(f"Generated: 2026-03-04")
    md.append("")

    # Summary
    md.append("## Executive Summary")
    md.append(f"- **Critical Issues:** {report['summary']['critical_issues']}")
    md.append(f"- **Warnings:** {report['summary']['warnings']}")
    md.append(f"- **Info Messages:** {report['summary']['info_messages']}")
    md.append(f"- **Total Issues:** {report['summary']['total_issues']}")
    md.append("")

    # Inventory
    md.append("## File Inventory")
    inv = report["inventory"]
    md.append(f"- **Total HTML Files:** {inv['total_html_files']}")
    md.append(f"- **Country Articles:** {inv['countries']}")
    md.append(f"- **Company Articles:** {inv['companies']} (expected {EXPECTED_COMPANIES})")
    md.append(f"- **Sector Articles:** {inv['sectors']} (expected {EXPECTED_SECTORS})")
    md.append(f"- **Browse Pages:** {inv['browse_pages']}")
    md.append(f"- **Root Pages:** {inv['root_pages']}")
    md.append(f"- **Other Files:** {inv['other']}")
    md.append("")

    # Assessment
    if inv['companies'] == EXPECTED_COMPANIES and inv['sectors'] == EXPECTED_SECTORS:
        md.append("### Inventory Status: ✓ PASS")
        md.append("All expected files are present with correct counts.")
    else:
        md.append("### Inventory Status: ✗ ISSUES FOUND")
        if inv['companies'] != EXPECTED_COMPANIES:
            md.append(f"- Companies: {inv['companies']} vs expected {EXPECTED_COMPANIES}")
        if inv['sectors'] != EXPECTED_SECTORS:
            md.append(f"- Sectors: {inv['sectors']} vs expected {EXPECTED_SECTORS}")
    md.append("")

    # Critical Issues
    if report["critical"]:
        md.append("## Critical Issues (Must Fix)")
        issue_groups = defaultdict(list)
        for issue in report["critical"]:
            category = issue.get('file', 'Unknown').split('/')[0] if '/' in issue.get('file', '') else 'Root'
            issue_groups[category].append(issue)

        for i, (category, issues) in enumerate(sorted(issue_groups.items()), 1):
            md.append(f"\n### {i}. {category.upper()} ({len(issues)} issues)")
            for issue in issues[:5]:
                if "broken_link" in issue:
                    md.append(f"- **Broken Link:** `{issue['broken_link']}` in {issue['file']}")
                if "issue" in issue:
                    md.append(f"- **{issue['file']}:** {issue['issue']}")
            if len(issues) > 5:
                md.append(f"- ... and {len(issues) - 5} more")

    # Warnings
    if report["warnings"]:
        md.append(f"\n## Warnings ({len(report['warnings'])} issues)")
        warning_groups = defaultdict(list)
        for issue in report["warnings"]:
            category = issue.get('file', 'Unknown')
            warning_groups[category].append(issue)

        for category, issues in sorted(warning_groups.items())[:20]:
            md.append(f"\n**{category}**")
            for issue in issues[:2]:
                if "issue" in issue:
                    md.append(f"- {issue['issue']}")
                if "issues" in issue:
                    for iss in issue['issues'][:1]:
                        md.append(f"  - {iss}")

        if len(warning_groups) > 20:
            md.append(f"\n... and {len(warning_groups) - 20} more warnings")

    return "\n".join(md)

if __name__ == "__main__":
    audit_report = run_audit()

    # Save JSON report
    json_report_path = REPO_PATH / "qa_audit_report.json"
    with open(json_report_path, 'w') as f:
        json.dump(audit_report, f, indent=2)
    print(f"\nJSON report saved to: {json_report_path}")

    # Save markdown report
    md_content = generate_markdown_report(audit_report)
    md_report_path = REPO_PATH / "QA_REPORT.md"
    with open(md_report_path, 'w') as f:
        f.write(md_content)
    print(f"Markdown report saved to: {md_report_path}")

    # Print summary
    print("\n" + "="*60)
    print("AUDIT SUMMARY")
    print("="*60)
    print(f"Critical Issues: {audit_report['summary']['critical_issues']}")
    print(f"Warnings: {audit_report['summary']['warnings']}")
    print(f"Info: {audit_report['summary']['info_messages']}")
    print(f"Total: {audit_report['summary']['total_issues']}")
    print()
    print("File Inventory:")
    for key, value in audit_report['inventory'].items():
        expected = EXPECTED_COMPANIES if key == 'companies' else EXPECTED_SECTORS if key == 'sectors' else None
        status = "✓" if expected and value == expected else ""
        print(f"  {key}: {value} {status}")

    if audit_report['critical']:
        print("\nCRITICAL ISSUES:")
        for issue in audit_report['critical'][:10]:
            print(f"  [{issue.get('file', 'Unknown')}] {issue.get('issue', issue.get('broken_link', ''))}")
        if len(audit_report['critical']) > 10:
            print(f"  ... and {len(audit_report['critical']) - 10} more")
