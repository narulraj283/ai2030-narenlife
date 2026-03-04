#!/usr/bin/env python3
"""Batch 11 (FINAL): Barbados, Congo, Georgia, Lebanon, Libya, Oman, Palestine, Serbia, Syria, Turkmenistan, Yemen, Europe"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from batch2_rewrite import gen_article, AUDIENCES, ARTICLES_DIR

COUNTRIES = {
    "barbados": {
        "name": "Barbados", "slug": "barbados-barbados", "population": "282,000",
        "gdp_per_capita": "$17,398", "gdp_per_capita_ppp": "$18,500", "gdp_growth": "4.4%",
        "currency": "BBD (pegged 2:1 to USD)", "avg_monthly_salary": "BBD 5,500 (~$2,750 USD)",
        "avg_salary_usd": "$2,750", "minimum_wage": "BBD 17.50/hour (~$8.75 USD)",
        "it_salary_range": "BBD 6,000-14,000/month (~$3,000-7,000 USD)",
        "manufacturing_salary": "BBD 3,500-6,000/month (~$1,750-3,000 USD)",
        "unemployment": "7.8%", "ai_adoption": "Low; small market, growing digital services ambitions",
        "internet_penetration": "87%", "literacy_rate": "99%", "stem_graduates": "~800 annually",
        "labor_force": "145,000",
        "key_industries": "Tourism, financial services/offshore banking, rum production, agriculture (sugar cane), information services, creative industries",
        "ai_risk_high": "Financial services back-office, hotel reservation systems, administrative services",
        "ai_risk_medium": "Banking, retail, insurance, telecom, tourism booking",
        "ai_risk_low": "Tourism hospitality, agriculture, construction, healthcare, education, creative industries (music, art)",
        "key_challenges": "Tiny domestic market, tourism over-dependence, climate vulnerability (hurricanes, sea-level rise), high public debt (120%+ of GDP), brain drain, energy import costs, water scarcity",
        "references": [("World Bank - Barbados", "https://data.worldbank.org/country/barbados"), ("BSS Barbados", "https://stats.gov.bb/"), ("IMF - Barbados", "https://www.imf.org/en/Countries/BRB"), ("Trading Economics - Barbados", "https://tradingeconomics.com/barbados/indicators"), ("IDB - Barbados", "https://www.iadb.org/en/countries/barbados")]
    },
    "congo": {
        "name": "Republic of Congo", "slug": "congo-congo", "population": "6.1 million",
        "gdp_per_capita": "$2,280", "gdp_per_capita_ppp": "$4,400", "gdp_growth": "2.2%",
        "currency": "XAF", "avg_monthly_salary": "XAF 150,000 (~$242 USD)",
        "avg_salary_usd": "$242", "minimum_wage": "XAF 90,000/month (~$145 USD)",
        "it_salary_range": "XAF 300,000-700,000/month (~$484-1,129 USD)",
        "manufacturing_salary": "XAF 100,000-200,000/month (~$161-323 USD)",
        "unemployment": "21.3%", "ai_adoption": "Minimal; oil-dependent economy with limited diversification",
        "internet_penetration": "32%", "literacy_rate": "81%", "stem_graduates": "~3,000 annually",
        "labor_force": "1.9 million",
        "key_industries": "Oil production (dominant — 50%+ of GDP), forestry/timber, mining (potash, iron), agriculture, construction, port services (Pointe-Noire)",
        "ai_risk_high": "Oil administration, government bureaucracy, basic data processing",
        "ai_risk_medium": "Banking, oil monitoring, telecom, port logistics",
        "ai_risk_low": "Forestry, farming, fishing, construction, healthcare, education, small trade",
        "key_challenges": "Extreme oil dependency, Dutch disease, high poverty despite oil wealth, governance/corruption, limited infrastructure, Pool region instability legacy, youth unemployment >40%",
        "references": [("World Bank - Congo", "https://www.worldbank.org/en/country/congo/overview"), ("INS Congo", "https://www.ins-congo.org/"), ("IMF - Congo", "https://www.imf.org/en/Countries/COG"), ("Trading Economics - Congo", "https://tradingeconomics.com/congo/indicators"), ("African Development Bank - Congo", "https://www.afdb.org/en/countries/central-africa/congo")]
    },
    "georgia": {
        "name": "Georgia", "slug": "georgia-georgia", "population": "3.7 million",
        "gdp_per_capita": "$7,670", "gdp_per_capita_ppp": "$20,400", "gdp_growth": "7.5%",
        "currency": "GEL", "avg_monthly_salary": "GEL 2,000 (~$740 USD)",
        "avg_salary_usd": "$740", "minimum_wage": "GEL 20/month (nominal, not enforced; real wages set by market)",
        "it_salary_range": "GEL 3,500-10,000/month (~$1,296-3,704 USD)",
        "manufacturing_salary": "GEL 1,200-2,500/month (~$444-926 USD)",
        "unemployment": "15.6%", "ai_adoption": "Emerging; Russian/Belarusian tech talent influx post-2022, growing Tbilisi startup scene",
        "internet_penetration": "80%", "literacy_rate": "99%", "stem_graduates": "~8,000 annually",
        "labor_force": "1.9 million",
        "key_industries": "Tourism, agriculture (wine, hazelnuts), mining (manganese, copper), IT services, logistics (transit corridor), food processing, financial services",
        "ai_risk_high": "Administrative services, banking, data processing, logistics documentation",
        "ai_risk_medium": "Tourism booking, retail, telecom, mining monitoring, wine production automation",
        "ai_risk_low": "Wine making, agriculture, construction, healthcare, education, tourism hospitality",
        "key_challenges": "Russia occupation of 20% of territory (Abkhazia, South Ossetia), EU accession process stalled, political polarization, brain drain, high unemployment, currency volatility, small domestic market",
        "references": [("World Bank - Georgia", "https://www.worldbank.org/en/country/georgia/overview"), ("Geostat", "https://www.geostat.ge/en"), ("IMF - Georgia", "https://www.imf.org/en/Countries/GEO"), ("ADB - Georgia", "https://www.adb.org/countries/georgia/main"), ("Trading Economics - Georgia", "https://tradingeconomics.com/georgia/indicators")]
    },
    "lebanon": {
        "name": "Lebanon", "slug": "lebanon-lebanon", "population": "5.5 million (plus ~1.5M Syrian refugees)",
        "gdp_per_capita": "$3,283 (collapsed from $8,000+ pre-crisis)", "gdp_per_capita_ppp": "$14,000 (estimated)",
        "gdp_growth": "-0.5% (extended collapse since 2019)",
        "currency": "LBP (collapsed; black market rate ~90,000:1 USD vs official 15,000:1)",
        "avg_monthly_salary": "LBP 15,000,000 (~$167 USD at market rate); public sector much lower",
        "avg_salary_usd": "$167 (market rate); was ~$1,000 pre-crisis",
        "minimum_wage": "LBP 9,000,000/month (~$100 USD at market rate; hasn't been meaningfully updated)",
        "it_salary_range": "$500-$2,500/month (often paid in USD in private sector)",
        "manufacturing_salary": "$100-$400/month",
        "unemployment": "30%+ (estimated)", "ai_adoption": "Low; but strong diaspora tech talent and Beirut startup culture surviving",
        "internet_penetration": "87%", "literacy_rate": "95%", "stem_graduates": "~10,000 annually (declining as universities collapse)",
        "labor_force": "2.2 million",
        "key_industries": "Banking (collapsed), tourism (recovering), agriculture, food processing, construction, diaspora services, tech startups, education/healthcare (formerly regional leader)",
        "ai_risk_high": "Banking sector (already collapsed), administrative services",
        "ai_risk_medium": "Telecom, retail, tourism services, education technology",
        "ai_risk_low": "Agriculture, construction, healthcare, artisan crafts, hospitality, small trade",
        "key_challenges": "Total economic collapse (90% currency devaluation since 2019), banking system frozen, Beirut port explosion aftermath, political paralysis, power outages (20+ hours/day), mass emigration of skilled workers, 2024 Israel-Hezbollah conflict impact",
        "references": [("World Bank - Lebanon", "https://www.worldbank.org/en/country/lebanon/overview"), ("CAS Lebanon", "https://www.cas.gov.lb/"), ("IMF - Lebanon", "https://www.imf.org/en/Countries/LBN"), ("Trading Economics - Lebanon", "https://tradingeconomics.com/lebanon/indicators"), ("UNDP - Lebanon", "https://www.undp.org/lebanon")]
    },
    "libya": {
        "name": "Libya", "slug": "libya-libya", "population": "7.1 million",
        "gdp_per_capita": "$6,357", "gdp_per_capita_ppp": "$16,000", "gdp_growth": "-2.5%",
        "currency": "LYD", "avg_monthly_salary": "LYD 1,500 (~$310 USD)",
        "avg_salary_usd": "$310", "minimum_wage": "LYD 450/month (~$93 USD; mostly unenforced)",
        "it_salary_range": "LYD 2,500-6,000/month (~$517-1,241 USD)",
        "manufacturing_salary": "LYD 800-1,800/month (~$165-372 USD)",
        "unemployment": "18.5%", "ai_adoption": "Non-existent; political division and conflict preclude development",
        "internet_penetration": "83%", "literacy_rate": "91%", "stem_graduates": "~10,000 annually (but most emigrate)",
        "labor_force": "2.5 million",
        "key_industries": "Oil & gas (95%+ of export revenue), construction, agriculture, fishing, retail trade",
        "ai_risk_high": "Oil administration, government bureaucracy",
        "ai_risk_medium": "Banking, telecom, oil monitoring",
        "ai_risk_low": "Oil field operations, agriculture, fishing, construction, healthcare, education, small trade",
        "key_challenges": "Divided government (Tripoli vs east), ongoing militia conflict, complete oil dependency, infrastructure destroyed, massive brain drain, migrant transit crisis, no functioning institutions",
        "references": [("World Bank - Libya", "https://www.worldbank.org/en/country/libya/overview"), ("IMF - Libya", "https://www.imf.org/en/Countries/LBY"), ("Trading Economics - Libya", "https://tradingeconomics.com/libya/indicators"), ("UNDP - Libya", "https://www.undp.org/libya"), ("African Development Bank - Libya", "https://www.afdb.org/en/countries/north-africa/libya")]
    },
    "oman": {
        "name": "Oman", "slug": "oman-oman", "population": "4.6 million (plus ~1.6M expat workers)",
        "gdp_per_capita": "$22,181", "gdp_per_capita_ppp": "$38,000", "gdp_growth": "1.3%",
        "currency": "OMR (pegged to USD at 0.385)", "avg_monthly_salary": "OMR 700 (~$1,818 USD) for Omanis; expats much lower",
        "avg_salary_usd": "$1,818 (nationals); $450-800 (expats)",
        "minimum_wage": "OMR 325/month (~$844 USD) for Omanis only; no minimum for expats",
        "it_salary_range": "OMR 800-2,500/month (~$2,078-6,494 USD)",
        "manufacturing_salary": "OMR 300-700/month (~$779-1,818 USD)",
        "unemployment": "2.3% (overall); ~15% for Omani youth", "ai_adoption": "Moderate; Oman Vision 2040 includes AI strategy, oil sector digitization",
        "internet_penetration": "96%", "literacy_rate": "97%", "stem_graduates": "~8,000 annually",
        "labor_force": "2.7 million (including expats)",
        "key_industries": "Oil & gas, petrochemicals, logistics (ports), tourism, fishing, mining (chromite, gypsum), construction, green hydrogen (emerging)",
        "ai_risk_high": "Administrative services, banking, oil back-office, government bureaucracy",
        "ai_risk_medium": "Oil monitoring, logistics, retail, telecom, tourism services",
        "ai_risk_low": "Oil field operations, fishing, agriculture (dates), construction, healthcare, education, tourism hospitality",
        "key_challenges": "Oil dependency and diversification urgency, Omanization (replacing expats with nationals), youth unemployment, water scarcity, fiscal deficits, regional geopolitical risks, limited private sector",
        "references": [("World Bank - Oman", "https://data.worldbank.org/country/oman"), ("NCSI Oman", "https://www.ncsi.gov.om/"), ("IMF - Oman", "https://www.imf.org/en/Countries/OMN"), ("Trading Economics - Oman", "https://tradingeconomics.com/oman/indicators"), ("Oman Vision 2040", "https://www.oman2040.om/")]
    },
    "palestine": {
        "name": "Palestine", "slug": "palestine-palestine", "population": "5.5 million (West Bank + Gaza)",
        "gdp_per_capita": "$3,664 (pre-2023 conflict)", "gdp_per_capita_ppp": "$6,500",
        "gdp_growth": "-35% in Gaza; -5% in West Bank (2024 estimates due to conflict)",
        "currency": "ILS (Israeli Shekel), JOD (Jordanian Dinar), USD all used",
        "avg_monthly_salary": "ILS 4,500 (~$1,200 USD) in West Bank; Gaza economy largely destroyed",
        "avg_salary_usd": "$1,200 (West Bank); $150 (Gaza, pre-conflict)",
        "minimum_wage": "ILS 1,880/month (~$503 USD)",
        "it_salary_range": "ILS 6,000-15,000/month (~$1,605-4,013 USD) in West Bank tech sector",
        "manufacturing_salary": "ILS 2,500-5,000/month (~$669-1,338 USD)",
        "unemployment": "24% (West Bank); 80%+ (Gaza, post-conflict)", "ai_adoption": "Low; but Ramallah had growing tech sector pre-conflict",
        "internet_penetration": "75% (West Bank); severely disrupted in Gaza",
        "literacy_rate": "97%", "stem_graduates": "~5,000 annually",
        "labor_force": "1.4 million",
        "key_industries": "IT/tech services (Ramallah), agriculture (olive oil), construction, stone cutting, manufacturing, services, work permits in Israel",
        "ai_risk_high": "Administrative services, data processing (limited formal economy)",
        "ai_risk_medium": "IT outsourcing, banking, telecom, retail",
        "ai_risk_low": "Agriculture, construction, stone cutting, healthcare, education, small trade",
        "key_challenges": "Ongoing conflict and humanitarian catastrophe in Gaza, occupation restricts economic sovereignty, movement restrictions, destroyed infrastructure, dependency on Israeli economy for work permits, aid dependency, political division (PA vs Hamas)",
        "references": [("World Bank - Palestine", "https://www.worldbank.org/en/country/westbankandgaza/overview"), ("PCBS", "https://www.pcbs.gov.ps/"), ("IMF - West Bank and Gaza", "https://www.imf.org/en/Countries/WBG"), ("UNCTAD - Palestine", "https://unctad.org/topic/palestinian-people"), ("UNDP - Palestine", "https://www.undp.org/papp")]
    },
    "serbia": {
        "name": "Serbia", "slug": "serbia-serbia", "population": "6.6 million",
        "gdp_per_capita": "$10,426", "gdp_per_capita_ppp": "$23,000", "gdp_growth": "2.5%",
        "currency": "RSD", "avg_monthly_salary": "RSD 105,000 (~$960 USD)",
        "avg_salary_usd": "$960", "minimum_wage": "RSD 47,073/month (~$430 USD)",
        "it_salary_range": "RSD 200,000-600,000/month (~$1,828-5,483 USD)",
        "manufacturing_salary": "RSD 70,000-120,000/month (~$640-1,096 USD)",
        "unemployment": "8.7%", "ai_adoption": "Moderate; Belgrade emerging as regional tech hub, strong math/CS education tradition",
        "internet_penetration": "81%", "literacy_rate": "99%", "stem_graduates": "~15,000 annually",
        "labor_force": "3.0 million",
        "key_industries": "Automotive (Fiat/Stellantis), IT services, agriculture, mining (copper, lithium deposits), food processing, energy, construction, military equipment",
        "ai_risk_high": "Administrative services, banking, manufacturing assembly, data processing",
        "ai_risk_medium": "Automotive production, retail, telecom, agriculture processing, insurance",
        "ai_risk_low": "Agriculture, construction, healthcare, education, skilled engineering, creative industries",
        "key_challenges": "EU accession stalled (Kosovo issue), brain drain (~50K/year emigrate), population decline, Russia/China balancing act, lithium mine controversy (Rio Tinto), corruption, regional inequality",
        "references": [("World Bank - Serbia", "https://www.worldbank.org/en/country/serbia/overview"), ("SORS", "https://www.stat.gov.rs/en-US/"), ("IMF - Serbia", "https://www.imf.org/en/Countries/SRB"), ("EBRD - Serbia", "https://www.ebrd.com/serbia.html"), ("Trading Economics - Serbia", "https://tradingeconomics.com/serbia/indicators")]
    },
    "syria": {
        "name": "Syria", "slug": "syria-syria", "population": "23 million (pre-war); ~18M remaining",
        "gdp_per_capita": "$421 (estimated; collapsed from $2,800 pre-war)",
        "gdp_per_capita_ppp": "$3,000 (estimated)",
        "gdp_growth": "N/A — economy collapsed; 85% GDP loss since 2011",
        "currency": "SYP (collapsed; black market rate ~15,000:1 USD)",
        "avg_monthly_salary": "SYP 600,000 (~$40 USD at market rate) public sector; private sector $100-200",
        "avg_salary_usd": "$40-$200 depending on sector",
        "minimum_wage": "SYP 185,000/month (~$12 USD at market rate; meaningless)",
        "it_salary_range": "$200-$600/month (extremely limited tech sector)",
        "manufacturing_salary": "$50-$150/month",
        "unemployment": "50%+ (estimated)", "ai_adoption": "Non-existent; infrastructure destroyed, sanctions, brain drain",
        "internet_penetration": "36% (severely degraded)", "literacy_rate": "86% (pre-war; declining)",
        "stem_graduates": "~5,000 annually (severely reduced from pre-war ~25,000)",
        "labor_force": "5.5 million (severely diminished)",
        "key_industries": "Agriculture (wheat, cotton, olives — severely damaged), oil (largely under non-state control), textiles (destroyed), construction (rebuilding), informal economy, aid economy",
        "ai_risk_high": "Almost no formal economy left to be disrupted",
        "ai_risk_medium": "Telecom, basic banking, aid organization operations",
        "ai_risk_low": "Farming, construction, small trade, healthcare, education, informal services",
        "key_challenges": "Civil war destruction (largest refugee crisis since WWII — 6.7M refugees), 85% GDP lost, sanctions, fragmented territorial control, infrastructure obliterated, massive brain drain, health/education system collapse, reconstruction estimated at $400B+",
        "references": [("World Bank - Syria", "https://www.worldbank.org/en/country/syria/overview"), ("IMF - Syria", "https://www.imf.org/en/Countries/SYR"), ("UNDP - Syria", "https://www.undp.org/syria"), ("UNHCR - Syria", "https://www.unhcr.org/syria-emergency.html"), ("Trading Economics - Syria", "https://tradingeconomics.com/syria/indicators")]
    },
    "turkmenistan": {
        "name": "Turkmenistan", "slug": "turkmenistan-turkmenistan", "population": "6.5 million",
        "gdp_per_capita": "$8,580", "gdp_per_capita_ppp": "$16,500", "gdp_growth": "6.3%",
        "currency": "TMT", "avg_monthly_salary": "TMT 3,500 (~$1,000 USD at official rate; much less at real rate)",
        "avg_salary_usd": "$1,000 (official); $200-400 (real purchasing power)",
        "minimum_wage": "TMT 1,160/month (~$331 USD official)",
        "it_salary_range": "TMT 5,000-12,000/month (~$1,429-3,429 USD official; real value much lower)",
        "manufacturing_salary": "TMT 2,000-4,000/month (~$571-1,143 USD official)",
        "unemployment": "4% (official); estimated 25-50% in reality",
        "ai_adoption": "Virtually non-existent; most isolated internet regime after North Korea",
        "internet_penetration": "38% (severely censored; only government ISP)", "literacy_rate": "99%",
        "stem_graduates": "~5,000 annually",
        "labor_force": "2.2 million",
        "key_industries": "Natural gas (world's 4th largest reserves), oil, cotton, textiles, chemicals, construction (prestige projects)",
        "ai_risk_high": "Government bureaucracy (all economy is state-controlled)",
        "ai_risk_medium": "Gas monitoring systems, basic banking, telecom",
        "ai_risk_low": "Cotton farming, construction, herding, healthcare, education, small trade",
        "key_challenges": "Most closed authoritarian regime in Central Asia, total state economic control, gas dependency (China is sole major buyer), severe internet censorship, forced labor in cotton sector, no reliable data (all statistics manipulated), massive capital flight",
        "references": [("World Bank - Turkmenistan", "https://www.worldbank.org/en/country/turkmenistan/overview"), ("IMF - Turkmenistan", "https://www.imf.org/en/Countries/TKM"), ("ADB - Turkmenistan", "https://www.adb.org/countries/turkmenistan/main"), ("Trading Economics - Turkmenistan", "https://tradingeconomics.com/turkmenistan/indicators"), ("Freedom House - Turkmenistan", "https://freedomhouse.org/country/turkmenistan")]
    },
    "yemen": {
        "name": "Yemen", "slug": "yemen-yemen", "population": "34.4 million",
        "gdp_per_capita": "$585 (estimated)", "gdp_per_capita_ppp": "$2,500 (estimated)",
        "gdp_growth": "-2.0% (war economy)",
        "currency": "YER (divided; different rates in Houthi vs government areas)",
        "avg_monthly_salary": "YER 100,000 (~$165 USD) where salaries are paid; many go unpaid",
        "avg_salary_usd": "$165 (where functional)", "minimum_wage": "YER 21,000/month (~$35 USD; rarely enforced)",
        "it_salary_range": "$200-$500/month (extremely limited)",
        "manufacturing_salary": "$50-$150/month",
        "unemployment": "30%+ (estimated)", "ai_adoption": "Non-existent; active war zone with destroyed infrastructure",
        "internet_penetration": "27%", "literacy_rate": "53%", "stem_graduates": "~3,000 annually (severely diminished)",
        "labor_force": "7.5 million",
        "key_industries": "Oil (disrupted), agriculture (qat, coffee), fishing, small manufacturing, aid economy, remittances",
        "ai_risk_high": "Almost no formal economy to be disrupted by AI",
        "ai_risk_medium": "Telecom (still functioning), aid logistics, basic banking",
        "ai_risk_low": "Farming, fishing, qat cultivation, construction, small trade, healthcare, education",
        "key_challenges": "Active civil war since 2014 (world's worst humanitarian crisis), infrastructure destroyed, divided governance (Houthi north vs internationally recognized government), 21M need humanitarian aid, cholera outbreaks, mass displacement, Red Sea shipping attacks (2024)",
        "references": [("World Bank - Yemen", "https://www.worldbank.org/en/country/yemen/overview"), ("IMF - Yemen", "https://www.imf.org/en/Countries/YEM"), ("UNDP - Yemen", "https://www.undp.org/yemen"), ("UNHCR - Yemen", "https://www.unhcr.org/yemen.html"), ("Trading Economics - Yemen", "https://tradingeconomics.com/yemen/indicators")]
    },
    "europe": {
        "name": "Europe", "slug": "europe-europe", "population": "448 million (EU-27); 750 million (continent)",
        "gdp_per_capita": "$38,234 (EU-27 average)", "gdp_per_capita_ppp": "$48,000 (EU-27 average)",
        "gdp_growth": "0.4% (EU-27, 2024)",
        "currency": "EUR (20 eurozone members); plus GBP, CHF, SEK, NOK, PLN, CZK, HUF, etc.",
        "avg_monthly_salary": "€2,800 (~$3,024 USD) EU average; ranges from €700 (Bulgaria) to €6,500 (Denmark)",
        "avg_salary_usd": "$3,024 (EU average)", "minimum_wage": "Ranges from €477 (Bulgaria) to €2,571 (Luxembourg); 6 EU countries have no statutory minimum",
        "it_salary_range": "€3,000-€8,000/month depending on country (~$3,240-8,640 USD)",
        "manufacturing_salary": "€1,500-€4,500/month depending on country",
        "unemployment": "5.9% (EU-27)", "ai_adoption": "High; EU AI Act (world's first comprehensive AI regulation), strong research (DeepMind UK, FAIR France), automotive AI, pharma AI",
        "internet_penetration": "90% (EU average)", "literacy_rate": "99%", "stem_graduates": "~1.5 million annually (EU-27)",
        "labor_force": "220 million (EU-27)",
        "key_industries": "Automotive, pharmaceuticals, financial services, aerospace, luxury goods, agriculture, tourism, technology, energy, chemicals, machinery",
        "ai_risk_high": "Administrative services, banking/insurance, manufacturing assembly, logistics, call centers",
        "ai_risk_medium": "Automotive production, retail, telecom, marketing, legal services, journalism",
        "ai_risk_low": "Healthcare, education, skilled trades, agriculture, creative industries, hospitality, construction",
        "key_challenges": "EU AI Act compliance costs, aging population (lowest fertility globally), competitiveness gap vs US/China in AI, energy transition costs, defense spending pressure (Ukraine), brain drain east-to-west, regulatory fragmentation, migration politics",
        "references": [("European Commission - AI", "https://digital-strategy.ec.europa.eu/en/policies/european-approach-artificial-intelligence"), ("Eurostat", "https://ec.europa.eu/eurostat"), ("OECD - European Union", "https://www.oecd.org/european-union/"), ("IMF - Euro Area", "https://www.imf.org/en/Countries/EUR"), ("EU AI Act", "https://artificialintelligenceact.eu/")]
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
