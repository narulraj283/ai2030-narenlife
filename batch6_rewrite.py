#!/usr/bin/env python3
"""Batch 6: Senegal, Rwanda, Tunisia, Zambia, Cote d'Ivoire, Niger, Burkina Faso, Mali, Chad, Somalia"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from batch2_rewrite import gen_article, AUDIENCES, ARTICLES_DIR

COUNTRIES = {
    "senegal": {
        "name": "Senegal", "slug": "senegal-senegal", "population": "18.3 million",
        "gdp_per_capita": "$1,691", "gdp_per_capita_ppp": "$4,100", "gdp_growth": "8.8%",
        "currency": "XOF", "avg_monthly_salary": "XOF 150,000 (~$245 USD)",
        "avg_salary_usd": "$245", "minimum_wage": "XOF 58,900/month (~$96 USD)",
        "it_salary_range": "XOF 300,000-900,000/month (~$490-1,470 USD)",
        "manufacturing_salary": "XOF 80,000-150,000/month (~$130-245 USD)",
        "unemployment": "3.6%", "ai_adoption": "Emerging; Dakar tech hub growing rapidly",
        "internet_penetration": "58%", "literacy_rate": "56%", "stem_graduates": "~12,000 annually",
        "labor_force": "5.2 million",
        "key_industries": "Agriculture (peanuts, fishing), phosphate mining, tourism, construction, telecom, oil & gas (emerging)",
        "ai_risk_high": "Administrative services, basic data entry, call centers",
        "ai_risk_medium": "Banking, telecom operations, retail services",
        "ai_risk_low": "Agriculture, fishing, construction, healthcare, artisan crafts, mining",
        "key_challenges": "Low literacy limits digital workforce readiness, infrastructure gaps outside Dakar, brain drain of tech talent, energy access challenges, informal economy dominates",
        "references": [("World Bank - Senegal", "https://www.worldbank.org/en/country/senegal/overview"), ("ANSD Senegal", "https://www.ansd.sn/"), ("IMF - Senegal", "https://www.imf.org/en/Countries/SEN"), ("Trading Economics - Senegal", "https://tradingeconomics.com/senegal/indicators"), ("African Development Bank - Senegal", "https://www.afdb.org/en/countries/west-africa/senegal")]
    },
    "rwanda": {
        "name": "Rwanda", "slug": "rwanda-rwanda", "population": "14.3 million",
        "gdp_per_capita": "$966", "gdp_per_capita_ppp": "$2,900", "gdp_growth": "8.2%",
        "currency": "RWF", "avg_monthly_salary": "RWF 120,000 (~$95 USD)",
        "avg_salary_usd": "$95", "minimum_wage": "No national minimum wage; sector-specific minimums",
        "it_salary_range": "RWF 400,000-1,500,000/month (~$315-1,180 USD)",
        "manufacturing_salary": "RWF 60,000-150,000/month (~$47-118 USD)",
        "unemployment": "15.5%", "ai_adoption": "Growing; government-led digitization (Irembo platform, smart city initiatives)",
        "internet_penetration": "36%", "literacy_rate": "75%", "stem_graduates": "~8,000 annually",
        "labor_force": "6.8 million",
        "key_industries": "Agriculture (coffee, tea), mining (tin, tantalum), tourism, ICT services, construction, financial services",
        "ai_risk_high": "Administrative services, data processing, basic customer service",
        "ai_risk_medium": "Banking, telecom, retail, tourism operations",
        "ai_risk_low": "Agriculture, mining, construction, healthcare, education, handicrafts",
        "key_challenges": "Small domestic market limits AI scale, limited internet outside Kigali, skills gap in advanced tech, energy costs, landlocked geography increases costs",
        "references": [("World Bank - Rwanda", "https://www.worldbank.org/en/country/rwanda/overview"), ("NISR Rwanda", "https://www.statistics.gov.rw/"), ("IMF - Rwanda", "https://www.imf.org/en/Countries/RWA"), ("Rwanda ICT Chamber", "https://ictchamber.rw/"), ("African Development Bank - Rwanda", "https://www.afdb.org/en/countries/east-africa/rwanda")]
    },
    "tunisia": {
        "name": "Tunisia", "slug": "tunisia-tunisia", "population": "12.5 million",
        "gdp_per_capita": "$3,895", "gdp_per_capita_ppp": "$11,800", "gdp_growth": "1.2%",
        "currency": "TND", "avg_monthly_salary": "TND 1,100 (~$355 USD)",
        "avg_salary_usd": "$355", "minimum_wage": "TND 480/month (~$155 USD) for 48-hour week",
        "it_salary_range": "TND 2,000-5,000/month (~$645-1,615 USD)",
        "manufacturing_salary": "TND 700-1,200/month (~$226-387 USD)",
        "unemployment": "15.8%", "ai_adoption": "Moderate; strong tech talent pipeline, nearshore IT hub for Europe",
        "internet_penetration": "72%", "literacy_rate": "82%", "stem_graduates": "~30,000 annually",
        "labor_force": "4.2 million",
        "key_industries": "Manufacturing (textiles, automotive parts), phosphate mining, tourism, agriculture (olive oil), IT offshoring, energy",
        "ai_risk_high": "Textile assembly, call center operations, administrative roles, basic manufacturing",
        "ai_risk_medium": "Banking, tourism services, retail, automotive parts assembly",
        "ai_risk_low": "Olive agriculture, skilled trades, healthcare, education, artisan crafts",
        "key_challenges": "High youth unemployment (35%+), political instability, brain drain to Europe, fiscal constraints limit investment, regional development disparities",
        "references": [("World Bank - Tunisia", "https://www.worldbank.org/en/country/tunisia/overview"), ("INS Tunisia", "https://www.ins.tn/"), ("IMF - Tunisia", "https://www.imf.org/en/Countries/TUN"), ("Trading Economics - Tunisia", "https://tradingeconomics.com/tunisia/indicators"), ("African Development Bank - Tunisia", "https://www.afdb.org/en/countries/north-africa/tunisia")]
    },
    "zambia": {
        "name": "Zambia", "slug": "zambia-zambia", "population": "20.6 million",
        "gdp_per_capita": "$1,284", "gdp_per_capita_ppp": "$3,800", "gdp_growth": "4.7%",
        "currency": "ZMW", "avg_monthly_salary": "ZMW 5,500 (~$210 USD)",
        "avg_salary_usd": "$210", "minimum_wage": "ZMW 1,698/month (~$65 USD)",
        "it_salary_range": "ZMW 12,000-35,000/month (~$460-1,340 USD)",
        "manufacturing_salary": "ZMW 3,000-7,000/month (~$115-268 USD)",
        "unemployment": "12.5%", "ai_adoption": "Low; emerging fintech sector leading adoption",
        "internet_penetration": "33%", "literacy_rate": "87%", "stem_graduates": "~7,000 annually",
        "labor_force": "7.5 million",
        "key_industries": "Copper mining, agriculture (maize, tobacco), tourism, construction, energy, financial services",
        "ai_risk_high": "Administrative support, basic data processing, routine banking tasks",
        "ai_risk_medium": "Mining operations (monitoring), retail, telecom services",
        "ai_risk_low": "Smallholder farming, skilled mining, construction, healthcare, education, tourism",
        "key_challenges": "Copper price dependency creates economic volatility, power supply deficits, debt restructuring aftermath, limited digital infrastructure outside Lusaka, informal economy (85%+)",
        "references": [("World Bank - Zambia", "https://www.worldbank.org/en/country/zambia/overview"), ("ZamStats", "https://www.zamstats.gov.zm/"), ("IMF - Zambia", "https://www.imf.org/en/Countries/ZMB"), ("Trading Economics - Zambia", "https://tradingeconomics.com/zambia/indicators"), ("African Development Bank - Zambia", "https://www.afdb.org/en/countries/southern-africa/zambia")]
    },
    "cote_d_ivoire": {
        "name": "Côte d'Ivoire", "slug": "cote-d-ivoire-cote-d-ivoire", "population": "30 million",
        "gdp_per_capita": "$2,549", "gdp_per_capita_ppp": "$6,600", "gdp_growth": "6.5%",
        "currency": "XOF", "avg_monthly_salary": "XOF 180,000 (~$295 USD)",
        "avg_salary_usd": "$295", "minimum_wage": "XOF 75,000/month (~$123 USD)",
        "it_salary_range": "XOF 350,000-1,000,000/month (~$570-1,635 USD)",
        "manufacturing_salary": "XOF 100,000-200,000/month (~$163-327 USD)",
        "unemployment": "3.4%", "ai_adoption": "Emerging; Abidjan becoming West African tech hub",
        "internet_penetration": "45%", "literacy_rate": "53%", "stem_graduates": "~15,000 annually",
        "labor_force": "10.2 million",
        "key_industries": "Cocoa (world's largest producer), agriculture (cashews, rubber), oil refining, mining (gold), construction, telecom",
        "ai_risk_high": "Administrative services, basic processing, customer service centers",
        "ai_risk_medium": "Banking, telecom, retail, cocoa processing automation",
        "ai_risk_low": "Cocoa farming, mining, construction, healthcare, fishing, artisan crafts",
        "key_challenges": "Low literacy rate limits workforce readiness, infrastructure gaps, cocoa sector modernization pressures, climate change threatens agriculture, regional security concerns",
        "references": [("World Bank - Côte d'Ivoire", "https://www.worldbank.org/en/country/cotedivoire/overview"), ("INS Côte d'Ivoire", "https://www.ins.ci/"), ("IMF - Côte d'Ivoire", "https://www.imf.org/en/Countries/CIV"), ("Trading Economics - Côte d'Ivoire", "https://tradingeconomics.com/ivory-coast/indicators"), ("African Development Bank - Côte d'Ivoire", "https://www.afdb.org/en/countries/west-africa/cote-divoire")]
    },
    "niger": {
        "name": "Niger", "slug": "niger-niger", "population": "27.2 million",
        "gdp_per_capita": "$560", "gdp_per_capita_ppp": "$1,400", "gdp_growth": "2.0%",
        "currency": "XOF", "avg_monthly_salary": "XOF 55,000 (~$90 USD)",
        "avg_salary_usd": "$90", "minimum_wage": "XOF 42,000/month (~$69 USD)",
        "it_salary_range": "XOF 200,000-500,000/month (~$327-818 USD)",
        "manufacturing_salary": "XOF 45,000-80,000/month (~$74-131 USD)",
        "unemployment": "0.5% (formal); vast underemployment in informal sector",
        "ai_adoption": "Minimal; extremely limited digital infrastructure",
        "internet_penetration": "14%", "literacy_rate": "35%", "stem_graduates": "~3,000 annually",
        "labor_force": "8.5 million",
        "key_industries": "Uranium mining, agriculture (millet, sorghum), livestock, oil (emerging), gold mining, informal trade",
        "ai_risk_high": "Basic clerical work in government, simple data processing",
        "ai_risk_medium": "Mining monitoring, telecom operations, banking services",
        "ai_risk_low": "Subsistence farming, pastoralism, artisan mining, construction, healthcare, teaching",
        "key_challenges": "Lowest HDI country in the world, 35% literacy severely limits digital workforce, political instability (2023 coup), Sahel security crisis, climate change (desertification), extreme poverty (>40%)",
        "references": [("World Bank - Niger", "https://www.worldbank.org/en/country/niger/overview"), ("INS Niger", "https://www.stat-niger.org/"), ("IMF - Niger", "https://www.imf.org/en/Countries/NER"), ("UNDP - Niger", "https://www.undp.org/niger"), ("African Development Bank - Niger", "https://www.afdb.org/en/countries/west-africa/niger")]
    },
    "burkina_faso": {
        "name": "Burkina Faso", "slug": "burkina-faso-burkina-faso", "population": "23.3 million",
        "gdp_per_capita": "$831", "gdp_per_capita_ppp": "$2,300", "gdp_growth": "3.6%",
        "currency": "XOF", "avg_monthly_salary": "XOF 75,000 (~$123 USD)",
        "avg_salary_usd": "$123", "minimum_wage": "XOF 45,000/month (~$74 USD)",
        "it_salary_range": "XOF 250,000-600,000/month (~$409-981 USD)",
        "manufacturing_salary": "XOF 55,000-100,000/month (~$90-163 USD)",
        "unemployment": "4.7%", "ai_adoption": "Minimal; limited connectivity and digital infrastructure",
        "internet_penetration": "21%", "literacy_rate": "46%", "stem_graduates": "~5,000 annually",
        "labor_force": "8.8 million",
        "key_industries": "Gold mining, cotton, agriculture (sorghum, millet), livestock, artisanal mining, informal trade",
        "ai_risk_high": "Government clerical work, basic administrative tasks",
        "ai_risk_medium": "Mining operations, banking, telecom services",
        "ai_risk_low": "Smallholder farming, livestock herding, construction, artisan mining, healthcare, education",
        "key_challenges": "Political instability (military government since 2022), Sahel security crisis displacing millions, low literacy, severe infrastructure gaps, climate vulnerability, heavy aid dependency",
        "references": [("World Bank - Burkina Faso", "https://www.worldbank.org/en/country/burkinafaso/overview"), ("INSD Burkina Faso", "https://www.insd.bf/"), ("IMF - Burkina Faso", "https://www.imf.org/en/Countries/BFA"), ("UNDP - Burkina Faso", "https://www.undp.org/burkina-faso"), ("African Development Bank - Burkina Faso", "https://www.afdb.org/en/countries/west-africa/burkina-faso")]
    },
    "mali": {
        "name": "Mali", "slug": "mali-mali", "population": "23.3 million",
        "gdp_per_capita": "$862", "gdp_per_capita_ppp": "$2,500", "gdp_growth": "3.7%",
        "currency": "XOF", "avg_monthly_salary": "XOF 80,000 (~$131 USD)",
        "avg_salary_usd": "$131", "minimum_wage": "XOF 40,000/month (~$65 USD)",
        "it_salary_range": "XOF 250,000-600,000/month (~$409-981 USD)",
        "manufacturing_salary": "XOF 55,000-100,000/month (~$90-163 USD)",
        "unemployment": "7.4%", "ai_adoption": "Minimal; very limited digital infrastructure outside Bamako",
        "internet_penetration": "33%", "literacy_rate": "31%", "stem_graduates": "~4,000 annually",
        "labor_force": "7.5 million",
        "key_industries": "Gold mining (3rd largest in Africa), cotton, agriculture (rice, millet), livestock, fishing, artisanal crafts",
        "ai_risk_high": "Government administration, basic data processing",
        "ai_risk_medium": "Banking, telecom, mining monitoring systems",
        "ai_risk_low": "Farming, pastoralism, fishing, construction, artisan crafts, healthcare, education",
        "key_challenges": "Military government (coup in 2020/2021), ongoing conflict in northern regions, one of lowest literacy rates globally, extreme poverty, infrastructure gaps, climate change (desertification)",
        "references": [("World Bank - Mali", "https://www.worldbank.org/en/country/mali/overview"), ("INSTAT Mali", "https://www.instat-mali.org/"), ("IMF - Mali", "https://www.imf.org/en/Countries/MLI"), ("UNDP - Mali", "https://www.undp.org/mali"), ("African Development Bank - Mali", "https://www.afdb.org/en/countries/west-africa/mali")]
    },
    "chad": {
        "name": "Chad", "slug": "chad-chad", "population": "18.3 million",
        "gdp_per_capita": "$716", "gdp_per_capita_ppp": "$1,700", "gdp_growth": "3.7%",
        "currency": "XAF", "avg_monthly_salary": "XAF 70,000 (~$113 USD)",
        "avg_salary_usd": "$113", "minimum_wage": "XAF 60,000/month (~$97 USD)",
        "it_salary_range": "XAF 200,000-500,000/month (~$323-807 USD)",
        "manufacturing_salary": "XAF 60,000-100,000/month (~$97-161 USD)",
        "unemployment": "1.9% (formal); massive underemployment",
        "ai_adoption": "Minimal; among world's least connected countries",
        "internet_penetration": "13%", "literacy_rate": "27%", "stem_graduates": "~2,000 annually",
        "labor_force": "6.0 million",
        "key_industries": "Oil production, cotton, livestock, agriculture (sorghum, millet), gum arabic, natron mining",
        "ai_risk_high": "Government clerical roles, basic oil industry administration",
        "ai_risk_medium": "Oil operations monitoring, banking, telecom",
        "ai_risk_low": "Pastoralism, subsistence farming, fishing, construction, healthcare, artisan trades",
        "key_challenges": "One of lowest literacy rates globally (27%), minimal internet access, political instability, oil price dependency, climate change (Lake Chad shrinking), extreme poverty (>40%), almost no tech infrastructure",
        "references": [("World Bank - Chad", "https://www.worldbank.org/en/country/chad/overview"), ("INSEED Chad", "https://www.inseed-td.net/"), ("IMF - Chad", "https://www.imf.org/en/Countries/TCD"), ("UNDP - Chad", "https://www.undp.org/chad"), ("African Development Bank - Chad", "https://www.afdb.org/en/countries/central-africa/chad")]
    },
    "somalia": {
        "name": "Somalia", "slug": "somalia-somalia", "population": "18.1 million",
        "gdp_per_capita": "$548", "gdp_per_capita_ppp": "$1,300", "gdp_growth": "3.7%",
        "currency": "SOS", "avg_monthly_salary": "SOS 150,000 (~$265 USD) in formal sector",
        "avg_salary_usd": "$265 (formal sector)", "minimum_wage": "No enforced national minimum wage",
        "it_salary_range": "$300-$900/month in Mogadishu",
        "manufacturing_salary": "$80-$200/month",
        "unemployment": "19.8%", "ai_adoption": "Minimal; but mobile money (Zaad/EVC Plus) is highly advanced",
        "internet_penetration": "20%", "literacy_rate": "40%", "stem_graduates": "~3,000 annually",
        "labor_force": "4.8 million",
        "key_industries": "Livestock, agriculture (bananas, sorghum), fishing, telecom, remittances, construction, mobile money",
        "ai_risk_high": "Basic administrative work, simple bookkeeping",
        "ai_risk_medium": "Telecom operations, mobile money services, banking",
        "ai_risk_low": "Pastoralism, farming, fishing, construction, small trade, healthcare, education",
        "key_challenges": "Ongoing conflict and al-Shabaab insurgency, clan-based governance fragmentation, no reliable national statistics, extremely limited formal economy, climate change (droughts), diaspora dependency for skills",
        "references": [("World Bank - Somalia", "https://www.worldbank.org/en/country/somalia/overview"), ("Somalia National Bureau of Statistics", "https://www.nbs.gov.so/"), ("IMF - Somalia", "https://www.imf.org/en/Countries/SOM"), ("UNDP - Somalia", "https://www.undp.org/somalia"), ("African Development Bank - Somalia", "https://www.afdb.org/en/countries/east-africa/somalia")]
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
            # try alternate patterns
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
