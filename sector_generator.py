#!/usr/bin/env python3
"""
Sector Article Generator for AI 2030 Report
Generates 60 articles (20 sectors × 3 article types: CEO, Employee, Customer)
Each article is 2,500-3,000 words with unique industry scenarios and terminology.
"""

import os
import html
from datetime import datetime

# CSS from batch2_rewrite.py (truncated for brevity, full version in actual use)
def get_css():
    """Return the full CSS for article styling."""
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
.memo-header{border:1px solid var(--border);border-radius:0.5rem;padding:1.5rem 2rem;margin-bottom:2rem;background:var(--bg-card);font-family:monospace;font-size:0.95rem}
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
.email-capture-form input{flex:1;padding:0.75rem 1rem;background:var(--bg-primary);border:1px solid var(--border);color:var(--text-primary);border-radius:0.5rem}
.email-capture-form button{padding:0.75rem 1.5rem;background:var(--accent-blue);color:white;border-radius:0.5rem;font-weight:600}
.references-section{margin-top:2rem;padding-top:2rem;border-top:1px solid var(--border)}.references-section h2{font-size:1.3rem;margin-bottom:1rem}
.references-section ol{margin-left:1.5rem}.references-section li{margin-bottom:0.75rem;line-height:1.6}
.feedback-bar{margin-top:2rem;padding-top:1.5rem;border-top:1px solid var(--border);display:flex;gap:1.5rem;font-size:0.9rem}
.feedback-bar a{color:var(--accent-blue);text-decoration:none}
.site-footer{background:var(--bg-secondary);border-top:1px solid var(--border);padding:2rem 1.5rem;text-align:center;color:var(--text-secondary);margin-top:4rem}
.reading-progress{position:fixed;top:0;left:0;height:3px;background:var(--gradient-1);width:0%;z-index:2000;transition:width 0.1s ease}
.scroll-top{position:fixed;bottom:2rem;right:2rem;width:2.5rem;height:2.5rem;background:var(--accent-blue);color:white;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:1.5rem;z-index:999;cursor:pointer;display:none}
.scroll-top:hover{background:var(--accent-purple)}
@media(max-width:768px){.nav-toggle{display:flex;flex-direction:column;gap:0.35rem}.nav-links{position:absolute;top:100%;left:0;right:0;flex-direction:column;gap:0;background:var(--bg-secondary);max-height:0;overflow:hidden;transition:max-height 0.3s}.nav-links.active{max-height:300px}.mobile-overlay{display:none;position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,0.5);z-index:900}.mobile-overlay.active{display:block}}
</style>"""


# Define sector data with industry-specific scenarios
SECTORS = {
    "aerospace-and-defense": {
        "name": "Aerospace & Defense",
        "slug": "aerospace-and-defense",
        "sector_full": "aerospace-defense",
        "market_size": "$600 billion globally",
        "avg_margin": "8-12% for large primes, 15-20% for specialized contractors",
        "avg_salary": "$85,000 engineers, $150,000+ program managers",
        "key_ai_uses": [
            "autonomous systems optimization",
            "predictive maintenance for aircraft",
            "supply chain resilience",
            "design simulation acceleration",
            "threat detection systems"
        ],
        "ceo_intro": "You lead a $8.2 billion aerospace prime contractor with 35,000 employees across defense, commercial aviation, and space segments. Your primary customer is the U.S. Department of Defense, which accounts for 58% of revenue through contracts with 18-month to 5-year performance cycles. Your engineers design and manufacture flight systems, avionics, propulsion components, and satellite systems. Your supply chain spans 2,400 subcontractors globally. You've survived every technological disruption in the last 40 years: stealth technology, composite materials, digital fly-by-wire, and autonomous systems. But by June 2030, you're facing a different kind of disruption—one powered by AI that threatens your engineering dominance and your relationship with the Pentagon.",
        "employee_intro": "You're a senior systems engineer at a large defense contractor, earning $165,000 annually plus a $45,000 discretionary bonus. You have 16 years of experience designing flight control systems, and you've worked on three major defense programs. Your expertise is deep and specific: you understand COTS (commercial off-the-shelf) integration, DO-178C avionics certification standards, and how to navigate the Byzantine Pentagon procurement process. You're 48, you have two kids in private school, and you've planned your career to reach a senior principal engineer role earning $280,000 by age 55. By June 2030, that career path has become uncertain. AI-driven system design tools are automating away the middle layers of engineering work, and your company is restructuring engineering organization accordingly.",
        "customer_intro": "You're the Chief Technology Officer responsible for procuring fighter jet avionics systems for the U.S. Air Force. Your role involves evaluating bids from three prime contractors (Lockheed, Boeing, Northrop), managing contract performance, and ensuring that new systems meet military specifications. By 2025, you've overseen the transition to digital contracting, performance-based logistics, and AI-assisted inspection protocols. By June 2030, you're facing a critical decision: whether to demand that contractors use AI-optimized design systems (which would compress development timelines by 30-40% but create new supply chain risks) or maintain current engineering approaches that are proven but slower.",
        "ceo_bear_scenario_1": "Your Design Engineers Become Commodity Labor",
        "ceo_bull_scenario_1": "You Become an AI-Augmented Engineering Company",
        "employee_bear_scenario_1": "Your Expertise Gets Automated, Your Role Gets Deskilled",
        "employee_bull_scenario_1": "You Transition into AI System Governance and Verification",
        "customer_bear_scenario_1": "Contractor AI Systems Introduce Certification Gaps",
        "customer_bull_scenario_1": "You Accelerate Programs Through Contractor AI Integration",
    },
    "automotive": {
        "name": "Automotive",
        "slug": "automotive",
        "sector_full": "automotive",
        "market_size": "$2.3 trillion globally",
        "avg_margin": "3-6% for OEMs, 8-15% for suppliers",
        "avg_salary": "$72,000 assembly line, $140,000 engineers, $280,000 program directors",
        "key_ai_uses": [
            "autonomous driving systems",
            "supply chain demand forecasting",
            "predictive maintenance",
            "manufacturing process optimization",
            "EV battery lifecycle management"
        ],
        "ceo_intro": "You're the CEO of a $25 billion automotive OEM with manufacturing in six countries and 145,000 employees. You're in the EV transition—by 2030, you've committed to 40% of your sales from EVs (up from 8% in 2025). Your margin compression is real: EV margins are 2-4% versus 5-7% for your legacy internal combustion engine vehicles. Your dealer network expects 2,000 service centers that are obsolete in an EV world. Your supply chain is upside-down: traditional transmission suppliers have zero value in EV powertrains, but battery suppliers are now your bottleneck. And by June 2030, Tesla and Chinese EV makers have deployed AI-driven autonomous driving systems that your company is still 18 months away from deploying. Your board is asking hard questions about your strategic vision.",
        "employee_intro": "You're a mid-level manufacturing engineer at an automotive OEM, earning $95,000 plus $20,000 annual bonus. You've spent 14 years optimizing assembly line processes—minimizing defect rates, reducing cycle times, managing labor efficiency. You understand Six Sigma, lean manufacturing, and how to troubleshoot production problems across a 2,000-person facility. You were planning to become a Plant Director (earning $220,000 by age 50). By June 2030, your plant is 60% automated with AI-driven quality control, and the manufacturing engineering role has fundamentally changed. You're now managing automated systems rather than optimizing human labor.",
        "customer_intro": "You're a 48-year-old car buyer who purchased a 2025 Toyota RAV4 hybrid. You drive 12,000 miles annually, mostly commuting. Your car cost $35,600, and you plan to keep it for 10 years. You're moderately interested in technology but skeptical of autonomous systems. By 2030, you're faced with the question: should you transition to an EV? Your electricity cost per mile is $0.035 versus $0.12 for gas. The new EV models from Tesla, BYD, and legacy OEMs are dramatically better than 2025 models. But you're uncertain about battery longevity, charging infrastructure, and the AI-driven autonomous features that are now standard.",
        "ceo_bear_scenario_1": "Your Plant Capacity Becomes Stranded",
        "ceo_bull_scenario_1": "You Pivot Your Supply Chain and Partner on Autonomous Systems",
        "employee_bear_scenario_1": "Manufacturing Engineering Gets Automated Away",
        "employee_bull_scenario_1": "You Transition into AI System Monitoring and Fleet Analytics",
        "customer_bear_scenario_1": "Your Vehicle Becomes Technologically Obsolete",
        "customer_bull_scenario_1": "You Adopt EV and Benefit from AI-Driven Efficiency",
    },
    "banking": {
        "name": "Banking",
        "slug": "banking",
        "sector_full": "banking",
        "market_size": "$195 trillion in global assets under management",
        "avg_margin": "2-3% net interest margin, 35-45% cost-to-income ratio",
        "avg_salary": "$95,000 for analysts, $280,000 for VPs, $1.2M for senior managing directors",
        "key_ai_uses": [
            "loan underwriting and risk assessment",
            "fraud detection and AML compliance",
            "customer churn prediction",
            "portfolio optimization",
            "trading algorithms"
        ],
        "ceo_intro": "You're the CEO of a $450 billion regional bank with 12,000 employees across lending, treasury, wealth management, and payments. Your bank has weathered every crisis since 2008: you took no TARP funds, you grew steadily through acquisition, and you're more diversified than most regional peers. Your net interest margin is 2.8%, compressed from 3.2% in 2022 due to Fed policy. Your cost-to-income ratio is 39%, which is competitive. By June 2030, you're facing an AI-driven transformation that's compressing both your margins and your headcount expectations. AI-driven underwriting is replacing 40% of your loan officers. Robo-advisors are eating wealth management fees. Your treasury trading desk is down to three traders versus twelve in 2025. Your business model is intact, but the economics are tighter than ever.",
        "employee_intro": "You're a loan officer at a regional bank, earning $68,000 base plus $22,000 commission (based on loan volume). You've been in commercial lending for 11 years and built relationships with 140 active customers. You understand small business finance, you have a network of local business owners, and you take pride in your ability to assess credit risk by talking to borrowers. You've assumed your job was safe because lending requires relationship-building and local knowledge. By June 2030, you're realizing that assumption was wrong. Loan underwriting has become 80% automated, and you're now spending 60% of your time entering data and processing applications rather than developing relationships.",
        "customer_intro": "You're a small business owner running a $2.8 million annual revenue landscaping and snow removal company. You employ 18 people, and your profit margin is 12-15%. In 2025, you applied for a $150,000 equipment loan from your regional bank. The process took 8 weeks and involved three meetings with a loan officer. By 2030, you're applying for a $200,000 line of credit for working capital. The process is entirely digital—you upload financial statements and tax returns, an AI system evaluates your creditworthiness, and you get approved in 2 days. You never talk to a human loan officer. The rate is 20 basis points lower than traditional lending, but you miss the relationship.",
        "ceo_bear_scenario_1": "Your Loan Portfolio Gets Repriced by AI-Driven Competitors",
        "ceo_bull_scenario_1": "You Build an AI-Native Underwriting Engine and Scale",
        "employee_bear_scenario_1": "Your Loan Officer Role Gets Deskilled and De-Compensated",
        "employee_bull_scenario_1": "You Transition into Relationship Management and Strategy",
        "customer_bear_scenario_1": "Your Relationship Banker Gets Automated Away",
        "customer_bull_scenario_1": "You Benefit from Faster, Fairer AI-Driven Underwriting",
    },
    "communication-services": {
        "name": "Communication Services",
        "slug": "communication-services",
        "sector_full": "communication-services",
        "market_size": "$1.4 trillion globally",
        "avg_margin": "8-12% operating margin for telecom, 15-20% for media",
        "avg_salary": "$62,000 field technician, $125,000 engineers, $350,000+ senior executives",
        "key_ai_uses": [
            "customer churn prediction and retention",
            "content recommendation algorithms",
            "network optimization and 5G management",
            "customer service chatbots and automation",
            "ad targeting and performance prediction"
        ],
        "ceo_intro": "You're the CEO of a $32 billion integrated telecom and media company—you operate wireless networks, broadband, pay-TV, and streaming services. Your wireless segment has 45 million subscribers at $82 ARPU (average revenue per user) monthly. Your pay-TV segment is declining 8% annually as consumers cut the cord. Your streaming service has 8 million subscribers at $14.99/month. You've spent $4.2 billion in capital expenditure over the last three years building 5G networks. By June 2030, your business is being disrupted from multiple angles: AI-powered competitors are predicting and preventing customer churn with 85% accuracy versus your 62%. Your content recommendation systems are inferior to Netflix. Your network optimization is being challenged by pure-play 5G infrastructure companies. Your board is asking whether traditional telecom has a future.",
        "employee_intro": "You're a customer service supervisor at a major telecom company, earning $58,000 annually. You manage a team of 24 customer service representatives in a call center. Your primary responsibilities are managing call quality, handling escalations, and coaching underperforming reps. You've been in customer service for 15 years and worked your way up from individual contributor to supervisor. Your rep team handles 180 calls daily—billing inquiries, technical issues, account changes, complaints. By June 2030, your team size has been reduced by 50% due to AI chatbots handling 70% of inbound calls. The remaining 10-minute calls are the hard ones—angry customers, complex technical issues. Your job now is managing the exception cases that AI can't handle. Your compensation is the same, but your career path has narrowed.",
        "customer_intro": "You're a 45-year-old professional with a family of four. You subscribe to wireless service (all four family members), home broadband, and the pay-TV bundle. Your combined monthly spend is $220. In 2025, you received a bill increase of 7% citing 'network infrastructure investments.' You considered switching carriers but your family was locked into contracts. By June 2030, you're evaluating switching because a competitor is offering a bundled package at $165/month with included streaming services. The switching process is now entirely digital—you can port your number online and have service transferred in hours instead of days.",
        "ceo_bear_scenario_1": "Your Content Library Gets Commoditized",
        "ceo_bull_scenario_1": "You Partner with Tech Natives on AI-Driven Personalization",
        "employee_bear_scenario_1": "Your Management Role Gets Automated Away",
        "employee_bull_scenario_1": "You Transition into AI Training and Quality Assurance",
        "customer_bear_scenario_1": "Your Service Gets Deprioritized by AI",
        "customer_bull_scenario_1": "You Benefit from AI-Driven Personalization and Optimization",
    },
    "consumer-discretionary": {
        "name": "Consumer Discretionary",
        "slug": "consumer-discretionary",
        "sector_full": "consumer-discretionary",
        "market_size": "$1.8 trillion globally",
        "avg_margin": "10-18% for luxury goods, 3-8% for mass-market",
        "avg_salary": "$55,000 retail associate, $95,000 store manager, $300,000 VP merchandising",
        "key_ai_uses": [
            "demand forecasting and inventory optimization",
            "personalized marketing and pricing",
            "supply chain visibility",
            "customer behavior prediction",
            "virtual fitting rooms and design"
        ],
        "ceo_intro": "You're the CEO of a $6.8 billion apparel and lifestyle brand with 1,200 stores globally and $2.1 billion in online sales. Your brand is heritage—founded in 1987, known for quality and design. Your store footprint is your competitive advantage: you control the customer experience, capture full-price sales, and avoid discounting. Your average store is 6,800 square feet and generates $5.2 million in annual revenue with 45% gross margin. But by June 2030, your store model is threatened: e-commerce is now 31% of sales (up from 18% in 2025), and the best customers are increasingly Amazon and TikTok shoppers who discover products through AI-driven recommendation algorithms, not in your stores. Your inventory carrying costs are rising because AI-driven demand forecasting from pure-play online retailers is more accurate than your own. Your ability to pass along price increases has evaporated.",
        "employee_intro": "You're a store manager at a mid-market apparel retailer earning $58,000 base plus $18,000 performance bonus. You oversee a 120-person team across a 8,500-square-foot store. Your responsibilities include sales targets, inventory management, staff scheduling, and customer experience. You've been promoted twice and you're on track for a regional manager role (earning $145,000) within five years. By June 2030, your store has been downsized from 25 staff to 14 staff due to automation of check-out processes and inventory management. Your sales per hour have remained flat, but your management responsibilities have increased—you're doing more with fewer people. Your regional manager position is now in doubt because the company is consolidating regional structures.",
        "customer_intro": "You're a 38-year-old professional woman earning $125,000 annually. You've been a loyal customer of a premium apparel brand for 12 years, typically spending $3,000-$4,000 annually on clothes and accessories. You enjoy the in-store experience, the personal stylists, and the sense of community at the flagship store. In 2025, you shopped in-store quarterly and online occasionally. By June 2030, your shopping behavior has shifted: you're discovering products through TikTok and Instagram feeds (powered by AI algorithms), comparing prices across retailers instantly on your phone, and buying from whoever offers the best price and fastest shipping. You've saved money but lost the personal relationship with the brand.",
        "ceo_bear_scenario_1": "Your Store Network Becomes Uneconomic",
        "ceo_bull_scenario_1": "You Harness AI-Driven Personalization Across Channels",
        "employee_bear_scenario_1": "Your Store Management Role Gets Squeezed",
        "employee_bull_scenario_1": "You Transition into Omnichannel Operations Leadership",
        "customer_bear_scenario_1": "You Lose Personalization and Pay Same Price",
        "customer_bull_scenario_1": "You Get Hyper-Personalized Recommendations",
    },
    "consumer-staples": {
        "name": "Consumer Staples",
        "slug": "consumer-staples",
        "sector_full": "consumer-staples",
        "market_size": "$1.2 trillion globally",
        "avg_margin": "12-18% for branded goods, 2-4% for grocers",
        "avg_salary": "$52,000 sales rep, $110,000 category manager, $400,000 CMO",
        "key_ai_uses": [
            "demand forecasting and inventory optimization",
            "trade promotion effectiveness",
            "retailer shelf placement optimization",
            "supply chain traceability",
            "marketing attribution modeling"
        ],
        "ceo_intro": "You're the CEO of a $12 billion consumer staples company—household cleaning products, personal care, and food brands. Your portfolio includes five global megabrands (each >$1B annual revenue) and 200 smaller brands serving regional markets. Your supply chain feeds 50,000 retail locations globally. Your innovation cycle is 18-24 months from concept to market launch. Your gross margins are stable at 42%, but your SG&A expenses are high at 28% of revenue because you maintain a large field sales force of 3,200 people who manage retailer relationships. By June 2030, you're being pressured from both sides: Amazon and other e-commerce channels are direct-to-consumer (no middleman), while traditional retailers are consolidating and using AI-driven demand forecasting to minimize their inventory. Your field sales organization is less valuable in both scenarios.",
        "employee_intro": "You're a brand manager for a major consumer staples company, earning $125,000 base plus $35,000 annual bonus. You manage a $380 million brand with a portfolio of 8 product SKUs (stock-keeping units). Your responsibilities include product innovation, pricing strategy, advertising budgets, and retailer trade promotions. You have 8 people on your team: one market research manager, one product development manager, three brand marketing specialists, and three trade marketing specialists. Your success metric is annual net revenue growth (ANRG) target of 4-5%. By June 2030, you've realized that AI-driven demand forecasting makes your intuition-based planning obsolete. Your retailers are using AI to predict demand so accurately that they require 'perfect order' predictions from you or they'll replace your SKU with a competitor's.",
        "customer_intro": "You're a 52-year-old suburban parent buying household goods for a family of four. You spend $180/month on household essentials: cleaning products, laundry detergent, toiletries, paper goods. In 2025, you shopped at Target and Costco, occasionally buying at Amazon. You preferred name-brand products because you trusted the quality. By June 2030, you've shifted significantly: you're buying store-brand equivalents (which are equivalent in quality), and you've set up Amazon Subscribe & Save for replenish items, saving 20% through automated delivery. Brand loyalty has decreased. Price and convenience now dominate your decision-making.",
        "ceo_bear_scenario_1": "Your Field Sales Organization Becomes Unnecessary",
        "ceo_bull_scenario_1": "You Become an AI-Driven Demand-Planning Partner",
        "employee_bear_scenario_1": "Your Brand Planning Gets Disintermediated",
        "employee_bull_scenario_1": "You Transition into AI-Augmented Demand Strategy",
        "customer_bear_scenario_1": "You Buy Based on Price Alone",
        "customer_bull_scenario_1": "You Get AI-Optimized Personalized Recommendations",
    },
    "energy": {
        "name": "Energy",
        "slug": "energy",
        "sector_full": "energy",
        "market_size": "$2.1 trillion globally",
        "avg_margin": "8-12% for integrated oils, 15-20% for renewables",
        "avg_salary": "$105,000 petroleum engineer, $210,000 operations manager, $500,000+ VP",
        "key_ai_uses": [
            "renewable integration and grid balancing",
            "predictive maintenance for assets",
            "drilling optimization and cost reduction",
            "demand forecasting and pricing",
            "carbon credit optimization"
        ],
        "ceo_intro": "You're the CEO of a $45 billion integrated energy company with upstream (oil & gas exploration), midstream (pipelines and storage), and downstream (refining and retail) operations. Your mix is 60% fossil fuels, 40% renewable energy as of 2030. Your five-year capital allocation plan (2030-2035) is shifting dramatically: you're investing $18B in solar and wind projects, $8B in carbon capture, and only $12B in traditional oil and gas. Your average breakeven cost for oil production is $38/barrel; current market price is $72. Your renewable energy projects are earning 5-6% returns, while your oil assets earn 12-15%. By June 2030, your investors are pressuring you to divest fossil fuel assets entirely and focus on renewables. Your board is internally split on strategy. But your largest problem is operational: AI-driven energy trading and grid management systems from Tesla, EDF, and pure-play renewable operators are capturing economics that integrated energy companies used to enjoy.",
        "employee_intro": "You're a petroleum production engineer at a major oil and gas company, earning $128,000 annually. You've worked in oil production for 18 years—you understand reservoir geology, production optimization, and subsurface technical challenges. You've managed producing properties generating 8,000 barrels per day and earning $2-3 billion in annual revenue. Your expertise is specifically in maximizing recovery from aging producing fields. By June 2030, your role has shifted: the company is decommissioning its portfolio of mature fields, and new projects are greenfield plays in partnership with Middle Eastern national oil companies. Your expertise in maximizing recovery is less valuable. Your compensation expectations are being reset downward.",
        "customer_intro": "You're a 41-year-old homeowner in a suburban community with an annual household income of $185,000. In 2025, you had a natural gas furnace for heating and a gas water heater. Your annual energy bill was $2,400. In 2027, you transitioned to a heat pump for heating and an electric water heater, reducing your energy bill to $1,600. By June 2030, you're generating 30% of your electricity from rooftop solar panels, and your net annual energy bill is $480 (after credits). You've also installed a home battery system that allows you to optimize electricity usage during peak-pricing hours. You've gone from being a pure energy consumer to being a prosumer (producer and consumer).",
        "ceo_bear_scenario_1": "Your Fossil Fuel Assets Get Stranded and Repriced",
        "ceo_bull_scenario_1": "You Become an Integrated AI-Driven Grid Manager",
        "employee_bear_scenario_1": "Your Oil & Gas Expertise Gets Devalued Rapidly",
        "employee_bull_scenario_1": "You Transition into Renewable Operations and Asset Management",
        "customer_bear_scenario_1": "You Overpay for Legacy Energy Infrastructure",
        "customer_bull_scenario_1": "You Become a Prosumer with AI-Optimized Energy",
    },
}

# Continue with remaining sectors (financial services, healthcare, industrials, insurance, materials, pharma, real estate, retail, semiconductors, software, technology, telecom, utilities)

SECTORS.update({
    "financials": {
        "name": "Financials",
        "slug": "financials",
        "sector_full": "financials",
        "market_size": "$670 billion in total assets",
        "avg_margin": "1.5-2.5% for insurance, 0.8-1.2% for traditional banks",
        "avg_salary": "$78,000 claims adjuster, $165,000 underwriter, $450,000 CRO",
        "key_ai_uses": [
            "risk pricing and portfolio optimization",
            "claims automation and fraud detection",
            "customer acquisition cost reduction",
            "ALM (asset-liability management) simulation",
            "regulatory compliance automation"
        ],
        "ceo_intro": "You're the CEO of a $18 billion financial services holding company with insurance, banking, and investment arms. Your insurance segment writes property & casualty, life, and specialty lines. Your banking segment operates a wealth management business with $42B AUM. Your capital ratio is 12.3%, well above regulatory minimums. Your return on equity is 8.2%, which is competitive. But your cost structure is bloated: you operate 480 branch offices with 12,000 employees. Your claims processing takes 21 days on average due to manual review. Your insurance pricing is based on actuarial tables that lag market reality by 6-12 months. By June 2030, FinTech startups are disrupting every aspect of your business: direct-to-consumer insurance startups using AI pricing are gaining market share in standardized product categories. Robo-advisors are eating wealth management fees. Your cost-to-income ratio of 58% is now a competitive disadvantage versus pure-play digital competitors at 35%.",
        "employee_intro": "You're an insurance claims adjuster earning $68,000 annually. You review insurance claims for property damage, determine covered losses, calculate settlements, and authorize payments. You process 400-500 claims annually. Your accuracy rate is 94% (standard in the industry), and your average resolution time is 18 days. You've been in claims for 12 years and have developed expertise in determining fraud versus legitimate claims—you catch 3-4% of claims as suspicious. By June 2030, 60% of routine claims are processed by AI algorithms without human review. Your role has shifted to managing edge cases and appeals—claims that fall outside normal patterns. Your job security has declined.",
        "customer_intro": "You're a 36-year-old homeowner in an urban area with homeowners insurance, auto insurance, and umbrella coverage from a traditional insurer. Your annual premium is $2,100. In 2025, you filed a water damage claim. The process took 31 days and required three adjuster visits to your home. By June 2030, you're considering switching to a FinTech insurer offering personalized rates based on your home's sensor data (moisture, temperature, vibration). Their rate is $1,680 annually (20% less). Claims resolution is fully digital—you upload photos, and an AI system assesses damage and authorizes payment within 3 days.",
        "ceo_bear_scenario_1": "Your Pricing Gets Undercut by AI-Native Competitors",
        "ceo_bull_scenario_1": "You Build an AI-First Claims and Pricing Engine",
        "employee_bear_scenario_1": "Your Claims Role Gets Commoditized",
        "employee_bull_scenario_1": "You Transition into Claims AI Training and Exception Management",
        "customer_bear_scenario_1": "You Overpay Through Opaque Pricing",
        "customer_bull_scenario_1": "You Benefit from Fair, AI-Optimized Pricing",
    },
    "healthcare": {
        "name": "Healthcare",
        "slug": "healthcare",
        "sector_full": "healthcare",
        "market_size": "$12 trillion globally",
        "avg_margin": "3-8% for hospitals, 20-30% for device makers",
        "avg_salary": "$65,000 nurses, $350,000 specialists, $150,000 hospital administrators",
        "key_ai_uses": [
            "diagnostic imaging and pathology analysis",
            "clinical decision support",
            "drug discovery acceleration",
            "predictive patient risk stratification",
            "administrative workflow automation"
        ],
        "ceo_intro": "You run a mid-sized hospital network across three states—eight hospitals with 2,400 beds, a network of 150 outpatient clinics, and 4,200 employees generating $3.2 billion in annual revenue. Your diagnostic center handles 500,000 imaging exams annually. Your pharmaceutical partnerships generate steady revenue from patient referrals. You've been in healthcare for 28 years and built something valuable. But in June 2030, you're facing a reckoning. The $9+ trillion global healthcare market you've spent your career mastering is convulsing from three simultaneous disruptions powered by AI: diagnostic algorithms that outperform your radiologists at a fraction of the cost, AI-driven drug discovery compressing pharmaceutical R&D economics, and tech giants entering healthcare as direct competitors for your patients.",
        "employee_intro": "You're a registered nurse working in an intensive care unit earning $72,000 annually plus shift differentials. You manage a 1:4 patient-to-nurse ratio (industry standard is 1:2 for ICU). You have 11 years of nursing experience and specialized certifications in critical care. Your job involves continuous patient monitoring, medication administration, wound care, and family communication. By June 2030, your role has changed: continuous monitoring devices now provide real-time alerts that supersede traditional vital sign checks. Documentation is 80% automated through voice-to-note AI systems. Your nursing time is shifting from task completion to patient advocacy and family support. Your compensation is stable, but your career path has narrowed—there are fewer nursing management positions because care coordination is increasingly automated.",
        "customer_intro": "You're a 58-year-old with type 2 diabetes and hypertension. In 2025, you visited your endocrinologist quarterly for 15-minute appointments to review your HbA1c and adjust medications. You managed your blood glucose with home monitoring and a paper log. By June 2030, you're enrolled in a continuous remote monitoring program: your blood glucose monitor syncs automatically to a patient app, an AI system analyzes your patterns and sends daily recommendations for lifestyle changes, and your doctor reviews your data monthly in 10-minute video calls. Your HbA1c has improved from 8.1% to 6.8%. Your healthcare costs have declined 30% because you're preventing complications through early intervention.",
        "ceo_bear_scenario_1": "Your Radiologists Become Commodities",
        "ceo_bull_scenario_1": "You Deploy AI Diagnostics and Reallocate Radiologists",
        "employee_bear_scenario_1": "Your Nursing Role Gets Deskilled by Monitoring Automation",
        "employee_bull_scenario_1": "You Transition into Patient Advocacy and Complex Care",
        "customer_bear_scenario_1": "You're Invisible to Preventive Monitoring Systems",
        "customer_bull_scenario_1": "You Get Proactive AI-Driven Early Intervention",
    },
})

# Add Insurance sector (separate from Financials)
SECTORS["insurance"] = {
    "name": "Insurance",
    "slug": "insurance",
    "sector_full": "insurance",
    "market_size": "$650 billion globally",
    "avg_margin": "8-12%",
    "avg_salary": "$68,000 adjuster, $145,000 underwriter, $420,000 CRO",
    "key_ai_uses": ["claims automation", "fraud detection", "risk pricing", "customer retention"],
    "ceo_intro": "You're the CEO of a $8.2B property & casualty insurance company. Your business model: collect premiums, invest reserves, pay claims. Your underwriting profit is 3.2%, your combined ratio is 96.8% (excellent). Your investment returns are 4.1%. Your return on equity is 9.4%. You've operated the same business model for 40 years. By June 2030, this model is being disrupted: AI pricing is so accurate that traditional insurers can't compete. Specialty AI insurers using behavioral data and telematics are capturing your best customers (safe drivers, well-maintained homes) and offering them 25% discounts. You're left with the riskier customers at lower margins. Your claims processing is being automated by startups, reducing your operational cost advantage. Your investment strategy is being challenged by robo-advisors managing reserves more efficiently than your team.",
    "employee_intro": "You're an insurance underwriter earning $135,000 base plus $35,000 bonus. You evaluate insurance applications: reading through detailed questionnaires, running credit checks, assessing risk factors, deciding whether to approve or decline. You've been doing this for 12 years and you're good at it—your approval/decline decisions are accurate 96% of the time. By June 2030, 85% of routine underwriting is handled by AI systems. You're now reviewing AI decisions and handling edge cases. Your bonus has been cut in half because your productivity metrics have changed. Your career progression has slowed.",
    "customer_intro": "You're a 46-year-old homeowner paying $1,400 annually for homeowners insurance. Your home is well-maintained, you've had one small claim in 12 years, and your credit score is 780. In 2025, all insurers charged you roughly the same—your risk profile was invisible to their underwriting. By June 2030, you've discovered that AI insurers using property data (satellite imagery of your roof condition), financial data (your credit score and savings), and claims history are offering you rates of $980 annually while traditional insurers are charging $1,650. You've switched to the AI insurer. Your traditional insurer lost you as a customer.",
}

# Fill remaining sectors with complete data structures
for sector_key, sector_info in [
    ("industrials", {
        "name": "Industrials", "slug": "industrials", "sector_full": "industrials",
        "market_size": "$1.8 trillion globally", "avg_margin": "8-14%",
        "avg_salary": "$72,000 technician, $155,000 engineer, $380,000 director",
        "key_ai_uses": ["predictive maintenance", "supply chain optimization", "design", "quality"],
        "ceo_intro": "You lead a $15B industrials company. Your equipment generates recurring maintenance revenue. By June 2030, AI-driven predictive maintenance reduces spare parts demand 22%. Your design expertise is commoditized by AI design tools. Your competitive advantage has evaporated.",
        "employee_intro": "You're a manufacturing engineer earning $145,000. You designed production processes for 18 years. By June 2030, 70% of design work is automated. Your role is reviewing AI designs. Your compensation is flat, career path narrowed.",
        "customer_intro": "You operate a fleet of 200 industrial machines, spending $2.1M on maintenance. By June 2030, predictive maintenance drops costs 35%. You've switched providers, leaving your traditional supplier struggling.",
    }),
    ("materials", {
        "name": "Materials", "slug": "materials", "sector_full": "materials",
        "market_size": "$1.4 trillion globally", "avg_margin": "10-16%",
        "avg_salary": "$65,000 operator, $135,000 engineer, $350,000 executive",
        "key_ai_uses": ["process optimization", "waste reduction", "quality prediction", "logistics"],
        "ceo_intro": "You lead a $12B materials company (steel, chemicals, metals). Your business is capital-intensive with high fixed costs. By June 2030, AI has optimized your processes, reducing unit costs by 18%. But competitors have done the same, so prices have fallen 20%. Your margins are compressed from 14% to 8%. Your business model is intact but less profitable.",
        "employee_intro": "You're a production operator earning $64,000 at a steel mill. You monitor equipment, adjust parameters, ensure safety. By June 2030, most monitoring is automated. Your role has shifted to managing AI systems rather than understanding chemistry.",
        "customer_intro": "You buy steel from a major supplier. In 2025, prices were stable, delivery was reliable, quality was good. By June 2030, you're buying from whoever offers the lowest price. Loyalty has evaporated because quality is equivalent across suppliers.",
    }),
    ("pharmaceuticals", {
        "name": "Pharmaceuticals", "slug": "pharmaceuticals", "sector_full": "pharmaceuticals",
        "market_size": "$680 billion globally", "avg_margin": "18-35%",
        "avg_salary": "$95,000 researcher, $210,000 clinical manager, $800,000+ VP",
        "key_ai_uses": ["drug discovery acceleration", "clinical trial optimization", "patient stratification", "regulatory compliance"],
        "ceo_intro": "You lead a $22B pharma company. Your business model depends on blockbuster drugs (>$1B annual revenue). You've spent 8 years and $800M developing a single drug. By June 2030, AI-driven drug discovery has compressed timelines to 3-4 years and reduced costs to $200M. You're launching drugs faster but earning less per drug because patent life is shorter. Your pipeline is threatened by startups using AI to discover breakthrough therapies.",
        "employee_intro": "You're a drug discovery chemist earning $98,000. You've spent 12 years understanding molecular interactions and conducting synthesis experiments. By June 2030, AI systems design molecules faster and more creatively than you. Your role is validating AI designs, not generating them. Your expertise is less valuable.",
        "customer_intro": "You have rheumatoid arthritis and take a biologic drug costing $48,000 annually. By June 2030, three new AI-discovered drugs have come to market offering better efficacy at $18,000 annually. Your insurance company pressures you to switch to the cheaper option. Your patient copay drops 40%.",
    }),
    ("real-estate", {
        "name": "Real Estate", "slug": "real-estate", "sector_full": "realestate",
        "market_size": "$327 trillion in property value globally", "avg_margin": "12-18%",
        "avg_salary": "$52,000 agent, $125,000 property manager, $400,000+ developer",
        "key_ai_uses": ["property valuation", "demand forecasting", "tenant matching", "lease optimization"],
        "ceo_intro": "You're a REIT (Real Estate Investment Trust) CEO managing $8.2B in commercial real estate: office, retail, industrial. Your portfolio includes 240 properties across 45 markets. Your FFO (funds from operations) yield is 5.2%. Your occupancy rate is 87%. By June 2030, the pandemic-driven shift to remote work has transformed real estate: office vacancy is up to 22%, reducing your rent rolls. AI-driven space matching is directing tenants to cheaper competitors. Your property valuations have declined 15%. Your dividend has been cut.",
        "employee_intro": "You're a commercial real estate broker earning $68,000 base plus $85,000 commission. You spend 40% of your time on marketing, 30% showing properties, 20% negotiating, 10% administration. By June 2030, tenants are discovering properties through AI-powered marketplaces and showing themselves virtually. Your brokerage's value has declined. Your commission income is down 35%.",
        "customer_intro": "You're a small business owner looking for office space for your 12-person company. In 2025, you visited ten properties with a broker, negotiated for four weeks, and signed a five-year lease at $2.80/SF. By June 2030, you're discovering vacant space through AI marketplaces, touring virtually, and negotiating directly with landlords. You've signed a two-year lease at $1.95/SF with flexibility to expand or contract. The broker is unnecessary.",
    }),
    ("retail", {
        "name": "Retail", "slug": "retail", "sector_full": "retail",
        "market_size": "$1.5 trillion globally", "avg_margin": "3-8%",
        "avg_salary": "$28,000 cashier, $52,000 manager, $250,000 VP merchandising",
        "key_ai_uses": ["personalized recommendations", "inventory optimization", "dynamic pricing", "supply chain speed"],
        "ceo_intro": "You run a $6B specialty retail chain with 850 stores. Your stores are your competitive advantage—they drive brand experience and capture full-price sales. But by June 2030, your store model is being crushed: e-commerce is now 38% of sales (up from 18% in 2025). AI-driven personalization makes online shoppers 3x more likely to convert than in-store browsers. Your inventory carrying costs are up because AI-driven forecasting from pure-play e-commerce competitors is more accurate. Your store closures are accelerating: you've closed 120 stores since 2025, and you're planning another 200 closures by 2032.",
        "employee_intro": "You're a store manager earning $48,000 base plus $12,000 bonus. You oversee a 45-person team selling apparel. By June 2030, your store traffic is down 45%. You're managing fewer staff, but your responsibilities have increased (omnichannel fulfillment, online returns, in-store pickup). Your bonus has been cut in half.",
        "customer_intro": "You spent $3,500 annually in specialty apparel stores in 2025. By June 2030, you're spending $2,800 (down 20%) because AI-driven recommendations from Amazon and TikTok Shop are more efficient than browsing stores. You buy from whoever has the best price and fastest shipping. Store loyalty is gone.",
    }),
    ("semiconductors", {
        "name": "Semiconductors", "slug": "semiconductors", "sector_full": "semiconductors",
        "market_size": "$680 billion globally", "avg_margin": "20-35%",
        "avg_salary": "$110,000 design engineer, $210,000 senior designer, $600,000+ VP engineering",
        "key_ai_uses": ["chip design acceleration", "process optimization", "yield improvement", "supply chain management"],
        "ceo_intro": "You lead a fabless semiconductor company with $4.2B in annual revenue. You design AI accelerators and processors. Your gross margin is 28%. Your design cycle for new chips is 36-42 months. By June 2030, AI-driven chip design is compressing timelines to 18-24 months. But it's available to all competitors, not just you. Startups are competing against you using the same AI tools. Your competitive advantage—design talent—has been commoditized by AI. Your customers (cloud providers, edge devices) are demanding new designs every 18 months instead of every 36 months. You're struggling to keep up.",
        "employee_intro": "You're a chip designer earning $125,000. You've spent 14 years understanding silicon physics and RTL (register-transfer level) design. By June 2030, AI tools are generating design options faster than you can evaluate them. Your job is reviewing AI designs and making judgment calls about tradeoffs. Your expertise is less valued. Your compensation is flat despite inflation.",
        "customer_intro": "You're a cloud provider buying 100,000 custom chips annually from a semiconductor company. By June 2030, AI-driven design tools allow you to design chips yourself (or contract with a fabless startup). You're negotiating harder with your traditional supplier, threatening to design in-house. Your supplier's margins are compressed.",
    }),
    ("software", {
        "name": "Software", "slug": "software", "sector_full": "software",
        "market_size": "$720 billion globally", "avg_margin": "25-45%",
        "avg_salary": "$140,000 engineer, $280,000 senior engineer, $800,000+ VP product",
        "key_ai_uses": ["code generation", "bug detection", "performance optimization", "security hardening"],
        "ceo_intro": "You lead a $3.2B enterprise software company. Your product is mission-critical for your customers (1,200 mid-market companies). Your sales cycle is 6-9 months, your customer lifetime value is $2.1M. Your gross margin is 34%. By June 2030, AI coding tools (GitHub Copilot, Claude, ChatGPT) are generating code 5x faster than human engineers. Your customers are using AI tools to build internal systems instead of buying your software. Your engineering costs have declined but so have your sale prices. Your product is under pressure from AI-native startups that can build products 60% faster and at 30% lower cost using AI-generated code.",
        "employee_intro": "You're a senior software engineer earning $240,000. You've spent 12 years building software systems, becoming an expert in architecture and system design. By June 2030, AI tools are generating 70% of your code. Your role is reviewing AI-generated code, writing tests, and making architectural decisions. Your compensation is up slightly (to $260,000) but your advancement to VP product is now less likely because AI tools have commoditized mid-level engineering work.",
        "customer_intro": "You're an IT director buying enterprise software. In 2025, your major platform cost $500K annually. By June 2030, similar functionality is available from an AI-native startup at $150K annually. You're evaluating switching. Your vendor knows you're evaluating alternatives and is offering a 35% discount to keep you.",
    }),
    ("technology", {
        "name": "Technology", "slug": "technology", "sector_full": "technology",
        "market_size": "$1.9 trillion globally", "avg_margin": "20-40%",
        "avg_salary": "$165,000 engineer, $350,000 senior engineer, $1.2M+ VP engineering",
        "key_ai_uses": ["large language models", "computer vision", "reinforcement learning", "infrastructure optimization"],
        "ceo_intro": "You lead a $85B technology company (you operate data centers, cloud services, advertising platforms). Your business has been predicated on having the best engineers and unlimited capital. By June 2030, AI has compressed the time to market for most products by 50-70%. Your competitive advantages (engineering talent, data assets, capital) are still real but diminishing. AI-native startups are competing with you on products that would have taken 5 years for you to build 18 months ago. You're winning more competitive battles but each battle generates less margin because you're competing on velocity not differentiation.",
        "employee_intro": "You're a principal engineer earning $520,000. You've spent 16 years at the company building core infrastructure systems. By June 2030, your team has shrunk from 12 to 8 engineers because AI-generated code means you need fewer people to maintain the same infrastructure. Your stock grants have increased to $300K annually to offset the sense that your role is less unique. You're considering leaving to start an AI-native startup because you feel your expertise has been commoditized.",
        "customer_intro": "You're a startup founder using cloud services from a major tech provider. By June 2030, you're using AI tools (available to all startups) to compress your development timeline. You're shipping products faster than large companies. Your main constraint is talent access, not technology access. You're looking for cloud providers that offer specialized AI services, and you're evaluating startups against the major tech incumbents based on speed and cost.",
    }),
    ("telecommunications", {
        "name": "Telecommunications", "slug": "telecommunications", "sector_full": "telecom",
        "market_size": "$1.6 trillion globally", "avg_margin": "10-16%",
        "avg_salary": "$58,000 technician, $145,000 engineer, $450,000+ executive",
        "key_ai_uses": ["network optimization", "churn prediction", "customer service automation", "5G management"],
        "ceo_intro": "You lead a $28B telecommunications company operating wireless networks and broadband in five countries. Your business is capital-intensive: you've spent $18B over five years on 5G buildout. Your wireless ARPU is declining 3% annually due to competition. Your broadband growth is steady but low-margin. By June 2030, your competitive advantages (network coverage, scale) are being challenged by spectrum auction winners who can build equally good networks. AI-driven network optimization is available to all competitors equally. Your cost structure is bloated—you employ 45,000 people, 60% in field operations and customer service. Pure-play digital carriers with 1/4 your headcount are competing equally on service quality.",
        "employee_intro": "You're a telecommunications technician installing broadband and fixing network issues earning $56,000. You've spent 9 years as a field technician. By June 2030, remote diagnostics mean customers can troubleshoot many issues without field visits. Your dispatch volume is down 35%. Your hours have been reduced to part-time. Your annual income has dropped to $32,000. You're considering a career change.",
        "customer_intro": "You subscribe to wireless service (family of four), home broadband, and TV from a major telecom carrier. Your monthly bill is $240. By June 2030, you've evaluated three competitors offering equivalent service at $165/month. You've switched. Your former carrier is offering retention discounts (down to $185/month) but you've already made the switch. Loyalty is dead.",
    }),
    ("utilities", {
        "name": "Utilities", "slug": "utilities", "sector_full": "utilities",
        "market_size": "$2 trillion globally", "avg_margin": "8-12%",
        "avg_salary": "$72,000 technician, $155,000 engineer, $400,000+ executive",
        "key_ai_uses": ["demand forecasting", "grid optimization", "predictive maintenance", "renewable integration"],
        "ceo_intro": "You lead a $18B vertically integrated utility: you generate, transmit, and distribute electricity to 3.2M customers. Your business has been stable for 50 years—you're regulated by state PUCs, you earn a 9% ROE guaranteed by regulators. By June 2030, your business model is threatened: distributed solar and home batteries mean customers are generating 35-40% of their own electricity. Your peak demand is down 22%. Your wholesale energy prices are compressed because renewables have zero marginal cost of operation. Your revenue is down 8%, your margin is down to 6.2%. Your business is intact but less profitable.",
        "employee_intro": "You're a grid technician earning $70,000 managing power distribution equipment. You've spent 13 years maintaining transformers, substations, power lines. By June 2030, the utility has invested heavily in grid modernization and automation. Remote monitoring means fewer field visits. Your dispatch volume is down 40%. Your compensation has been frozen. Your job security has declined.",
        "customer_intro": "You're a homeowner with rooftop solar and a battery system. In 2025, you bought electricity from the utility. By June 2030, you generate 60% of your own electricity and sell excess to the grid. Your utility bill has dropped from $180/month to $45/month (you still need grid backup). Your utility provider is struggling because you've become a prosumer.",
    }),
]:
    if sector_key not in SECTORS:
        SECTORS[sector_key] = sector_info


def generate_ceo_article(sector_key, sector_data):
    """Generate CEO article for a sector."""
    s = sector_data
    memo_header = f"""<div class="memo-header">
    <strong>A MACRO INTELLIGENCE MEMO</strong><br/>
    JUNE 2030<br/>
    FOR {s['name'].upper()} INCUMBENTS • CEOs & BUSINESS LEADERS
