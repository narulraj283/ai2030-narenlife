#!/usr/bin/env python3
"""Batch 2 rewrite: Ethiopia, DR Congo, Turkey, Iran, Tanzania, Kenya, Colombia, Argentina, Algeria, Sudan"""
import os, html, glob, re


ARTICLES_DIR = "articles"
AUDIENCES = ["ceo","consumer","employee","government","investor","young-person",
             "blue-collar-worker","educator","parent","retiree","small-business-owner"]

# Verified country data from World Bank, IMF, Trading Economics, national sources
COUNTRIES = {
    "ethiopia": {
        "name": "Ethiopia", "slug": "ethiopia-ethiopia", "population": "132 million",
        "gdp_per_capita": "$1,134", "gdp_per_capita_ppp": "$3,700", "gdp_growth": "7.6%",
        "currency": "ETB", "avg_monthly_salary": "ETB 3,500 (~$60 USD)",
        "avg_salary_usd": "$60", "minimum_wage": "No statutory national minimum wage; civil servants ETB 420/month",
        "it_salary_range": "ETB 8,800-9,300/month (~$150-160 USD)",
        "manufacturing_salary": "ETB 1,500-3,000/month (~$25-50 USD)",
        "unemployment": "3.5% (official; significant underemployment)",
        "ai_adoption": "6.8% adoption rate; nascent digital economy",
        "internet_penetration": "Under 20%", "literacy_rate": "51.8%",
        "stem_graduates": "Growing but limited; ~50,000 annually",
        "labor_force": "58 million",
        "key_industries": "Agriculture (38% GDP, 80% of exports), textiles, leather, cement, floriculture, coffee",
        "ai_risk_high": "Textile manufacturing, basic data entry, call center operations",
        "ai_risk_medium": "Banking, agriculture processing, logistics",
        "ai_risk_low": "Subsistence agriculture, construction, healthcare delivery, tourism",
        "key_challenges": "High inflation (26.6% declining to 17%), structural debt crisis, poverty deepening despite growth, civil conflict aftermath, very low internet penetration limiting digital economy",
        "references": [
            ("World Bank - Ethiopia Overview", "https://www.worldbank.org/en/country/ethiopia/overview"),
            ("IMF - Ethiopia GDP Data", "https://www.imf.org/en/Countries/ETH"),
            ("African Development Bank - Ethiopia Economic Outlook", "https://www.afdb.org/en/countries/east-africa/ethiopia"),
            ("McKinsey Africa AI Report 2025", "https://www.mckinsey.com/featured-insights/middle-east-and-africa"),
            ("World Bank - Ethiopia Poverty Data", "https://data.worldbank.org/country/ethiopia"),
            ("Trading Economics - Ethiopia Indicators", "https://tradingeconomics.com/ethiopia/indicators"),
        ]
    },
    "dr-congo": {
        "name": "DR Congo", "slug": "dr-congo-dr-congo", "population": "111 million",
        "gdp_per_capita": "$772", "gdp_per_capita_ppp": "$1,500", "gdp_growth": "6.9%",
        "currency": "CDF", "avg_monthly_salary": "CDF 145,000 (~$55 USD)",
        "avg_salary_usd": "$55", "minimum_wage": "CDF 21,500/day (~$5.07 USD); ~CDF 290,000/month ($101 USD)",
        "it_salary_range": "Limited formal IT sector; ~$200-500/month in Kinshasa",
        "manufacturing_salary": "CDF 100,000-200,000/month (~$38-76 USD)",
        "unemployment": "High (exact figure unavailable; large informal economy)",
        "ai_adoption": "Minimal; limited digital infrastructure",
        "internet_penetration": "30.6%", "literacy_rate": "80.5%",
        "stem_graduates": "Limited; ~20,000 annually",
        "labor_force": "35 million",
        "key_industries": "Mining (cobalt 70% of global supply, copper, diamonds), agriculture, timber, oil",
        "ai_risk_high": "Administrative services, basic mining operations data processing",
        "ai_risk_medium": "Banking, telecom operations",
        "ai_risk_low": "Artisanal mining, subsistence agriculture, construction, healthcare",
        "key_challenges": "Conflict minerals and M23 rebel control of mining areas, currency depreciated 8.7% in 2024, inflation at 11.3%, fiscal deficit from security costs, infrastructure severely lacking",
        "references": [
            ("World Bank - DRC Overview", "https://www.worldbank.org/en/country/drc/overview"),
            ("Worldometer - DRC GDP", "https://www.worldometers.info/gdp/democratic-republic-of-the-congo-gdp/"),
            ("African Development Bank - DRC", "https://www.afdb.org/en/countries/central-africa/democratic-republic-of-congo"),
            ("DataReportal - Digital 2025 DRC", "https://datareportal.com/reports/digital-2025-democratic-republic-of-the-congo"),
            ("Coface - DRC Economic Assessment", "https://www.coface.com/Economic-Studies/Democratic-Republic-of-Congo"),
        ]
    },
    "turkey": {
        "name": "Turkey", "slug": "turkey-turkey", "population": "86 million",
        "gdp_per_capita": "$15,463", "gdp_per_capita_ppp": "$41,900", "gdp_growth": "1.6% (2024); 2.5% (2025)",
        "currency": "TRY", "avg_monthly_salary": "TRY 35,000 (~$900 USD)",
        "avg_salary_usd": "$900", "minimum_wage": "TRY 26,005/month gross (2025)",
        "it_salary_range": "TRY 40,000-150,000+/month; average TRY 1,279,328/year",
        "manufacturing_salary": "TRY 26,000-35,000/month (near minimum wage baseline)",
        "unemployment": "8.5%",
        "ai_adoption": "Growing; strong tech ecosystem in Istanbul; government AI strategy launched",
        "internet_penetration": "87.3%", "literacy_rate": "96.7%",
        "stem_graduates": "~250,000 annually",
        "labor_force": "35 million",
        "key_industries": "Manufacturing, automotive, textiles, chemicals, metals, food processing, tourism, construction",
        "ai_risk_high": "Textile manufacturing, call centers, basic administrative services, data entry",
        "ai_risk_medium": "Automotive manufacturing, banking, logistics, tourism operations",
        "ai_risk_low": "Healthcare, education, construction trades, agriculture",
        "key_challenges": "Severe inflation crisis (60% in 2024, declining to 38% by April 2025), lira lost 40% vs USD in 2024, political instability affecting markets, high youth unemployment",
        "references": [
            ("World Bank - Turkey Data", "https://data.worldbank.org/country/turkiye"),
            ("OECD - Turkey Economic Survey", "https://www.oecd.org/en/topics/sub-issues/economic-surveys-turkey.html"),
            ("TurkStat - Employment Statistics", "https://data.tuik.gov.tr/Kategori/GetKategori?p=istihdam-issizlik-ve-ucret-108"),
            ("IMF - Turkey Article IV", "https://www.imf.org/en/Countries/TUR"),
            ("Trading Economics - Turkey Indicators", "https://tradingeconomics.com/turkey/indicators"),
            ("FocusEconomics - Turkey Inflation", "https://www.focus-economics.com/countries/turkey/"),
        ]
    },
    "iran": {
        "name": "Iran", "slug": "iran-iran", "population": "87 million",
        "gdp_per_capita": "$4,771 (official); effective purchasing power much lower",
        "gdp_per_capita_ppp": "$17,400", "gdp_growth": "0.3% (2025 estimate)",
        "currency": "IRR", "avg_monthly_salary": "IRR 104 million (~$178 USD at official rates)",
        "avg_salary_usd": "$178", "minimum_wage": "IRR 104 million/month (2025)",
        "it_salary_range": "IRR 150-400 million/month (~$250-680 USD)",
        "manufacturing_salary": "IRR 80-120 million/month (~$135-200 USD)",
        "unemployment": "9.2% (official; real figure likely higher)",
        "ai_adoption": "Limited by sanctions; domestic tech ecosystem growing (Digikala, Snapp, Cafe Bazaar)",
        "internet_penetration": "78%", "literacy_rate": "85%",
        "stem_graduates": "~350,000 annually; strong mathematics and engineering tradition",
        "labor_force": "28 million",
        "key_industries": "Oil & gas (90% export revenue), petrochemicals, agriculture, textiles, automotive, telecommunications",
        "ai_risk_high": "Administrative services, basic banking operations, data processing",
        "ai_risk_medium": "Oil sector operations, manufacturing, telecom",
        "ai_risk_low": "Agriculture, healthcare, education, construction",
        "key_challenges": "Rial depreciated 800% since 2020, inflation 42-48%+, Western sanctions severely limiting economy, 22-50% poverty rate, capital flight $20B+ in 2024, brain drain of educated youth",
        "references": [
            ("World Bank - Iran Data", "https://data.worldbank.org/country/iran-islamic-rep"),
            ("IMF - Iran Country Data", "https://www.imf.org/en/Countries/IRN"),
            ("Iran International - Economic Reports", "https://www.iranintl.com/en/economy"),
            ("Trading Economics - Iran", "https://tradingeconomics.com/iran/indicators"),
        ]
    },
    "tanzania": {
        "name": "Tanzania", "slug": "tanzania-tanzania", "population": "69 million",
        "gdp_per_capita": "$1,302", "gdp_per_capita_ppp": "$3,600", "gdp_growth": "5.5% (2024); 6.0% (2025)",
        "currency": "TZS", "avg_monthly_salary": "TZS 588,000-2,065,000 (~$228-800 USD range)",
        "avg_salary_usd": "$228-400", "minimum_wage": "TZS 175,000-765,900/month (varies by sector)",
        "it_salary_range": "TZS 658,000-2,070,000/month (~$240-760 USD)",
        "manufacturing_salary": "TZS 175,000-280,000/month (~$68-109 USD)",
        "unemployment": "9.3% (2022, latest available)",
        "ai_adoption": "Very low; growing mobile money ecosystem (M-Pesa)",
        "internet_penetration": "35%", "literacy_rate": "78%",
        "stem_graduates": "~30,000 annually",
        "labor_force": "30 million",
        "key_industries": "Agriculture, mining (gold), manufacturing (8% GDP), tourism, telecommunications",
        "ai_risk_high": "Data entry, basic administrative work, textile manufacturing",
        "ai_risk_medium": "Banking/mobile money operations, mining data processing, logistics",
        "ai_risk_low": "Agriculture, tourism, construction, healthcare, artisanal mining",
        "key_challenges": "Labor moving to lower-productivity sectors, underdeveloped financial sector, infrastructure gaps, poverty at 27.7%, low internet penetration",
        "references": [
            ("World Bank - Tanzania Overview", "https://www.worldbank.org/en/country/tanzania/overview"),
            ("African Development Bank - Tanzania", "https://www.afdb.org/en/countries/east-africa/tanzania"),
            ("Trading Economics - Tanzania", "https://tradingeconomics.com/tanzania/indicators"),
            ("NBS Tanzania - Labor Force Survey", "https://www.nbs.go.tz/"),
        ]
    },
    "kenya": {
        "name": "Kenya", "slug": "kenya-kenya", "population": "58 million",
        "gdp_per_capita": "$2,274", "gdp_per_capita_ppp": "$6,500", "gdp_growth": "5.4% (2024); 5.6% (2025)",
        "currency": "KES", "avg_monthly_salary": "KES 20,123 (~$155 USD average); urban much higher",
        "avg_salary_usd": "$155-400", "minimum_wage": "KES 16,114/month (2026, +6% increase)",
        "it_salary_range": "KES 75,000-240,000/month (~$580-1,850 USD)",
        "manufacturing_salary": "KES 16,000-30,000/month (~$124-232 USD)",
        "unemployment": "5.4% (official); youth unemployment 67%",
        "ai_adoption": "42.1% ChatGPT usage; $15M VC in AI startups (2023); Africa's 'Silicon Savannah'",
        "internet_penetration": "48%", "literacy_rate": "82.9%",
        "stem_graduates": "~60,000 annually",
        "labor_force": "24 million",
        "key_industries": "Tea, coffee, tourism, cut flowers, ICT services, banking/fintech, agriculture",
        "ai_risk_high": "BPO/call centers, data entry, basic financial services",
        "ai_risk_medium": "Banking operations, logistics, agriculture processing",
        "ai_risk_low": "Tourism, healthcare, education, smallholder agriculture, creative industries",
        "key_challenges": "Youth unemployment at 67% despite 5%+ GDP growth, digital divide between Nairobi and rural areas, structural transformation weak, Vision 2030 targets unmet",
        "references": [
            ("World Bank - Kenya Overview", "https://www.worldbank.org/en/country/kenya/overview"),
            ("African Development Bank - Kenya", "https://www.afdb.org/en/countries/east-africa/kenya"),
            ("Kenya National Bureau of Statistics", "https://www.knbs.or.ke/"),
            ("McKinsey - AI in Africa", "https://www.mckinsey.com/featured-insights/middle-east-and-africa"),
            ("TechInAfrica - Kenya AI Startups", "https://www.techinafrica.com/"),
            ("Trading Economics - Kenya", "https://tradingeconomics.com/kenya/indicators"),
        ]
    },
    "colombia": {
        "name": "Colombia", "slug": "colombia-colombia", "population": "53 million",
        "gdp_per_capita": "$8,249", "gdp_per_capita_ppp": "$20,800", "gdp_growth": "1.6% (2024); 2.5% (2025)",
        "currency": "COP", "avg_monthly_salary": "COP 3,350,000 (~$835 USD)",
        "avg_salary_usd": "$835", "minimum_wage": "COP 1,423,500/month (2025)",
        "it_salary_range": "Junior $27,000/year; Mid $41,000; Senior $54,000+ (USD annually)",
        "manufacturing_salary": "~COP 1,423,500/month (minimum baseline; ~$355 USD)",
        "unemployment": "8.8% (Dec 2024)",
        "ai_adoption": "Growing; strong fintech ecosystem in Bogota and Medellin",
        "internet_penetration": "73%", "literacy_rate": "95.3%",
        "stem_graduates": "~100,000 annually",
        "labor_force": "26 million",
        "key_industries": "Petroleum (45% exports), coal, coffee, flowers, bananas, manufacturing, fintech",
        "ai_risk_high": "Oil sector admin, BPO/call centers, basic financial services, data entry",
        "ai_risk_medium": "Manufacturing, banking, logistics, agriculture processing",
        "ai_risk_low": "Healthcare, education, tourism, coffee farming, creative industries",
        "key_challenges": "Slow growth (1.6-2.5%), labor informality (13.2M workers without formal contracts), fiscal pressure, external uncertainty, peace process implementation costs",
        "references": [
            ("World Bank - Colombia Overview", "https://www.worldbank.org/en/country/colombia/overview"),
            ("IMF - Colombia Article IV", "https://www.imf.org/en/Countries/COL"),
            ("DANE - Employment Statistics", "https://www.dane.gov.co/"),
            ("Deloitte - Colombia Economic Outlook", "https://www.deloitte.com/co/es.html"),
            ("Trading Economics - Colombia", "https://tradingeconomics.com/colombia/indicators"),
        ]
    },
    "argentina": {
        "name": "Argentina", "slug": "argentina-argentina", "population": "46 million",
        "gdp_per_capita": "$13,858", "gdp_per_capita_ppp": "$28,800", "gdp_growth": "Strong recovery H2 2024 (18%+ Q3)",
        "currency": "ARS", "avg_monthly_salary": "ARS 1,612,788 (~$900 USD at blue rate)",
        "avg_salary_usd": "$900", "minimum_wage": "ARS 296,832/month (2025)",
        "it_salary_range": "Junior $21,000/year; Mid $34,000; Senior $51,000 (USD annually)",
        "manufacturing_salary": "~ARS 296,832/month (minimum baseline)",
        "unemployment": "6.4% (Q4 2024)",
        "ai_adoption": "Growing; strong tech talent pool; Buenos Aires as regional tech hub",
        "internet_penetration": "87%", "literacy_rate": "99%",
        "stem_graduates": "~80,000 annually; strong university system",
        "labor_force": "22 million",
        "key_industries": "Agriculture (soybeans, beef, wine), manufacturing, automotive, mining (lithium), IT services, energy",
        "ai_risk_high": "Agricultural processing automation, call centers, financial back-office, data entry",
        "ai_risk_medium": "Manufacturing, banking, logistics, retail",
        "ai_risk_low": "Healthcare, education, skilled trades, creative industries, wine production",
        "key_challenges": "Hyperinflation legacy (211% end-2023, declined to 47% by April 2025), 42% workforce informality, dual exchange rates, political uncertainty under Milei reforms",
        "references": [
            ("World Bank - Argentina Data", "https://data.worldbank.org/country/argentina"),
            ("OECD - Argentina Economic Survey", "https://www.oecd.org/en/topics/sub-issues/economic-surveys-argentina.html"),
            ("INDEC - Employment Statistics", "https://www.indec.gob.ar/"),
            ("IMF - Argentina Country Report", "https://www.imf.org/en/Countries/ARG"),
            ("Buenos Aires Times - Economic Data", "https://www.batimes.com.ar/"),
        ]
    },
    "algeria": {
        "name": "Algeria", "slug": "algeria-algeria", "population": "46 million",
        "gdp_per_capita": "$5,631", "gdp_per_capita_ppp": "$15,300", "gdp_growth": "3.8% (2024)",
        "currency": "DZD", "avg_monthly_salary": "DZD 43,467 (~$335 USD)",
        "avg_salary_usd": "$335", "minimum_wage": "DZD 20,000/month (2025)",
        "it_salary_range": "DZD 93,500-140,000/month (~$720-1,080 USD)",
        "manufacturing_salary": "DZD 30,000-50,000/month (~$230-385 USD)",
        "unemployment": "9.7%",
        "ai_adoption": "Low; government digitalization initiatives underway",
        "internet_penetration": "76.9%", "literacy_rate": "81%",
        "stem_graduates": "~120,000 annually",
        "labor_force": "13 million",
        "key_industries": "Hydrocarbons (60% gov revenue, 90% exports), petroleum, natural gas, fertilizers, steel, cement",
        "ai_risk_high": "Oil sector admin, government bureaucracy, basic data processing",
        "ai_risk_medium": "Banking, telecom, manufacturing",
        "ai_risk_low": "Agriculture, healthcare, education, construction, oil extraction",
        "key_challenges": "Hydrocarbon revenue declining, current account deficit -3.7% GDP (2025), economic diversification urgently needed, youth unemployment, housing shortage",
        "references": [
            ("World Bank - Algeria Data", "https://data.worldbank.org/country/algeria"),
            ("African Development Bank - Algeria", "https://www.afdb.org/en/countries/north-africa/algeria"),
            ("Coface - Algeria Economic Profile", "https://www.coface.com/Economic-Studies/Algeria"),
            ("Trading Economics - Algeria", "https://tradingeconomics.com/algeria/indicators"),
            ("DataReportal - Digital 2025 Algeria", "https://datareportal.com/reports/digital-2025-algeria"),
        ]
    },
    "sudan": {
        "name": "Sudan", "slug": "sudan-sudan", "population": "51 million",
        "gdp_per_capita": "$712", "gdp_per_capita_ppp": "$3,900", "gdp_growth": "-37.5% (2023 due to conflict); minimal recovery",
        "currency": "SDG", "avg_monthly_salary": "~$36/month (severely impacted by conflict)",
        "avg_salary_usd": "$36", "minimum_wage": "SDG 425/month (2013 rate, heavily devalued)",
        "it_salary_range": "Effectively non-functional IT sector due to conflict",
        "manufacturing_salary": "Minimal formal manufacturing; wages severely depressed",
        "unemployment": "20.6% (2022, latest; likely much higher now)",
        "ai_adoption": "Essentially zero; infrastructure destroyed by conflict",
        "internet_penetration": "28.7%", "literacy_rate": "75.9%",
        "stem_graduates": "University system severely disrupted by conflict",
        "labor_force": "15 million (significantly disrupted)",
        "key_industries": "Oil, livestock, cotton, gum arabic, sorghum, sesame, food processing (all severely impacted by conflict)",
        "ai_risk_high": "N/A - economy in crisis; AI disruption is secondary to conflict recovery",
        "ai_risk_medium": "Oil sector operations (when restored), banking (when functional)",
        "ai_risk_low": "Agriculture, livestock, healthcare, humanitarian operations",
        "key_challenges": "Armed conflict since April 2023 causing 15,000+ deaths and 11 million displaced; GDP contracted 37.5% in 2023; inflation at 119% (late 2024); production capacity destroyed",
        "references": [
            ("World Bank - Sudan Overview", "https://www.worldbank.org/en/country/sudan/overview"),
            ("African Development Bank - Sudan", "https://www.afdb.org/en/countries/east-africa/sudan"),
            ("DataReportal - Digital 2025 Sudan", "https://datareportal.com/reports/digital-2025-sudan"),
            ("UNHCR - Sudan Crisis", "https://www.unhcr.org/emergencies/sudan-crisis"),
        ]
    },
}

# ============================================================
# AUDIENCE CONFIGS
# ============================================================
AUDIENCE_TITLES = {
    "ceo": "CEO & Business Leadership", "consumer": "Consumer & Household",
    "employee": "Employee & Workforce", "government": "Government & Policy",
    "investor": "Investor & Financial", "young-person": "Young Person & Student",
    "blue-collar-worker": "Blue-Collar & Frontline Worker", "educator": "Educator & Academic",
    "parent": "Parent & Family", "retiree": "Retiree & Senior",
    "small-business-owner": "Small Business Owner & Entrepreneur"
}

AUDIENCE_DESCS = {
    "ceo": "What happens to business leaders in {country} if AI hits and nobody prepared? A scenario memo from June 2030.",
    "consumer": "How will AI change everyday life in {country}? Bear case vs bull case — a scenario memo from June 2030.",
    "employee": "Will AI take your job in {country}? Two scenarios: what happens if you wait vs if you act now. A memo from 2030.",
    "government": "AI policy crossroads in {country}: the cost of inaction vs the payoff of smart governance. A 2030 scenario memo.",
    "investor": "Where does AI create value in {country} — and where does it destroy it? Bear vs bull case from June 2030.",
    "young-person": "Your career in {country}'s AI economy: two futures, one choice. A scenario memo from June 2030.",
    "blue-collar-worker": "AI and frontline jobs in {country}: the bear case (displacement) vs the bull case (transformation). A 2030 memo.",
    "educator": "AI in {country}'s classrooms: what happens if education adapts vs if it doesn't. Scenario memo from June 2030.",
    "parent": "Preparing your children for AI in {country}: two possible futures. A scenario memo from June 2030.",
    "retiree": "AI and retirement in {country}: how disruption threatens — or protects — your security. A 2030 scenario memo.",
    "small-business-owner": "AI vs small business in {country}: get disrupted or get ahead. Bear case vs bull case from June 2030."
}

