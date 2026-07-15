---
name: dailyfinds-brain-autopilot
description: >
  Hermes-side wrapper for the existing D:\my_bot autopilot_brain + analytics_brain + product_score_engine.
  Triggers local-only brain pipelines on schedule and returns a concise Telegram-friendly summary.
  NEVER calls Shopify/Printify/CJ/Spocket live APIs and NEVER mutates products/orders.
version: 0.1.0
trigger:
  - "run DailyFinds brain pipeline"
  - "refresh autopilot brain"
  - "daily analytics report"
  - "product audit"
---

# DailyFinds Brain Autopilot

Runs the existing local DailyFinds brain stack as a scheduled/on-demand pipeline from Hermes.

## Source of truth

- `D:\my_bot\scripts\autopilot_brain.py` — observe → analyze → decide → memory-only execute → self_check → learn
- `D:\my_bot\analytics_brain\analytics_brain.py` — orders / validated / rejected / traffic / creative metrics
- `D:\my_bot\product_score_engine.py` — 0-100 scoring gate, ≥80 list-ready

## Hard rules

1. Local-only. Do not call Shopify Admin, CJ, Spocket, Printify fulfillment, email, or social APIs.
2. Read-only by default. Existing code already blocks live mutations; preserve that invariant.
3. Output goes to Telegram summary + local reports under `D:\my_bot\reports\`.
4. If an exception occurs, report the traceback and stop; do not auto-publish or edit `.env`.

## Invocation

Preferred entry point is Hermes terminal running from `D:\my_bot`.

```bash
cd /d/my_bot && python scripts/autopilot_brain.py
cd /d/my_bot && python analytics_brain/analytics_brain.py
```

If `python scripts/autopilot_brain.py` fails due to import path, fallback:
```bash
cd /d/my_bot/scripts && python autopilot_brain.py
```

## Cron prompt template

Use this exact prompt structure when creating the scheduled Hermes job.

Prompt:
```
Run the DailyFinds local brain pipeline from D:\my_bot and return a compact status summary suitable for Telegram delivery.

Steps:
1) `cd /d/my_bot && python scripts/autopilot_brain.py`
2) `cd /d/my_bot && python analytics_brain/analytics_brain.py`
3) Read:
   - reports/daily_brain_report.md
   - reports/analytics_report.md
   - reports/daily_brain_report.json
   - reports/analytics_report.json
4) Build a short Telegram-style summary including:
   - observed / analyzed / publish_candidates / needs_fix / rejected
   - orders / estimated_revenue / estimated_profit / winner_candidates
   - top rule suggestions from rule_evolver if any
   - profit risks and content gaps
5) Keep it under 1200 Chinese + English mixed chars. No guarantees or medical claims.
6) If any step fails, say which step failed and include the error text truncated to useful length.
```

Skill files:
- references/dailyfinds-context.md — brand rules, sourcing constraints, red-team concerns
- references/shopify-printify-dailyfinds.md — Windows CJ/Printify/Shopify API path constraints

## Safety invariants

- Do not enable live mutations through `config/autonomy.yaml` during this run unless explicitly approved by user.
- If mutation flags appear true in report output, route as a red/yellow issue and ask for approval instead of publishing.

## Verification

After each scheduled run, expected artifacts:
- `D:\my_bot\reports\daily_brain_report.md`
- `D:\my_bot\reports\daily_brain_report.json`
- `D:\my_bot\reports\analytics_report.md`
- `D:\my_bot\reports\analytics_report.json`
- `D:\my_bot\memory\product_memory.jsonl` append
- `D:\my_bot\memory\decision_journal.jsonl` append
- `D:\my_bot\analytics_memory\latest_analytics.json`

If any required file is missing after success, treat as partial failure in the Telegram summary.

## Works with

- hermes cron
- Hermes memory
- Telegram gateway
- coding-agent-cli for deeper code review
