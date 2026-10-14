"""Browser tests (Playwright + Chromium) against a local stdlib server that runs the REAL service/prompt/fidelity
pipeline with the MODEL MOCKED. This proves the UI and plumbing, not the quality of real model output.
Run: python test_ui.py [screenshot_dir]"""
import glob, json, os, sys, threading, time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

os.environ["RATE_LIMIT"] = "1000"
os.environ.setdefault("ANTHROPIC_API_KEY", "test-not-real")
import test_core  # noqa: F401  (installs the SDK stand-in if needed)
import anthropic, core, service

ROOT = Path(__file__).parent
SHOTS = Path(sys.argv[1]) if len(sys.argv) > 1 else None
CALLS = []


def fake_llm(text, context="general", opts=None, sample="", hint=""):
    CALLS.append({"text": text, "context": context, "opts": opts, "sample": sample})
    if "[[fail]]" in text:
        raise anthropic.APIError("boom")
    if "[[timeout]]" in text:
        raise anthropic.APITimeoutError("slow")
    if "[[slow]]" in text:
        time.sleep(2.5)
    return (text.replace("utilize", "use").replace("In conclusion, ", "").replace("[[slow]]", "")
            .replace("Moreover, ", "And ").strip())


core.llm = fake_llm
core.semantic = lambda s, o: (None, None)  # models not installed here: deterministic checks only


class H(BaseHTTPRequestHandler):
    def log_message(self, *a): pass

    def send(self, code, body, ctype="application/json"):
        b = body if isinstance(body, bytes) else json.dumps(body).encode()
        self.send_response(code); self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(b))); self.end_headers(); self.wfile.write(b)

    def do_GET(self):
        if self.path == "/config":
            self.send(200, service.config())
        else:
            self.send(200, (ROOT / "index.html").read_bytes(), "text/html; charset=utf-8")

    def do_POST(self):
        raw = self.rfile.read(int(self.headers["Content-Length"]))
        try:
            self.send(200, service.run(service.Req(**json.loads(raw)), "t"))
        except service.ApiError as e:
            self.send(e.status, {"detail": e.msg})
        except Exception:
            self.send(422, {"detail": []})


srv = ThreadingHTTPServer(("127.0.0.1", 0), H)
threading.Thread(target=srv.serve_forever, daemon=True).start()
URL = f"http://127.0.0.1:{srv.server_address[1]}/"

DOC = ("Moreover, we utilize a panel of 1,200 firms. Revenue grew 15% in 2024.\n\n"
       "In conclusion, results may differ across sectors.")
results = []


def check(name, cond, detail=""):
    results.append((name, bool(cond)))
    print(("PASS " if cond else "FAIL ") + name + (f"  [{detail}]" if detail and not cond else ""))


def go(page, trigger):
    """Run an action that starts a request, then wait until that request has finished."""
    n = len(CALLS)
    trigger()
    t = time.time()
    while len(CALLS) == n and time.time() - t < 10:
        time.sleep(0.02)
    page.wait_for_function("document.getElementById('spin').hidden && !document.getElementById('hum').disabled")


