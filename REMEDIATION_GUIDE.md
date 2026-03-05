# Accessibility Remediation Guide

## Fix #1: Add Skip Navigation Link (CRITICAL)

**Effort:** 30 minutes | **Impact:** HIGH (WCAG A compliance)

### Problem
All 26 pages lack a "skip to content" link, forcing keyboard users to tab through the entire navigation.

### Solution
Add this HTML at the very top of the `<body>` in every page template:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <title>...</title>
    <!-- other head content -->
</head>
<body>
    <!-- Add this as first element in body -->
    <a href="#main-content" class="skip-link">Skip to main content</a>

    <!-- Rest of page content -->
    <header role="banner">
        <nav role="navigation">
            <!-- navigation links -->
        </nav>
    </header>

    <main id="main-content">
        <!-- Page content -->
    </main>

    <footer role="contentinfo">
        <!-- Footer content -->
    </footer>
</body>
</html>
```

### CSS to Add to `style.css`

```css
/* Skip Navigation Link */
.skip-link {
    position: absolute;
    top: -40px;
    left: 0;
    background: #000;
    color: #fff;
    padding: 8px 16px;
    text-decoration: none;
    border-radius: 0 0 4px 0;
    z-index: 999;
    font-weight: 500;
}

.skip-link:focus {
    top: 0;
    outline: 2px solid #3b82f6;
    outline-offset: 2px;
}
```

### Testing
- Load any page and press Tab immediately
- You should see a "Skip to main content" link appear at top-left
- Press Enter to jump to main content
- All pages should have this behavior

### Files to Update
- Any HTML file or template that generates pages
- Include in base template/layout file if using template system

---

## Fix #2: Fix Focus Indicators (CRITICAL)

**Effort:** 15 minutes | **Impact:** HIGH (WCAG AA compliance, keyboard navigation)

### Problem
Current CSS at line 189 of `style.css`:
```css
.search-box input {
    outline: none;  /* ← REMOVES focus indicator */
}
```

This breaks keyboard navigation for anyone using assistive technology.

### Current Code
**File:** `/tmp/ai2030-repo/style.css` lines 180-196

```css
.search-box input {
    width: 100%;
    padding: 14px 20px 14px 48px;
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 50px;
    color: var(--text-primary);
    font-size: 1rem;
    font-family: var(--font-sans);
    outline: none;              /* ← REMOVE THIS LINE */
    transition: all 0.2s;
}

.search-box input:focus {
    border-color: var(--accent-blue);
    box-shadow: 0 0 0 3px rgba(59,130,246,0.15);
}
```

### Fixed Code

```css
.search-box input {
    width: 100%;
    padding: 14px 20px 14px 48px;
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 50px;
    color: var(--text-primary);
    font-size: 1rem;
    font-family: var(--font-sans);
    /* outline: none; ← DELETED */
    transition: all 0.2s;
}

.search-box input:focus {
    border-color: var(--accent-blue);
    box-shadow: 0 0 0 3px rgba(59,130,246,0.15);
    outline: 2px solid var(--accent-blue);
    outline-offset: 2px;
}

/* Also add focus styles for links and buttons */
a:focus-visible {
    outline: 2px solid var(--accent-blue);
    outline-offset: 2px;
}

button:focus-visible {
    outline: 2px solid var(--accent-blue);
    outline-offset: 2px;
}
```

### Implementation Steps

1. Open `/tmp/ai2030-repo/style.css`
2. Find line 189 with `outline: none;`
3. Delete that line entirely
4. Update `.search-box input:focus` to include outline (see above)
5. Add focus styles for `a:focus-visible` and `button:focus-visible`

### Testing
- Load any page
- Press Tab to navigate through links/buttons
- Each focused element should have a visible 2px blue outline
- Outline should be visible on all interactive elements

---

## Fix #3: Add Form Labels (CRITICAL)

**Effort:** 1-2 hours | **Impact:** MEDIUM (WCAG A compliance, accessibility)

### Problem
Search inputs lack associated `<label>` elements. Current code structure:

```html
<!-- WRONG - No label -->
<div class="search-box">
    <input type="search" id="search-input" placeholder="Search...">
    <span class="search-icon">🔍</span>
