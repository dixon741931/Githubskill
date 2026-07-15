# GitHub Auto-publish for Hermes Skills

## Verified repo on this machine
- Remote: `https://github.com/dixon741931/DD.git`
- Working tree: `D:/my_bot`
- Default branch: `master`

## Recommended layout inside repo
- `D:/my_bot/github-skills/` — mirror of `D:/Hermes/skills/`
- Optionally keep class-level skill docs under `D:/my_bot/github-skills/<skill>/`
- A thin `README.md` in repo root explaining this is the user's shared AI skills library; include categories and a link back to the original skill docs/vault paths if needed

## Commit + push rules (owner-approved cache-cleanup/auto schema)
- Only commit skill docs/readme; never include secrets or local caches.
- Group changes into one commit when possible.
- If something fails, report the exact command/output instead of retrying blindly.

## Future automatable path
- A scheduled shell wrapper under `~/.hermes/scripts/` can:
  - diff `D:/Hermes/skills/` against `D:/my_bot/github-skills/`
  - copy changed/new skills
  - commit and push
- Do not auto-run until owner explicitly approves live GitHub publishing from this side.
