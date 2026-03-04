#!/usr/bin/env python3
"""Batch 9: Jamaica, Haiti, Venezuela, Paraguay, Nicaragua, El Salvador, Papua New Guinea, Laos, Tajikistan, Kyrgyzstan"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from batch2_rewrite import gen_article, AUDIENCES, ARTICLES_DIR

COUNTRIES = {
    "jamaica": {
        "name": "Jamaica", "slug": "jamaica-jamaica", "population": "2.8 million",
        "gdp_per_capita": "$6,047", "gdp_per_capita_ppp": "$12,400", "gdp_growth": "2.2%",
        "currency": "JMD", "avg_monthly_salary": "JMD 180,000 (~$1,160 USD)",
        "avg_salary_usd": "$1,160", "minimum_wage": "JMD 13,000/week (~$335/month USD)",
        "it_salary_range": "JMD 250,000-600,000/month (~$1,613-3,871 USD)",
        "manufacturing_salary": "JMD 120,000-220,000/month (~$774-1,419 USD)",
        "unemployment": "4.5%", "ai_adoption": "Low; growing BPO sector, fintech emerging",
        "internet_penetration": "82%", "literacy_rate": "88%", "stem_graduates": "~3,000 annually",
        "labor_force": "1.4 million",
        "key_industries": "Tourism, BPO/call centers, agriculture (sugar, coffee, bananas), mining (bauxite/alumina), manufacturing, remittances",
        "ai_risk_high": "BPO/call center operations, hotel administration, data entry, basic banking",
        "ai_risk_medium": "Tourism services, retail, telecom, manufacturing quality control",
        "ai_risk_low": "Agriculture, construction, skilled tourism, healthcare, education, creative industries (music)",
        "key_challenges": "High public debt (~80% of GDP), crime and violence, brain drain to US/UK/Canada, hurricane vulnerability, energy costs (imported fuel), small domestic market",
        "references": [("World Bank - Jamaica", "https://www.worldbank.org/en/country/jamaica/overview"), ("STATIN Jamaica", "https://statinja.gov.jm/"), ("IMF - Jamaica", "https://www.imf.org/en/Countries/JAM"), ("Trading Economics - Jamaica", "https://tradingeconomics.com/jamaica/indicators"), ("IDB - Jamaica", "https://www.iadb.org/en/countries/jamaica")]
    },
    "haiti": {
        "name": "Haiti", "slug": "haiti-haiti", "population": "11.7 million",
        "gdp_per_capita": "$1,748", "gdp_per_capita_ppp": "$3,000", "gdp_growth": "-1.9%",
        "currency": "HTG", "avg_monthly_salary": "HTG 18,000 (~$135 USD)",
        "avg_salary_usd": "$135", "minimum_wage": "HTG 685/day (~$5.10 USD) for textile sector",
        "it_salary_range": "HTG 50,000-150,000/month (~$375-1,125 USD)",
        "manufacturing_salary": "HTG 15,000-30,000/month (~$113-225 USD)",
        "unemployment": "14.6%", "ai_adoption": "Non-existent; state collapse precludes any digital development",
        "internet_penetration": "39%", "literacy_rate": "62%", "stem_graduates": "~2,000 annually",
        "labor_force": "4.9 million",
        "key_industries": "Textiles/garment assembly (free trade zones), agriculture (coffee, mangoes), remittances, construction, informal trade",
        "ai_risk_high": "Textile assembly (limited automation already occurring)",
        "ai_risk_medium": "Telecom, basic banking, garment quality inspection",
        "ai_risk_low": "Subsistence farming, informal trade, construction, healthcare, education, fishing",
        "key_challenges": "Gang control of Port-au-Prince, state collapse/no functioning government, catastrophic infrastructure, earthquake/hurricane reconstruction stalled, mass emigration, extreme poverty (60%+), health system collapse",
        "references": [("World Bank - Haiti", "https://www.worldbank.org/en/country/haiti/overview"), ("IHSI Haiti", "https://www.ihsi.ht/"), ("IMF - Haiti", "https://www.imf.org/en/Countries/HTI"), ("UNDP - Haiti", "https://www.undp.org/haiti"), ("IDB - Haiti", "https://www.iadb.org/en/countries/haiti")]
    },
    "venezuela": {
        "name": "Venezuela", "slug": "venezuela-venezuela", "population": "28.4 million",
        "gdp_per_capita": "$3,740 (estimated)", "gdp_per_capita_ppp": "$7,000 (estimated)",
        "gdp_growth": "4.0% (recovery from 75% GDP decline 2014-2021)",
        "currency": "VES (Bolívar Digital); economy largely dollarized informally",
        "avg_monthly_salary": "$80-$150 USD (public sector); $200-$500 (private)",
        "avg_salary_usd": "$150 (average); highly bifurcated economy",
        "minimum_wage": "VES 130/month (~$3.60 USD) — one of world's lowest; supplemented with bonuses",
        "it_salary_range": "$400-$1,500/month (private sector, often USD-paid)",
        "manufacturing_salary": "$100-$300/month",
        "unemployment": "40%+ (estimated; official data unreliable)",
        "ai_adoption": "Minimal; collapsed infrastructure, but diaspora tech talent exists",
        "internet_penetration": "72% (but quality extremely poor)", "literacy_rate": "97%",
        "stem_graduates": "~20,000 annually (pre-crisis; declining rapidly)",
        "labor_force": "12.0 million (pre-emigration; 7M+ have left)",
        "key_industries": "Oil (largest reserves globally), gold mining, agriculture, informal economy, remittances, petrochemicals",
        "ai_risk_high": "State oil company administration, government bureaucracy",
        "ai_risk_medium": "Banking, telecom, oil monitoring systems, retail",
        "ai_risk_low": "Informal trade, agriculture, mining, construction, healthcare, education",
        "key_challenges": "Economic collapse (75% GDP loss), hyperinflation aftermath, 7M+ emigrated, oil infrastructure decay, US sanctions, authoritarian governance, brain drain, healthcare system collapse",
        "references": [("World Bank - Venezuela", "https://www.worldbank.org/en/country/venezuela"), ("IMF - Venezuela", "https://www.imf.org/en/Countries/VEN"), ("Trading Economics - Venezuela", "https://tradingeconomics.com/venezuela/indicators"), ("Brookings - Venezuela", "https://www.brookings.edu/topics/venezuela/"), ("UNHCR - Venezuela", "https://www.unhcr.org/venezuela-emergency.html")]
    },
    "paraguay": {
        "name": "Paraguay", "slug": "paraguay-paraguay", "population": "6.9 million",
        "gdp_per_capita": "$6,110", "gdp_per_capita_ppp": "$14,500", "gdp_growth": "4.7%",
        "currency": "PYG", "avg_monthly_salary": "PYG 4,500,000 (~$610 USD)",
        "avg_salary_usd": "$610", "minimum_wage": "PYG 2,680,373/month (~$363 USD)",
        "it_salary_range": "PYG 7,000,000-18,000,000/month (~$949-2,441 USD)",
        "manufacturing_salary": "PYG 3,000,000-5,500,000/month (~$407-746 USD)",
        "unemployment": "5.6%", "ai_adoption": "Low; growing fintech sector, cheap electricity attracting crypto/data centers",
        "internet_penetration": "78%", "literacy_rate": "94%", "stem_graduates": "~8,000 annually",
        "labor_force": "3.6 million",
        "key_industries": "Agriculture (soybeans, beef), hydroelectric power (Itaipu), manufacturing, construction, re-export trade (Ciudad del Este)",
        "ai_risk_high": "Administrative services, data processing, basic banking, re-export logistics",
        "ai_risk_medium": "Agricultural processing, retail, telecom, manufacturing",
        "ai_risk_low": "Farming, cattle ranching, construction, hydroelectric operations, healthcare, education",
        "key_challenges": "Soybean/beef dependency, inequality, landlocked geography, informal economy (~40%), governance/corruption concerns, deforestation in Chaco, limited tech ecosystem, bilingual (Guaraní-Spanish) complexity",
        "references": [("World Bank - Paraguay", "https://www.worldbank.org/en/country/paraguay/overview"), ("DGEEC Paraguay", "https://www.ine.gov.py/"), ("IMF - Paraguay", "https://www.imf.org/en/Countries/PRY"), ("Trading Economics - Paraguay", "https://tradingeconomics.com/paraguay/indicators"), ("IDB - Paraguay", "https://www.iadb.org/en/countries/paraguay")]
    },
    "nicaragua": {
        "name": "Nicaragua", "slug": "nicaragua-nicaragua", "population": "7.0 million",
        "gdp_per_capita": "$2,280", "gdp_per_capita_ppp": "$6,400", "gdp_growth": "3.8%",
        "currency": "NIO", "avg_monthly_salary": "NIO 14,000 (~$380 USD)",
        "avg_salary_usd": "$380", "minimum_wage": "NIO 5,854-13,672/month (~$159-371 USD) depending on sector",
        "it_salary_range": "NIO 20,000-55,000/month (~$543-1,493 USD)",
        "manufacturing_salary": "NIO 8,000-15,000/month (~$217-407 USD)",
        "unemployment": "3.3%", "ai_adoption": "Low; limited tech ecosystem, growing BPO sector",
        "internet_penetration": "57%", "literacy_rate": "83%", "stem_graduates": "~5,000 annually",
        "labor_force": "3.2 million",
        "key_industries": "Agriculture (coffee, beef, sugar, tobacco), free trade zone manufacturing (textiles), BPO, gold mining, remittances, tourism",
        "ai_risk_high": "Free trade zone assembly, BPO operations, administrative services",
        "ai_risk_medium": "Banking, telecom, retail, agricultural processing",
        "ai_risk_low": "Coffee farming, cattle ranching, gold mining, construction, healthcare, education, informal trade",
        "key_challenges": "Authoritarian governance limiting investment, US/EU sanctions, mass emigration, remittance dependency, hurricane vulnerability, limited press freedom, shrinking civic space",
        "references": [("World Bank - Nicaragua", "https://www.worldbank.org/en/country/nicaragua/overview"), ("INIDE Nicaragua", "https://www.inide.gob.ni/"), ("IMF - Nicaragua", "https://www.imf.org/en/Countries/NIC"), ("Trading Economics - Nicaragua", "https://tradingeconomics.com/nicaragua/indicators"), ("IDB - Nicaragua", "https://www.iadb.org/en/countries/nicaragua")]
    },
    "el_salvador": {
        "name": "El Salvador", "slug": "el-salvador-el-salvador", "population": "6.3 million",
        "gdp_per_capita": "$5,129", "gdp_per_capita_ppp": "$10,800", "gdp_growth": "3.5%",
        "currency": "USD (dollarized since 2001; Bitcoin legal tender since 2021)",
        "avg_monthly_salary": "$500 USD",
        "avg_salary_usd": "$500", "minimum_wage": "$365/month (commerce/services sector, 2024)",
        "it_salary_range": "$800-$2,500/month",
        "manufacturing_salary": "$365-$700/month",
        "unemployment": "5.8%", "ai_adoption": "Low; but Bitcoin adoption created some fintech infrastructure",
        "internet_penetration": "63%", "literacy_rate": "89%", "stem_graduates": "~6,000 annually",
        "labor_force": "2.9 million",
        "key_industries": "Textiles/maquila, agriculture (coffee, sugar), BPO/call centers, remittances (24% of GDP), tourism, construction",
        "ai_risk_high": "Maquila assembly, BPO/call centers, administrative services",
        "ai_risk_medium": "Banking, retail, telecom, agricultural processing",
        "ai_risk_low": "Coffee farming, construction, informal trade, healthcare, education, tourism services",
        "key_challenges": "Gang crackdown (state of exception since 2022 — mass incarceration), remittance dependency, Bitcoin experiment uncertainty, migration/brain drain, small domestic market, climate vulnerability",
        "references": [("World Bank - El Salvador", "https://www.worldbank.org/en/country/elsalvador/overview"), ("DIGESTYC El Salvador", "https://www.digestyc.gob.sv/"), ("IMF - El Salvador", "https://www.imf.org/en/Countries/SLV"), ("Trading Economics - El Salvador", "https://tradingeconomics.com/el-salvador/indicators"), ("IDB - El Salvador", "https://www.iadb.org/en/countries/el-salvador")]
    },
    "papua_new_guinea": {
        "name": "Papua New Guinea", "slug": "papua-new-guinea-papua-new-guinea", "population": "10.3 million",
        "gdp_per_capita": "$2,845", "gdp_per_capita_ppp": "$4,300", "gdp_growth": "3.0%",
        "currency": "PGK", "avg_monthly_salary": "PGK 2,500 (~$650 USD) in formal sector",
        "avg_salary_usd": "$650 (formal sector; 85% are in subsistence economy)",
        "minimum_wage": "PGK 3.50/hour (~$0.91 USD)",
        "it_salary_range": "PGK 5,000-15,000/month (~$1,300-3,900 USD)",
        "manufacturing_salary": "PGK 1,500-3,000/month (~$390-780 USD)",
        "unemployment": "2.5% (formal); 85% in subsistence economy",
        "ai_adoption": "Minimal; extremely limited connectivity outside Port Moresby",
        "internet_penetration": "15%", "literacy_rate": "64%", "stem_graduates": "~2,000 annually",
        "labor_force": "4.0 million",
        "key_industries": "Mining (gold, copper), LNG, agriculture (palm oil, coffee, cocoa), forestry, fishing, construction",
        "ai_risk_high": "Mining administration, government clerical, basic data processing",
        "ai_risk_medium": "LNG operations monitoring, banking, telecom",
        "ai_risk_low": "Subsistence farming, fishing, artisanal mining, construction, healthcare, education, forestry",
        "key_challenges": "800+ languages (most linguistically diverse country), extreme geographic isolation, tribal violence, 85% subsistence economy, infrastructure nearly non-existent outside cities, resource curse dynamics, climate vulnerability",
        "references": [("World Bank - PNG", "https://www.worldbank.org/en/country/png/overview"), ("NSO PNG", "https://www.nso.gov.pg/"), ("IMF - PNG", "https://www.imf.org/en/Countries/PNG"), ("ADB - PNG", "https://www.adb.org/countries/papua-new-guinea/main"), ("Trading Economics - PNG", "https://tradingeconomics.com/papua-new-guinea/indicators")]
    },
    "laos": {
        "name": "Laos", "slug": "laos-laos", "population": "7.6 million",
        "gdp_per_capita": "$2,054", "gdp_per_capita_ppp": "$9,000", "gdp_growth": "4.0%",
        "currency": "LAK", "avg_monthly_salary": "LAK 4,000,000 (~$190 USD)",
        "avg_salary_usd": "$190", "minimum_wage": "LAK 1,600,000/month (~$76 USD)",
        "it_salary_range": "LAK 8,000,000-20,000,000/month (~$381-952 USD)",
        "manufacturing_salary": "LAK 2,500,000-5,000,000/month (~$119-238 USD)",
        "unemployment": "1.2%", "ai_adoption": "Very low; limited digital infrastructure",
        "internet_penetration": "62%", "literacy_rate": "87%", "stem_graduates": "~5,000 annually",
        "labor_force": "3.8 million",
        "key_industries": "Hydroelectric power (electricity exports), mining (copper, gold), agriculture (rice, coffee), tourism, garments, construction, Laos-China railway (2021)",
        "ai_risk_high": "Garment factory operations, administrative services",
        "ai_risk_medium": "Banking, telecom, mining monitoring, tourism services",
        "ai_risk_low": "Rice farming, construction, hydropower operations, tourism guiding, healthcare, education, fishing",
        "key_challenges": "Severe debt crisis (China debt ~60% of GDP), currency depreciation (LAK lost 50%+ value), one-party state limits private sector, UXO contamination (most bombed country per capita), brain drain to Thailand, limited skilled workforce",
        "references": [("World Bank - Laos", "https://www.worldbank.org/en/country/lao/overview"), ("LSB Laos", "https://www.lsb.gov.la/"), ("IMF - Laos", "https://www.imf.org/en/Countries/LAO"), ("ADB - Laos", "https://www.adb.org/countries/lao-pdr/main"), ("Trading Economics - Laos", "https://tradingeconomics.com/laos/indicators")]
    },
    "tajikistan": {
        "name": "Tajikistan", "slug": "tajikistan-tajikistan", "population": "10.1 million",
        "gdp_per_capita": "$1,058", "gdp_per_capita_ppp": "$4,500", "gdp_growth": "8.3%",
        "currency": "TJS", "avg_monthly_salary": "TJS 2,200 (~$202 USD)",
        "avg_salary_usd": "$202", "minimum_wage": "TJS 600/month (~$55 USD)",
        "it_salary_range": "TJS 4,000-12,000/month (~$367-1,101 USD)",
        "manufacturing_salary": "TJS 1,500-3,000/month (~$138-275 USD)",
        "unemployment": "6.7% (official); remittance dependency masks true unemployment",
        "ai_adoption": "Very low; limited infrastructure, government-controlled internet",
        "internet_penetration": "35%", "literacy_rate": "99%", "stem_graduates": "~8,000 annually",
        "labor_force": "2.5 million (domestically; ~1M labor migrants in Russia)",
        "key_industries": "Aluminum production (Talco), cotton, agriculture (fruits, grain), hydroelectric power, gold/silver mining, remittances (30%+ of GDP from Russia)",
        "ai_risk_high": "Aluminum plant administration, government clerical, basic data processing",
        "ai_risk_medium": "Banking, telecom, mining operations, energy monitoring",
        "ai_risk_low": "Farming, construction, herding, small trade, healthcare, education",
        "key_challenges": "Extreme remittance dependency (Russia), authoritarian government, internet censorship/restrictions, water/energy disputes with neighbors, climate change (glacier melt), border tensions with Afghanistan, brain drain",
        "references": [("World Bank - Tajikistan", "https://www.worldbank.org/en/country/tajikistan/overview"), ("TAJSTAT", "https://www.stat.tj/en"), ("IMF - Tajikistan", "https://www.imf.org/en/Countries/TJK"), ("ADB - Tajikistan", "https://www.adb.org/countries/tajikistan/main"), ("Trading Economics - Tajikistan", "https://tradingeconomics.com/tajikistan/indicators")]
    },
    "kyrgyzstan": {
        "name": "Kyrgyzstan", "slug": "kyrgyzstan-kyrgyzstan", "population": "7.1 million",
        "gdp_per_capita": "$1,675", "gdp_per_capita_ppp": "$6,200", "gdp_growth": "6.2%",
        "currency": "KGS", "avg_monthly_salary": "KGS 30,000 (~$340 USD)",
        "avg_salary_usd": "$340", "minimum_wage": "KGS 2,440/month (~$28 USD)",
        "it_salary_range": "KGS 60,000-200,000/month (~$680-2,270 USD)",
        "manufacturing_salary": "KGS 20,000-40,000/month (~$227-454 USD)",
        "unemployment": "5.3%", "ai_adoption": "Low; emerging tech scene in Bishkek, IT park initiative",
        "internet_penetration": "72%", "literacy_rate": "99%", "stem_graduates": "~10,000 annually",
        "labor_force": "2.7 million (domestically; ~1M labor migrants abroad)",
        "key_industries": "Gold mining (Kumtor), agriculture (livestock, cotton, tobacco), remittances (30% of GDP), hydroelectric power, tourism, garments, IT services (emerging)",
        "ai_risk_high": "Administrative services, data processing, basic banking, garment assembly",
        "ai_risk_medium": "Mining monitoring, retail, telecom, tourism services",
        "ai_risk_low": "Farming, herding, construction, skilled mining, healthcare, education, tourism guiding",
        "key_challenges": "Remittance dependency on Russia, political instability (3 revolutions since 2005), Kumtor gold mine dependency, water/energy disputes with neighbors, corruption, informal economy, brain drain",
        "references": [("World Bank - Kyrgyzstan", "https://www.worldbank.org/en/country/kyrgyzrepublic/overview"), ("NSC Kyrgyzstan", "https://www.stat.kg/en/"), ("IMF - Kyrgyzstan", "https://www.imf.org/en/Countries/KGZ"), ("ADB - Kyrgyzstan", "https://www.adb.org/countries/kyrgyz-republic/main"), ("Trading Economics - Kyrgyzstan", "https://tradingeconomics.com/kyrgyzstan/indicators")]
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