</div>
```

### Fixed Code

Option A: Visible label (recommended for clarity)
```html
<div class="search-box">
    <label for="search-input" class="search-label">Search</label>
    <input type="search" id="search-input" placeholder="Search...">
    <span class="search-icon" aria-hidden="true">🔍</span>
</div>
```

Option B: Hidden label (if you want to maintain design)
```html
<div class="search-box">
    <label for="search-input" class="sr-only">Search</label>
    <input type="search" id="search-input" placeholder="Search...">
    <span class="search-icon" aria-hidden="true">🔍</span>
</div>
```

### CSS for Hidden Label
Add to `style.css`:
```css
/* Screen reader only text */
.sr-only {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border-width: 0;
}
```

### Files to Update
- Template containing search box
- Every page with search input
- Check: `index.html`, `browse/companies.html`, `browse/sectors.html`, etc.

### Testing
1. Use browser DevTools Inspector
2. Search for any `<input>` element
3. Verify there's an associated `<label for="input-id">`
4. Test with screen reader (NVDA on Windows, VoiceOver on Mac)

---

## Fix #4: Fix Heading Hierarchy (HIGH)

**Effort:** 1-2 hours | **Impact:** MEDIUM (WCAG A compliance, SEO)

### Problem
Current hierarchy skips levels:
```html
<h1>AI by 2030</h1>
<!-- h2 missing -->
<h3>Feature Section</h3>  <!-- ← Skipped h2! -->
```

Affects pages:
- Homepage
- Browse Data
- Browse Sectors

### Correct Hierarchy

```html
<h1>AI by 2030</h1>
<h2>Main Section</h2>
<h3>Subsection</h3>
<h4>Sub-subsection</h4>
```

### Rule
- Start with h1 (exactly one per page)
- Only increase by 1 level: h1→h2, h2→h3, h3→h4, etc.
- Never skip: h1→h3 is invalid
- OK to decrease multiple levels: h3→h1

### Implementation
1. Open the problematic page in browser DevTools
2. Find all `<h1>`, `<h2>`, `<h3>` tags
3. Identify skipped levels
4. Update HTML to fix hierarchy
5. Test with axe DevTools extension

Example fix:
```html
<!-- BEFORE (WRONG) -->
<h1>Title</h1>
<h3>Subsection</h3>
<h4>Detail</h4>

<!-- AFTER (CORRECT) -->
<h1>Title</h1>
<h2>Main Section</h2>
<h3>Subsection</h3>
<h4>Detail</h4>
```

### Files to Check/Update
- `/tmp/ai2030-repo/index.html` (skips h1→h3)
- `/tmp/ai2030-repo/browse/data.html`
- `/tmp/ai2030-repo/browse/sectors.html`

---

## Fix #5: Remove Fixed-Width CSS (CRITICAL)

**Effort:** 3-4 hours | **Impact:** CRITICAL (Google Mobile Friendly, Core Web Vitals)

### Problem
Fixed-width CSS makes pages non-responsive:
```css
/* WRONG - Fixed width */
.container {
    width: 1200px;  /* ← Not responsive */
    margin: 0 auto;
}

.card {
    width: 300px;   /* ← Fixed, can't shrink on mobile */
}
```

### Audit Results
All 26 pages fail mobile responsiveness check.

### Solution: Use Responsive Units

```css
/* CORRECT - Responsive */
.container {
    max-width: 1200px;  /* Max width, but can shrink */
    width: 100%;        /* Full width of parent */
    margin: 0 auto;
    padding: 0 1rem;    /* Horizontal padding */
}

.card {
    width: 100%;        /* Full width on mobile */
}

@media (min-width: 768px) {
    .card {
        width: 48%;     /* 2 columns on tablet */
    }
}

