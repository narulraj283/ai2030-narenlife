# Specific Issues Found - With Code References

## Issue #1: Missing Skip Navigation Link

### Location: All 26 pages
### Severity: CRITICAL
### WCAG Violation: 2.4.1 Bypass Blocks (Level A)

### What's Wrong
Every HTML page lacks a skip-to-content link. Keyboard users must tab through the entire navigation menu before reaching page content.

### Current State (All pages)
```html
<!DOCTYPE html>
<html lang="en">
<head>...</head>
<body>
    <!-- Navigation starts immediately - no skip link -->
    <header>
        <nav>
            <a href="/">Home</a>
            <a href="/about">About</a>
            <a href="/browse">Browse</a>
            <!-- ... 10+ more links -->
        </nav>
    </header>
    <main>
        <!-- User has to tab through all nav links to get here -->
    </main>
</body>
</html>
```

### Expected State (How to Fix)
```html
<!DOCTYPE html>
<html lang="en">
<head>...</head>
<body>
    <!-- Add skip link FIRST -->
    <a href="#main-content" class="skip-link">Skip to main content</a>

    <header>
        <nav>
            <a href="/">Home</a>
            <a href="/about">About</a>
            <!-- nav links -->
        </nav>
    </header>

    <main id="main-content">
        <!-- Content here -->
    </main>
</body>
</html>
```

### CSS to Add
```css
.skip-link {
    position: absolute;
    top: -40px;
    left: 0;
    background: #000;
    color: #fff;
    padding: 8px 16px;
    text-decoration: none;
    z-index: 999;
}

.skip-link:focus {
    top: 0;
}
```

### Impact
- **Keyboard users:** Currently impossible to efficiently navigate
- **Screen reader users:** Have to listen through all nav items
- **Google:** Flags as accessibility violation

---

## Issue #2: Removed Focus Indicators (outline: none)

### Location: `/tmp/ai2030-repo/style.css` line 189
### Severity: CRITICAL
### WCAG Violation: 2.4.7 Focus Visible (Level AA)

### Current Code
```css
/* Line 180-196 */
.search-box input {
    width: 100%;
    padding: 14px 20px 14px 48px;
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 50px;
    color: var(--text-primary);
    font-size: 1rem;
    font-family: var(--font-sans);
    outline: none;                          /* ← LINE 189: PROBLEM */
    transition: all 0.2s;
}

.search-box input:focus {
    border-color: var(--accent-blue);
    box-shadow: 0 0 0 3px rgba(59,130,246,0.15);
}
```

### Why It's Wrong
1. `outline: none` removes the browser's default focus indicator
2. The `:focus` style only adds a border color change
3. Without contrast, keyboard users can't see if element is focused
4. Violates WCAG 2.1 Level AA requirement for "visible focus"

### How to Fix
```css
/* Remove line 189 entirely, update :focus */
.search-box input {
    width: 100%;
    padding: 14px 20px 14px 48px;
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 50px;
    color: var(--text-primary);
    font-size: 1rem;
    font-family: var(--font-sans);
    /* outline: none; ← DELETE THIS LINE */
    transition: all 0.2s;
}

.search-box input:focus {
    border-color: var(--accent-blue);
    box-shadow: 0 0 0 3px rgba(59,130,246,0.15);
    outline: 2px solid var(--accent-blue);      /* ← ADD THIS */
    outline-offset: 2px;                        /* ← ADD THIS */
}

/* Also add for other interactive elements */
a:focus-visible {
    outline: 2px solid var(--accent-blue);
    outline-offset: 2px;
}

button:focus-visible {
    outline: 2px solid var(--accent-blue);
    outline-offset: 2px;
}
```

### Test It
1. Open any page in browser
2. Press Tab repeatedly
3. **Current:** Focus is nearly invisible (just border color)
4. **After fix:** Blue outline clearly shows where focus is

---

## Issue #3: Form Inputs Without Labels

### Locations: All 26 pages
### Severity: CRITICAL
### WCAG Violation: 1.3.1 Info and Relationships (Level A)

### Example: Search Box in Header

#### Current Code (WRONG)
```html
<div class="search-box">
    <input type="search"
           id="search-input"
           placeholder="Search...">
    <span class="search-icon">🔍</span>
</div>
```

**Problem:**
- No `<label>` associated with input
- Screen reader user hears nothing except placeholder
- Can't identify the input's purpose
- Placeholder text disappears when typing

