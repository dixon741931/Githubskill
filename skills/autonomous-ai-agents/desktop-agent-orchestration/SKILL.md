---
name: desktop-agent-orchestration
description: "Orchestrate Claude Code Desktop and Codex CLI from Hermes on Windows. Covers file-based task handoff, direct CLI invocation, sandbox pitfalls, and process monitoring patterns."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [windows]
tags: [Claude, Codex, Windows, PTY, Desktop, orchestration]
---

# Desktop Agent Orchestration — Windows

Use this skill when the user wants Hermes to control Claude Code Desktop or Codex on a Windows machine, especially when tmux is unavailable or unreliable.

## Core Principle

On Windows, **tmux is often unavailable in Hermes desktop sessions**. Do not rely on interactive TUI orchestration as the primary channel.

## Channel 1: File-Based Task Handoff (Preferred on Windows)

### How it works
1. Hermes writes a task to one of the project's shared files.
2. The desktop client reads the file on its next cycle/chunk.
3. The client writes results back.
4. Hermes reads the result.

### Task files to write to
- `TASKS.md` — numbered priorities + acceptance criteria
- `.clinerules.md` — permanent project rules, enforced every run
- `reports/CEO_REPORT.md` — CEO decisions, approval queue
- `memory/ceo_decisions.json` — machine-readable decisions
- Project vault folders, e.g. `DailyFinds_Vault/`

### Task writing format
```markdown
### Task [N]: [clear title]
**Priority:** P0/P1/P2
**Acceptance:** [what done looks like]
**Prompt:** [exact prompt the agent should execute]
```

### When to use
- Claude Code Desktop is already running
- Multi-turn work where state must persist
- User is on Windows without tmux
- You need reliable handoff without PTY gymnastics

## Channel 2: Direct CLI Invocation (Fallback)

### Claude Code print mode
```
terminal(command="claude -p 'task description' --max-turns 5", workdir="/path/to/project", timeout=120)
```

### Codex one-shot
```
terminal(command="codex exec 'task description'", workdir="/path/to/project", pty=true)
```

### Caveats
- `pty=true` is required for Codex.
- `--dangerously-skip-permissions` is unavailable in `claude -p`; print mode skips permission dialogs.
- If `python` symlink is missing on Windows, the first bash command may fail; the agent usually self-corrects.
- Direct invocation is best for simple, single-turn tasks.

## Channel 3: Background Codex (Long Tasks)

```
terminal(command="codex exec --full-auto 'task'", workdir="~/project", background=true, pty=true, notify_on_complete=true)
process(action="poll", session_id="<id>")
process(action="log", session_id="<id>")
```

Use `--sandbox danger-full-access` if bubblewrap/user-namespace errors occur in gateway-driven sessions.

## Hermes Gateway -> Telegram delivery

When the user is on Telegram and asks the desktop agent to do work:
1. Hermes receives the Telegram message.
2. Hermes writes the task to the appropriate file.
3. Hermes replies: "已写入 TASKS.md / Vault，Claude Code 下次执行时会读到。"
4. If the user explicitly asks for immediate execution and the task is simple, use direct CLI invocation.

Do not leave the user hanging with "I cannot control Claude Code" when file-based handoff is available.

## Verification

After writing a task file, confirm:
- Path exists and content was written.
- If direct CLI was used, confirm exit code and captured the output.
- Report back what the agent will do next, not just "task written."

## Channel 1a: Hermes Memory Bridge to Claude Code (Project Root)

When Claude Code / Codex must inherit Hermes long-term memory without repeated prompting:

1. Create `HERMES_CONTEXT.md` at the project root.
2. Structure it with: founder preferences, live project state, non-negotiable rules, API/tool status, current trust/blocked assets, and preferred working directories.
3. In `AGENTS.md`, add a mandatory first-read rule: `HERMES_CONTEXT.md` is read before any code change, ahead of everything else.
4. Add a cron that refreshes `HERMES_CONTEXT.md` from current Hermes memory + latest reports on a schedule appropriate to project velocity.
5. Never put secrets/tokens/API keys in this file.

This is cheaper than re-teaching Claude Code every session and survives platform switches (Telegram ↔ GUI).

## Cross-Platform Session Continuity

