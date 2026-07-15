# Same-Style Sourcing Audit Cookbook

## When to use
- User has existing store products on channel A.
- Goal: find lower-cost same-style/same-image/same-SKU candidates on channel B or C.
- Trigger phrases: 同款, 同图, 更低的成本, CJ 同款, AliExpress 同款.

## Channel status assumptions
| Channel | Status | Notes |
|---------|--------|-------|
| CJ Dropshipping | usable | `from config import settings` under `shopify/` works; `CJ_API_KEY` present. Search `listV2` with `countryCode=US`. |
| Zendrop UI | usable | Logged Chrome pid; fresh `get_window_state` per action. |
| Zendrop API | blocked | WAF/CDN 1010/403; do not retry. |
| AliExpress search hub | captcha-blocked | `aliexpress.com/w/wholesale-...` returns captcha in both `browser_navigate` and Playwright headless Chromium. |
| AliExpress listings | usable | `web_search` plus direct individual listing URLs. |
| Spocket | blocked | App pages return 403/login-wall. |

## Keyword hygiene rule
For design-led aesthetic products, derive short product-noun keywords:
- `adjective + core noun + style/material cue`
- Examples: `japandi desk mat`, `terracotta dune desk mat`, `sage line art desk mat`, `clay arch mouse pad`, `greige travertine mouse pad`, `cozy cabin wood table lamp`, `rawlins leather desk pad`.

Do not use long marketing sentences; they fail on supplier search UIs.

## Match taxonomy
- **Exact same-style / same-image candidate** — same design language, same visual reference; valid for cost-cut replacement.
- **Functional approximation** — same use case, different design. **Never present as same-style savings.**
- **Mismatch / banned** — unrelated category or previously rejected product.

## Reporting rule
If no exact-style match exists, say "Cannot find same-style match on channel X" with searched keywords. Do not substitute functional alternatives as solutions.

## Multi-channel evidence signal
Some aesthetic desk products appear as named retail listings across DTC/Etsy/Amazon/Simon/Walmart. When multiple resale sites show the identical product name + image family, that is a same-style candidate even if the mainstream supplier API does not surface it.

Example product families with confirmed multi-channel presence:
- Named desk lamps lamp families on retail sites.
- Named large-grain leather desk pads on DTC/Etsy/Amazon.
- Framed dried-botanical study wall art.

## Validation links
For every candidate, provide a clickable source URL so the user can visually verify design identity. Do not rely on name-only claims for aesthetic matches.
