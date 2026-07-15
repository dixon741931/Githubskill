# GitHub Push Protection — observed behavior and safe recovery

GitHub may block a push with `GH013: Repository rule violations found` / `Push cannot contain secrets` even after the offending file is edited in the working tree, because the secret still exists in earlier commit history.

## Recovery options
1. **Preferred: history rewrite**
   - Install `git filter-repo` or BFG.
   - Remove the secret from all history.
   - Force-push cleaned history.
   - Rotate the exposed credential afterwards.

2. **Quick: GitHub unblock link**
   - Use the URL from the push rejection message.
   - Approve the push despite the secret.
   - Still rotate the credential afterwards; this path only bypasses the block, it does not clean history.

3. **Nuclear: new empty repo**
   - Create a fresh repo with no history.
   - Re-add only sanitized files.
   - Fast when the contaminated history is small and the skill set is small.

## Prevention
- Skill `references/` files and public repo docs must never contain live tokens.
- Use placeholders (`<SHOPIFY_ADMIN_TOKEN>`) and describe format/prefix in prose only.
- Before onboarding skill files to a public repo, scan for known secret prefixes: `shpat_`, `shpca_`, `shpss_`, `ghp_`, `gho_`, `sk-`, `AKIA`, etc.