Telegram and the Hermes GUI do **not** share live conversation context. Each platform sees only its own messages. If the user switches from Telegram to the GUI mid-task, the new session won't know what the other side already decided.

### Pattern: durable context files

After any nontrivial decision in one channel, write the conclusion to a durable location so the other channel can pick it up:

- `D:\Hermes\memories\MEMORY.md` — session-spanning facts, user preferences, project state
- `reports/CEO_REPORT.md` or `DailyFinds_Vault/01_Strategy/*.md` — project-specific context
- `TASKS.md` — executable next steps

Do not rely on the user restating decisions when they switch platforms.

## Monitoring Claude Desktop Progress

When Claude Code Desktop is running a long task, you need to verify progress without stealing focus. On Windows, minimized windows cannot be screenshot-captured, so rely on the UIA tree snapshot instead.

### Detecting Claude's status from the tree

Look for these signals in `get_window_state` output:
- **Processing**: Text node containing `"Claude is responding"` or `"Claude is thinking"`
- **Finished**: Text node containing `"Claude finished the response"`
- **Tool use**: Buttons with labels like `"Used Claude in Chrome (N actions)"`, `"Ran N commands"`, `"Searched the web"`
- **Active phase**: Text nodes showing `"Using Claude in Chrome…"` or `"Navigating to..."`

Example tree signals from a real session:
```
- Text "Claude is responding"
- Text "Read 4 files, ran an agent"
- Text "Edited 5 files, read a file, created a file"
- Text "Claude finished the response"
- Button "Used Claude in Chrome (28 actions), loaded tools, used 2 tools"
```

### Handling minimized Claude windows

On Windows, `get_window_state` will return `screenshot_error: "cannot capture minimized window"` but the element tree still works. Use the tree only; do not attempt screenshot-based verification on minimized windows.

### Review-first-then-discuss pattern (mandatory)

Per user requirement: when the user asks you to monitor an autonomous agent, do NOT notify or discuss results until you have:
1. Confirmed the agent has stopped working (`"Claude finished the response"`)
2. Reviewed the actual outputs (files edited/created, tool actions taken, deliverables produced)
3. Verified alignment with requirements before raising the topic with the user

Only after the review is complete should you present findings. Do not send celebratory/status notifications midway through an autonomous task unless explicitly asked.

## Shopify / Ecommerce Project Notes

When orchestrating work on `D:\\my_bot`:

- This repo is a Shopify DailyFinds project with a `DailyFinds_Vault/` folder acting as the central brain.
- Product decisions live in `DailyFinds_Vault/01_Strategy/` and `02_Products/`.
- Preferred task handoff path: write to `DailyFinds_Vault/01_Strategy/<date>_<Task>.md`.
- Git remote is usually `origin https://github.com/dixon741931/DD.git`; push after meaningful edits.

## New Pitfalls

13. **Treating Chrome CDP path as universally available on Windows** — `mcp_cua_driver_page` needs a Chrome launched with `--remote-debugging-port=N`; otherwise `click_element` / `execute_javascript` will fail with a CDP/fallback error. Without that port, legacy browser automation can redirect to a Shopify verification page instead of the real admin flow. Detect CDP availability before choosing the browser-action path.

14. **Using `browser_navigate` to Shopify admin from Hermes desktop browser sessions** — it commonly redirects to "Your connection needs to be verified before you can proceed". Prefer reusing the existing authenticated pid/window instead of a fresh navigation.

15. **Scheduling Codex continuation jobs with local-only delivery** — default cron output is not delivered into the Hermes TUI. If the user wants post-run status, set `deliver=telegram` or `deliver=all`, or instruct the one-shot job to write a durable status file under `D:\\my_bot\\.claude\\`.

16. **Guessing Claude Code MCP package names** — socially-trusted names often npm-publish under different names. `claude mcp add <name> -- npx -y <package>` may write config but fail health checks immediately. Before add, verify the package name on npm, or use the user's known-good plugin config from `~/.claude/settings.json` / `enabledPlugins` as the source of truth.

17. **Trusting plugin config without inspecting actual MCP config** — a plugin being enabled in `~/.claude/settings.json` affects plugin behavior, but Claude Code MCP servers are governed separately by `~/.claude.json` `mcpServers`. Adding plugins and adding MCP servers are distinct actions; listing one does not prove the other works.

