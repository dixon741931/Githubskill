---
name: shopify-theme-surgery
description: "Targeted edits to Shopify Online Store 2.0 theme assets: sections, snippets, templates, and order manifests."
---

# Shopify Theme Surgery

## When to use
- Removing/reordering hardcoded template sections from PDP/collection/blog templates.
- Replacing a section with a cleaner block-driven version.
- Backing up theme assets before live edits, and verifying edits through Admin API + live page probes.

## Hard rules
- ALWAYS snapshot relevant assets before any write.
- NEVER delete `layout/theme.liquid`, `config/settings_schema.json`, or checkout/liquid unless explicitly approved. Limit scope to PDP/collection/blog regions.
- NEVER publish, duplicate, or rename theme files without explicit approval.
- NEVER invent block types inside template JSON. Types must match the target section schema or Admin API returns 422.
- Prefer rebuilding sections/snippets and rewiring through template `order` arrays instead of inline markup.

## Workflow
1. Read canonical theme id from memory/env.
2. Enumerate only the 5-10 files touching the region.
3. Backup to a dedicated theme backup folder.
4. Edit locally. Use Liquid sections/snippets for content; keep template JSON to `type`, `settings`, `blocks`, `block_order`, `order`.
5. Upload with `PUT /admin/api/2024-01/themes/{id}/assets.json`.
6. Verify with a focused script.
7. If Admin API writes fail AND browser admin is blocked, STOP and hand a handoff URL to the user.

## Known gotchas
- Template JSON block types are not free-form; they must match section schema.
- Malformed JSON yields opaque 422s rather than helpful diffs.
- `section.blocks | where: 'type', 'x'` requires exact type strings from schema.
- Keep block IDs stable across writes to avoid duplicated blocks in the theme editor.
- **Count/type 422s are silent about root cause.** If `PUT /assets.json` returns 422 with Block count exceeds maximum or Setting must be a valid number, the template JSON is structurally wrong at the section level — NOT a general API bad-request. Inspect the section's `{% schema %}` first: check `max_blocks` for any section receiving blocks, and check whether a setting declared as `range`/`number`/`integer` is being passed as a string in template JSON. These mismatches return 422 before Liquid render.
- **Small validation trick after writes:** include a verification script that re-reads the template asset and prints `order`, section keys, and a few block settings. If the read-back JSON parses, Liquid schema compliance is very likely.

## DailyFinds-specific guarantee audit checklist
Before any product/content rollout, scan for hardcoded guarantee wording in the active main theme. From 2026-07-09 audit, only `sections/df-product-hero.liquid` contained hardcoded `30-day guarantee`; product body_html and Contact page had already been cleaned via Admin API.

Edit mapping for guarantee replacements:
- product hero trust bar: `30-day guarantee` -> `30-day returns`
- default panel label schema: `SHIPPING & GUARANTEE` -> `SHIPPING & RETURNS`
- approval-controlled only; do not change unapproved snippets.

## User preferences
- Implement only approved items; keep unapproved items as plans/files.
- Concise blocker statements when automation is impossible.
- Verification is mandatory: re-probe changed endpoints/assets.
- Theme backup required before live mutations.
- Collection routing must keep Shop, Lamp, and desk-first categories as first-class links in header and homepage; don't leave stale `all-finds`/`daily-need` links behind.
- For template JSON writes: JSON types matter. `max_blocks`, `range` `default: 3`, and dict-coded block assignments must match the section's `{% schema %}` exactly, or Admin API returns 422.
- Send large template JSON as form body `data={'asset[key]':..., 'asset[value]':...}` rather than URL `params=` to avoid HTTP 414.
- Shopify programmatic guarantee cleanup: product body_html overrides only modify product.content; trust-block and schema defaults in sections still render to shoppers. Always verify live PDP after API edits.

## References
- `references/verify_template_after_edit.md`
- `references/dailyfinds_pdp_cleanup_plan.md`

## Verification script pattern
Run AFTER every theme mutation to confirm:
1) product_type / collection fixes are still live
2) deleted section files return 404
3) template order no longer contains removed sections
4) new section asset exists if one was uploaded

### Used report keys
- `shop_api`: status + shop name
- `product_type_fixes`: pid -> expected / actual / ok
- `sections_deleted`: section / still_exists / http
- `product_template`: order / legacy_still_in_template
- `new_section_asset`: exists / http
- `overall`: pass or enumerated issues

### Blocker phrasing
"Admin API write blocked with HTTP {status}. Browser path blocked by Cloudflare challenge. Please complete the human verification at: https://admin.shopify.com/store/{shop}/themes/{theme_id}/editor?context=theme&key={theme_id}"