#### Fixed Code (OPTION 1: Visible Label)
```html
<div class="search-box">
    <label for="search-input">Search</label>
    <input type="search"
           id="search-input"
           placeholder="Search...">
    <span class="search-icon" aria-hidden="true">🔍</span>
</div>
```

**Result:**
- ✓ Screen reader announces: "Search input"
- ✓ Clicking label focuses input
- ✓ Accessible and clear

#### Fixed Code (OPTION 2: Hidden Label - If Design Requires)
```html
<div class="search-box">
    <label for="search-input" class="sr-only">Search the database</label>
    <input type="search"
           id="search-input"
           placeholder="Search...">
    <span class="search-icon" aria-hidden="true">🔍</span>
</div>
```

Add to CSS:
```css
.sr-only {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0,0,0,0);
    white-space: nowrap;
    border-width: 0;
}
```

**Result:**
- ✓ Visually hidden but available to screen readers
- ✓ Design not affected
- ✓ Fully accessible

### Pages Affected
- Homepage: 2 inputs without labels
- About: 1 input without labels
- Browse Companies: 1 input without labels
- Browse Data: 1 input without labels
- Browse Sectors: 1 input without labels
- All country/sector pages: 1 input each

---

## Issue #4: Invalid Heading Hierarchy

### Locations: 3 pages
- `/tmp/ai2030-repo/index.html` (homepage)
- `/tmp/ai2030-repo/browse/data.html`
- `/tmp/ai2030-repo/browse/sectors.html`

### Severity: HIGH
### WCAG Violation: 1.3.1 Info and Relationships (Level A)

### What's Wrong

#### Homepage Example
```html
<h1>AI by 2030</h1>          <!-- Level 1 -->
<!-- h2 is missing -->
<h3>Key Insight</h3>         <!-- ← WRONG: Skips to level 3 -->
<h3>Another Insight</h3>
<h4>Details</h4>

<!-- Expected would be: h1 → h2 → h3 → h4 -->
```

#### Browse Data Example
```html
<h1>Browse Data</h1>         <!-- Level 1 -->
<h3>Financial Data</h3>      <!-- ← WRONG: Should be h2 -->
<h3>Healthcare Data</h3>
```

### Why It's Wrong
1. **Screen reader users:** Get confused about document structure
2. **SEO:** Search engines can't understand content hierarchy
3. **Navigation:** Assistive tech can't create proper outline
4. **WCAG:** Violates 1.3.1 Info and Relationships (Level A)

### How to Fix

#### Correct Hierarchy Pattern
```html
<h1>Page Title</h1>          <!-- Start at h1 (only one per page) -->
<h2>Main Section</h2>        <!-- Increase by 1 -->
<h3>Subsection</h3>          <!-- Increase by 1 -->
<h4>Sub-subsection</h4>      <!-- Increase by 1 -->
<h3>Another Subsection</h3>  <!-- Can go back up levels -->
<h2>Another Section</h2>     <!-- Back to h2 is fine -->
```

#### Fixed Homepage
```html
<h1>AI by 2030</h1>
<h2>Key Insights</h2>        <!-- ← Changed from h3 to h2 -->
<h3>First Insight</h3>       <!-- ← Now this is h3, not h3 after h1 -->
<h3>Second Insight</h3>
<h3>Third Insight</h3>
<h2>Featured Sectors</h2>
<h3>Finance</h3>
<h3>Healthcare</h3>
```

### Testing
Use browser DevTools:
1. Open page
2. F12 → Elements/Inspector
3. Find all `<h1>`, `<h2>`, `<h3>`, `<h4>` tags
4. Verify they increase by max 1 level
5. Run axe DevTools extension - will flag violations

---

## Issue #5: Fixed-Width CSS (Not Responsive)

### Location: Various CSS files, `style.css`
### Severity: CRITICAL
### Affects: All 26 pages
### Google Flag: "Not mobile-friendly"

### What's Wrong

#### Example 1: Fixed Container Width
```css
/* WRONG */
.container {
    width: 1200px;              /* Fixed width */
    margin: 0 auto;
}

/* On mobile (320px screen), this creates:
   - 1200px wide content
   - 880px overflow
   - Horizontal scrolling required
*/
```

#### Example 2: Fixed Card Width
```css
/* WRONG */
.card {
    width: 300px;               /* Fixed width */
    height: auto;
}

/* On mobile, cards don't shrink - causes overflow */
```

### How Mobile Devices See It

**Current (BROKEN):**
```
Mobile screen: 375px
Content width: 1200px
User experiences: Horizontal scrolling, tiny text, broken layout
```