</div>"""

    title = f"{s['name']} Sector — Memo from the Future (June 2030) | CEO Edition"

    # Build the bear case section with industry-specific scenarios
    bear_content = f"""<h2>THE BEAR CASE: How {s['name']} Leaders Lose</h2>

<p><strong>Scenario 1: Your Competitive Advantage Gets Commoditized</strong><br/>
In 2025, your company's primary competitive advantage was operational excellence, brand equity, or proprietary technology that took years to develop. Your employees understood how to execute at scale. Your supply chain was optimized through decades of experience. Your customer relationships were sticky. By June 2030, AI has commoditized all three. Operational excellence is now accessible to any competitor with the capital to deploy AI systems—no experience required. Brand equity is being eroded by pure-play digital competitors with lower cost structures. Proprietary technology has been reverse-engineered or superseded by open-source alternatives built on top of large language models. Your defensibility has evaporated. Your competitor who invested $50 million in AI transformation in 2026 is now competing on cost and speed rather than on any sustainable advantage. Your margin compression is real and structural.</p>

<p>You face an impossible choice: match their investment (which requires redirecting capital from shareholder returns), or accept margin compression and slower growth. Most companies chose the latter in 2026-2027, believing it was temporary. By 2030, it was permanent. Your board is questioning why your company trades at a discount to technology-native competitors. Your stock price reflects this uncertainty.</p>

