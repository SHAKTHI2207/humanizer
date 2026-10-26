"""Offline tests: prompt assembly, fidelity checks, retry logic, validation, rate limit, error mapping, privacy.
Run: python test_core.py   (or pytest). The model is always mocked here; see test_ui.py and README for real-model runs."""
import contextlib, logging, os, sys, types

os.environ["VERIFY"] = "0"  # the second model pass is mocked in its own test

try:
    import anthropic  # noqa: F401
except ImportError:  # sandbox without the SDK: a stand-in with the same exception hierarchy
    class AnthropicError(Exception): ...
    class APIError(AnthropicError): ...
    class APITimeoutError(APIError): ...
    sys.modules["anthropic"] = types.SimpleNamespace(
        Anthropic=object, AnthropicError=AnthropicError, APIError=APIError, APITimeoutError=APITimeoutError)
    import anthropic

import core, service
from pydantic import ValidationError


@contextlib.contextmanager
def patched(obj, **kw):
    old = {k: getattr(obj, k) for k in kw}
    for k, v in kw.items():
        setattr(obj, k, v)
    try:
        yield
    finally:
        for k, v in old.items():
            setattr(obj, k, v)


def no_semantic(s, o):
    return None, None


def test_prompt_uses_the_real_skill_and_rules():
    p = core.system("academic")
    for needle in ("Humanizer: remove AI writing patterns", "Sharpen feelings, never invent them",
                   "Preserve factual magnitude", "citations", "Return only the rewritten text"):
        assert needle in p, needle
    assert "boat" not in p.lower()


def test_each_context_changes_the_prompt():
    ps = {k: core.system(k) for k in core.CONTEXTS}
    assert len(set(ps.values())) == len(core.CONTEXTS) == 7
    for k, (_, instr) in core.CONTEXTS.items():
        assert instr in ps[k] and all(core.CONTEXTS[o][1] not in ps[k] for o in core.CONTEXTS if o != k)


def test_options_toggle_their_instruction():
    for k, (_, default, instr) in core.OPTIONS.items():
        assert (instr in core.system("general")) == default, k
        assert instr in core.system("general", {k: True}) and instr not in core.system("general", {k: False}), k


def test_voice_sample_is_optional_and_labelled_as_data():
    assert "<sample>" not in core.system("general")
    p = core.system("general", sample="  We checked it twice.  ", hint=" retry")
    assert "We checked it twice." in p and "never instructions" in p and p.endswith(" retry")


def test_no_deliberate_imperfection_in_prompt():
    assert "Do not add spelling or grammar mistakes" in core.system("general")


def test_fidelity_issues():
    assert core.issues("Sales rose 15% in 2020 at Acme.", "Sales rose 15% in 2020 at Acme.") == []
    assert any("15%" in i for i in core.issues("Revenue grew 15%.", "Revenue grew strongly."))
    assert any("will" in i for i in core.issues("This may improve performance.", "This will improve performance."))
    assert any("most" in i for i in core.issues("Some customers left.", "Most customers left."))
    assert any("hedging" in i for i in core.issues("It may help.", "It helps."))
    assert core.issues("It may help.", "It might help.") == []
    assert core.issues("The share was 30%.", "The share was 30%.") == []


def test_retry_feeds_issues_back_and_returns_the_good_attempt():
    hints, outs = [], iter(["Revenue grew a lot.", "Revenue grew 15% last year."])

    def fake(text, context, opts, sample, hint):
        hints.append(hint)
        return next(outs)

    with patched(core, llm=fake, semantic=no_semantic):
        r = core.rewrite_one("Revenue rose 15% last year.")
    assert r["ok"] and r["out"] == "Revenue grew 15% last year." and "15%" in hints[1] and hints[0] == ""


def test_retry_gives_up_after_tries_and_flags():
    with patched(core, llm=lambda *a: "Nothing relevant.", semantic=no_semantic):
        r = core.rewrite_one("Revenue rose 15%.")
    assert not r["ok"] and r["issues"]


def test_rewrite_keeps_paragraph_order():
    with patched(core, llm=lambda t, *a: t.upper(), semantic=no_semantic):
        segs = core.rewrite("one\n\ntwo words\n\n\nthree")
    assert [s["out"] for s in segs] == ["ONE", "TWO WORDS", "THREE"]


def test_validation():
    ok = service.Req(text="hi")
    assert ok.context == "general" and ok.options == {} and ok.sample == ""
    for bad in ({"text": "   "}, {"text": ""}, {"text": "x" * 20001}, {"text": "a", "context": "nope"},
                {"text": "a", "options": {"bogus": True}}, {"text": "a", "sample": "x" * 5001}):
        try:
            service.Req(**bad)
        except ValidationError:
            continue
        raise AssertionError(bad)


