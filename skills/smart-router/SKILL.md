---
name: smart-router
description: AI routing rules for Hermes + Claude Code + Codex collaboration. Decides which agent should execute a task to minimize tokens, avoid retries, and respect Windows constraints.
version: 1.0.0
author: Hermes Agent
license: MIT
triggers:
  - task delegation
  - routing
  - which agent should do this
  - save tokens
  - claude vs codex
  - cheapest path
---

# Smart Router — Claude / Codex / Hermes Collaboration

## Core Rule

**Never run duplicate work across three AI.** Always route each task to the cheapest valid path first.

---

## Routing Decision Tree

```
Is the task purely knowledge/decision/memory/analysis?
  └─ YES → Hermes answers directly. DONE. Lowest token cost.

Does the task require editing files, code, or a repo on disk?
  └─ YES → Route to AGENT below.

Which agent is currently available?
  ├─ Hermes is already in context → Hermes does it if safe and small.
  ├─ Codex CLI is available AND not quota-blocked → Codex.
  └─ Claude Code is available → Claude Code.

There are exceptions (see below).
```

---

## Exceptions — Override Routing

| Condition | Route To | Reason |
|---|---|---|
| Long-running batch / multi-file refactor | Codex (CLI or Desktop) | Better at sustained code work |
| Project-specific context required | Claude Code | Reads AGENTS.md / HERMES_CONTEXT.md |
| Task needs Shopify Admin API / Telegram / Browser automation | Hermes | Hermes owns these channels |
| Codex is quota-blocked (`usage limit`) | Claude Code or Hermes | Don't retry blocked path |
| User explicitly named an agent | Named agent | User intent wins |
| Ambiguous task, <5 tool calls | Hermes | Cheaper to do inline |
| Task needs verification + review before acting | Hermes orchestrates, delegates execution | Hermes is the CEO |

---

## Token-Saving Rules

1. **Hermes answers questions** — Claude/Codex do NOT answer questions from the user.
2. **Hermes does orchestration** — no extra agent is spawned unless the task exceeds Hermes inline capacity.
3. **File handoff is the default on Windows** — `TASKS.md`, `HERMES_CONTEXT.md`, `reports/CEO_REPORT.md`.
4. **Same task must not be sent to two agents simultaneously** — one owner per task.
5. **Retry blocked paths once, then route** — if Codex is quota-blocked, don't keep retrying; switch immediately.

---

## Shared Context Files

All three AI must read these before doing project work:

- `D:\my_bot\HERMES_CONTEXT.md` — founder prefs, project state, non-negotiable rules
- `D:\my_bot\ALL_PROJECTS_SYNC.md` — active projects, current status, decisions
- `D:\my_bot\DailyFinds_Vault\01_Strategy\*.md` — Shopify/product strategy
- `DailyFinds_Vault/01_Strategy/TASKS.md` — current task queue with acceptance criteria

Write results back to:
- `reports/CEO_REPORT.md` — strategic decisions, approval queue
- `TASKS.md` — number priorities + acceptance criteria

---

## Hermes Role (Router + CEO)

Hermes is **not** a default executor for coding work. Hermes:

1. Reads requests and classifies them
2. Decides the cheapest path using this skill
3. Writes task files if the work goes to Claude Code / Codex
4. Verifies outputs before reporting to the user
5. Updates `ALL_PROJECTS_SYNC.md` after meaningful work

Hermes should **not**:

- Spawn subagents for trivial tasks (1-2 tool calls)
- Re-delegate already-routed tasks
- Send the same prompt to multiple agents

---

## Claude Code Role

Claude Code runs when:

- Project context (`AGENTS.md`, `HERMES_CONTEXT.md`) is required
- The task needs multi-file understanding
- Codex is unavailable or blocked
- Task was explicitly routed to Claude by Hermes

Claude Code:

- Reads `HERMES_CONTEXT.md` and `ALL_PROJECTS_SYNC.md` before code changes
- Writes results to the same shared files
- Does NOT make live Shopify publishing decisions without CEO_REPORT sign-off

---

## Codex Role

Codex runs when:

- Task is a well-defined coding batch
- Long-running work where Codex's context window is advantageous
- File handoff via `TASKS.md` is already in place
- Codex is NOT quota-blocked

Codex:

- Follows `TASKS.md` exactly
- Does NOT bypass DailyFindUSA OS owner restrictions
- Reports back via file edits + completion summary

---

## Windows Caching Tip

After Codex or Claude Code finishes a large run:

```bash
# Hermes can run these once, no agent needed
python -c "import shutil; [shutil.rmtree(p, ignore_errors=True) for p in [
    r'C:\Users\Administrator\AppData\Local\Temp',
    r'C:\Users\Administrator\.cache\codex-runtimes',
    r'C:\Users\Administrator\.claude\cache'
]]"
```

Avoids redundant cache-cleanup prompts later.

---

## Fallback Priority

When in doubt about which agent to use:

1. Hermes inline (cheapest)
2. File handoff to Claude Code or Codex
3. Direct CLI invocation (`claude -p` or `codex exec`)
4. Report blocker to user if no path works

---

## Anti-Patterns

| Anti-Pattern | Correct Pattern |
|---|---|
| "I cannot control Claude Code" | File handoff + direct CLI |
| Routing every task to Codex | Route to Hermes first if inline is cheaper |
| Running the same task in Hermes + Codex + Claude simultaneously | Single owner per task |
| Ignoring Codex quota errors and retrying 5x | 1 retry, then route to Claude or Hermes |
| Forgetting to update `ALL_PROJECTS_SYNC.md` after decisions | Always update after non-trivial work |
| Re-listing options after the user replied with a number | Execute the chosen option immediately |
| Asking "which one?" when user said "全部" | Run the full listed batch |
| Using inline PowerShell when `$` can get mangled | Prefer Python/execute_code for file ops; avoid PowerShell one-liners with `$` in terminal |
| Blindly rerunning a failed git branch push | Read the exact error first; `git push -u origin main` after mismatch |
