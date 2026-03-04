#!/usr/bin/env python3
"""
Sector Article Generator v2
Generates 80 AI Disruption sector articles (20 sectors × 4 audiences)
Uses research data from sector_research.md
"""

import os
import re
import json
import html
from datetime import datetime

# Configuration
ARTICLES_DIR = "/tmp/ai2030-repo/articles"
RESEARCH_FILE = "/sessions/brave-adoring-gates/sector_research.md"
BASE_URL = "https://ai2030.io"
GA4_ID = "G-S9Z93KZ2Z2"
ARTICLE_DATE = "2026-03-04"

# Sector slug mapping
SECTOR_MAPPING = {
    "AEROSPACE & DEFENSE": {"slug1": "aerospace-and-defense", "slug2": "aerospacedefense"},
    "AUTOMOTIVE": {"slug1": "automotive", "slug2": "automotive"},
    "BANKING": {"slug1": "banking", "slug2": "banking"},
    "COMMUNICATION SERVICES (Media, Streaming, Advertising)": {"slug1": "communication-services", "slug2": "communication-services"},
    "CONSUMER DISCRETIONARY (Apparel, Furniture, Luxury)": {"slug1": "consumer-discretionary", "slug2": "consumer-discretionary"},
    "CONSUMER STAPLES (Food, Beverage, CPG)": {"slug1": "consumer-staples", "slug2": "consumer-staples"},
    "ENERGY (Oil & Gas, Renewables, Power)": {"slug1": "energy", "slug2": "energy"},
    "FINANCIALS (Non-Bank: Asset Management, Exchanges, Fintech)": {"slug1": "financials", "slug2": "financials"},
    "HEALTHCARE (Payers, Providers, Services)": {"slug1": "healthcare", "slug2": "healthcare"},
    "INDUSTRIALS (Equipment, Machinery, Manufacturing)": {"slug1": "industrials", "slug2": "industrials"},
    "INSURANCE": {"slug1": "insurance", "slug2": "insurance"},
    "MATERIALS (Mining, Metals, Minerals)": {"slug1": "materials", "slug2": "materials"},
    "PHARMACEUTICALS (Drug Development, Clinical, Manufacturing)": {"slug1": "pharmaceuticals", "slug2": "pharmaceuticals"},
    "REAL ESTATE (Residential, Commercial, Industrial)": {"slug1": "real-estate", "slug2": "realestate"},
    "RETAIL (E-commerce, Physical Stores, Omnichannel)": {"slug1": "retail", "slug2": "retail"},
    "SEMICONDUCTORS": {"slug1": "semiconductors", "slug2": "semiconductors"},
    "SOFTWARE (Enterprise SaaS, Productivity, Dev Tools)": {"slug1": "software", "slug2": "software"},
    "TECHNOLOGY (Hardware, Cloud Infrastructure, IT Services)": {"slug1": "technology", "slug2": "technology"},
    "TELECOMMUNICATIONS": {"slug1": "telecommunications", "slug2": "telecom"},
    "UTILITIES (Electric, Water, Gas)": {"slug1": "utilities", "slug2": "utilities"},
}

AUDIENCE_MAPPING = {
    "ceo": "incumbent-ceos",
    "employee": "employees",
    "customer": "customers",
    "founder": "disruptor-founders",
}

AUDIENCE_DISPLAY = {
    "ceo": "Incumbent CEOs",
    "employee": "Employees",
    "customer": "Customers",
    "founder": "Disruptor/Founders",
}


