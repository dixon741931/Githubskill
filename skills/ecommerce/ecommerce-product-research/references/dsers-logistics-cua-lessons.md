# DSERS Logistics Settings — Browser / CUA Lessons (2026-07-09)

Source: session configuring `https://www.dsers.com/application/settings?type=Logistics_Setting` on Windows / cua-driver against the user's logged Chrome.

## Stable Actions
- `get_window_state` is reliable for discovering Advanced Shipping Method controls: country ComboBox, period Spinner, cost Spinner, less day RadioButton.
- `set_value` AXValue writes to the ComboBox/Spinner succeed and the tool returns `✅ Set AXValue on [index]`.
- Current verified target controls on the Advanced block:
  - Country: `rc_select_2`
  - Delivery period: delivery-period Spinner (`value="7"`)
  - Shipping cost: cost Spinner (`value="$ 0"`)
  - Preference radio: `less day`

## Fragile Behaviors
- **Form collapse after SAVE click:** After clicking `SAVE`, Chrome reloads/navigates and the Advanced block collapses. Subsequent `get_window_state` may surface only top-level chrome with the Advanced fields hidden, looking identical to the pre-edit state.
- **Form reset after refresh:** After navigation/refresh, Advanced values revert to previous saved state. There is no visible confirmation toast/element surfaced via UIA in the observed flow.
- **SAVE button state is unverifiable from UIA:** UIA snapshot does not include form-validation status; do not infer save success from the snapshot alone.

## Required Verification Procedure
After pressing SAVE:
1. Re-grab `get_window_state` for the same pid/window_id.
2. If Advanced block fields are missing, click the Advanced Shipping Method row/tab to expand it.
3. Read the visible values via `get_text` or `get_window_state` and confirm:
   - country == `United States`
   - delivery period == `7`
   - cost == `$ 0`
   - preference == `less day`
4. If values did not persist, repeat the field edits and SAVE while the Advanced block is still expanded.

## Fallback Rule
If repeated automated reads cannot verify persistence, do not continue clicking blindly. State the edit targets and ask the user to confirm with one visible read of the Advanced block.
