# Verification script pattern
Run AFTER every theme mutation to confirm:
1) product_type / collection fixes are still live
2) deleted section files return 404
3) template order no longer contains removed sections
4) new section asset exists if one was uploaded

## Expected report keys
- `shop_api`: status + shop name
- `product_type_fixes`: pid -> expected / actual / ok
- `sections_deleted`: section / still_exists / http
- `product_template`: order / legacy_still_in_template
- `new_section_asset`: exists / http
- `overall`: pass or enumerated issues

## Blocker phrasing
"Admin API write blocked with HTTP {status}. Browser path blocked by Cloudflare challenge. Please complete the human verification at: https://admin.shopify.com/store/{shop}/themes/{theme_id}/editor?context=theme&key={theme_id}"
