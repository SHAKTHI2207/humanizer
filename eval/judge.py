#!/usr/bin/env python3
"""Blind pairwise comparison of two runs, judged in both orders.

Usage: python3 eval/judge.py <labelA> <labelB> [name-filter] [--model opus] [--jobs 6]
Each sample is judged twice with X and Y swapped, by separate calls. A version wins a sample
only if it wins both orders; a split counts as a tie, which cancels position bias.
Writes blind/<A>-vs-<B>/judgments.json and prints the tally.
"""
import argparse, json, random, re, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from run import HERE, call


def verdict(raw):
    m = re.search(r"\{[^{}]*\}", raw, re.S)
    return json.loads(m.group(0)) if m else {"human": "tie", "faithful": "tie", "why": "unparsed: " + raw[:200]}


def tally(results, a, b):
    """results: {sample: [order1, order2]} with each order {"human": "a"|"b"|"tie", ...} after unblinding."""
    out = {}
    for q in ("human", "faithful"):
        c = {a: 0, b: 0, "tie": 0}
        for pair in results.values():
            v = {r[q] for r in pair}
            c[v.pop() if len(v) == 1 else "tie"] += 1
        out[q] = c
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("a"); ap.add_argument("b"); ap.add_argument("filter", nargs="?", default="")
    ap.add_argument("--model", default=None); ap.add_argument("--jobs", type=int, default=6)
    args = ap.parse_args()
    system = (HERE / "judge_prompt.md").read_text()
    ra, rb = HERE / "runs" / args.a, HERE / "runs" / args.b
    names = sorted(p.stem for p in ra.glob("*.md") if (rb / p.name).exists() and args.filter in p.stem)
    out = HERE / "blind" / f"{args.a}-vs-{args.b}"
    out.mkdir(parents=True, exist_ok=True)
    jobs = [(n, order) for n in names for order in (0, 1)]

    def one(job):
        n, order = job
        x, y = (ra, rb) if order == 0 else (rb, ra)
        prompt = (f"## Original\n\n{(HERE / 'samples' / f'{n}.md').read_text()}\n\n"
                  f"## Rewrite X\n\n{(x / f'{n}.md').read_text()}\n\n## Rewrite Y\n\n{(y / f'{n}.md').read_text()}")
        v = verdict(call(system, prompt, args.model))
        unblind = {"X": x.name, "Y": y.name, "tie": "tie"}
        return n, {"human": unblind.get(v.get("human"), "tie"), "faithful": unblind.get(v.get("faithful"), "tie"),
                   "why": v.get("why", ""), "x_was": x.name}

    results = {}
    with ThreadPoolExecutor(args.jobs) as ex:
        for n, r in ex.map(one, jobs):
            results.setdefault(n, []).append(r)
    (out / "judgments.json").write_text(json.dumps(results, indent=1))
    print(json.dumps(tally(results, args.a, args.b), indent=1))


if __name__ == "__main__":
    sys.exit(main())
