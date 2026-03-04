# AI 2030 Country Intelligence Briefs

## Overview

This directory contains 2-page PDF intelligence briefs for the top 20 countries' AI readiness and disruption scenarios by 2030.

## Contents

### PDF Briefs (20 countries)

Each brief is a professionally formatted 2-page PDF document containing:

**Page 1:**
- Header: "AI 2030 INTELLIGENCE BRIEF"
- Country name and subtitle: "Bear Case vs Bull Case: What AI Means for [Country] by 2030"
- Executive Summary (3-4 sentences)
- Bear Case section with 3-4 key risk scenarios

**Page 2:**
- Bull Case section with 3-4 opportunity scenarios
- "What Leaders Should Do Now" (3 key recommendations)
- Professional footer with full report URL
- Copyright notice

### Available Countries

1. United States (brief-us-us.pdf)
2. China (brief-china-china.pdf)
3. India (brief-india-india.pdf)
4. United Kingdom (brief-uk-uk.pdf)
5. Germany (brief-germany-germany.pdf)
6. Japan (brief-japan-japan.pdf)
7. France (brief-france-france.pdf)
8. Canada (brief-canada-canada.pdf)
9. Australia (brief-australia-australia.pdf)
10. South Korea (brief-south-korea-south-korea.pdf)
11. Brazil (brief-brazil-brazil.pdf)
12. Mexico (brief-mexico-mexico.pdf)
13. Indonesia (brief-indonesia-indonesia.pdf)
14. Saudi Arabia (brief-saudi-arabia-saudi-arabia.pdf)
15. Turkey (brief-turkey-turkey.pdf)
16. Switzerland (brief-switzerland-switzerland.pdf)
17. Singapore (brief-singapore-singapore.pdf)
18. Israel (brief-israel-israel.pdf)
19. Nigeria (brief-nigeria-nigeria.pdf)
20. United Arab Emirates (brief-uae-uae.pdf)

### Index Page

**index.html** - A professional download center listing all 20 country briefs with:
- Gradient background matching AI 2030 report styling
- Brief card grid layout with download buttons
- Summary statistics (20 countries, 2 pages each, PDF format)
- Responsive design for desktop and mobile
- Back link to main AI 2030 Report

## Technical Details

### Technology Stack
- **Python 3**: ReportLab for PDF generation
- **HTML Parsing**: BeautifulSoup4 for extracting content from source articles
- **Source Data**: CEO edition articles from /tmp/ai2030-repo/articles/

### PDF Features
- **Professional Styling**: Dark blue (#1a1a2e) header with accent colors (#3b82f6)
- **Typography**: Helvetica fonts with proper hierarchy
- **Layout**: 0.5-inch margins, letter-size pages (612x792 pts)
- **Content Extraction**: Intelligent parsing of Bear Case, Bull Case, and recommendation sections

### File Sizes
- Each PDF: ~4.4-4.5 KB
- Total for all 20 briefs: ~168 KB
- Index page: ~11 KB

## Usage

### Viewing Briefs
1. Download any PDF directly from the index.html page
2. Or download specific PDFs by filename from this directory
3. Open with any PDF reader (Adobe Reader, browser, etc.)

### Batch Download
All PDF files can be downloaded in bulk from `/tmp/ai2030-repo/briefs/`

### Integration
The briefs can be:
- Hosted on a web server alongside the main AI 2030 report
- Embedded in email campaigns
- Shared via download links
- Used as executive summaries for stakeholders

## Generation Script

The briefs were generated using `/tmp/generate_pdf_briefs.py` which:
1. Reads HTML CEO edition articles from the repository
2. Extracts key sections using BeautifulSoup
3. Formats content with ReportLab into professional 2-page PDFs
4. Generates an HTML index for easy access
5. Outputs all files to this directory

To regenerate briefs, run:
```bash
python3 /tmp/generate_pdf_briefs.py
```

## Metadata

- **Generated**: March 4, 2026
- **Format**: PDF 1.4
- **Pages Per Brief**: 2
- **Total Countries**: 20
- **Copyright**: © 2026 The 2030 Intelligence Report

---

Learn more at: [ai2030report.com](https://ai2030report.com)
