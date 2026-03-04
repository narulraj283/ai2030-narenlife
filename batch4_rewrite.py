#!/usr/bin/env python3
"""Batch 4: Vietnam, Thailand, Malaysia, Morocco, Peru, Chile, Uganda, Ghana, Nepal, Cambodia"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from batch2_rewrite import gen_article, AUDIENCES, ARTICLES_DIR

COUNTRIES = {
    "vietnam": {
        "name": "Vietnam", "slug": "vietnam-vietnam", "population": "101 million",
        "gdp_per_capita": "$4,700", "gdp_per_capita_ppp": "$15,000", "gdp_growth": "8.0%",
        "currency": "VND", "avg_monthly_salary": "VND 8,300,000 (~$317 USD)",
        "avg_salary_usd": "$317", "minimum_wage": "VND 4,960,000/month (Region I, 2025)",
        "it_salary_range": "VND 15M-50M/month; senior VND 50M-100M+ ($600-4,000 USD)",
        "manufacturing_salary": "VND 6M-10M/month (~$230-385 USD)",
        "unemployment": "2.2%", "ai_adoption": "Growing rapidly; FDI in tech manufacturing (Samsung, Intel); digital economy $36B",
        "internet_penetration": "75%", "literacy_rate": "95%", "stem_graduates": "~200,000 annually",
        "labor_force": "56 million",
        "key_industries": "Electronics manufacturing (Samsung), textiles/garments, agriculture (rice, coffee), seafood, tourism, IT outsourcing",
        "ai_risk_high": "Textile/garment assembly, electronics assembly, data entry, call centers",
        "ai_risk_medium": "Banking, agriculture processing, manufacturing, logistics",
        "ai_risk_low": "Agriculture, tourism, healthcare, education, construction, skilled trades",
        "key_challenges": "Rapid industrialization requiring labor standard improvements, skill gaps in advanced manufacturing, infrastructure bottlenecks, climate vulnerability (Mekong Delta flooding)",
        "references": [("World Bank - Vietnam", "https://www.worldbank.org/en/country/vietnam/overview"), ("GSO Vietnam", "https://www.gso.gov.vn/en/"), ("Trading Economics - Vietnam", "https://tradingeconomics.com/vietnam/indicators")]
    },
    "thailand": {
        "name": "Thailand", "slug": "thailand-thailand", "population": "72 million",
        "gdp_per_capita": "$7,942", "gdp_per_capita_ppp": "$21,800", "gdp_growth": "2.5%",
        "currency": "THB", "avg_monthly_salary": "THB 15,738 (~$420 USD)",
        "avg_salary_usd": "$420", "minimum_wage": "THB 337-400/day (varies by province, 2025)",
        "it_salary_range": "THB 30,000-100,000/month; senior THB 100,000-200,000+",
        "manufacturing_salary": "THB 12,000-20,000/month (~$320-535 USD)",
        "unemployment": "0.8% (extremely low)", "ai_adoption": "Moderate; Thailand 4.0 initiative; growing tech startup scene in Bangkok",
        "internet_penetration": "91%", "literacy_rate": "94%", "stem_graduates": "~120,000 annually",
        "labor_force": "40 million",
        "key_industries": "Automotive (ASEAN's largest), electronics, tourism, agriculture (rice, rubber), food processing, petrochemicals",
        "ai_risk_high": "Electronics assembly, basic manufacturing, customer service, data entry",
        "ai_risk_medium": "Automotive manufacturing, banking, logistics, agriculture processing",
        "ai_risk_low": "Tourism services, healthcare, education, agriculture, creative industries, construction",
        "key_challenges": "Political instability affecting investment, aging population, tourism volatility, middle-income trap, household debt at 91% of GDP",
        "references": [("World Bank - Thailand", "https://www.worldbank.org/en/country/thailand/overview"), ("NESDC Thailand", "https://www.nesdc.go.th/"), ("Trading Economics - Thailand", "https://tradingeconomics.com/thailand/indicators")]
    },
    "malaysia": {
        "name": "Malaysia", "slug": "malaysia-malaysia", "population": "36 million",
        "gdp_per_capita": "$11,868", "gdp_per_capita_ppp": "$35,200", "gdp_growth": "5.2%",
        "currency": "MYR", "avg_monthly_salary": "MYR 3,652 (~$780 USD)",
        "avg_salary_usd": "$780", "minimum_wage": "MYR 1,700/month (2025)",
        "it_salary_range": "MYR 4,000-15,000/month; senior MYR 15,000-30,000+",
        "manufacturing_salary": "MYR 2,000-3,500/month (~$428-750 USD)",
        "unemployment": "2.9%", "ai_adoption": "Growing; major data center hub (Google, Microsoft investing); semiconductor testing/packaging hub",
        "internet_penetration": "98%", "literacy_rate": "95%", "stem_graduates": "~100,000 annually",
        "labor_force": "17 million",
        "key_industries": "Semiconductors, palm oil, petroleum, electronics, Islamic finance, tourism, manufacturing",
        "ai_risk_high": "Electronics assembly, palm oil processing automation, call centers, data entry",
        "ai_risk_medium": "Banking/Islamic finance, manufacturing, logistics, plantation management",
        "ai_risk_low": "Healthcare, education, tourism, construction, oil & gas engineering",
        "key_challenges": "Income inequality, over-reliance on commodity exports, brain drain to Singapore, middle-income trap concerns, migrant worker dependency",
        "references": [("World Bank - Malaysia", "https://www.worldbank.org/en/country/malaysia/overview"), ("DOSM Malaysia", "https://www.dosm.gov.my/"), ("Trading Economics - Malaysia", "https://tradingeconomics.com/malaysia/indicators")]
    },
    "morocco": {
        "name": "Morocco", "slug": "morocco-morocco", "population": "37 million",
        "gdp_per_capita": "$4,298", "gdp_per_capita_ppp": "$10,200", "gdp_growth": "3.0%",
        "currency": "MAD", "avg_monthly_salary": "MAD 5,000 (~$500 USD)",
        "avg_salary_usd": "$500", "minimum_wage": "MAD 3,111/month (industry, 2025)",
        "it_salary_range": "MAD 8,000-25,000/month; offshoring center salaries",
        "manufacturing_salary": "MAD 3,111-5,000/month (~$310-500 USD)",
        "unemployment": "13.1%", "ai_adoption": "Growing; automotive manufacturing hub; nearshoring from Europe",
        "internet_penetration": "91%", "literacy_rate": "74%", "stem_graduates": "~60,000 annually",
        "labor_force": "12 million",
        "key_industries": "Phosphates (70% global reserves), automotive (Renault, Stellantis), agriculture, tourism, textiles, aerospace, offshoring/BPO",
        "ai_risk_high": "BPO/call centers (francophone), textile manufacturing, data entry",
        "ai_risk_medium": "Automotive assembly, banking, phosphate processing, logistics",
        "ai_risk_low": "Agriculture, tourism, healthcare, education, construction, artisanal crafts",
        "key_challenges": "Youth unemployment 30% for tertiary-educated, rural-urban divide, water scarcity, low literacy rate despite economic growth",
        "references": [("World Bank - Morocco", "https://www.worldbank.org/en/country/morocco/overview"), ("HCP Morocco", "https://www.hcp.ma/"), ("Trading Economics - Morocco", "https://tradingeconomics.com/morocco/indicators")]
    },
    "peru": {
        "name": "Peru", "slug": "peru-peru", "population": "34 million",
        "gdp_per_capita": "$8,650", "gdp_per_capita_ppp": "$16,600", "gdp_growth": "3.1% (2024)",
        "currency": "PEN", "avg_monthly_salary": "PEN 2,500 (~$650 USD)",
        "avg_salary_usd": "$650", "minimum_wage": "PEN 1,025/month (2024)",
        "it_salary_range": "PEN 3,000-12,000/month; senior PEN 12,000-25,000+",
        "manufacturing_salary": "PEN 1,200-2,500/month (~$310-650 USD)",
        "unemployment": "5.9%", "ai_adoption": "Low; growing fintech sector in Lima",
        "internet_penetration": "75%", "literacy_rate": "94%", "stem_graduates": "~50,000 annually",
        "labor_force": "18 million",
        "key_industries": "Mining (copper, gold, silver, zinc), agriculture, fishing, textiles, tourism, construction",
        "ai_risk_high": "Mining admin, data entry, basic financial services, textile manufacturing",
        "ai_risk_medium": "Banking, logistics, agriculture processing, mining operations",
        "ai_risk_low": "Mining engineering, tourism, healthcare, education, construction, agriculture",
        "key_challenges": "Political instability, mining sector volatility, large informal economy (70%+ of workers), inequality between Lima and provinces",
        "references": [("World Bank - Peru", "https://www.worldbank.org/en/country/peru/overview"), ("INEI Peru", "https://www.inei.gob.pe/"), ("Trading Economics - Peru", "https://tradingeconomics.com/peru/indicators")]
    },
    "chile": {
        "name": "Chile", "slug": "chile-chile", "population": "20 million",
        "gdp_per_capita": "$16,437", "gdp_per_capita_ppp": "$32,500", "gdp_growth": "2.4%",
        "currency": "CLP", "avg_monthly_salary": "CLP 700,000 (~$730 USD)",
        "avg_salary_usd": "$730", "minimum_wage": "CLP 519,333/month (2025)",
        "it_salary_range": "CLP 1.5M-4M/month; senior CLP 4M-8M+",
        "manufacturing_salary": "CLP 500,000-800,000/month (~$520-835 USD)",
        "unemployment": "8.4%", "ai_adoption": "Growing; strongest in Latin America per capita; Santiago tech hub",
        "internet_penetration": "88%", "literacy_rate": "97%", "stem_graduates": "~40,000 annually",
        "labor_force": "9.5 million",
        "key_industries": "Copper mining (world's largest producer), lithium, agriculture (wine, fruit), salmon, forestry, finance, solar energy",
        "ai_risk_high": "Mining admin, financial back-office, call centers, data entry",
        "ai_risk_medium": "Banking, logistics, agriculture processing, retail",
        "ai_risk_low": "Mining engineering, healthcare, education, wine production, renewable energy",
        "key_challenges": "High income inequality, pension system reform pressure, copper price volatility, water scarcity in north, social unrest legacy",
        "references": [("World Bank - Chile", "https://www.worldbank.org/en/country/chile/overview"), ("INE Chile", "https://www.ine.gob.cl/"), ("Trading Economics - Chile", "https://tradingeconomics.com/chile/indicators")]
    },
    "uganda": {
        "name": "Uganda", "slug": "uganda-uganda", "population": "46 million",
        "gdp_per_capita": "$1,353", "gdp_per_capita_ppp": "$3,100", "gdp_growth": "7.0%",
        "currency": "UGX", "avg_monthly_salary": "UGX 500,000 (~$130 USD)",
        "avg_salary_usd": "$130", "minimum_wage": "No statutory minimum wage (pending legislation)",
        "it_salary_range": "UGX 1.5M-5M/month (~$390-1,300 USD)",
        "manufacturing_salary": "UGX 300,000-600,000/month (~$78-156 USD)",
        "unemployment": "2.7% (official; high youth NEET 42.6%)", "ai_adoption": "Minimal; growing mobile money ecosystem",
        "internet_penetration": "27%", "literacy_rate": "74%", "stem_graduates": "~25,000 annually",
        "labor_force": "18 million",
        "key_industries": "Agriculture (coffee, tea, tobacco), oil (emerging), services, construction, manufacturing, tourism",
        "ai_risk_high": "Basic admin, data entry, telecom customer service",
        "ai_risk_medium": "Banking/mobile money, agriculture processing",
        "ai_risk_low": "Agriculture, tourism, healthcare, education, construction, oil extraction",
        "key_challenges": "Youth unemployment (42.6% NEET), very low internet penetration, limited infrastructure, emerging oil sector needs governance, population growth straining services",
        "references": [("World Bank - Uganda", "https://www.worldbank.org/en/country/uganda/overview"), ("UBOS Uganda", "https://www.ubos.org/"), ("Trading Economics - Uganda", "https://tradingeconomics.com/uganda/indicators")]
    },
    "ghana": {
        "name": "Ghana", "slug": "ghana-ghana", "population": "34 million",
        "gdp_per_capita": "$2,363", "gdp_per_capita_ppp": "$6,800", "gdp_growth": "4.5%",
        "currency": "GHS", "avg_monthly_salary": "GHS 3,500 (~$250 USD)",
        "avg_salary_usd": "$250", "minimum_wage": "GHS 18.15/day; ~GHS 490/month (2025)",
        "it_salary_range": "GHS 3,000-12,000/month (~$210-850 USD)",
        "manufacturing_salary": "GHS 1,500-3,000/month (~$106-210 USD)",
        "unemployment": "3.0%", "ai_adoption": "Growing; Accra emerging as West African tech hub; Google AI Research Center",
        "internet_penetration": "65%", "literacy_rate": "72%", "stem_graduates": "~30,000 annually",
        "labor_force": "14 million",
        "key_industries": "Gold mining, cocoa, oil, agriculture, services, fintech, manufacturing",
        "ai_risk_high": "Call centers, data entry, basic admin, cocoa processing automation",
        "ai_risk_medium": "Banking/fintech operations, mining admin, logistics",
        "ai_risk_low": "Agriculture, healthcare, education, tourism, artisanal mining, construction",
        "key_challenges": "Inflation falling but above target (11.1%), debt restructuring aftermath (2023 default), cedi depreciation, power sector challenges, youth unemployment",
        "references": [("World Bank - Ghana", "https://www.worldbank.org/en/country/ghana/overview"), ("GSS Ghana", "https://statsghana.gov.gh/"), ("Trading Economics - Ghana", "https://tradingeconomics.com/ghana/indicators")]
    },
    "nepal": {
        "name": "Nepal", "slug": "nepal-nepal", "population": "30 million",
        "gdp_per_capita": "$1,447", "gdp_per_capita_ppp": "$4,800", "gdp_growth": "6.1%",
        "currency": "NPR", "avg_monthly_salary": "NPR 25,000 (~$185 USD)",
        "avg_salary_usd": "$185", "minimum_wage": "NPR 17,300/month (2024)",
        "it_salary_range": "NPR 30,000-100,000/month (~$220-740 USD)",
        "manufacturing_salary": "NPR 17,300-25,000/month (~$128-185 USD)",
        "unemployment": "11.4%", "ai_adoption": "Minimal; growing IT freelancer community",
        "internet_penetration": "42%", "literacy_rate": "67%", "stem_graduates": "~20,000 annually",
        "labor_force": "8 million (many working abroad; remittances 25% of GDP)",
        "key_industries": "Agriculture, tourism (Himalayas), hydropower, remittances, garments, carpets",
        "ai_risk_high": "Data entry, basic admin, garment assembly",
        "ai_risk_medium": "Banking, telecom, agriculture processing",
        "ai_risk_low": "Tourism, healthcare, education, construction, hydropower, agriculture",
        "key_challenges": "Extreme poverty (20%), limited infrastructure, brain drain (4M+ workers abroad), earthquake vulnerability, landlocked geography limiting trade",
        "references": [("World Bank - Nepal", "https://www.worldbank.org/en/country/nepal/overview"), ("CBS Nepal", "https://cbs.gov.np/"), ("Trading Economics - Nepal", "https://tradingeconomics.com/nepal/indicators")]
    },
    "cambodia": {
        "name": "Cambodia", "slug": "cambodia-cambodia", "population": "17 million",
        "gdp_per_capita": "$2,754", "gdp_per_capita_ppp": "$6,100", "gdp_growth": "4.8%",
        "currency": "KHR", "avg_monthly_salary": "$300-400 USD (heavily dollarized economy)",
        "avg_salary_usd": "$300-400", "minimum_wage": "$208/month (garment sector, 2025)",
        "it_salary_range": "$400-1,500/month; senior $1,500-3,000+",
        "manufacturing_salary": "$208-350/month (garment and light manufacturing)",
        "unemployment": "0.5% (very low; large informal economy)", "ai_adoption": "Very low; growing digital payments",
        "internet_penetration": "64%", "literacy_rate": "84%", "stem_graduates": "~15,000 annually",
        "labor_force": "10 million",
        "key_industries": "Garments (70% of exports), tourism, agriculture (rice), construction, real estate, light manufacturing",
        "ai_risk_high": "Garment assembly (700,000+ workers), data entry, basic admin",
        "ai_risk_medium": "Banking, tourism operations, agriculture processing",
        "ai_risk_low": "Agriculture, construction, tourism services, healthcare, education",
        "key_challenges": "Over-dependence on garments and Chinese investment, governance concerns, deforestation, rising household debt, limited social safety net",
        "references": [("World Bank - Cambodia", "https://www.worldbank.org/en/country/cambodia/overview"), ("NIS Cambodia", "https://www.nis.gov.kh/"), ("Trading Economics - Cambodia", "https://tradingeconomics.com/cambodia/indicators")]
    },
}

def rewrite_country(key):
    c = COUNTRIES[key]
    slug = c["slug"]
    count = 0
    existing = {}
    for f in os.listdir(ARTICLES_DIR):
        if not f.endswith(".html"): continue
        for aud in AUDIENCES:
            if f"-{aud}-edition.html" in f:
                cp = slug.split("-")[0]
                if cp in f.lower():
                    existing[aud] = os.path.join(ARTICLES_DIR, f)
    for aud in AUDIENCES:
        fn = existing.get(aud, os.path.join(ARTICLES_DIR, f"countries-{slug}-{aud}-edition.html"))
        with open(fn, 'w', encoding='utf-8') as f:
            f.write(gen_article(c, aud, fn))
        count += 1
    print(f"  ✓ {c['name']}: {count} articles")
    return count

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    total = sum(rewrite_country(k) for k in COUNTRIES)
    print(f"\nDone! {total} articles rewritten.")
