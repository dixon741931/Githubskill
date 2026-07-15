---
name: ecommerce-product-research
description: "Multi-channel product research for dropshipping/ecommerce: sellability-first filtering, API-to-UI fallback when platforms block programmatic access, and structured extraction of cost/shipping/trend/saturation/stock data from Zendrop, CJ, Printify, Shopify Catalog, and similar sources."
---

# Ecommerce Product Research

## Core Principle

**Sellability first, not just keyword match.**

When sourcing products, always extract and evaluate concrete sellability signals:
- Product cost / supplier price
- Shipping cost and avg delivery time
- Current stock status (in stock / out of stock)
- Order trend score and trend % (e.g. +40% vs -70%)
- Saturation level (Low/Medium/High)
- Orders by country (US share matters most for US stores)
- Supplier reliability (Zendrop Fulfillment, The Boss Store, Amazon Products, etc.)

Discard listings that are Out of stock or have sharply negative trend unless there is a specific reason to wait.

## DailyFinds Commerce OS Preflight

Before doing any product research or execution for DailyFinds, confirm these rules are loaded:
- Source file: `D:/my_bot/DAILYFINDS_COMMERCE_OS_MASTER.md`
- Source file: `D:/my_bot/DAILYFINDS_DESIGN_SYSTEM.md`

Provider/runtime constraints:
- Hermes gateway and any scheduled jobs must run on Nous Portal free tier (`stepfun/step-3.7-flash:free`) unless the user explicitly switches providers.
- DeepSeek is allowed for local Hermes TUI sessions only when the user confirms available balance; never assign deepseek to cron or background automations.
- If `.env` writes are blocked by Hermes, tell the user to append the line manually and restart the gateway from a detached shell; do not retry programmatic `.env` mutation blindly.

Required rules:
- Product must fit exactly one of the 5 pillars: Desk Body Reset / Sleep & Screen Reset / Recovery Comfort / Travel Comfort / Everyday Functional Tools
- Gross margin target is 55%+ before ads
- U.S. fast shipping must be verified, not assumed
- Do not create Shopify products until Deep Dive result is DO
- Do not publish live edits without approval
- Never use guarantee/shipping-guarantee/medical-cure language
- PDP must follow mature standard order: image/video → benefit → problem → solution → features → included → specs → shipping & returns → care/safety → FAQ → soft CTA
- Design tokens from `DAILYFINDS_DESIGN_SYSTEM.md` govern color/type/voice; do not invent new hex or hype language

If any of the above is unclear, stop and learn from the source files before continuing rather than creating partial work.

## Multi-Channel Search Order

1. **Zendrop** — best direct UI data; if API is blocked by WAF/CDN, fall back to logged-in browser UI search
2. **CJ / Printify** — parallel search with same sellability checklist
3. **Shopify Catalog API** — only if credentials are valid and endpoints respond
4. Mark any channel that consistently 403/1010 as blocked for the session and do not retry

## API-to-UI Fallback Pattern

When programmatic API calls return 403/1010/WAF errors despite valid keys:
1. Stop retrying the API
2. Open the platform's logged-in browser session
3. Use the platform's native search UI (`desk organizer`, brand-free category terms)
4. Extract data from listing cards (cost, trend %, saturation) and detail pages (shipping time, stock, description)
5. Record the product URL as the source-of-truth link

This bypasses CDN/WAF that targets headless requests while the browser session is whitelisted.

### Zendrop Chrome-Search Pitfall

In the Zendrop Electron app, typing into the search field through UIA/value writes often does not reliably reach the renderer. Do not keep retrying blind keystrokes. Prefer one of:
- Use URL-based search: `app.zendrop.com/product?page=1&shipsFrom=US&search=<term>`
- Click visible product links on the current listing page to open detail pages
- Re-grab a fresh window snapshot after each action instead of assuming the input landed

Also prefer the logged-in pid/window path for data extraction; `browser_navigate` to the same Zendrop URL can land on `(empty page)` while the existing pid session still has live DOM.

#### Zendrop Windows / cua-driver workarounds

See `references/zendrop-windows-cua-workarounds.md` for the stable address-bar navigation, keyboard sequencing, click-retry rules, UIA write verification, and verified short keywords for this niche.

