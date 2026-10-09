#!/usr/bin/env python3
"""Blind pair files for judges that are not driven by judge.py (for example, agent judges).

  python3 eval/blind_pairs.py make <labelA> <labelB> --keydir DIR
      Writes blind/<A>-vs-<B>/order0.md and order1.md. X and Y are shuffled per sample in order0
      and swapped in order1. The key goes to DIR (keep it away from the judges), not into blind/.

  python3 eval/blind_pairs.py tally <labelA> <labelB> --keydir DIR
      Reads blind/<A>-vs-<B>/judgments0.json and judgments1.json ({sample: {"human", "faithful", "why"}}),
      unblinds them with the key, copies the key into blind/, and prints the tally.
      A version wins a sample only if it wins in both orders.
"""
import argparse, json, random
from pathlib import Path

from judge import tally

HERE = Path(__file__).parent


def make(a, b, keydir):
    ra, rb = HERE / "runs" / a, HERE / "runs" / b
    names = sorted(p.stem for p in ra.glob("*.md") if (rb / p.name).exists())
    out = HERE / "blind" / f"{a}-vs-{b}"
    out.mkdir(parents=True, exist_ok=True)
    rng = random.Random(f"{a}|{b}")
    key = {}
    for n in names:
        first = rng.choice([a, b])
        second = b if first == a else a
        key[n] = [{"X": first, "Y": second}, {"X": second, "Y": first}]
    instructions = (HERE / "judge_prompt.md").read_text()
    for order in (0, 1):
        parts = [f"# Blind pairs ({len(names)} samples)\n\n{instructions}\n\nJudge each sample separately.\n"]
        for n in names:
            m = key[n][order]
            parts.append(f"\n\n=============== SAMPLE {n} ===============\n\n## Original\n\n"
                         f"{(HERE / 'samples' / f'{n}.md').read_text()}\n\n## Rewrite X\n\n"
                         f"{(HERE / 'runs' / m['X'] / f'{n}.md').read_text()}\n\n## Rewrite Y\n\n"
                         f"{(HERE / 'runs' / m['Y'] / f'{n}.md').read_text()}")
        (out / f"order{order}.md").write_text("".join(parts))
    Path(keydir).mkdir(parents=True, exist_ok=True)
    (Path(keydir) / f"{a}-vs-{b}.key.json").write_text(json.dumps(key, indent=1))
    print(f"{out}/order0.md, order1.md: {len(names)} samples")


def unblind(a, b, keydir):
    out = HERE / "blind" / f"{a}-vs-{b}"
    key = json.loads((Path(keydir) / f"{a}-vs-{b}.key.json").read_text())
    results = {}
    for order in (0, 1):
        j = json.loads((out / f"judgments{order}.json").read_text())
        for n, v in j.items():
            m = dict(key[n][order], tie="tie")
            results.setdefault(n, []).append({"human": m.get(v["human"], "tie"), "faithful": m.get(v["faithful"], "tie"),
                                              "why": v.get("why", ""), "x_was": m["X"]})
    (out / "key.json").write_text(json.dumps(key, indent=1))
    (out / "judgments.json").write_text(json.dumps(results, indent=1))
    return results


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["make", "tally"]); ap.add_argument("a"); ap.add_argument("b")
    ap.add_argument("--keydir", required=True)
    args = ap.parse_args()
    if args.cmd == "make":
        make(args.a, args.b, args.keydir)
    else:
        res = unblind(args.a, args.b, args.keydir)
        t = tally(res, args.a, args.b)
        print(json.dumps(t, indent=1))
        for n, pair in sorted(res.items()):
            print(f"{n:26} human: {pair[0]['human']:>9} / {pair[1]['human']:<9}  faithful: {pair[0]['faithful']:>9} / {pair[1]['faithful']}")