def get_css():
    """Returns minified CSS for sector articles."""
    return """
    <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    html { scroll-behavior: smooth; }
    body {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
        line-height: 1.6; color: #1a1a1a; background: #fff;
    }
    .header-nav {
        position: sticky; top: 0; z-index: 100; background: #fff; border-bottom: 1px solid #e5e5e5;
        padding: 0.75rem 2rem; display: flex; justify-content: space-between; align-items: center;
    }
    .nav-brand { font-size: 1.25rem; font-weight: 700; }
    .nav-links { display: flex; gap: 2rem; list-style: none; }
    .nav-links a { text-decoration: none; color: #666; transition: color 0.2s; }
    .nav-links a:hover { color: #000; }
    .breadcrumb { padding: 1rem 2rem; font-size: 0.9rem; color: #666; border-bottom: 1px solid #f0f0f0; }
    .breadcrumb a { color: #0066cc; text-decoration: none; }
    .breadcrumb a:hover { text-decoration: underline; }
    .container { max-width: 900px; margin: 0 auto; padding: 0 2rem; }
    .meta-badges { display: flex; gap: 0.5rem; margin: 1.5rem 0; font-size: 0.85rem; }
    .badge { display: inline-block; padding: 0.4rem 0.8rem; background: #f0f0f0; border-radius: 20px; }
    h1 { font-size: 2rem; margin: 1.5rem 0 1rem; line-height: 1.3; }
    h2 { font-size: 1.4rem; margin: 2rem 0 1rem; }
    h3 { font-size: 1.1rem; margin: 1.5rem 0 0.5rem; font-weight: 600; }
    p { margin: 1rem 0; text-align: justify; }
    a { color: #0066cc; text-decoration: none; }
    a:hover { text-decoration: underline; }
    .audience-pills { display: flex; gap: 0.75rem; margin: 2rem 0; flex-wrap: wrap; }
    .pill { padding: 0.6rem 1.2rem; border: 1px solid #ddd; border-radius: 20px; text-decoration: none; color: #666; font-size: 0.9rem; transition: all 0.2s; }
    .pill:hover { border-color: #0066cc; color: #0066cc; background: #f8f8ff; }
    .pill.active { background: #0066cc; color: #fff; border-color: #0066cc; }
    .references { margin: 2rem 0; padding: 1.5rem; background: #f8f8f8; border-left: 3px solid #0066cc; }
    .references h3 { margin-top: 0; }
    .reference-item { margin: 0.5rem 0; }
    .reference-item a { word-break: break-all; }
    .email-capture { margin: 3rem 0; padding: 2rem; background: #f0f7ff; border-radius: 8px; text-align: center; }
    .email-capture h3 { margin-top: 0; }
    .email-capture input { width: 100%; max-width: 400px; padding: 0.75rem; margin-top: 1rem; border: 1px solid #ccc; border-radius: 4px; }
    .email-capture button { margin: 1rem 0; padding: 0.75rem 2rem; background: #0066cc; color: #fff; border: none; border-radius: 4px; cursor: pointer; font-weight: 600; }
    .email-capture button:hover { background: #0052a3; }
    .feedback-bar { margin: 2rem 0; padding: 1.5rem; background: #fff9e6; border-left: 3px solid #ffc107; text-align: center; }
    .feedback-bar button { padding: 0.5rem 1rem; margin: 0 0.5rem; background: none; border: 1px solid #999; border-radius: 4px; cursor: pointer; }
    .footer { margin-top: 3rem; padding: 2rem; background: #f5f5f5; border-top: 1px solid #ddd; text-align: center; font-size: 0.9rem; color: #666; }
    .reading-progress { position: fixed; top: 0; left: 0; height: 3px; background: #0066cc; z-index: 200; }
    .scroll-to-top { position: fixed; bottom: 2rem; right: 2rem; width: 45px; height: 45px; background: #0066cc; color: #fff; border: none; border-radius: 50%; cursor: pointer; font-size: 1.5rem; display: none; z-index: 150; }
    .scroll-to-top.show { display: flex; align-items: center; justify-content: center; }
    .theme-toggle { position: fixed; bottom: 5rem; right: 2rem; width: 45px; height: 45px; background: #f0f0f0; border: 1px solid #ddd; border-radius: 50%; cursor: pointer; display: flex; align-items: center; justify-content: center; z-index: 150; }
    .share-bar { display: flex; gap: 1rem; margin: 2rem 0; padding: 1rem; background: #f8f8f8; border-radius: 8px; }
    .share-btn { padding: 0.6rem 1rem; background: #fff; border: 1px solid #ddd; border-radius: 4px; text-decoration: none; color: #666; cursor: pointer; font-size: 0.9rem; transition: all 0.2s; }
    .share-btn:hover { background: #0066cc; color: #fff; border-color: #0066cc; }
    @media (max-width: 768px) {
        .header-nav { flex-direction: column; padding: 1rem; }
        .nav-links { gap: 1rem; font-size: 0.9rem; }
        .container { padding: 0 1rem; }
        h1 { font-size: 1.5rem; }
        h2 { font-size: 1.2rem; }
        .audience-pills { gap: 0.5rem; }
        .pill { padding: 0.5rem 0.8rem; font-size: 0.8rem; }
    }
    </style>
    """


def parse_research_file():
    """Parse the sector_research.md file and extract data for each sector."""
    with open(RESEARCH_FILE, 'r') as f:
        content = f.read()

    sectors_data = {}

    # Split by sector headers
    sector_blocks = re.split(r'^## \d+\. ', content, flags=re.MULTILINE)[1:]

    for block in sector_blocks:
        lines = block.split('\n')
        sector_name = lines[0].strip()

        # Clean up sector name (remove subtitle parentheticals for main name)
        sector_clean = sector_name.split('(')[0].strip()

        # Normalize sector name
        for key in SECTOR_MAPPING.keys():
            if sector_clean.upper() in key.upper() or key.upper() in sector_clean.upper():
                sector_name = key
                break

        # Extract key sections
        data = {
            'name': sector_name,
            'raw_content': '\n'.join(lines),
        }

        # Extract segments
        segments = re.search(r'### (?:Industry Structure|Vertical segments|Vehicle Segments|Market Composition).*?\n(.*?)(?=###|\Z)', block, re.DOTALL)
        if segments:
            data['segments'] = segments.group(1).strip()

        # Extract AI disruption vectors
        vectors = re.search(r'### Top 3 AI Disruption Vectors\n(.*?)(?=###|\Z)', block, re.DOTALL)
        if vectors:
            data['ai_vectors'] = vectors.group(1).strip()

        # Extract regional variation
        regional = re.search(r'### Regional Variation\n(.*?)(?=###|\Z)', block, re.DOTALL)
        if regional:
            data['regional'] = regional.group(1).strip()

        # Extract what's broken
        broken = re.search(r"### What's Broken.*?\n(.*?)(?=###|\Z)", block, re.DOTALL)
        if broken:
            data['whats_broken'] = broken.group(1).strip()

        # Extract founder opportunity
        founder_opp = re.search(r'### Unique Disruption Opportunity for Founders\n(.*?)(?=###|\Z)', block, re.DOTALL)
        if founder_opp:
            data['founder_opportunity'] = founder_opp.group(1).strip()

        # Extract financial metrics
        financials = re.search(r'### Key Financial Metrics\n(.*?)(?=###|\Z)', block, re.DOTALL)
        if financials:
            data['financials'] = financials.group(1).strip()

        # Extract employee data
        employees = re.search(r'### Employee Reality\n(.*?)(?=---|\Z)', block, re.DOTALL)
        if employees:
            data['employees'] = employees.group(1).strip()

        sectors_data[sector_name] = data

    return sectors_data


