# Zendrop Windows / cua-driver Workarounds

## Stable navigation pattern
- Use absolute URL in address bar Edit: `https://app.zendrop.com/product?page=1&search=<term>`
- Always `ctrl+a` before typing; read back `value` from a fresh snapshot to avoid concatenation.
- Execute with `return` key press.

## Click reliability
- After every navigation, re-grab `get_window_state` before any element-indexed click.
- Element indices are snapshot-scoped; they shift after page changes.
- Sidebar indices are especially unstable; prefer Back link, Find Products hyperlink value, or address bar navigation.
- For Chrome input/button no-ops: try `background` first; if no state change, retry same element with `delivery_mode: "foreground"` after re-snapshot.

## What to avoid
- Do not rely on `browser_navigate` to Zendrop when a logged Chrome pid exists; it often returns empty page.
- Do not keep retrying the same long-tail keyword if it returns no products; switch to shorter niche nouns.
- Do not scroll the generic Trending/Find Products feed looking for desk items; go straight to search.
- Do not click sidebar items by remembered index after navigation: indices renumber and can open unrelated pages. Always re-snapshot first.

## Click failure modes on Windows Electron targets

Two patterns seen on Zendrop/Chrome:
1. UIA click returns success but does nothing — retry foreground after fresh snapshot.
2. UIA click returns success but opens unrelated UI (user menu, My Products, bookmarks) — same retry path, then verify with address bar `value` or visible page title before repeating.

Observed wrong-target indices after navigation:
- Element 47 sometimes becomes a different element than FindProducts/Trending before search.
- Address bar clicks may land on existing YouTube/new-tab/bookmark behaviors if the Chrome session has unrelated focus state; ensure the target window actually shows Zendrop before retrying.

## UIA write verification

On Zendrop's Electron/Chrome surface, UIA `set_value`/`type_text` often returns success while the renderer ignores the keystrokes. "Sent (unverified)" is not proof.

Reliable sequence:
1. Click address/edit field.
2. `ctrl+a` to select existing content.
3. Type the full URL/search term.
4. Re-grab `get_window_state` and read Edit `value`.
5. If it didn't update, retry with pixel-focus + type, or after a re-snapshot use `delivery_mode: "foreground"` on the same element.
6. Only then press `return`.

## Wrong-page / concatenation hazard

If an Edit still holds an old unrelated value, typing may concatenate onto it. Always do `ctrl+a`, read back `value`, and only then type the full desired absolute value.

## Desktop-scope fallback note

When an element-indexed action is not reliable on Chrome content, desktop-scope pixel click can be used as last resort via `capture_scope: "desktop"`. Prefer window-scoped element index first; desktop-scope loses element context and is only for unstuck Chrome surfaces where element indexes miss.

## Verified short keywords for workstation/desk niche
`monitor stand`, `desk lamp`, `headphone stand`, `cable management`, `desk pad`, `under desk shelf`, `rgb desk mat`, `desk riser`, `usb hub desk`, `phone stand desk`
