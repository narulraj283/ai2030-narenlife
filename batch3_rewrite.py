#!/usr/bin/env python3
"""Batch 3: France, UK, Germany, South Korea, Australia, Canada, Mexico, South Africa, Egypt, Philippines"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the template engine from batch2
from batch2_rewrite import gen_article, AUDIENCES, ARTICLES_DIR, AUDIENCE_TITLES

COUNTRIES = {
    "france": {
        "name": "France", "slug": "france-france", "population": "67 million",
        "gdp_per_capita": "$48,982", "gdp_per_capita_ppp": "$58,800", "gdp_growth": "1.2%",
        "currency": "EUR", "avg_monthly_salary": "€2,587 net (~$2,800 USD)",
        "avg_salary_usd": "$2,800", "minimum_wage": "€1,802/month gross (SMIC, 2025)",
        "it_salary_range": "€43,000-70,000/year; senior €80,000-120,000+",
        "manufacturing_salary": "€25,252/year (~€2,104/month)",
        "unemployment": "7.4%",
        "ai_adoption": "Growing; France AI Strategy (€2.2B committed); strong AI research ecosystem (INRIA, Paris-Saclay)",
        "internet_penetration": "93%", "literacy_rate": "99%",
        "stem_graduates": "~180,000 annually",
        "labor_force": "31 million",
        "key_industries": "Automotive, pharmaceuticals, aerospace (Airbus), luxury goods, tourism, agriculture, banking, nuclear energy",
        "ai_risk_high": "Administrative services, call centers, financial back-office, basic manufacturing",
        "ai_risk_medium": "Banking, insurance, automotive manufacturing, logistics, retail",
        "ai_risk_low": "Healthcare, education, luxury goods craftsmanship, tourism, agriculture, nuclear engineering",
        "key_challenges": "Skills gap in digital sectors despite strong education, high labor costs, pension reform tensions, integration of AI while maintaining social protections",
        "references": [
            ("World Bank - France Data", "https://data.worldbank.org/country/france"),
            ("INSEE - French Statistics", "https://www.insee.fr/en/accueil"),
            ("France AI Strategy", "https://www.gouvernement.fr/en/artificial-intelligence"),
            ("OECD - France Economic Survey", "https://www.oecd.org/en/topics/sub-issues/economic-surveys-france.html"),
            ("Trading Economics - France", "https://tradingeconomics.com/france/indicators"),
        ]
    },
    "uk": {
        "name": "United Kingdom", "slug": "uk-uk", "population": "69 million",
        "gdp_per_capita": "$47,265", "gdp_per_capita_ppp": "$56,800", "gdp_growth": "1.1%",
        "currency": "GBP", "avg_monthly_salary": "£2,634 net (~$3,300 USD; £31,602/year)",
        "avg_salary_usd": "$3,300", "minimum_wage": "£11.44/hour (National Living Wage, 2025)",
        "it_salary_range": "£50,000-95,000/year; senior/London £100,000-150,000+",
        "manufacturing_salary": "£25,004/year (~£2,084/month)",
        "unemployment": "4.7%",
        "ai_adoption": "Strong; UK AI Safety Institute; £1B+ government AI investment; London as European AI hub",
        "internet_penetration": "96%", "literacy_rate": "99%",
        "stem_graduates": "~200,000 annually",
        "labor_force": "34 million",
        "key_industries": "Financial services, technology, pharmaceuticals, automotive, oil & gas, creative industries, higher education",
        "ai_risk_high": "Financial services back-office, administrative roles, call centers, basic legal services",
        "ai_risk_medium": "Banking operations, insurance, logistics, retail, media",
        "ai_risk_low": "Healthcare (NHS), education, creative arts, skilled trades, renewable energy",
        "key_challenges": "Post-Brexit economic adjustment, labor market skill mismatches, productivity growth lag, regional inequality between London/southeast and rest of UK",
        "references": [
            ("World Bank - UK Data", "https://data.worldbank.org/country/united-kingdom"),
            ("ONS - UK Statistics", "https://www.ons.gov.uk/"),
            ("UK AI Safety Institute", "https://www.gov.uk/government/organisations/ai-safety-institute"),
            ("OECD - UK Economic Survey", "https://www.oecd.org/en/topics/sub-issues/economic-surveys-united-kingdom.html"),
            ("Trading Economics - UK", "https://tradingeconomics.com/united-kingdom/indicators"),
        ]
    },
    "germany": {
        "name": "Germany", "slug": "germany-germany", "population": "83 million",
        "gdp_per_capita": "$56,061", "gdp_per_capita_ppp": "$66,000", "gdp_growth": "-0.5% (recession in 2024)",
        "currency": "EUR", "avg_monthly_salary": "€4,358 gross (~$4,700 USD)",
        "avg_salary_usd": "$4,700", "minimum_wage": "€12.82/hour; ~€2,220/month gross (2025)",
        "it_salary_range": "€54,700-72,300/year; senior €80,000-110,000+",
        "manufacturing_salary": "€4,000/month gross (~€48,000/year)",
        "unemployment": "3.3%",
        "ai_adoption": "Moderate; strong Industry 4.0 focus; €3B AI strategy; Fraunhofer leading applied AI research",
        "internet_penetration": "93%", "literacy_rate": "99%",
        "stem_graduates": "~300,000 annually; strong apprenticeship system",
        "labor_force": "46 million",
        "key_industries": "Automotive (VW, BMW, Mercedes), machinery, chemicals, pharmaceuticals, renewable energy, engineering",
        "ai_risk_high": "Administrative services, basic manufacturing assembly, data processing, customer service",
        "ai_risk_medium": "Automotive manufacturing, banking, insurance, logistics",
        "ai_risk_low": "Skilled manufacturing, engineering, healthcare, renewable energy, R&D",
        "key_challenges": "Recession and manufacturing weakness from energy crisis, automotive industry transition to EVs, demographic decline, dependence on China trade, defense spending pressure",
        "references": [
            ("World Bank - Germany Data", "https://data.worldbank.org/country/germany"),
            ("Destatis - Federal Statistics", "https://www.destatis.de/EN/Home/_node.html"),
            ("German AI Strategy", "https://www.ki-strategie-deutschland.de/home.html"),
            ("OECD - Germany Survey", "https://www.oecd.org/en/topics/sub-issues/economic-surveys-germany.html"),
            ("Trading Economics - Germany", "https://tradingeconomics.com/germany/indicators"),
        ]
    },
    "south-korea": {
        "name": "South Korea", "slug": "south-korea-southkorea", "population": "52 million",
        "gdp_per_capita": "$36,024", "gdp_per_capita_ppp": "$56,700", "gdp_growth": "1.3%",
        "currency": "KRW", "avg_monthly_salary": "KRW 3,500,000 (~$2,500 USD)",
        "avg_salary_usd": "$2,500", "minimum_wage": "KRW 10,030/hour (2025)",
        "it_salary_range": "KRW 50M-100M+/year; Samsung/tech giants KRW 70M-150M",
        "manufacturing_salary": "KRW 3,000,000-4,000,000/month",
        "unemployment": "3.0%",
        "ai_adoption": "High; world leader in semiconductors; Samsung, SK Hynix driving AI chip production; government AI Digital Platform Government initiative",
        "internet_penetration": "97%", "literacy_rate": "99%",
        "stem_graduates": "~200,000 annually; top PISA scores",
        "labor_force": "29 million",
        "key_industries": "Semiconductors, electronics, automotive (Hyundai/Kia), shipbuilding, steel, K-culture (entertainment)",
        "ai_risk_high": "Administrative services, basic manufacturing assembly, data entry, customer service",
        "ai_risk_medium": "Financial services, automotive manufacturing, logistics, retail",
        "ai_risk_low": "Semiconductor engineering, healthcare, R&D, creative industries (K-pop, film), education",
        "key_challenges": "Severe demographic crisis (world's lowest fertility rate 0.72), aging population, chaebols dominance, youth unemployment pressure, housing affordability crisis",
        "references": [
            ("World Bank - South Korea", "https://data.worldbank.org/country/korea-rep"),
            ("KOSTAT - Korea Statistics", "https://kostat.go.kr/eng/"),
            ("Trading Economics - South Korea", "https://tradingeconomics.com/south-korea/indicators"),
            ("OECD - Korea Survey", "https://www.oecd.org/en/topics/sub-issues/economic-surveys-korea.html"),
        ]
    },
    "australia": {
        "name": "Australia", "slug": "australia-australia", "population": "26 million",
        "gdp_per_capita": "$65,530", "gdp_per_capita_ppp": "$65,400", "gdp_growth": "0.4% (weak)",
        "currency": "AUD", "avg_monthly_salary": "AUD 7,500 (~$4,800 USD; AUD 90,000/year)",
        "avg_salary_usd": "$4,800", "minimum_wage": "AUD 24.10/hour (2025)",
        "it_salary_range": "AUD 80,000-150,000/year; senior AUD 150,000-250,000+",
        "manufacturing_salary": "AUD 55,000-75,000/year",
        "unemployment": "4.1%",
        "ai_adoption": "Growing; National AI Centre established; strong fintech and health-tech sectors",
        "internet_penetration": "97%", "literacy_rate": "99%",
        "stem_graduates": "~80,000 annually",
        "labor_force": "14 million",
        "key_industries": "Mining (iron ore, coal, LNG), agriculture, services, finance, tourism, education exports",
        "ai_risk_high": "Administrative services, financial back-office, data processing, customer service",
        "ai_risk_medium": "Mining operations, banking, logistics, retail, agriculture",
        "ai_risk_low": "Healthcare, education, skilled trades, mining engineering, renewable energy",
        "key_challenges": "Real GDP per capita declined 7 consecutive quarters, housing affordability crisis, over-reliance on China for exports, cost of living pressures, regional inequality",
        "references": [
            ("World Bank - Australia", "https://data.worldbank.org/country/australia"),
            ("ABS - Australian Statistics", "https://www.abs.gov.au/"),
            ("Trading Economics - Australia", "https://tradingeconomics.com/australia/indicators"),
            ("OECD - Australia Survey", "https://www.oecd.org/en/topics/sub-issues/economic-surveys-australia.html"),
        ]
    },
    "canada": {
        "name": "Canada", "slug": "canada-canada", "population": "41 million",
        "gdp_per_capita": "$54,866", "gdp_per_capita_ppp": "$60,200", "gdp_growth": "1.5%",
        "currency": "CAD", "avg_monthly_salary": "CAD 5,500 (~$4,000 USD; CAD 66,000/year)",
        "avg_salary_usd": "$4,000", "minimum_wage": "CAD 17.20/hour (federal); provinces CAD 15-17.40",
        "it_salary_range": "CAD 70,000-130,000/year; senior CAD 130,000-200,000+ (Toronto/Vancouver)",
        "manufacturing_salary": "CAD 45,000-65,000/year",
        "unemployment": "6.7%",
        "ai_adoption": "Strong; Montreal and Toronto as global AI research hubs (MILA, Vector Institute); federal AI strategy since 2017",
        "internet_penetration": "95%", "literacy_rate": "99%",
        "stem_graduates": "~120,000 annually",
        "labor_force": "22 million",
        "key_industries": "Oil & gas, mining, automotive, aerospace, technology, agriculture, banking, forestry",
        "ai_risk_high": "Administrative services, financial back-office, customer service, data processing",
        "ai_risk_medium": "Oil & gas operations, banking, automotive, logistics, retail",
        "ai_risk_low": "Healthcare, education, skilled trades, natural resources engineering, creative industries",
        "key_challenges": "Housing affordability crisis, immigration policy tensions, oil sector transition to clean energy, productivity gap vs US, rising unemployment",
        "references": [
            ("World Bank - Canada", "https://data.worldbank.org/country/canada"),
            ("Statistics Canada", "https://www.statcan.gc.ca/"),
            ("CIFAR Pan-Canadian AI Strategy", "https://cifar.ca/ai/"),
            ("Trading Economics - Canada", "https://tradingeconomics.com/canada/indicators"),
        ]
    },
    "mexico": {
        "name": "Mexico", "slug": "mexico-mexico", "population": "129 million",
        "gdp_per_capita": "$14,158", "gdp_per_capita_ppp": "$24,600", "gdp_growth": "-0.5% (2025 contraction)",
        "currency": "MXN", "avg_monthly_salary": "MXN 16,000 (~$800 USD)",
        "avg_salary_usd": "$800", "minimum_wage": "MXN 6,041/month (2025); border zone MXN 9,061",
        "it_salary_range": "MXN 25,000-80,000/month; senior MXN 80,000-150,000+",
        "manufacturing_salary": "MXN 10,000-18,000/month (~$500-900 USD)",
        "unemployment": "2.4% (low but significant underemployment)",
        "ai_adoption": "Growing; nearshoring driving tech investment; strong auto industry automation",
        "internet_penetration": "78%", "literacy_rate": "95%",
        "stem_graduates": "~250,000 annually",
        "labor_force": "60 million",
        "key_industries": "Manufacturing (automotive, electronics, aerospace), oil (Pemex), agriculture, tourism, remittances, services",
        "ai_risk_high": "Maquiladora assembly, call centers, data entry, basic administrative services",
        "ai_risk_medium": "Automotive manufacturing, banking, logistics, agriculture processing",
        "ai_risk_low": "Tourism, healthcare, education, construction, creative industries, skilled trades",
        "key_challenges": "Economic contraction, remittance dependency ($63B/year), large informal economy (56% of workers), US tariff risks, security concerns, energy sector reform delays",
        "references": [
            ("World Bank - Mexico", "https://data.worldbank.org/country/mexico"),
            ("INEGI - Mexico Statistics", "https://www.inegi.org.mx/"),
            ("Trading Economics - Mexico", "https://tradingeconomics.com/mexico/indicators"),
            ("OECD - Mexico Survey", "https://www.oecd.org/en/topics/sub-issues/economic-surveys-mexico.html"),
        ]
    },
    "south-africa": {
        "name": "South Africa", "slug": "south-africa-southafrica", "population": "60 million",
        "gdp_per_capita": "$6,253", "gdp_per_capita_ppp": "$16,100", "gdp_growth": "1.0% (2024)",
        "currency": "ZAR", "avg_monthly_salary": "ZAR 25,000 (~$1,350 USD)",
        "avg_salary_usd": "$1,350", "minimum_wage": "ZAR 28.79/hour (2025); ~ZAR 5,000/month",
        "it_salary_range": "ZAR 400,000-900,000/year; senior ZAR 1M+",
        "manufacturing_salary": "ZAR 8,000-15,000/month (~$430-810 USD)",
        "unemployment": "31.4% (highest structural unemployment globally)",
        "ai_adoption": "Growing but limited; Cape Town and Johannesburg emerging as African tech hubs",
        "internet_penetration": "73%", "literacy_rate": "94%",
        "stem_graduates": "~80,000 annually",
        "labor_force": "24 million",
        "key_industries": "Mining (gold, platinum, diamonds), manufacturing, agriculture, finance, tourism, automotive",
        "ai_risk_high": "Mining admin, call centers (major BPO sector), financial back-office, data entry",
        "ai_risk_medium": "Banking, manufacturing, logistics, retail",
        "ai_risk_low": "Mining engineering, healthcare, education, tourism, renewable energy, skilled trades",
        "key_challenges": "31.4% unemployment crisis (youth 60%+), power crisis (load shedding), extreme inequality (Gini 0.63), infrastructure decay, crime affecting investment",
        "references": [
            ("World Bank - South Africa", "https://data.worldbank.org/country/south-africa"),
            ("Stats SA", "https://www.statssa.gov.za/"),
            ("Trading Economics - South Africa", "https://tradingeconomics.com/south-africa/indicators"),
            ("OECD - South Africa", "https://www.oecd.org/en/topics/sub-issues/economic-surveys-south-africa.html"),
        ]
    },
    "egypt": {
        "name": "Egypt", "slug": "egypt-egypt", "population": "108 million",
        "gdp_per_capita": "$3,570", "gdp_per_capita_ppp": "$16,000", "gdp_growth": "2.4% (FY2024)",
        "currency": "EGP", "avg_monthly_salary": "EGP 8,000-12,000 (~$160-240 USD)",
        "avg_salary_usd": "$160-240", "minimum_wage": "EGP 6,000/month (2024, public sector)",
        "it_salary_range": "EGP 15,000-50,000/month; senior EGP 60,000-100,000+",
        "manufacturing_salary": "EGP 4,000-8,000/month (~$80-160 USD)",
        "unemployment": "6.4%",
        "ai_adoption": "Growing; National AI Strategy launched; Egypt AI Center of Excellence",
        "internet_penetration": "72%", "literacy_rate": "72%",
        "stem_graduates": "~200,000 annually",
        "labor_force": "32 million",
        "key_industries": "Agriculture, tourism, oil & gas, textiles, Suez Canal revenues, construction, telecoms",
        "ai_risk_high": "Administrative government services, call centers, textile manufacturing assembly, data entry",
        "ai_risk_medium": "Banking, tourism operations, oil sector admin, logistics",
        "ai_risk_low": "Agriculture, construction, healthcare, education, tourism services",
        "key_challenges": "Currency devaluation (EGP lost ~50% since 2022), inflation pressures, high public debt, youth unemployment, population growth straining services",
        "references": [
            ("World Bank - Egypt Overview", "https://www.worldbank.org/en/country/egypt/overview"),
            ("CAPMAS - Egypt Statistics", "https://www.capmas.gov.eg/"),
            ("Egypt National AI Strategy", "https://mcit.gov.eg/en/Artificial_Intelligence"),
            ("Trading Economics - Egypt", "https://tradingeconomics.com/egypt/indicators"),
        ]
    },
    "philippines": {
        "name": "Philippines", "slug": "philippines-philippines", "population": "116 million",
        "gdp_per_capita": "$4,079", "gdp_per_capita_ppp": "$11,500", "gdp_growth": "6.0%",
        "currency": "PHP", "avg_monthly_salary": "PHP 50,000-60,000 (~$830-1,000 USD)",
        "avg_salary_usd": "$830-1,000", "minimum_wage": "PHP 645/day (NCR, 2025); varies by region",
        "it_salary_range": "PHP 40,000-120,000/month; BPO/IT-BPM sector; senior PHP 150,000+",
        "manufacturing_salary": "PHP 15,000-25,000/month (~$250-420 USD)",
        "unemployment": "3.8%",
        "ai_adoption": "Growing; major BPO/IT-BPM hub ($32B industry) facing AI disruption; government AI roadmap",
        "internet_penetration": "73%", "literacy_rate": "96%",
        "stem_graduates": "~150,000 annually",
        "labor_force": "49 million",
        "key_industries": "BPO/IT-BPM ($32B), electronics manufacturing, agriculture, remittances ($38B), tourism, mining",
        "ai_risk_high": "BPO/call centers (1.4M workers at risk), data entry, basic financial processing, electronics assembly",
        "ai_risk_medium": "Banking, manufacturing, logistics, government services",
        "ai_risk_low": "Healthcare (nursing), education, agriculture, tourism, creative industries, seafaring",
        "key_challenges": "BPO industry (8% of GDP, 1.4M direct jobs) faces severe AI disruption, remittance dependency, infrastructure gaps, typhoon vulnerability, inequality",
        "references": [
            ("World Bank - Philippines", "https://www.worldbank.org/en/country/philippines/overview"),
            ("PSA - Philippine Statistics", "https://psa.gov.ph/"),
            ("IBPAP - IT-BPM Industry", "https://ibpap.org/"),
            ("Trading Economics - Philippines", "https://tradingeconomics.com/philippines/indicators"),
            ("ADB - Philippines", "https://www.adb.org/countries/philippines/main"),
        ]
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


def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    total = 0
    for key in COUNTRIES:
        total += rewrite_country(key)
    print(f"\nDone! {total} articles rewritten.")

if __name__ == "__main__":
    main()
