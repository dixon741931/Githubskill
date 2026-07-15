# Codex exec blocker reference — 2026-07-03

## Observed failure: usage limit
- Command: `codex exec "..."` from Hermes terminal on Windows
- Exit code: 1
- Key stderr: `ERROR: You've hit your usage limit. Upgrade to Pro ... or try again at Jul 4th, 2026 3:36 AM.`
- Other noise in same run: `rmcp::transport::worker` Higgsfield MCP `AuthRequiredError`; `heygen-avatar` / `heygen-video` skill descriptions too long.
- Implication: provider quota/account limit, not local path/sandbox. Do not quote this as permanent tool failure; it resets after the stated time or after upgrade.
- Pattern: if `codex exec` returns this, schedule after the reset time or fall back to `claude -p` or file handoff.

## Observed failure: Telegram "Chat not found"
- Affected delivery target: `telegram:-1008807877069`
- Error: `live adapter send failed: Chat not found; delivery error: Telegram send failed: Chat not found`
- Direct implication: cron→telegram notification path is currently broken for this chat target.
- Diagnose before future runs:
  - bot still member of target group/chat?
  - chat ID changed after group promotion?
  - bot token still valid?
- Pattern: when `last_delivery_error` contains `Chat not found`, switch cron `deliver` to `local` and alert user to fix Telegram target before relying on cron notifications.

## Workarounds / patterns
- For quota-blocked Codex: schedule after reset time, or fall back to `claude -p` / file handoff.
- For Telegram delivery: use `deliver=local` until chat/token issue is fixed; or run a manual `cronjob action='run ...'` and inspect `last_status` / `last_delivery_error`.

## Time context
- Observed around 2026-07-03 23:53 local.