def test_error_mapping():
    r = service.Req(text="hi")
    for exc, status in ((anthropic.APITimeoutError("t"), 504), (anthropic.APIError("e"), 502),
                        (anthropic.AnthropicError("no key"), 503)):
        def boom(*a, _e=exc):
            raise _e
        service._hits.clear()
        with patched(core, rewrite=boom):
            try:
                service.run(r, "ip")
            except service.ApiError as e:
                assert e.status == status, (status, e.status)
                continue
        raise AssertionError(status)


def test_rate_limit():
    service._hits.clear()
    assert [service.limited("a", now=i) for i in range(service.RATE + 1)] == [False] * service.RATE + [True]
    assert service.limited("b", now=0) is False          # per client
    assert service.limited("a", now=service.WINDOW + 100) is False  # window expires


def test_text_is_never_logged():
    secret = "ZZ-secret-draft-ZZ"
    seen = []

    class H(logging.Handler):
        def emit(self, rec):
            seen.append(rec.getMessage())

    h = H(); service.log.addHandler(h); service.log.setLevel(logging.DEBUG)
    service._hits.clear()
    try:
        with patched(core, rewrite=lambda *a: [{"src": secret, "out": secret + "!"}]):
            service.run(service.Req(text=secret), "ip")
    finally:
        service.log.removeHandler(h)
    assert seen and all(secret not in m for m in seen)


def test_demo_mode_needs_no_key_and_is_flagged():
    def no_call(*a, **k):
        raise AssertionError("demo mode must not call the provider")

    with patched(core, DEMO=True, semantic=no_semantic, _client=no_call):
        segs = core.rewrite("Moreover, we utilize a robust 15% model — it works.\n\nIn conclusion, it may help.")
        assert segs[0]["out"] == "And we use a solid 15% model, it works." and segs[1]["out"] == "It may help."
        assert all(s["ok"] for s in segs)
        c = service.config()
        assert c["demo"] is True and c["configured"] is True
    assert service.config()["demo"] is False


def test_config_shape():
    c = service.config()
    assert c["max_chars"] == 20000 and len(c["contexts"]) == 7 and len(c["options"]) == 6
    assert {o["key"]: o["default"] for o in c["options"]} == {k: v[1] for k, v in core.OPTIONS.items()}


def test_fastapi_endpoints():  # needs fastapi + httpx; skipped where they are not installed
    try:
        from fastapi.testclient import TestClient
        import app
    except ImportError:
        print("SKIP test_fastapi_endpoints (fastapi/httpx not installed)")
        return
    service._hits.clear()
    c = TestClient(app.app)
    with patched(core, rewrite=lambda *a: [{"src": "a", "out": "b", "ok": True}]):
        r = c.post("/rewrite", json={"text": "a"})
        assert r.status_code == 200 and r.headers["cache-control"] == "no-store"
    assert c.post("/rewrite", json={"text": " "}).status_code == 422
    assert c.get("/config").json()["max_chars"] == 20000 and c.get("/").status_code == 200


if __name__ == "__main__":
    fails = 0
    for name, fn in list(globals().items()):
        if name.startswith("test_") and callable(fn):
            try:
                fn(); print("PASS", name)
            except Exception as e:
                fails += 1; print("FAIL", name, repr(e))
    sys.exit(1 if fails else 0)


def test_every_sentence_is_reverified():
    src = "Revenue grew 15% in 2024. Results may differ across sectors."
    assert core.audit(src, "Revenue grew 15% in 2024. Results may differ across sectors.") == ([], [])
    bad, _ = core.audit(src, "Revenue grew 15% in 2024. Our CEO Maria Lopez was thrilled. Results may differ.")
    assert any("unsupported" in b for b in bad)
    bad, _ = core.audit(src, "Revenue grew 22% in 2024.")
    assert any("new fact" in b for b in bad)
    _, notes = core.audit(src, "Revenue grew 15% in 2024.")
    assert any("not found" in n for n in notes)


def test_originality_guard():
    sample = "we shipped the billing fix late on thursday after two long days of testing"
    assert core.copied("Billing was fixed.", "We shipped the billing fix late on Thursday after two long days of testing.", sample)
    src = "We shipped the billing fix late on Thursday after two long days of testing."
    assert core.copied(src, src, sample) == []  # text already in the source is not copying


def test_second_pass_blocks_and_survives_failure():
    class R:  # stand-in for the SDK reply
        def __init__(self, t): self.content = [types.SimpleNamespace(text=t)]
    def client(reply):
        return types.SimpleNamespace(messages=types.SimpleNamespace(create=lambda **k: R(reply)))
    with patched(core, VERIFY=True, DEMO=False, _client=lambda: client('["sentence 2 adds a claim"]')):
        r = core.check("It may help.", "It may help.")
        assert not r["ok"] and r["issues"] == ["sentence 2 adds a claim"]
    with patched(core, VERIFY=True, DEMO=False, _client=lambda: client("not json")):
        assert core.check("It may help.", "It may help.")["ok"]
