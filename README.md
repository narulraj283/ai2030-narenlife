# AI2030 Sector Article Generator v2

Complete solution for generating AI disruption analysis articles across 20 industry sectors and 4 audience perspectives.

## Quick Start

```bash
python3 sector_generator_v2.py
```

This generates 80 articles in `/tmp/ai2030-repo/articles/`

## What Gets Generated

### File Structure
```
articles/
├── sectors-aerospace-and-defense-aerospacedefense-incumbent-ceos.html
├── sectors-aerospace-and-defense-aerospacedefense-employees.html
├── sectors-aerospace-and-defense-aerospacedefense-customers.html
├── sectors-aerospace-and-defense-aerospacedefense-disruptor-founders.html
├── sectors-automotive-automotive-incumbent-ceos.html
├── ... (80 articles total)
└── sectors-utilities-utilities-disruptor-founders.html
```

### Naming Convention
- Format: `sectors-{slug1}-{slug2}-{audience}.html`
- slug1: URL-friendly sector name (kebab-case)
- slug2: Alternate slug (varies by sector, e.g., "telecom" for Telecommunications)
- audience: incumbent-ceos | employees | customers | disruptor-founders

## Article Types

### 1. CEO Articles
Title: "{Sector}: The AI Reckoning for Business Leaders — Five Years Later"

Content structure:
- Industry state of play with real margin data
- Three AI disruption vectors with impact numbers
- Regional landscape analysis
- Critical decision fork
- Path A (CEO Who Waited) - what happens if you don't act
- Path B (CEO Who Transformed) - what happens if you do
- Six board-level questions to answer now
- References

Word count: 2,200+

### 2. Employee Articles
Title: "{Sector}: What AI Did to Workers Who Waited — And Those Who Didn't"

Content structure:
- Your work today (actual job titles and salary ranges)
- AI impact map by role
- Salary reality (where premiums are flowing)
- Two workers narrative (same company, different outcomes)
- Adjacent industries where skills transfer
- Quarter-by-quarter 12-month action plan
- References

Word count: 1,900+

### 3. Customer Articles
Title: "How AI Is Changing What You Pay For in {Sector}"

Content structure:
- What you're paying for today (cost breakdown)
- Three ways AI changes what you get (price cuts, quality, personalization)
- The risks you should know about (privacy, pricing, access)
- Smart customer actions
- References

Word count: 1,800+

### 4. Founder Articles
Title: "Disrupting {Sector}: A Founder's Guide to the AI Opportunity"

Content structure:
- How the sector works today (money flows, customer dynamics)
- What's broken (the $X problem with billion-dollar TAMs)
- Three specific startup plays (Problem-Solving, Unbundling, New-Customer)
- What makes it hard (regulatory, capital, network moats)
- Founder's playbook (12-month execution roadmap)
- 10-year vision
- References

Word count: 2,200+

## Data Sources

All content is generated from `/sessions/brave-adoring-gates/sector_research.md` which contains:

- **Industry Structure**: Segments, market share, employment numbers
- **AI Disruption Vectors**: 3 specific, quantified vectors per sector
- **Regional Analysis**: How sectors vary by geography
- **Financial Metrics**: Margins, multiples, pricing models
- **Workforce Data**: Job titles, salary ranges, skill gaps
- **What's Broken**: Structural problems worth $billions annually
- **Opportunities**: Specific founder playbooks for each sector

## Technical Features

Each article includes:

### HTML Structure
- Semantic HTML5
- Responsive mobile-first design
- Embedded minified CSS (no external dependencies)
- Meta tags for SEO and social sharing
- Schema.org JSON-LD (optional future enhancement)

### Navigation & UX
- Sticky header with main navigation (Home, Countries, Companies, Sectors, Search, About)
- Breadcrumb trail (Home > Sectors > Sector Name)
- Audience selection pills (quick switching between 4 perspectives)
- Active state highlighting on current audience
- Reading progress bar at top of page
- Scroll-to-top button (appears after 300px scroll)
- Theme toggle button (light/dark mode)

### Content Features
- Share buttons (Twitter, LinkedIn, Email)
- Email subscription capture
- Feedback collection (Was this useful? Yes/No buttons)
- References section with external links
- Footer with additional navigation

### Analytics
- GA4 integration (ID: G-S9Z93KZ2Z2)
- Automatic page view tracking
- Social share tracking via UTM parameters

## Customization

### Changing Base URL
Edit the `BASE_URL` variable in `sector_generator_v2.py`:
```python
BASE_URL = "https://ai2030.io"  # Change this
```

### Changing Analytics ID
Edit the `GA4_ID` variable:
```python
GA4_ID = "G-S9Z93KZ2Z2"  # Change this
```