#### TikTok Aesthetic Signal Bank

For this user's workstation-beautification niche, TikTok supplies strong hook cues: multifunction desk gadgets with visible light/motion/charging.

### Current strong archetypes
- 7in1/6in1 alarm clock + wireless charger + night light + bluetooth speaker + phone stand
- Modern alarm clock wireless charger desk lamp
- Jellyfish / mood lamp desk decor (LED movement is TikTok-friendly)
- Spiral tree / wrought-iron LED desk ornament with high growth velocity
- Minimalist digital alarm clock + desk lamp combo with app control

When searching Zendrop for these, prefer short nouns: `alarm clock wireless charger`, `desk lamp wireless charger`, `jellyfish lamp desk`, `spiral lamp desk`. Full signals with source notes are in `references/tiktok-aesthetic-signals.md`.

#### Zendrop Search Workflow That Actually Works

On Windows / cua-driver:
1. Re-grab `get_window_state` for the Zendrop pid to get the freshest element indices.
2. Click visible search / address bar Edit element from that snapshot.
3. Send `ctrl+a`, then type the full expected term or URL; verify the `value` from a fresh snapshot before executing.
4. Press `return` to execute the search.
5. Read results with `mcp_cua_driver_page action=get_text` or `get_window_state`; do not rely on `execute_javascript` — on Windows it may be unavailable if no CDP bookmark/port is configured.
6. If a term returns "No products found", do not retry the same term — switch to a synonym/adjacent niche keyword and rerun the search from step 2.

#### URL/Addressbar Concatenation / Wrong-Page Hazard

When reusing a visible browser Edit after navigation, its hidden value may still be an unrelated URL or leftover search term. Typing then concatenates. Before search, always do `ctrl+a`, read `value` back, and only then type the full desired value.

#### Zendrop Default Feed Is Not Desk-Filtered

The `Find Products` home listing is a mixed generic catalog. Do not spend turns scrolling it hoping for desk/DESKO items. Go straight to search. Valid directional nouns for this niche:
`monitor stand`, `headphone stand`, `desk lamp`, `rgb desk mat`, `cable management`, `desk riser`, `acrylic organizer`, `wood desk organizer`, `standing desk converter`.

#### Delivery-Mode Escalation For Chrome Input On Windows

Some Chrome/Electron surfaces drop background input events entirely. Two distinct failure modes:
1. Input no-op: typed text never lands. Error shape: empty/no-op result. Remedy: same element with delivery_mode:"foreground" after re-snapshot.
2. Click no-op / wrong-page jump: UIA Invoke reports success but launches an unrelated surface. Error shape: invokes a different role or page. Remedy: retry exact same element_index with delivery_mode:"foreground" on a fresh get_window_state, then verify current page by reading the address bar value or page title.

Do not preemptively use foreground on the first attempt. Do not repeat the same stale index after navigation; re-grab get_window_state first.

### Zendrop Navigation Hygiene

- After every click/navigation that could change pages, **always re-grab `get_window_state`** before the next element-indexed action; element indices are snapshot-scoped and become stale after page changes.
- If the URL bar shows a detail/product page you did not intend, use the visible **Back** link or the nav **Find Products** link to return to the listing page before searching again.
- Avoid `browser_navigate` on Zendrop once you already have a logged Chrome pid; it frequently resets to an empty page and wastes turns. Use pid-scoped CUA actions instead.

## Niche Alignment Filter

Before scoring sellability, confirm the product fits the user's target niche. For this user, the niche is: **workstation beautification + gaming/PC workspace + desk aesthetics**. Preferred attributes:
- Design cues: RGB, acrylic, wood grain, minimalist/Nordic, magnetic, wireless charging, clean cable-management aesthetics
- Functional cues: stand, dock, tray, headphone mount, riser, mat, organizer with visual polish
- Buyer persona: PC workers, gamers, creators who treat their desk as a visual identity
Reject products that are purely utilitarian with no design/beauty signal, or that belong to unrelated categories.

## Image-Visibility Requirement

