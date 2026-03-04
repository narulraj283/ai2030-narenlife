#!/usr/bin/env python3
"""Batch 10: Azerbaijan, Kazakhstan, Belarus, Belgium, Denmark, Finland, Norway, Portugal, Greece, Hungary, Czech Republic, Poland, Croatia"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from batch2_rewrite import gen_article, AUDIENCES, ARTICLES_DIR

COUNTRIES = {
    "azerbaijan": {
        "name": "Azerbaijan", "slug": "azerbaijan-azerbaijan", "population": "10.2 million",
        "gdp_per_capita": "$7,762", "gdp_per_capita_ppp": "$18,600", "gdp_growth": "1.1%",
        "currency": "AZN", "avg_monthly_salary": "AZN 1,000 (~$588 USD)",
        "avg_salary_usd": "$588", "minimum_wage": "AZN 345/month (~$203 USD)",
        "it_salary_range": "AZN 1,500-4,000/month (~$882-2,353 USD)",
        "manufacturing_salary": "AZN 600-1,200/month (~$353-706 USD)",
        "unemployment": "5.6%", "ai_adoption": "Low; oil sector digitization beginning, limited tech ecosystem",
        "internet_penetration": "82%", "literacy_rate": "99%", "stem_graduates": "~15,000 annually",
        "labor_force": "5.2 million",
        "key_industries": "Oil & gas (dominant), petrochemicals, agriculture (cotton, hazelnuts), tourism, construction, ICT (emerging)",
        "ai_risk_high": "Oil sector administration, government bureaucracy, banking operations",
        "ai_risk_medium": "Petrochemicals, telecom, retail, tourism services",
        "ai_risk_low": "Agriculture, construction, skilled oil operations, healthcare, education, handicrafts",
        "key_challenges": "Oil dependency (90% of exports), Dutch disease, authoritarian governance, Nagorno-Karabakh aftermath, limited economic diversification, corruption concerns, brain drain",
        "references": [("World Bank - Azerbaijan", "https://www.worldbank.org/en/country/azerbaijan/overview"), ("SSC Azerbaijan", "https://www.stat.gov.az/"), ("IMF - Azerbaijan", "https://www.imf.org/en/Countries/AZE"), ("ADB - Azerbaijan", "https://www.adb.org/countries/azerbaijan/main"), ("Trading Economics - Azerbaijan", "https://tradingeconomics.com/azerbaijan/indicators")]
    },
    "kazakhstan": {
        "name": "Kazakhstan", "slug": "kazakhstan-kazakhstan", "population": "19.8 million",
        "gdp_per_capita": "$12,369", "gdp_per_capita_ppp": "$32,000", "gdp_growth": "5.1%",
        "currency": "KZT", "avg_monthly_salary": "KZT 380,000 (~$820 USD)",
        "avg_salary_usd": "$820", "minimum_wage": "KZT 85,000/month (~$183 USD)",
        "it_salary_range": "KZT 600,000-2,000,000/month (~$1,293-4,310 USD)",
        "manufacturing_salary": "KZT 250,000-500,000/month (~$539-1,078 USD)",
        "unemployment": "4.7%", "ai_adoption": "Growing; Astana Hub tech park, government digitization, Kaspi.kz fintech leader",
        "internet_penetration": "88%", "literacy_rate": "99%", "stem_graduates": "~40,000 annually",
        "labor_force": "9.2 million",
        "key_industries": "Oil & gas, mining (uranium — world #1, copper, zinc), agriculture (wheat), financial services, construction, logistics, IT/fintech",
        "ai_risk_high": "Administrative services, banking operations, data processing, oil sector back-office",
        "ai_risk_medium": "Mining monitoring, retail, telecom, logistics, agricultural processing",
        "ai_risk_low": "Farming, skilled mining/drilling, construction, healthcare, education, transport",
        "key_challenges": "Oil/gas dependency, Russia economic exposure, political transition risks, vast geography with sparse population, environmental damage (Aral Sea), inequality between urban/rural, corruption",
        "references": [("World Bank - Kazakhstan", "https://www.worldbank.org/en/country/kazakhstan/overview"), ("Bureau of National Statistics Kazakhstan", "https://stat.gov.kz/en/"), ("IMF - Kazakhstan", "https://www.imf.org/en/Countries/KAZ"), ("ADB - Kazakhstan", "https://www.adb.org/countries/kazakhstan/main"), ("Trading Economics - Kazakhstan", "https://tradingeconomics.com/kazakhstan/indicators")]
    },
    "belarus": {
        "name": "Belarus", "slug": "belarus-belarus", "population": "9.2 million",
        "gdp_per_capita": "$7,888", "gdp_per_capita_ppp": "$22,700", "gdp_growth": "3.9%",
        "currency": "BYN", "avg_monthly_salary": "BYN 2,000 (~$615 USD)",
        "avg_salary_usd": "$615", "minimum_wage": "BYN 626/month (~$192 USD)",
        "it_salary_range": "BYN 5,000-15,000/month (~$1,538-4,615 USD) — but IT sector hollowed out by emigration",
        "manufacturing_salary": "BYN 1,200-2,500/month (~$369-769 USD)",
        "unemployment": "3.6% (official)", "ai_adoption": "Moderate pre-2020; Hi-Tech Park was major hub, now severely diminished by sanctions and emigration",
        "internet_penetration": "85%", "literacy_rate": "99%", "stem_graduates": "~20,000 annually (declining)",
        "labor_force": "4.8 million",
        "key_industries": "Machinery, petrochemicals (refining Russian oil), potash mining, agriculture, IT services (declining), military equipment",
        "ai_risk_high": "Manufacturing administration, banking, government bureaucracy",
        "ai_risk_medium": "Petrochemical operations, telecom, retail, logistics",
        "ai_risk_low": "Agriculture, construction, skilled manufacturing, healthcare, education",
        "key_challenges": "Western sanctions over 2020 crackdown and Russia alliance, massive IT talent emigration (50K+ left), Russia dependency, isolated from global tech ecosystem, aging population, state-dominated economy limits innovation",
        "references": [("World Bank - Belarus", "https://www.worldbank.org/en/country/belarus/overview"), ("Belstat", "https://www.belstat.gov.by/en/"), ("IMF - Belarus", "https://www.imf.org/en/Countries/BLR"), ("Trading Economics - Belarus", "https://tradingeconomics.com/belarus/indicators"), ("EBRD - Belarus", "https://www.ebrd.com/belarus.html")]
    },
    "belgium": {
        "name": "Belgium", "slug": "belgium-belgium", "population": "11.7 million",
        "gdp_per_capita": "$51,247", "gdp_per_capita_ppp": "$65,500", "gdp_growth": "1.0%",
        "currency": "EUR", "avg_monthly_salary": "€3,800 (~$4,100 USD)",
        "avg_salary_usd": "$4,100", "minimum_wage": "€1,994/month (~$2,153 USD) — one of highest in EU",
        "it_salary_range": "€4,500-9,000/month (~$4,860-9,720 USD)",
        "manufacturing_salary": "€2,800-4,500/month (~$3,024-4,860 USD)",
        "unemployment": "5.5%", "ai_adoption": "High; EU AI Act headquarters, strong pharma/biotech AI, research institutions (IMEC, KU Leuven AI)",
        "internet_penetration": "93%", "literacy_rate": "99%", "stem_graduates": "~25,000 annually",
        "labor_force": "5.2 million",
        "key_industries": "Pharmaceuticals, chemicals, logistics (Port of Antwerp), automotive, food processing, financial services, diamond trade, EU institutions",
        "ai_risk_high": "Administrative services, financial processing, logistics documentation, diamond sorting",
        "ai_risk_medium": "Banking, insurance, retail, pharmaceutical research support, port logistics",
        "ai_risk_low": "Healthcare, education, skilled manufacturing, creative industries, food production, construction",
        "key_challenges": "Complex federal structure (3 languages, 6 governments), high labor costs, high public debt (105% of GDP), regional inequality (Flanders vs Wallonia), aging population, energy transition costs",
        "references": [("World Bank - Belgium", "https://data.worldbank.org/country/belgium"), ("Statbel", "https://statbel.fgov.be/en"), ("IMF - Belgium", "https://www.imf.org/en/Countries/BEL"), ("OECD - Belgium", "https://www.oecd.org/belgium/"), ("Trading Economics - Belgium", "https://tradingeconomics.com/belgium/indicators")]
    },
    "denmark": {
        "name": "Denmark", "slug": "denmark-denmark", "population": "5.9 million",
        "gdp_per_capita": "$67,790", "gdp_per_capita_ppp": "$72,000", "gdp_growth": "1.8%",
        "currency": "DKK", "avg_monthly_salary": "DKK 45,000 (~$6,500 USD)",
        "avg_salary_usd": "$6,500", "minimum_wage": "No statutory minimum; collective agreements set ~DKK 130/hour (~$18.80)",
        "it_salary_range": "DKK 50,000-90,000/month (~$7,230-13,014 USD)",
        "manufacturing_salary": "DKK 30,000-45,000/month (~$4,338-6,507 USD)",
        "unemployment": "2.8%", "ai_adoption": "Very high; Danish AI Strategy, strong pharma AI (Novo Nordisk), green tech AI, Pioneer Centre for AI",
        "internet_penetration": "98%", "literacy_rate": "99%", "stem_graduates": "~15,000 annually",
        "labor_force": "3.1 million",
        "key_industries": "Pharmaceuticals (Novo Nordisk, Lundbeck), wind energy (Vestas, Ørsted), shipping (Maersk), agriculture (pork, dairy), IT, financial services, design",
        "ai_risk_high": "Administrative services, financial processing, logistics planning, data analysis",
        "ai_risk_medium": "Pharmaceutical research support, retail, insurance, marketing, shipping logistics",
        "ai_risk_low": "Healthcare, education, wind turbine maintenance, agriculture, creative industries, skilled manufacturing",
        "key_challenges": "Labor shortages, high cost of living, aging population, green transition costs, housing crisis in Copenhagen, maintaining flexicurity model with AI displacement",
        "references": [("World Bank - Denmark", "https://data.worldbank.org/country/denmark"), ("Statistics Denmark", "https://www.dst.dk/en"), ("IMF - Denmark", "https://www.imf.org/en/Countries/DNK"), ("OECD - Denmark", "https://www.oecd.org/denmark/"), ("Trading Economics - Denmark", "https://tradingeconomics.com/denmark/indicators")]
    },
    "finland": {
        "name": "Finland", "slug": "finland-finland", "population": "5.6 million",
        "gdp_per_capita": "$53,654", "gdp_per_capita_ppp": "$58,500", "gdp_growth": "-1.0%",
        "currency": "EUR", "avg_monthly_salary": "€3,900 (~$4,212 USD)",
        "avg_salary_usd": "$4,212", "minimum_wage": "No statutory minimum; collective agreements typically €1,800-2,200/month",
        "it_salary_range": "€4,500-8,500/month (~$4,860-9,180 USD)",
        "manufacturing_salary": "€2,800-4,200/month (~$3,024-4,536 USD)",
        "unemployment": "7.2%", "ai_adoption": "Very high; Elements of AI course (1% of population), Nokia legacy in tech, strong AI research (FCAI)",
        "internet_penetration": "96%", "literacy_rate": "99%", "stem_graduates": "~12,000 annually",
        "labor_force": "2.8 million",
        "key_industries": "Technology (Nokia, gaming — Supercell, Rovio), forestry/paper, machinery, chemicals, pharmaceuticals, financial services, cleantech",
        "ai_risk_high": "Administrative services, banking operations, insurance processing, logistics",
        "ai_risk_medium": "Manufacturing, retail, telecom, paper/pulp processing, marketing",
        "ai_risk_low": "Healthcare, education, skilled engineering, forestry, creative industries, construction",
        "key_challenges": "Recession/slow growth, aging population (among oldest in EU), Russia border security costs, NATO integration costs, Nokia decline legacy, brain drain risk, high taxation",
        "references": [("World Bank - Finland", "https://data.worldbank.org/country/finland"), ("Statistics Finland", "https://www.stat.fi/index_en.html"), ("IMF - Finland", "https://www.imf.org/en/Countries/FIN"), ("OECD - Finland", "https://www.oecd.org/finland/"), ("Trading Economics - Finland", "https://tradingeconomics.com/finland/indicators")]
    },
    "norway": {
        "name": "Norway", "slug": "norway-norway", "population": "5.5 million",
        "gdp_per_capita": "$87,925", "gdp_per_capita_ppp": "$82,000", "gdp_growth": "1.1%",
        "currency": "NOK", "avg_monthly_salary": "NOK 55,000 (~$5,225 USD)",
        "avg_salary_usd": "$5,225", "minimum_wage": "No statutory minimum; sector agreements set NOK 200-230/hour (~$19-22) for some industries",
        "it_salary_range": "NOK 60,000-100,000/month (~$5,700-9,500 USD)",
        "manufacturing_salary": "NOK 40,000-55,000/month (~$3,800-5,225 USD)",
        "unemployment": "3.5%", "ai_adoption": "High; oil/gas AI applications, Nordic AI leader, strong digital government services",
        "internet_penetration": "98%", "literacy_rate": "99%", "stem_graduates": "~10,000 annually",
        "labor_force": "2.9 million",
        "key_industries": "Oil & gas, maritime/shipping, seafood (salmon farming), renewable energy (hydropower), technology, financial services, tourism",
        "ai_risk_high": "Oil administration, financial services, government bureaucracy, data analysis",
        "ai_risk_medium": "Shipping logistics, retail, insurance, oil monitoring, telecom",
        "ai_risk_low": "Healthcare, education, fishing/aquaculture, offshore oil operations, construction, tourism",
        "key_challenges": "Oil dependency and green transition tension, high costs/Dutch disease, labor shortages, aging population, housing costs, maintaining welfare state with AI displacement",
        "references": [("World Bank - Norway", "https://data.worldbank.org/country/norway"), ("Statistics Norway", "https://www.ssb.no/en"), ("IMF - Norway", "https://www.imf.org/en/Countries/NOR"), ("OECD - Norway", "https://www.oecd.org/norway/"), ("Trading Economics - Norway", "https://tradingeconomics.com/norway/indicators")]
    },
    "portugal": {
        "name": "Portugal", "slug": "portugal-portugal", "population": "10.4 million",
        "gdp_per_capita": "$26,409", "gdp_per_capita_ppp": "$42,000", "gdp_growth": "2.3%",
        "currency": "EUR", "avg_monthly_salary": "€1,500 (~$1,620 USD)",
        "avg_salary_usd": "$1,620", "minimum_wage": "€820/month (~$886 USD) — 14 payments/year",
        "it_salary_range": "€2,500-6,000/month (~$2,700-6,480 USD)",
        "manufacturing_salary": "€900-1,500/month (~$972-1,620 USD)",
        "unemployment": "6.1%", "ai_adoption": "Moderate; Lisbon tech hub (Web Summit host), growing startup ecosystem",
        "internet_penetration": "85%", "literacy_rate": "96%", "stem_graduates": "~20,000 annually",
        "labor_force": "5.2 million",
        "key_industries": "Tourism, automotive parts, textiles, cork (world #1), wine, technology/startups, renewable energy, financial services, real estate",
        "ai_risk_high": "Administrative services, tourism booking, financial processing, textile quality control",
        "ai_risk_medium": "Banking, retail, automotive manufacturing, call centers, telecom",
        "ai_risk_low": "Tourism (hospitality), agriculture (wine, cork), construction, healthcare, education, creative industries",
        "key_challenges": "Low wages compared to Western Europe, brain drain to higher-paying EU countries, housing crisis (Lisbon/Porto), aging population, fiscal discipline constraints, tourism over-reliance",
        "references": [("World Bank - Portugal", "https://data.worldbank.org/country/portugal"), ("INE Portugal", "https://www.ine.pt/"), ("IMF - Portugal", "https://www.imf.org/en/Countries/PRT"), ("OECD - Portugal", "https://www.oecd.org/portugal/"), ("Trading Economics - Portugal", "https://tradingeconomics.com/portugal/indicators")]
    },
    "greece": {
        "name": "Greece", "slug": "greece-greece", "population": "10.4 million",
        "gdp_per_capita": "$22,440", "gdp_per_capita_ppp": "$38,000", "gdp_growth": "2.0%",
        "currency": "EUR", "avg_monthly_salary": "€1,200 (~$1,296 USD)",
        "avg_salary_usd": "$1,296", "minimum_wage": "€780/month (~$842 USD) — 14 payments/year",
        "it_salary_range": "€2,000-5,000/month (~$2,160-5,400 USD)",
        "manufacturing_salary": "€800-1,400/month (~$864-1,512 USD)",
        "unemployment": "9.6%", "ai_adoption": "Moderate; growing tech scene in Athens, government digitization, shipping AI adoption",
        "internet_penetration": "83%", "literacy_rate": "98%", "stem_graduates": "~18,000 annually",
        "labor_force": "4.5 million",
        "key_industries": "Tourism, shipping (world's largest merchant fleet), agriculture (olives, wine), food processing, pharmaceuticals, construction, energy, tech startups",
        "ai_risk_high": "Administrative services, banking, tourism booking, shipping documentation",
        "ai_risk_medium": "Retail, insurance, telecom, agricultural processing, shipping logistics",
        "ai_risk_low": "Tourism hospitality, agriculture (olive/wine), construction, healthcare, education, maritime operations",
        "key_challenges": "Debt crisis legacy (still >160% of GDP), brain drain (350K+ young Greeks left), aging population, tourism seasonality, public sector inefficiency, energy transition costs, island connectivity",
        "references": [("World Bank - Greece", "https://data.worldbank.org/country/greece"), ("ELSTAT", "https://www.statistics.gr/en/home"), ("IMF - Greece", "https://www.imf.org/en/Countries/GRC"), ("OECD - Greece", "https://www.oecd.org/greece/"), ("Trading Economics - Greece", "https://tradingeconomics.com/greece/indicators")]
    },
    "hungary": {
        "name": "Hungary", "slug": "hungary-hungary", "population": "9.6 million",
        "gdp_per_capita": "$18,935", "gdp_per_capita_ppp": "$41,000", "gdp_growth": "-0.8%",
        "currency": "HUF", "avg_monthly_salary": "HUF 600,000 (~$1,600 USD)",
        "avg_salary_usd": "$1,600", "minimum_wage": "HUF 266,800/month (~$712 USD); skilled minimum HUF 326,000 (~$870)",
        "it_salary_range": "HUF 900,000-2,500,000/month (~$2,400-6,676 USD)",
        "manufacturing_salary": "HUF 350,000-600,000/month (~$935-1,602 USD)",
        "unemployment": "4.3%", "ai_adoption": "Moderate; automotive sector AI (Mercedes, BMW, Audi factories), Budapest tech scene",
        "internet_penetration": "89%", "literacy_rate": "99%", "stem_graduates": "~18,000 annually",
        "labor_force": "4.7 million",
        "key_industries": "Automotive (largest sector — Mercedes, BMW, Audi, Suzuki), electronics, pharmaceuticals, agriculture, tourism, financial services, EV batteries (CATL, Samsung SDI)",
        "ai_risk_high": "Administrative services, banking, automotive assembly (already automating), data processing",
        "ai_risk_medium": "Manufacturing quality control, retail, telecom, logistics, insurance",
        "ai_risk_low": "Healthcare, education, agriculture, construction, tourism, skilled engineering",
        "key_challenges": "EU tensions over rule of law, automotive dependency risk from EV transition, inflation aftermath, brain drain to Western Europe, aging/declining population, energy dependency (Russia), forint volatility",
        "references": [("World Bank - Hungary", "https://data.worldbank.org/country/hungary"), ("KSH Hungary", "https://www.ksh.hu/"), ("IMF - Hungary", "https://www.imf.org/en/Countries/HUN"), ("OECD - Hungary", "https://www.oecd.org/hungary/"), ("Trading Economics - Hungary", "https://tradingeconomics.com/hungary/indicators")]
    },
    "czech_republic": {
        "name": "Czech Republic", "slug": "czech-republic-czech-republic", "population": "10.9 million",
        "gdp_per_capita": "$27,220", "gdp_per_capita_ppp": "$49,000", "gdp_growth": "-0.4%",
        "currency": "CZK", "avg_monthly_salary": "CZK 43,000 (~$1,870 USD)",
        "avg_salary_usd": "$1,870", "minimum_wage": "CZK 18,900/month (~$822 USD)",
        "it_salary_range": "CZK 60,000-130,000/month (~$2,609-5,652 USD)",
        "manufacturing_salary": "CZK 30,000-50,000/month (~$1,304-2,174 USD)",
        "unemployment": "2.6%", "ai_adoption": "High; strong manufacturing AI, Prague tech hub, Avast/JetBrains heritage, automotive AI",
        "internet_penetration": "91%", "literacy_rate": "99%", "stem_graduates": "~22,000 annually",
        "labor_force": "5.4 million",
        "key_industries": "Automotive (Škoda/VW), machinery, electronics, IT services, glass/ceramics, chemicals, tourism, beer/food processing",
        "ai_risk_high": "Administrative services, banking, automotive assembly (robotics), data processing, insurance",
        "ai_risk_medium": "Manufacturing quality control, retail, telecom, logistics, marketing",
        "ai_risk_low": "Healthcare, education, skilled engineering, construction, agriculture, tourism, creative industries",
        "key_challenges": "Labor shortage (lowest unemployment in EU), automotive dependency + EV disruption, energy costs, Russia energy dependency reduction, aging population, housing crisis in Prague, wage gap with Western Europe",
        "references": [("World Bank - Czech Republic", "https://data.worldbank.org/country/czechia"), ("CZSO", "https://www.czso.cz/csu/czso/home"), ("IMF - Czech Republic", "https://www.imf.org/en/Countries/CZE"), ("OECD - Czech Republic", "https://www.oecd.org/czech-republic/"), ("Trading Economics - Czech Republic", "https://tradingeconomics.com/czech-republic/indicators")]
    },
    "poland": {
        "name": "Poland", "slug": "poland-poland", "population": "37.8 million",
        "gdp_per_capita": "$20,592", "gdp_per_capita_ppp": "$45,500", "gdp_growth": "0.2%",
        "currency": "PLN", "avg_monthly_salary": "PLN 7,500 (~$1,875 USD)",
        "avg_salary_usd": "$1,875", "minimum_wage": "PLN 4,300/month (~$1,075 USD) in 2024",
        "it_salary_range": "PLN 12,000-30,000/month (~$3,000-7,500 USD)",
        "manufacturing_salary": "PLN 5,000-8,000/month (~$1,250-2,000 USD)",
        "unemployment": "2.8%", "ai_adoption": "Growing; strong IT outsourcing sector, Warsaw/Krakow tech hubs, gaming industry (CD Projekt)",
        "internet_penetration": "87%", "literacy_rate": "99%", "stem_graduates": "~60,000 annually",
        "labor_force": "17.5 million",
        "key_industries": "Automotive, IT services/BPO, machinery, food processing, gaming (CD Projekt, Techland), electronics, logistics, financial services, renewable energy",
        "ai_risk_high": "BPO/shared services, banking, administrative services, data processing, manufacturing assembly",
        "ai_risk_medium": "Automotive production, retail, telecom, insurance, logistics, food processing",
        "ai_risk_low": "Healthcare, education, agriculture, construction, gaming development, skilled engineering, creative industries",
        "key_challenges": "Rapid wage growth compressing BPO advantage, demographic decline (aging + emigration), judicial independence concerns, energy transition from coal, Ukraine war proximity/refugee integration, labor shortages",
        "references": [("World Bank - Poland", "https://data.worldbank.org/country/poland"), ("GUS Poland", "https://stat.gov.pl/en/"), ("IMF - Poland", "https://www.imf.org/en/Countries/POL"), ("OECD - Poland", "https://www.oecd.org/poland/"), ("Trading Economics - Poland", "https://tradingeconomics.com/poland/indicators")]
    },
    "croatia": {
        "name": "Croatia", "slug": "croatia-croatia", "population": "3.9 million",
        "gdp_per_capita": "$19,324", "gdp_per_capita_ppp": "$37,000", "gdp_growth": "3.1%",
        "currency": "EUR (adopted January 2023)", "avg_monthly_salary": "€1,400 (~$1,512 USD)",
        "avg_salary_usd": "$1,512", "minimum_wage": "€740/month (~$799 USD)",
        "it_salary_range": "€2,500-5,500/month (~$2,700-5,940 USD)",
        "manufacturing_salary": "€900-1,500/month (~$972-1,620 USD)",
        "unemployment": "6.0%", "ai_adoption": "Moderate; growing IT sector (Infobip, Rimac), Zagreb tech ecosystem",
        "internet_penetration": "84%", "literacy_rate": "99%", "stem_graduates": "~8,000 annually",
        "labor_force": "1.7 million",
        "key_industries": "Tourism (coast/islands), shipbuilding, food processing, IT (Infobip, Nanobit), pharmaceuticals, energy, automotive (Rimac — EV hypercar)",
        "ai_risk_high": "Administrative services, banking, tourism booking, basic manufacturing",
        "ai_risk_medium": "Shipbuilding automation, retail, telecom, insurance, food processing",
        "ai_risk_low": "Tourism hospitality, agriculture, construction, healthcare, education, maritime operations",
        "key_challenges": "Population decline (severe emigration to EU + aging), tourism over-reliance, seasonal employment, brain drain, high public debt, regional inequality (coast vs interior)",
        "references": [("World Bank - Croatia", "https://data.worldbank.org/country/croatia"), ("DZS Croatia", "https://dzs.gov.hr/en"), ("IMF - Croatia", "https://www.imf.org/en/Countries/HRV"), ("OECD - Croatia", "https://www.oecd.org/croatia/"), ("Trading Economics - Croatia", "https://tradingeconomics.com/croatia/indicators")]
    },
}

def rewrite_country(key):
    c = COUNTRIES[key]
    slug = c["slug"]
    prefix = slug.split("-")[0]
    count = 0
    for aud in AUDIENCES:
        fname = f"countries-{slug}-{aud}-edition.html"
        fpath = os.path.join(ARTICLES_DIR, fname)
        if not os.path.exists(fpath):
            for f in os.listdir(ARTICLES_DIR):
                if f.startswith(f"countries-{prefix}") and f.endswith(f"-{aud}-edition.html"):
                    fpath = os.path.join(ARTICLES_DIR, f)
                    fname = f
                    break
        html = gen_article(c, aud, fname)
        with open(fpath, "w", encoding="utf-8") as fh:
            fh.write(html)
        count += 1
    print(f"  ✓ {c['name']}: {count} articles")
    return count

def main():
    total = 0
    for key in COUNTRIES:
        total += rewrite_country(key)
    print(f"\nDone! {total} articles rewritten.")

if __name__ == "__main__":
    main()