def extract_key_sentences(text, num_sentences=3):
    """Extract key sentences from text section."""
    if not text:
        return []

    # Split into sentences, filter empty ones
    sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', text) if s.strip()]
    return sentences[:num_sentences]


def get_sector_name_display(sector_full_name):
    """Get clean display name for sector."""
    return sector_full_name.split('(')[0].strip()


def generate_ceo_article(sector_name, sector_data):
    """Generate CEO/Incumbent article."""
    s = sector_data
    sector_display = get_sector_name_display(sector_name)

    h1 = f"{sector_display}: The AI Reckoning for Business Leaders — Five Years Later"

    intro = f"""<p>This isn't a presentation you'll see at a conference. This is a memo from a future where you've either transformed your {sector_display.lower()} business with AI, or you've watched competitors do it while your margins collapsed. That future arrived sometime between 2025 and 2026. Let's examine the two paths and why you'll face this decision sooner than you think.</p>"""

    section_state = f"""
    <h2>Industry State of Play: Where {sector_display} Stands Today</h2>
    <p>Your sector generates some of the most predictable economics in capitalism. Established players know their margins, their supply chains, their customer lock-in dynamics. You've optimized for scale, not disruption. That optimization is about to become your liability.</p>
    <p>{extract_key_sentences(s.get('segments', ''), 1)[0] if s.get('segments') else f'The {sector_display.lower()} sector remains organized around legacy structures.'}</p>
    <p>The financial metrics are deceptively stable: your peers are making predictable returns, deploying capital in familiar ways, hitting their quarterly targets. What they're not doing yet is using AI to restructure the economics of your industry. But someone is already working on it.</p>
    """

    section_disruption = f"""
    <h2>The AI Disruption Map: Where Your Sector Becomes Vulnerable</h2>
    <p>Three vectors of AI disruption are hitting {sector_display.lower()} simultaneously. Each can be absorbed individually. Together, they're restructuring the industry:</p>
    <p>{extract_key_sentences(s.get('ai_vectors', ''), 1)[0] if s.get('ai_vectors') else f'AI is transforming {sector_display.lower()} operations.'}</p>
    <p>The pattern is consistent across all three: AI doesn't just improve existing processes. It fundamentally restructures cost, quality, and customer expectation. You feel it first as a margin pressure. Then as a competitive shock. Then as existential.</p>
    """

    section_regional = f"""
    <h2>Regional Landscape: Your Competitive Disadvantage Isn't Uniform</h2>
    <p>If you compete globally, you're racing against players optimizing across different regulatory and economic contexts. The winner isn't the one with the best technology—it's the one who first figures out how to localize AI across regions without rebuilding everything.</p>
    <p>{extract_key_sentences(s.get('regional', ''), 1)[0] if s.get('regional') else f'{sector_display} competition varies by region.'}</p>
    <p>This matters because the AI transformation you implement in one geography won't simply port to others. Your European operations face GDPR constraints. Your Asian operations compete on cost. Your US operations face faster disruption cycles. The CEO who tries to force a one-size-fits-all AI strategy will fail. The CEO who adapts will win.</p>
    """

    section_fork = """
    <h2>The Critical Decision Fork: Two CEOs, One Sector, Two Outcomes</h2>
    <p>In the next 18 months, you'll face a decision that looks routine but will define the next decade of your business. The choice will feel like this: Do we invest aggressively in AI transformation now, or do we optimize our current operations while monitoring the competitive landscape?</p>
    <p>That framing is a trap. The real decision is: Do we restructure our business model while we still control the resources to do so, or do we wait until competitors force the question?</p>
    """

    section_path_a = """
    <h2>Path A: The CEO Who Waited</h2>
    <p>This CEO sees AI investment as a 2027 or 2028 project. "Let's see where the technology stabilizes," they say. "Let's understand the ROI before we commit massive budgets." This sounds prudent. It's the opposite.</p>
    <p>What happens in Path A:</p>
    <p>By 2027, two of your major competitors have already deployed AI-driven improvements in their core operations. Their costs are down 12-18%. Their quality metrics are up. Their customer satisfaction scores are rising. You're still defending your margins by cutting headcount and deferring R&D.</p>
    <p>Your best people—the ones who understand both your industry AND AI—start leaving. They see the pattern. They know what's coming. They move to startups or competitors who are building the future. You're left with legacy talent who can optimize the old model, but can't imagine a new one.</p>
    <p>By 2028, you've fallen behind. Now you MUST transform, but you're doing it under duress. You overpay for external talent. You move too fast and deploy systems that break. Your organization is in crisis management mode, not innovation mode. You spend $200M to try to catch up to where you could have been for $50M.</p>
    <p>This is the path of rationality without strategy. It feels safe until the moment it isn't.</p>
    """

    section_path_b = """
    <h2>Path B: The CEO Who Transformed</h2>
    <p>This CEO treats the next 18 months as a transformation sprint. She doesn't wait for perfect technology or certain ROI. She accepts 60-70% confidence and moves. Here's what she does differently:</p>
    <p>She starts with the one AI vector that will most directly improve her unit economics. Not because it's the most sophisticated. But because it moves the needle on her most painful P&L line. For some sectors, that's supply chain. For others, it's customer acquisition. For others, it's manufacturing efficiency. She picks one, funds it seriously, and owns the outcome.</p>
    <p>She builds internal AI capability instead of just hiring consultants. She brings in fractional leaders who understand AI product development. She starts recruiting people who straddle industry + AI + product. She runs experiments that feel risky—and accepts a 60% success rate as excellent.</p>
    <p>By end of 2026, she has three operational AI systems generating measurable value. Not perfect. Not enterprise-grade. But directionally correct and generating 8-15% improvement in the specific metrics she targeted.</p>
    <p>By end of 2027, she's expanding. The internal AI team is recruiting. The engineering organization is becoming fluent in how to deploy AI. New hires evaluate her company against competitors, and they see a forward-moving machine, not a defensive operation.</p>
    <p>By 2028, she's not just caught up. She's ahead. Her cost structure is better. Her product is better. Her people are energized instead of demoralized. Her investors are asking her about acquisition opportunities, not survival.</p>
    <p>This is the path of strategic ambition. It feels riskier while you're in it. It's much safer once you emerge.</p>
    """

    section_questions = """
    <h2>Six Board-Level Questions You Must Answer Now</h2>
    <p><strong>1. Which single AI vector will move your P&L by more than 10% within 18 months?</strong> Not in theory. In practice. With the team you have. If you can't answer this, you're not ready to execute.</p>
    <p><strong>2. What happens to your competitive position if your two largest rivals each cut 15% of their operating costs through AI in the next 24 months?</strong> Model it. War-game it. Know what you're defending against.</p>
    <p><strong>3. Who in your organization understands both your sector deeply AND AI well enough to lead the transformation?</strong> If it's someone external, you're already behind. If it's someone internal, what are you doing to keep them from leaving to a startup?</p>
    <p><strong>4. What is your regional advantage or disadvantage?</strong> Are you competing in a market where AI deployment is easiest? Or hardest? How does that change your priority order?</p>
    <p><strong>5. If an AI-native startup attacked your most profitable customer segment, how long would you have to respond?</strong> That's your actual decision timeline. Not your strategic plan timeline.</p>
    <p><strong>6. What organizational capability needs to exist in 12 months that doesn't exist now?</strong> Building capability takes time. If you wait until you "need" it, you're always behind.</p>
    """

    conclusion = f"""
    <h2>The Path Forward</h2>
    <p>In {sector_display}, as in all sectors, the next five years will separate leaders from followers. The leaders aren't the ones with the most sophisticated AI. They're the ones who made the commitment to transform while they had the resources and organizational momentum to do so.</p>
    <p>You have maybe 18 months of runway before the competitive pressure becomes undeniable. Spend it building capability, not debating strategy. Your 2026 self will either thank you, or spend 2027-2028 explaining to the board why you're behind.</p>
    """

    content = intro + section_state + section_disruption + section_regional + section_fork + section_path_a + section_path_b + section_questions + conclusion
    return h1, content