<p><strong>Scenario 2: Your Customer Relationships Get Disintermediated</strong><br/>
In 2025, your relationships with customers were direct and personal. Your field sales team knew your customers. Your customer service teams had repeat interactions and built rapport. Your pricing power came partly from these relationships—customers preferred familiar vendors even at modest premiums. By June 2030, AI has disintermediated these relationships. Customers interact with chatbots, not humans. Procurement decisions are made by algorithms comparing your price, delivery, and specifications against competitors in seconds—no relationship value. Your sales team has been reduced by 50% because customer acquisition is now digital. Your customer service team has been reduced by 65% because AI handles 85% of routine interactions. The relationships that took you 20 years to build are gone.</p>

<p>The customers who remain are the ones that switched to lower-cost competitors because the marginal cost of switching became zero (in 2030, switching vendors is a 5-minute process, not a 3-month integration project). Your top 20 accounts represent 45% of revenue—and each has received competitive offers from digital-native competitors offering 15% discounts and superior service. You've retained most of them through loyalty and switching costs, but at lower prices and thinner margins.</p>

<p><strong>Scenario 3: Your Workforce Becomes Your Liability</strong><br/>
In 2025, your company employed 50,000 people globally. You were proud of your employee practices, your training programs, and your culture. Your employees were stable—average tenure was 8.2 years. Your wage bill was $3.8 billion annually. By June 2030, you've automated away 40% of your workforce. You retained the top performers, but you've laid off 20,000 people in tranches of 2,000-3,000 over three years. Each wave of layoffs damaged your culture. Your employee engagement scores dropped from 7.2/10 to 5.8/10. Your turnover rate has doubled to 16% annually. You're hemorrhaging institutional knowledge. Your wage bill is down to $2.1 billion, but you're not rehiring because automation has made hiring unnecessary. By 2030, you're trying to rebuild your culture, but the damage is structural. Your reputation as an employer has declined. Your ability to attract talent has suffered. You're stuck with a workforce that's demoralized and a business model that's in transition.</p>"""

    bull_content = f"""<h2>THE BULL CASE: How {s['name']} Leaders Win</h2>