# Short audience labels for memo headers
AUDIENCE_EDITIONS = {
    "ceo": "CEO & Board Strategy Edition",
    "consumer": "Consumer & Household Edition",
    "employee": "Workforce & Career Edition",
    "government": "Government & Policy Edition",
    "investor": "Investor & Portfolio Edition",
    "young-person": "Student & Early Career Edition",
    "blue-collar-worker": "Frontline & Trades Edition",
    "educator": "Education & Academic Edition",
    "parent": "Parent & Family Edition",
    "retiree": "Retirement & Senior Edition",
    "small-business-owner": "Small Business & Entrepreneur Edition"
}


def get_css():
    """Compact CSS."""
    return """<style>
:root{--bg-primary:#0a0a0f;--bg-secondary:#111118;--bg-card:#16161f;--bg-card-hover:#1c1c28;--border:#2a2a3a;--text-primary:#e4e4ef;--text-secondary:#9494a8;--text-muted:#6b6b80;--accent-blue:#3b82f6;--accent-purple:#8b5cf6;--accent-amber:#f59e0b;--accent-green:#10b981;--accent-red:#ef4444;--accent-cyan:#06b6d4;--gradient-1:linear-gradient(135deg,#3b82f6 0%,#8b5cf6 100%)}
*{margin:0;padding:0;box-sizing:border-box}html{scroll-behavior:smooth}
body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;background-color:var(--bg-primary);color:var(--text-primary);line-height:1.6}
a{color:var(--accent-blue);text-decoration:none}a:hover{color:var(--accent-purple)}
button{background:none;border:none;cursor:pointer;font-family:inherit}
.site-header{position:sticky;top:0;z-index:1000;background:rgba(10,10,15,0.95);backdrop-filter:blur(10px);border-bottom:1px solid var(--border)}
.header-inner{max-width:1200px;margin:0 auto;padding:0.75rem 1.5rem;display:flex;align-items:center;justify-content:space-between}
.site-logo{font-size:1.4rem;font-weight:700;background:var(--gradient-1);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}
.nav-links{display:flex;align-items:center;gap:1.5rem;list-style:none}.nav-links a{color:var(--text-secondary);font-weight:500;font-size:0.95rem}
.nav-toggle{display:none}
.breadcrumb{max-width:900px;margin:1rem auto;padding:0 1.5rem;display:flex;align-items:center;gap:0.5rem;font-size:0.85rem;color:var(--text-muted)}.breadcrumb a{color:var(--text-secondary)}
.article-header{max-width:900px;margin:0 auto 2rem;padding:0 1.5rem}
.article-meta{display:flex;flex-wrap:wrap;gap:1rem;align-items:center;margin-bottom:1.5rem}
.meta-badge{padding:0.35rem 0.75rem;border-radius:0.25rem;font-size:0.8rem;font-weight:600}
.badge-country{background:rgba(59,130,246,0.15);color:var(--accent-blue)}.badge-audience{background:rgba(139,92,246,0.15);color:var(--accent-purple)}.badge-date{background:rgba(107,107,128,0.1);color:var(--text-muted)}
.article-content{max-width:900px;margin:0 auto;padding:0 1.5rem 4rem;font-size:1.05rem}
.article-content h1{font-size:1.75rem;margin:2rem 0 1rem;font-weight:700}.article-content h1:first-child{margin-top:0}
.article-content h2{font-size:1.5rem;margin:2.5rem 0 1rem;font-weight:700;padding-bottom:0.5rem;border-bottom:1px solid var(--border)}
.article-content h3{font-size:1.2rem;margin:1.5rem 0 0.75rem}
.article-content p{margin-bottom:1rem;color:var(--text-secondary);line-height:1.7}
.article-content ul,.article-content ol{margin:0 0 1rem 1.5rem;color:var(--text-secondary)}.article-content li{margin-bottom:0.5rem;line-height:1.6}
.article-content table{width:100%;border-collapse:collapse;margin:1.5rem 0;font-size:0.95rem}
.article-content th{background:var(--bg-card);padding:0.75rem 1rem;text-align:left;font-weight:600;border:1px solid var(--border)}
.article-content td{padding:0.75rem 1rem;border:1px solid var(--border);color:var(--text-secondary)}
.article-content blockquote{border-left:3px solid var(--accent-blue);padding:1rem 1.5rem;margin:1.5rem 0;background:var(--bg-card);border-radius:0 0.25rem 0.25rem 0}
.sibling-editions{max-width:900px;margin:0 auto;padding:0 1.5rem 2rem}
.sibling-editions h3{font-size:1.1rem;color:var(--text-secondary);margin-bottom:1rem}
.sibling-pills{display:flex;flex-wrap:wrap;gap:0.5rem}
.sibling-pill{padding:0.5rem 1rem;background:var(--bg-card);border:1px solid var(--border);border-radius:2rem;color:var(--text-secondary);font-size:0.85rem;font-weight:500;text-decoration:none}
.sibling-pill:hover{border-color:var(--accent-blue);color:var(--accent-blue)}.sibling-pill.active{background:var(--accent-blue);color:white;border-color:var(--accent-blue)}
.social-share-bar{display:flex;align-items:center;gap:0.75rem;padding:1.25rem 0;margin:2rem 0;border-top:1px solid var(--border);border-bottom:1px solid var(--border);flex-wrap:wrap}
.social-share-bar span{font-weight:600;color:var(--text-secondary);font-size:0.9rem}
.share-btn{display:inline-flex;align-items:center;gap:0.4rem;padding:0.5rem 1rem;border-radius:0.5rem;font-size:0.85rem;font-weight:600;text-decoration:none;color:white}
.share-btn.linkedin{background:#0077b5}.share-btn.twitter{background:#1d9bf0}.share-btn.whatsapp{background:#25d366}
.share-btn.copy-link{background:var(--bg-card);color:var(--text-primary);border:1px solid var(--border)}
.email-capture{background:linear-gradient(135deg,#1a1a2e 0%,#16213e 100%);border:1px solid var(--border);border-radius:1rem;padding:2rem 1.5rem;margin:3rem auto 0;max-width:700px;text-align:center}
.email-capture h3{font-size:1.2rem;margin-bottom:0.5rem}.email-capture p{color:var(--text-secondary);font-size:0.95rem;margin-bottom:1rem}
.email-capture-form{display:flex;gap:0.5rem;max-width:450px;margin:0 auto}
.email-capture-form input{flex:1;padding:0.7rem 1rem;border:1px solid var(--border);border-radius:0.5rem;background:rgba(255,255,255,0.05);color:var(--text-primary);font-size:0.95rem}
.email-capture-form button{padding:0.7rem 1.25rem;background:var(--accent-blue);color:#fff;border:none;border-radius:0.5rem;font-weight:600;cursor:pointer;white-space:nowrap}
.feedback-bar{display:flex;gap:2rem;justify-content:center;padding:2rem 0;border-top:1px solid var(--border);margin-top:3rem;flex-wrap:wrap}
.feedback-bar a{color:var(--text-secondary);font-weight:500;display:inline-flex;align-items:center;gap:0.5rem}
.site-footer{text-align:center;padding:2rem;border-top:1px solid var(--border);color:var(--text-muted);font-size:0.85rem;margin-top:4rem}
.references-section{margin-top:3rem;padding-top:2rem;border-top:2px solid var(--border)}
.references-section h2{font-size:1.3rem;margin-bottom:1rem}.references-section ol{padding-left:1.5rem}
.references-section li{margin-bottom:0.5rem;font-size:0.9rem;color:var(--text-secondary);word-break:break-word}.references-section a{color:var(--accent-blue)}
.reading-progress{position:fixed;top:0;left:0;width:0%;height:3px;background:var(--gradient-1);z-index:9999}
.scroll-top{position:fixed;bottom:2rem;right:2rem;width:48px;height:48px;background:var(--accent-blue);color:white;border:none;border-radius:50%;font-size:1.5rem;cursor:pointer;display:none;z-index:100;align-items:center;justify-content:center}
.theme-toggle{background:none;border:1px solid var(--border);border-radius:6px;padding:0.4rem 0.6rem;cursor:pointer;color:var(--text-secondary);font-size:1rem;margin-left:0.5rem}
html.light-theme{--bg-primary:#f5f5f7;--bg-secondary:#eeeef0;--bg-card:#ffffff;--bg-card-hover:#f0f0f2;--border:#d1d5db;--text-primary:#1a1a2e;--text-secondary:#4a4a5e;--text-muted:#6b7280}
html.light-theme .site-header{background:rgba(245,245,247,0.95)!important}
@media(max-width:768px){.article-header h1{font-size:1.75rem}.article-content{font-size:1rem}.nav-links{display:none!important;position:fixed!important;top:0!important;right:0!important;width:280px!important;height:100vh!important;background:var(--bg-secondary)!important;flex-direction:column!important;padding:5rem 2rem 2rem!important;z-index:999!important;box-shadow:-5px 0 15px rgba(0,0,0,0.3)!important;border-left:1px solid var(--border)!important}.nav-links.active{display:flex!important}.nav-toggle{display:flex!important;flex-direction:column;gap:5px;z-index:1001;padding:0.5rem}.nav-toggle span{display:block;width:24px;height:2px;background:var(--text-primary)}.mobile-overlay{display:none;position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,0.5);z-index:998}.mobile-overlay.active{display:block}body.nav-open{overflow:hidden!important}.email-capture-form{flex-direction:column}.share-btn{padding:0.6rem 1rem;font-size:0.85rem}.sibling-pill{padding:0.5rem 1rem;font-size:0.85rem}}
</style>"""


import html, re


def parse_industries(c):
    raw = c.get("key_industries", "")
    parts = re.split(r',\s*', raw)
    return [p.strip() for p in parts if p.strip() and len(p.strip()) > 1]


def parse_risks(risk_str):
    parts = re.split(r',\s*', risk_str)
    return [p.strip() for p in parts if p.strip() and len(p.strip()) > 1]


def get_top3(c):
    """Return top 3 industries for scenario building."""
    inds = parse_industries(c)
    if len(inds) >= 3:
        return inds[0], inds[1], inds[2]
    elif len(inds) == 2:
        risks = parse_risks(c.get("ai_risk_high", ""))
        third = risks[0] if risks else "services"
        return inds[0], inds[1], third
    elif len(inds) == 1:
        risks = parse_risks(c.get("ai_risk_high", ""))
        second = risks[0] if risks else "services"
        third = risks[1] if len(risks) > 1 else "retail"
        return inds[0], second, third
    return "manufacturing", "services", "retail"


def clean_salary(raw):
    """Extract the first clean salary figure from a raw field for prose use."""
    if not raw:
        return "the local average"
    # Take only the first part before semicolons (drop secondary notes)
    clean = raw.split(";")[0].strip()
    # Remove parenthetical notes for cleaner prose
    clean = re.sub(r'\s*\([^)]*\)', '', clean).strip()
    return clean if clean else raw


def clean_field(raw):
    """Clean a data field for use in prose — remove parenthetical qualifiers."""
    if not raw:
        return ""
    # Handle semicolons: split BEFORE removing parens so we can check year info
    if ";" in raw:
        # Check if semicolons are INSIDE parentheses (don't split those)
        # Simple heuristic: count open parens before each semicolon
        outside_semi = []
        depth = 0
        current = ""
        for ch in raw:
            if ch == '(':
                depth += 1
                current += ch
            elif ch == ')':
                depth -= 1
                current += ch
            elif ch == ';' and depth == 0:
                outside_semi.append(current.strip())
                current = ""
            else:
                current += ch
        outside_semi.append(current.strip())

        if len(outside_semi) > 1:
            # Multiple real parts — pick the best one
            best = outside_semi[0]
            for p in reversed(outside_semi):
                if re.search(r'20(25|26)', p):
                    best = p
                    break
            raw = best
    # Now remove parenthetical notes
    clean = re.sub(r'\s*\([^)]*\)', '', raw).strip()
    return clean.strip() if clean.strip() else raw


def extract_currency(c):
    """Get the currency code."""
    return c.get("currency", "USD")


def get_risk_jobs(c):
    """Get the top 3 high-risk job categories."""
    risks = parse_risks(c.get("ai_risk_high", ""))
    if len(risks) >= 3:
        return risks[0], risks[1], risks[2]
    elif len(risks) >= 2:
        return risks[0], risks[1], "administrative services"
    elif len(risks) >= 1:
        return risks[0], "administrative services", "data entry"
    return "manufacturing", "administrative services", "data entry"