For any candidate product to be considered sellable in this user's workflow, the listing must expose viewable product images in the supplier UI. If a product card or detail page has no photo / broken image / empty media, it is **unsellable regardless of cost or trend data**. This matches the user's explicit rejection: "都看不到照片" → product discarded.

## Personalization Requirement

When the user requests personalized/custom products:
- On each listing, look for explicit customization signals: variant names like “Custom/Engrave/Name/Photo upload/POD”, supplier-tagged personalization, or multi-SKU configurators
- If supported, record the personalization type so launch-cell can expose it at checkout
- Also capture an original product image URL from the listing detail/media assets; requirement is “original image viewable”, not just a generic thumbnail
- Target count is part of the deliverable: eg 2 of 5 products must be personalizable with viewable original images

### Zendrop Personalization Signals

In the current UI, personalization is usually visible as:
- Buttons/variants labeled with custom-related text under a “Size” or choice group
- Multiple named design/style variants (eg Galaxy, Dragon, Anime)
- SKU/configurator listings with visible selection buttons and at least 1 high-res product image

If none of the above are present, mark the product `personalizable: false` unless the detail page explicitly states engraving/upload/customization.

## Channel Availability Notes

With the current Zendrop/Shopify/Spocket implementations:
- **Zendrop API**: treated as **blocked for the session** on WAF/CDN signals (HTTP 1010 / 403). Do not retry programmatic API probes.
- **Zendrop API key presence ≠ usable client**: `.env` may contain `ZENDROP_API_KEY`, but the local codebase has no Zendrop SDK/MCP consumer that can turn this key into working product/order/sourcing API calls. Do not spend turns constructing ad-hoc Zendrop API requests; treat this channel as browser-UI-only until a client is explicitly implemented.
- **Zendrop UI current limitation on Windows / cua-driver**: In the observed setup, `browser_navigate` to Zendrop returns `(empty page)`, and `mcp_cua_driver get_window_state` on the Chrome pid exposes the browser shell (tabs, address bar, menus) but **not** the inner webpage content/table DOM. This means **Zendrop product-list extraction is currently blocked at the tooling layer**, not just a navigation issue. Do not keep retrying Zendrop page reads once this limitation is confirmed — switch to known snapshots, user-supplied screenshots, or another channel.
- **Shopify → Zendrop direct bridge**: No local code path currently exists to enter Zendrop from Shopify side. The Zendrop "Linked" status visible in the UI reflects a cloud-side integration; it is not reusable from local scripts.
- **Shopify Catalog API**: treat as unavailable if the interface/admin surfaces “Catalog search failed”. Do not rely on it as a primary source until validated.
- **Spocket**: in this environment, external app pages are consistently 403/login-walled; mark it blocked and do not retry.

## Same-Style Sourcing Conclusions (2026-07-07)

For aesthetic desk / workstation-beautification SKUs already on Zendrop/Shopify:
- **CJ Dropshipping**: 12 checked SKUs → **10 have no exact same-style / same-SKU / same-image matches**. Only 2 products show external same-name signals (`Cozy Cabin Natural Wood Table Lamp`, `Rawlins Leather Desk Pads`).
- **Functional approximations on CJ exist**, but they do not clear the same-style bar for cost-cut replacement.
- **Decision rule**: do not spend additional turns retrying CJ for exact same-style matches on aesthetic desk products. Either switch channels or treat current supplier as source of truth.
- **AliExpress direct search**: headless browser and `browser_navigate` both return CAPTCHA pages. Do not retry AliExpress search URLs automatically. Preferred paths: web_search, DSers plugin on user's Chrome, or user-supplied AliExpress links.
- **Playwright/verification fallback**: when browser automation is unstable, Playwright can verify product pages, but it does not bypass platform bot checks. Use it for evidence gathering, not as a sourcing bypass.

## Frontline Status Habit

After substantive sourcing/shop work, write a consolidated frontline status file under `02_Products/YYYY-MM-DD_Frontline_Status.md` and update `00_Home/HOME.md` with a pointer. This preserves exact state across sessions and replaces ad-hoc chat-based handoffs.

## TikTok Aesthetic Signal Bank