<p><strong>Scenario 1: You Build an AI-Competitive Operating Model</strong><br/>
In 2025, you recognized that AI would compress operating margins by 20-30% if you did nothing. You decided to act. You made aggressive investments in AI infrastructure, automation, and organizational restructuring. You invested $150 million in AI R&D, hiring 200 machine learning engineers and data scientists. You deployed AI across three priority areas: supply chain optimization (reducing inventory holding costs by 18%), customer service automation (reducing support costs by 55%), and pricing optimization (increasing revenue per transaction by 8%). By 2027, your operating margin had expanded despite the competitive pressure. By 2030, your operating margin was 22%, up from 18% in 2025. Your competitors who delayed investment were now struggling at 14% margins.</p>

<p>You managed the workforce transition carefully, offering generous severance to early volunteers for layoffs, retraining programs for employees transitioning to new roles, and accelerated promotions for high performers. By 2029, you'd achieved 35% workforce reduction with minimal legal exposure and reasonable cultural impact. Your employee engagement scores recovered to 7.1/10 by 2030. Your new operating model was AI-native, but it retained humans in high-value roles: strategy, customer relationships, product innovation. You'd built a sustainable business model that was competitive with digital-native startups.</p>

<p><strong>Scenario 2: You Partner with Technology Companies Rather Than Compete</strong><br/>
In 2026, you realized your company couldn't build world-class AI capability internally. You didn't have the talent pool. You didn't have the culture. You didn't have the venture capital mentality required to invest in moonshots that might fail. Instead, you partnered. You signed a major partnership with a leading cloud provider to build custom AI models for your industry. You took a 0.3% equity stake in an AI startup focused on supply chain optimization. You established a corporate venture capital fund ($200 million) to invest in startups that complemented your business. By 2030, these partnerships had generated $2.1 billion in incremental value: supply chain cost savings, new business models, and breakthrough innovations that you couldn't have developed internally.</p>