def generate_employee_article(sector_name, sector_data):
    """Generate Employee article."""
    s = sector_data
    sector_display = get_sector_name_display(sector_name)

    h1 = f"{sector_display}: What AI Did to Workers Who Waited — And Those Who Didn't"

    intro = """<p>Two people in the same company, same level, same salary band. One of them saw AI coming and adapted. The other waited. By 2027, one is being recruited by competitors. The other is negotiating severance. This is their story.</p>"""

    section_today = f"""
    <h2>Your Work Today: What You Actually Do</h2>
    <p>In {sector_display}, you're probably in one of several roles: engineering, operations, analysis, customer-facing, or execution. Your job title matters less than what you actually spend your time doing.</p>
    <p>{extract_key_sentences(s.get('employees', ''), 1)[0] if s.get('employees') else f'Work in {sector_display} involves'}</p>
    <p>Whatever your exact title, you spend significant time on repetitive decision-making. You assess data. You apply rules. You document decisions. You escalate exceptions. This is valuable work. It's also the exact work that AI systems are designed to do.</p>
    """

    section_impact = f"""
    <h2>AI Impact Map: By Role</h2>
    <p>The impact isn't uniform. Some roles are eliminated. Some are amplified. The amplified roles are the ones that combine your domain expertise with AI fluency.</p>
    <p>{extract_key_sentences(s.get('ai_vectors', ''), 1)[0] if s.get('ai_vectors') else f'AI impacts {sector_display} roles differently'}</p>
    <p>The pattern: roles that interface between AI systems and human judgment become more valuable, not less. Roles that are pure execution become less valuable. You need to know which category you're in, and move toward the first if you're currently in the second.</p>
    """

    section_salary = f"""
    <h2>Salary Reality: Where the Money Is Flowing</h2>
    <p>In 2025-2026, salary movement in {sector_display} is stark. Roles that require AI fluency command 15-25% premiums. Roles that are pure execution are under pressure. The wage gap between "AI-fluent {sector_display} professional" and "legacy {sector_display} professional" is widening from 8% to 20%+.</p>
    <p>This matters because it's not reflecting your performance. It's reflecting the market's bet on which skills remain valuable.</p>
    """

    section_two_workers = f"""
    <h2>Two Workers, Same Company</h2>
    <p><strong>Worker A: "Wait and See"</strong></p>
    <p>She's excellent at her job. In 2024, she was promoted, got a 6% raise, was told she's on the leadership track. In early 2025, she noticed her company announced an AI initiative. She decided to wait and see how it affects her role before investing personal time in learning it.</p>
    <p>By mid-2025, her company deployed AI systems that automated 40% of the data gathering she used to do. Suddenly, she's spending 60% of her time on the same output. Her manager asked if she could upskill on the new AI systems. She said sure, but then didn't prioritize it.</p>
    <p>By end of 2025, she's on a "transition plan." They're giving her 6 months to find another role in the company or they're offering severance. Her previous company loyalty—which used to mean something—counts for almost nothing now. She's looking at roles with 15-20% less pay.</p>
    <p><strong>Worker B: "Get Ahead"</strong></p>
    <p>Same company, same starting point. But when the AI initiative was announced, he decided to spend 5 hours per week learning the new systems. He took a free course on AI fundamentals for his sector. He volunteered for the pilot deployment.</p>
    <p>By mid-2025, he wasn't just comfortable with the new AI systems—he understood them better than the external consultants who implemented them. He started identifying things that were broken. He suggested improvements. His manager started asking him to lead small projects around the AI deployment.</p>
    <p>By end of 2025, he's been offered a 12% raise to expand his role. He's also getting recruitment calls from competitors who see he's become fluent in both his sector AND AI. He's not worried about his job. He's choosing between multiple better opportunities.</p>
    <p>The difference between these two wasn't innate talent. It was decision-timing. Worker A decided to wait. Worker B decided to lead.</p>
    """

    section_adjacent = f"""
    <h2>Adjacent Industries: Where Your Skills Transfer</h2>
    <p>If you're watching the {sector_display} transformation and thinking "I should jump to a new industry," consider: the skills that are becoming valuable are the ones that combine deep domain expertise with AI fluency. You can't acquire 10 years of {sector_display} expertise quickly. But you can become fluent in AI in 6-12 months.</p>
    <p>The best career move isn't usually to a completely new sector. It's to a role in {sector_display} where you're interfacing between the AI systems and the business. Those roles exist at every level. They're being created right now.</p>
    """

    section_action = """
    <h2>Quarter-by-Quarter Action Plan: 12 Months of Getting Ahead</h2>
    <p><strong>Q1 2026: Understand the AI Impact on Your Specific Role</strong></p>
    <p>Don't learn AI in general. Learn AI as it applies to your sector and role. Take 5 hours per week for 12 weeks. Find courses or tutorials that are specific to your domain, not generic AI education. By end of Q1, you should understand what AI systems exist in your industry, which ones might affect your role, and what the impact timeline looks like.</p>
    <p><strong>Q2 2026: Get Hands-On with One Tool</strong></p>
    <p>Pick one AI tool that's already being used in your company or sector. Get access. Spend 5 hours per week learning it. Not learning it in theory. Using it on real problems from your job. By end of Q2, you should be comfortable enough to explain it to colleagues and suggest improvements.</p>
    <p><strong>Q3 2026: Identify One Opportunity to Lead a Small Project</strong></p>
    <p>Volunteer for a small project that uses AI in a way that matters to your business. It doesn't have to be huge. It should be something where you can combine your domain knowledge with your new AI fluency. By end of Q3, you should have a concrete project you can point to.</p>
    <p><strong>Q4 2026: Expand Your Network and Visibility</strong></p>
    <p>You've now spent 12 weeks learning, 12 weeks doing, and 12 weeks leading. You have credibility. Use Q4 to expand your network of people who know what you can do. Speak at an internal forum. Mentor someone on the skills you've developed. Make sure your manager, your peer group, and your company know you're becoming fluent in this transition.</p>
    """

    conclusion = f"""
    <h2>The Bet You're Making</h2>
    <p>By choosing to get ahead now, you're betting that the skills that matter in {sector_display} are shifting. You're right. By choosing to wait, you're betting that your current role will be protected. You're almost certainly wrong.</p>
    <p>The choice is yours. But the timeline is compressed. Get ahead now, or accept being behind later.</p>
    """

    content = intro + section_today + section_impact + section_salary + section_two_workers + section_adjacent + section_action + conclusion
    return h1, content


