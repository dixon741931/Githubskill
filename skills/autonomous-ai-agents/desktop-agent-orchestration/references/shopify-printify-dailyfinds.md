# Shopify + Printify Automation Notes (DailyFinds)

## Observed constraints
- Chrome pid 70428 on this Windows box does not launch with `--remote-debugging-port`.
- `mcp_cua_driver_page` click/execute_javascript paths fail without remote debugging port.
- `browser_navigate` to Shopify admin commonly lands on "Your connection needs to be verified before you can proceed".
- Shopify admin embeds Printify as an iframe; UIA snapshots may expose outer chrome but not Printify content.

## Practical paths
1. Use Shopify Admin REST API for product/metafield work from Hermes.
2. Use Printify API for shop/catalog/product operations where the public API supports it.
3. For Printify customization hub / visual product builder, fall back to a desktop agent or manual GUI action.
4. File-based handoff remains the most reliable Windows pattern for multi-step workflows requiring GUI interaction.

## API surface validated here
- Shopify Admin REST v2024-10: works with `SHOPIFY_API_KEY` from `.env`
- Printify shops API: returns shop list including `sales_channel=shopify`
- Shopify Products API: can read active products, images, variants, metafields
- Metafield write: PUT `/admin/api/<ver>/products/<id>.json` with `product.metafields[0]`

## Current product IDs (DailyFinds Warm Desk Collection)
- Desk Mat: 8911436021839
- Mouse Pad: 8911436054607
- Art Print: 8911436120143