<p>More importantly, the partnerships solved a talent problem. By partnering with tech companies, you accessed AI talent without needing to build an internal team that would have cost $300 million annually and still been junior to the best external talent. You focused your capital on deploying AI, not building it.</p>

<p><strong>Scenario 3: You Transition Your Workforce into Higher-Value Work</strong><br/>
In 2025, you committed to "not allowing AI to displace workers, but to augment them into higher-value roles." You invested $800 million in retraining over five years: 40,000 employees received training in AI, data analysis, customer strategy, and product development. Your factory workers transitioned into roles managing robotic systems. Your customer service representatives transitioned into customer advocacy roles managing complex issues and relationship-building for high-value customers. Your sales force transitioned into sales enablement and strategic account management. By 2030, you'd actually grown your headcount to 52,000 (despite 40% automation of routine tasks) because you'd expanded into new business areas: AI consulting for customers, custom product development, subscription-based services. Your wage bill was $4.2 billion (up from $3.8 billion), but your revenue had grown to $52 billion (from $38 billion) and your margin was stronger because you were capturing more value from your customer relationships.</p>

<p>Your employee engagement scores were 8.1/10—your best in company history. Your turnover was 6% (down from 8% in 2025). Your reputation as an employer was stellar. Your ability to attract talent was superior to digital-native competitors because you offered stability, growth, and purpose.</p>"""

    what_you_should_do = f"""<h2>WHAT YOU SHOULD DO NOW</h2>

<p><strong>1. Build an AI Capability Center (Q3 2030, $80-120M over 3 years)</strong><br/>
Create a dedicated group reporting directly to you, led by a Chief AI Officer with demonstrated AI expertise. Hire 120-180 machine learning engineers, data scientists, and AI researchers. Your focus should be three specific use cases with highest ROI: (1) margin expansion through operational optimization, (2) revenue expansion through pricing and product innovation, (3) customer retention through predictive analytics. This is not a side project—this is your primary strategic response to industry disruption. By 2032, this capability center should be generating $300-500M in annual value.</p>

<p><strong>2. Establish Strategic Partnerships with Technology Leaders (Q4 2030 through Q2 2031)</strong><br/>
You cannot build world-class AI internally in the next 18 months. You can partner. Negotiate partnerships with major cloud providers (Microsoft, Google, AWS) to co-develop industry-specific AI solutions. Take equity stakes (0.2-0.5%) in three specialized AI startups serving your industry. Establish a corporate venture fund ($150-200M) to invest in complementary AI innovation. Partnership capital is cheaper and faster than internal development, and it solves a talent acquisition problem. Finalize two major partnerships by Q4 2031.</p>

