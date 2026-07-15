# Printify public API block evidence / fallback notes
Collected 2026-07-03 from Warm Desk Collection launch on shop `28123491`.

## Observed failures
- `GET https://printify.com/api/v1/shops/28123491/products.json` -> `404` HTML page, not JSON.
- `GET https://printify.com/api/v1/shops/28123491/products.json?search=<term>` -> `404` HTML page.
- `GET https://personalized.products.printify.com/api/v1/shops/28123491/personalizations/products.json` -> `SSLError: SSLV3_ALERT_HANDSHAKE_FAILURE` when called from Python `requests` with normal SSL context.
- Shopify-admin-embedded Printify iframe UI does not expose actionable elements after interaction; stale `element_index` and unverifiable pixel clicks. Chrome also showed a permission/verification barrier at the address bar level.

## Conclusion
Do not retry the same Printify public API write routes for this shop. Treat them as blocked from the current origin/environment.

## Shopify fallback that already worked
- `dailyfinds.personalize_url` metafield is writable via Shopify Admin API and is already set to `https://printify.com/app/store/products` on products `8911436021839`, `8911436054607`, `8911436120143`.
- `df-product-hero.liquid` already renders a conditional Personalize CTA when that metafield is present.

## Required manual step
Enable Personalization in Printify Product Creator and bind mockups to blueprints/variants in the Printify dashboard; API automation cannot complete those steps at this time.