18. **Treating `computer_use` as time-travel for cron** — `computer_use`/`cua-driver` can only drive the desktop while the parent Hermes session is online. A cron job cannot use them later to type into Codex Desktop or any GUI. For future actions, use a runnable script or API path; do not promise future CUA input. If the user asks `can't you just control my computer at 03:50?`, explain this constraint directly and offer the `codex exec` cron path.

19. **Assuming Codex remote-control daemon works on Windows** — `codex remote-control start` currently fails on Windows with `"only supported on Unix platforms"`. Do not rely on external daemon-based control here.

20. **Codex account quota errors blocking `codex exec`** — if stderr contains `"You've hit your usage limit"` and a recovery timestamp, the run is blocked at provider level, not at CLI/path level. Treat this as a non-retryable session blocker until the reset time or upgrade.

21. **Inline PowerShell quoting breaks in `terminal()`** — on this Windows host, `terminal()` runs bash/MSYS, not PowerShell. `$var`, subexpressions `$(...)`, and here-string lines get mangled by the outer shell. It does not matter whether the command starts with `powershell -NoProfile -Command`; use one of: a `.ps1` file written with `Set-Content`/`write_file` and run via `-File`, escaped `$` via `\$(...)`, or `execute_code` with Python for filesystem work.

22. **Secrets in skill references / public repos** — never commit a real token, key, password, or cookie into a skill `references/` file or any public repo path. Even a single historical commit can trigger GitHub push protection. Use placeholders like `<SHOPIFY_ADMIN_TOKEN>` and describe the format/prefix in prose only. If a past commit already contains a secret, first remove it from the current working tree, then: if GitHub still rejects the push because of history, either rewrite history with `git filter-repo`/BFG and force-push, or use GitHub's unblock link plus rotate the credential.

23. **Treating git status warnings as safe-to-ignore** — LF/CRLF warnings during commit are normal on Windows, but `error: src refspec main does not match any` after `git init` means you created a root commit on `master` while the remote default branch is `main`. Fix with `git branch -M main` before the first push. Truncated `git status` output means the commit/push may not have completed; verify with `git status --short | wc -l` or the final push line.

## Failure Recovery Order for Failing MCP Servers

When `claude mcp list` shows `Failed to connect` for a newly added server:
1. Confirm the package name actually exists on npm.
2. Confirm auth prerequisites: token, login, OAuth, or device code.
3. Run the server command standalone to inspect startup errors.
4. Re-add with corrected command or config; do not keep adding new guesses.

## Reliable Claude Code Plugin/MCP Decision Pattern

Prefer these sources, in order:
1. `claude plugins list` and `claude mcp list` for installed state.
2. `~/.claude/settings.json` for enabled plugins.
3. `npm search <keyword> mcp` or official docs for new additions.
4. Re-add with exact package command; validate with `claude mcp list` before switching projects.

## Verified Package Name Mappings for Claude Code MCP

Trusted names often publish under different npm package names. Before `claude mcp add`, verify via `npm search` or official install docs.

| Desired MCP | Bad guess | Known-good package / install |
|---|---|---|
| Firecrawl | `@firecrawl/mcp-server` | `npx -y firecrawl-mcp` |
| GitHub | `plugin:github` Copilot HTTP | `claude mcp add github -- npx -y @modelcontextprotocol/server-github` with `GITHUB_PERSONAL_ACCESS_TOKEN` |
| Linear | `@linear/mcp-server` | `npx -y @mseep/linear-mcp` or `@hatcloud/linear-mcp` |
| Sentry | may require auth state | `npx -y @sentry/mcp-server`, expects `SENTRY_ACCESS_TOKEN` or device-code login |
| Vercel | `@vercel/mcp-server` | `@robinson_ai_systems/vercel-mcp` or framework adapters |
| Postgres | `@postgres/mcp-server` | `ainative-postgres-mcp` or `@edelciomolina/postgres-mcp` |
| Supabase | `@supabase/mcp-server` | `supabase-mcp` or `@supabase/mcp-utils` |
| Codex CLI | | `npx -y @cexll/codex-mcp-server` |