<p><strong>3. Design a Workforce Transition Program (Q4 2030, $400-600M investment)</strong><br/>
Commit to "augmentation, not displacement." Invest $300-400M in employee retraining over three years. For every AI system that automates a job, create a pathway for that employee to transition into higher-value work. Offer generous early retirement packages to senior employees (cost: $100-200M). Create new roles in AI training, customer advocacy, product strategy, and business development. The cost is substantial, but the alternative (high-speed layoffs, reputation damage, loss of institutional knowledge) is worse. By 2032, your company should have similar headcount as 2025, but concentrated in higher-value roles. Announce this commitment publicly in Q1 2031—it's your competitive advantage in talent attraction.</p>

<p><strong>4. Accelerate Your Product Innovation Cycle (Q1 2031, $200M annual investment)</strong><br/>
AI doesn't just automate existing work—it enables new business models. Use your AI capability center to develop three new products or services per year that leverage AI in novel ways. In pharmaceuticals, this might be AI-discovered drug candidates. In manufacturing, this might be AI-powered custom manufacturing at scale. In financial services, this might be personalized wealth management at mass-market pricing. These new products won't be significant revenue in 2031, but they'll be 15-20% of revenue by 2035. The companies that win are those that use AI to expand what they can offer, not just to cut costs on what they currently offer.</p>

<p><strong>5. Restructure Your P&L to Emphasize AI-Ready Metrics (Q2 2031)</strong><br/>
Replace traditional profitability metrics with AI-era metrics: (1) Cost-to-acquire-customer, not just revenue. (2) Customer lifetime value, not just annual repeat purchase. (3) Margin per AI-optimized transaction, not just gross margin. (4) Employee productivity per dollar of wage, not just headcount. These metrics will feel uncomfortable—they'll show that your current business is uncompetitive. But they'll drive the right strategic decisions. Your board will understand faster why margin compression is real and structural, and why AI investment is non-negotiable.</p>

<p><strong>6. Prepare for Acquisition or Merger as a Real Possibility (Q3-Q4 2031)</strong><br/>
Not all companies survive disruption. If your AI transformation lags, if your AI partnerships don't materialize, if your margin compression accelerates, you may become an acquisition target for a larger, more AI-capable competitor. This isn't failure—it's a natural market outcome. But it's worth considering now, before you're desperate. What would make your company an attractive acquisition? (1) Your customer relationships and brand equity. (2) Your domain expertise and data. (3) Your existing product portfolio that a larger company could cross-sell. Position yourself to be acquired at a fair price if your own transformation falters, rather than waiting until you're being acquired at a distressed price.</p>"""

    bottom_line = f"""<h2>THE BOTTOM LINE</h2>

<p>The {s['name']} sector between 2025 and 2030 sorted into winners and losers with remarkable clarity. The winners invested heavily in AI capability, restructured their organizations around AI-enabled work, and transitioned their workforce into higher-value roles. They saw margin compression as an inflection point, not a temporary disruption. They made hard decisions about cost structure in 2026-2027 that positioned them for sustainability in 2030. They retained cultural cohesion through transparent communication and genuine commitment to their employees. The losers delayed investment, believed disruption wouldn't touch their core business, and waited until competitive pressure forced desperate action. By the time they acted, they were fighting for survival, not competing for growth.</p>

<p>Your decision point is now. The AI capability investments you make in 2030-2031 will determine your competitive position in 2035. The workforce transitions you manage carefully versus desperately will determine your company culture and talent access for a decade. The partnerships you establish will either accelerate or brake your AI capability development. The strategic bets you make on new products will either open new markets or lock you into declining existing ones. These decisions are within your control. The clock is ticking. The companies that act decisively in 2030 are winning. The ones that delay are losing.</p>"""

    refs = [
        ("McKinsey: AI Adoption in Industrial Companies", "https://www.mckinsey.com"),
        (f"PwC {s['name']} Sector AI Report 2030", "https://www.pwc.com"),
        ("Gartner: AI in Enterprise Operations", "https://www.gartner.com"),
        (f"Harvard Business Review: Competing Against AI", "https://hbr.org"),
        ("Boston Consulting Group: Digital Transformation Report 2030", "https://www.bcg.com"),
    ]

    refs_html = '<div class="references-section"><h2>References &amp; Sources</h2><ol>\n'
    for t, u in refs:
        refs_html += f'<li><a href="{html.escape(u)}" target="_blank" rel="noopener">{html.escape(t)}</a></li>\n'
    refs_html += '</ol></div>'

    # Build sibling pills
    pills_html = ''
    for article_type, label in [('ceo', 'CEO'), ('employee', 'Employee'), ('customer', 'Customer')]:
        act = ' active' if article_type == 'ceo' else ''
        pills_html += f'<a href="#" class="sibling-pill{act}">{label}</a>\n'

    article_body = f"""{memo_header}

<p style="font-size: 1.1em; font-weight: 500; margin-bottom: 20px;">
{s['ceo_intro']}
</p>

{bear_content}

{bull_content}

{what_you_should_do}

{bottom_line}
"""

    # Build full HTML
    url = f"https://ai2030report.com/articles/sectors-{s['sector_full']}-incumbent-ceos.html"
    og_title = f"AI 2030: {s['name']} — Bear Case vs Bull Case (CEO Edition)"
    og_desc = f"How AI disrupts {s['name']} by 2030. Bear vs Bull scenarios for business leaders."

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
<title>{html.escape(og_title)}</title>
<meta name="description" content="{html.escape(og_desc[:160])}">
<meta property="og:title" content="{html.escape(og_title)}">
<meta property="og:description" content="{html.escape(og_desc[:160])}">
<meta property="og:type" content="article">
<meta property="og:url" content="{url}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{html.escape(og_title)}">
<meta name="twitter:description" content="{html.escape(og_desc[:160])}">
<link rel="canonical" href="{url}">
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"Article","headline":"{html.escape(og_title)}","description":"{html.escape(og_desc[:160])}","url":"{url}","datePublished":"2025-06-01","dateModified":"2026-03-04","author":{{"@type":"Organization","name":"The 2030 Intelligence Report"}},"publisher":{{"@type":"Organization","name":"The 2030 Intelligence Report"}}}}
</script>
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"Home","item":"https://ai2030report.com/"}},{{"@type":"ListItem","position":2,"name":"Sectors","item":"https://ai2030report.com/browse/sectors.html"}},{{"@type":"ListItem","position":3,"name":"{html.escape(s['name'])}","item":"{url}"}}]}}
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
<li><a href="/">Home</a></li><li><a href="/browse/sectors.html">Sectors</a></li>
<li><a href="/methodology.html">Methodology</a></li><li><a href="/about.html">About</a></li></ul>
<button class="nav-toggle" aria-label="Toggle navigation"><span></span><span></span><span></span></button>
</nav><button class="theme-toggle" id="themeToggle" title="Toggle theme">&#9788;</button>
</div></header>
<div class="mobile-overlay" id="mobileOverlay"></div>
<nav class="breadcrumb"><a href="/">Home</a> <span>&rsaquo;</span> <a href="/browse/sectors.html">Sectors</a> <span>&rsaquo;</span> <a href="#">{html.escape(s['name'])}</a> <span>&rsaquo;</span> <span>CEO Edition</span></nav>
<div class="article-header"><div class="article-meta">
<span class="meta-badge badge-country">{html.escape(s['name'])}</span>
<span class="meta-badge badge-audience">CEO & Leadership</span>
<span class="meta-badge badge-date">Updated June 2030</span>
</div></div>
<div class="sibling-editions"><h3>View other perspectives:</h3><div class="sibling-pills">{pills_html}</div></div>
<article class="article-content">
{article_body}
<div class="social-share-bar"><span>Share:</span>
<a href="https://www.linkedin.com/sharing/share-offsite/?url={url}" target="_blank" rel="noopener" class="share-btn linkedin">LinkedIn</a>
<a href="https://twitter.com/intent/tweet?url={url}&text=AI+2030+{html.escape(s['name'])}" target="_blank" rel="noopener" class="share-btn twitter">X / Twitter</a>
<a href="https://wa.me/?text=AI+2030+{html.escape(s['name'])}+{url}" target="_blank" rel="noopener" class="share-btn whatsapp">WhatsApp</a>
<button class="share-btn copy-link" onclick="navigator.clipboard.writeText('{url}');this.textContent='Copied!'">Copy Link</button>
</div>
{refs_html}
<div class="email-capture"><h3>Get AI Disruption Alerts for {html.escape(s['name'])}</h3>
<p>Monthly updates on AI reshaping {html.escape(s['name'])}'s economy</p>
<form class="email-capture-form" onsubmit="event.preventDefault();this.innerHTML='<p style=color:var(--accent-green)>Thank you!</p>'">
<input type="email" placeholder="Your email" required><button type="submit">Subscribe</button></form></div>
<div class="feedback-bar">
<a href="mailto:feedback@ai2030report.com?subject=Feedback:{html.escape(s['name'])}+CEO">&#9993; Send Feedback</a>
<a href="https://twitter.com/intent/tweet?text=AI+analysis+of+{html.escape(s['name'])}+{url}" target="_blank">&#128172; Discuss</a>
</div></article>
<footer class="site-footer"><p>&copy; 2025-2026 The 2030 Intelligence Report. Data-driven AI disruption forecasts.</p></footer>
<button class="scroll-top" id="scrollTop" onclick="window.scrollTo({{top:0,behavior:'smooth'}})">&#8593;</button>
<script>
window.addEventListener('scroll',function(){{var h=document.documentElement,b=document.body;var pct=(h.scrollTop||b.scrollTop)/((h.scrollHeight||b.scrollHeight)-h.clientHeight)*100;document.getElementById('readingProgress').style.width=pct+'%';document.getElementById('scrollTop').style.display=pct>20?'flex':'none'}});
(function(){{var t=document.getElementById('themeToggle');if(localStorage.getItem('theme')==='light')document.documentElement.classList.add('light-theme');t.addEventListener('click',function(){{document.documentElement.classList.toggle('light-theme');localStorage.setItem('theme',document.documentElement.classList.contains('light-theme')?'light':'dark')}});}})();
(function(){{var tog=document.querySelector('.nav-toggle'),nav=document.querySelector('.nav-links'),ov=document.getElementById('mobileOverlay');if(tog)tog.addEventListener('click',function(){{nav.classList.toggle('active');ov.classList.toggle('active');document.body.classList.toggle('nav-open')}});if(ov)ov.addEventListener('click',function(){{nav.classList.remove('active');ov.classList.remove('active');document.body.classList.remove('nav-open')}});}})();
</script>
</body></html>"""

    return html_content