For this user's workstation-beautification niche, TikTok supplies strong hook cues: multifunction desk gadgets with visible light/motion/charging.

### Current strong archetypes in window
- 7in1/6in1 alarm clock + wireless charger + night light + bluetooth speaker + phone stand
- Modern alarm clock wireless charger desk lamp
- Jellyfish / mood lamp desk decor (LED movement is TikTok-friendly)
- Spiral tree / wrought-iron LED desk ornament with high growth velocity
- Minimalist digital alarm clock + desk lamp combo with app control

When searching Zendrop for these, prefer short nouns: `alarm clock wireless charger`, `desk lamp wireless charger`, `jellyfish lamp desk`, `spiral lamp desk`.

See `references/same-style-audit-cookbook.md` for same-style matching, match taxonomy, and AliExpress/CJ/Zendrop source-of-truth rules.

## Search Strategy

- If exact brand/keyword returns no products (e.g. `DESKO` → `No products found`), broaden to niche terms (`gaming desk setup`, `desk organizer`, `desk mat`, `headphone stand`, `monitor stand`, `cable management`, `acrylic desk accessories`)
- If the research pipeline does not contain DESKO-relevant keywords, inject manual DESKO seeds into `data/cj_search_seeds.json` **before** running CJ searches.
- Run the broad search once, then drill into individual listings for full data
- For each promising listing, capture: title, URL, cost, shipping time, stock, trend score, trend %, saturation, orders by country, supplier, personalization support, image URLs

## Shipping-claim Enforcement Rule

When enriching product descriptions, do NOT add "US 1–2 day shipping" claims unless one of these is confirmed:
- Supplier is explicitly US-warehoused and the listing states 1–2 business-day shipping
- SKU/order data clearly indicates US domestic fulfillment with fast transit
- The user explicitly approves a broader claim

If the only signal is an Amazon ASIN prefix (B0...) or generic notion, treat it as **unconfirmed** and omit the claim rather than risk a false promise.

## DSERS Logistics Browser Behavior

For DSERS Shipping Settings (`Logistics_Setting`) form edits on Windows / cua-driver:
- AX value writes to Advanced Shipping Method controls usually succeed, but the form may collapse or reset after SAVE.
- Use the verification procedure in `references/dsers-logistics-cua-lessons.md` instead of assuming persistence.
- If verification remains unstable, stop re-clicking blindly and ask for one visible user-side confirmation.

## Stuck-State Reporting Rule

If the browser falls into an about:blank, login-wall, or unchanged-page state after navigation, do **not** keep retrying blind CUA clicks or cookie-modal guesses. Switch to one of:
- Use an available logged-in browser session snapshot from a prior successful page
- Use `browser_navigate` to a known authenticated app URL
- Ship findings from already-captured listings and state which channels still need re-attempt later
This is especially important on Zendrop after navigation-driven context loss.

If the available feed is clearly off-niche after one targeted search, stop scrolling and **switch channels or keywords** instead of consuming more turns.

### Zendrop Sidebar-Index Hazard (Windows / cua-driver)

After any navigation or page change, **sidebar nav element indices can shift**. When UIA elements are re-indexed, clicking a remembered index may open a completely different menu. Remedy:
- Re-grab `get_window_state` after each navigation before clicking sidebar links.
- Prefer stable anchors such as the visible `Back` link, the current URL/edit control `value`, or exact page `query` filtering.
- If an index jump is suspected, stop clicking sidebar indices by memory; re-snapshot or read `value` from the address/search Edit to confirm current location.

### Trend/Generic-Feed Risk

`Trending Products` is useful for spotting growing aesthetics fast, but it is **not a filtered desk/DESKO feed**. When Trending shows mostly unrelated categories, treat it as a signal that Zendrop’s default recommendation surface cannot replace keyword targeting for this niche; switch back to targeted search terms.

## Shopify Draft-First Rule

Once a product passes sellability filtering, interpret "add to draft" literally: queue it into Shopify draft immediately without waiting to complete the full 5-product target. Do not batch-draft after returning a full report.

## Sellability Scoring Heuristic

