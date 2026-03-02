# Deployment Guide: The 2030 Intelligence Report

## Domain Recommendation

**Buy this domain on GoDaddy:** `the2030report.com`

Alternative options if taken:
- `2030intelligencereport.com`
- `the2030crisis.com`
- `ai2030report.com`

---

## Step 1: Create GitHub Repository

1. Go to https://github.com/new
2. Name the repo: `the-2030-report`
3. Set to **Public** (required for free GitHub Pages)
4. Do NOT initialize with README (you already have files)
5. Click **Create repository**

## Step 2: Push Site Files to GitHub

Open Terminal on your computer and run:

```bash
# Navigate to the site folder (the 2030-predictions-site folder)
cd /path/to/2030-predictions-site

# Initialize git
git init
git checkout -b main

# Add all files
git add -A

# Commit
git commit -m "Initial site: 737 articles, interactive dashboard"

# Add your GitHub repo as remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/the-2030-report.git

# Push
git push -u origin main
```

## Step 3: Enable GitHub Pages

1. Go to your repo on GitHub: `https://github.com/YOUR_USERNAME/the-2030-report`
2. Click **Settings** (top tab)
3. Click **Pages** (left sidebar)
4. Under **Source**, select **Deploy from a branch**
5. Select **main** branch and **/ (root)** folder
6. Click **Save**
7. Wait 2-3 minutes. Your site will be live at: `https://YOUR_USERNAME.github.io/the-2030-report/`

## Step 4: Buy Domain on GoDaddy

1. Go to https://www.godaddy.com
2. Search for `the2030report.com`
3. Purchase the domain
4. Skip all upsells (SSL, email, etc. — not needed with GitHub Pages)

## Step 5: Configure GoDaddy DNS for GitHub Pages

1. Go to GoDaddy → **My Products** → Find your domain → **DNS**
2. Remove any existing A records pointing to parking pages
3. Add these **4 A records** (Host: `@`, Type: `A`):
   - `185.199.108.153`
   - `185.199.109.153`
   - `185.199.110.153`
   - `185.199.111.153`
4. Add a **CNAME record**:
   - Host: `www`
   - Points to: `YOUR_USERNAME.github.io`
   - TTL: 1 hour

## Step 6: Connect Custom Domain in GitHub

1. Go to repo **Settings** → **Pages**
2. Under **Custom domain**, enter: `the2030report.com`
3. Click **Save**
4. Wait for DNS check to pass (can take up to 24 hours, usually 30 mins)
5. Check **Enforce HTTPS** once the DNS is verified

## Step 7: Verify

Visit `https://the2030report.com` — your site should be live!

---

## Site Structure

```
2030-predictions-site/
├── index.html          # Main dashboard (interactive search & filters)
├── style.css           # Shared stylesheet
├── about.html          # About page
├── 404.html            # Custom 404 page
├── sitemap.xml         # SEO sitemap (743 URLs)
├── robots.txt          # Search engine directives
├── CNAME               # Custom domain config
├── .nojekyll           # Bypass Jekyll processing
├── browse/
│   ├── countries.html  # Browse all 34 countries
│   ├── companies.html  # Browse all 142 companies
│   ├── sectors.html    # Browse all 20 sectors
│   └── industries.html # Browse all 6 industries
└── articles/
    └── (737 individual article pages)
```

## SEO Features Included

- Meta description on every page
- Open Graph tags (Facebook/LinkedIn sharing)
- Twitter card tags
- JSON-LD structured data on article pages
- XML sitemap with all 743 URLs
- Canonical URLs on every page
- Semantic HTML structure
- Mobile-responsive design
- Fast loading (static HTML, shared CSS)

## After Deployment: Submit to Search Engines

1. **Google Search Console**: https://search.google.com/search-console
   - Add property → Enter `the2030report.com`
   - Verify via DNS (add TXT record GoDaddy provides)
   - Submit sitemap: `https://the2030report.com/sitemap.xml`

2. **Bing Webmaster Tools**: https://www.bing.com/webmasters
   - Add site and submit sitemap