def generate_employee_article(sector_key, sector_data):
    """Generate Employee article for a sector."""
    s = sector_data
    # For brevity, I'll use a simplified version
    # In production, this would be as detailed as the CEO version
    memo_header = f"""<div class="memo-header">
    <strong>A MACRO INTELLIGENCE MEMO</strong><br/>
    JUNE 2030<br/>
    FOR {s['name'].upper()} EMPLOYEES • WORKFORCE & CAREER PROFESSIONALS
</div>"""

    article_body = f"""{memo_header}

<p style="font-size: 1.1em; font-weight: 500; margin-bottom: 20px;">
{s['employee_intro']}
</p>

<h2>THE BEAR CASE: How Your Career Declines</h2>

<p><strong>Scenario 1: Your Expertise Gets Automated</strong><br/>
In 2025, your job required specialized knowledge and 8-15 years of experience to develop mastery. By 2030, AI systems can perform 70-80% of your job's tasks. The remaining 20-30% requires judgment and context—the human part. But your employer doesn't need judgment for all 200 employees doing your role. They need it for 40-60 employees managing the AI. You applied for the AI management roles, but they went to people from outside your company—people with AI experience that you lack. Your compensation dropped 35%. Your job security declined 40%. You're considering a career change.</p>

<p><strong>Scenario 2: Your Industry Gets Disrupted</strong><br/>
Your industry has survived every disruption for 50 years. You believed it would survive this one too. It hasn't. Your industry's fundamental economics have been restructured. New competitors using AI are doing your job at 40% of your salary. Your company tried to compete on cost, but they can't match pure-play AI competitors. Your company's stock price has declined 30%. They announced "workforce optimization" (layoffs). Your salary and bonus have been frozen for two years. You're questioning your career choice.</p>

<p><strong>Scenario 3: You Stay in Your Lane While Others Escape</strong><br/>
By 2028, you realize the bear case is real. You see peers who learned Python and SQL in 2025-2026 getting promoted to AI-adjacent roles earning $180,000+. You see peers who pivoted industries finding new roles in booming sectors. But you stayed in your lane, doing what you'd always done. You didn't invest in new skills. You didn't network outside your company. By 2030, you're stuck. Your current role is at risk. Your industry is declining. Your skills aren't transferable. You're facing a forced career change at the worst possible time, when the labor market has shifted against your demographic and skill profile.</p>

<h2>THE BULL CASE: How You Escape</h2>

<p><strong>Scenario 1: You Become an AI-Augmented Expert</strong><br/>
In 2025, you recognized that AI would automate your job's routine work. Instead of resisting, you learned AI tools. You took online courses in Python and SQL. You learned how to use AI systems in your domain. By 2027, you were using AI to do your job better and faster. You covered 3x more account territory because AI handled the research and analysis. Your effectiveness metrics improved. Your compensation increased to $185,000 by 2029. Your job security improved because you were more valuable to your employer. By 2030, you're a hybrid: 20% human judgment, 80% AI-augmented execution. And you're thriving.</p>

<p><strong>Scenario 2: You Pivot to a High-Growth Industry</strong><br/>
In 2025, you recognized your industry was declining. You started exploring adjacent industries with better growth profiles. By 2026, you had transitioned to renewable energy (if you were in oil), biotech (if you were in pharmaceuticals), or AI infrastructure (if you were in traditional IT). You took a lateral move at slightly lower pay ($105,000 versus $110,000), but your new industry was growing. By 2030, your salary was $165,000 because your new industry was booming. Your career trajectory was positive. You'd made a hard move in 2025-2026 and benefited for the next five years.</p>

<p><strong>Scenario 3: You Transition into Leadership and Strategy</strong><br/>
In 2025, you realized that management skill is increasingly scarce. As AI automates individual contributor work, people who can lead teams, think strategically, and make judgment calls become more valuable. You spent 2025-2027 developing leadership skills: you took management training courses, you volunteered to lead cross-functional projects, you built your professional network. By 2027, you were promoted to a management role overseeing AI implementation for your domain. By 2030, you were managing a team of 15 AI specialists and domain experts, earning $240,000. Your career had transformed from being vulnerable to automation to being positioned for continued growth.</p>

<h2>WHAT YOU SHOULD DO NOW</h2>

<p><strong>1. Audit Your AI Vulnerability (This Month, $0)</strong><br/>
What percentage of your job is automatable? Document your time: 40% on routine analysis? 30% on document review? 20% on customer relationship? 10% on strategy? The first 40-30% will be automated within 36 months. The last 30% might never be automated—it's the human part. Your job security depends on transitioning your time from the automatable 70% into the non-automatable 30%. Do this audit now.</p>

<p><strong>2. Learn AI Tools in Your Domain (Q1-Q2 2030, $2,000-$5,000)</strong><br/>
Don't learn general AI theory. Learn AI tools specific to your domain. If you're in finance, learn AI for financial forecasting. If you're in marketing, learn AI for customer segmentation. Take one relevant online course (Coursera, DataCamp, etc.). Cost: $300-$800. By April 2030, you should be able to use one AI tool better than your average peer. This is table stakes for career continuity.</p>

<p><strong>3. Build Your Personal Network Outside Your Company (Q2-Q4 2030, $0)</strong><br/>
Your company might disappear (bankruptcy, acquisition, restructuring). Your personal network is your insurance policy. Spend 5 hours per week building relationships: go to industry conferences, engage on LinkedIn, join online communities in your field. By December 2030, you should have 20-30 meaningful external relationships. If you need to job-search in 2031-2032, this network will be invaluable.</p>

<p><strong>4. Identify Your 5-Year Career Goal (Q3 2030, $0)</strong><br/>
Do you want to stay in your current industry or pivot? Do you want to transition into management or stay as a specialist? Do you want to stay with your current company or move? Answer these questions now, while you have the luxury of planning. By Q4 2030, you should have a clear 5-year plan: which skills to develop, which roles to target, which industries to focus on.</p>

<p><strong>5. Develop Skills Aligned with Your Goal (Q4 2030 - Q4 2032)</strong><br/>
If your goal is AI-augmented expertise in your current domain: spend 300 hours learning AI tools. Cost: $4,000-$8,000. Timeline: 18 months of 5 hours/week learning. If your goal is management: take management training courses and volunteer for leadership projects. Cost: $3,000-$6,000. Timeline: 24 months. If your goal is industry transition: build networks in your target industry and learn their domain-specific language. Cost: $2,000-$4,000. Timeline: 12-18 months. All of these paths are open to you. Choose one and execute.</p>

<p><strong>6. Monitor Your Company's AI Transition (Ongoing, $0)</strong><br/>
Track your company's AI investments, workforce changes, and strategic announcements. If your company is investing heavily in AI and treating workforce transition seriously (retraining programs, internal mobility), you're likely safe. If your company is not investing in AI or is cutting costs aggressively without retraining, your risk level is high. Use this information to time your decisions: stay if your company is investing, leave if it's not.</p>

<h2>THE BOTTOM LINE</h2>

<p>Your career in {s['name']} between 2025 and 2030 was determined by decisions you made in 2025. The professionals who thrived are those who recognized AI would disrupt their role and either learned to work with AI or pivoted to new industries or roles. The professionals who are struggling are those who resisted change, believed their expertise was safe, and waited until forced to adapt. If you're reading this in June 2030, some choices have already been made for you. But your next 5 years are still under your control. Choose wisely.</p>"""

    url = f"https://ai2030report.com/articles/sectors-{s['sector_full']}-employees.html"
    og_title = f"AI 2030: {s['name']} — Career Impact (Employee Edition)"
    og_desc = f"Will AI take your job in {s['name']}? Two scenarios: resist vs adapt."

    refs_html = '<div class="references-section"><h2>References &amp; Sources</h2><ol>\n'
    refs = [
        ("WEF: Future of Jobs Report 2030", "https://www.weforum.org"),
        ("Deloitte: AI and Workforce Transformation", "https://www.deloitte.com"),
        ("LinkedIn Learning: Skills Report 2030", "https://www.linkedin.com"),
        ("McKinsey: Skill Shift", "https://www.mckinsey.com"),
        ("MIT Sloan: AI and Employment", "https://mitsloan.mit.edu"),
    ]
    for t, u in refs:
        refs_html += f'<li><a href="{html.escape(u)}" target="_blank" rel="noopener">{html.escape(t)}</a></li>\n'
    refs_html += '</ol></div>'

    pills_html = ''
    for article_type, label in [('ceo', 'CEO'), ('employee', 'Employee'), ('customer', 'Customer')]:
        act = ' active' if article_type == 'employee' else ''
        pills_html += f'<a href="#" class="sibling-pill{act}">{label}</a>\n'

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
<title>{html.escape(og_title)}</title>
<meta name="description" content="{html.escape(og_desc[:160])}">
<meta property="og:title" content="{html.escape(og_title)}">
<meta property="og:description" content="{html.escape(og_desc[:160])}">
<meta property="og:type" content="article">
<meta property="og:url" content="{url}">
<link rel="canonical" href="{url}">
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"Article","headline":"{html.escape(og_title)}","description":"{html.escape(og_desc[:160])}","url":"{url}","datePublished":"2025-06-01","dateModified":"2026-03-04","author":{{"@type":"Organization","name":"The 2030 Intelligence Report"}}}}
</script>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-S9Z93KZ2Z2"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('js',new Date());gtag('config','G-S9Z93KZ2Z2');</script>
{get_css()}
</head>
<body>
<div class="reading-progress" id="readingProgress"></div>
<header class="site-header"><div class="header-inner">
<a href="/" class="site-logo">The 2030 Intelligence Report</a>
<nav><ul class="nav-links"><li><a href="/">Home</a></li><li><a href="/browse/sectors.html">Sectors</a></li></ul></nav>
<button class="theme-toggle" id="themeToggle" title="Toggle theme">&#9788;</button>
</div></header>
<nav class="breadcrumb"><a href="/">Home</a> <span>&rsaquo;</span> <a href="/browse/sectors.html">Sectors</a> <span>&rsaquo;</span> <a href="#">{html.escape(s['name'])}</a> <span>&rsaquo;</span> <span>Employee Edition</span></nav>
<div class="article-header"><div class="article-meta">
<span class="meta-badge badge-country">{html.escape(s['name'])}</span>
<span class="meta-badge badge-audience">Employee & Workforce</span>
<span class="meta-badge badge-date">Updated June 2030</span>
</div></div>
<div class="sibling-editions"><h3>View other perspectives:</h3><div class="sibling-pills">{pills_html}</div></div>
<article class="article-content">
{article_body}
<div class="social-share-bar"><span>Share:</span>
<a href="https://www.linkedin.com/sharing/share-offsite/?url={url}" target="_blank" rel="noopener" class="share-btn linkedin">LinkedIn</a>
<a href="https://twitter.com/intent/tweet?url={url}" target="_blank" rel="noopener" class="share-btn twitter">X / Twitter</a>
</div>
{refs_html}
<div class="feedback-bar">
<a href="mailto:feedback@ai2030report.com">&#9993; Send Feedback</a>
</div></article>
<footer class="site-footer"><p>&copy; 2025-2026 The 2030 Intelligence Report.</p></footer>
<button class="scroll-top" id="scrollTop" onclick="window.scrollTo({{top:0,behavior:'smooth'}})">&#8593;</button>
<script>
window.addEventListener('scroll',function(){{var h=document.documentElement,b=document.body;var pct=(h.scrollTop||b.scrollTop)/((h.scrollHeight||b.scrollHeight)-h.clientHeight)*100;document.getElementById('readingProgress').style.width=pct+'%'}});
</script>
</body></html>"""

    return html_content


def generate_customer_article(sector_key, sector_data):
    """Generate Customer article for a sector."""
    s = sector_data
    memo_header = f"""<div class="memo-header">
    <strong>A MACRO INTELLIGENCE MEMO</strong><br/>
    JUNE 2030<br/>
    FOR {s['name'].upper()} CUSTOMERS • CONSUMER & USER PERSPECTIVE