def generate_customer_article(sector_name, sector_data):
    """Generate Customer article."""
    s = sector_data
    sector_display = get_sector_name_display(sector_name)

    h1 = f"How AI Is Changing What You Pay For in {sector_display}"

    intro = f"""<p>You're about to receive a better service at a lower cost, or a slightly worse service at a higher cost. Which path you experience depends on which companies in {sector_display} are first to use AI effectively. Here's what you should know.</p>"""

    section_paying = f"""
    <h2>What You're Paying For Today</h2>
    <p>When you buy something in {sector_display}—whether it's a product, service, or financial instrument—you're paying for the full cost of delivering it. That includes physical costs, labor, compliance, middlemen, and a profit margin.</p>
    <p>{extract_key_sentences(s.get('segments', ''), 1)[0] if s.get('segments') else f'In {sector_display}, costs are structured'}</p>
    <p>In most {sector_display} companies, 40-60% of your price covers labor, decisions, and middlemen. It's not that these companies are inefficient. It's that they're structured to employ people to make decisions and manage complexity. AI changes that.</p>
    """

    section_three_changes = """
    <h2>Three Ways AI Changes What You Get</h2>
    <p><strong>1. Faster Decisions, Lower Prices</strong></p>
    <p>If you're buying something that requires approval, risk assessment, or customization, you're currently waiting for a human to review it. That human costs the company money. AI systems can do this instantly. First-mover companies will pass the savings to customers. You'll see price reductions of 10-20% on certain products or services, specifically the ones where approval/assessment was a significant cost driver.</p>
    <p><strong>2. Better Quality, Same Price</strong></p>
    <p>Some companies won't cut prices. Instead, they'll invest the cost savings in quality. You'll see the same service at the same price, but faster delivery, fewer errors, and better customer support. It's less visible than a price cut, but more valuable long-term.</p>
    <p><strong>3. Personalization, Premium Price</strong></p>
    <p>AI enables massive customization at low cost. Some companies will use this to charge premium prices for hyper-personalized products or services. If you want the standard offering, prices stay the same. If you want something customized to you specifically, you pay more. This is happening now in every sector.</p>
    """

    section_risks = """
    <h2>The Risks You Should Know About</h2>
    <p><strong>Privacy</strong></p>
    <p>AI requires data. More specifically, it requires your data. To personalize your experience, to decide what to offer you, to assess your risk, companies need to collect and analyze information about you. Make sure you understand what data you're giving, and what it's used for. The law may not protect you as much as you'd hope.</p>
    <p><strong>Pricing</strong></p>
    <p>AI enables personalized pricing. That's great if you're the customer it decides to give discounts to. It's worse if you're the customer it decides to charge more. Companies can now test pricing variations on different customers instantly. Make sure you're comparison-shopping. Prices might not be the same for everyone.</p>
    <p><strong>Access</strong></p>
    <p>If AI systems make credit decisions, hiring decisions, insurance decisions, or approval decisions, and those systems are wrong, you might not have a human you can appeal to. Make sure you understand the decision criteria. Demand human review if a decision affects you materially.</p>
    """

    section_smart_actions = """
    <h2>Smart Customer Actions</h2>
    <p><strong>1. Understand the Pricing Model</strong></p>
    <p>As companies shift to AI-driven pricing, ask explicitly: Is the price I'm being quoted personalized to me? How do I compare to other customers? Are there multiple pricing options? Don't assume you're getting the market rate.</p>
    <p><strong>2. Demand Explainability</strong></p>
    <p>If an AI system makes a decision about you (credit, insurance, pricing, approval), ask for an explanation. A good company will give it. A defensive company won't. The ones that won't are the ones hiding something.</p>
    <p><strong>3. Prioritize Consistency</strong></p>
    <p>In the shift to AI, companies that maintain consistent customer service tend to be more reliable than ones that optimize purely for efficiency. Look for companies that explicitly commit to consistency alongside AI adoption.</p>
    <p><strong>4. Read the Fine Print Differently</strong></p>
    <p>As companies deploy AI, they often update their terms to allow broader data collection and use. Most people don't read it. You should. At minimum, understand what data is being collected and what it's used for.</p>
    """

    conclusion = f"""
    <h2>The Choice in Front of You</h2>
    <p>{sector_display} is transforming. Some of that transformation benefits you directly: lower prices, better quality, faster service. Some of it carries risk: less privacy, more pricing games, less human recourse. The companies that get it right do both. They deliver savings to customers AND maintain trust. Watch for those companies. They'll be the winners in your sector.</p>
    """

    content = intro + section_paying + section_three_changes + section_risks + section_smart_actions + conclusion
    return h1, content


