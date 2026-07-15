# Shopify JSON homepage template edit pattern (2026-07-07)

## What
`templates/index.json` is a real JSON template, not liquid. It contains a `sections` map. Each section has `type`, optional `blocks`, `block_order`, and `settings`.

## Readback
Always `GET /themes/{id}/assets?asset[key]=templates/index.json` after write. The `asset.value` field contains the JSON string. Do not trust editor UI.

## Edit pattern
1. Load with GraphQL/REST admin API.
2. Change `sections.*.settings` for section-level configs.
3. Replace `sections.featured.blocks` and `sections.featured.block_order` for product rails.
4. `json.dumps(homepage, indent=2, ensure_ascii=False)` and `PUT /themes/{id}/assets` with `asset[key]=templates/index.json` and `asset[content_type]=application/json`.

## Pitfalls
- `templates/index.liquid` may not exist; this store uses the JSON template.
- `sections.new_finds` and `sections.featured` both use `df-featured` type but are independent blocks; update both separately if needed.
- Collection section keys are `shop_by_need`, `how_we_pick`, `yes_no`.
- Liquid section filenames use hyphens (`df-how-we-pick`); JSON template keys use underscores (`how_we_pick`). Do not confuse them.
- Homepage has no `image` asset key; product images come from `shopify://shop_images/...` references.
