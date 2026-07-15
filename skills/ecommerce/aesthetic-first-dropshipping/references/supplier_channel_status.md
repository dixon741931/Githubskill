# Supplier Channel Status — DailyFinds / D:\my_bot

## Active channels

| Channel | Status | Notes |
|---|---|---|
| `shopify.product.finder` (`smart-autopilot`) | ✅ working | Default queries need taste-driven replacement |
| `supplier.cj` | ✅ working | US warehouse filter required; rate limit ~20 req/min |
| `printify.printify_client` | ✅ token present | `.printify_token` at `D:\my_bot\printify\.printify_token`; discovery script exists |
| Spocket | ⚠️ draft only | No live API client in codebase; used for manual draft push (leather line) |
| ZenDrop | 🆕 key added | `.env` now contains `ZENDROP_API_KEY`; no client yet; discovery pending |

## Key files

- `D:\my_bot\shopify\product\finder.py` — CJ search → detail → freight → economics
- `D:\my_bot\shopify\product\pricing.py` — margin / price calculation
- `D:\my_bot\supplier\cj.py` — CJ API 2.0 client
- `D:\my_bot\printify\printify_client.py` — Printify order + upload
- `D:\my_bot\printify\printify_discover.py` — blueprint / provider discovery
- `D:\my_bot\agents\product\aesthetic_translator.py` — design → supplier queries

## Known quirks

- `finder.py` imports `config.settings` from `shopify/config/settings.py`, not top-level `config`. Must run from `D:\my_bot` with `PYTHONPATH=D:\my_bot` if calling from outside `shopify/` package context.
- `dailyfindusa_os.py` now has `aesthetic-hunter` subcommand; standalone translator is in `agents/product/aesthetic_translator.py`.
- `taste_profile.json` lives at `D:\my_bot\data\taste_profile.json`; includes `desk_organizer` section with CJ/Printify/Spocket query mappings.
