# Draftwell (working name)

A writing workspace around the **humaniser** skill. Paste text, pick a writing context, review the rewrite beside the
original, edit it, copy it. The name is temporary: change `BRAND` and `<title>` in `index.html`.

It rewrites for natural, context-appropriate prose and checks that numbers, names, certainty and meaning survive.
It does **not** measure or promise AI-detection results, and it never adds mistakes to seem human.

## Run

```
pip install -r requirements.txt
export ANTHROPIC_API_KEY=...          # required, server-side only
uvicorn app:app --host 127.0.0.1 --port 8000
```

Open http://127.0.0.1:8000. No frontend build step: the UI is one dependency-free `index.html`.

| Variable | Default | Purpose |
|---|---|---|
| `ANTHROPIC_API_KEY` | none | Model credentials. Without it the UI shows a banner and Humanize is disabled. |
| `REWRITE_MODELS` | `claude-sonnet-5-5,claude-haiku-4-5-20251001` | Tried in order; the next is the fallback on provider errors. |
| `DEMO_MODE` | off | Set to `1` to run with no API key. A small rule-based stand-in (not a model) makes simple word swaps, and the UI says so. For exploring the interface and API only. |
| `RATE_LIMIT` | `20` | Requests per client per minute (in memory, per process). |

The first run downloads two small models (`all-MiniLM-L6-v2`, `cross-encoder/nli-deberta-v3-small`) for the
similarity and entailment checks. Without them the app still runs and says so under the output; only the
deterministic checks run.

## How it works

```
index.html  ->  POST /rewrite  ->  service.py (validate, rate limit, error mapping)
                                   core.py   (prompt = ../SKILL.md + fidelity rules + context + options
                                              + optional voice sample; model call; fidelity checks; retry)
```

- **The skill is the engine.** The repo's root `SKILL.md` (v4.0.0, read at runtime; override with `SKILL_PATH`). `core.system()` sends it as the system prompt, then adds the fidelity rules, the writing context,
  the enabled options and an optional voice sample. The skill's "note after the text" line is overridden so the
  API returns text only.
- **Writing contexts** (7) and **options** (6) live in `core.CONTEXTS` and `core.OPTIONS`; the UI reads them from
  `/config`, so adding one is a one-line change.
- **Fidelity checks** run on every paragraph: numbers and names kept, no added certainty or magnitude words
  ("will", "most", "always"...), hedges kept, plus embedding similarity and two-way entailment when the models are
  installed. A failed paragraph is retried up to 3 times with the problem fed back; if it still fails it is kept
  and flagged under "Review notes".
- **Voice sample** (optional) steers rhythm and wording from your own writing. Style never comes from a built-in
  example.

## Tests

```
python test_core.py     # 15 backend tests, model mocked (the FastAPI endpoint test needs fastapi installed)
python test_ui.py       # 46 browser checks (needs Playwright + Chromium), model mocked, real pipeline
python bench.py [file] [context]   # real-model benchmark: similarity, entailment, edit distance, readability, perplexity
```

Mocked tests prove the plumbing, not the quality of real model output. Only `bench.py` and a manual run with a key
exercise the real model.

## Privacy

- Document text is never stored by this app, never written to logs (only sizes and timing are logged), and
  `/rewrite` responses are sent with `Cache-Control: no-store`. Preferences (theme, context, switches) are kept in
  your browser's local storage; text and the voice sample are not.
- Text and any voice sample are sent to the Anthropic API on every request. Check Anthropic's current API data
  retention terms for your account before pasting confidential material.
- The API key stays in the server environment and is never sent to the browser.
- Behind a reverse proxy, rate limiting sees the proxy's address unless you forward the client IP.

## Known limits

- Rate limiting is in memory, so it is per process. Use a shared store for multiple workers.
- Whole-document regenerate only; there is no per-paragraph redo.
- Input is capped at 20,000 characters and a 5,000-character voice sample.
- No accounts, history or export formats beyond `.txt`, by design.