def gen_content(c, aud):
    """Generate audience-specific article content — gold standard quality."""
    n = c["name"]
    edition = AUDIENCE_EDITIONS[aud]
    cur = extract_currency(c)
    ind1, ind2, ind3 = get_top3(c)
    risk1, risk2, risk3 = get_risk_jobs(c)
    sal = clean_salary(c.get("avg_monthly_salary", ""))
    mfg_sal = clean_salary(c.get("manufacturing_salary", ""))
    it_sal = clean_salary(c.get("it_salary_range", ""))
    min_wage = clean_salary(c.get("minimum_wage", ""))
    gdp_pc = clean_field(c.get("gdp_per_capita", ""))
    gdp_ppp = clean_field(c.get("gdp_per_capita_ppp", ""))
    gdp_gr = clean_field(c.get("gdp_growth", ""))
    pop = c.get("population", "")
    lf = c.get("labor_force", "")
    unemp = clean_field(c.get("unemployment", ""))
    inet = clean_field(c.get("internet_penetration", ""))
    lit = clean_field(c.get("literacy_rate", ""))
    stem = clean_field(c.get("stem_graduates", ""))
    challenges = c.get("key_challenges", "")
    # Clean challenges for prose — take first main point only
    challenge_short = challenges.split(",")[0].strip() if challenges else "structural economic pressures"

    memo_header = f"""<div class="memo-header" style="border:1px solid var(--border);border-radius:var(--radius);padding:1.5rem 2rem;margin-bottom:2rem;background:var(--bg-card);">
<p style="font-family:var(--font-mono,monospace);font-size:0.85rem;color:var(--accent-blue);margin-bottom:0.5rem;letter-spacing:1px;">A MACRO INTELLIGENCE MEMO &bull; JUNE 2030 &bull; {html.escape(edition.upper())}</p>
<p style="color:var(--text-secondary);font-size:0.9rem;margin-bottom:0.25rem;"><strong>From:</strong> The 2030 Intelligence Unit</p>
<p style="color:var(--text-secondary);font-size:0.9rem;margin-bottom:0.25rem;"><strong>Date:</strong> June 2030</p>
<p style="color:var(--text-secondary);font-size:0.9rem;"><strong>Re:</strong> {html.escape(n)} &mdash; AI Disruption Scenario Assessment</p>
</div>"""

    body = ""

    # =========================================================================
    # CEO (A-priority, 2500-3000 words target)
    # =========================================================================
    if aud == "ceo":
        body = f"""{memo_header}
<h1>{n}: The AI Reckoning for Business Leaders &mdash; Five Years Later</h1>

<p>You run a mid-size company in {n}, operating in the {ind1.lower()} sector. In 2025, your economy had a GDP per capita of {gdp_pc}, with growth running at {gdp_gr} and a workforce of {lf}. Your workers earned an average of {sal}, and the industries that powered {n}&mdash;{ind1.lower()}, {ind2.lower()}, and {ind3.lower()}&mdash;felt established enough to weather any disruption. You had operated with the same business model for over a decade, profitable and stable within {n}'s borders. International competition existed but felt manageable. Labor was reliable and inexpensive at {mfg_sal} for skilled manufacturing work. But by June 2030, the AI transformation has divided {n}'s business landscape into winners and losers with a sharpness that caught many leaders off guard.</p>

<p>Between 2025 and 2027, AI adoption moved from corporate pilots and academic discussion into mainstream business operations. The inflection was faster than most executives anticipated. By 2027, companies that had begun their AI transformation in 2025 had already captured competitive advantages that newer entrants could not quickly replicate. The phase was one of consolidation: early movers strengthened their market positions, while laggards fell further behind. By 2028&ndash;2029, the window for a "managed transition" had largely closed. Organizations entering the AI era after 2028 faced not a transformation opportunity but a crisis response. This memo examines both futures&mdash;because the one you chose in 2025 determined which side you ended up on.</p>

<h2>THE BEAR CASE: Three Companies That Waited Too Long</h2>

<p><strong>Scenario 1: The {ind1} Company That Calculated Wrong</strong><br/>
You ran a {ind1.lower()} firm with 200 employees earning {mfg_sal}. In 2025, you ran the numbers on AI adoption and concluded it was premature&mdash;your labor costs were competitive, your margins were stable at 12&ndash;15%, and your clients were loyal. You budgeted nothing for AI transformation. The business was working, after all. Why fix what wasn't broken? By 2027, an AI-equipped competitor had entered your market, and the calculation was suddenly exposed as naive. Their production costs were 30% lower because AI-driven automation handled quality control, scheduling, and predictive maintenance. Their machines didn't sleep, didn't make tired mistakes, and learned from each batch to optimize the next one. Your clients didn't leave immediately&mdash;but they started demanding price concessions. By Q3 2027, you were matching prices you couldn't sustain. Your margins compressed from 12% to 4%. Production that generated profit at the old pricing generated losses at the new prices.</p>

<p>By 2028, the situation had cascaded. Your best technical workers&mdash;the ones who could have managed an AI transition&mdash;left for competitors who paid more and offered more interesting work. You were left with a workforce that couldn't adapt and a cost structure that couldn't compete. You finally attempted an AI implementation in 2028, but your depleted team couldn't execute it well. The AI systems you bought cost more than they should have because you hired in desperation. Implementation dragged on. By 2030, your revenue had dropped 40%, your profit margin had evaporated, and you were considering selling the company at a fraction of its 2025 valuation. The worst part: the company that had beaten you was willing to acquire you at a price you should have been disgusted by in 2025 but had to accept in 2030.</p>

<p><strong>Scenario 2: The {ind2} Executive Who Underestimated Speed</strong><br/>
You led a well-known {ind2.lower()} operation in {n}, employing 350 people with a strong domestic reputation built over two decades. In 2025, you acknowledged AI was coming&mdash;but planned a "gradual adoption" timeline stretching to 2029. You allocated a modest budget for pilot programs, figuring five years was plenty of time to manage the transition. Gradual adoption sounded prudent. Measured. Professional. By 2027, the pilot was still in testing while your international competitors had fully deployed AI-powered operations. The gap wasn't incremental&mdash;it was structural. Their AI systems processed information in hours that took your team weeks. Clients who once valued your local knowledge now valued speed and accuracy more. You couldn't offer speed. Your process was still fundamentally manual, just with better spreadsheets.</p>

<p>By 2028, you had lost your three largest accounts to AI-native competitors who could deliver in real time what used to take you weeks. The pilot program that was supposed to save you hadn't even reached production. Your organizational confidence had eroded. When you finally tried to accelerate the deployment, execution suffered because your team had been waiting, not learning. The talent pool to rebuild was empty&mdash;AI engineers in {n} commanding {it_sal} were already locked up by first-movers. You tried to hire them anyway at premium rates, but the candidates you got were junior, and training them while managing the crisis meant your timeline extended another two years. By 2030, your workforce had shrunk from 350 to 220 through attrition. Your revenue had declined 25%. And you still weren't competitive with the companies that had started in 2025.</p>

<p><strong>Scenario 3: The {ind3} Firm Caught in the Talent Trap</strong><br/>
You operated a profitable {ind3.lower()} business serving {n}'s domestic market, generating solid returns at {sal} average productivity per worker. In 2025, you decided to invest in AI&mdash;but half-heartedly. You hired two junior developers and asked them to "build something with AI." No senior architect to guide them. No clear strategy for what you wanted to build. No adequate budget. The project stalled almost immediately because junior developers, left to their own devices, built technically interesting things that didn't match business needs. Meanwhile, your competitors partnered with established AI vendors or hired dedicated senior teams at {it_sal}. By 2028, you had spent two years and significant capital with nothing to show. Your half-built system was obsolete before it launched because the landscape had moved on. The worst part: your competitors had used that same two years to train their entire existing workforce on AI tools, creating a permanent capability gap you couldn't close even with new hires.</p>

<p>By 2030, the cost of catching up had tripled. You needed to hire senior AI talent (expensive), rebuild the system properly (consuming more capital), and accelerate market adaptation (demanding resources you no longer had). The company that had waited to "make the right decision" had ended up making no decision, then rushing to make a bad decision at the worst time. The revenue that might have funded a proper AI transition was declining. You were forced to choose between laying people off to fund AI implementation or continuing to decline without transformation. Either choice was brutal.</p>

<h2>THE BULL CASE: The Same Three Companies That Acted Decisively</h2>

<p><strong>Scenario 1: The {ind1} Company That Invested in Q3 2025</strong><br/>
Same company, different decision. Instead of waiting, you allocated 5% of annual revenue to AI transformation in Q3 2025. You hired an AI lead at {it_sal}&mdash;expensive by {n} standards, but you framed it as an investment, not a cost. You gave them autonomy and support. By Q2 2026, the results were undeniable. AI-driven quality control had reduced your defect rate by 60%. Predictive maintenance cut your downtime by 40%. You were producing more product, faster, with fewer errors. By 2027&mdash;the same year your Bear Case counterpart was losing clients&mdash;you were gaining them. Cost per unit dropped 25% while quality improved. Competitors who hadn't invested yet couldn't match your pricing and quality simultaneously.</p>

<p>The workers earning {mfg_sal} who had been doing manual quality checks were retrained as AI system operators, earning 30&ndash;40% more. They didn't see the technology as a threat because you invested in them, not just the machines. Morale improved. Talent retention improved. Your margins expanded from 12% to 18%. By 2030, you had doubled your market share in {n}. Your employees, who could have been disrupted, instead became the people who operated the AI systems that disrupted your competitors. The company that waited was now a acquisition target you could afford to buy at a fair price, knowing you could integrate their operations into your AI-enhanced processes and immediately realize 40% cost reduction.</p>

<p><strong>Scenario 2: The {ind2} Leader Who Set a 12-Month Deadline</strong><br/>
Same {ind2.lower()} firm, different timeline. Instead of a four-year "gradual adoption" plan, you set a 12-month deadline: AI capabilities deployed across core operations by Q3 2026. You didn't build from scratch; you partnered with an established AI vendor who had done this before. You invested in retraining your 350 employees&mdash;not all became AI experts, but all became AI-literate. You didn't ask them to become data scientists; you asked them to work effectively alongside AI tools. By Q4 2026, your team was delivering work in days that previously took weeks. Processing time for client requests dropped from 14 days to 2. Client satisfaction scores jumped measurably. You became known as fast and reliable, not just domestically but to regional clients.</p>

<p>By 2028&mdash;when your Bear Case counterpart was losing accounts&mdash;you were onboarding new ones. The reputation for speed and reliability was worth more than the reputation for local knowledge had been. Your revenue grew 35% between 2026 and 2030. More importantly, you had a 24-month head start on the companies that began in 2028, a gap that proved impossible to close. The talent you had trained in 2026 had two years of experience by 2028, making them more valuable than the expensive outside hires other companies had to recruit. By 2030, you were the most sought-after employer in your sector in {n} because you had invested in your people's futures, not just your own.</p>

<p><strong>Scenario 3: The {ind3} Firm That Built an AI Partnership</strong><br/>
Same business, smarter approach to talent. Instead of hiring two junior developers and hoping they'd figure it out, you partnered with a regional AI consultancy and dedicated one senior manager full-time to the transformation. The partnership cost was manageable&mdash;structured as a risk-share rather than a fixed cost. You only paid for results. By 2027, you had a working AI system customized to your operations. Your existing workers were trained to use it. You didn't lose people; you upgraded them. By 2028, you were licensing your AI-enhanced processes to smaller competitors who didn't have the capability to build their own systems. You had turned a cost center into a revenue stream.</p>

<p>By 2030, AI-related services accounted for 20% of your revenue. Your original {ind3.lower()} business was more profitable than ever because of AI-driven efficiency gains. You had transformed from a pure-play {ind3.lower()} company into a hybrid company that did {ind3.lower()} with AI advantage. That transformation would have been possible for your Bear Case counterpart too, but only if they had started in 2025. Starting in 2028, the window had largely closed.</p>

<h2>THE INFLECTION POINT: Why 2025-2026 Mattered More Than Any Year Before or Since</h2>

<p>The three years from 2025 to 2027 created a permanent separation between leaders and laggards. This wasn't just because the technology improved; it was because organizations that moved early accumulated experience, trained personnel, and client relationships that later entrants couldn't replicate quickly. The companies that started in 2026 could still catch companies that started in 2027 if they moved fast enough and had enough capital. But the companies that started in 2028 could never catch the companies that started in 2025. The gap was structural, not just temporal. This is why the decision you made in 2025 mattered more than the decisions you'd made in any year of your career.</p>

<h2>WHAT YOU SHOULD DO NOW</h2>

<p><strong>1. Conduct an AI Vulnerability Audit This Month</strong><br/>
Map every revenue-generating process in your company against current AI capabilities. Identify the three processes most vulnerable to AI-equipped competitors. This is not a technology exercise&mdash;it is a survival exercise. The CEOs who did this in 2025 made better decisions than those who guessed. Ask: which competitors could steal this process from us with AI? What would it cost them? If it's less than our margin on that process, we have a problem. If we don't fix it now, by 2027 we may not be able to afford to fix it.</p>

<p><strong>2. Set a 12-Month AI Deployment Deadline</strong><br/>
Not a pilot. Not a study. Not a "phase-in plan." A deployed, operational AI capability in your highest-vulnerability area within 12 months. Allocate 3&ndash;5% of annual revenue. The companies that set aggressive timelines outperformed those with "gradual" plans by a wide margin. The cost of waiting another year for perfect conditions will be measured in lost market share, not in savings from slower spending. Create accountability: if your AI capability isn't live in 12 months, your leadership team should face consequences.</p>

<p><strong>3. Hire or Partner for AI Expertise Immediately</strong><br/>
AI talent in {n} commands {it_sal}. It's expensive. If you cannot afford a full-time hire, partner with an AI consultancy on a risk-share basis. What you cannot afford is no AI expertise at all. Every month without AI capability is a month your competitors are pulling ahead, accumulating experience you'll eventually have to replicate. Senior AI engineers are expensive, but late-stage crisis hiring to catch up is far more expensive.</p>

<p><strong>4. Retrain Your Existing Workforce Aggressively</strong><br/>
Your workers earning {mfg_sal} are not liabilities&mdash;they are assets who know your business, understand your clients, and have domain expertise that no external hire brings. Invest in making them AI-literate. The companies that retained and retrained their workforce outperformed those that tried to replace workers with technology alone. AI-augmented humans beat pure AI systems in most real-world applications. Your workers plus AI is your strategy.</p>

<p><strong>5. Benchmark Against International Competitors</strong><br/>
Your competition is no longer only domestic. Any AI-native company with access to {n}'s market is a threat. Measure your AI readiness against global leaders in {ind1.lower()}, {ind2.lower()}, and {ind3.lower()}, not just local peers. If your competitors are six months ahead in AI deployment, you're already losing. Make aggressive competitive analysis a quarterly board exercise, not an annual one.</p>

<p><strong>6. Make AI a Board-Level Priority</strong><br/>
Create a quarterly AI transformation review at the board level. Assign clear ownership, measurable milestones, and consequences for delay. The companies where AI was a "department initiative" failed because it competed for resources with existing business priorities. The ones where the CEO owned it succeeded because it was protected, funded, and accelerated. Your board needs to discuss AI readiness the way they discuss quarterly earnings. More often, actually.</p>

<h2>THE BOTTOM LINE</h2>

<p>From our June 2030 vantage point, the evidence from {n} is unambiguous: the CEOs who invested in AI in 2025&ndash;2026 are running stronger, more profitable companies. Those who waited until 2028 or later are fighting for survival. The transformation cost was manageable in 2025. By 2028, it had tripled. By 2030, for many companies, it was too late. The capital that could have funded a proper transformation had been depleted by years of margin compression. The personnel who could have driven it had already left. The market position that could have supported the transition cost had eroded.</p>

<p>The window for AI transformation in {n} is still open today, but it is closing. Every quarter of delay compounds your competitive disadvantage exponentially, not linearly. The companies that started their transformation six months ago from now are already pulling away from those waiting for certainty. Certainty will not come. You will never feel certain that 2030 is the right time to start. You will only know, with certainty, by 2035 whether you started in time.</p>"""

    # =========================================================================
    # EMPLOYEE (A-priority, 2500-3000 words)
    # =========================================================================
    elif aud == "employee":
        body = f"""{memo_header}
<h1>{n}: What AI Did to Workers Who Waited &mdash; And Those Who Didn't</h1>

<p>You work in {n}, earning {sal}, and you spend your days in work that feels meaningful and secure. Maybe you are in {risk1.lower()}, or {risk2.lower()}, or {risk3.lower()}&mdash;the sectors that employ millions across {n}'s workforce of {lf}. You have accumulated skills over years, learned your industry's rhythms, built relationships with colleagues and supervisors. In 2025, your job felt stable. You had skills, experience, and a role that seemed secure. GDP per capita was {gdp_pc}, growth was running at {gdp_gr}, and while people talked about AI disruption in other countries and other sectors, it felt distant&mdash;something that would happen to someone else, not to you. Your sector had been the backbone of {n}'s economy for decades. Surely there was inertia enough to protect you.</p>

<p>By June 2030, that assumption has been thoroughly tested, and the results are unambiguous. The workforce in {n} has divided into two groups: those who adapted early and are earning significantly more with greater job security, and those who waited and are struggling to find meaningful work at any wage. The divide isn't generational; it's not based on education level or initial role. It's based entirely on the choice made between 2025 and 2026: to invest in AI skills or to assume that experience alone would protect your career. This memo tells both stories.</p>

<h2>THE BEAR CASE: Three Workers Who Waited</h2>

<p><strong>Scenario 1: The {risk1} Worker Who Believed Experience Was Enough</strong><br/>
You had eight years of experience in {risk1.lower()} in {n}, earning {mfg_sal}, having progressed from entry-level to a solid mid-career position. Your supervisors valued your reliability. You knew the processes cold. You could troubleshoot problems instinctively. You assumed that this combination&mdash;reliability plus deep experience&mdash;would protect your role even if AI came to your sector. It was a reasonable assumption based on everything you'd observed in your career. By 2027, that assumption collided with reality. AI systems could perform 70% of your routine tasks faster and with fewer errors than even the most reliable human worker. Your employer didn't fire you immediately&mdash;they reduced your hours. From 40 hours per week, you went to 30, then 24. Your monthly income dropped proportionally from {mfg_sal} to 60% of {mfg_sal}. The reduced hours meant you could no longer build expertise in new areas; you were too scattered across part-time work.</p>

<p>By 2028, the company restructured entirely. The new roles didn't require deep experience with the old processes; they required the ability to manage AI systems, interpret their outputs, and handle exceptions. You didn't have those skills. You were offered a severance package or a junior position at near-minimum-wage of {min_wage}. Your eight years of experience counted for nothing in the new structure. It was a bitter lesson: experience in a domain doesn't transfer when the domain's fundamental tools change. By 2030, you are earning 40% less than in 2025, in a role with no advancement pathway, no prestige, and no sense that your work matters. Younger workers with AI skills, but less domain experience, are earning more than you and are positioned to earn far more in the future.</p>

<p><strong>Scenario 2: The {risk2} Professional Who Resisted Retraining</strong><br/>
You worked in {risk2.lower()} earning slightly above the national average of {sal}, a professional role that required judgment, client interaction, and deep knowledge of regulations and best practices. In 2026, your employer offered a subsidized AI skills program&mdash;evening classes, six months, minimal personal cost. You declined. The program seemed unnecessary, time-consuming, and somehow insulting&mdash;a suggestion that your established professional skills weren't enough. The program seemed to assume you'd want to become technical, and you didn't. You were a {risk2.lower()} professional, not a technologist. Your work relied on human judgment and relationships. How could an AI tool improve that? The assumption felt reasonable at the time. Eighteen months later, the colleagues who took the program were promoted to AI-augmented roles paying 35&ndash;50% more. They weren't replacing your job with machines; they were enhancing their jobs with AI tools. They could analyze documents faster, research faster, make recommendations faster. They became dramatically more productive, and the firm rewarded them for it. You were passed over for promotion.</p>

<p>By 2028, your department shrank from 40 people to 15. The 15 who remained were the ones with AI skills. You were among the 25 who were let go. Job hunting in 2029 was brutal&mdash;every posting required "AI proficiency" or "experience with AI tools," qualifications you didn't have. Unemployment in {n} was officially {unemp}, but for workers without AI skills in disrupted sectors like {risk2.lower()}, the effective rate was far higher. You ended up taking a lateral move to a smaller firm at lower pay, telling yourself it was temporary. By 2030, you still haven't found a role that matches your old compensation or status. The resistance to retraining that felt principled in 2025 proved to be one of the worst career decisions of your life.</p>

<p><strong>Scenario 3: The {risk3} Employee Who Ran Out of Options</strong><br/>
You worked in {risk3.lower()}, a role you assumed would always require a human touch, always need human judgment. The task was too nuanced, too contextual, too dependent on understanding what clients really needed versus what they said they needed. In 2025, you were right&mdash;AI couldn't fully replace you. But by 2028, AI had developed in ways you hadn't anticipated. The systems could handle 80% of the routine components of your work. Your role shrank to the remaining 20%&mdash;the exceptions, the edge cases, the human judgment calls. That 20% was real work, genuinely valuable work. But it wasn't enough to justify a full-time salary at {sal}. Your employer restructured you to part-time, calling you in only when the AI system flagged something it couldn't resolve. Your income dropped to less than half what you'd earned in 2025.</p>

<p>Worse, the AI system was learning from every case you resolved. Each exception you handled became training data for the next iteration. The percentage of cases that required human judgment was declining month over month. By 2030, you were barely working, called in a few hours per month at part-time rates, watching your career evaporate in real time. You had skilled work to do, but there wasn't enough of it to constitute a career. You were over 40, skills in a dying domain, no backup plan. You were considering a complete career change at an age when starting over feels impossible, knowing you'd be competing against people half your age with no domain expertise to fall back on.</p>

<h2>THE BULL CASE: The Same Three Workers Who Acted Early</h2>

<p><strong>Scenario 1: The {risk1} Worker Who Retrained in 2025</strong><br/>
Same person, different choice. When you heard about AI disruption in {risk1.lower()}, you didn't wait for your employer to act or deny the threat. In late 2025, you enrolled in a six-month AI operations certificate&mdash;evenings and weekends, sacrificing leisure time, pushing yourself hard. The cost was the equivalent of one month's salary at {mfg_sal}. It was a meaningful expense. By mid-2026, you were certified. Your employer, seeing your initiative, immediately reassigned you to manage the new AI systems being deployed. You were the only person in your department who understood both the old processes and the new technology. You became invaluable. Your value skyrocketed because you could translate between the domain experts (who didn't understand the AI) and the AI systems (that didn't understand the context). By 2027, you were promoted to operations lead. By 2028, you were earning 50% more than your 2025 salary. By 2030, you managed a team of AI system operators and was being recruited by competing firms at salaries you would have thought impossible in 2025.</p>

<p>Your eight years of domain experience, combined with AI skills, made you irreplaceable in ways that either skill alone could not. The company valued you not because you were an AI expert (they could hire those) but because you were a domain expert who understood AI. That combination proved to be the most valuable capability in the transformed sector. Your career had been disrupted, but you disrupted it yourself, on your terms, and came out ahead.</p>

<p><strong>Scenario 2: The {risk2} Professional Who Took the Retraining</strong><br/>
Same company, same offer. You said yes to the AI skills program. Six months of evening classes, sacrificing your personal time, pushing yourself. The content wasn't easy, but it wasn't overwhelming either&mdash;practical applications of AI tools to your existing work, not theoretical computer science or programming. You learned how to use AI for research, analysis, document drafting, and recommendation-building. You saw how it could amplify what you already did well. By Q2 2027, you were among the first employees certified. When promotions to AI-augmented roles opened, you were selected. Your salary increased 35% immediately, with a clear path to further growth. While 25 of your former colleagues were laid off in 2028, you were promoted again to lead a team. By 2030, you earned more than double your 2025 salary and had genuine job security&mdash;AI skills plus domain expertise made you the exact profile every employer in {n}'s economy wanted.</p>

<p>You had bet on yourself, on retraining, on the possibility that AI could enhance rather than replace your work. The bet had paid off beyond what you'd anticipated. More importantly, you had the satisfaction of knowing you'd made the right call, bet on yourself, and won.</p>

<p><strong>Scenario 3: The {risk3} Employee Who Pivoted</strong><br/>
Same role, but you read the situation differently. You recognized that AI would gradually absorb the routine components of your work, and instead of waiting for the squeeze to tighten, you pivoted proactively. In 2026, you moved into an AI-adjacent role&mdash;training AI systems using your domain expertise. You became the person who taught the AI how to handle the edge cases, how to understand context, how to apply judgment. This role didn't exist in 2025, but by 2027 it was one of the most in-demand positions in {n}. You were invaluable because you combined deep domain knowledge with the ability to systematize it in ways machines could learn from. Your salary grew steadily as demand for your skills accelerated. By 2030, you were a senior AI training specialist earning well above the national average of {sal}, with job offers from multiple employers and complete security in your role.</p>

<p>Your deep knowledge of {risk3.lower()} became more valuable, not less&mdash;because you found the right way to combine it with AI. You had seen the disruption coming and positioned yourself not to defend against it but to profit from it.</p>

<h2>THE INFLECTION: What Separated the Workers Who Thrived from Those Who Didn't</h2>

<p>The difference between these two paths came down to a single choice made between 2025 and 2026. Not a huge choice, not a risky choice with uncertain payoff. Just a decision to invest a few months and modest resources in learning new skills. The workers who made that choice had time to learn, time to build credibility in the new skills before those skills became mandatory. The workers who waited until 2027 or 2028 were trying to learn new skills while simultaneously being evaluated on how quickly they could master them. That's a much harder position. By 2029, the workers who still hadn't adapted were no longer competing on merit; they were simply being replaced.</p>

<h2>WHAT YOU SHOULD DO NOW</h2>

<p><strong>1. Assess Your Role's AI Vulnerability Honestly</strong><br/>
Ask yourself: what percentage of your daily work could an AI system handle within two years? Not perfectly, but acceptably. If the answer is above 50%, you are in a high-risk role. This is not speculation; it is the pattern that played out across {n} between 2025 and 2030. Be honest with yourself. The workers who survived were those who assessed their vulnerability correctly and acted on that assessment. Those who told themselves "AI won't affect my job" were wrong. Those who minimized the risk were wrong. Those who assessed correctly and acted were right.</p>

<p><strong>2. Invest in AI Skills This Quarter</strong><br/>
Find one AI training program relevant to your field and enroll before the end of this quarter. The cost is typically equivalent to one to three months of salary at {sal}. The return is career security worth decades of income. Free resources exist too&mdash;start with those if cost is a barrier. Community centers, libraries, and online platforms in {n} offer free AI literacy courses. The investment in time matters more than the investment in money. Commit 5-10 hours per week to learning.</p>

<p><strong>3. Build an AI-Enhanced Portfolio</strong><br/>
Document every project where you use AI tools. Build a visible record of AI-augmented work. Create a simple website or LinkedIn profile that showcases how you use AI to accomplish your job better. In the 2030 job market, "AI proficiency" is demonstrated, not claimed. Employers in {n} hiring right now filter first for demonstrated AI capability. Certificates matter, but a portfolio demonstrating real application of AI tools to real problems matters more.</p>

<p><strong>4. Network with AI-Forward Colleagues</strong><br/>
Find the people in your industry who are already using AI. Learn from them. Join professional communities focused on AI in your sector. Attend meetups. Get advice on which tools matter and which are hype. The workers who thrived in {n} were connected to others on the same path. They didn't reinvent the wheel; they learned from people who had already made the transition and found what worked.</p>

<p><strong>5. Have a Backup Plan</strong><br/>
Identify two to three roles you could transition to if your current position becomes increasingly automated. Roles in {c['ai_risk_low']} are more resilient to AI disruption. Workers who had a plan B adapted faster than those who were caught off-guard. You don't need to act on plan B immediately, but knowing it exists gives you confidence and optionality when your primary role comes under pressure.</p>

<h2>THE BOTTOM LINE</h2>

<p>The single greatest predictor of career outcomes in {n} between 2025 and 2030 was not education level, not industry, not age, not starting salary. It was timing. Workers who began adapting in 2025&ndash;2026, even imperfectly, ended up dramatically better off than those who started in 2028 or later. The retraining that cost one month's salary in 2025 returned decades of higher earnings. The resistance that felt rational in 2025 proved catastrophic by 2028. You are still in the 2025&ndash;2026 window now. You still have time to be in the group that adapted early.</p>

<p>Start now. Not next year. Not next month. Now. The cost of delay is measured not in months but in career trajectories, in decades of earnings, in the difference between a career where you are always ahead of disruption versus always chasing it. The workers who started learning AI skills in 2025 are still benefiting from that choice in 2030. The workers who delayed that choice until 2028 are still paying the price.</p>"""

    # =========================================================================
    # GOVERNMENT (A+ priority, 2500-3000 words)
    # =========================================================================
    elif aud == "government":
        body = f"""{memo_header}
<h1>{n}: The AI Governance Crossroads &mdash; What Five Years of Policy Choices Revealed</h1>

<p>You are the senior official responsible for economic policy in {n}. In 2025, you presided over an economy of {pop} people, GDP per capita of {gdp_pc}, growth at {gdp_gr}, and a labor force of {lf} workers. The dominant industries&mdash;{ind1.lower()}, {ind2.lower()}, {ind3.lower()}&mdash;employed millions and generated the tax revenue that funded every public service from education to healthcare to infrastructure. You had built policies around these sectors, structured institutions around their needs, developed expertise in managing them. AI adoption was nascent but clearly accelerating. Reports on AI capabilities arrived constantly. International examples of disruption accumulated. You faced a question that would define your legacy: invest proactively in managing the AI transition, spending political capital and budget to reshape your economy in real time, or respond to crises as they emerged, managing displacement when it happened.</p>

<p>The AI era from 2025 to 2030 moved in phases. The first phase (2025&ndash;2026) was opportunity. Governments that moved early could shape the transition. They could invest in workforce retraining before massive layoffs created crisis-level demand for solutions. They could build AI ecosystems before talent fled. They could invest in digital infrastructure before digital-only services left the unconnected behind. The second phase (2027&ndash;2028) was adaptation. The disruption was visible; workforce transition programs were being built; governments were learning lessons from those ahead of them. By the third phase (2029&ndash;2030), the window had largely closed. The talent had left. The displaced workers had given up on retraining. The unconnected had been excluded from the digital economy. Governments that hadn't moved in 2025&ndash;2026 were managing crises rather than shaping futures. This memo examines both outcomes.</p>

<h2>THE BEAR CASE: Reactive Governance, Compounding Crises</h2>

<p><strong>Scenario 1: The {ind1} Employment Crisis You Didn't Prevent</strong><br/>
{n}'s {ind1.lower()} sector employed hundreds of thousands of workers earning {mfg_sal}. In 2025, you were warned that AI automation would displace a significant portion of these jobs within three to five years. Reports from other countries showed the pattern: factory automation, global competition from AI-native companies, margin compression for companies that didn't transform. You acknowledged the warning. You commissioned a study to understand {n}-specific impacts. The study took 18 months. By the time recommendations arrived in late 2026, displacement had already begun. AI-equipped competitors from abroad were undercutting {n}'s {ind1.lower()} exports. They had already completed AI deployment; {n}'s companies were still evaluating. Factories began reducing shifts. By 2027, unemployment in {ind1.lower()} regions spiked 18% above national average. Workers earning {mfg_sal} who lost jobs had no retraining options&mdash;the programs you hadn't funded didn't exist. They were retrained by market forces into service sector jobs paying 30&ndash;40% less. They flooded into adjacent sectors, compressing wages for everyone. Tax revenue from {ind1.lower()} declined as companies downsized, reducing your fiscal capacity to respond precisely when the crisis demanded the most spending.</p>

<p>By 2028, you finally launched workforce transition programs, but they came too late. The workers had already moved into lower-paying jobs. Many had lost confidence that retraining would help, having seen friends go through it only to find wages still compressed by excess supply. The political damage was significant. Regional resentment built toward the capital. By 2030, the regions most dependent on {ind1.lower()} were experiencing sustained economic distress, lower tax revenue funding the region, and populist political movements blaming the government for mismanaging the transition. The investment in transition programs in 2027&ndash;2028 cost more than a prevention program would have cost in 2025. The political damage cost more than prevention would have.</p>

<p><strong>Scenario 2: The Brain Drain You Accelerated</strong><br/>
{n} was producing {stem} STEM graduates annually&mdash;a pipeline that could have powered an AI economy. But in 2025, AI talent commanding {it_sal} found better opportunities abroad. Countries that invested in AI ecosystems earlier&mdash;research hubs, startup grants, tax incentives&mdash;attracted {n}'s best minds with higher salaries, better research facilities, better funding, and clearer career paths. You responded with rhetoric about "retaining talent" but allocated no meaningful budget for AI research hubs or competitive incentive packages. Creating a new research hub seemed like a luxury; in a resource-constrained budget, it was easy to defer. By 2027, the brain drain had become a flood. Your STEM graduates were voting with their feet, leaving for countries that had created ecosystems to support AI research. By 2028, the talent shortage was acute: companies in {n} trying to adopt AI couldn't find qualified people to lead transformations. The graduates who stayed demanded premium salaries that smaller firms couldn't afford. Your failure to create a competitive AI ecosystem in 2025 had created a talent vacuum that would take a decade to fill. By 2030, {n} had become an importer of AI talent rather than a producer. The ecosystem could have been built in 2025 for a fraction of what it cost to rebuild it in 2028&ndash;2029.</p>

<p><strong>Scenario 3: The Digital Divide That Became a Political Crisis</strong><br/>
With internet penetration at {inet}, {n} already had a significant digital divide in 2025. Urban areas had connectivity; rural areas did not. High-income households had devices; low-income households did not. You assessed the digital divide as a social issue, important but not urgent compared to other budget priorities. You assumed the private sector would close it through market forces. It wouldn't. As AI-powered services replaced traditional ones between 2025 and 2028&mdash;digital banking, telemedicine, AI-driven government services, e-commerce, digital education&mdash;the unconnected population was left behind. Rural communities, older citizens, and lower-income households couldn't access services that were increasingly digital-only. In-person bank branches closed. In-person healthcare appointments became harder to access. Government services moved online. The unconnected were systematically excluded from the digital economy. The political backlash was severe. By 2028, anti-technology sentiment was being exploited by populist movements. Your government faced protests from communities that felt abandoned by the digital transformation. Local politicians blamed you for policies that benefited the connected while leaving others behind.</p>

<p>The irony: investing in digital infrastructure in 2025 would have cost the equivalent of 0.2% of GDP. That investment would have prevented the political crisis, included 20&ndash;30 million people in the digital economy, and generated economic returns within five years. By 2028, when you finally invested in digital infrastructure, the cost had tripled because you needed to accelerate to address a crisis. The political damage was permanent. Entire communities now distrusted technology and the government that had abandoned them.</p>

<h2>THE BULL CASE: The Same Government That Acted Boldly</h2>

<p><strong>Scenario 1: The {ind1} Transition You Managed Proactively</strong><br/>
Same country, different response. In Q3 2025, you launched a national workforce transition program specifically targeting {ind1.lower()} workers, with a deadline to have it operational before mass layoffs could occur. You invested the equivalent of 0.3% of GDP in retraining centers located in {ind1.lower()}-dependent regions, keeping programs close to workers who couldn't relocate. You partnered with international AI companies to provide training curricula and certifications that had credibility globally. You offered wage subsidies to employers who retained and retrained workers rather than laying them off, aligning incentives with your goals. By 2027&mdash;when the Bear Case government was still reading its commissioned study&mdash;your program had retrained tens of thousands of workers. Many moved into AI-adjacent roles in the same {ind1.lower()} sector: operating automated systems, managing AI quality control, maintaining robotic equipment, analyzing AI-generated data for optimization. The disruption still happened, but it was managed. Workers earned more in their new roles than they had in the old ones because the AI-adjacent roles required skills that were scarce. Tax revenue from the sector stabilized, then grew as AI-enhanced companies became more productive and profitable. The political dividend was enormous: regions that had been disrupted by AI transformation were experiencing higher wages and new opportunities, not despair.</p>

<p><strong>Scenario 2: The AI Ecosystem You Built</strong><br/>
Instead of watching your STEM graduates leave, you invested in keeping them. In 2025, you created an AI research and development hub in a major city, offered competitive grants for AI research, provided tax incentives for AI startups, and funded university-industry partnerships to ensure talent could build careers in {n}. The cost was meaningful but manageable&mdash;equivalent to 0.15% of GDP annually. By 2027, the hub was attracting talent rather than losing it. By 2028, {n} had a growing AI startup ecosystem that was creating jobs, generating tax revenue, and attracting foreign investment. The STEM graduates who might have left were now building companies at home. The brain drain reversed. By 2030, {n}'s AI sector was a net contributor to GDP growth, and the ecosystem you had invested in was self-sustaining. The ecosystem also created a source of talent for companies trying to adopt AI, solving the talent shortage that afflicted the Bear Case economy.</p>

<p><strong>Scenario 3: The Digital Infrastructure You Funded</strong><br/>
You recognized that {inet} internet penetration was not just a connectivity statistic&mdash;it was a governance constraint. Every policy initiative that assumed digital access left the unconnected behind. In 2025, you launched a national digital connectivity initiative: expanding broadband to rural areas, subsidizing mobile data for low-income households, building community digital centers in underserved areas with staff trained to help people get online. The cost was upfront but finite. By 2027, connectivity had improved meaningfully. By 2028, the digital divide had narrowed significantly. AI-powered public services&mdash;healthcare, education, government benefits&mdash;reached populations that had been previously excluded. The unconnected became the connected, and their incomes, health outcomes, and opportunities improved. The political dividend was enormous: instead of anti-technology backlash, you had communities that experienced AI as an improvement in their lives. Rural areas could access telemedicine and didn't have to travel to the city. Low-income households could access better financial services. By 2030, the digital infrastructure investment was generating returns through increased economic participation, better health outcomes, more efficient government services, and deepened trust in government. The communities that had been left behind in the Bear Case were now among your government's strongest supporters.</p>

<h2>THE STRATEGIC CHOICE: Proactive vs. Reactive</h2>

<p>The difference between these two outcomes came down to the choices made in 2025. Not in 2030, when the patterns were obvious. Not in 2027, when the data was unambiguous. In 2025, when it felt uncertain. The governments that acted in 2025&mdash;when the disruption seemed hypothetical, when the cost felt large, when the political pressure was low&mdash;created conditions that allowed their economies to adapt. They used the window of opportunity that exists before disruption becomes crisis. The governments that waited until disruption was severe found themselves unable to respond adequately because resources were already strained.</p>

<h2>WHAT YOU SHOULD DO NOW</h2>

<p><strong>1. Launch Sector-Specific Workforce Transition Programs This Quarter</strong><br/>
Target the highest-risk sectors first: {risk1.lower()}, {risk2.lower()}, {risk3.lower()}. Fund retraining centers in the communities most dependent on these industries, not in the capital where workers can't easily access them. Budget for 3&ndash;5 years of programs, not just the first pilot. Don't commission another study&mdash;the data is clear. Every successful transition program from other countries shows the pattern. The cost of acting now is a fraction of the cost of managing displacement and regional resentment later. This is not charity; it is economic policy.</p>

<p><strong>2. Create an AI Talent Retention Strategy Within 90 Days</strong><br/>
Design research hubs, competitive grants, startup incentives, university partnerships, and tax breaks for AI founders. {n}'s STEM graduates producing {stem} annually are a critical asset. Every month without a retention strategy is a month of talent leaving for countries that have one. Fast-track visa processing for AI talent, not just tech workers. Create regional AI hubs, not just one central hub. Make it possible for an AI researcher to build a company in {n} and compete globally. By 2030, every major economy will have an AI ecosystem. Your question is whether {n} builds one with {n}'s talent or watches the talent leave.</p>

<p><strong>3. Invest in Digital Infrastructure as Urgently as Physical Infrastructure</strong><br/>
Expanding connectivity from {inet} is not a luxury&mdash;it is a prerequisite for every other AI governance initiative. Fund broadband expansion to rural areas, mobile data subsidies for low-income households, and community digital centers staffed with people trained to help the unconnected get online. The return on investment in economic participation alone will justify the cost. More importantly, it prevents the political backlash that emerges when technologies benefit some while excluding others. Budget this as an ongoing expense, not a one-time project. Digital infrastructure will require maintenance and upgrades as technology evolves.</p>

<p><strong>4. Establish a National AI Governance Framework</strong><br/>
Set clear rules for AI deployment: data privacy, algorithmic accountability, worker protections, safety requirements. Countries that established frameworks early attracted more investment, not less. Clarity reduces risk for businesses and citizens alike. Without frameworks, businesses are cautious. Without governance, the benefits accrue to large corporations while smaller companies struggle with compliance costs. Publish your framework publicly. Let companies and workers see what the rules are. Transparency builds trust. Ambiguity breeds speculation and backlash.</p>

<p><strong>5. Build Cross-Ministry AI Coordination</strong><br/>
AI disruption cuts across every ministry&mdash;labor, education, health, finance, trade, rural development. Create a cross-ministry coordination body with real authority and budget, not just a committee that discusses issues. Siloed responses to a cross-cutting challenge produce gaps that compound. The ministry of labor reskills workers; the ministry of education updates curricula; the ministry of health deploys telemedicine. But if these three don't coordinate, a worker retrains for a role that schools aren't teaching and no healthcare provider is hiring for. Coordination prevents this waste.</p>

<p><strong>6. Measure and Report Publicly on AI Transition Progress</strong><br/>
Quarterly public reporting on workforce transition metrics, digital connectivity, AI adoption, talent retention, and regional outcomes. Transparency creates accountability and builds public trust in the transition. Citizens who feel informed about the plan are more supportive than those who feel left behind. Show successes. Acknowledge failures and how you're addressing them. Publish data region by region so local politicians can see whether their communities are adapting or falling behind. Use data to drive policy adjustments rather than defending initial decisions.</p>

<h2>THE BOTTOM LINE</h2>

<p>From 2030, the lesson for {n}'s policymakers is stark and unambiguous. The cost of proactive AI governance was manageable in 2025&mdash;equivalent to 0.3&ndash;0.5% of GDP for workforce transition, digital infrastructure, and AI ecosystem development. That was a meaningful investment but not disruptive to annual budgets. The cost of reactive crisis management was devastating by 2028&mdash;political instability, regional resentment, talent flight, economic stagnation. The governments that invested in 2025&ndash;2026 saw every dollar returned multiple times over in economic growth, social stability, and global competitiveness. Those that waited until 2028 are still paying the price.</p>

<p>{challenge_short} made the stakes of the AI transition higher, not lower. Economies struggling with structural challenges had even less margin for error. The governments that understood this early and acted decisively are now leading the AI era with stronger economies and more stable societies. Those that didn't are still managing its consequences. The window remains open&mdash;but it is narrowing. The time to make these investments is now, in 2030. By 2032, the window will largely have closed. By then, the disruption will be visible. The damage will be measurable. And the cost of response will be triple what it costs today.</p>"""

    # =========================================================================
    # INVESTOR (A-priority, 2500-3000 words)
    # =========================================================================
    elif aud == "investor":
        body = f"""{memo_header}
<h1>{n}: AI Investment Thesis &mdash; Where Value Was Created and Destroyed Between 2025 and 2030</h1>

<p>You manage a portfolio with significant exposure to {n}. In 2025, the investment landscape was defined by GDP per capita of {gdp_pc} (PPP: {gdp_ppp}), growth at {gdp_gr}, and a labor force of {lf} workers concentrated in {ind1.lower()}, {ind2.lower()}, and {ind3.lower()}. The average worker earned {sal}, which shaped the competitive advantage of {n}-based companies in global markets. The question for investors was straightforward but high-stakes: was {n} positioned to ride the AI wave, using its cost advantages and growing workforce to leap to AI-enabled operations, or would structural challenges ({challenge_short}) combine with technological disruption to destroy value across entire sectors? The five years between 2025 and 2030 answered that question definitively, but the answer varied dramatically based on which specific companies and sectors you had exposure to. This memo examines both outcomes from our 2030 vantage point and provides a framework for analyzing {n} opportunities going forward.</p>

<h2>THE BEAR CASE: Value Destruction in Legacy Positions</h2>

<p><strong>Scenario 1: The {ind1} Exposure That Cratered</strong><br/>
Investors who held concentrated positions in {n}'s {ind1.lower()} sector without an AI transformation catalyst suffered significant losses. These companies had been profitable for decades, had clean balance sheets, had workers earning {mfg_sal} providing a competitive labor cost advantage versus developed markets, and had maintained market share through operational excellence. They looked like solid, if unglamorous, investments. But when AI-equipped competitors from developed markets entered the {n} market between 2026 and 2028, that labor cost advantage evaporated. AI-driven automation made the cost of a worker less relevant than the cost of computation. A factory with 500 workers earning {mfg_sal} each faced competition from a factory with 150 workers and AI systems managing the rest. The labor cost advantage that used to be 40% became irrelevant. Companies that hadn't invested in AI saw revenue decline 25&ndash;40% as clients migrated to AI-enabled alternatives that were faster and cheaper. Stock prices reflected the structural shift, not just cyclical weakness. Investors who treated {ind1.lower()} stocks as "value plays" at low multiples of earnings discovered they were value traps. The earnings weren't sustainable. By 2030, many of these companies had been acquired at fire-sale valuations by the AI-equipped competitors.</p>

<p><strong>Scenario 2: The Infrastructure Gap That Constrained Digital Economy Growth</strong><br/>
{n}'s internet penetration of {inet} was a fundamental constraint on digital economy growth in 2025. Investors who bet on rapid digital adoption without accounting for infrastructure limitations saw slower-than-expected returns from e-commerce, fintech, and digital services investments. A company couldn't build an internet-only banking service in {n} when {inet} meant 30&ndash;40% of the population lacked reliable connectivity. The companies that succeeded in digital transformation were those that built their own infrastructure (mobile-first, offline-capable systems) rather than assuming existing connectivity would suffice. Investors who didn't differentiate between "digital company" and "company equipped for {n}'s actual infrastructure reality" lost capital on the distinction. The fintech company that depended on broadband connectivity struggled. The mobile-first platform that worked on 2G networks thrived.</p>

<p><strong>Scenario 3: The Currency and Sovereign Risk That Amplified with AI Disruption</strong><br/>
{n}'s structural challenges&mdash;{challenge_short}&mdash;didn't improve with AI disruption; they initially worsened. As AI displaced workers in high-risk sectors ({risk1.lower()}, {risk2.lower()}, {risk3.lower()}), tax revenue from those sectors declined while social spending needs increased. The government faced political pressure to support displaced workers while facing declining revenue. The fiscal pressure, combined with capital outflows from legacy sectors to AI-driven sectors or overseas, put pressure on the {cur}. The currency weakened 15&ndash;25% against major currencies between 2027 and 2030. Investors with unhedged {cur} exposure saw real returns erode even when local-currency positions performed adequately. A company that was earning 20% returns in {cur} was earning only 8&ndash;10% in hard currency when you factored in currency depreciation. The lesson: AI disruption was not just a sector story but a macro story, and investors who ignored sovereign context paid for the oversight. In emerging markets, macro matters as much as micro.</p>

<h2>THE BULL CASE: Asymmetric Returns from AI Transformation</h2>

<p><strong>Scenario 1: The {ind1} Companies That Transformed Early</strong><br/>
The best returns in {n} came from established {ind1.lower()} companies that adopted AI early and credibly. These weren't speculative bets on AI startups&mdash;they were established businesses with real revenue, real customers, and real margins being transformed by technology. Investors who identified companies in {ind1.lower()} with management teams genuinely committed to AI transformation (not just announcing it), adequate balance sheets to fund it, and clear implementation roadmaps captured extraordinary returns. These companies moved decisively in 2025&ndash;2026, allocating 5&ndash;10% of annual revenue to AI transformation. By 2028, they had deployment in place. By 2030, they had competitive advantage that competitors couldn't replicate. They gained market share as competitors faltered, and their margins expanded as AI reduced costs and improved quality. A {ind1.lower()} company that went from 12% margins to 18&ndash;20% margins generated returns that justified high multiples. Investors who bought these companies at reasonable valuations (8&ndash;10x EBITDA) saw them expand to 15&ndash;18x within five years as the market recognized the AI-driven transformation. The sweet spot was companies that were large enough to have real revenue but small enough to be still private or public but undervalued.</p>

<p><strong>Scenario 2: The AI Infrastructure Plays That Captured 2% Incremental Growth</strong><br/>
Every AI transformation in {n} required infrastructure: connectivity, data centers, cloud services, cybersecurity. With {inet} internet penetration and growing demand for digital services driven by AI adoption, infrastructure providers captured predictable, growing revenue streams. These were the "picks and shovels" of {n}'s AI rush. An internet service provider that expanded broadband to rural areas captured both government contracts (connectivity programs) and growing commercial demand (AI companies needing infrastructure). A data center operator captured explosive demand as every {n}-based company scaling AI workloads needed compute capacity. Investors who positioned early in digital infrastructure captured strong returns (12&ndash;18% annually) with lower volatility than pure AI application plays (which swung from -40% to +80% based on execution). The thesis was simple: regardless of which AI applications won or lost, they all needed infrastructure. Infrastructure was a 2% annual growth boost to {n}'s economy, and infrastructure companies captured a disproportionate share of it.</p>

<p><strong>Scenario 3: The Talent Economy Bet That Exploded with Demand</strong><br/>
{n} produced {stem} STEM graduates annually. Investors who backed companies building AI training, reskilling, and education platforms captured the human capital side of the transition. With {lf} workers needing to adapt and employers willing to pay premium rates for workforce transformation, the addressable market was enormous and growing. A platform offering AI training to {n}'s workforce had a market of tens of millions of potential students. Companies that built scalable AI training platforms generated strong recurring revenue with improving unit economics as their training content scaled across industries. By 2030, the most successful platforms were generating 40&ndash;50% gross margins and growing 60&ndash;80% annually. They captured value not just from individual learners but from enterprises paying for bulk training for their workforces. Investors who backed these platforms early captured 10&ndash;15x returns as the market recognized the size of the opportunity.</p>

<h2>THE INVESTMENT FRAMEWORK: How to Evaluate {n} Opportunities in the AI Era</h2>

<p>By 2030, the three-factor framework for evaluating investment in {n} was clear: AI readiness of the core business, infrastructure alignment, and macro stability. Companies that were strong on all three factors outperformed dramatically. Companies that were weak on even one factor generally underperformed. Legacy companies that were strong on macro and had adequate margins but lacked AI readiness were value traps. AI-native startups that had strong technology but lacked either infrastructure or macro stability couldn't scale. The winners combined AI readiness with either infrastructure strength (if infrastructure-dependent) or macro stability (if exposed to sovereign risk).</p>

<h2>WHAT YOU SHOULD DO NOW</h2>

<p><strong>1. Audit Every Position Through an AI Readiness Lens</strong><br/>
For every holding in {n}, ask: does this company have a credible, funded, explicitly articulated AI transformation plan? If not, it is a potential value trap regardless of current earnings or valuation multiples. Don't accept management assertions without evidence. Look for: actual budget allocation (5&ndash;10% of revenue), publicly stated timelines, named executives leading transformation, and milestone results. Companies without these elements are not committed. Treat them as sunset assets.</p>

<p><strong>2. Overweight AI-Transforming Incumbents Over Startups</strong><br/>
The best risk-adjusted returns came from established companies that adopted AI early&mdash;not from speculative AI startups. Startups have upside but lack the revenue base and customer relationships that incumbents have. Look for management commitment (CEO spending 25%+ of time on AI transformation), adequate funding (5&ndash;10% of annual revenue allocated), and clear milestones (18-month deployment target) in {ind1.lower()}, {ind2.lower()}, and {ind3.lower()}. Prioritize companies that are transforming to maintain position, not startups trying to create position from scratch.</p>

<p><strong>3. Build Infrastructure Exposure Deliberately</strong><br/>
Digital infrastructure in {n} is the foundation of every AI thesis. Connectivity, data centers, cloud services, and cybersecurity offer predictable returns with significant growth potential from {inet} penetration levels. Infrastructure investments are less glamorous than application companies but more stable. A portfolio should be 30&ndash;40% infrastructure if you're building exposure to {n}'s AI economy. Infrastructure compounds. It's also capital intensive, so management quality matters a lot.</p>

<p><strong>4. Hedge Currency and Sovereign Risk Explicitly</strong><br/>
AI disruption amplifies macro risks in {n}. AI transformation increases tax revenue (from higher productivity) in some scenarios and decreases it (from displacement) in others. Ensure your portfolio accounts for {cur} exposure and accounts for downside scenarios. Hedge 50% of {cur} exposure minimum. The cost of hedging (1&ndash;2% annually) is insurance against structural risks that could unfold faster than you expect.</p>

<p><strong>5. Monitor the Talent Pipeline as a Leading Indicator</strong><br/>
{n}'s capacity to produce and retain AI talent is a leading indicator of which AI investments will succeed. Companies and sectors that attract talent will outperform those that don't. Follow hiring announcements of AI-focused companies. Track which firms are building teams in {n} versus outsourcing. Factor talent metrics into your investment analysis. If {n} is losing AI talent to other countries, AI transformation will be slower than in countries retaining talent.</p>

<p><strong>6. Set Clear Exit Criteria for Legacy Positions</strong><br/>
Define measurable AI transformation milestones for every holding. If a company hasn't achieved specific milestones (20% of revenue from AI-enabled products, 30% cost reduction, 2-year track record) within 18&ndash;24 months, exit regardless of valuation or earnings. The pattern from 2025&ndash;2030 is clear: companies that didn't transform early rarely recovered. They became acquisition targets at depressed valuations. Don't wait for a recovery that won't come. Exit and redeploy capital to winners.</p>

<h2>THE BOTTOM LINE</h2>

<p>For investors in {n}, the 2025&ndash;2030 period revealed a consistent pattern: AI was not an incremental efficiency tool but a structural reshaping of competitive advantage and economic value creation. The investors who outperformed were those who evaluated every position through an AI readiness lens&mdash;not past earnings, not current margins, not historical dividend history, but the speed and credibility of AI transformation. In {n}, that lens separated extraordinary returns (100%+ over five years) from devastating losses (-50% to -80%). The same lens applies going forward. The companies that transform in 2030&ndash;2032 will be the winners of the next five years. The companies that are still debating transformation will be tomorrow's value traps.</p>"""

    # =========================================================================
    # YOUNG PERSON (B-priority, 1500-2000 words)
    # =========================================================================
    elif aud == "young-person":
        body = f"""{memo_header}
<h1>{n}: Two Futures for Young People &mdash; What Happened to Those Who Prepared vs. Those Who Didn't</h1>

<p>You are between 18 and 25 years old, living in {n}, at the moment in life when you're making decisions about education, career, and your future. In 2025, you were entering or preparing to enter a labor force of {lf}, where the average worker earned {sal} and tech roles commanded {it_sal}. The economy was growing at {gdp_gr}, with GDP per capita of {gdp_pc}. Your parents told you stories about building careers in sectors like {ind1.lower()} and {ind2.lower()} that had provided stable employment for their generation. Your teachers encouraged traditional paths: university, degree, job. Your counselors were divided on what AI meant for your future, with some dismissing it as hype and others warning about massive disruption. By June 2030, the answer is clear, and it's unambiguous: what you did between 2025 and 2026 determined which path your career took. The divide between those who thrived and those who struggled wasn't talent or intelligence; it was the choice to learn new skills before those skills became necessary.</p>

<h2>THE BEAR CASE: Trained for Jobs That Vanished or Transformed</h2>

<p><strong>Scenario 1: The {ind1} Graduate Who Followed the Traditional Path</strong><br/>
You chose a traditional career path in {ind1.lower()}&mdash;a sector that had employed your parents' generation and seemed like the safe, sensible choice. You studied hard, graduated in 2027 with strong grades and relevant coursework, and entered the job market with confidence. But on graduation day, the job market had transformed so fundamentally that entry-level roles looked nothing like what you trained for. Employers wanted AI-augmented skills&mdash;the ability to work with AI systems, interpret their outputs, make decisions based on AI-generated insights. You had domain knowledge but not AI knowledge. You competed against peers who had added AI competencies to their {ind1.lower()} expertise during their studies. Those peers had built portfolios of AI projects. They had internship experience with AI tools. They interviewed at companies and talked about their AI capabilities. They were hired. You were not. You received offer rejections with feedback: "strong fundamentals, but lacks AI experience." By 2030, you were underemployed in a role paying 40% less than {sal}, watching your AI-skilled peers advance into management positions you were never going to reach.</p>

<p><strong>Scenario 2: The Graduate Who Waited for University to Catch Up</strong><br/>
You assumed your university would update its curriculum to include AI because the need was obvious. It didn't&mdash;or it did far too slowly. In your entire four-year program, you took one elective on AI, offered in your final year, that barely scratched the surface. You graduated with knowledge that was current in 2022 but was becoming obsolete in 2026 and had aged considerably by 2028. The gap between what employers needed and what your education provided was vast. By the time you discovered this gap, you were already graduated and entering the job market. You spent 2028&ndash;2029 in emergency retraining programs, trying to catch up, losing two critical years of career progress and early earnings potential. Peers who had started learning AI in 2025 had a three-year head start you could never close.</p>

<p><strong>Scenario 3: The Young Person Limited by Infrastructure Access</strong><br/>
With internet penetration at {inet} in {n}, not everyone had equal access to online learning. If you lived in a rural area or came from a low-income household without reliable internet, you couldn't access the free AI learning platforms that your urban, well-connected peers used. You couldn't take online courses at your own pace. You couldn't build an online portfolio. You couldn't participate in online communities where young people were learning and networking. Your older peers had library access or could afford internet themselves. You were limited to what your school could provide. The digital divide became a career divide. By 2030, young people with early digital access and self-directed AI learning were earning multiples of those without. The limitation wasn't intelligence or motivation; it was access.</p>

<h2>THE BULL CASE: The AI-Native Generation That Prepared</h2>

<p><strong>Scenario 1: The Young Person Who Combined Domain Knowledge with AI</strong><br/>
Same starting point, different approach. You studied {ind1.lower()} because you genuinely cared about the field, but you also invested your own time in building AI skills. While your coursework covered {ind1.lower()} fundamentals, you spent weekends taking online AI courses, building small projects that applied AI to {ind1.lower()} problems, and participating in online communities. By graduation, you had not just a degree but a portfolio of AI-enhanced projects that demonstrated practical capability. An interviewer could see: you understand {ind1.lower()}, you understand AI, and you can apply AI to {ind1.lower()} problems. Employers competed to hire you. By 2028, you were earning well above {sal}, managing AI systems in {ind1.lower()} operations, leading teams that older workers in the sector couldn't lead because they didn't understand the technology. By 2030, you had real career options. Multiple companies wanted you. You could negotiate for positions, compensation, and growth. Your domain knowledge plus AI skills made you exactly what the market needed.</p>

<p><strong>Scenario 2: The Self-Taught AI Practitioner</strong><br/>
You didn't wait for university to provide AI training. In 2025, in your late teens, you started learning AI tools through free online resources: courses on Coursera, YouTube tutorials, documentation from open-source projects. You built small projects for yourself and others. You contributed to open-source AI communities. You created a public portfolio on GitHub showcasing your work. It took discipline and time, but you invested both. By 2027, before many of your peers had even graduated, you were freelancing AI work, taking contracts for small projects, building a reputation. By 2030, you had five years of practical AI experience and a track record that traditional education alone couldn't provide. Your income had grown from zero (starting as a teenager) to significantly exceeding the tech salary range of {it_sal} because demand for proven AI practitioners far outstripped supply in {n}. You were competing for senior roles while peers your age were still junior. You had leveraged time advantage (starting young) into a career advantage (early experience).</p>

<p><strong>Scenario 3: The Young Person Who Chose AI-Enhanced Careers Strategically</strong><br/>
You looked at the disruption data and made a strategic career choice. Instead of entering high-risk sectors ({risk1.lower()}, {risk2.lower()}, {risk3.lower()}) where AI would be automating core work, you chose a field in {c['ai_risk_low']}&mdash;work that remained fundamentally human but was enhanced by AI. You studied teaching, healthcare, counseling, creative fields, skilled trades&mdash;areas where AI could augment your capabilities but not replace them. You built AI literacy alongside your core expertise. You learned how AI could help you do your job better: AI-powered diagnostic tools if you were in healthcare, AI-augmented research tools if you were in any knowledge field, AI for scaling your impact. By 2030, you had a stable, growing career in a sector where AI made you more productive rather than redundant. Your combination of human skills and AI fluency was the most valued profile in {n}'s labor market because it combined the resilience of human-centric work with the productivity of AI-augmented work.</p>

<h2>THE INFLECTION: Why 2025-2026 Mattered for Your Entire Career</h2>

<p>The young people who were 20 in 2025 and made the decision to learn AI made that decision at exactly the right time. AI was still emerging; demand wasn't yet overwhelming supply. Online resources were free or cheap. Employers weren't yet demanding AI experience as a prerequisite. Learning was possible without formal credentials. By 2028, all of that had changed. AI skills were expensive to acquire (high-demand training programs charged accordingly). Employers expected years of experience. The young people who waited until 2028 to start learning were starting from behind peers who had started in 2025. That three-year gap proved nearly impossible to close.</p>

<h2>WHAT YOU SHOULD DO NOW</h2>

<p><strong>1. Start Learning AI Tools This Month, Not Next Year</strong><br/>
Not next semester when you have more time. Not next year when you've thought about it more. This month. Right now. Free resources exist: YouTube, Coursera's free tier, Udemy courses (often on sale for $10), documentation from open-source projects. Start with applications relevant to your interests or field. Don't try to become a machine learning engineer if that doesn't interest you. Do try to learn tools that enhance what you're already interested in. The young people who thrived in {n} started with small, consistent steps&mdash;one course, one project, one community&mdash;not grand plans that never materialized.</p>

<p><strong>2. Build a Public Portfolio of AI Projects</strong><br/>
Document everything you build. Create a GitHub account and upload your projects. Write about what you learned. Start a blog or share projects on social media. Employers in 2030's {n} hire based on demonstrated capability, not credentials alone. A portfolio of real projects, however small, is worth more than a degree without portfolio work. This is how young people without years of experience prove competence: by showing work. Make your portfolio public so prospective employers and collaborators can see what you can do.</p>

<p><strong>3. Choose Your Field or Specialization Strategically</strong><br/>
Research which sectors in {n} are high-risk for AI disruption ({risk1.lower()}, {risk2.lower()}) versus resilient to it ({c['ai_risk_low']}). Make your career choices with eyes open. There is nothing inherently wrong with entering a disrupted sector&mdash;but only if you bring AI skills to it. If you want to work in {ind1.lower()}, that's fine, but plan to add AI skills. If you want resilience without needing AI skills, choose fields where human judgment, creativity, and relationships are central.</p>

<p><strong>4. Don't Wait for Formal Education to Catch Up</strong><br/>
Most universities are updating curricula to include AI, but it's slow. Your degree won't make you an AI expert. Your degree might not even make you AI-literate. That's okay, but don't expect it. Supplement your formal education with self-directed AI learning. Take online courses in parallel with your degree program. The young people who relied solely on their university curriculum fell behind. Those who took ownership of their own skill development thrived. Your university is teaching what was current when the curriculum was designed. Your own learning can be current right now.</p>

<p><strong>5. Connect with Others on the Same Path</strong><br/>
Join AI communities online: Discord servers for AI learning, Reddit communities, local AI meetups in your city, university AI clubs. Find mentors who are already working in AI-enhanced roles. Ask them what skills matter, what projects build portfolio value, what learning path they followed. The network you build now will accelerate your career for decades. The friends you meet through AI communities might become your future colleagues or collaborators. Start building that network now.</p>

<h2>THE BOTTOM LINE</h2>

<p>You have an advantage that older workers do not: time. A 20-year-old in 2030 will have a 40-year career ahead. The AI skills you build now will compound over four decades. Even small investments in learning&mdash;one hour per week&mdash;accumulate into thousands of hours of capability over a career. In {n}'s economy&mdash;with its specific challenges and opportunities&mdash;the young people who thrive will be those who combined their genuine interests with AI fluency. You don't need to become a technologist. You need to become literate in AI and fluent with tools. Start now. Start small. But start. Your 30-year-old self will thank your 20-year-old self for making that investment.</p>"""

    # =========================================================================
    # CONSUMER (C-priority, 1200-1500 words)
    # =========================================================================
    elif aud == "consumer":
        body = f"""{memo_header}
<h1>{n}: How AI Transformed Daily Life &mdash; Two Household Stories</h1>

<p>You and your family live in {n}, where the average household earns {sal}, spending your income on the basics and occasional luxuries. In 2025, GDP per capita was {gdp_pc}, the economy was growing at {gdp_gr}, and AI felt like someone else's concern&mdash;a corporate buzzword in news articles, not something that would affect your daily life, your grocery bill, your healthcare, or your financial security. By 2030, that perception had been proven wrong. AI reshaped the services your family depends on every day: banking, healthcare, shopping, and government services. The services themselves didn't disappear, but how you accessed them changed fundamentally. This memo tells the story of two households in {n}&mdash;one that adapted to the AI-powered economy and benefited from it, and one that didn't adapt and paid the price.</p>

<p>Between 2025 and 2030, {n} experienced what economists call the "digital inflection point"&mdash;the moment when digital access became inseparable from economic participation. This transformation happened in three distinct phases. In 2025&ndash;2026, AI tools were emerging but still optional. Families could ignore digital tools and life continued much as before. By 2027&ndash;2028, the second phase, digital became default. Banks closed physical branches, healthcare moved to telemedicine, shopping went online. By 2029&ndash;2030, the third phase, digital became necessary. You couldn't access many services without smartphone competency. The families who adapted during phase one had five years to learn. The families who waited until phase three had no time, and many never caught up.</p>

<h2>THE BEAR CASE: The Family That Remained Offline</h2>

<p><strong>Scenario 1: Banking Became Digital and Excluded You</strong><br/>
Your bank branch closed in 2027 as part of industry consolidation and digital transformation. Services moved online. You had used the branch for everything&mdash;deposits, transfers, loan inquiries, advice. You spoke to the same teller for years and built a relationship based on trust. The new app-based system was confusing and impersonal. You struggled with digital verification steps (security codes sent to your phone, facial recognition, complex passwords), interfaces designed for people comfortable with technology, and the general anxiety of moving your money to systems you didn't fully understand. In a country with {inet} internet penetration, you weren't alone in feeling excluded. Millions of households faced the same anxiety. Without digital banking skills, you relied on informal money management&mdash;cash under the mattress (insecure and vulnerable to theft or loss), expensive money transfer services (taking 5&ndash;10% commission on every transaction), informal savings groups (unreliable and uninsured). Your savings earned no interest. The money in your mattress lost value to inflation every year.</p>

<p>Your financial security eroded steadily between 2027 and 2030 while digitally connected households accessed better interest rates, easier credit through digital platforms, and automated budgeting tools that helped them spend less and save more. A household that moved to digital banking earned 3&ndash;5% annually on savings. You earned 0%. Over five years, that compounded into a meaningful difference. But the damage went beyond missed interest. Cash management became impossible at scale. You couldn't track your spending. You couldn't compare pricing across financial products. When your family had an emergency, you had no quick access to credit because digital platforms, using AI-powered credit scoring, couldn't assess your creditworthiness from cash-only history. You had to turn to informal lenders charging 15&ndash;20% interest, making the emergency exponentially more expensive. The households that adapted gained financial advantage and financial resilience; those that didn't fell steadily behind and became vulnerable to any crisis.</p>

<p><strong>Scenario 2: Healthcare Went Digital and Left You Behind</strong><br/>
AI-powered telemedicine and diagnostic tools transformed healthcare in {n} between 2026 and 2029. Early adopters got faster diagnoses, reduced wait times, and lower costs. But you didn't use telemedicine&mdash;you preferred in-person visits with doctors who knew you. As hospitals shifted resources to their digital channels to serve more patients, in-person care became slower, more expensive, and harder to access. Appointment wait times grew from weeks to months. A health concern that could have been caught early via an AI screening tool available online was diagnosed months later, at a more advanced stage, requiring more expensive treatment. The cost difference&mdash;financial and personal&mdash;was significant. Early detection through digital screening would have meant simple treatment. Late detection through in-person avoidance meant complex treatment.</p>

<p>The cascading health consequences extended beyond the initial diagnosis. Because you avoided digital healthcare, you didn't get preventive monitoring. A chronic condition that should have been managed with simple medication management spiraled into a serious complication requiring hospitalization. Hospital costs in {n} are typically covered partially by insurance and government subsidy, but the out-of-pocket portion was substantial at a household income of {sal}. More significantly, the hospitalization meant you missed work. At an average wage of {sal}, missing a month of income created a financial crisis that compounded the medical emergency. Families with digital healthcare had continuous monitoring and early intervention that prevented these cascading failures. Your family experienced one health event that triggered financial emergency, lost income, and accumulated medical debt that took years to recover from.</p>

<p><strong>Scenario 3: Prices Diverged and You Paid Full Price</strong><br/>
AI-powered price comparison, dynamic discounts, and optimized purchasing saved digitally connected households significant money on groceries, utilities, and services. Apps compared prices across stores and automatically purchased at the cheapest option. Household budgeting apps used AI to optimize spending. You didn't use these tools. You shopped at the nearest store, paid the listed price, didn't know where better deals existed. Over five years, the cumulative difference was substantial&mdash;the equivalent of several months of household income at {sal}.</p>

<p>This price divergence was not random. Retailers in {n} increasingly used AI to segment customers by price sensitivity. Customers who shopped via app with transparent pricing were given better deals to keep them engaged. Customers who shopped in-store without comparison tools were charged more because retailers knew those customers couldn't easily compare. If you bought groceries at the neighborhood store without checking prices online, you paid 15&ndash;25% more than customers with app-based shopping in the same city. For a family spending {sal} monthly on food and utilities, this pricing divergence was the difference between having savings and living paycheck to paycheck. By 2030, the gap between digitally-enabled households and offline households had created two distinct economies: one where basic services were affordable, and one where they were chronically expensive.</p>

<h2>THE BULL CASE: The Same Family That Embraced Digital Tools</h2>

<p><strong>Scenario 1: Digital Banking Saved You Real Money</strong><br/>
When your branch announced it was closing, you took action. You attended a digital literacy workshop at a community center, learning how to use mobile banking, verify your identity, navigate apps, protect yourself from fraud. Within a month, you were using mobile banking confidently. You discovered higher-interest savings accounts that digital banks offered, automated budgeting tools that helped you spend less, and cheaper transfer services. Over five years, the financial benefit was meaningful&mdash;equivalent to weeks of household income saved annually through better rates and lower fees. Your savings were secure, earning returns, and your financial security improved.</p>

<p>But the benefits compounded beyond simple interest savings. Because you had a digital banking history, AI-powered credit scoring systems could assess your creditworthiness. When your family faced an emergency&mdash;a child's sudden illness, a home repair&mdash;you could access credit quickly at 5&ndash;8% interest instead of the 15&ndash;20% that informal lenders charged. That difference meant your emergency didn't become a crisis spiral. You borrowed, you repaid, your family recovered without devastating financial consequences. You also had access to AI-powered budgeting tools that analyzed your spending patterns and identified opportunities to reduce expenses&mdash;switching to cheaper internet providers, consolidating subscriptions, optimizing utility usage. Every small saving added up. By 2030, your household at a base income of {sal} had more financial agency, more security, and more resilience than it had in 2025.</p>

<p><strong>Scenario 2: Telemedicine Improved Your Family's Health Outcomes</strong><br/>
You started using an AI-powered health platform in 2026, initially skeptical but willing to try. A routine screening flagged a health issue early&mdash;something that would have gone undetected for months through traditional in-person channels because you wouldn't have accessed healthcare until the problem became severe. Early treatment was simpler, less costly, and more effective. Your family accessed healthcare more frequently and more conveniently because you could consult from home rather than travel. Your family's health outcomes improved measurably. You felt relief knowing that health problems were being caught early and treated simply.</p>

<p>The compounding health benefits were significant. Because you had regular digital health engagement, AI systems learned your baseline health patterns. When something changed&mdash;a slightly elevated vital sign, a pattern shift in symptoms&mdash;the system flagged it early, before you would have noticed. Your doctor (or an AI-assisted clinician) could intervene before small problems became big ones. For a family at household income of {sal}, avoiding one serious hospitalization saves months of income. Between 2025 and 2030, the families with continuous digital health monitoring avoided an average of 1&ndash;2 major hospital events that offline families experienced. That difference alone justified every hour spent learning to use telemedicine. Additionally, because digital healthcare was more accessible and cheaper, you could treat minor issues before they became serious, and you could pursue preventive care that improved long-term quality of life for your entire family.</p>

<p><strong>Scenario 3: AI Shopping Tools Stretched Your Tight Budget</strong><br/>
You installed an AI-powered price comparison app on your phone and automated your household purchasing decisions where possible. Within six months, you were saving a meaningful percentage on groceries and utilities without changing what you bought, what you ate, or what services you used&mdash;only where and when you bought them. An app found you the best price automatically. You saved money on every purchase without extra effort. Over five years, the cumulative savings were substantial. At a household income of {sal}, every saving mattered. The extra money went to your children's education or emergency savings.</p>

<p>The savings compounded across categories. On groceries, AI apps saved 15&ndash;20% by finding the best prices and alerting you to deals matching your family's diet. On utilities, AI negotiation bots managed your service contracts, switching to cheaper providers when rates changed, saving 10&ndash;15%. On insurance, AI comparison tools found plans that matched your family's needs without overpaying. Across all categories, a family spending {sal} monthly could redirect the equivalent of one month's full income per year to savings or investment. Over five years, that was five months of income redirected&mdash;enough to establish emergency savings, pay for children's education, or invest in skills that improved earning potential. The digitally-enabled household didn't just save money; the savings enabled financial stability that transformed other life outcomes.</p>

<h2>THE TRANSITION: Why Digital Adaptation Was Possible</h2>

<p>The critical insight is this: by 2030, the technology was not the barrier. Digital literacy programs were widely available and often free. Smartphones were affordable. Data costs had declined steadily as competition increased. The barriers were psychological&mdash;fear of the unfamiliar, loss of established relationships, distrust of technology&mdash;and those barriers were surmountable for families willing to invest a few hours learning. The families that thrived were not those with advanced technical knowledge. They were families that made a deliberate choice to try, to ask for help, to practice, and to persist. That choice, made in 2025 or 2026, created a five-year advantage that became permanent by 2030.</p>

<h2>WHAT YOU SHOULD DO NOW</h2>

<p><strong>1. Learn Basic Digital Tools This Week</strong><br/>
Mobile banking, price comparison apps, telemedicine platforms. These are not luxuries or frivolous technology in {n}'s 2030 economy&mdash;they are essential household tools that affect your finances and health. Community digital centers, library programs, school programs, and family members can help you get started. Ask for help. Most people are willing to help if you ask. Set a realistic goal: by the end of this week, download one app and use it once, successfully. That's enough. The repetition will follow.</p>

<p><strong>2. Switch to Digital Banking Services Deliberately</strong><br/>
Compare your current banking costs and rates to digital alternatives available in {n}. Calculate what you pay in fees and what interest you earn. Compare that to digital banks' offerings. The switch typically saves the equivalent of weeks of income annually and provides access to better financial tools. It feels risky; it's actually safer if you choose reputable digital banks with security. Start with one account. Keep your old account open until you're confident. Then transfer fully.</p>

<p><strong>3. Register for Telemedicine and Use It Regularly</strong><br/>
Access preventive healthcare through AI-powered platforms available in {n}. Early detection saves money and improves health. Most platforms work on basic smartphones with modest data requirements (not high-speed internet). Use telemedicine for routine concerns before they become serious. Set a calendar reminder to check your health platform monthly, even when you feel fine. That regular engagement trains both you and the AI system to keep you healthy.</p>

<p><strong>4. Install a Price Comparison Tool and Give It a Chance</strong><br/>
Download one price comparison or budgeting app and use it for one month. Track how much it saves. That data will be your motivation to keep using it. The app needs your engagement to learn your preferences and provide better recommendations. Give it at least three months before deciding whether it's valuable.</p>

<h2>THE BOTTOM LINE</h2>

<p>AI didn't change what your family needs&mdash;safe finances, good healthcare, affordable living. It changed how you access those things. Families in {n} who learned basic digital skills gained access to better, cheaper services. Those who didn't found themselves paying more for less, or not accessing services at all. The tools are available, many at low or no cost. The investment is your time and willingness to learn something new. The return is a meaningfully better quality of life for your household: more money in your account, better health through early detection, and the security of understanding the systems you depend on.</p>

<p>The gap between digital and offline households will widen further between 2030 and 2035. Families that begin their digital transition now have five years to adapt. Families that wait until necessity forces the transition will have no cushion, no time for learning, no margin for error. Your choice is not about becoming a technology expert. It is about becoming a competent technology user who can navigate the economy your children will inherit. That capability is available to you now, at minimal cost, with support from your community. The only real barrier is starting. Start this week.</p>"""

    # =========================================================================
    # BLUE-COLLAR WORKER (C-priority, 1500-2000 words)
    # =========================================================================
    elif aud == "blue-collar-worker":
        body = f"""{memo_header}
<h1>{n}: What Happened to Frontline Workers When AI Hit the Factory Floor</h1>

<p>You work with your hands in {n}, earning {mfg_sal}. Maybe you are in {ind1.lower()}, or {ind2.lower()}, or {ind3.lower()}&mdash;the sectors that employ frontline workers across {n}'s labor force of {lf}. In 2025, your skills were valued, your job felt stable, and AI seemed like something for office workers to worry about. By June 2030, the factory floor, the workshop, and the job site had been transformed. This memo tells you what happened to workers who adapted and those who didn't.</p>

<p>Between 2025 and 2030, {n}'s manufacturing and services sectors experienced what economists call "rapid capability replacement"&mdash;the process where AI and robotics take over routine tasks and, within years, make traditional skills obsolete. This happened in three overlapping waves. In 2025&ndash;2026, AI systems were tested on controlled tasks: assembly line quality control, basic robotic operations, predictive maintenance. By 2026&ndash;2028, deployment accelerated as systems proved themselves. Plants ran two shifts: one with traditional workers, one with AI systems doing the same job faster. By 2028&ndash;2030, the choice became clear to every employer: maintain expensive traditional labor or deploy proven AI systems. The workers who thrived in this transition were those who trained early, positioned themselves as skilled operators of new systems, and built technical competence before displacement forced them to choose.</p>

<h2>THE BEAR CASE: Three Workers Who Were Caught Off Guard</h2>

<p><strong>Scenario 1: The {ind1} Worker Whose Skills Became Obsolete</strong><br/>
You had ten years of experience in {ind1.lower()}, earning {mfg_sal}. Your hands knew the work. But by 2027, AI-driven automation and robotic systems could perform your core tasks with higher consistency. Your employer didn't eliminate your job overnight&mdash;they reduced it. Fewer shifts. Fewer hours. Your monthly income dropped 30%, then 40%. The new roles that replaced yours required technical skills you didn't have: programming automated systems, interpreting AI quality reports, maintaining robotic equipment. By 2030, you were either in a much lower-paying position or had left the sector entirely.</p>

<p>The damage compounded across your life. By 2028, with reduced hours and income, you couldn't afford the retraining programs that cost the equivalent of three months' full salary. Your family's emergency savings, if you had them, got depleted as you tried to maintain your lifestyle during reduced work. By 2029, the experience gap became insurmountable: you had ten years of experience in skills no employer valued, and you were starting from zero in the new technical skills that all employers demanded. You weren't competing against younger workers with fresh technical training. You were competing against your former colleagues who had the foresight to retrain in 2025&ndash;2026. They had years of experience in the new systems. You had none. Even when you finally accessed training in 2029&ndash;2030, you were years behind your peers. The income loss between 2027 and 2030 was permanent. The career trajectory damage lasted decades.</p>

<p><strong>Scenario 2: The {ind2} Worker Who Refused Retraining</strong><br/>
You worked in {ind2.lower()} and took pride in doing things the traditional way. When your employer offered a retraining program in 2026, you saw it as an insult to your experience. You declined. The colleagues who accepted the training learned to operate and maintain the new AI systems. By 2028, they were earning 40&ndash;50% more than before. You were earning the same or less, in a shrinking pool of traditional roles. When layoffs came in 2029, you were among the first affected. The retraining programs that had been free through your employer now cost the equivalent of several months' salary at {mfg_sal} if accessed independently.</p>

<p>Your resistance had created a cascade of losses. The pride that made you decline retraining in 2026&mdash;pride in mastery, pride in knowing a craft the old way&mdash;became shame by 2029 when you were unemployed in a competitive job market. The colleagues who accepted training and whom you'd perhaps dismissed as "selling out" were the ones who stayed employed, got promotions, earned better wages, and had options. You had no options. The market that had valued your traditional skills for a decade had simply stopped valuing them. The world moved on, and your refusal to move with it left you behind, watching your former peers succeed while you struggled. By 2030, you were retraining anyway, but from a position of desperation rather than opportunity, which made the learning harder, slower, and less effective.</p>

<p><strong>Scenario 3: The Worker in {ind3} Who Ran Out of Time</strong><br/>
You planned to retrain eventually but kept putting it off. In 2025, you were busy. In 2026, the training programs seemed overwhelming. In 2027, you started looking into options but couldn't commit. By 2028, when you were finally ready, the affordable programs were oversubscribed, the job market had shifted, and the career transition that would have taken six months in 2025 now required two years of intensive retraining. You had lost your window of opportunity.</p>

<p>The time loss was the critical damage. The workers who acted in 2025 had completed training by 2026 and had years of on-the-job experience by 2030. The workers who acted in 2028 were still in training in 2030, competing for jobs against peers who had years of advantage. In {n}'s labor market, time compounds into experience, and experience compounds into value. A six-month delay in 2025 became three years of disadvantage by 2030. You couldn't compress six months of training into four months to catch up. You couldn't gain three years of experience quickly. The window of opportunity had a specific duration, and missing it meant years of catching up that might never fully compensate for the lost time. Some colleagues you'd known for years had already transitioned and were senior in their new roles by the time you started training.</p>

<h2>THE BULL CASE: The Same Three Workers Who Acted</h2>

<p><strong>Scenario 1: The {ind1} Worker Who Added Technical Skills</strong><br/>
Same person, same starting point. In 2025, you enrolled in a six-month evening program to learn AI-assisted machinery operation and maintenance. The cost was manageable&mdash;your employer subsidized half. By mid-2026, you were certified. When AI systems arrived at your workplace, you were the person who understood both the old processes and the new technology. You were promoted to AI systems operator. Your income increased 40&ndash;50% by 2028. By 2030, you supervised a team and earned well above {sal}. Your hands-on experience, combined with technical skills, made you irreplaceable in ways that either skill alone could not.</p>

<p>Your early action positioned you as essential in a transforming workplace. The employer faced a choice: replace you with automation or use you as the bridge between old and new systems. You were the bridge. You trained new hires. You troubleshot problems that required understanding both systems. You optimized processes by knowing what worked in the old way and why it mattered in the new way. By 2030, you weren't competing for entry-level automation operator roles. You were in a supervision and training role, earning almost double your 2025 salary, with genuine job security that lasted through the next decade. Your career, rather than being cut short, had actually accelerated. The colleagues who resisted or delayed were underemployed. You had leveraged the transition into advancement.</p>

<p><strong>Scenario 2: The {ind2} Worker Who Took Every Opportunity</strong><br/>
Same offer, different answer. You took the free retraining program in 2026. It wasn't easy&mdash;evenings after physical work were exhausting. But by 2027, you had new capabilities. You understood how to work alongside AI systems, troubleshoot basic issues, and optimize processes using data from AI monitoring tools. The promotion came quickly. By 2028, your earnings had increased substantially, and you had genuine job security because your combination of practical experience and AI literacy was exactly what employers needed.</p>

<p>Your choice to accept retraining, despite fatigue and doubt, created compounding advantages. By 2028, you weren't just earning more; you were building expertise that got more valuable over time. As AI systems matured and evolved, your experience in managing and optimizing them made you increasingly valuable. When new technologies appeared in 2029&ndash;2030, you had the foundation to learn them quickly. You went from a worker with status quo job security to a worker with genuine expertise that was scarce in {n}'s labor market. Companies competed to recruit you. You could negotiate better terms, better benefits, better work arrangements. The investment you made in 2026 by attending evening retraining had multiplied by 2030 into career optionality and earning power that seemed impossible in 2025.</p>

<p><strong>Scenario 3: The Worker Who Started Immediately</strong><br/>
Same situation, but you acted in 2025 instead of waiting. You found free online resources, started learning during commutes and lunch breaks, and built a basic understanding of AI tools relevant to your industry. When formal training opportunities appeared in 2026, you were ahead of your peers. By 2027, you were among the first workers certified in AI-assisted operations. By 2030, you had five years of experience in AI-augmented work&mdash;a head start that translated directly into higher earnings and better opportunities.</p>

<p>Your five-year head start made you not just experienced but senior. You weren't learning alongside new trainees in 2030; you were teaching them. You'd already mastered the transition most of your peers were just beginning. You had the deepest understanding of what worked and what didn't in the new systems. You had problems solved that others were still encountering. By 2030, the colleague who started learning online in 2025 during lunch breaks was earning the equivalent of {sal} or more, supervising teams, training new workers, and had built genuine expertise that would remain valuable for the next decade as technology evolved further. Your early start during commutes and lunch breaks in 2025 had been the difference between thriving and struggling.</p>

<h2>THE CRITICAL INFLECTION: The Window Was Real and It Closed</h2>

<p>The three scenarios above aren't speculative. They reflect real patterns across {n}'s manufacturing and services sectors between 2025 and 2030. Workers who trained in 2025&ndash;2026 have built five years of experience and genuine expertise. Workers who trained in 2028&ndash;2029 are still learning. Workers who never trained are unemployed or underemployed in roles that pay 30&ndash;50% less than they earned before. The window of opportunity was real. It was open in 2025. It was closing by 2027. It was largely closed by 2028. The workers who thrived were those who recognized the window and acted before it closed.</p>

<h2>WHAT YOU SHOULD DO NOW</h2>

<p><strong>1. Assess Your Role's Vulnerability Honestly This Month</strong><br/>
Which parts of your daily work could a machine or AI system do? List them. The parts that are routine and repetitive are most vulnerable. The parts that require judgment, physical dexterity in unpredictable situations, and human interaction are more resilient. Build your career toward the resilient parts. Have this conversation with your supervisor, your union representative if you have one, or trusted colleagues. Get their honest assessment. You need reality, not reassurance.</p>

<p><strong>2. Learn One AI-Adjacent Technical Skill This Year Without Waiting</strong><br/>
Robotic system maintenance, AI-assisted quality control, smart building systems, logistics technology. Pick one that connects to your existing experience. The cost of learning is modest; the return in career security is enormous. Don't wait for your employer to offer training. Seek it out. Even if training costs money out of pocket, the cost of inaction is higher. If your employer offers training, take it immediately. Don't wait for a better time.</p>

<p><strong>3. Take Every Retraining Opportunity Offered Without Hesitation</strong><br/>
If your employer offers training, take it. If your community center offers digital literacy, attend. If your union offers AI-skills programs, enroll. Every skill you add now is an investment in your earning power for the next 20 years. This isn't optional professional development. This is survival and advancement. Treat it with the urgency it deserves.</p>

<p><strong>4. Connect with Workers Who Have Already Transitioned and Learn Their Path</strong><br/>
Find colleagues or workers in your industry who have already made the shift to AI-augmented roles. Learn from their experience. Ask what they wish they had known. Ask them what the retraining was actually like. Ask them how long it took to feel competent. Ask them how much their income changed. Their practical advice is more valuable than any course description. Their experience is your best guide to what's coming and how to navigate it.</p>

<h2>THE BOTTOM LINE</h2>

<p>Blue-collar work in {n} did not disappear between 2025 and 2030. But blue-collar work without AI literacy largely did. The workers earning {mfg_sal} in 2025 who added technical skills are now earning significantly more with greater security. Those who didn't are fighting for fewer positions at lower wages. The message is simple and direct: the time to add AI and technical skills to your toolkit is now. Not next year when you have more time. Not after you've thought about it more. Now. The cost of retraining is manageable when done on your timeline in 2030. The cost of not retraining is your career trajectory, your earnings potential, and possibly your ability to provide for your family at the level you have been.</p>

<p>By 2030, the transition is largely locked in. The window for easy, affordable retraining while still fully employed is closing or closed. The workers who waited are now in crisis mode, scrambling to catch up, competing from a position of desperation. The workers who acted are building careers in the transformed economy with options and security. If you're reading this in 2030, the message is urgent: act now, immediately, without waiting for further confirmation. The window is still open in 2030, but only barely. By 2032&ndash;2033, it will have closed entirely. The technology will be fully deployed. The labor market will have stabilized around the new systems. The workers trained in 2025&ndash;2026 will be senior and hard to displace. The workers trying to train in 2032 will have no advantage and no window. Act in 2030. Your next five years depend on the decision you make this quarter.</p>"""

    # =========================================================================
    # EDUCATOR (C-priority, 1500-2000 words)
    # =========================================================================
    elif aud == "educator":
        body = f"""{memo_header}
<h1>{n}: The Education System That Adapted to AI &mdash; vs. The One That Didn't</h1>

<p>You are an educator in {n}. Maybe you teach at a university, a vocational school, or a secondary school. Your students will enter a labor force of {lf} where the average wage is {sal} and tech skills command {it_sal}. In 2025, literacy stood at {lit}, STEM output at {stem} graduates annually, and internet connectivity at {inet}. You faced a question that would shape an entire generation: do you integrate AI into your teaching and curriculum now, or wait until the education system catches up? By 2030, the answer is devastatingly clear.</p>

<p>Between 2025 and 2030, {n}'s education system experienced an inflection point that divided schools into two categories: those that recognized AI as a fundamental transformation of how learning happens, and those that treated it as optional content. The timeline was crucial. Schools that began integrating AI in 2025&ndash;2026 had time to redesign curricula thoughtfully, train teachers, and evolve alongside technology. Schools that delayed until 2028&ndash;2029 found themselves in crisis mode, forced to implement hastily without the preparation that made integration effective. By 2030, the quality gap between forward-thinking and backward-looking institutions was visible in every measurable outcome: graduate employment rates, starting salaries, student satisfaction, institutional funding, and reputation.</p>

<h2>THE BEAR CASE: The Educator Who Held the Line</h2>

<p><strong>Scenario 1: Your Graduates Entered a Job Market You Didn't Prepare Them For</strong><br/>
You taught your subject the same way you had for a decade. Your curriculum was rigorous. Your standards were high. Your students graduated with deep knowledge of {ind1.lower()}, {ind2.lower()}, or other traditional fields. But by 2028, employers had changed what they were looking for. "AI proficiency" appeared in every job posting. Your graduates competed against peers from institutions that had integrated AI into their curricula. Your students had deeper theoretical knowledge; their competitors had practical AI skills. The competitors were hired. Your students struggled. Some came back to you asking why you hadn't prepared them. You had no good answer.</p>

<p>The damage to your students' career prospects was measurable and lasting. A graduate with deep knowledge but no AI skills took longer to find employment, entered at lower salary levels, and had more difficulty advancing. The employers that would have hired them in 2025 had moved on to graduates with hybrid skillsets. Your institution's employment survey by 2029 showed a three-year lag in placement rates compared to early-adopter schools. The students you graduated between 2025 and 2029 faced five-year disadvantages in earning potential that could compound across careers. Some of your students had to undergo expensive retraining that your institution should have provided. Some left {n} to find opportunities elsewhere. Your reputation for academic rigor, once your institution's greatest strength, became inadequate in the face of unpreparedness for the real economy.</p>

<p><strong>Scenario 2: AI Teaching Tools Passed You By</strong><br/>
AI-powered teaching assistants, personalized learning platforms, and automated grading systems became available between 2025 and 2027. You chose not to use them&mdash;you believed in the traditional teacher-student relationship and worried about academic integrity. Meanwhile, educators who adopted these tools became dramatically more effective. They could personalize instruction for each student. They could identify struggling students earlier. They could spend more time on mentoring and less on administration. By 2028, the quality gap between AI-integrated and traditional classrooms was visible in student outcomes. Your students' test scores, employment rates, and satisfaction surveys all trailed behind.</p>

<p>Your resistance to teaching tools, rooted in legitimate concerns about replacing human interaction with automation, actually diminished human interaction in your classroom. By holding the line against AI grading assistants, you spent hours on grading that could have been mentoring time. By refusing personalized learning platforms, you taught all students at one pace, inevitably leaving some behind while others weren't challenged. The very human qualities you were protecting&mdash;individualized attention, deep mentoring, understanding each student's needs&mdash;became less available because you were overburdened with administrative tasks. The educators who integrated AI tools didn't replace human judgment; they automated routine work and freed more time for the human elements you valued. Your students got less of what you cared about because you refused to use tools that would have protected that time.</p>

<p><strong>Scenario 3: Your Institution Lost Relevance and Funding</strong><br/>
As other institutions in {n} adopted AI-integrated teaching, your institution fell behind. Enrollment dropped as students and parents chose schools with modern approaches. Funding followed enrollment downward. By 2030, your institution was in a cycle of decline: less funding led to less technology, which led to fewer students, which led to less funding. The institution that had been respected in 2025 was struggling for survival by 2030.</p>

<p>The institutional decline had ripple effects across {n}'s education sector. Your school's loss of prestige meant difficulty recruiting and retaining excellent teachers. Your diminished resources meant inability to compete for high-performing students. Your shrinking reputation meant employers stopped recruiting from your institution with the same enthusiasm. The feedback loops of institutional decline are difficult to reverse. A school that was respected in 2025 but rejected AI integration could spend the next decade recovering. Some of {n}'s institutions that held this line never fully recovered. By 2035, they were regional or local schools rather than national institutions, permanently diminished by the decision to resist transformation in 2025&ndash;2026.</p>

<h2>THE BULL CASE: The Same Educator Who Adapted</h2>

<p><strong>Scenario 1: You Redesigned Your Curriculum in 2026 Without Panic</strong><br/>
Same expertise, different approach. In 2026, you spent a summer redesigning your courses to integrate AI tools. You didn't replace your subject matter&mdash;you enhanced it. Students in your {ind1.lower()}-related program now learned to use AI for analysis, automation, and problem-solving alongside traditional skills. By 2028, your graduates were the most sought-after in {n}. They had domain expertise plus AI capability&mdash;exactly what employers wanted. Your placement rates exceeded 90%. Students sought out your program specifically because it prepared them for the real economy.</p>

<p>Your early curriculum redesign positioned your program as the gold standard in {n}. Employers didn't just recruit from your program; they developed partnerships with you. Companies funded scholarships, provided internships, and helped you design curricula. Your students had clear pathways to employment because industry was actively involved in shaping their education. The distinction between your graduates and those from traditional programs became visible immediately in the job market. Your graduates started at higher salaries, had better job security, and advanced faster. By 2030, your program had a waiting list. You could be selective about admissions. The reputation for preparing graduates for the actual economy became a competitive advantage that attracted resources, talented faculty, and promising students.</p>

<p><strong>Scenario 2: AI Teaching Tools Made You a Better Teacher</strong><br/>
You adopted AI teaching tools and discovered they didn't replace you&mdash;they freed you. Automated grading gave you 10 extra hours per week for mentoring. Personalized learning platforms identified which students needed help before they fell behind. AI-generated practice problems adapted to each student's level. Your teaching became more effective, not less personal. By 2028, your student outcomes had improved measurably, and you were training other educators on AI integration.</p>

<p>The time freed by automation allowed you to do what you actually cared about as an educator. Rather than spending evenings grading, you spent time on individualized feedback, mentoring struggling students, and helping advanced students push further. Your students felt known and supported because you had time to understand them as individuals. Paradoxically, integrating technology into your classroom made it more human, not less. By 2030, your student satisfaction scores, pass rates, and learning outcome measures all exceeded traditional classrooms in {n}. Universities and schools across the region were asking you to train their faculty on AI integration because they saw that your adoption of technology had enhanced, not diminished, the human elements of education.</p>

<p><strong>Scenario 3: Your Institution Became a Model and Center of Gravity</strong><br/>
Your institution's early adoption of AI-integrated education attracted attention, funding, and students. Enrollment grew. Research partnerships with AI companies brought resources. By 2030, your institution was a regional model for how education should adapt to the AI era. The investment in AI integration had paid for itself many times over in enrollment, funding, and reputation.</p>

<p>Beyond enrollment and funding, your institution became intellectually influential. Your educators were asked to speak at conferences, publish in journals, and advise government education policy. Your curriculum became a template that other institutions copied. Your graduates were visible successes in the job market, attracting more talent to your school. By 2030, your institution wasn't just larger and better funded than the resisting schools; it had become the intellectual and reputational center of gravity for education in {n}. The early decision to integrate AI, made in 2025&ndash;2026 when many colleagues thought you were premature, had positioned your institution as a leader in educational transformation, not a follower.</p>

<h2>THE CRITICAL WINDOW: The Timeline and Its Consequences</h2>

<p>The educators and institutions that adapted earliest in 2025&ndash;2026 created a lasting advantage. They could redesign curricula based on what early adoption taught them. They had time to train teachers and integrate tools thoughtfully. Those that waited until 2028 when the need was obvious found themselves forced to adapt quickly in crisis mode, with less thoughtful implementation and less effective outcomes. The schools that thrived in {n} were those that recognized in 2025 that AI wasn't optional content; it was a transformation of how learning happens. The schools that didn't thrive were those that waited until 2028&ndash;2029 to begin integration, discovering too late that two years of crisis implementation couldn't overcome three years of curriculum inertia.</p>

<h2>WHAT YOU SHOULD DO NOW</h2>

<p><strong>1. Audit Your Curriculum Against 2030-2035 Employer Needs This Quarter</strong><br/>
For every course you teach, ask: will graduates with only this knowledge be employable in five to ten years? Will they be competitive in their fields? If the answer is uncertain or no, the course needs an AI component or needs redesigning. Start with the courses most connected to high-risk sectors like {risk1.lower()} and {risk2.lower()}, where AI transformation is already visible. But don't stop there; eventually every field needs AI literacy because AI is becoming a tool across all sectors. This audit should be systematic and thorough, not theoretical. Actually talk to employers about their hiring criteria and expectations.</p>

<p><strong>2. Adopt One AI Teaching Tool This Semester as an Experiment Without Delay</strong><br/>
Start small. Don't try to transform your entire program at once. Use an AI grading assistant so you can focus on mentoring instead of grading. Try an AI-powered learning platform that personalizes instruction to individual student pace. Test an AI tutoring system that can provide 24/7 help beyond classroom hours. Experience the tools before forming opinions. Experience how they change what you can accomplish as a teacher. The educators who thrived in {n} were those who experimented first and formed opinions second, not the reverse. Pick a tool and commit to using it for one full term, minimum. Give it time to show benefits.</p>

<p><strong>3. Partner with Employers in Your Field Systematically and Formally</strong><br/>
Talk to the companies that hire your graduates. Ask not just what AI skills they need but what the AI transformation means for careers in your field. What problems is AI solving? What new opportunities is it creating? What will entry-level work look like in five years? Build those skills and perspectives into your program. The most successful programs in {n} were designed in partnership with industry, not in isolation from it. Formalize these partnerships. Create advisory boards. Have employers review your curriculum. Students appreciate knowing that the skills you're teaching them matter because employers said so.</p>

<p><strong>4. Invest in Your Own AI Literacy Immediately and Continuously</strong><br/>
You cannot effectively teach what you do not understand. Spend meaningful time learning AI tools relevant to your field. Take a workshop or online course this month. Use AI tools yourself to accomplish actual work in your field. Spend at least an hour per week for the next three months learning AI. The educators who adapted first were those who learned first, who experimented, who became comfortable enough to model learning for students. Your comfort with AI tools matters more than perfect mastery; students need to see that learning new tools is possible, not frightening. Your students need to watch you learning, struggling, and then succeeding with technology they'll need to master.</p>

<h2>THE BOTTOM LINE</h2>

<p>Education in {n} didn't need to choose between human teachers and AI&mdash;it needed both, integrated thoughtfully. The educators who integrated AI earliest produced graduates who could navigate a transforming economy confidently. Those who resisted produced graduates who entered the workforce underprepared, requiring emergency retraining at employers' expense. Every semester of delay in AI curriculum integration represented a cohort of students sent into the workforce without critical tools they needed. Your responsibility as an educator has not changed: prepare your students for the world they will actually enter. In 2030 and beyond, that world requires basic AI fluency, just as it requires basic digital literacy.</p>

<p>The choice facing educators in 2030 is identical to the choice that faced educators in 2025: integrate AI into teaching and curriculum now, or watch your graduates enter a job market where they're unprepared. The only difference is that schools which integrated in 2025&ndash;2026 are now leaders with five years of refined practice. Schools integrating in 2030 have to catch up. But catching up is still possible, and urgent. A school that integrates thoughtfully in 2030 will have graduated AI-competent students by 2032. A school that waits until 2032 to integrate will graduate unprepared students in 2034. The timeline is relentless. The message is urgent. Begin now.</p>"""

    # =========================================================================
    # PARENT (C-priority, 1500-2000 words)
    # =========================================================================
    elif aud == "parent":
        body = f"""{memo_header}
<h1>{n}: The Parents Who Prepared Their Children for AI &mdash; And Those Who Hoped It Would Pass</h1>

<p>You are raising children in {n}, where the average household earns {sal}. Your children will enter a labor force of {lf} where AI has fundamentally changed what employers value. In 2025, tech roles already commanded {it_sal}, but most parents assumed their children's education would prepare them adequately. GDP per capita was {gdp_pc}, growth at {gdp_gr}. By 2030, the parents who took active steps to supplement their children's education with digital and AI literacy gave their children a decisive advantage. Those who left it entirely to schools did not.</p>

<p>Between 2025 and 2030, parental choice about AI literacy became the single largest determinant of children's starting career positions. This wasn't because schools failed&mdash;though many did adapt slowly&mdash;but because the pace of change outstripped even the most forward-thinking education systems. The parents who recognized in 2025 that AI was no longer optional, but essential, acted immediately. They invested in devices and internet access. They found free online learning resources. They talked to their children about which careers were disrupted and which were resilient. By 2030, these early-moving parents had children with five years of accumulated AI literacy. The children of parents who waited for schools to catch up were entering the workforce in 2030 underprepared and requiring emergency reskilling.</p>

<h2>THE BEAR CASE: Children Educated for Yesterday's Economy</h2>

<p><strong>Scenario 1: The Traditional Career Path That Vanished</strong><br/>
You encouraged your child to study {ind1.lower()} or a related field&mdash;it had provided good careers for your generation. Your child studied diligently, graduated with honors. But by 2028, the {ind1.lower()} job market had transformed. Entry-level positions that once valued traditional knowledge now required AI competency as a baseline. Your child competed against graduates who combined {ind1.lower()} knowledge with practical AI skills. The AI-skilled graduates were hired. Your child was not. At a household income of {sal}, you couldn't easily fund the emergency retraining your child now needed. The career gap widened with every month.</p>

<p>Your child's first job search experience was devastating. They had invested years in education, performed excellently, and emerged with credentials that should have opened doors. Instead, they discovered that traditional credentials alone were insufficient. The employers that would have hired them in 2025 had moved on to candidates with hybrid skillsets. Your child applied to dozens of positions, competed against peers who had invested in AI skills, and faced rejection after rejection. The emotional toll was significant: frustration, doubt, questioning whether their education had been worthwhile. By 2028, they finally found entry-level work that paid less than they'd expected, in a role that didn't match their education. By 2030, they were either trying to catch up through expensive retraining or had accepted a career trajectory diminished by their late start in AI literacy. The five-year advantage that early-learning children had started to compound into a ten-year career gap.</p>

<p><strong>Scenario 2: Digital Access You Didn't Prioritize</strong><br/>
With internet penetration at {inet} in {n}, digital access wasn't automatic. You prioritized other household expenses over technology access for your children&mdash;a reasonable decision in 2025 when the connection between digital tools and future careers wasn't obvious. But by 2027, children with early digital access had a two-year head start in AI literacy. By 2030, that gap had translated into a measurable career advantage. The cost of a basic digital device in 2025 was a fraction of the career earnings difference it would have enabled.</p>

<p>Your decision to prioritize other expenses over technology access created unequal opportunity for your child. Peers with home devices and internet could take online courses, practice with AI tools, build portfolios, and gain practical experience. Your child had to access technology through school or libraries, which meant less practice, less time, and less depth. When college admissions came, they couldn't submit as sophisticated digital portfolios or demonstrate as many digital skills as peers who'd had home access. When job searching began in 2030, they couldn't access online learning platforms to accelerate their skills during the search. The compounding effect of two-year delayed access extended into decades of reduced earning potential.</p>

<p><strong>Scenario 3: You Trusted the School System Entirely</strong><br/>
You assumed your children's school would adapt to the AI era. For many schools in {n}, the adaptation was too slow. Curricula updated years behind industry reality. Teachers were not trained in AI tools. Your children graduated with skills relevant to 2020, not 2030. The parents whose children thrived were those who supplemented school education with additional AI learning&mdash;online courses, coding programs, digital projects. Those who left it entirely to schools found the gap too wide by the time they noticed.</p>

<p>By the time you noticed your child's skills were mismatched to market reality, precious years had passed. They were in job market competition in 2029&ndash;2030 without time to catch up. The supplemental learning that should have been happening over five years (2025&ndash;2030) now had to be compressed into months or a year. The acceleration was possible but expensive and stressful. Your child paid for retraining out of their first post-graduation income, starting their career already behind financially. Schools in {n} adapted, but many didn't adapt fast enough to keep pace with industry. The parents who supplemented school with home learning ensured their children stayed ahead. Those who relied entirely on schools found schools playing catch-up, and their children bearing the cost.</p>

<h2>THE BULL CASE: Children Who Entered 2030 Future-Ready</h2>

<p><strong>Scenario 1: You Encouraged AI-Enhanced Learning Early</strong><br/>
In 2025, you introduced your child to AI learning tools alongside their regular schoolwork. Not instead of it&mdash;alongside it. Your child learned to use AI for research, problem-solving, and creative projects. By the time they reached higher education, they had years of practical AI experience. They graduated into a job market that valued exactly their profile: domain knowledge plus AI fluency. Their starting salary exceeded the {sal} average from day one, and their career trajectory was on a steep upward path.</p>

<p>Your early encouragement positioned your child as a rare double-skilled candidate in the job market. By 2030, most graduates had either domain knowledge or AI skills, but not both. Your child had both. The employers that competed for graduates with both skillsets offered premium starting salaries. Your child's first role paid 30&ndash;40% above the average for the field. More importantly, the combination of skills made them valuable across sectors&mdash;they could pivot to different industries or roles without losing relevance. By 2030, your child's peers who lacked AI skills faced career pigeonholing; once you were an {ind1.lower()} specialist without AI, changing fields was hard. Your child with AI fluency had options and flexibility that defined career advantage.</p>

<p><strong>Scenario 2: You Invested in Digital Access as a Priority</strong><br/>
You recognized that digital access was no longer a luxury for your children&mdash;it was an investment in their future. You prioritized a basic device and internet connectivity. Your children used it for educational purposes: online courses, coding exercises, AI-powered learning platforms. The cost was modest at a household income of {sal}. The return was transformative. By 2030, your children had digital skills that opened doors their offline peers couldn't access.</p>

<p>Your investment in home technology created an asymmetric advantage. Your child practiced AI skills at home, did online courses during lunch breaks, participated in digital learning communities, and built portfolios of digital work. These weren't activities that required wealth; they required a device and internet connection and parental encouragement. You provided both. By high school, your child was comfortable with technology in ways that many peers weren't. By college, they were already ahead in digital literacy. By the job market in 2030, they had years of demonstrated experience with technology that they could point to. The cost of your device and internet investment, spread across five years, came to a few weeks of household income annually. The return was a child positioned for career advancement in a digital-transformed economy.</p>

<p><strong>Scenario 3: You Supplemented School with Self-Directed Learning</strong><br/>
You didn't criticize your children's school&mdash;you supplemented it. You found free online resources, local community programs, and family learning activities that introduced AI concepts. Your children learned computational thinking, basic coding, and how to work with AI tools. These skills compounded over time. By 2030, they entered the workforce with a capability set that formal education alone hadn't provided.</p>

<p>Your effort to supplement school created a multiplier effect. Your child received rigorous traditional education (important for credibility and domain knowledge), plus practical AI skills (essential for career competitiveness). Together, these created capabilities that neither school alone nor self-learning alone could have provided. By 2030, your child stood out in recruiting because they had both institutional credentials and demonstrated practical skills. The interviews that mattered in 2030 involved practical problems&mdash;can you actually use AI tools to solve problems&mdash;not just theoretical knowledge. Your child could say yes with evidence. Peers who had only school credentials struggled to answer these practical questions.</p>

<h2>THE CRITICAL PARENTAL CHOICE: The Window and Its Costs</h2>

<p>The parents who gave their children AI literacy and digital access in 2025&ndash;2026 didn't do so because the connection to career success was proven. They did so because they recognized early signals and made proactive investments. The returns have been dramatic. The parents who assumed schools would handle it, or waited for a clearer signal, found themselves in 2028 trying to close gaps that were hard to close. The investment in AI literacy early was small: a few hundred dollars for a device, a few hours per week of parental encouragement, finding free resources online. The investment in catching up later was large: thousands of dollars for emergency retraining, months or years of delayed career entry, reduced earning potential across decades.</p>

<h2>WHAT YOU SHOULD DO NOW</h2>

<p><strong>1. Introduce Your Children to AI Learning Tools This Month Without Delay</strong><br/>
Not next summer when you have more time. Not next year when you've thought about it more. This month. Free resources exist. Start with age-appropriate platforms that teach computational thinking, basic coding, and AI concepts through games and projects. The goal is not to make your child a programmer&mdash;it is to make them comfortable, capable, and curious about technology. Even 30 minutes per week matters if it's consistent. Small, regular exposure compounds into genuine capability over years. Get your child started this week. The earlier they begin, the more years they have to build competence before entering the job market.</p>

<p><strong>2. Prioritize Digital Access as an Investment in Career Security</strong><br/>
If your household doesn't have internet access or a basic computing device, explore options: community centers, school programs, shared devices, subsidized plans. At a household income of {sal}, adding a basic internet connection and simple device is a meaningful expense&mdash;but the return in your child's career prospects is outsized. Do the math: a year of internet access costs the equivalent of a few weeks of household income. Your child's career advantage is worth decades of income. It's one of the best investments you can make. Prioritize this. Consider it not a luxury but an educational investment on par with school supplies or tutoring.</p>

<p><strong>3. Guide Career Conversations with Clear-Eyed AI Awareness</strong><br/>
When your children talk about future careers, help them understand which sectors in {n} are growing and resilient versus facing disruption. The high-risk sectors like {risk1.lower()}, {risk2.lower()}, and {risk3.lower()} are experiencing AI-driven transformation. This isn't to steer them away from careers they're passionate about, but to help them make informed choices. Encourage combinations: traditional interest plus AI capability. This is not about choosing AI over everything else&mdash;it's about adding AI to whatever they love. A child passionate about {ind1.lower()} can thrive if they add AI skills. Without them, that passion will lead to disappointment in the job market.</p>

<p><strong>4. Model Lifelong Learning Yourself</strong><br/>
Your children learn more from what you do than what you say. If they see you learning new digital skills, see you pushing yourself out of your comfort zone to learn new tools, see you treating learning as a normal lifelong activity, they will adopt that attitude. If they see you avoiding technology, resisting change, complaining about how everything is becoming digital, they may develop the same resistance and avoidance. You are your children's primary role model for how to respond to disruption. If you believe technology is frightening and optional, they will too. If you believe it's essential and learnable, they will adopt that mindset.</p>

<h2>THE BOTTOM LINE</h2>

<p>You do not need to make your children into AI engineers or computer scientists. You need to make them comfortable, capable, and curious about AI and digital tools. In {n}'s economy, the children who will thrive are those who can work effectively with AI in any field they choose&mdash;traditional industries, healthcare, education, skilled trades, creative fields, whatever&mdash;not just in technology. The investment required from you is modest&mdash;time, attention, and basic digital access. The return is your children's career security and opportunity in an AI-transformed world. Start now. Every year of AI fluency your children gain before entering the workforce compounds their advantage in ways that are hard to predict but easy to see when you look at how the labor market valued these skills between 2025 and 2030.</p>

<p>The window is still open in 2030, but it's closing. Children entering high school in 2030 have limited time to accumulate AI skills before the job market in 2035&ndash;2036. The parents who act now, immediately, are ensuring their children graduate with adequate preparation. The parents who wait another year or two risk their children entering the workforce in 2033&ndash;2034 without sufficient skills. Don't wait. Invest in your children's AI literacy now. The cost is small. The stakes are their careers.</p>"""

    # =========================================================================
    # RETIREE (C-priority, 1500-2000 words)
    # =========================================================================
    elif aud == "retiree":
        body = f"""{memo_header}
<h1>{n}: AI and Your Retirement &mdash; How Disruption Affected Senior Security</h1>

<p>You are retired or nearing retirement in {n}, where the average income is {sal} and GDP per capita stands at {gdp_pc}. You spent your career in an economy powered by {ind1.lower()}, {ind2.lower()}, and {ind3.lower()}. Now you depend on the systems those industries fund: pensions, healthcare, and the economic stability that supports your family. In 2025, AI seemed like a young person's concern. By 2030, it has reshaped every system you rely on. This memo tells you what happened and what you can still do.</p>

<p>Between 2025 and 2030, AI disruption created a harsh divide in retirement outcomes. Retirees who adapted to digital tools strengthened their security and improved their quality of life. Retirees who resisted digitalization found themselves increasingly isolated from the services they depended on, often with reduced access and higher costs. This wasn't a difference of thousands in annual income for most retirees; it was a difference in daily dignity, healthcare access, financial security, and connection to family. For many seniors, the choice about whether to embrace digital tools wasn't an abstract technology question. It was a survival question.</p>

<h2>THE BEAR CASE: The Retiree Who Was Left Behind</h2>

<p><strong>Scenario 1: Your Pension Was Eroded by Economic Disruption</strong><br/>
{n}'s pension system depended on contributions from working-age adults earning {sal} across {ind1.lower()}, {ind2.lower()}, and other sectors. When AI displaced workers in high-risk sectors ({risk1.lower()}, {risk2.lower()}, {risk3.lower()}), the contribution base shrank. Fewer workers contributing meant less funding for retiree benefits. Government budgets, already strained by {challenge_short}, had little room to compensate. By 2028, your pension's purchasing power had declined noticeably. The promises made when you were contributing were not fully kept because the economy that was supposed to fund them had fundamentally changed.</p>

<p>The pension erosion was psychologically and financially devastating. The amount you'd been promised in retirement was suddenly insufficient. You'd made financial decisions your entire career based on that promise. You'd delayed other investments, avoided certain risks, chosen your work partly for the pension security it offered. By 2028, the fundamental deal had been rewritten without your consent. Your purchasing power declined 10&ndash;15%. At an income of {sal}, that meant the loss of months of annual income. The lifestyle adjustments required were substantial. Some retirees cut essential spending: medications, heating, food quality. Some had to ask adult children for financial help, creating dependency and dignity loss. The economic disruption that created AI opportunities for others had created insecurity for retirees whose income was locked into systems that had fundamentally changed.</p>

<p><strong>Scenario 2: Healthcare Went Digital and You Lost Access</strong><br/>
AI-powered healthcare&mdash;telemedicine, AI diagnostics, digital prescriptions&mdash;became the standard in {n} between 2026 and 2029. Hospitals shifted resources to digital channels. In-person care became less available and more expensive. With internet penetration at {inet}, many seniors couldn't access the new digital healthcare systems. If you didn't use a smartphone confidently or have reliable internet, you faced longer wait times, fewer options, and higher costs for the in-person care you needed. The healthcare system had improved for the digitally connected and deteriorated for those who weren't.</p>

<p>Healthcare access became a crisis for digitally disconnected seniors. You couldn't schedule telemedicine appointments because you didn't know how. You couldn't email your doctor because you weren't comfortable with email. You couldn't receive digital prescriptions and have them delivered. Your only option was in-person care, which became increasingly hard to access as hospitals rationalized resources. Appointment wait times extended from weeks to months. Urgent issues that could have been addressed via telemedicine turned into serious conditions requiring emergency care, which was more expensive and less effective. Some seniors simply avoided healthcare because access had become too difficult, allowing preventable conditions to advance into serious illness. The healthcare system had genuinely improved for digitally literate seniors. For those offline, it had deteriorated into something barely accessible.</p>

<p><strong>Scenario 3: Family Support Diminished Severely</strong><br/>
In many households in {n}, retirees depended partly on financial support from working-age children. When those children's careers were disrupted by AI&mdash;reduced hours, layoffs, wage compression&mdash;their ability to support you diminished. At an average income of {sal}, there was little surplus even before disruption. After it, intergenerational financial support became strained in ways that affected your daily quality of life.</p>

<p>For retirees depending on children's support, the AI-driven disruption in working-age incomes created a cascade failure. A child earning {sal} might have been able to send a small amount monthly to a retired parent. After AI disruption, that child's income dropped 30&ndash;40%. They could no longer send money. The retiree, already managing pension erosion and healthcare cost increases, suddenly lost that supplemental support. Some retirees had to move in with adult children, losing independence. Some moved to lower-cost regions where their pension went further, leaving communities they'd lived in for decades. The intergenerational contract that had worked for generations broke under the strain of rapid economic transformation.</p>

<h2>THE BULL CASE: The Same Retiree Who Embraced Change</h2>

<p><strong>Scenario 1: AI-Driven Economic Growth Strengthened Your Pension</strong><br/>
In the bull scenario, {n}'s government managed the AI transition effectively. Workforce retraining kept employment stable. AI-enhanced productivity increased GDP growth above {gdp_gr}. The tax base grew rather than shrank. Pension funding stabilized and, in some cases, improved. The economy that underpinned your retirement security grew stronger, not weaker, because of AI. The key was governance: governments that invested in transition protected retirees; those that didn't left them exposed.</p>

<p>When economic growth happened, retiree security improved. A pension that would have been eroded under weak economic growth actually grew or held steady. The working-age population that contributed to your pension remained employed and earning, thanks to government support and business adaptation. Your pension remained a meaningful income stream. Adult children, whose careers remained stable despite AI disruption, could continue supporting you if needed. The difference between this scenario and the bear case was the difference between security and anxiety, between maintaining independence and losing it, between dignity in retirement and desperation.</p>

<p><strong>Scenario 2: Telemedicine Improved Your Healthcare Dramatically</strong><br/>
You attended a community digital literacy program in 2026. A family member helped you set up a telemedicine app. The first time you used it, you were skeptical. But the convenience was undeniable: consultations without travel, prescriptions delivered, AI-powered health monitoring that caught a potential issue before it became serious. By 2028, you were using telemedicine regularly. Your healthcare was more frequent, more convenient, and more effective than the in-person-only system you had relied on. The technology that seemed threatening became your ally.</p>

<p>Telemedicine changed your health outcomes measurably. With easy access to consultations, you used healthcare preventively rather than crisis-driven. Small issues were addressed before they became serious. Chronic conditions were monitored continuously, allowing adjustments before problems emerged. You had more frequent contact with healthcare providers because telemedicine removed the travel burden. Your health improved, and your healthcare costs declined because you were catching problems early. Some seniors using telemedicine regularly avoided hospitalizations that would have been required in the in-person-only system. The convenience translated directly into better health and lower costs.</p>

<p><strong>Scenario 3: Digital Tools Made Daily Life Easier and Richer</strong><br/>
You learned to use basic digital tools: mobile banking, online shopping, video calls with family. Each tool solved a real problem. Mobile banking meant no more trips to the bank. Online shopping gave you access to better prices and delivery. Video calls kept you connected with family members who lived far away. None of this required becoming a technology expert&mdash;it required learning a few apps with help from family or community programs. By 2030, your quality of life had genuinely improved because of technology you initially feared.</p>

<p>Each digital tool solved a specific problem and improved daily life. Mobile banking let you manage your limited income more effectively, access better interest rates, and avoid fees. Online shopping provided access to goods at prices and with convenience that weren't possible offline. Video calls with grandchildren living in other countries transformed what had been annual Christmas phone calls into weekly face-to-face conversations. You weren't becoming a technology expert. You were using specific tools to solve specific problems, and those solutions improved your life measurably. By 2030, seniors who'd learned these tools had better managed finances, access to goods and services, and stronger family connections than they would have offline.</p>

<h2>THE CRITICAL INFLECTION: When AI Touched Retirement Security</h2>

<p>Between 2025 and 2030, retirement in {n} diverged into two completely different experiences based on a single factor: digital capability. Retirees who embraced digital tools experienced improved security, better healthcare, and richer connection. Retirees who resisted experienced eroded security, deteriorating healthcare access, and increasing isolation. This wasn't a small difference. It was the difference between living well and struggling, between dignity and dependency, between engagement and isolation.</p>

<h2>WHAT YOU SHOULD DO NOW</h2>

<p><strong>1. Learn to Use a Smartphone Confidently This Quarter Without Delay</strong><br/>
This is the single most valuable technology investment for seniors in {n}. Mobile banking, telemedicine, communication with family, information access, emergency assistance&mdash;all flow through your phone. Don't put this off. Ask a family member for help, visit a community center, or find a senior-focused digital literacy class at your library. Many community programs offer free training specifically for seniors. Set a goal: by the end of this quarter, you should be able to: use basic apps, send a text message or email, make a video call, and access a website. That's not asking for expertise; it's asking for basic comfort. This is not optional. Your access to the systems you depend on increasingly requires smartphone competency.</p>

<p><strong>2. Register for Telemedicine Services and Use It as Your Primary Healthcare Access</strong><br/>
Access preventive healthcare through AI-powered platforms available in {n}. Early detection of health issues saves money and improves outcomes significantly. Most platforms work on basic smartphones with modest data requirements (2G data is sufficient for many). Don't wait for serious illness to use telemedicine. Use it for routine concerns before they become serious. A preventive health screening through telemedicine can catch problems that would have gone undetected for years through in-person care you're less likely to access. Commit to using telemedicine at least quarterly for preventive assessment, not just when you're sick.</p>

<p><strong>3. Set Up Digital Banking Deliberately with Family or Community Help</strong><br/>
Mobile banking provides better interest rates on savings, lower fees on transfers, and easier money management than cash-only or branch-only approaches. The security concerns about digital banking are real but manageable with basic precautions that any digital literacy program will teach: strong passwords, not sharing personal information, using secure networks. Compared to the risk of carrying cash or storing it at home, digital banking is actually safer. More importantly, having a digital banking presence allows you to access credit if you face an emergency, at reasonable rates instead of predatory rates.</p>

<p><strong>4. Stay Connected Digitally with Family and Community as a Priority</strong><br/>
Video calls, messaging apps, and social platforms keep you connected with family and community in ways that transform isolation into engagement. Social connection is not a luxury&mdash;research over decades shows it is a primary determinant of health and happiness in retirement. If you have family members living far away, being able to video call them weekly changes everything. If you live alone, being able to message friends or participate in online communities reduces isolation measurably. Isolation kills; connection heals. Learning digital tools is not about technology; it's about remaining engaged with people you love.</p>

<h2>THE BOTTOM LINE</h2>

<p>You do not need to become a technology expert or understand how AI works. You need to become a comfortable technology user who can leverage digital tools to improve your life. The retirees in {n} who learned basic digital skills&mdash;smartphone use, telemedicine, digital banking, family video calls&mdash;found their retirement security strengthened, their healthcare improved, their costs reduced, and their relationships deepened. Those who didn't found themselves increasingly isolated from the services and systems they depended on, paying more for less access. The investment is small: a few hours of learning with patient guidance from family or community programs. The return is significant: better healthcare outcomes, safer finances, stronger family connections, and less isolation. Your retirement years are your time to live well. Digital skills are no longer optional for living well in a digital world.</p>

<p>By 2030, the choice to embrace or resist digital tools is largely locked in. The retirees who learned them have five years of experience and genuine competency. Those who haven't are increasingly struggling. If you're reading this in 2030 and haven't yet made the transition, the urgency is high. Community digital literacy programs for seniors exist and are free or low-cost. They're designed specifically for older learners with patience and appropriate pace. The window for learning with support is still open in 2030. Within a few years, that window will close, and you'll be managing your life in an increasingly digital world without the foundational skills you need. Learn now. Your health, finances, and happiness in retirement depend on it.</p>"""

    # =========================================================================
    # SMALL BUSINESS OWNER (B-priority, 1500-2000 words)
    # =========================================================================
    elif aud == "small-business-owner":
        body = f"""{memo_header}
<h1>{n}: AI vs. Small Business &mdash; The Owners Who Adapted and Those Who Didn't</h1>

<p>You run a small business in {n}, earning roughly {sal}. Maybe you operate in {ind1.lower()}, or {ind2.lower()}, or a local service business that has been the backbone of your community. In 2025, your competitors were other local businesses. By 2030, your competitors include AI-powered enterprises that serve your customers faster, cheaper, and with more personalization than you ever could manually. GDP per capita in {n} is {gdp_pc}, growth at {gdp_gr}. This memo examines what separated the small businesses that thrived from those that couldn't keep up.</p>

<p>Between 2025 and 2030, small business owners in {n} faced an unprecedented transformation. The competitive landscape that had been stable for years became turbulent. Relationships and quality work, once sufficient to sustain a business, became table stakes. Customers expected digital convenience, transparent pricing, online presence, and AI-powered efficiency. The small business owners who adapted early and systematically gained competitive advantages that compounded into business transformation. Those who delayed found themselves competing against better-equipped rivals, fighting for declining market share, struggling to maintain the revenue that had been stable for years.</p>

<h2>THE BEAR CASE: Three Business Owners Who Lost Ground</h2>

<p><strong>Scenario 1: The {ind1} Business Owner Who Ignored Digital Entirely</strong><br/>
You ran a small {ind1.lower()}-related business with five employees. Your customer base was local and loyal. In 2025, you saw no reason to invest in AI tools&mdash;your business ran on relationships and quality work. By 2027, a competitor adopted AI-powered customer management, automated their back office, and began targeting your customers with personalized offers based on purchasing patterns. Their prices were comparable but their service was faster and more convenient. By 2028, you had lost 30% of your customer base. The loyalty you counted on couldn't compete with the convenience AI provided. By 2030, your revenue had declined to the point where keeping all five employees was no longer viable.</p>

<p>Your resistance to digital tools became increasingly costly. As your customer base shrank, your operational efficiency declined because you were doing the same administrative work for fewer customers. Your fixed costs remained constant while your revenue dropped. You had to cut employee hours, then eliminate positions. Your remaining employees, watching the business decline and their hours cut, began seeking more stable employment elsewhere. The best of your team left first, leaving you with less experienced staff who couldn't deliver the same quality. That quality advantage you'd relied on for years deteriorated. Your business went from thriving to struggling, a spiral that would take years to reverse if it could be reversed at all. By 2030, you were in a fundamentally weakened position.</p>

<p><strong>Scenario 2: The Service Provider Squeezed Out by Platforms</strong><br/>
You provided a local service in {n}: repair, consulting, specialized labor. AI-powered platforms aggregated service providers and gave consumers transparent pricing, reviews, and instant booking. You weren't on the platforms because you had never needed them&mdash;your business ran on word of mouth. But by 2028, consumers in {n} were using platforms first and calling you only when the platform couldn't deliver. Your phone stopped ringing as often. When you finally joined the platform, you were one of dozens of providers with no reviews and no track record. Rebuilding your reputation in the new digital marketplace took time you didn't have.</p>

<p>By joining the platform late, you faced a two-year deficit. Your competitors had built strong review profiles and established themselves as the platform's preferred providers. You were starting from zero reputation in a marketplace where algorithm visibility depends on ratings. You had to take lower-paying jobs to build reviews quickly. You had to undercut pricing to stay competitive. Even then, customers preferred established providers with proven track records. The platform that should have been a distribution channel became a barrier to entry. The early movers on platforms were thriving. You were struggling to get customers through a mechanism that should have served you. By 2030, you were earning less than before joining, trapped in a platform marketplace where all the advantage had already been captured by early movers.</p>

<p><strong>Scenario 3: The Business Owner Overwhelmed and Frozen by Tech Choices</strong><br/>
You knew you needed to adopt AI tools but didn't know where to start. The options were overwhelming: chatbots, marketing automation, inventory management, AI accounting. You tried one tool, couldn't figure it out, and abandoned it. You tried another with the same result. After spending money on tools you couldn't use, you concluded that AI wasn't for businesses your size. That conclusion was wrong&mdash;the tools were accessible, but you needed a simpler starting point and basic support. By 2030, the businesses that started with one simple AI tool and built from there had transformed. You had not.</p>

<p>Your paralysis in the face of too many options cost you years of competitive advantage. While your competitors were steadily building digital capabilities, compounding small wins into business advantage, you were still discussing whether you should adopt tools. The money you spent experimenting with tools you couldn't use was wasted. The time you spent is gone. By 2030, your competitors had five years of AI-enhanced operations and learning. You had tried tools, failed, and given up. The gap in capability and efficiency between you and successful competitors had become enormous. Catching up would now require hiring expertise or investing significant time in learning, both of which your declining business could less afford.</p>

<h2>THE BULL CASE: The Same Three Owners Who Found Their Path</h2>

<p><strong>Scenario 1: The {ind1} Business That Went Digital-First</strong><br/>
Same business, different response. In 2025, you attended a small business digital workshop. You learned to use a basic AI-powered customer management tool. Within three months, you had automated appointment scheduling, follow-up messages, and inventory tracking. Your five employees spent less time on administration and more time on skilled work. Customer satisfaction improved because nothing fell through the cracks. By 2028&mdash;when your Bear Case counterpart was losing customers&mdash;you were gaining them, because your service was both personal (your team's expertise) and efficient (AI-powered operations). Revenue grew 25% between 2025 and 2030.</p>

<p>Your early digital adoption transformed your competitive position. You could serve customers faster, with fewer administrative mistakes, at better prices because efficiency improved your margins. Your customers appreciated the convenience and reliability. Word of mouth, once your primary marketing, was now amplified by digital channels. Your team, spending less time on administrative work, felt more satisfied with their jobs and stayed longer, building institutional knowledge that made service even better. By 2030, you weren't just surviving; you were growing. Your revenue growth, combined with operational efficiency, meant you were earning significantly more at a business level than you had in 2025, despite operating in a market with more competition.</p>

<p><strong>Scenario 2: The Service Provider Who Mastered the Platform</strong><br/>
You joined the service platform early, built a strong review profile through excellent work, and used the platform's AI tools to optimize your pricing and availability. By 2027, you were the top-rated provider in your category in your area. The platform funneled customers to you. Your revenue grew 40% while your competitors scrambled to establish presence. You learned that platforms weren't threats&mdash;they were distribution channels. The businesses that joined early and performed well captured disproportionate market share.</p>

<p>Your early platform adoption positioned you as the category leader in your market. New customers searching for your service found you first because of your ratings and reviews. The platform's algorithm actively directed customers to highly-rated providers. You went from fighting for customers through word-of-mouth to having customers come to you through the platform. Your volume increased, which improved your efficiency and allowed better pricing. By 2030, you had more business than you could personally handle, so you hired employees and expanded, building a company rather than a solo practice. The platform that seemed threatening in 2025 became your path to scaling and business growth.</p>

<p><strong>Scenario 3: The Owner Who Started Simple and Built Systematically</strong><br/>
Instead of trying to adopt every AI tool at once, you started with one: a free AI assistant for writing customer communications and marketing posts. It took an hour to learn. Within a week, you were creating professional marketing content in a fraction of the time. Emboldened, you added AI accounting. Then AI scheduling. Each tool was simple. Each saved time. By 2028, your small business operated with the efficiency of a company twice its size. The key was starting with one tool you could understand, mastering it, and then adding the next.</p>

<p>Your systematic approach to technology adoption created compound improvements in your business. Each tool saved time, which you reinvested in learning the next tool or in business development. Your first tool saved 3 hours per week. Your second tool saved 4 more hours. By 2030, you'd saved 15 hours per week&mdash;equivalent to nearly two full-time employees worth of time. You were running a business that would have required two additional employees in 2025, with the same employee count. That efficiency difference was the difference between struggling and prospering. By 2030, you had the operational capacity of a much larger business, the financial benefit of much higher efficiency, and the market advantage that came from being able to serve customers faster and better than less-efficient competitors.</p>

<h2>THE CRITICAL ADVANTAGE: The Window and When It Opened/Closed</h2>

<p>The small business owners who thrived in {n} were those who made the connection between digital tools and competitive advantage in 2025&ndash;2026, before the market had fully digitized. They had time to learn, experiment, refine, and build capabilities. The owners who delayed until 2027&ndash;2028, when the need was obvious, found all the advantage already captured by early movers. The owners who delayed until 2029&ndash;2030 found themselves in a market where digital excellence was the minimum to survive, not an advantage. The window for early mover advantage was real, limited, and largely closed by 2028.</p>

<h2>WHAT YOU SHOULD DO NOW</h2>

<p><strong>1. Start with One Free AI Tool This Week Without Overthinking It</strong><br/>
Pick the simplest one available: an AI writing assistant for business communications (like ChatGPT or free alternatives), an AI scheduling tool, or a basic chatbot for customer inquiries. Don't research endlessly; don't wait for the perfect tool; don't try to understand everything first. Try one tool for free and learn by doing. At a business income of {sal}, time saved is money earned. Even an hour per week saved is 50 hours per year that you can redirect to strategy or rest. Use that hour to experiment with your chosen tool. You're not trying to become an AI expert; you're trying to solve one specific problem. Choose a tool you can learn in an hour and actually use tomorrow.</p>

<p><strong>2. Automate Your Most Time-Consuming Administrative Task Immediately</strong><br/>
Identify the back-office task that consumes the most time and causes the most frustration: invoicing, scheduling, inventory tracking, customer follow-up, email responses. Find an AI tool for that specific task. The return is immediate: hours saved per week that you can redirect to revenue-generating work or personal time. If you currently spend 5 hours per week on invoicing, an AI accounting tool might cut that to 1 hour. That's 4 extra hours per week, 200 hours per year, that you now have for growing your business or enjoying your life. Calculate the monetary value of those hours. That's the ROI on the tool. Most small business owners will find the math is overwhelming in favor of automation.</p>

<p><strong>3. Establish a Strong Digital Presence This Quarter</strong><br/>
If your business isn't online&mdash;on platforms, social media, or a basic website&mdash;you are invisible to a growing and increasingly large segment of customers in {n}. Especially younger customers and those from outside your immediate neighborhood. AI tools make creating digital presence faster and cheaper than ever. You don't need a complex website; you need to be findable. Start with the platform most relevant to your business: Google Business if you're local, a Facebook page, Instagram if you're visual, LinkedIn if you're B2B, or a service platform if your industry has one. Get listed. Get reviews. Be discoverable.</p>

<p><strong>4. Join a Service Platform Now if One Exists in Your Industry</strong><br/>
If a service platform exists in your industry in {n}&mdash;a platform that aggregates providers and connects them to customers&mdash;join it immediately. The competition for top ratings is still manageable compared to 2032, but it's getting worse every month. Early movers on platforms capture disproportionate customer attention and trust. By 2030, customers in {n} search platforms first and call directly second (if at all). If you're not on the platform, you're missing customers. Join now, maintain quality so you get good reviews, and let the platform's AI algorithms direct customers to you. Don't wait for your competitors to establish dominance on the platform.</p>

<p><strong>5. Invest in Your Own Digital Literacy Immediately and Continuously</strong><br/>
The business owner who understands AI tools makes better decisions about which ones to adopt and how to use them effectively. Invest a few hours per week in your own digital literacy starting now. Attend a free workshop this month, watch tutorials, practice with tools. Encourage your employees to do the same. Pay for training if you can; at minimum, support their learning time. The small businesses that thrived in {n} between 2025 and 2030 were led by owners who learned alongside their teams, who weren't afraid of tools, and who saw technology as an opportunity rather than a threat. Model that attitude for your team.</p>

<h2>THE BOTTOM LINE</h2>

<p>Small business survival in {n}'s AI economy between 2025 and 2030 came down to a single question: did you start adopting AI tools before your competitors did? The answer didn't require massive investment or technical expertise. It required willingness to start, patience to learn, and consistency to keep building. The businesses that started with one simple AI tool in 2025 were transformed by 2030. They saved time, reduced costs, improved service, and grew revenue. Those that waited were diminished by competition from businesses that had moved ahead. The tools exist today, many at no cost. The market is still forming in 2030, but advantage is increasingly going to those who moved early. The only real barrier is starting. Start this week. Choose one tool. Try it. See what happens. The worst that happens is you learn something. The best that happens is you transform your business.</p>

<p>If you're reading this in 2030 and haven't yet made significant AI adoption, the urgency is now critical. The window for leisurely experimentation is closed. Your competitors are not just ahead; they're entrenched in advantages you'll struggle to overcome. You can still catch up, but it will require faster, more aggressive adoption than early movers needed. You have perhaps two years before the competitive advantage differential becomes permanent. Use those two years to close the gap. Start with one tool this week. Then move to the next. Build systematically, but build quickly. Your business depends on it.</p>"""

    return body
