#!/usr/bin/env python3
"""Batch 5: Mozambique, Angola, Myanmar, Afghanistan, Uzbekistan, Romania, Switzerland, New Zealand, Iraq, Jordan"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from batch2_rewrite import gen_article, AUDIENCES, ARTICLES_DIR

COUNTRIES = {
    "mozambique": {
        "name": "Mozambique", "slug": "mozambique-mozambique", "population": "35 million",
        "gdp_per_capita": "$603", "gdp_per_capita_ppp": "$1,500", "gdp_growth": "1.8%",
        "currency": "MZN", "avg_monthly_salary": "MZN 8,000 (~$125 USD)",
        "avg_salary_usd": "$125", "minimum_wage": "MZN 5,500-8,800/month (varies by sector)",
        "it_salary_range": "MZN 25,000-80,000/month (~$390-1,250 USD)",
        "manufacturing_salary": "MZN 5,500-10,000/month (~$86-156 USD)",
        "unemployment": "3.5%", "ai_adoption": "Minimal; very limited digital infrastructure",
        "internet_penetration": "22%", "literacy_rate": "63%", "stem_graduates": "~10,000 annually",
        "labor_force": "14 million",
        "key_industries": "Agriculture, mining (coal, gas), aluminum smelting, fishing, tourism, LNG (emerging)",
        "ai_risk_high": "Administrative services, basic data processing",
        "ai_risk_medium": "Banking, mining operations, telecom",
        "ai_risk_low": "Agriculture, fishing, construction, healthcare, education, LNG extraction",
        "key_challenges": "Growth subdued below population growth rate, insurgency in northern Cabo Delgado, LNG project delays, climate vulnerability (cyclones), debt crisis aftermath",
        "references": [("World Bank - Mozambique", "https://www.worldbank.org/en/country/mozambique/overview"), ("INE Mozambique", "https://www.ine.gov.mz/"), ("Trading Economics - Mozambique", "https://tradingeconomics.com/mozambique/indicators")]
    },
    "angola": {
        "name": "Angola", "slug": "angola-angola", "population": "37 million",
        "gdp_per_capita": "$2,931", "gdp_per_capita_ppp": "$7,800", "gdp_growth": "4.4%",
        "currency": "AOA", "avg_monthly_salary": "AOA 150,000 (~$175 USD)",
        "avg_salary_usd": "$175", "minimum_wage": "AOA 70,000/month (2024)",
        "it_salary_range": "AOA 300,000-800,000/month (~$350-935 USD)",
        "manufacturing_salary": "AOA 80,000-150,000/month (~$94-175 USD)",
        "unemployment": "30% (estimated)", "ai_adoption": "Minimal; oil sector using some automation",
        "internet_penetration": "36%", "literacy_rate": "71%", "stem_graduates": "~15,000 annually",
        "labor_force": "14 million",
        "key_industries": "Oil & gas (90% of exports), diamonds, agriculture, fisheries, cement, construction",
        "ai_risk_high": "Oil sector admin, basic data processing, government bureaucracy",
        "ai_risk_medium": "Banking, telecom, mining operations",
        "ai_risk_low": "Agriculture, fishing, construction, healthcare, education, oil extraction",
        "key_challenges": "Oil-dependent economy with declining production, high unemployment (~30%), limited economic diversification, infrastructure gaps, corruption",
        "references": [("World Bank - Angola", "https://www.worldbank.org/en/country/angola/overview"), ("INE Angola", "https://www.ine.gov.ao/"), ("Trading Economics - Angola", "https://tradingeconomics.com/angola/indicators")]
    },
    "myanmar": {
        "name": "Myanmar", "slug": "myanmar-myanmar", "population": "58 million",
        "gdp_per_capita": "$1,122", "gdp_per_capita_ppp": "$4,800", "gdp_growth": "-1.0% (contraction)",
        "currency": "MMK", "avg_monthly_salary": "MMK 250,000 (~$120 USD)",
        "avg_salary_usd": "$120", "minimum_wage": "MMK 4,800/day (2024)",
        "it_salary_range": "Very limited; $200-600/month where available",
        "manufacturing_salary": "MMK 150,000-250,000/month (~$72-120 USD)",
        "unemployment": "High (data unreliable due to conflict)", "ai_adoption": "Effectively zero; infrastructure destroyed",
        "internet_penetration": "49%", "literacy_rate": "93%", "stem_graduates": "Severely disrupted",
        "labor_force": "23 million (significantly disrupted by coup)",
        "key_industries": "Agriculture, natural gas, mining, timber, garments, jade",
        "ai_risk_high": "N/A - economy in crisis; recovery is priority",
        "ai_risk_medium": "Telecom (when restored), basic banking",
        "ai_risk_low": "Agriculture, construction, healthcare, education (all disrupted)",
        "key_challenges": "Military coup (Feb 2021) causing economic contraction, humanitarian crisis, Western sanctions, infrastructure destruction, massive displacement",
        "references": [("World Bank - Myanmar", "https://www.worldbank.org/en/country/myanmar/overview"), ("Trading Economics - Myanmar", "https://tradingeconomics.com/myanmar/indicators")]
    },
    "afghanistan": {
        "name": "Afghanistan", "slug": "afghanistan-afghanistan", "population": "40 million",
        "gdp_per_capita": "$417", "gdp_per_capita_ppp": "$2,300", "gdp_growth": "1.7%",
        "currency": "AFN", "avg_monthly_salary": "AFN 15,000 (~$210 USD)",
        "avg_salary_usd": "$210", "minimum_wage": "AFN 6,000/month (~$83 USD, 2024)",
        "it_salary_range": "Very limited; $150-400/month where available",
        "manufacturing_salary": "AFN 8,000-15,000/month (~$111-210 USD)",
        "unemployment": "High (data unreliable)", "ai_adoption": "Essentially zero",
        "internet_penetration": "29%", "literacy_rate": "37%", "stem_graduates": "Severely limited; women banned from education",
        "labor_force": "9 million (women largely excluded since Taliban takeover)",
        "key_industries": "Agriculture, natural resources, handicrafts, services (all severely impacted)",
        "ai_risk_high": "N/A - basic economic recovery is the priority",
        "ai_risk_medium": "N/A",
        "ai_risk_low": "Agriculture, construction, healthcare (all face severe constraints)",
        "key_challenges": "Taliban governance reducing international investment, women banned from education and most employment, humanitarian crisis, 37% literacy rate, international isolation",
        "references": [("World Bank - Afghanistan", "https://www.worldbank.org/en/country/afghanistan/overview"), ("Trading Economics - Afghanistan", "https://tradingeconomics.com/afghanistan/indicators")]
    },
    "uzbekistan": {
        "name": "Uzbekistan", "slug": "uzbekistan-uzbekistan", "population": "37 million",
        "gdp_per_capita": "$3,093", "gdp_per_capita_ppp": "$10,400", "gdp_growth": "6.5%",
        "currency": "UZS", "avg_monthly_salary": "UZS 4,500,000 (~$360 USD)",
        "avg_salary_usd": "$360", "minimum_wage": "UZS 1,050,000/month (~$84 USD)",
        "it_salary_range": "UZS 5M-20M/month (~$400-1,600 USD)",
        "manufacturing_salary": "UZS 2M-4M/month (~$160-320 USD)",
        "unemployment": "6.0%", "ai_adoption": "Low; government digitalization program underway",
        "internet_penetration": "85%", "literacy_rate": "100%", "stem_graduates": "~80,000 annually",
        "labor_force": "19 million",
        "key_industries": "Natural gas, cotton, gold, mining, agriculture, textiles, automotive (Chevrolet/UzAuto)",
        "ai_risk_high": "Cotton processing, administrative services, basic data entry",
        "ai_risk_medium": "Banking, telecom, manufacturing, mining operations",
        "ai_risk_low": "Agriculture, construction, healthcare, education, gas extraction",
        "key_challenges": "Economic transition from central planning, commodity dependence, labor migration (millions work abroad), water scarcity (Aral Sea), governance reforms ongoing",
        "references": [("World Bank - Uzbekistan", "https://www.worldbank.org/en/country/uzbekistan/overview"), ("Trading Economics - Uzbekistan", "https://tradingeconomics.com/uzbekistan/indicators")]
    },
    "romania": {
        "name": "Romania", "slug": "romania-romania", "population": "19 million",
        "gdp_per_capita": "$20,209", "gdp_per_capita_ppp": "$43,600", "gdp_growth": "0.9%",
        "currency": "RON", "avg_monthly_salary": "RON 8,355 net (~$1,865 USD)",
        "avg_salary_usd": "$1,865", "minimum_wage": "RON 3,700/month gross (2025)",
        "it_salary_range": "RON 10,000-30,000/month net (~$2,200-6,700 USD); Romania is major IT hub",
        "manufacturing_salary": "RON 4,000-6,000/month (~$890-1,340 USD)",
        "unemployment": "5.4%", "ai_adoption": "Growing; strong IT outsourcing sector; Cluj-Napoca, Bucharest tech hubs",
        "internet_penetration": "85%", "literacy_rate": "98%", "stem_graduates": "~50,000 annually",
        "labor_force": "9 million",
        "key_industries": "IT services, automotive (Dacia/Renault), agriculture, machinery, textiles, energy, tourism",
        "ai_risk_high": "BPO/outsourcing, data entry, basic manufacturing, customer service",
        "ai_risk_medium": "Automotive manufacturing, banking, logistics",
        "ai_risk_low": "Healthcare, education, agriculture, IT development, tourism, skilled trades",
        "key_challenges": "Infrastructure gaps, wage disparities driving emigration to Western Europe despite strong IT sector, population decline, fiscal deficit concerns",
        "references": [("World Bank - Romania", "https://data.worldbank.org/country/romania"), ("INS Romania", "https://insse.ro/cms/en"), ("Trading Economics - Romania", "https://tradingeconomics.com/romania/indicators")]
    },
    "switzerland": {
        "name": "Switzerland", "slug": "switzerland-switzerland", "population": "9 million",
        "gdp_per_capita": "$104,520", "gdp_per_capita_ppp": "$87,400", "gdp_growth": "1.8%",
        "currency": "CHF", "avg_monthly_salary": "CHF 6,665 (~$7,500 USD)",
        "avg_salary_usd": "$7,500", "minimum_wage": "No national statutory minimum; Geneva CHF 24/hour; Neuchâtel CHF 21.09",
        "it_salary_range": "CHF 90,000-160,000/year; senior CHF 160,000-250,000+",
        "manufacturing_salary": "CHF 5,500-7,500/month (~$6,200-8,450 USD)",
        "unemployment": "2.9%", "ai_adoption": "High; ETH Zurich world-leading AI research; strong pharma/fintech AI adoption",
        "internet_penetration": "99%", "literacy_rate": "99%", "stem_graduates": "~25,000 annually; ETH Zurich, EPFL",
        "labor_force": "5.2 million",
        "key_industries": "Banking/finance, pharmaceuticals (Novartis, Roche), precision manufacturing, watches, tourism, chemicals, technology",
        "ai_risk_high": "Banking back-office, administrative services, basic financial processing",
        "ai_risk_medium": "Insurance, pharmaceutical testing, logistics, manufacturing",
        "ai_risk_low": "Precision manufacturing, pharma R&D, healthcare, education, watchmaking, tourism",
        "key_challenges": "Skill shortages in specialized sectors despite high wages, EU relationship tensions, aging population, housing costs, maintaining competitiveness with AI while preserving quality of life",
        "references": [("World Bank - Switzerland", "https://data.worldbank.org/country/switzerland"), ("Swiss Federal Statistics", "https://www.bfs.admin.ch/bfs/en/home.html"), ("Trading Economics - Switzerland", "https://tradingeconomics.com/switzerland/indicators")]
    },
    "new-zealand": {
        "name": "New Zealand", "slug": "new-zealand-nz", "population": "5.1 million",
        "gdp_per_capita": "$48,310", "gdp_per_capita_ppp": "$51,700", "gdp_growth": "1.1%",
        "currency": "NZD", "avg_monthly_salary": "NZD 6,000 (~$3,500 USD; NZD 72,000/year)",
        "avg_salary_usd": "$3,500", "minimum_wage": "NZD 23.50/hour (2025)",
        "it_salary_range": "NZD 70,000-130,000/year; senior NZD 130,000-180,000+",
        "manufacturing_salary": "NZD 50,000-70,000/year",
        "unemployment": "5.4%", "ai_adoption": "Moderate; strong agritech innovation",
        "internet_penetration": "95%", "literacy_rate": "99%", "stem_graduates": "~15,000 annually",
        "labor_force": "2.9 million",
        "key_industries": "Agriculture (dairy, meat, wool), tourism, forestry, fishing, wine, technology, film production",
        "ai_risk_high": "Administrative services, financial back-office, customer service, data processing",
        "ai_risk_medium": "Banking, agriculture processing, logistics, retail",
        "ai_risk_low": "Agriculture, tourism, healthcare, education, film production, skilled trades",
        "key_challenges": "Economic stagnation, low consumer spending, housing affordability crisis, distance from major markets, small domestic market size",
        "references": [("World Bank - NZ", "https://data.worldbank.org/country/new-zealand"), ("Stats NZ", "https://www.stats.govt.nz/"), ("Trading Economics - NZ", "https://tradingeconomics.com/new-zealand/indicators")]
    },
    "iraq": {
        "name": "Iraq", "slug": "iraq-iraq", "population": "44 million",
        "gdp_per_capita": "$5,970", "gdp_per_capita_ppp": "$12,000", "gdp_growth": "2.0% (2024)",
        "currency": "IQD", "avg_monthly_salary": "IQD 800,000 (~$545 USD)",
        "avg_salary_usd": "$545", "minimum_wage": "IQD 350,000/month (~$238 USD)",
        "it_salary_range": "IQD 1.5M-4M/month (~$1,000-2,700 USD)",
        "manufacturing_salary": "IQD 500,000-800,000/month (~$340-545 USD)",
        "unemployment": "15.5%", "ai_adoption": "Minimal; oil sector uses some automation",
        "internet_penetration": "60%", "literacy_rate": "86%", "stem_graduates": "~40,000 annually",
        "labor_force": "10 million",
        "key_industries": "Oil & gas (99% of exports), agriculture, construction, telecommunications",
        "ai_risk_high": "Government admin, basic data processing, customer service",
        "ai_risk_medium": "Banking, telecom, oil sector operations",
        "ai_risk_low": "Oil extraction, agriculture, construction, healthcare, education",
        "key_challenges": "Extreme oil dependency (99% exports), high unemployment, political instability, infrastructure reconstruction ongoing, youth bulge with limited opportunities, water scarcity",
        "references": [("World Bank - Iraq", "https://www.worldbank.org/en/country/iraq/overview"), ("Trading Economics - Iraq", "https://tradingeconomics.com/iraq/indicators")]
    },
    "jordan": {
        "name": "Jordan", "slug": "jordan-jordan", "population": "11 million",
        "gdp_per_capita": "$4,700", "gdp_per_capita_ppp": "$13,500", "gdp_growth": "2.4%",
        "currency": "JOD", "avg_monthly_salary": "JOD 550 (~$775 USD)",
        "avg_salary_usd": "$775", "minimum_wage": "JOD 290/month (~$409 USD, 2025)",
        "it_salary_range": "JOD 600-2,000/month (~$845-2,820 USD)",
        "manufacturing_salary": "JOD 300-500/month (~$423-705 USD)",
        "unemployment": "21.4%", "ai_adoption": "Growing; Amman emerging as regional tech hub; MODEE digital strategy",
        "internet_penetration": "83%", "literacy_rate": "98%", "stem_graduates": "~30,000 annually",
        "labor_force": "2.8 million",
        "key_industries": "Services, tourism, pharmaceuticals, mining (potash, phosphate), IT outsourcing, agriculture",
        "ai_risk_high": "BPO/call centers, government admin, data entry",
        "ai_risk_medium": "Banking, tourism operations, pharmaceutical processing",
        "ai_risk_low": "Healthcare, education, mining engineering, tourism services, agriculture",
        "key_challenges": "21.4% unemployment (youth 46%), refugee hosting burden (750K+ Syrian refugees), water scarcity (most water-scarce country globally), limited natural resources, regional instability",
        "references": [("World Bank - Jordan", "https://www.worldbank.org/en/country/jordan/overview"), ("DOS Jordan", "https://dosweb.dos.gov.jo/"), ("Trading Economics - Jordan", "https://tradingeconomics.com/jordan/indicators")]
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