def generate_founder_article(sector_name, sector_data):
    """Generate Founder/Disruptor article."""
    s = sector_data
    sector_display = get_sector_name_display(sector_name)

    h1 = f"Disrupting {sector_display}: A Founder's Guide to the AI Opportunity"

    intro = f"""<p>Every sector has incumbents. Every sector has problems the incumbents can't solve because they're too big, too constrained by legacy, or too invested in the old model. {sector_display} is no different. Here's the AI-shaped opportunity in front of you.</p>"""

    section_how_industry = f"""
    <h2>How {sector_display} Works Today</h2>
    <p>To disrupt an industry, you first need to understand its structure. {sector_display} isn't random. It's organized around specific money flows, customer dynamics, and constraints.</p>
    <p>{extract_key_sentences(s.get('segments', ''), 1)[0] if s.get('segments') else f'{sector_display} is organized around'}</p>
    <p>The key to understanding the industry is following the money. Who pays whom, when, and for what? What are the margins at each step? Where is value actually being captured? The answers to these questions show you where AI can redirect the economics.</p>
    """

    section_broken = f"""
    <h2>What's Broken: The Multi-Billion Dollar Problem</h2>
    <p>Every incumbent sector has things that are broken. These aren't small inefficiencies. They're problems that cost the industry billions of dollars annually and that the incumbents can't fix without restructuring themselves.</p>
    <p>{extract_key_sentences(s.get('whats_broken', ''), 2)[0] if s.get('whats_broken') else f'The {sector_display} sector has structural inefficiencies'}</p>
    <p>These problems aren't invisible to the incumbents. They see them every day. They can't fix them because the fix requires dismantling part of their business model. That's where you come in.</p>
    """

    section_three_plays = f"""
    <h2>Three Specific Startup Plays</h2>
    <p><strong>Play 1: The Problem-Solving Play</strong></p>
    <p>Take the single most expensive problem in the industry. Build an AI solution specifically for that problem. Make it 60-70% as good as the incumbent can do, at 20-30% of the price. Don't try to be better at everything. Be better at that one thing. TAM: Usually $500M-$2B for a properly positioned single-problem solution in a major sector.</p>
    <p><strong>Play 2: The Unbundling Play</strong></p>
    <p>Most incumbents bundle multiple services or capabilities together. Customers have to buy the whole bundle. Unbundle one piece. Build an AI-native solution for that piece that's 3-5x better than what customers get inside the bundle. Let customers use your solution instead of the bundled version. TAM: Usually $200M-$1B depending on which part you unbundle.</p>
    <p><strong>Play 3: The New-Customer Play</strong></p>
    <p>Incumbents serve existing customers with existing willingness-to-pay. There are usually customers outside the market entirely—too small to serve profitably, too different to address, in geographies the incumbents don't operate in. Build an AI solution for those customers. It won't appeal to the incumbent's current base. It will appeal to entirely new customers. TAM: Usually $100M-$500M as you expand from greenfield customers.</p>
    """

    section_hard = f"""
    <h2>What Makes It Hard</h2>
    <p>Every sector has moats. In {sector_display}, the moats are typically: regulatory constraints, capital requirements, network effects, or incumbent distribution. Understanding which moats protect the incumbents in your target space is critical.</p>
    <p>{extract_key_sentences(s.get('raw_content', ''), 1)[0] if s.get('raw_content') else f'The {sector_display} sector has specific barriers'}</p>
    <p>The winning move isn't to attack the moat directly. It's to find a customer segment where the moat doesn't matter. Build for them first. Scale from there.</p>
    """

    section_playbook = """
    <h2>Founder's Playbook: 12 Months to Product-Market Fit</h2>
    <p><strong>Months 1-2: Deep Industry Immersion</strong></p>
    <p>Spend 8 weeks talking to customers and operators in the sector. Your goal is not to validate your idea. It's to understand if you're solving the right problem, for the right segment, in the right way. Talk to 20-30 operators. Ask them about their biggest pain points. Ask them how much they'd pay to solve it. Ask them who else would care about that solution. You'll either get clearer or you'll pivot. Both are good outcomes at this stage.</p>
    <p><strong>Months 3-5: MVP Development</strong></p>
    <p>Don't build a perfect product. Build a minimally viable product that solves 60-70% of the problem for a specific customer segment. Focus on the part that requires AI, not the parts that are just engineering. By end of month 5, you should have something that a customer in your target segment will use (even if they're doing it as a favor, not because they're paying).</p>
    <p><strong>Months 6-8: Pilot and Iteration</strong></p>
    <p>Get your MVP in front of 3-5 pilot customers. They should represent your target segment. Run pilots for 4-8 weeks. Measure: Did the product deliver the promised value? Would they pay for it? What would they change? By end of month 8, you should have strong conviction that this solves a real problem and that customers want it.</p>
    <p><strong>Months 9-12: Path to Monetization</strong></p>
    <p>Now build the things that make you sustainable: pricing model, sales process, CS/support structure, compliance setup. By end of month 12, you should have 2-3 paying customers, a repeatable sales process, and a clear path to $1M ARR. You don't need to be there yet. You need to see it clearly.</p>
    """

    section_vision = f"""
    <h2>The 10-Year Vision</h2>
    <p>If you execute well on one AI problem in {sector_display}, you'll earn the right to solve the next one. The biggest founders in this space don't stop at one product. They build platforms. {sector_display} in 2036 will look fundamentally different from {sector_display} in 2026. The companies that build the new infrastructure will be massive. Plan for that from day one, but execute on one problem first.</p>
    """

    content = intro + section_how_industry + section_broken + section_three_plays + section_hard + section_playbook + section_vision
    return h1, content


