# Zendrop Extraction Limitation — Session Note 2026-07-07

## Observed failure mode

- `browser_navigate` to `https://app.zendrop.com/my-products#store-listings` returns `(empty page)` / blank.
- `mcp_cua_driver get_window_state` on logged Chrome pid returns the browser shell only:
  - window chrome, tabs, address bar, bookmarks
  - **inner webpage content/table DOM is not exposed**
- This is not a login-wall or navigation timing issue; the data path itself is unavailable through current Windows/cua-driver Chrome instrumentation.

## Consequence

- Cannot extract `My Products` listing details, sourcing status, or shipping guarantees directly from Zendrop UI from this session.
- Do not retry the same dead-end tool path.

## Preferred alternatives for this blocker

- Use prior successful snapshot data the user already supplied (screenshots / manual copy-paste).
- Reuse Shopify-side data for products already synced/connected.
- Wait for either a Zendrop client implementation or a different extraction surface.

## Key quote from session

User: "我登入给你进去了... 这个zendrop api key为什么用不到".
Real blocker is not API key validity; it is the lack of a working extraction path from live Zendrop UI.
