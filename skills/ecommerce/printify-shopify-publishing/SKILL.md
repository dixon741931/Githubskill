---
name: printify-shopify-publishing
description: "Class-level workflow for pushing Printify products into a connected Shopify store, covering blueprint discovery, asset prep, dry-run, serial builds, publish sanity checks, post-publish SOP, and store cleanup."
---

# Printify → Shopify Publishing (POD)

Class-level workflow for pushing Printify products into a connected Shopify store, with conventions for DailyFinds-style catalog generation and post-publish SOP.

## Workflow

1. **Discover blueprints**  
   Run `python agents/product/<catalog>.py --discover` to list candidate blueprints. Confirm real IDs, then hardcode `BP_*`, `PP_*`, and `VP_*` constants. Variant counts can explode (e.g. poster blueprints → 46 variants); pin a single variant ID after inspecting the first product.

2. **Prepare assets**  
   Art files must exist at the exact paths referenced in `ART_DIR / cfg["img"]`. Use absolute-generation scripts instead of moving renamed files between directories; renaming mismatches (`*_flat.png` vs `*.png`) causes silent skips.

3. **Dry-run**  
   `python <catalog>.py` without `--go` prints every SKU config and exits. Verify tags, handles, prices, and art paths before touching the API.

4. **Create products**  
   `python <catalog>.py --go <sku>` (serial, one SKU at a time). Background `--go all` runs can hang after ~12 products; prefer explicit serial calls or small batches with `time.sleep(0.5)` between them.

5. **Publish and detect integration state**  
   After each create, inspect the Printify product: if `status` is `None` and `sales_channel_ids` / `shopify_product_id` are `None`, the shop’s sales channel is **disconnected**. `publish.json` will return 400. Fix at Printify Dashboard → My Stores → Shopify, then re-publish.

## Post-publish SOP on Shopify
  Set `template_suffix = dailyfinds`, confirm tag `DailyFinds` exists, and assign shipping profile. Printify cannot do this via API; emit a `*_post_publish_sop.json` checklist per run.

  **Personalization hook**  
  `df-product-hero.liquid` conditionally shows a Personalize CTA when `product.metafields.dailyfinds.personalize_url` is set. The Printify app exposes a **Personalizable** tab and per-product editor link (`/app/editor/<productId>`); actual personalization layers are configured in the Printify UI, not via API. Set `personalize_url` to the customizer page or external URL after enabling personalization in Printify.

  **Shopify theme-side Personalize Button block**  
  In the theme editor, add an **Apps** section, then add the **Personalize Button** block inside it. Configure button text, modal title, colors, and CSS classes in the sidebar. Save the theme with `Ctrl+S`. When `product.metafields.dailyfinds.personalize_url` is set, the native block renders the Personalize CTA automatically. Verify via Admin API readback of the theme asset rather than trusting UIA state alone.

## Store cleanup
   Use `scripts/store_cleanup.py --dry-run` to list off-brand products older than N days. Keep products tagged `DailyFinds` or in protected collections (e.g. `remembrance`, `a-beloved-pet`). Run `--archive` or `--delete` after reviewing the dry-run.

## Catalog file conventions

- `agents/product/<name>.py` should expose `CATALOG`, `build(cfg, go=False)`, and `--discover` / `--go` CLI.
- `PRODUCT_TYPES` dict must include `provider_id` and `variant_ids` per type to prevent variant explosion.
- Tags per SKU: `["DailyFinds", "warm-desk-collection", "desk", <product_type_handle>, <design_kw>]`

## Pitfalls
  
- **Variant explosion**: Poster / art-print blueprints often ship 40+ variants. Do not publish until `variant_ids` is pinned to the intended SKU.
- **Sales channel disconnect**: `GET /shops.json` returns `sales_channel: "disconnected"` when Shopify integration is broken. The product is still created in Printify but never reaches Shopify. Detect this before scaling.
- **Wrong .env path**: Scripts in `scripts/` must not use `load_dotenv("../.env")`. Use `Path(__file__).resolve().parent.parent / ".env"`.
- **Background batch timeout**: `python <catalog>.py --go all` in background can hang after ~12 publishes. Serial invocations are more reliable.
- **Image path mismatches**: Renaming or relocating art files without updating `DESIGNS[...]["file"]` causes silent `SKIP: art file missing`.
- **Products invisible despite `status=active`**: In Shopify Admin API, `status=active` alone does not mean a product is visible on the storefront. `published_at` must be set. A missing `published_at` means the product is effectively draft/unpublished even though `status=active`.
- **Token discovery fallback**: If `SHOPIFY_ADMIN_TOKEN` is absent, `SHOPIFY_API_KEY` may still authenticate for product/theme reads/writes in some stores, but not all scopes (e.g., `script_tags.json` returns 403). Preferred env var name is `SHOPIFY_ADMIN_TOKEN`.
- **Printify embedded-app automation limits on Windows/Chrome**: The Shopify-admin-embedded Printify app lives inside an iframe/app-frame container. On Windows, cua-driver UIA often exposes only the outer Shopify shell; inner Printify buttons/forms may not be actionable, and CDP `execute_javascript` requires a separately launched `--remote-debugging-port` Chrome. Repeated blind pixel clicks and address-bar navigation attempts are usually unverifiable and waste turns. Stop after one confirmed read-only failure and fall back to: Shopify Admin API metafields, manual dashboard steps, or a different tool path.
- **Theme edits need API readback confirmation**: After saving changes in the theme editor, UIA can continue showing stale success/neutral state. Confirm save by reading the asset back with `GET /themes/{id}/assets?asset[key]=...` before claiming the patch is live.

## References

- `references/printify-quirks.md` — provider/variant discovery results and sales-channel behavior
- `references/shopify-collections.md` — smart collection rules and template_suffix conventions

## Scripts

- `scripts/store_cleanup.py` — archive/delete off-brand products
- `references/live-theme-diff.md` — pattern for pulling live theme assets via Admin API (`GET /themes/{id}/assets`) before editing worktree copies, to avoid pushing stale `df-product-hero.liquid` variants.
