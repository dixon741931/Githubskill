# Printify iframe / Chrome automation evidence (2026-07-03)

## What worked
- Readable text extraction via cua-driver `get_text` from the Shopify-admin-embedded Printify app.
- UIA snapshot exposing outer Shopify nav and some app chrome, but not inner Printify product editor content.
- `Ctrl+S` save in the Shopify theme editor succeeded and was confirmed by Shopify Admin API readback of `sections/df-product-hero.liquid`.

## What did not work
- `execute_javascript` with CDP fallback on Chrome pid 70428 on Windows failed because Chrome was not launched with `--remote-debugging-port`. The bookmark-URL bypass also failed.
- `query_dom` with advanced selectors such as `iframe` or comma-separated tag selectors failed with the Windows UIA backend's limited selector support.
- Repeated `send_input` retries to navigate the Omni box did not change the page or change the address-bar value.
- Inner Printify buttons/lists in the app editor were not reliably clickable via UIA; element indices were stale after interactions.
- Printify public API returned 404 / SSL handshake failure from Python for this shop (`28123491`).

## Lesson
For the Shopify-admin-embedded Printify app on Windows, treat UIA/CDP as read-only reconnaissance at best. Prefer Shopify Admin API and manual dashboard steps for Printify configuration.