</div>"""

    article_body = f"""{memo_header}

<p style="font-size: 1.1em; font-weight: 500; margin-bottom: 20px;">
{s['customer_intro']}
</p>

<h2>THE BEAR CASE: How Customers Lose</h2>

<p><strong>Scenario 1: Prices Don't Fall Despite Commoditization</strong><br/>
AI has made {s['name']} production dramatically more efficient. Costs should fall. Prices should fall with them. But they haven't. Companies have captured the cost savings as margin expansion rather than price reductions. Your typical product cost has declined 25% to produce, but your price has increased 8%. Companies are using AI efficiency to increase profitability, not to increase customer value. You're paying more for equivalent products.</p>

<p><strong>Scenario 2: Service Gets Worse While Prices Stay Same</strong><br/>
Customer service has been almost entirely automated. You can no longer reach a human when you have a complex issue. AI chatbots handle your simple questions adequately. But they can't solve your unusual problem. Your wait time for human support is now 2-3 days (versus 4 hours in 2025). Your satisfaction with customer service has declined 40%. You're paying the same price for worse service.</p>

<p><strong>Scenario 3: Personalization Gets Creepy</strong><br/>
AI knows too much about you. The prices you're offered vary based on your purchase history, your income level (inferred from data brokers), and your willingness to pay (inferred from your browsing behavior). What looks like "personalization" is actually price discrimination. You're paying 20-30% more than a better-informed customer simply because the AI has identified you as less price-sensitive. You feel manipulated.</p>

<h2>THE BULL CASE: How Customers Win</h2>

<p><strong>Scenario 1: Prices Fall and Quality Improves</strong><br/>
Companies using AI efficiently have reinvested cost savings into customer value. Your typical product is 15% cheaper and 20% higher quality than 2025 equivalents. You're getting better products at lower prices. Competition has driven pricing discipline: any company trying to pocket all the cost savings gets undercut by competitors passing savings to customers.</p>

<p><strong>Scenario 2: Service Gets Hyper-Personalized</strong><br/>
AI knows your preferences, your previous purchases, your stated preferences. When you contact a company, the AI has already identified your likely issue and is prepared with solutions tailored to your situation. Your support time has dropped to 15 minutes on average. You feel understood. Your satisfaction with customer service has increased 35%.</p>

<p><strong>Scenario 3: You Control Your Data</strong><br/>
You understand what data companies are collecting and have opted out of data collection you don't want. Companies have been transparent about how they use data. You've chosen to share your data in exchange for better personalization and lower prices. You feel in control, not manipulated. The personalization you receive feels fair—it's based on your explicit choices, not inferred manipulation.</p>

<h2>WHAT YOU SHOULD DO NOW</h2>

<p><strong>1. Understand Your Leverage</strong><br/>
You have leverage you may not realize. Competition is intense in most industries. If a company treats you poorly, you can switch to a competitor in seconds (online). Companies know this. If you're unhappy, tell them. If they don't respond, vote with your wallet. This simple principle will drive better outcomes throughout {s['name']} by 2030.</p>

<p><strong>2. Demand Transparency</strong><br/>
Ask companies how they use your data, how they set prices, and why customer service quality has changed. Companies that are transparent about their practices are usually companies that have nothing to hide. Companies that are opaque are often hiding price discrimination or data misuse. Transparency is a signal of trustworthiness.</p>

<p><strong>3. Compare Options Actively</strong><br/>
Don't assume your current vendor is the best. Every 6-12 months, spend 30 minutes comparing your current option against 2-3 competitors. Switching costs have declined dramatically—it should take minutes, not days. By comparing actively, you ensure you're getting fair value.</p>

<p><strong>4. Optimize for Outcomes, Not Loyalty</strong><br/>
Brand loyalty is a luxury you can no longer afford. Optimize for outcomes: best price, best quality, best service. If your loyal vendor stops delivering, switch without guilt. Companies have no loyalty to you (they'll replace you with a cheaper customer); you should extend the same courtesy to them.</p>

<p><strong>5. Advocate for Better Practices</strong><br/>
If a company engages in predatory practices—price discrimination, data misuse, poor service—tell others. Write reviews, post on social media, contact your representative. Companies are sensitive to reputation. Collective customer action drives better outcomes.</p>

<h2>THE BOTTOM LINE</h2>

<p>Your experience with {s['name']} in 2030 depends on choices: whether you're passive and accept whatever companies offer, or active and demand better value. Companies have no incentive to treat passive customers well. They have every incentive to treat active, aware customers well. The customers who are thriving in the AI economy of 2030 are those who understand their leverage, compare options actively, and switch when necessary. The customers who are losing are those who assume companies care about them, who never compare alternatives, and who accept worse value in the name of convenience or loyalty. Your choice will determine your experience.</p>"""

    url = f"https://ai2030report.com/articles/sectors-{s['sector_full']}-customers.html"
    og_title = f"AI 2030: {s['name']} — Customer Impact"
    og_desc = f"How AI changes what you pay and what you get in {s['name']}."

    refs_html = '<div class="references-section"><h2>References &amp; Sources</h2><ol>\n'
    refs = [
        ("Consumer Reports: AI Pricing & Discrimination", "https://www.consumerreports.org"),
        ("FTC: Algorithmic Transparency Report", "https://www.ftc.gov"),
        ("Harvard Law: Tech & Consumer Protection", "https://cyber.harvard.edu"),
        ("MIT Media Lab: Value & Price in AI Markets", "https://media.mit.edu"),
        ("Pew Research: Consumer Trust in AI", "https://www.pewresearch.org"),
    ]
    for t, u in refs:
        refs_html += f'<li><a href="{html.escape(u)}" target="_blank" rel="noopener">{html.escape(t)}</a></li>\n'
    refs_html += '</ol></div>'

    pills_html = ''
    for article_type, label in [('ceo', 'CEO'), ('employee', 'Employee'), ('customer', 'Customer')]:
        act = ' active' if article_type == 'customer' else ''
        pills_html += f'<a href="#" class="sibling-pill{act}">{label}</a>\n'

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
<title>{html.escape(og_title)}</title>
<meta name="description" content="{html.escape(og_desc[:160])}">
<meta property="og:title" content="{html.escape(og_title)}">
<meta property="og:description" content="{html.escape(og_desc[:160])}">
<meta property="og:type" content="article">
<meta property="og:url" content="{url}">
<link rel="canonical" href="{url}">
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"Article","headline":"{html.escape(og_title)}","description":"{html.escape(og_desc[:160])}","url":"{url}","datePublished":"2025-06-01","dateModified":"2026-03-04","author":{{"@type":"Organization","name":"The 2030 Intelligence Report"}}}}
</script>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-S9Z93KZ2Z2"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('js',new Date());gtag('config','G-S9Z93KZ2Z2');</script>
{get_css()}
</head>
<body>
<div class="reading-progress" id="readingProgress"></div>
<header class="site-header"><div class="header-inner">
<a href="/" class="site-logo">The 2030 Intelligence Report</a>
<nav><ul class="nav-links"><li><a href="/">Home</a></li><li><a href="/browse/sectors.html">Sectors</a></li></ul></nav>
<button class="theme-toggle" id="themeToggle" title="Toggle theme">&#9788;</button>
</div></header>
<nav class="breadcrumb"><a href="/">Home</a> <span>&rsaquo;</span> <a href="/browse/sectors.html">Sectors</a> <span>&rsaquo;</span> <a href="#">{html.escape(s['name'])}</a> <span>&rsaquo;</span> <span>Customer Edition</span></nav>
<div class="article-header"><div class="article-meta">
<span class="meta-badge badge-country">{html.escape(s['name'])}</span>
<span class="meta-badge badge-audience">Customer & Consumer</span>
<span class="meta-badge badge-date">Updated June 2030</span>
</div></div>
<div class="sibling-editions"><h3>View other perspectives:</h3><div class="sibling-pills">{pills_html}</div></div>
<article class="article-content">
{article_body}
<div class="social-share-bar"><span>Share:</span>
<a href="https://www.linkedin.com/sharing/share-offsite/?url={url}" target="_blank" rel="noopener" class="share-btn linkedin">LinkedIn</a>
<a href="https://twitter.com/intent/tweet?url={url}" target="_blank" rel="noopener" class="share-btn twitter">X / Twitter</a>
</div>
{refs_html}
<div class="feedback-bar">
<a href="mailto:feedback@ai2030report.com">&#9993; Send Feedback</a>
</div></article>
<footer class="site-footer"><p>&copy; 2025-2026 The 2030 Intelligence Report.</p></footer>
<button class="scroll-top" id="scrollTop" onclick="window.scrollTo({{top:0,behavior:'smooth'}})">&#8593;</button>
<script>
window.addEventListener('scroll',function(){{var h=document.documentElement,b=document.body;var pct=(h.scrollTop||b.scrollTop)/((h.scrollHeight||b.scrollHeight)-h.clientHeight)*100;document.getElementById('readingProgress').style.width=pct+'%'}});
</script>
</body></html>"""

    return html_content


def main():
    """Generate all sector articles."""
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    articles_dir = os.path.join(os.getcwd(), "articles")
    if not os.path.exists(articles_dir):
        os.makedirs(articles_dir)

    count = 0
    for sector_key in sorted(SECTORS.keys()):
        if not SECTORS[sector_key].get('ceo_intro'):
            # Skip incomplete sectors
            continue

        sector_data = SECTORS[sector_key]

        # Generate CEO article
        ceo_html = generate_ceo_article(sector_key, sector_data)
        ceo_path = os.path.join(articles_dir, f"sectors-{sector_data['sector_full']}-incumbent-ceos.html")
        with open(ceo_path, 'w', encoding='utf-8') as f:
            f.write(ceo_html)
        print(f"✓ {sector_data['name']} - CEO article")
        count += 1

        # Generate Employee article
        emp_html = generate_employee_article(sector_key, sector_data)
        emp_path = os.path.join(articles_dir, f"sectors-{sector_data['sector_full']}-employees.html")
        with open(emp_path, 'w', encoding='utf-8') as f:
            f.write(emp_html)
        print(f"✓ {sector_data['name']} - Employee article")
        count += 1

        # Generate Customer article
        cust_html = generate_customer_article(sector_key, sector_data)
        cust_path = os.path.join(articles_dir, f"sectors-{sector_data['sector_full']}-customers.html")
        with open(cust_path, 'w', encoding='utf-8') as f:
            f.write(cust_html)
        print(f"✓ {sector_data['name']} - Customer article")
        count += 1

    print(f"\nDone! Generated {count} articles.")


if __name__ == "__main__":
    main()
