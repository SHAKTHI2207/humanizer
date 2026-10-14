# Provenance

## Original contributions (this application)
`core.py`, `service.py`, `app.py`, `index.html`, `bench.py`, `test_core.py`, `test_ui.py`, this documentation.
Written with Claude (Anthropic) in a Claude Code session. The fidelity rules in `core.FIDELITY` restate the project
brief's rules; the deterministic checks (`issues()`) are new.

## Engine
Nothing is vendored. `core.py` reads the repo's root `SKILL.md` (MIT, derived from blader/humanizer by Siqi Chen; see the root `LICENSE` and `PROVENANCE.md`) at runtime.

## External dependencies (licenses not verified here)
FastAPI, Uvicorn, Pydantic, Anthropic Python SDK, sentence-transformers (`all-MiniLM-L6-v2`), Transformers
(`cross-encoder/nli-deberta-v3-small`), PyTorch; Playwright for tests.