Strong candidate = most of:
- In stock or restockable
- Cost low enough for 2–3x markup
- Trend % positive or score above 30
- Saturation not maxed out
- US shipping ≤ 7–8 days
- Supplier is a reliable fulfillment source

Weak candidate = any of:
- Out of stock with no restock path
- Sharp negative trend (-50%+)
- Saturation 100% High + declining trend
- Shipping > 15 days
- Supplier unknown or dropship reliability unclear

## Report Format

Output products as structured cards with the exact fields above. Rank by sellability, not by search relevance. If a product cannot be sold (no stock, bad trend, opaque shipping), say so explicitly rather than listing it neutrally.

## Same-Style Cross-Channel Sourcing Audit

Use this workflow when the user already has products on Shopify/Zendrop and wants exact-style matches on another channel to lower cost.

### Trigger

The user asks for same-style / same-product / same-SKU / same-image matches on another supplier channel, especially phrases like "同款", "更低的成本", "同图", "CJ 同款", "AliExpress 同款".

### Required inputs

- Existing Shopify product list, strongest signals first: exact product name, aesthetic keywords, and current channel cost/price.
- Preferred cost threshold: usually `< current selling price × 0.7` for meaningful savings.

### Execution order

1. **Same-style keyword mining from existing storefront**
   Derive 6–14 short product-noun keywords from each product: aesthetic adjective + core noun + style cue. Avoid long marketing sentences.
   Examples: `japandi desk mat`, `terracotta dune desk mat`, `sage line art desk mat`, `clay arch mouse pad`, `greige travertine mouse pad`, `cozy cabin wood table lamp`, `rawlins leather desk pad`.

2. **Exact-match candidate search**
   For each keyword, search the target channel with channel-native source:
   - CJ Dropshipping: use `supplier.cj.search` from `shopify/` project with `sys.path.insert(0, 'shopify')` so `config.settings` resolves.
   - AliExpress: do **not** use `browser_navigate` to AliExpress search URLs — they return captcha pages. Use one of:
     - web_search with descriptive queries, or
     - logged Chrome automation on AliExpress with DSers or existing session, or
     - AliExpress business/wholesale search via the extension if available.
   - Zendrop: use logged Chrome pid with URL-based search.

3. **Match classification**
   Classify every result as:
   - **Exact same-style / same-image candidate** — same design, same color story, same composition.
   - **Functional approximation** — same use case, different design; insufficient for cost-cut replacement.
   - **Mismatch / banned** — unrelated category or previously rejected product.

4. **Cost-cut audit table**
   Produce one table per product with columns:
   `product | current_channel | current_price | match_channel | match_price | shipping | stock | personalization | notes | save?`

5. **Recommendation rule**
   - If no exact-style match exists on the cheaper channel, say so directly. Do not propose functional approximations as same-style savings.
   - If a named external listing appears on multiple resale sites with the same product name and image, treat it as a same-style candidate for comparison even if the supplier API does not surface it.

### Platform status assumptions for this task class

- CJ Dropshipping: usable if `from config import settings` works under `shopify/` and `CJ_API_KEY` is present in `.env`. Search `listV2` with `countryCode=US`; do not retry blocked endpoints.
- AliExpress: direct page search is captcha-walled; prefer web search, DSers, or existing browser session. Do not retry AliExpress search URLs through `browser_navigate` after one captcha result.
- Zendrop UI: use logged pid with fresh `get_window_state` snapshots; avoid blind sidebar clicks.
- Spocket: treat as blocked if app pages return 403/login-wall.

### User style requirements for this workflow

- Do not explain the research process; present conclusion first, then evidence.
- When no same-style match exists, say "Cannot find" with the searched keywords, not "only functional alternatives available".
- Provide clickable validation links for every candidate.
- If the user asks for channel A only, do not pivot to channel B unless A returns empty results.

### Same-style watch list

From recent same-style audits, these product families showed external multi-channel same-style evidence beyond Zendrop:
- Natural wood table lamp with named retail listings on eBay/Walmart/Simon.
- Large rawlins-style leather desk pads appearing on multiple DTC/Amazon/Etsy sellers with identical size + nominal product name.
- Botanical dried-study wall art appearing on Atelier Printworks / Amazon / Etsy.