@media (min-width: 1024px) {
    .card {
        width: 32%;     /* 3 columns on desktop */
    }
}
```

### CSS Patterns to Replace

| Current (Wrong) | Replace With |
|---|---|
| `width: 300px` | `max-width: 300px; width: 100%` |
| `width: 1200px` | `max-width: 1200px; width: 100%` |
| `height: 500px` | `min-height: 500px` (only when necessary) |

### Implementation
1. Open `/tmp/ai2030-repo/style.css`
2. Search for all instances of `width: XXXpx`
3. Replace with responsive equivalents
4. Test at breakpoints: 320px, 768px, 1024px
5. Use browser DevTools device emulator

### Testing
- Open DevTools (F12)
- Click device toggle (mobile icon)
- Select iPhone SE (375px)
- Scroll and verify no horizontal scroll bars
- Test on tablet (768px) and desktop (1024px+)

---

## Fix #6: Increase Touch Target Sizes (HIGH)

**Effort:** 2-3 hours | **Impact:** HIGH (Mobile usability, WCAG AAA)

### Problem
Buttons and links may be smaller than 44x44px (WCAG 2.5.5 minimum).

### Correct Sizes
```css
/* Minimum touch target */
button, a, input[type="checkbox"], input[type="radio"] {
    min-width: 44px;
    min-height: 44px;
}

/* Add padding to meet minimum */
button {
    padding: 10px 16px;     /* Minimum 44px height */
    min-height: 44px;
}

a {
    display: inline-block;  /* Required for width/height */
    min-width: 44px;
    min-height: 44px;
    line-height: 44px;      /* Vertical centering */
}

.nav-links a {
    min-height: 44px;
    padding: 12px 16px;     /* Increases hit area */
    display: flex;
    align-items: center;
}
```

### Implementation Steps
1. Measure all interactive elements in DevTools
2. Elements smaller than 44x44px need increased padding/margins
3. Use flexbox to center content within touch target
4. Test on actual mobile device if possible

### Files to Update
- `/tmp/ai2030-repo/style.css` - button, link, input styles

---

## Fix #7: Add Missing Landmarks (for briefs page)

**Effort:** 30 minutes | **Impact:** MEDIUM (WCAG A compliance)

### Problem
**File:** `/tmp/ai2030-repo/briefs/index.html`

Missing semantic landmarks: `<nav>` and `<main>`

### Current (Wrong)
```html
<body>
    <header>
        <!-- nav links not in <nav> element -->
    </header>
    <div class="content">
        <!-- no <main> element -->
    </div>
</body>
```

### Fixed Version
```html
<body>
    <header role="banner">
        <nav role="navigation">
            <!-- navigation links -->
        </nav>
    </header>

    <main id="main-content">
        <!-- page content -->
    </main>

    <footer role="contentinfo">
        <!-- footer content -->
    </footer>