## Failure Recovery Order for Failing MCP Servers

When `claude mcp list` shows `Failed to connect` for a newly added server:
1. Confirm the package name actually exists on npm.
2. Confirm auth prerequisites: token, login, OAuth, or device code.
3. Run the server command standalone to inspect startup errors.
4. Re-add with corrected command or config; do not keep adding new guesses.

## Notification Reliability for Cron Jobs

`local` delivery does not message the user. `telegram` delivery may fail with the same `Chat not found`/durable-binding issue even when other tasks appear healthy. If the user needs notification reliability:
- stay `local` and inspect via `cronjob action='list'`
- switch to `deliver='all'` only after Telegram routing is verified
- instruct the job to write a durable status file under `D:\\my_bot\\.claude\\` so delivery success/failure is independent of Telegram routing

## Codex Desktop vs Codex CLI

When the user says "Codex Desktop", they mean the Windows GUI app (`Codex.exe`, pid 156952 on this machine), not the `codex exec` CLI.
- `codex remote-control start` is unsupported on Windows.
- `computer_use` cannot be deferred to a future cron run; it only works while the parent Hermes session is online.
- The only reliable future-action path on Windows is a bash wrapper calling `codex exec "..."` from cron.

## Codex One-Shot Job Pattern (Windows)

For "do work at X time via Codex" requests:

1. Write a small bash wrapper under `C:\Users\Administrator\.hermes\scripts\<name>.sh` that `cd`s to the project workdir and runs `codex exec "<task prompt>"`.
2. Create a cron job with:
   - `script=<filename>.sh` relative to `~/.hermes/scripts/`
   - `no_agent=true`
   - `repeat=1`
   - explicit ISO `schedule=` for the requested time
3. If the user wants completion notification, set `deliver=telegram` or `deliver=all`; otherwise tell them output is available via `cronjob action='list'`.

## Shopify / Printify GUI Reality on This Machine

- pid 70428 can provide read-only UIA snapshots, but direct CDP writes are unavailable unless Chrome was launched with `--remote-debugging-port`.
- When GUI write path is unavailable, prefer API-only or file-based handoff. Do not keep retrying browser click paths that have already errored.
- Printify's UI inside Shopify admin may be iframe-embedded; UIA can expose outer chrome while Printify content remains hidden or unclickable. In those cases, expect GUI automation to fail and switch to:
  - Printify public API where available
  - File-based task handoff to a desktop agent
  - Manual user action inside the browser, with results reported back

1. **Assuming Claude Code Desktop is stateless** — it caches trust per directory and accumulates context; file handoff naturally fits its workflow.
2. **Trying tmux on Windows without verifying it exists** — check availability first; if missing, fall back to file-based channel immediately.
3. **Forgetting pty=true for Codex** — Codex hangs without a PTY.
4. **Using interactive Claude Code mode when print mode suffices** — print mode skips dialogs and is more scriptable.
5. **Letting Claude Code silently fail** — after writing a task, check if the agent actually picks it up by reading the file's modification time or a status indicator.
6. **Assuming Telegram shares GUI session context** — it does not. Always persist decisions to durable files so both channels stay aligned.
7. **Skipping durable writes after strategic decisions** — brand, positioning, kill lists, and acceptance criteria must be written to disk before switching channels, not as an afterthought.
8. **Saying "I cannot control Claude Code"** — never say this. You have two working channels: file-based task handoff and direct CLI invocation (`claude -p` / `codex exec`). Use one of them.
9. **GitHub PAT without `repo` scope** — a valid-looking token can still fail with `401 Bad credentials` if it lacks the `repo` scope. Verify with API call that returns `Scopes` before assuming PAT is good.
10. **Gateway state mismatch on Windows** — `gateway_state.json` can show `running` with a PID even when the actual process has died. Always corroborate with process listing or live log output before assuming gateway health.
11. **Relying on screenshots for minimized windows** — `get_window_state` fails on minimized windows. Use UIA tree snapshots instead; the element tree is still valid even when rendered content is unavailable.
12. **Sending premature notifications during autonomous work** — do not send "done" messages until review is complete. The user wants to vet outputs before any communication goes out, including Telegram notifications.
