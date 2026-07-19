# Ninja Luxe Cafe — Planning Session

## 1. Accuracy Audit — Machine Spec Corrections Needed

### Confirmed Errors (need fixing)

| Issue | Current | Correction | Severity |
|-------|---------|-----------|----------|
| **Cold-Pressed Espresso brew time** | "~30 sec" | **~2.5 minutes** — real extraction is much longer | High |
| **Cleaning cycle frequency** | "Monthly" | When the machine's **CLEAN light** appears — intelligent, not calendar-based | Medium |
| **Luxe basket capacity** | "18-20g" | Actual capacity is **~40g** (39-41g reported) — the 18-20g is for the *Double* basket | High |
| **Quad shot description** | "pulls two double shots back-to-back" | It's a single **40g continuous extraction** using the Luxe basket | Medium |
| **5 recipes with duplicated/contradictory steps** | Breve Latte, Eggnog Latte, Hot Chocolate, Vanilla Steamer, Low-Cal Cold Brew | Steps have redundant or conflicting instructions | Medium |

### Ambiguous Items (review needed)

| Claim | Issue |
|-------|-------|
| **ES601 vs ES701 features** | Guide conflates both models — ES701 Pro has hot water spout, ES601 doesn't (already removed) |
| **Single espresso recipe** | Says "Use the Double basket (10-12g)" but also mentions 18-20g — contradictory for a single shot |
| **Source URLs** | Many link to generic Ninja product pages or coffee blogs, not the specific recipe source |
| **Preheat instructions** | Only a few recipes mention preheating cups — should be consistent across espresso drinks |
| **Brew ratio mention** | "~1:2 ratio" mentioned in Brew Options but not consistently referenced in recipes |

### What's Correct (verified)
✅ Espresso brew temperature (195-205°F), grind settings (6-12 fine, 19-22 medium, 23-25 coarse)
✅ Dual Froth System settings and milk tips
✅ Barista Assist technology description
✅ Advanced settings menu (h00-h08)
✅ Drip coffee basket insertion/removal
✅ Cold brew ~10-15 min brew time
✅ All 25 grind settings and their uses

---

## 2. New Recipe Recommendations (Top 18)

### Tier 1 — High Priority (trending, filling big gaps)

| # | Recipe | Category | Why |
|---|--------|----------|-----|
| 1 | **Pistachio Latte** | Specialty | #1 coffee trend of 2025 |
| 2 | **Iced Chai Latte** | Iced/Tea | Hot chai exists but no iced — essential staple |
| 3 | **Cookies & Cream Frappe** | Blended | Only 3 frappés currently; most-requested flavor |
| 4 | **Dubai Chocolate Latte** | Specialty | Viral TikTok — pistachio + dark chocolate |
| 5 | **Ube Iced Latte** | Iced | Filipino purple yam; visually viral |
| 6 | **Matcha Frappe** | Blended | Matcha exists hot/iced but not blended |

### Tier 2 — Seasonal & Variety

| # | Recipe | Category | Why |
|---|--------|----------|-----|
| 7 | **Apple Crisp Latte** | Specialty | Fall bridge between Pumpkin Spice and Gingerbread |
| 8 | **Snickerdoodle Latte** | Specialty | Cozy cookie-inspired, simple ingredients |
| 9 | **Peach Iced Tea** | Tea | Most popular iced tea; no fruit teas exist |
| 10 | **Coconut Cream Cold Brew** | Iced | No coconut cold brew variant yet |
| 11 | **Raspberry Mocha Iced Latte** | Iced | First fruit+chocolate combo |
| 12 | **Rooibos Honey Latte** | Tea | First caffeine-free latte option |

### Tier 3 — Niche & Interest

| # | Recipe | Category | Why |
|---|--------|----------|-----|
| 13 | **Red Velvet Latte** | Specialty | Instagram-worthy dessert latte |
| 14 | **Cookie Butter Latte** | Specialty | Biscoff flavor — Starbucks secret menu staple |
| 15 | **Vanilla Bean Frappe** | Blended | Builds out the frappé section |
| 16 | **SF Pistachio Latte** | Sugar-Free | Wellness counterpart to trend #1 |
| 17 | **Sparkling Berry Espresso** | Specialty | Opens fruity mocktail sub-category |
| 18 | **Affogato al Caramello** | Cocktails | Elevated affogato with caramel gelato |

---

## 3. Feature Brainstorm (Priority Matrix)

### ✅ Quick Wins (< 2 hrs each, high impact)

| # | Feature | Effort | Why |
|---|---------|--------|-----|
| 1 | **Share recipe button** | ~1 hr | Site already supports `#recipe-id` hash links — just expose the Web Share API |
| 2 | **"Surprise Me" random recipe** | ~30 min | Trivial `Math.random()` — gives users a reason to explore |
| 3 | **Recently viewed history** | ~1 hr | Track last 10 in localStorage, show as horizontal scroll on home page |
| 4 | **Sort recipes** (A-Z, rating, type) | ~1.5 hr | Basic UX — currently only search + filter |
| 5 | **Filter by milk compatibility** | ~1 hr | All Milks / Dairy Only / Plant-Based / No Milk — data already exists |
| 6 | **Print-friendly CSS** | ~1.5 hr | `@media print` — users want to print recipes for the kitchen |
| 7 | **Caffeine strength indicator** | ~1 hr | ⚡ Low / ⚡⚡ Med / ⚡⚡⚡ High badge on each recipe card |

### 🔷 Medium Value (2-6 hrs)

| # | Feature | Effort | Why |
|---|---------|--------|-----|
| 8 | **Prep & brew time** on each recipe | 2-3 hrs | 90 recipes need the data field added |
| 9 | **Seasonal collections** (curated lists) | ~2 hr | "Summer Sips", "Holiday", "Low-Cal" horizontal scrolls |
| 10 | **Milk-aware ingredient scaling** | ~2 hr | When you select milk, ingredients update (oat milk instead of "milk of choice") |
| 11 | **PWA support** (offline, Add to Home Screen) | 5-6 hr | Biggest UX leap — turns site into a countertop app |
| 12 | **Custom notes per recipe** | 1.5 hr | Users jot grind adjustments |
| 13 | **Calorie estimator** | ~2 hr | Dynamic based on milk + size selection |

### 🚀 Big Ideas (5+ hrs)

| # | Feature | Effort |
|---|---------|--------|
| 14 | Export/Import user data (favorites, ratings, notes) | ~2 hr |
| 15 | Custom recipe builder (user-created recipes) | 5-6 hr |
| 16 | Dark/Light theme toggle | ~2 hr |
| 17 | Brew journal / tasting log with history | ~5 hr |
| 18 | Page transitions & micro-animations | ~3 hr |

### Recommended first sprint
**Quick Wins (#1-7)** — ~8 hours total, no new data fields needed, biggest polish per hour.

---

## Next Steps for Kate

1. **Review the 3 confirmed errors** (Cold-Pressed brew time, Luxe basket capacity, cleaning cycle) — these affect recipe accuracy
2. **Pick your top 5 recipes** from the new list to start with
3. **Choose which features** you want first from the Quick Wins tier
4. Reply here or in the thread and we'll start implementing

*This document is saved in the repo as `PLANNING.md`.*