</body>
```

### Explanation
- `<header>` → wraps site header with logo/title
- `<nav>` → wraps navigation links (can have multiple on page)
- `<main>` → wraps main page content (only one per page, must have id="main-content")
- `<footer>` → wraps footer content

---

## Fix #8: Verify Color Contrast (IMPORTANT)

**Effort:** 2-3 hours | **Impact:** MEDIUM (WCAG AA compliance)

### Problem
21 pages have potential color contrast issues.

### Contrast Requirements
- Normal text (< 18px): **4.5:1** ratio minimum
- Large text (≥ 18px or ≥ 14px bold): **3:1** ratio minimum
- UI components: **3:1** ratio minimum

### Check Your Colors
Use WebAIM Contrast Checker: https://webaim.org/resources/contrastchecker/

Current colors in `/tmp/ai2030-repo/style.css`:
```css
--bg-primary: #0a0a0f;          /* Dark background */
--text-primary: #e4e4ef;        /* Light text */
--text-secondary: #9494a8;      /* Medium text */
--text-muted: #6b6b80;          /* Muted text */
```

**Testing combinations:**
- Text Primary (#e4e4ef) on BG Primary (#0a0a0f) → Test this!
- Text Secondary (#9494a8) on BG Primary (#0a0a0f) → Test this!
- Text Muted (#6b6b80) on BG Primary (#0a0a0f) → May fail!

### Steps
1. Go to https://webaim.org/resources/contrastchecker/
2. Enter each text color and background color
3. Check result - should show PASS for AAA level
4. If FAIL, darken text color or lighten background
5. Example fix:
   ```css
   /* If FAIL: lighten the text */
   --text-muted: #8b8ba0;  /* Lighter muted color */
   ```

### Automation
You can also test in Chrome DevTools:
1. F12 → Elements
2. Select an element with text
3. Inspect color indicator
4. DevTools shows contrast ratio

---

## Implementation Checklist

### Priority 1 (Start Here - 1 week)
- [ ] Add skip navigation link to all pages
- [ ] Remove `outline: none` from CSS
- [ ] Add focus-visible styles
- [ ] Add labels to form inputs
- [ ] Fix heading hierarchy on homepage, browse pages

### Priority 2 (Week 2)
- [ ] Remove all fixed-width CSS
- [ ] Make layouts fully responsive
- [ ] Increase touch target sizes
- [ ] Add landmarks to briefs page
- [ ] Test mobile responsiveness

### Priority 3 (Week 3-4)
- [ ] Verify color contrast on all pages
- [ ] Test with screen readers
- [ ] Test keyboard navigation throughout
- [ ] Run automated audit tools
- [ ] Deploy and monitor GSC

### Testing Tools to Use
```bash
# Automated accessibility testing
npm install -g axe-core
npm install -g pa11y

# Run lighthouse audit
lighthouse https://yourdomain.com --view

# Chrome DevTools (F12 > Lighthouse tab)
# Firefox Accessibility Inspector (F12 > Inspector > Accessibility tab)
```

### Verification Checklist
- [ ] All focus indicators visible when tabbing
- [ ] Skip link appears and works
- [ ] All form inputs have labels
- [ ] No heading hierarchy skips
- [ ] All text has sufficient contrast (4.5:1)
- [ ] All buttons 44x44px or larger
- [ ] Page responsive at 320px, 768px, 1024px
- [ ] Keyboard navigation works throughout
- [ ] Screen reader announces landmarks properly
- [ ] Google Lighthouse score 90+

---

## Quick Reference: WCAG 2.1 Violations Found

| Issue | WCAG Level | Your Status | Fix Time |
|-------|-----------|-----------|----------|
| No skip link | A | All pages | 30 min |
| No focus indicators | AA | 20/26 | 15 min |
| Missing form labels | A | 20/26 | 1-2 hr |
| Invalid heading hierarchy | A | 3/26 | 1-2 hr |
| Fixed-width layout | A | All pages | 3-4 hr |
| Small touch targets | AAA | All pages | 2-3 hr |
| Missing landmarks | A | 1/26 | 30 min |
| Color contrast | AA | 21/26 | 2-3 hr |
| **Total Effort** | | | **14-17 hours** |

---

## Additional Resources

### Learning
- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [MDN Accessibility](https://developer.mozilla.org/en-US/docs/Web/Accessibility)
- [WebAIM Articles](https://webaim.org/)

### Tools
- [axe DevTools](https://www.deque.com/axe/devtools/) - Chrome/Firefox extension
- [Lighthouse](https://developers.google.com/web/tools/lighthouse) - Chrome DevTools
- [WAVE](https://wave.webaim.org/) - Web accessibility evaluator
- [Color Contrast Analyzer](https://www.tpgi.com/color-contrast-checker/)

### Testing
- [NVDA Screen Reader](https://www.nvaccess.org/) - Windows free option
- [macOS VoiceOver](https://www.apple.com/accessibility/voiceover/) - Built-in
- [JAWS Screen Reader](https://www.freedomscientific.com/products/software/jaws/) - Premium option

### Validation
- [HTML Validator](https://validator.w3.org/)
- [CSS Validator](https://jigsaw.w3.org/css-validator/)
- [Mobile-Friendly Test](https://search.google.com/test/mobile-friendly)
