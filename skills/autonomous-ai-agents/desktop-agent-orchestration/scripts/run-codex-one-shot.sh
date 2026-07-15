#!/usr/bin/env bash
set -euo pipefail
cd /d/my_bot
codex exec "Read D:/my_bot/.claude/COWORK_Brief_PRINTIFY_RESET.md and continue the DailyFinds Printify relist work from where it left off. Work in /d/my_bot. If GUI action is needed, use available cua-driver / browser tools. Do NOT stop at planning; execute the next concrete step and save a concise status report to /d/my_bot/.claude/COWORK_STATUS_$(date +%Y%m%d_%H%M%S).md"