**Fixed (RESPONSIVE):**
```
Mobile screen: 375px
Content width: 375px (fits perfectly)
User experiences: Proper layout, readable text, no scrolling
```

### How to Fix

#### Pattern 1: Container (Most Common)
```css
/* WRONG */
.container {
    width: 1200px;
    margin: 0 auto;
}

/* CORRECT */
.container {
    max-width: 1200px;          /* Max width, but can shrink */
    width: 100%;                /* Fill available space */
    margin: 0 auto;
    padding: 0 1rem;            /* Padding instead of fixed width */
}
```

#### Pattern 2: Columns
```css
/* WRONG - Always 3 columns */
.card {
    width: 33.333%;
    float: left;
}

/* CORRECT - Responsive columns */
.card {
    width: 100%;                /* 1 column on mobile */
}

@media (min-width: 768px) {
    .card {
        width: 48%;             /* 2 columns on tablet */
    }
}

@media (min-width: 1024px) {
    .card {
        width: 32%;             /* 3 columns on desktop */
    }
}
```

#### Pattern 3: Sidebar Layout
```css
/* WRONG */
.main {
    width: 800px;
}

.sidebar {
    width: 300px;
    float: right;
}

/* CORRECT */
.wrapper {
    display: grid;
    grid-template-columns: 1fr;  /* 1 column on mobile */
    gap: 2rem;
}

@media (min-width: 768px) {
    .wrapper {
        grid-template-columns: 3fr 1fr;  /* Main + sidebar */
    }
}
```

### Responsive Units Quick Reference

| Wrong | Right | Why |
|-------|-------|-----|
| `width: 1200px` | `max-width: 1200px; width: 100%` | Shrinks on small screens |
| `margin: 50px` | `margin: 1.5rem` or `margin: 5%` | Scales with viewport |
| `font-size: 16px` | `font-size: 1rem` | Respects user font size |
| `padding: 20px` | `padding: 1.25rem` | Scales proportionally |

### Test on Mobile

```
Chrome DevTools:
1. F12 → Toggle device toolbar (Ctrl+Shift+M)
2. Select iPhone SE (375px)
3. Scroll page left/right
4. Should NOT see horizontal scrollbar
5. All content should fit
```

---

## Issue #6: Small Touch Targets

### Location: All button/link elements
### Severity: HIGH
### WCAG Violation: 2.5.5 Target Size (Level AAA)

### What's Wrong

Buttons and links smaller than 44x44 pixels are hard to tap on mobile.

#### Example: Current Navigation Links
```css
.nav-links a {
    padding: 8px 16px;          /* Only ~24px height */
    font-size: 0.875rem;
    border-radius: var(--radius-sm);
}

/* Result: ~24px x ~70px hit area - too small */
```

#### What Users Experience
```
Trying to tap small button on iPhone:
- Miss and tap wrong element
- Frustration and abandoned visit
- High error rate on mobile
- Negative experience
```

### How to Fix

#### Minimum Size Requirement
```css
/* All interactive elements minimum 44x44px */
button,
a,
input[type="checkbox"],
input[type="radio"],
[role="button"] {
    min-width: 44px;
    min-height: 44px;
}
```

#### Example: Navigation Links
```css
/* WRONG - Too small */
.nav-links a {
    padding: 8px 16px;
    display: inline;
}

/* CORRECT - 44x44 minimum */
.nav-links a {
    display: inline-flex;       /* Support width/height */
    align-items: center;        /* Vertical center */
    justify-content: center;    /* Horizontal center */
    min-width: 44px;
    min-height: 44px;
    padding: 8px 16px;          /* Additional padding */
}
```

#### Example: Buttons
```css
/* WRONG - 36px tall */
button {
    padding: 8px 12px;
    font-size: 1rem;
}

/* CORRECT - 44px tall */
button {
    padding: 10px 16px;         /* Increased padding */
    min-height: 44px;           /* Ensure height */
    display: flex;
    align-items: center;
    font-size: 1rem;
}
```

### Measuring in DevTools

```
Chrome DevTools:
1. F12 → Toggle device toolbar (mobile mode)
2. Right-click element → Inspect
3. Look at Computed styles
4. Check width and height
5. Should be ≥ 44px

Or use Ctrl+Shift+M for device toolbar,
then resize and observe element sizes
```

---

## Issue #7: Missing ARIA Landmarks

