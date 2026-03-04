#!/usr/bin/env python3
"""Batch 7: Zimbabwe, Benin, Guinea, Madagascar, Malawi, Sierra Leone, Togo, Liberia, Central African Republic, Eritrea"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from batch2_rewrite import gen_article, AUDIENCES, ARTICLES_DIR

COUNTRIES = {
    "zimbabwe": {
        "name": "Zimbabwe", "slug": "zimbabwe-zimbabwe", "population": "16.7 million",
        "gdp_per_capita": "$1,464", "gdp_per_capita_ppp": "$3,500", "gdp_growth": "3.5%",
        "currency": "ZiG (Zimbabwe Gold, introduced 2024)", "avg_monthly_salary": "$200-$350 USD (mostly USD-denominated economy)",
        "avg_salary_usd": "$280", "minimum_wage": "$100 USD/month (varies by sector)",
        "it_salary_range": "$400-$1,200/month",
        "manufacturing_salary": "$150-$300/month",
        "unemployment": "19.3% (formal); informal economy employs ~85% of workforce",
        "ai_adoption": "Low; growing fintech sector, limited outside Harare",
        "internet_penetration": "35%", "literacy_rate": "90%", "stem_graduates": "~8,000 annually",
        "labor_force": "6.5 million",
        "key_industries": "Mining (gold, platinum, lithium, diamonds), agriculture (tobacco, maize), tourism, manufacturing, financial services",
        "ai_risk_high": "Administrative roles, basic data processing, clerical banking",
        "ai_risk_medium": "Mining operations, telecom, retail, tobacco processing",
        "ai_risk_low": "Smallholder farming, skilled mining, construction, healthcare, education, tourism guiding",
        "key_challenges": "Currency instability (new ZiG currency), hyperinflation legacy, massive brain drain, power shortages, sanctions impact, limited foreign investment, informal economy dominance",
        "references": [("World Bank - Zimbabwe", "https://www.worldbank.org/en/country/zimbabwe/overview"), ("ZIMSTAT", "https://www.zimstat.co.zw/"), ("IMF - Zimbabwe", "https://www.imf.org/en/Countries/ZWE"), ("Trading Economics - Zimbabwe", "https://tradingeconomics.com/zimbabwe/indicators"), ("African Development Bank - Zimbabwe", "https://www.afdb.org/en/countries/southern-africa/zimbabwe")]
    },
    "benin": {
        "name": "Benin", "slug": "benin-benin", "population": "13.7 million",
        "gdp_per_capita": "$1,400", "gdp_per_capita_ppp": "$3,800", "gdp_growth": "6.0%",
        "currency": "XOF", "avg_monthly_salary": "XOF 90,000 (~$147 USD)",
        "avg_salary_usd": "$147", "minimum_wage": "XOF 52,000/month (~$85 USD)",
        "it_salary_range": "XOF 250,000-600,000/month (~$409-981 USD)",
        "manufacturing_salary": "XOF 60,000-120,000/month (~$98-196 USD)",
        "unemployment": "1.5% (formal); vast informal underemployment",
        "ai_adoption": "Emerging; government investing in digital identity and e-services",
        "internet_penetration": "34%", "literacy_rate": "46%", "stem_graduates": "~6,000 annually",
        "labor_force": "4.5 million",
        "key_industries": "Cotton, agriculture (cashews, palm oil), port services (Cotonou), tourism, construction, informal trade",
        "ai_risk_high": "Port administrative functions, government clerical, data entry",
        "ai_risk_medium": "Banking, telecom, port logistics, retail",
        "ai_risk_low": "Cotton farming, fishing, construction, artisan crafts, healthcare, education",
        "key_challenges": "Low literacy rate, limited internet infrastructure, regional security spillover from Sahel, reliance on cotton/Nigeria trade, climate vulnerability, weak tertiary education system",
        "references": [("World Bank - Benin", "https://www.worldbank.org/en/country/benin/overview"), ("INSAE Benin", "https://insae.bj/"), ("IMF - Benin", "https://www.imf.org/en/Countries/BEN"), ("Trading Economics - Benin", "https://tradingeconomics.com/benin/indicators"), ("African Development Bank - Benin", "https://www.afdb.org/en/countries/west-africa/benin")]
    },
    "guinea": {
        "name": "Guinea", "slug": "guinea-guinea", "population": "14.2 million",
        "gdp_per_capita": "$1,336", "gdp_per_capita_ppp": "$3,100", "gdp_growth": "5.5%",
        "currency": "GNF", "avg_monthly_salary": "GNF 2,500,000 (~$290 USD)",
        "avg_salary_usd": "$290", "minimum_wage": "GNF 550,000/month (~$64 USD)",
        "it_salary_range": "GNF 5,000,000-12,000,000/month (~$580-1,395 USD)",
        "manufacturing_salary": "GNF 1,500,000-3,000,000/month (~$174-349 USD)",
        "unemployment": "4.8%", "ai_adoption": "Minimal; very limited digital infrastructure",
        "internet_penetration": "28%", "literacy_rate": "39%", "stem_graduates": "~4,000 annually",
        "labor_force": "5.2 million",
        "key_industries": "Bauxite mining (world's largest reserves), gold mining, agriculture (rice, cassava), fishing, alumina refining",
        "ai_risk_high": "Government administrative tasks, basic data processing",
        "ai_risk_medium": "Mining operations monitoring, banking, telecom",
        "ai_risk_low": "Subsistence farming, artisanal mining, fishing, construction, healthcare, education",
        "key_challenges": "Military government (2021 coup), extremely low literacy, Ebola/disease vulnerability, infrastructure gaps, heavy dependence on bauxite exports, limited formal economy",
        "references": [("World Bank - Guinea", "https://www.worldbank.org/en/country/guinea/overview"), ("INS Guinea", "https://www.stat-guinee.org/"), ("IMF - Guinea", "https://www.imf.org/en/Countries/GIN"), ("UNDP - Guinea", "https://www.undp.org/guinea"), ("African Development Bank - Guinea", "https://www.afdb.org/en/countries/west-africa/guinea")]
    },
    "madagascar": {
        "name": "Madagascar", "slug": "madagascar-madagascar", "population": "30.3 million",
        "gdp_per_capita": "$515", "gdp_per_capita_ppp": "$1,700", "gdp_growth": "4.0%",
        "currency": "MGA", "avg_monthly_salary": "MGA 600,000 (~$130 USD)",
        "avg_salary_usd": "$130", "minimum_wage": "MGA 250,000/month (~$54 USD)",
        "it_salary_range": "MGA 1,500,000-5,000,000/month (~$325-1,085 USD)",
        "manufacturing_salary": "MGA 300,000-700,000/month (~$65-152 USD)",
        "unemployment": "3.5% (formal); 90%+ in informal/subsistence economy",
        "ai_adoption": "Minimal; but growing BPO/francophone call center sector",
        "internet_penetration": "22%", "literacy_rate": "77%", "stem_graduates": "~7,000 annually",
        "labor_force": "13.5 million",
        "key_industries": "Agriculture (vanilla, cloves, rice), mining (nickel, cobalt, sapphires), textiles, fishing, tourism, BPO services",
        "ai_risk_high": "BPO/call center operations, data entry, textile quality control",
        "ai_risk_medium": "Mining monitoring, banking, telecom, vanilla processing",
        "ai_risk_low": "Vanilla farming, fishing, construction, ecotourism, healthcare, artisan crafts",
        "key_challenges": "Extreme poverty (>75%), cyclone vulnerability, deforestation crisis, political instability cycles, infrastructure collapse outside Antananarivo, energy access (<25%)",
        "references": [("World Bank - Madagascar", "https://www.worldbank.org/en/country/madagascar/overview"), ("INSTAT Madagascar", "https://www.instat.mg/"), ("IMF - Madagascar", "https://www.imf.org/en/Countries/MDG"), ("Trading Economics - Madagascar", "https://tradingeconomics.com/madagascar/indicators"), ("African Development Bank - Madagascar", "https://www.afdb.org/en/countries/southern-africa/madagascar")]
    },
    "malawi": {
        "name": "Malawi", "slug": "malawi-malawi", "population": "20.9 million",
        "gdp_per_capita": "$645", "gdp_per_capita_ppp": "$1,600", "gdp_growth": "2.0%",
        "currency": "MWK", "avg_monthly_salary": "MWK 150,000 (~$87 USD)",
        "avg_salary_usd": "$87", "minimum_wage": "MWK 50,000/month (~$29 USD)",
        "it_salary_range": "MWK 500,000-1,500,000/month (~$290-870 USD)",
        "manufacturing_salary": "MWK 80,000-200,000/month (~$46-116 USD)",
        "unemployment": "5.7%", "ai_adoption": "Very low; extremely limited connectivity",
        "internet_penetration": "18%", "literacy_rate": "67%", "stem_graduates": "~3,000 annually",
        "labor_force": "8.2 million",
        "key_industries": "Agriculture (tobacco, tea, sugar), mining (uranium, coal), fisheries, tourism, manufacturing (small scale)",
        "ai_risk_high": "Government administrative tasks, basic data entry",
        "ai_risk_medium": "Tobacco processing, banking, telecom, retail",
        "ai_risk_low": "Smallholder farming, fishing, construction, healthcare, education, tea picking",
        "key_challenges": "One of world's poorest countries, currency devaluation crisis, tobacco dependency (60% of exports), limited electricity access, landlocked increasing costs, climate vulnerability (floods/droughts), very limited tech infrastructure",
        "references": [("World Bank - Malawi", "https://www.worldbank.org/en/country/malawi/overview"), ("NSO Malawi", "https://www.nsomalawi.mw/"), ("IMF - Malawi", "https://www.imf.org/en/Countries/MWI"), ("Trading Economics - Malawi", "https://tradingeconomics.com/malawi/indicators"), ("African Development Bank - Malawi", "https://www.afdb.org/en/countries/southern-africa/malawi")]
    },
    "sierra_leone": {
        "name": "Sierra Leone", "slug": "sierra-leone-sierra-leone", "population": "8.8 million",
        "gdp_per_capita": "$527", "gdp_per_capita_ppp": "$1,800", "gdp_growth": "3.5%",
        "currency": "SLL", "avg_monthly_salary": "SLL 3,000,000 (~$135 USD)",
        "avg_salary_usd": "$135", "minimum_wage": "SLL 600,000/month (~$27 USD)",
        "it_salary_range": "SLL 5,000,000-12,000,000/month (~$225-540 USD)",
        "manufacturing_salary": "SLL 1,500,000-3,500,000/month (~$68-158 USD)",
        "unemployment": "4.2%", "ai_adoption": "Minimal; among world's least digitized economies",
        "internet_penetration": "22%", "literacy_rate": "48%", "stem_graduates": "~2,000 annually",
        "labor_force": "3.0 million",
        "key_industries": "Mining (diamonds, iron ore, rutile, bauxite), agriculture (rice, cocoa), fishing, small-scale manufacturing",
        "ai_risk_high": "Government clerical, basic diamond sorting automation",
        "ai_risk_medium": "Mining operations, banking, telecom services",
        "ai_risk_low": "Farming, artisanal mining, fishing, construction, healthcare, teaching, small trade",
        "key_challenges": "Post-civil war and Ebola recovery ongoing, extremely low literacy, power access below 25%, diamond dependency, limited human capital, infrastructure gaps, youth unemployment",
        "references": [("World Bank - Sierra Leone", "https://www.worldbank.org/en/country/sierraleone/overview"), ("Statistics Sierra Leone", "https://www.statistics.sl/"), ("IMF - Sierra Leone", "https://www.imf.org/en/Countries/SLE"), ("UNDP - Sierra Leone", "https://www.undp.org/sierra-leone"), ("African Development Bank - Sierra Leone", "https://www.afdb.org/en/countries/west-africa/sierra-leone")]
    },
    "togo": {
        "name": "Togo", "slug": "togo-togo", "population": "9.1 million",
        "gdp_per_capita": "$986", "gdp_per_capita_ppp": "$2,500", "gdp_growth": "5.3%",
        "currency": "XOF", "avg_monthly_salary": "XOF 80,000 (~$131 USD)",
        "avg_salary_usd": "$131", "minimum_wage": "XOF 52,500/month (~$86 USD)",
        "it_salary_range": "XOF 200,000-500,000/month (~$327-818 USD)",
        "manufacturing_salary": "XOF 55,000-110,000/month (~$90-180 USD)",
        "unemployment": "3.5%", "ai_adoption": "Emerging; Lomé port digitization and growing fintech",
        "internet_penetration": "35%", "literacy_rate": "66%", "stem_graduates": "~4,000 annually",
        "labor_force": "3.5 million",
        "key_industries": "Port services (Lomé deep-water port), phosphate mining, agriculture (cocoa, coffee, cotton), cement, clinker, re-export trade",
        "ai_risk_high": "Port administration, government clerical, basic data processing",
        "ai_risk_medium": "Banking, port logistics automation, telecom, retail",
        "ai_risk_low": "Farming, fishing, construction, artisan trades, healthcare, education",
        "key_challenges": "Political governance concerns, Sahel security spillover, limited skilled workforce, infrastructure gaps outside Lomé, climate vulnerability, heavy reliance on phosphate exports",
        "references": [("World Bank - Togo", "https://www.worldbank.org/en/country/togo/overview"), ("INSEED Togo", "https://inseed.tg/"), ("IMF - Togo", "https://www.imf.org/en/Countries/TGO"), ("Trading Economics - Togo", "https://tradingeconomics.com/togo/indicators"), ("African Development Bank - Togo", "https://www.afdb.org/en/countries/west-africa/togo")]
    },
    "liberia": {
        "name": "Liberia", "slug": "liberia-liberia", "population": "5.4 million",
        "gdp_per_capita": "$676", "gdp_per_capita_ppp": "$1,600", "gdp_growth": "4.3%",
        "currency": "LRD", "avg_monthly_salary": "LRD 30,000 (~$155 USD)",
        "avg_salary_usd": "$155", "minimum_wage": "LRD 5,600/month (~$29 USD) for unskilled workers",
        "it_salary_range": "$300-$800/month (mostly USD-denominated)",
        "manufacturing_salary": "$80-$200/month",
        "unemployment": "3.9%", "ai_adoption": "Minimal; one of Africa's least connected economies",
        "internet_penetration": "19%", "literacy_rate": "48%", "stem_graduates": "~1,500 annually",
        "labor_force": "2.1 million",
        "key_industries": "Iron ore mining, rubber, agriculture (palm oil, cocoa), forestry, gold mining, shipping registry",
        "ai_risk_high": "Government administrative roles, basic data processing",
        "ai_risk_medium": "Mining operations, banking, telecom, shipping registry services",
        "ai_risk_low": "Rubber tapping, farming, artisanal mining, fishing, construction, healthcare, teaching",
        "key_challenges": "Post-civil war institutional weakness, Ebola recovery legacy, extremely limited electricity (<20% access), low literacy, infrastructure gaps, dual currency system, aid dependency",
        "references": [("World Bank - Liberia", "https://www.worldbank.org/en/country/liberia/overview"), ("LISGIS Liberia", "https://www.lisgis.net/"), ("IMF - Liberia", "https://www.imf.org/en/Countries/LBR"), ("UNDP - Liberia", "https://www.undp.org/liberia"), ("African Development Bank - Liberia", "https://www.afdb.org/en/countries/west-africa/liberia")]
    },
    "central_african_republic": {
        "name": "Central African Republic", "slug": "central-african-republic-central-african-republic", "population": "5.7 million",
        "gdp_per_capita": "$461", "gdp_per_capita_ppp": "$1,000", "gdp_growth": "1.0%",
        "currency": "XAF", "avg_monthly_salary": "XAF 50,000 (~$81 USD)",
        "avg_salary_usd": "$81", "minimum_wage": "XAF 35,000/month (~$57 USD)",
        "it_salary_range": "XAF 150,000-400,000/month (~$242-645 USD)",
        "manufacturing_salary": "XAF 40,000-80,000/month (~$65-129 USD)",
        "unemployment": "6.0%", "ai_adoption": "Virtually non-existent; near-zero digital infrastructure",
        "internet_penetration": "7%", "literacy_rate": "37%", "stem_graduates": "~500 annually",
        "labor_force": "2.2 million",
        "key_industries": "Diamonds, gold, timber, agriculture (cotton, coffee, cassava), livestock",
        "ai_risk_high": "Government clerical tasks (extremely limited formal sector)",
        "ai_risk_medium": "Mining monitoring, basic banking, telecom",
        "ai_risk_low": "Subsistence farming, artisanal mining, livestock herding, forestry, construction, healthcare",
        "key_challenges": "Active armed conflict, near-total infrastructure collapse, 7% internet penetration, among world's poorest countries, Wagner Group/Russia influence, mass displacement, aid dependency, no meaningful tech sector",
        "references": [("World Bank - CAR", "https://www.worldbank.org/en/country/centralafricanrepublic/overview"), ("ICASEES CAR", "https://www.icasees.org/"), ("IMF - CAR", "https://www.imf.org/en/Countries/CAF"), ("UNDP - CAR", "https://www.undp.org/central-african-republic"), ("African Development Bank - CAR", "https://www.afdb.org/en/countries/central-africa/central-african-republic")]
    },
    "eritrea": {
        "name": "Eritrea", "slug": "eritrea-eritrea", "population": "3.7 million",
        "gdp_per_capita": "$643", "gdp_per_capita_ppp": "$2,000", "gdp_growth": "2.9%",
        "currency": "ERN", "avg_monthly_salary": "ERN 3,000 (~$200 USD at official rate)",
        "avg_salary_usd": "$200 (official rate)", "minimum_wage": "No official minimum; public sector pays ERN 700-3,500/month",
        "it_salary_range": "ERN 5,000-15,000/month (~$333-1,000 USD at official rate)",
        "manufacturing_salary": "ERN 1,500-3,000/month (~$100-200 USD)",
        "unemployment": "6.4% (official); much higher in practice",
        "ai_adoption": "Virtually non-existent; most isolated internet environment in Africa",
        "internet_penetration": "2%", "literacy_rate": "77%", "stem_graduates": "~1,000 annually",
        "labor_force": "1.8 million",
        "key_industries": "Mining (gold, copper, zinc), agriculture (sorghum, lentils), fishing, cement, small-scale manufacturing, military-linked enterprises",
        "ai_risk_high": "Almost no formal economy exposed to AI disruption",
        "ai_risk_medium": "Mining operations, basic government administration",
        "ai_risk_low": "Farming, fishing, herding, construction, military service, small trade, healthcare",
        "key_challenges": "2% internet penetration (world's lowest), authoritarian government controls all media/internet, mandatory indefinite national service, mass emigration (brain drain), international isolation, no private sector to speak of",
        "references": [("World Bank - Eritrea", "https://www.worldbank.org/en/country/eritrea/overview"), ("IMF - Eritrea", "https://www.imf.org/en/Countries/ERI"), ("UNDP - Eritrea", "https://www.undp.org/eritrea"), ("Freedom House - Eritrea", "https://freedomhouse.org/country/eritrea"), ("Trading Economics - Eritrea", "https://tradingeconomics.com/eritrea/indicators")]
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
