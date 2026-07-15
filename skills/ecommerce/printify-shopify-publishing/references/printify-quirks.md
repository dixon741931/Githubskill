# Printify API quirks for DailyFinds catalog generation

## Confirmed blueprint/provider/variant IDs (2026-07-03)
- BP 488 / provider 48 / variant 81075 => Desk Mat 31.5" x 15.5"
- BP 582 / provider 70 / variant 71664 => Mouse Pad rectangle
- BP 282 / provider 99 / variant 43138 => Art Print 16" x 20" Matte

## Sales channel behavior
- `GET /shops.json` returns `sales_channel: "disconnected"` for unlinked stores.
- When disconnected, `POST /shops/{id}/products/{pid}/publish.json` returns 400 and `shopify_product_id` is None.
- Publish payloads require `images`, `variants`, and `title` fields even when only syncing to Shopify.
- Product creation does NOT require an active sales channel; publishing does.

## Variant explosion
- Blueprint 282 poster line exposes 46 variants by default. Always pin exact variant IDs to avoid accidentally enabling every size.
- Build script must support `cfg.get("variant_ids")` fallback + exact position resolution.

## Tag behavior
- Product-level `tags` in the publish/create body do not auto-populate Shopify product `tags` in this integration.
- Post-publish SOP must include manual/add-tag step in Shopify admin.

## Image upload
- Re-uploading the same image filename returns a new image ID each time; no deduplication.
- Image URLs are returned by upload endpoint; rely on ID for print_areas.