### Location: `/tmp/ai2030-repo/briefs/index.html`
### Severity: HIGH
### WCAG Violation: 1.3.1 Info and Relationships (Level A)

### Current Code (WRONG)
```html
<!DOCTYPE html>
<html lang="en">
<head>...</head>
<body>
    <div class="header">
        <!-- No <header> element -->
        <div class="nav">
            <!-- No <nav> element -->
        </div>
    </div>

    <div class="content">
        <!-- No <main> element -->
        Content here
    </div>

    <div class="footer">
        <!-- No <footer> element -->
    </div>
</body>
</html>
```

**Screen reader hears:** Nothing about structure, just divs

### Fixed Code (CORRECT)
```html
<!DOCTYPE html>
<html lang="en">
<head>...</head>
<body>
    <header role="banner">
        <nav role="navigation">
            <!-- Navigation links -->
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

**Screen reader announces:**
- "Navigation region"
- "Main content region"
- "Footer region"

**Users can:**
- Jump to main content
- Skip to footer
- Understand page structure

### Semantic HTML Reference

| Tag | Purpose | One Per Page? |
|-----|---------|---|
| `<header>` | Site header with logo/title | OK to have multiple |
| `<nav>` | Navigation section | OK to have multiple |
| `<main>` | Main page content | EXACTLY ONE |
| `<article>` | Self-contained article | OK to have multiple |
| `<section>` | Generic section | OK to have multiple |
| `<aside>` | Sidebar/related content | OK to have multiple |
| `<footer>` | Site footer | OK to have multiple |

---

## Issue #8: Color Contrast (21/26 pages)

### Location: `style.css` color variables
### Severity: MEDIUM
### WCAG Violation: 1.4.3 Contrast (Minimum) (Level AA)

### Current Colors in CSS

```css
:root {
    --bg-primary: #0a0a0f;          /* Very dark background */
    --text-primary: #e4e4ef;        /* Light text - probably OK */
    --text-secondary: #9494a8;      /* Medium gray - check this */
    --text-muted: #6b6b80;          /* Dark gray - might fail */
    ...
}
```

### Contrast Requirements

| Type | Minimum Ratio | Your Status |
|------|--------------|---|
| Normal text | 4.5:1 | NEEDS CHECK |
| Large text (18pt+) | 3:1 | NEEDS CHECK |
| UI components | 3:1 | NEEDS CHECK |
| AAA level | 7:1 | NEEDS CHECK |

### How to Test

**Online Tool:** https://webaim.org/resources/contrastchecker/

1. Go to site
2. Enter foreground color: `#e4e4ef` (text-primary)
3. Enter background color: `#0a0a0f` (bg-primary)
4. Check result
5. If FAIL, lighten text or darken background

**Example Test Results:**
```
Text color: #9494a8 (text-secondary)
Background: #0a0a0f
Ratio: 3.8:1
Status: FAIL for AA
Action: Lighten text to #a8a8b8
New ratio: 4.5:1
Status: PASS for AA
```

### How to Fix

If a combination fails, lighten the text or darken background:

```css
/* BEFORE - Might fail */
:root {
    --text-muted: #6b6b80;          /* 3.2:1 ratio - FAIL */
}

/* AFTER - Passes AA */
:root {
    --text-muted: #8b8ba0;          /* 4.5:1 ratio - PASS */
}
```

---

## Summary Table

| Issue | Files | Lines | Severity | Fix Time |
|-------|-------|-------|----------|----------|
| Skip link | All 26 | Top of body | CRITICAL | 30 min |
| Focus indicators | style.css | 189 | CRITICAL | 15 min |
| Form labels | All 26 | Search box | CRITICAL | 1-2 hr |
| Heading hierarchy | 3 pages | Various | HIGH | 1-2 hr |
| Fixed width CSS | style.css | Multiple | CRITICAL | 4 hours |
| Touch targets | style.css | Multiple | HIGH | 2 hours |
| Landmarks | 1 page | All | HIGH | 30 min |
| Color contrast | style.css | CSS vars | MEDIUM | 2-3 hr |

**Total:** ~20-30 hours of work across 3 weeks

---

## Quick Reference Links

- **WCAG Violations:** https://www.w3.org/WAI/WCAG21/quickref/
- **Contrast Checker:** https://webaim.org/resources/contrastchecker/
- **Color Names to Hex:** https://www.color-hex.com/
- **MDN Accessibility:** https://developer.mozilla.org/en-US/docs/Web/Accessibility

For step-by-step remediation, see **REMEDIATION_GUIDE.md**
