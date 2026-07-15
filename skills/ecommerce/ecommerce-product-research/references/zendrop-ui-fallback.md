# Zendrop UI Fallback (Windows + CUA driver)

Use this when Zendrop API returns 403 / 1010 / WAF blocks.

## Browser state
- Working session: Chrome pid=70428, window_id=1642584
- The session starts logged in from prior runs; if `browser_navigate` shows login form, stop retrying that session and switch to CUA driver on the existing Chrome window.

## Search UI
- Search bar address index: 62
- Back / Find Products link index: 47
- Default listing URL shape: `https://app.zendrop.com/product?page=1&search=<term>`
- If typing + Enter does not update URL, type into element_index 62 then press_key `return`.

## Data to extract from search cards
- Title, product URL
- Price
- "Add to My Products" button presence = importable?
- Related products carousel sometimes surfaces better candidates

## Data to extract from detail page
- Supplier name
- Product cost / shipping
- Shipping days + handling days
- Trend % / trend score / saturation / orders by country
- Bullet description lines contain design keywords and variant names

## Personalization signals in UI
- Variant/style buttons or named design choices
- Multi-design sets (Galaxy, Dragon, Anime, World Map, etc.)
- Supplier descriptions that mention custom / engrave / upload / name / photo

## Observed stuck states in this environment
- After homepage search + detail click + JS `location.href=...` + typing the URL directly, the product listing view can land on a blank page state where `get_text` returns very small text and the DOM query returns only generic nodes such as `Document "搜索图标"`.
- In that state, cached tool result files may also show empty `structuredContent` / `markdown_len=0` responses.

## Anti-loop rule
If after 2 navigation attempts you get login wall, about:blank, or unchanged URL, stop and report with durable links; do not keep clicking.
- If you need a reusable search result, prefer PET mapping available cached listings from prior successful captures.
- Do not regenerate product data by fabricating prices/trends; only report what was directly visible or already captured.

## Session note 2026-07-06
- Confirmed desk-related candidate from current listing page: `Mesh Desk Organizer` at `https://app.zendrop.com/product/1913985`, supplier `The Boss Store`, shown cost `$22.94`, growth `-70%`. Verify stock and personalization on detail page if needed.
- Confirmed in-session typing into the Electron search field is unreliable; direct URL search is preferred. Also confirmed `browser_navigate` to `app.zendrop.com` may return `(empty page)` while the existing pid/window DOM still contains live listings.