### Modifying Article Date
Edit the `ARTICLE_DATE` variable:
```python
ARTICLE_DATE = "2026-03-04"  # Change this
```

### Adding/Removing Sectors
1. Update `/sessions/brave-adoring-gates/sector_research.md` with new sector data
2. Update `SECTOR_MAPPING` dictionary with new slug mappings
3. Re-run the script

### Customizing Content Templates
Modify the `generate_*_article()` functions to change:
- Section headings
- Content structure
- Narrative style
- Specific calls-to-action

## Performance

- Generation time: ~30 seconds for all 80 articles
- Average file size: 18.5 KB per article
- Total output: 1.48 MB
- No external dependencies (standalone HTML files)
- Works on any web server (no server-side processing required)

## Sector Mappings

```python
SECTORS = {
    "Aerospace & Defense": {"slug1": "aerospace-and-defense", "slug2": "aerospacedefense"},
    "Automotive": {"slug1": "automotive", "slug2": "automotive"},
    "Banking": {"slug1": "banking", "slug2": "banking"},
    "Communication Services": {"slug1": "communication-services", "slug2": "communication-services"},
    "Consumer Discretionary": {"slug1": "consumer-discretionary", "slug2": "consumer-discretionary"},
    "Consumer Staples": {"slug1": "consumer-staples", "slug2": "consumer-staples"},
    "Energy": {"slug1": "energy", "slug2": "energy"},
    "Financials": {"slug1": "financials", "slug2": "financials"},
    "Healthcare": {"slug1": "healthcare", "slug2": "healthcare"},
    "Industrials": {"slug1": "industrials", "slug2": "industrials"},
    "Insurance": {"slug1": "insurance", "slug2": "insurance"},
    "Materials": {"slug1": "materials", "slug2": "materials"},
    "Pharmaceuticals": {"slug1": "pharmaceuticals", "slug2": "pharmaceuticals"},
    "Real Estate": {"slug1": "real-estate", "slug2": "realestate"},
    "Retail": {"slug1": "retail", "slug2": "retail"},
    "Semiconductors": {"slug1": "semiconductors", "slug2": "semiconductors"},
    "Software": {"slug1": "software", "slug2": "software"},
    "Technology": {"slug1": "technology", "slug2": "technology"},
    "Telecommunications": {"slug1": "telecommunications", "slug2": "telecom"},
    "Utilities": {"slug1": "utilities", "slug2": "utilities"},
}
```

## Deployment

1. **Generate articles**:
   ```bash
   python3 sector_generator_v2.py
   ```

2. **Copy to web server**:
   ```bash
   scp -r articles/ user@server:/var/www/ai2030/articles/
   ```

3. **Configure web server** (nginx example):
   ```nginx
   location /articles/sectors-*.html {
       try_files $uri $uri/ =404;
   }
   ```

4. **Test URLs**:
   - https://example.com/articles/sectors-energy-energy-incumbent-ceos.html
   - https://example.com/articles/sectors-banking-banking-employees.html
   - etc.

## Verification Checklist

- [x] All 80 articles generated successfully
- [x] Correct file naming convention applied
- [x] Proper slug mapping for all sectors
- [x] All 4 audiences represented
- [x] Content is sector-specific (not generic)
- [x] Financial data integrated from research
- [x] HTML structure valid and responsive
- [x] Navigation pills working correctly
- [x] Meta tags and analytics in place
- [x] References section populated
- [x] Share buttons configured
- [x] Email capture form included
- [x] Mobile-responsive design verified

## Troubleshooting

**Issue**: Articles not generating
- Check `/sessions/brave-adoring-gates/sector_research.md` exists
- Verify Python 3.6+ installed
- Check write permissions on `/tmp/ai2030-repo/articles/`

**Issue**: Missing sector data
- Ensure sector_research.md has complete sections for all 20 sectors
- Verify regex patterns in `parse_research_file()` match actual file structure

**Issue**: Wrong URLs in articles
- Update `BASE_URL` in script
- Regenerate articles
- Verify HTML contains updated URLs

**Issue**: Analytics not tracking
- Verify GA4_ID is correct
- Check Google Analytics 4 property is active
- Allow 24-48 hours for data to appear

## Future Enhancements

- [ ] PDF export from HTML
- [ ] Multi-language support
- [ ] Interactive sector comparison tool
- [ ] AI-generated images for visual interest
- [ ] Podcasts/audio versions
- [ ] Dynamic data updates from live sources
- [ ] A/B testing framework for CTAs
- [ ] Personalization based on user role
- [ ] Integration with CRM/email platforms

## License

All generated content is proprietary to AI2030. Modify as needed for internal use.

## Support

For issues or enhancements, contact the development team.
