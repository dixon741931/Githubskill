# Spocket / Visual Signal Evidence (2026-07-06)

## Spocket Discovery
- No live Spocket API client in `D:\my_bot`.
- Public search indexes weakly; supplier pricing hidden behind signup.
- One concrete product found: **4 Compartment Rustic Wood Desk Organizer** (Home & Garden).
  - Fixed 4-compartment, not modular.
  - Rustic wood / warm / minimal vs current CJ mechanical candidates.

## Behance Visual Observation Notes
- `desk prodcut` search mostly concept CGI, not real products.
- Design signals worth tracking: **KOMBO**, **Moushi**, **Modular Desk Set Concept for Ikea**.
- Best translation target remains **KOMBO-style modular-soft organizer**.

## API Route Decision
1. Preferred: **Spocket REST API**
   - Needs API key + base URL from user.
   - Lightweight client shape: `search`, `product`, `variants`, `shipping`.
2. Fallback: **browser route**
   - Requires logged Chrome window on Shopify admin / Spocket app.
   - Detect with `mcp_cua_driver_list_windows`.
   - If not available, stay on API/manual search.

## Next Actions
- If API key granted: implement `D:\my_bot\shopify\supplier\spocket.py`.
- Else: continue manual Spocket backend search until API access is obtained.