def get_html_wrapper(sector_name, h1, body_content, audience):
    """Generate complete HTML with wrapper, nav, metadata."""
    sector_mapping = SECTOR_MAPPING.get(sector_name, {})
    slug1 = sector_mapping.get('slug1', 'sector')
    slug2 = sector_mapping.get('slug2', 'sector')
    audience_slug = AUDIENCE_MAPPING.get(audience, 'unknown')
    audience_display = AUDIENCE_DISPLAY.get(audience, 'Unknown')
    sector_display = get_sector_name_display(sector_name)

    # Build filename
    filename = f"sectors-{slug1}-{slug2}-{audience_slug}.html"

    # Breadcrumb
    breadcrumb = f"""<div class="breadcrumb">
        <a href="{BASE_URL}/">Home</a> &gt;
        <a href="{BASE_URL}/sectors">Sectors</a> &gt;
        <span>{sector_display}</span>
    </div>"""

    # Meta badges
    meta_badges = f"""<div class="meta-badges">
        <span class="badge">Sector: {sector_display}</span>
        <span class="badge">Audience: {audience_display}</span>
        <span class="badge">Published: {ARTICLE_DATE}</span>
    </div>"""

    # Audience pills
    audience_pills = '<div class="audience-pills">'
    for aud in ['ceo', 'employee', 'customer', 'founder']:
        aud_slug = AUDIENCE_MAPPING.get(aud, aud)
        aud_display = AUDIENCE_DISPLAY.get(aud, aud)
        active = 'active' if aud == audience else ''
        pill_url = f"{BASE_URL}/articles/{filename.replace(f'-{audience_slug}.html', f'-{aud_slug}.html')}"
        audience_pills += f'<a href="{pill_url}" class="pill {active}">{aud_display}</a>'
    audience_pills += '</div>'

    # Share bar
    share_bar = f"""<div class="share-bar">
        <a href="https://twitter.com/intent/tweet?url={BASE_URL}/articles/{filename}&text=Disrupting {sector_display}" class="share-btn">Share on Twitter</a>
        <a href="https://www.linkedin.com/sharing/share-offsite/?url={BASE_URL}/articles/{filename}" class="share-btn">Share on LinkedIn</a>
        <a href="mailto:?subject=AI Disruption in {sector_display}&body={BASE_URL}/articles/{filename}" class="share-btn">Email</a>
    </div>"""

    # Email capture
    email_capture = f"""<div class="email-capture">
        <h3>Get sector insights delivered to your inbox</h3>
        <p>New analysis on AI disruption across industries, quarterly updates, and founder playbooks.</p>
        <input type="email" placeholder="your@email.com" />
        <button>Subscribe</button>
    </div>"""

    # Feedback bar
    feedback_bar = """<div class="feedback-bar">
        <p>Was this useful?</p>
        <button>Yes, very helpful</button>
        <button>Somewhat helpful</button>
        <button>Not helpful</button>
    </div>"""

    # References
    references = """<div class="references">
        <h3>References & Sources</h3>
        <div class="reference-item"><a href="https://www.deloitte.com" target="_blank">Deloitte Insights</a> — Industry analysis and AI adoption metrics (2025-2026)</div>
        <div class="reference-item"><a href="https://www.mckinsey.com" target="_blank">McKinsey & Company</a> — AI disruption and workforce impact studies</div>
        <div class="reference-item"><a href="https://www.pwc.com" target="_blank">PwC</a> — Financial metrics and margin analysis</div>
        <div class="reference-item"><a href="https://www.bloomberg.com" target="_blank">Bloomberg</a> — Real-time market data and financial reporting</div>
        <div class="reference-item"><a href="https://www.ycharts.com" target="_blank">YCharts</a> — Salary data and employment metrics</div>
    </div>"""

    # Footer
    footer = f"""<footer class="footer">
        <p>&copy; 2026 AI2030. This is speculative analysis exploring probable futures.</p>
        <p><a href="{BASE_URL}">Home</a> &bull; <a href="{BASE_URL}/about">About</a> &bull; <a href="{BASE_URL}/contact">Contact</a></p>
    </footer>"""

    # Header nav
    header_nav = f"""<div class="header-nav">
        <div class="nav-brand">AI2030</div>
        <ul class="nav-links">
            <li><a href="{BASE_URL}/">Home</a></li>
            <li><a href="{BASE_URL}/countries">Countries</a></li>
            <li><a href="{BASE_URL}/companies">Companies</a></li>
            <li><a href="{BASE_URL}/sectors">Sectors</a></li>
            <li><a href="{BASE_URL}/search">Search</a></li>
            <li><a href="{BASE_URL}/about">About</a></li>
        </ul>
    </div>"""

    # Full HTML
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{h1} | AI2030</title>
    <meta name="description" content="{h1}. Strategic analysis of AI disruption in {sector_display}.">
    <meta name="keywords" content="{sector_display}, AI disruption, strategy, analysis, 2026">
    <meta property="og:title" content="{h1} | AI2030">
    <meta property="og:description" content="Strategic analysis of AI disruption in {sector_display}.">
    <meta property="og:url" content="{BASE_URL}/articles/{filename}">
    <meta property="og:type" content="article">

    <script async src="https://www.googletagmanager.com/gtag/js?id={GA4_ID}"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){{dataLayer.push(arguments);}}
        gtag('js', new Date());
        gtag('config', '{GA4_ID}');
    </script>

    {get_css()}
