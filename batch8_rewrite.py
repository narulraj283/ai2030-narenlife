#!/usr/bin/env python3
"""Batch 8: Mauritania, South Sudan, Mongolia, Cameroon, Bolivia, Ecuador, Guatemala, Dominican Republic, Honduras, Cuba"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from batch2_rewrite import gen_article, AUDIENCES, ARTICLES_DIR

COUNTRIES = {
    "mauritania": {
        "name": "Mauritania", "slug": "mauritania-mauritania", "population": "4.9 million",
        "gdp_per_capita": "$2,166", "gdp_per_capita_ppp": "$6,100", "gdp_growth": "4.8%",
        "currency": "MRU", "avg_monthly_salary": "MRU 12,000 (~$320 USD)",
        "avg_salary_usd": "$320", "minimum_wage": "MRU 3,000/month (~$80 USD)",
        "it_salary_range": "MRU 25,000-60,000/month (~$667-1,600 USD)",
        "manufacturing_salary": "MRU 8,000-15,000/month (~$213-400 USD)",
        "unemployment": "10.1%", "ai_adoption": "Minimal; limited digital infrastructure",
        "internet_penetration": "29%", "literacy_rate": "67%", "stem_graduates": "~2,000 annually",
        "labor_force": "1.5 million",
        "key_industries": "Iron ore mining, fishing, agriculture (livestock, dates), oil & gas (emerging), gold mining",
        "ai_risk_high": "Government clerical, basic data processing",
        "ai_risk_medium": "Mining monitoring, banking, telecom, fishing industry logistics",
        "ai_risk_low": "Pastoralism, fishing, artisanal mining, construction, healthcare, education",
        "key_challenges": "Slavery legacy and social inequality, desert climate limits agriculture, tribal/ethnic tensions, limited formal economy, infrastructure gaps, oil/gas dependent future, limited skilled workforce",
        "references": [("World Bank - Mauritania", "https://www.worldbank.org/en/country/mauritania/overview"), ("ONS Mauritania", "https://www.ons.mr/"), ("IMF - Mauritania", "https://www.imf.org/en/Countries/MRT"), ("Trading Economics - Mauritania", "https://tradingeconomics.com/mauritania/indicators"), ("African Development Bank - Mauritania", "https://www.afdb.org/en/countries/north-africa/mauritania")]
    },
    "south_sudan": {
        "name": "South Sudan", "slug": "south-sudan-south-sudan", "population": "11.4 million",
        "gdp_per_capita": "$421", "gdp_per_capita_ppp": "$800", "gdp_growth": "-0.3%",
        "currency": "SSP", "avg_monthly_salary": "SSP 50,000 (~$60 USD at market rate)",
        "avg_salary_usd": "$60", "minimum_wage": "No established minimum wage",
        "it_salary_range": "$200-$600/month (NGO/international sector)",
        "manufacturing_salary": "$30-$80/month",
        "unemployment": "12.7% (formal); vast underemployment",
        "ai_adoption": "Non-existent; world's newest and most fragile state",
        "internet_penetration": "8%", "literacy_rate": "35%", "stem_graduates": "~300 annually",
        "labor_force": "3.5 million",
        "key_industries": "Oil production (98% of government revenue), agriculture (subsistence), livestock, forestry, fishing",
        "ai_risk_high": "Almost no formal sector jobs exposed to AI",
        "ai_risk_medium": "Oil industry administration, NGO operations, government services",
        "ai_risk_low": "Subsistence farming, cattle herding, fishing, construction, petty trade, healthcare",
        "key_challenges": "Active civil conflict and ethnic violence, total oil dependency, catastrophic humanitarian crisis, near-zero infrastructure, 35% literacy, 8% internet, no functioning education system, massive displacement",
        "references": [("World Bank - South Sudan", "https://www.worldbank.org/en/country/southsudan/overview"), ("NBS South Sudan", "https://www.ssnbs.org/"), ("IMF - South Sudan", "https://www.imf.org/en/Countries/SSD"), ("UNDP - South Sudan", "https://www.undp.org/south-sudan"), ("African Development Bank - South Sudan", "https://www.afdb.org/en/countries/east-africa/south-sudan")]
    },
    "mongolia": {
        "name": "Mongolia", "slug": "mongolia-mongolia", "population": "3.4 million",
        "gdp_per_capita": "$5,024", "gdp_per_capita_ppp": "$14,500", "gdp_growth": "6.9%",
        "currency": "MNT", "avg_monthly_salary": "MNT 1,800,000 (~$525 USD)",
        "avg_salary_usd": "$525", "minimum_wage": "MNT 660,000/month (~$193 USD)",
        "it_salary_range": "MNT 3,000,000-8,000,000/month (~$875-2,335 USD)",
        "manufacturing_salary": "MNT 1,000,000-2,000,000/month (~$292-584 USD)",
        "unemployment": "5.8%", "ai_adoption": "Emerging; government digitization initiatives, Ulaanbaatar tech startups growing",
        "internet_penetration": "69%", "literacy_rate": "99%", "stem_graduates": "~6,000 annually",
        "labor_force": "1.3 million",
        "key_industries": "Mining (copper, gold, coal), agriculture (livestock — cashmere, meat), construction, tourism, financial services",
        "ai_risk_high": "Administrative services, data processing, customer service, basic banking operations",
        "ai_risk_medium": "Mining monitoring, retail, telecom, construction planning",
        "ai_risk_low": "Herding/livestock, skilled mining, construction labor, healthcare, education, tourism",
        "key_challenges": "Dutch disease from mining boom, extreme geographic isolation, harsh climate limits diversification, Ulaanbaatar over-concentration (50% of population), air pollution crisis, China/Russia economic dependency, small domestic market",
        "references": [("World Bank - Mongolia", "https://www.worldbank.org/en/country/mongolia/overview"), ("NSO Mongolia", "https://www.1212.mn/en"), ("IMF - Mongolia", "https://www.imf.org/en/Countries/MNG"), ("Trading Economics - Mongolia", "https://tradingeconomics.com/mongolia/indicators"), ("ADB - Mongolia", "https://www.adb.org/countries/mongolia/main")]
    },
    "cameroon": {
        "name": "Cameroon", "slug": "cameroon-cameroon", "population": "28.6 million",
        "gdp_per_capita": "$1,666", "gdp_per_capita_ppp": "$4,200", "gdp_growth": "4.0%",
        "currency": "XAF", "avg_monthly_salary": "XAF 120,000 (~$194 USD)",
        "avg_salary_usd": "$194", "minimum_wage": "XAF 41,875/month (~$68 USD)",
        "it_salary_range": "XAF 300,000-800,000/month (~$484-1,290 USD)",
        "manufacturing_salary": "XAF 70,000-150,000/month (~$113-242 USD)",
        "unemployment": "3.7%", "ai_adoption": "Low; growing tech scene in Douala and Yaoundé",
        "internet_penetration": "38%", "literacy_rate": "78%", "stem_graduates": "~15,000 annually",
        "labor_force": "11.5 million",
        "key_industries": "Oil production, agriculture (cocoa, coffee, bananas), timber, aluminum smelting, manufacturing, construction, telecom",
        "ai_risk_high": "Administrative services, basic data entry, customer service centers",
        "ai_risk_medium": "Banking, telecom, oil operations, retail, port logistics (Douala)",
        "ai_risk_low": "Farming, fishing, forestry, construction, healthcare, education, artisan crafts",
        "key_challenges": "Anglophone crisis/separatist conflict, Boko Haram in north, governance challenges, infrastructure gaps, power shortages, youth unemployment, bilingual administration complexity",
        "references": [("World Bank - Cameroon", "https://www.worldbank.org/en/country/cameroon/overview"), ("INS Cameroon", "https://www.ins-cameroun.cm/"), ("IMF - Cameroon", "https://www.imf.org/en/Countries/CMR"), ("Trading Economics - Cameroon", "https://tradingeconomics.com/cameroon/indicators"), ("African Development Bank - Cameroon", "https://www.afdb.org/en/countries/central-africa/cameroon")]
    },
    "bolivia": {
        "name": "Bolivia", "slug": "bolivia-bolivia", "population": "12.4 million",
        "gdp_per_capita": "$3,600", "gdp_per_capita_ppp": "$9,500", "gdp_growth": "1.8%",
        "currency": "BOB", "avg_monthly_salary": "BOB 4,500 (~$651 USD)",
        "avg_salary_usd": "$651", "minimum_wage": "BOB 2,362/month (~$342 USD)",
        "it_salary_range": "BOB 6,000-15,000/month (~$868-2,171 USD)",
        "manufacturing_salary": "BOB 3,000-6,000/month (~$434-868 USD)",
        "unemployment": "3.6%", "ai_adoption": "Low; limited tech ecosystem, growing mobile penetration",
        "internet_penetration": "66%", "literacy_rate": "94%", "stem_graduates": "~12,000 annually",
        "labor_force": "5.8 million",
        "key_industries": "Mining (tin, silver, lithium, zinc), natural gas, agriculture (soy, quinoa), manufacturing, construction",
        "ai_risk_high": "Administrative services, data processing, basic banking",
        "ai_risk_medium": "Mining operations, telecom, retail, natural gas monitoring",
        "ai_risk_low": "Smallholder farming, mining labor, construction, informal trade, healthcare, education",
        "key_challenges": "Lithium potential vs. extraction challenges, gas reserves declining, political instability, informal economy (>60%), landlocked geography, limited tech infrastructure, currency pressure",
        "references": [("World Bank - Bolivia", "https://www.worldbank.org/en/country/bolivia/overview"), ("INE Bolivia", "https://www.ine.gob.bo/"), ("IMF - Bolivia", "https://www.imf.org/en/Countries/BOL"), ("Trading Economics - Bolivia", "https://tradingeconomics.com/bolivia/indicators"), ("IDB - Bolivia", "https://www.iadb.org/en/countries/bolivia")]
    },
    "ecuador": {
        "name": "Ecuador", "slug": "ecuador-ecuador", "population": "18.2 million",
        "gdp_per_capita": "$6,400", "gdp_per_capita_ppp": "$12,800", "gdp_growth": "-0.2%",
        "currency": "USD (dollarized since 2000)", "avg_monthly_salary": "$550 USD",
        "avg_salary_usd": "$550", "minimum_wage": "$460/month (2024)",
        "it_salary_range": "$800-$2,500/month",
        "manufacturing_salary": "$460-$800/month",
        "unemployment": "3.4%", "ai_adoption": "Low; growing fintech and e-government initiatives",
        "internet_penetration": "76%", "literacy_rate": "94%", "stem_graduates": "~20,000 annually",
        "labor_force": "8.5 million",
        "key_industries": "Oil production, agriculture (bananas, shrimp, cacao, flowers), fishing, tourism, mining, manufacturing",
        "ai_risk_high": "Administrative services, basic banking, customer service, data entry",
        "ai_risk_medium": "Oil monitoring, agricultural processing, telecom, retail",
        "ai_risk_low": "Banana farming, fishing, flower cultivation, construction, healthcare, tourism, education",
        "key_challenges": "Security crisis (gang violence surge), oil dependency, dollarization limits monetary policy, fiscal constraints, Amazon deforestation pressures, political instability, informal economy (~45%)",
        "references": [("World Bank - Ecuador", "https://www.worldbank.org/en/country/ecuador/overview"), ("INEC Ecuador", "https://www.ecuadorencifras.gob.ec/"), ("IMF - Ecuador", "https://www.imf.org/en/Countries/ECU"), ("Trading Economics - Ecuador", "https://tradingeconomics.com/ecuador/indicators"), ("IDB - Ecuador", "https://www.iadb.org/en/countries/ecuador")]
    },
    "guatemala": {
        "name": "Guatemala", "slug": "guatemala-guatemala", "population": "17.6 million",
        "gdp_per_capita": "$5,476", "gdp_per_capita_ppp": "$10,300", "gdp_growth": "3.5%",
        "currency": "GTQ", "avg_monthly_salary": "GTQ 4,500 (~$580 USD)",
        "avg_salary_usd": "$580", "minimum_wage": "GTQ 3,268/month (~$421 USD) for non-agricultural; GTQ 3,165 for agricultural",
        "it_salary_range": "GTQ 8,000-25,000/month (~$1,032-3,226 USD)",
        "manufacturing_salary": "GTQ 3,200-6,000/month (~$413-774 USD)",
        "unemployment": "2.2%", "ai_adoption": "Low; growing BPO/call center sector, emerging fintech",
        "internet_penetration": "65%", "literacy_rate": "83%", "stem_graduates": "~10,000 annually",
        "labor_force": "7.2 million",
        "key_industries": "Agriculture (coffee, sugar, bananas, cardamom), textiles/apparel, BPO/call centers, remittances, tourism, construction",
        "ai_risk_high": "BPO/call center operations, textile quality control, administrative services",
        "ai_risk_medium": "Banking, retail, agricultural processing, telecom",
        "ai_risk_low": "Smallholder coffee farming, construction, informal trade, healthcare, education, tourism",
        "key_challenges": "Extreme inequality (highest Gini in Central America), indigenous exclusion, remittance dependency (18% of GDP), gang violence/migration, weak governance, malnutrition crisis, limited rural infrastructure",
        "references": [("World Bank - Guatemala", "https://www.worldbank.org/en/country/guatemala/overview"), ("INE Guatemala", "https://www.ine.gob.gt/"), ("IMF - Guatemala", "https://www.imf.org/en/Countries/GTM"), ("Trading Economics - Guatemala", "https://tradingeconomics.com/guatemala/indicators"), ("IDB - Guatemala", "https://www.iadb.org/en/countries/guatemala")]
    },
    "dominican_republic": {
        "name": "Dominican Republic", "slug": "dominican-republic-dominican-republic", "population": "11.3 million",
        "gdp_per_capita": "$10,260", "gdp_per_capita_ppp": "$22,500", "gdp_growth": "5.1%",
        "currency": "DOP", "avg_monthly_salary": "DOP 30,000 (~$510 USD)",
        "avg_salary_usd": "$510", "minimum_wage": "DOP 15,447-21,000/month (~$263-357 USD) depending on company size",
        "it_salary_range": "DOP 50,000-150,000/month (~$851-2,554 USD)",
        "manufacturing_salary": "DOP 18,000-35,000/month (~$306-596 USD)",
        "unemployment": "5.3%", "ai_adoption": "Moderate; growing tech sector, free trade zone digitization",
        "internet_penetration": "78%", "literacy_rate": "95%", "stem_graduates": "~15,000 annually",
        "labor_force": "5.0 million",
        "key_industries": "Tourism, free trade zones (manufacturing), agriculture (sugar, tobacco, cacao), mining (gold), construction, remittances, BPO services",
        "ai_risk_high": "Free trade zone assembly, BPO/call centers, hotel administration, data entry",
        "ai_risk_medium": "Banking, retail, tourism services, manufacturing quality control",
        "ai_risk_low": "Agriculture, construction, skilled tourism (guides), healthcare, education, artisan trades",
        "key_challenges": "Tourism over-reliance, inequality despite growth, Haitian immigration tensions, climate vulnerability (hurricanes), energy costs, education quality gaps, informal economy (~50%)",
        "references": [("World Bank - Dominican Republic", "https://www.worldbank.org/en/country/dominicanrepublic/overview"), ("ONE Dominican Republic", "https://www.one.gob.do/"), ("IMF - Dominican Republic", "https://www.imf.org/en/Countries/DOM"), ("Trading Economics - Dominican Republic", "https://tradingeconomics.com/dominican-republic/indicators"), ("IDB - Dominican Republic", "https://www.iadb.org/en/countries/dominican-republic")]
    },
    "honduras": {
        "name": "Honduras", "slug": "honduras-honduras", "population": "10.5 million",
        "gdp_per_capita": "$3,050", "gdp_per_capita_ppp": "$6,500", "gdp_growth": "3.5%",
        "currency": "HNL", "avg_monthly_salary": "HNL 12,000 (~$487 USD)",
        "avg_salary_usd": "$487", "minimum_wage": "HNL 8,882-13,091/month (~$360-531 USD) depending on sector and company size",
        "it_salary_range": "HNL 20,000-55,000/month (~$812-2,233 USD)",
        "manufacturing_salary": "HNL 9,000-15,000/month (~$365-609 USD)",
        "unemployment": "5.7%", "ai_adoption": "Low; growing BPO/maquila sector, limited tech ecosystem",
        "internet_penetration": "55%", "literacy_rate": "88%", "stem_graduates": "~7,000 annually",
        "labor_force": "4.6 million",
        "key_industries": "Textiles/maquila, agriculture (coffee, bananas, palm oil), BPO/call centers, remittances, shrimp farming, tourism",
        "ai_risk_high": "Maquila/textile assembly, BPO/call centers, administrative services",
        "ai_risk_medium": "Banking, retail, agricultural processing, telecom",
        "ai_risk_low": "Coffee farming, construction, fishing, informal trade, healthcare, education",
        "key_challenges": "Gang violence and insecurity, remittance dependency (25% of GDP), hurricane vulnerability, extreme inequality, migration/brain drain, weak institutions, maquila wage pressure",
        "references": [("World Bank - Honduras", "https://www.worldbank.org/en/country/honduras/overview"), ("INE Honduras", "https://www.ine.gob.hn/"), ("IMF - Honduras", "https://www.imf.org/en/Countries/HND"), ("Trading Economics - Honduras", "https://tradingeconomics.com/honduras/indicators"), ("IDB - Honduras", "https://www.iadb.org/en/countries/honduras")]
    },
    "cuba": {
        "name": "Cuba", "slug": "cuba-cuba", "population": "11.1 million",
        "gdp_per_capita": "$9,500 (estimated; limited data)", "gdp_per_capita_ppp": "$12,300 (estimated)",
        "gdp_growth": "1.8% (estimated)", "currency": "CUP (Cuban Peso)",
        "avg_monthly_salary": "CUP 4,200 (~$35 USD at official rate; ~$15-20 at informal rate)",
        "avg_salary_usd": "$35 (official); real purchasing power much lower",
        "minimum_wage": "CUP 2,100/month (~$17.50 USD at official rate)",
        "it_salary_range": "CUP 6,000-15,000/month; state employment dominates",
        "manufacturing_salary": "CUP 3,500-6,000/month",
        "unemployment": "1.4% (official); massive underemployment in state sector",
        "ai_adoption": "Minimal; severely restricted internet, limited hardware access",
        "internet_penetration": "71% (mobile data since 2018, but slow/expensive/censored)",
        "literacy_rate": "99%", "stem_graduates": "~25,000 annually (strong education system)",
        "labor_force": "5.0 million",
        "key_industries": "Tourism, sugar, tobacco (cigars), nickel mining, pharmaceuticals/biotech, agriculture, rum production",
        "ai_risk_high": "State administrative bureaucracy, sugar processing automation",
        "ai_risk_medium": "Tourism services, banking (state), telecom, pharmaceutical production",
        "ai_risk_low": "Agriculture, tobacco cultivation, construction, healthcare, education, artisan crafts",
        "key_challenges": "US embargo limits technology access, centrally planned economy restricts private sector, severe economic crisis (food/fuel shortages), mass emigration (700K+ left 2022-2024), internet censorship and speed, dual currency aftermath, aging population",
        "references": [("World Bank - Cuba", "https://www.worldbank.org/en/country/cuba"), ("ONEI Cuba", "https://www.onei.gob.cu/"), ("Trading Economics - Cuba", "https://tradingeconomics.com/cuba/indicators"), ("Brookings - Cuba Economy", "https://www.brookings.edu/topics/cuba/"), ("ECLAC - Cuba", "https://www.cepal.org/en/topics/cuba")]
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