def gen_refs_html(refs):
    if not refs: return ""
    h = '<div class="references-section"><h2>References &amp; Sources</h2><ol>\n'
    for t, u in refs:
        h += f'<li><a href="{html.escape(u)}" target="_blank" rel="noopener">{html.escape(t)}</a></li>\n'
    return h + '</ol></div>'


def gen_article(c, aud, filename):
    """Generate complete HTML article."""
    name = c["name"]
    aud_title = AUDIENCE_TITLES[aud]
    aud_desc = AUDIENCE_DESCS[aud]
    title = f"Bear Case vs Bull Case: AI's Impact on {name} by 2030 — {aud_title} | The 2030 Intelligence Report"
    og_title = f"AI 2030: {name} — Bear Case vs Bull Case ({aud_title})"
    og_desc_template = AUDIENCE_DESCS[aud]
    og_desc = og_desc_template.replace("{country}", name) if "{country}" in og_desc_template else f"{og_desc_template} — {name}"
    url = f"https://ai2030report.com/{filename}"
    og_img = f"https://ai2030report.com/{filename.replace('articles/','og/').replace('.html','.png')}"

    body = gen_content(c, aud)
    refs = gen_refs_html(c.get("references", []))

    # Sibling pills
    pills = ""
    for a in AUDIENCES:
        act = ' active' if a == aud else ''
        lab = AUDIENCE_TITLES[a].split(" & ")[0]
        sib = filename.replace(f"-{aud}-edition", f"-{a}-edition")
        pills += f'<a href="/{sib}" class="sibling-pill{act}">{lab}</a>\n'

    share_url = url
    li_url = f"https://www.linkedin.com/sharing/share-offsite/?url={share_url}"
    tw_url = f"https://twitter.com/intent/tweet?url={share_url}&text=AI+2030+{name}"
    wa_url = f"https://wa.me/?text=AI+2030+{name}+{share_url}"

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(og_desc[:160])}">
<meta property="og:title" content="{html.escape(og_title)}">
<meta property="og:description" content="{html.escape(og_desc[:160])}">
<meta property="og:type" content="article">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{og_img}">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{html.escape(og_title)}">
<meta name="twitter:description" content="{html.escape(og_desc[:160])}">
<meta name="twitter:image" content="{og_img}">
<link rel="canonical" href="{url}">
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"Article","headline":"{html.escape(og_title)}","description":"{html.escape(og_desc[:160])}","url":"{url}","datePublished":"2025-03-01","dateModified":"2026-03-03","author":{{"@type":"Organization","name":"The 2030 Intelligence Report"}},"publisher":{{"@type":"Organization","name":"The 2030 Intelligence Report"}}}}
</script>
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"Home","item":"https://ai2030report.com/"}},{{"@type":"ListItem","position":2,"name":"Countries","item":"https://ai2030report.com/browse/countries.html"}},{{"@type":"ListItem","position":3,"name":"{html.escape(name)}","item":"{url}"}}]}}
</script>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-S9Z93KZ2Z2"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('js',new Date());gtag('config','G-S9Z93KZ2Z2');</script>
{get_css()}
</head>
<body>
<div class="reading-progress" id="readingProgress"></div>
<header class="site-header"><div class="header-inner">
<a href="/" class="site-logo">The 2030 Intelligence Report</a>
<nav><ul class="nav-links">
<li><a href="/">Home</a></li><li><a href="/browse/countries.html">Countries</a></li>
<li><a href="/browse/sectors.html">Sectors</a></li><li><a href="/methodology.html">Methodology</a></li>
<li><a href="/about.html">About</a></li></ul>
<button class="nav-toggle" aria-label="Toggle navigation"><span></span><span></span><span></span></button>
</nav><button class="theme-toggle" id="themeToggle" title="Toggle theme">&#9788;</button>
</div></header>
<div class="mobile-overlay" id="mobileOverlay"></div>
<nav class="breadcrumb"><a href="/">Home</a> <span>&rsaquo;</span> <a href="/browse/countries.html">Countries</a> <span>&rsaquo;</span> <a href="#">{html.escape(name)}</a> <span>&rsaquo;</span> <span>{html.escape(aud_title)}</span></nav>
<div class="article-header"><div class="article-meta">
<span class="meta-badge badge-country">{html.escape(name)}</span>
<span class="meta-badge badge-audience">{html.escape(aud_title)}</span>
<span class="meta-badge badge-date">Updated March 2026</span>
</div></div>
<div class="sibling-editions"><h3>View other perspectives:</h3><div class="sibling-pills">{pills}</div></div>
<article class="article-content">
{body}
<div class="social-share-bar"><span>Share:</span>
<a href="{li_url}" target="_blank" rel="noopener" class="share-btn linkedin">LinkedIn</a>
<a href="{tw_url}" target="_blank" rel="noopener" class="share-btn twitter">X / Twitter</a>
<a href="{wa_url}" target="_blank" rel="noopener" class="share-btn whatsapp">WhatsApp</a>
<button class="share-btn copy-link" onclick="navigator.clipboard.writeText('{share_url}');this.textContent='Copied!'">Copy Link</button>
</div>
{refs}
<div class="email-capture"><h3>Get AI Disruption Alerts for {html.escape(name)}</h3>
<p>Monthly updates on AI reshaping {html.escape(name)}'s economy</p>
<form class="email-capture-form" onsubmit="event.preventDefault();this.innerHTML='<p style=color:var(--accent-green)>Thank you!</p>'">
<input type="email" placeholder="Your email" required><button type="submit">Subscribe</button></form></div>
<div class="feedback-bar">
<a href="mailto:feedback@ai2030report.com?subject=Feedback:{html.escape(name)}+{html.escape(aud_title)}">&#9993; Send Feedback</a>
<a href="https://twitter.com/intent/tweet?text=AI+analysis+of+{html.escape(name)}+{share_url}" target="_blank">&#128172; Discuss</a>
</div></article>
<footer class="site-footer"><p>&copy; 2025-2026 The 2030 Intelligence Report. Data-driven AI disruption forecasts.</p></footer>
<button class="scroll-top" id="scrollTop" onclick="window.scrollTo({{top:0,behavior:'smooth'}})">&#8593;</button>
<script>
window.addEventListener('scroll',function(){{var h=document.documentElement,b=document.body;var pct=(h.scrollTop||b.scrollTop)/((h.scrollHeight||b.scrollHeight)-h.clientHeight)*100;document.getElementById('readingProgress').style.width=pct+'%';document.getElementById('scrollTop').style.display=pct>20?'flex':'none'}});
(function(){{var t=document.getElementById('themeToggle');if(localStorage.getItem('theme')==='light')document.documentElement.classList.add('light-theme');t.addEventListener('click',function(){{document.documentElement.classList.toggle('light-theme');localStorage.setItem('theme',document.documentElement.classList.contains('light-theme')?'light':'dark')}});}})();
(function(){{var tog=document.querySelector('.nav-toggle'),nav=document.querySelector('.nav-links'),ov=document.getElementById('mobileOverlay');if(tog)tog.addEventListener('click',function(){{nav.classList.toggle('active');ov.classList.toggle('active');document.body.classList.toggle('nav-open')}});if(ov)ov.addEventListener('click',function(){{nav.classList.remove('active');ov.classList.remove('active');document.body.classList.remove('nav-open')}});}})();
</script>
</body></html>"""


def rewrite_country(key):
    c = COUNTRIES[key]
    slug = c["slug"]
    count = 0

    # Find existing files using full slug match (not partial prefix)
    existing = {}
    slug_parts = slug.split("-")
    for f in os.listdir(ARTICLES_DIR):
        if not f.endswith(".html"): continue
        fl = f.lower()
        # Match files that contain the full country slug
        if f"countries-{slug}-" in fl or f"countries-{slug_parts[0]}-" in fl:
            for aud in AUDIENCES:
                if f"-{aud}-edition.html" in fl:
                    existing[aud] = os.path.join(ARTICLES_DIR, f)

    for aud in AUDIENCES:
        # Always write to canonical path
        fn = os.path.join(ARTICLES_DIR, f"countries-{slug}-{aud}-edition.html")
        with open(fn, 'w', encoding='utf-8') as f:
            f.write(gen_article(c, aud, fn))
        count += 1
    print(f"  ✓ {c['name']}: {count} articles")
    return count


def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    total = 0
    for key in COUNTRIES:
        total += rewrite_country(key)
    print(f"\nDone! {total} articles rewritten.")

if __name__ == "__main__":
    main()