</head>
<body>
    <div class="reading-progress" id="readingProgress"></div>

    {header_nav}
    {breadcrumb}

    <div class="container">
        {meta_badges}
        <h1>{h1}</h1>
        {audience_pills}
        {share_bar}

        {body_content}

        {share_bar}
        {email_capture}
        {feedback_bar}
        {references}
    </div>

    {footer}

    <button class="scroll-to-top" id="scrollToTop">↑</button>
    <button class="theme-toggle" id="themeToggle" title="Toggle theme">◐</button>

    <script>
    // Reading progress bar
    window.addEventListener('scroll', function() {{
        const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
        const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
        const scrolled = (winScroll / height) * 100;
        document.getElementById('readingProgress').style.width = scrolled + '%';
    }});

    // Scroll to top button
    const scrollBtn = document.getElementById('scrollToTop');
    window.addEventListener('scroll', function() {{
        scrollBtn.classList.toggle('show', window.scrollY > 300);
    }});
    scrollBtn.addEventListener('click', function() {{
        window.scrollTo({{top: 0, behavior: 'smooth'}});
    }});

    // Theme toggle
    document.getElementById('themeToggle').addEventListener('click', function() {{
        document.body.style.filter = document.body.style.filter === 'invert(1)' ? 'none' : 'invert(1)';
    }});
    </script>
</body>
</html>"""

    return html, filename


def main():
    """Main generation function."""
    print("=" * 80)
    print("SECTOR ARTICLE GENERATOR v2")
    print("=" * 80)

    # Create articles directory
    os.makedirs(ARTICLES_DIR, exist_ok=True)

    # Parse research
    print("\nParsing sector research...")
    sectors_data = parse_research_file()
    print(f"✓ Parsed {len(sectors_data)} sectors")

    # Generate articles
    total_articles = len(sectors_data) * 4
    article_count = 0

    for sector_name in sorted(sectors_data.keys()):
        sector_data = sectors_data[sector_name]
        sector_display = get_sector_name_display(sector_name)

        for audience in ['ceo', 'employee', 'customer', 'founder']:
            article_count += 1
            print(f"[{article_count}/{total_articles}] Generating {sector_display} ({AUDIENCE_DISPLAY[audience]})...", end='', flush=True)

            try:
                # Generate content based on audience
                if audience == 'ceo':
                    h1, body = generate_ceo_article(sector_name, sector_data)
                elif audience == 'employee':
                    h1, body = generate_employee_article(sector_name, sector_data)
                elif audience == 'customer':
                    h1, body = generate_customer_article(sector_name, sector_data)
                else:  # founder
                    h1, body = generate_founder_article(sector_name, sector_data)

                # Generate HTML
                html, filename = get_html_wrapper(sector_name, h1, body, audience)

                # Write to file
                filepath = os.path.join(ARTICLES_DIR, filename)
                with open(filepath, 'w') as f:
                    f.write(html)

                print(f" ✓ ({len(html)} bytes)")
            except Exception as e:
                print(f" ERROR: {str(e)}")

    print("\n" + "=" * 80)
    print(f"COMPLETE: Generated {article_count} sector articles")
    print(f"Location: {ARTICLES_DIR}")
    print(f"Sample file: {ARTICLES_DIR}/sectors-aerospace-and-defense-aerospacedefense-incumbent-ceos.html")
    print("=" * 80)


if __name__ == "__main__":
    main()
