# Shopify collection conventions for DailyFinds

## Collection structure
- Smart collections are preferred for auto-population by tag.
- `warm-desk-collection` matches products with tag `warm-desk-collection`.
- Rule column `product_type` is NOT valid in Shopify Admin API; use `tag` or `vendor`.

## Template suffix
- Published theme id: `147553779791` (as of 2026-07-03).
- Known-good `template_suffix`: `dailyfinds`.
- Shopify Admin API does not expose template suffix listing; infer from existing products.

## Store-wide tag convention
- Every DailyFinds product must include tag `DailyFinds`.
- Collection handle tags: `warm-desk-collection`, `desk`, `desk-mat`, `mouse-pad`, `art-print`.
- Design keyword tags: `pink-salt`, `morning-mist`, `warm-oak`, `desert-stone`, `linen-ink`.

## Off-brand cleanup boundaries
- Protected collections: `remembrance`, `a-beloved-pet` — never archive/delete.
- Keep products with `DailyFinds` tag regardless of age.
- Archive before delete; destructive ops require explicit confirmation.
