# Changelog

## 0.1.0
- Added the writing workspace: two-panel editor, writing-context selector (7), humanization options (6), optional
  voice sample, side-by-side / original / humanized / changes views, word diff with readable merged regions, word and
  character statistics, copy, `.txt` download, replace-with-undo, restore-last-generated, light and dark themes.
- Backend now builds its prompt from the vendored humaniser skill plus fidelity rules, instead of a short generic prompt.
- Added deterministic fidelity checks (added certainty or magnitude words, dropped hedges) alongside numbers/names
  and embedding/entailment checks; checks degrade to deterministic-only when the models are not installed.
- Added request validation, per-client rate limit, timeouts, error mapping, `/config`, `Cache-Control: no-store`.
- Removed: the earlier tone selector (replaced by writing contexts) and per-paragraph redo (replaced by whole-text regenerate).
- Tests: `test_core.py` (backend, mocked model) and `test_ui.py` (browser, mocked model).

## 0.2.0 (unreleased)
- Self-check layers run on every paragraph before output: per-sentence audit (unsupported or new-fact sentences block, dropped source sentences are noted), a second model pass that acts as a strict checker, an originality guard (no 8-word runs from the voice sample or `app/reference/*.txt` unless the source has them), and an AI-tell rate check using `eval/tells.py`. Set `VERIFY=0` to skip the second model pass.