def main():
    from playwright.sync_api import sync_playwright
    exe = (glob.glob("/opt/pw-browsers/chromium-*/chrome-linux/chrome") + [None])[0]
    with sync_playwright() as pw:
        br = pw.chromium.launch(executable_path=exe, args=["--no-sandbox"])
        ctx = br.new_context(viewport={"width": 1366, "height": 800}, permissions=["clipboard-read", "clipboard-write"])
        page = ctx.new_page()
        errors = []
        page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.goto(URL)
        page.wait_for_function("document.querySelectorAll('#ctx option').length === 7")

        # empty state
        check("empty: humanize disabled", page.is_disabled("#hum"))
        check("empty: placeholder invites input", "Paste or type" in page.get_attribute("#src", "placeholder"))
        check("seven contexts and six switches", page.locator("#switches input").count() == 6)

        # stats + success
        page.fill("#src", DOC)
        check("input word count", page.inner_text("#sw") == str(len(DOC.split())), page.inner_text("#sw"))
        check("input char count", page.inner_text("#sc").replace(",", "") == str(len(DOC)))
        page.select_option("#ctx", "business")
        go(page, lambda: page.click("#hum"))
        o = page.input_value("#out")
        check("output generated through real pipeline", "use a panel of 1,200" in o and "Moreover" not in o, o)
        check("original untouched", page.input_value("#src") == DOC)
        check("paragraphs kept", o.count("\n\n") == 1)
        check("output stats", page.inner_text("#ow") == str(len(o.split())))
        check("context and options reached the backend",
              CALLS[-1]["context"] in ("business",) and CALLS[-1]["opts"]["voice"] is True and CALLS[-1]["opts"]["formality"] is False)
        page.screenshot(path=str(SHOTS / "desktop-light.png")) if SHOTS else None

        # editing, restore, regenerate guard
        page.fill("#out", o + " My own edit.")
        check("restore enabled after edit", page.is_enabled("#restore"))
        page.click("#regen")
        check("regenerate asks before discarding edits", page.is_visible("#confirm"))
        page.click("#confirm button[value=cancel]")
        check("edits kept after cancel", page.input_value("#out").endswith("My own edit."))
        page.click("#restore")
        check("restore brings back generated text", page.input_value("#out") == o)
        page.fill("#out", o + " Edit two.")
        go(page, lambda: (page.click("#hum"), page.click("#confirm button[value=ok]")))
        check("regenerate after confirm replaces edits", "Edit two." not in page.input_value("#out"))

        # copy + replace/undo
        page.click("#copy")
        page.wait_for_function("document.getElementById('toast').textContent.includes('Copied')")
        check("copy toast", True)
        check("clipboard holds output", page.evaluate("navigator.clipboard.readText()") == page.input_value("#out"))
        out_now = page.input_value("#out")
        page.click("#replace")
        check("replace is explicit and copies output", page.input_value("#src") == out_now)
        page.click("#undo")
        check("undo restores original", page.input_value("#src") == DOC)

        # views + diff
        page.click("#views button[data-view=changes]")
        check("changes view highlights", page.locator("#diff ins").count() > 0 and page.locator("#diff del").count() > 0)
        check("changes count shown", "change" in page.inner_text("#chg"))
        page.screenshot(path=str(SHOTS / "desktop-changes.png")) if SHOTS else None
        page.click("#views button[data-view=original]")
        check("original-only view hides output", not page.is_visible("#pOut") and page.is_visible("#pSrc"))
        page.click("#views button[data-view=humanized]")
        check("humanized-only view hides original", page.is_visible("#pOut") and not page.is_visible("#pSrc"))
        page.click("#views button[data-view=split]")

        # keyboard shortcut
        n = len(CALLS)
        go(page, lambda: (page.focus("#src"), page.keyboard.press("Control+Enter")))
        check("Ctrl+Enter humanizes", len(CALLS) == n + 2)  # two paragraphs, one call each

        # errors: provider failure, timeout, retry, source preserved
        page.fill("#src", "Please fix [[fail]] this.")
        page.click("#hum")
        page.wait_for_selector("#err:not([hidden])")
        check("provider error explained", "provider returned an error" in page.inner_text("#errMsg"))
        check("source kept on error", page.input_value("#src") == "Please fix [[fail]] this.")
        page.fill("#src", "Please fix [[timeout]] this.")
        page.click("#retry")
        page.wait_for_function("document.querySelector('#errMsg').textContent.includes('too long')")
        check("model timeout explained with retry", page.is_visible("#retry"))
        page.fill("#src", "All good now.")
        page.click("#retry")
        page.wait_for_function("document.querySelector('#status').textContent.startsWith('Done')")
        check("retry succeeds and clears the error", page.is_hidden("#err"))

        # loading + cancel
        page.fill("#src", "A [[slow]] request.")
        page.click("#hum")
        page.wait_for_selector("#cancel:not([hidden])")
        page.wait_for_timeout(100)
        check("loading state: spinner, busy, inputs locked", page.is_visible("#spin") and page.is_disabled("#hum") and
              page.get_attribute("#src", "readonly") is not None)
        page.click("#cancel")
        page.wait_for_function("document.querySelector('#status').textContent === 'Cancelled'")
        check("cancel keeps the source", page.input_value("#src") == "A [[slow]] request." and page.is_enabled("#hum"))

        # network failure
        page.route("**/rewrite", lambda r: r.abort())
        page.fill("#src", "Offline test.")
        page.click("#hum")
        page.wait_for_selector("#err:not([hidden])")
        check("network failure message", "Could not reach the server" in page.inner_text("#errMsg") and page.is_visible("#retry"))
        page.unroute("**/rewrite")

        # limits, clear confirm, options
        page.fill("#src", "x" * 20001)
        check("over-limit disables humanize and says so", page.is_disabled("#hum") and "Over the limit" in page.inner_text("#over"))
        page.fill("#src", "y" * 300)
        page.click("#clear")
        check("clearing substantial text asks first", page.is_visible("#confirm"))
        page.click("#confirm button[value=ok]")
        page.wait_for_function("document.getElementById('src').value === ''")
        check("cleared", True)
        page.click("#undo")
        check("clear is undoable", page.input_value("#src") == "y" * 300)
        page.fill("#src", "Voice test.")
        page.click("#menu summary")
        page.fill("#sample", "We shipped it late, honestly.")
        page.locator("#switches input[data-key=formality]").check()
        page.screenshot(path=str(SHOTS / "desktop-options.png")) if SHOTS else None
        page.keyboard.press("Escape")
        go(page, lambda: (page.focus("#src"), page.keyboard.press("Control+Enter")))
        check("voice sample and switch sent", CALLS[-1]["sample"] == "We shipped it late, honestly." and CALLS[-1]["opts"]["formality"] is True)

        # keyboard focus visibility + accessibility basics
        page.focus("#hum")
        check("focus ring on buttons", page.evaluate("getComputedStyle(document.activeElement).boxShadow") != "none")
        names = page.evaluate("[...document.querySelectorAll('button.icon')].every(b => b.getAttribute('aria-label'))")
        check("icon buttons are labelled", names)
        # the browser itself logs "Failed to load resource" for the 502/504/aborted requests this test triggers on purpose
        real = [e for e in errors if "Failed to load resource" not in e]
        check("no script or console errors", not real, str(real))

        # theme + responsive
        page.click("#theme")
        check("theme switches", page.evaluate("document.documentElement.dataset.theme") in ("dark", "light"))
        page.fill("#src", DOC)
        go(page, lambda: page.click("#hum"))
        page.screenshot(path=str(SHOTS / "desktop-dark.png")) if SHOTS else None
        for w, h, tag in ((820, 1000, "tablet"), (390, 844, "phone")):
            page.set_viewport_size({"width": w, "height": h})
            page.wait_for_timeout(150)
            check(f"{tag}: no horizontal scroll", page.evaluate("document.documentElement.scrollWidth <= window.innerWidth"))
            check(f"{tag}: panels stacked", page.evaluate("document.querySelector('#pOut').getBoundingClientRect().top >= document.querySelector('#pSrc').getBoundingClientRect().bottom - 1"))
            page.screenshot(path=str(SHOTS / f"{tag}.png"), full_page=True) if SHOTS else None

        # diff unit checks (pure functions in the page)
        ch = page.evaluate("chunks(diffOps(toks('the old cat sat on the mat'), toks('the new cat sat on a mat')))")
        regions = [c for c in ch if "del" in c]
        check("diff: small gaps merged into readable regions", len(regions) == 2 and regions[0]["del"] == ["old"] and regions[0]["ins"] == ["new"], str(ch))
        check("diff: identical text has no changes", all("eq" in c for c in page.evaluate("chunks(diffOps(toks('a b'), toks('a b')))")))
        br.close()


if __name__ == "__main__":
    if SHOTS:
        SHOTS.mkdir(parents=True, exist_ok=True)
    main()
    bad = [n for n, ok in results if not ok]
    print(f"\n{len(results) - len(bad)}/{len(results)} passed")
    sys.exit(1 if bad else 0)
