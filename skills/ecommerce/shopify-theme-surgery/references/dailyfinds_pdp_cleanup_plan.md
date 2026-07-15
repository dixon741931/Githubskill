# DailyFinds PDP cleanup plan (approved items only)
Approved:
1. Remove hardcoded sections from PDP template: df-benefits-strip, df-how-it-works, df-problem-solution, df-included-usecases, df-comparison
2. Rebuild order in templates/product.dailyfinds.json to: crumb, hero, personalize, reviews, faq_shipping, related, sticky_atc
3. Rewrite sections/df-faq-shipping.liquid as a block-driven section with faq + panel_item blocks
4. Make existing dp-trust visible across all PDPs

Not approved / do not implement:
- New "U.S. Shipping · Made to Order · 30-Day Support" trust badge bar at PDP top

Blockers encountered:
- Admin API PUT /assets.json on template JSON returns 422 when embedded blocks reference section types without live schema; browser path may be required.
- Browser admin path is blocked by Cloudflare human verification until user interacts in Chrome.
