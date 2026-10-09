#!/usr/bin/env python3
"""Rewrite every sample with one version of the skill.

Usage: python3 eval/run.py <skill.md> <label> [name-filter] [--model sonnet] [--jobs 6]
Writes runs/<label>/<sample>.md (final text only) and runs/<label>/raw/<sample>.txt.

Needs a logged-in `claude` CLI (set CLAUDE_BIN if it is not on PATH).
"""
import argparse, os, re, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).parent
CLAUDE = os.environ.get("CLAUDE_BIN", "claude")


def body(sample):
    return re.sub(r"\A---\n.*?\n---\n", "", sample.read_text(), flags=re.S).strip()


def prompt_for(sample):
    """prompts/<name>.txt is the canonical prompt; build it if missing. The rewriter never sees the front matter."""
    p = HERE / "prompts" / f"{sample.stem}.txt"
    if not p.exists():
        text = (HERE / "rewrite_prompt.md").read_text().rstrip("\n").replace("{TEXT}", body(sample))
        m = re.search(r"^context: \|\n((?:  .*\n)+)", sample.read_text(), re.M)
        if m:  # a reply: show the thread it answers, as the Slack samples do
            ctx = "\n".join(l[2:] for l in m.group(1).splitlines())
            text = text.replace("<text>", f"It is a reply in this conversation:\n<context>\n{ctx}\n</context>\n\n<text>", 1)
        p.write_text(text)
    return p.read_text()


def call(system, prompt, model):
    cmd = [CLAUDE, "-p", "--system-prompt", system, "--tools", "", "--disable-slash-commands"]
    if model:
        cmd += ["--model", model]
    r = subprocess.run(cmd, input=prompt, capture_output=True, text=True, timeout=600)
    if r.returncode != 0 or "Not logged in" in r.stdout:
        raise RuntimeError(r.stdout + r.stderr)
    return r.stdout


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("skill"); ap.add_argument("label"); ap.add_argument("filter", nargs="?", default="")
    ap.add_argument("--model", default=None); ap.add_argument("--jobs", type=int, default=6)
    a = ap.parse_args()
    system = Path(a.skill).read_text()
    out = HERE / "runs" / a.label
    (out / "raw").mkdir(parents=True, exist_ok=True)
    samples = [s for s in sorted((HERE / "samples").glob("*.md")) if a.filter in s.stem]

    def one(s):
        raw = call(system, prompt_for(s), a.model)
        (out / "raw" / f"{s.stem}.txt").write_text(raw)
        m = re.search(r"<final>\s*(.*?)\s*</final>", raw, re.S)
        (out / f"{s.stem}.md").write_text((m.group(1) if m else raw).strip() + "\n")
        return s.stem, bool(m)

    with ThreadPoolExecutor(a.jobs) as ex:
        for name, ok in ex.map(one, samples):
            print(f"{name}: {'ok' if ok else 'NO <final> TAG, kept raw output'}")


if __name__ == "__main__":
    sys.exit(main())
