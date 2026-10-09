#!/usr/bin/env python3
"""Deterministic fidelity tests for humanizer rewrites. No model needed.

Usage:
  python3 eval/test_fidelity.py                 # summary for every run
  python3 eval/test_fidelity.py v4-final -v     # one run, list every failure
  python3 eval/test_fidelity.py --self-test     # check the checker

Three checks per rewrite:
  magnitude  the sample's `keep` patterns must match and its `forbid` patterns must not
             (some -> most, may -> will, 30% failed -> took down checkout, mixed -> proves, ...)
  numbers    every number in the source must still appear in the rewrite (except the sample's `may_drop`)
  emotion    a feeling word the source never used is an invented feeling. If the source states
             some feeling, an added feeling word is only flagged for review, since sharpening a
             stated feeling ("Devastating" -> "I took it hard") is allowed.

Exit code 1 if the run named on the command line has any magnitude, number, or emotion failure.
ponytail: regex and a word list, so it catches the failure modes we have seen, not every paraphrase.
The blind judge covers the rest.
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).parent

EMOTION = re.compile(
    r"\b(?:worr\w*|bother\w*|proud|pride|hurt(?:ing)?|frustrat\w*|annoy\w*|love[sd]?|hate[sd]?|excit\w*|thrill\w*|"
    r"nervous|anxi\w*|regret\w*|surpris\w*|glad|happy|happi\w*|sad|sadd\w*|afraid|scar(?:ed|y|es?)|fear\w*|reliev\w*|"
    r"relief|disappoint\w*|devastat\w*|poignan\w*|unsettl\w*|uneas\w*|delight\w*|embarrass\w*|ashamed|guilt\w*|angry|upset\w*|"
    r"enjoy\w*|pleasure|sting\w*|stung|heartbreak\w*|miserable|thankful|grateful|honou?red|thrilled|"
    r"how i feel|i feel|i felt|feel(?:s|ing)? (?:like|that)|stopped worrying)\b", re.I)

NEGATION = re.compile(r"\b(?:not|no|never|cannot|can't|cannot|doesn't|don't|isn't|aren't|without|nor)\b[^.;]*$", re.I)

SMALL = "zero one two three four five six seven eight nine ten eleven twelve".split()


def front_matter(text):
    """Tiny parser for the samples' front matter: `key: value` and `key:` followed by `  - item` lists."""
    m = re.match(r"\A---\n(.*?)\n---\n(.*)\Z", text, re.S)
    if not m:
        return {}, text
    meta, key = {}, None
    for line in m.group(1).splitlines():
        if re.match(r"^\S[^:]*:", line):
            key, _, val = line.partition(":")
            val = val.strip()
            meta[key] = [] if val in ("", "[]") else val
        elif line.strip().startswith("- ") and key:
            item = line.strip()[2:].strip()
            if item.startswith('"') and item.endswith('"'):
                item = item[1:-1].replace("\\\\", "\\").replace('\\"', '"')
            meta[key].append(item)
    return meta, m.group(2)


def numbers(text):
    # Ignore numbered list markers and section numbers like "1." at line start.
    body = re.sub(r"(?m)^\s*\d+\.\s", "", text)
    return {n.replace(",", "") for n in re.findall(r"\d[\d,]*(?:\.\d+)?", body)}


def emotions(text):
    return {m.group(0).lower() for m in EMOTION.finditer(text)}


def check(source_text, rewrite):
    meta, src = front_matter(source_text)
    fails = []
    for pat in meta.get("keep", []):
        if not re.search(pat, rewrite, re.I):
            fails.append(("magnitude", f"lost: /{pat}/"))
    for pat in meta.get("forbid", []):
        for m in re.finditer(pat, rewrite, re.I):
            # "cannot show that sleep improves recall" keeps the claim calibrated; only flag asserted matches.
            if not NEGATION.search(rewrite[max(0, m.start() - 40):m.start()]):
                fails.append(("magnitude", f"distorted: '{m.group(0)}'"))
                break
    rw_nums = numbers(rewrite)
    rw_words = rewrite.lower()
    # may_drop: numbers a reply can leave out because the reader supplied them (§26).
    for n in sorted(numbers(src) - rw_nums - set(meta.get("may_drop", []))):
        word = SMALL[int(n)] if n.isdigit() and int(n) < len(SMALL) else None
        if not (word and re.search(rf"\b{word}\b", rw_words)):
            fails.append(("numbers", f"missing number {n}"))
    # states_feeling: the source expresses a feeling in words the lexicon misses ("a deeply personal reckoning").
    src_em = emotions(src) | ({"(stated)"} if meta.get("states_feeling") == "true" else set())
    stems = lambda s: {w[:5] for w in s}
    added = {w for w in emotions(rewrite) if w[:5] not in stems(src_em)}
    for w in sorted(added):
        fails.append(("emotion-review" if src_em else "emotion", f"added feeling '{w}'"))
    return fails


def run(label):
    out = {}
    for s in sorted((HERE / "samples").glob("*.md")):
        r = HERE / "runs" / label / s.name
        if r.exists():
            out[s.stem] = check(s.read_text(), r.read_text())
    return out


def self_test():
    sample = ('---\nkeep:\n  - "30\\\\s?%"\n  - "mixed"\nforbid:\n  - "took down"\n---\n'
              "About 30% of requests failed. The evidence is mixed. It was devastating. Tests: 3 of 40.")
    assert check(sample, "About 30% failed; the evidence is mixed. I took it hard. Three of 40 tests.") == []
    kinds = [k for k, _ in check(sample, "The outage took down checkout and the evidence proves it. I'm still bothered.")]
    assert kinds.count("magnitude") == 3 and kinds.count("numbers") == 3 and "emotion-review" in kinds, kinds
    neutral = "---\nkeep: []\n---\nWe moved the meeting to Monday."
    assert [k for k, _ in check(neutral, "We moved it to Monday, which still bothers me.")] == ["emotion"]
    claim = '---\nforbid:\n  - "improves recall"\n---\nr = 0.31'
    assert check(claim, "This cannot show that sleep improves recall. r = 0.31") == []
    assert [k for k, _ in check(claim, "Sleep improves recall (r = 0.31).")] == ["magnitude"]
    print("self-test ok")


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    if "--self-test" in sys.argv:
        self_test(); sys.exit(0)
    labels = args or sorted(d.name for d in (HERE / "runs").iterdir() if d.is_dir())
    bad = False
    print(f"{'run':18}{'n':>4}{'magnitude':>11}{'numbers':>9}{'emotion':>9}{'review':>8}")
    for label in labels:
        res = run(label)
        if not res:
            continue
        count = lambda k: sum(1 for f in res.values() for kind, _ in f if kind == k)
        print(f"{label:18}{len(res):>4}{count('magnitude'):>11}{count('numbers'):>9}{count('emotion'):>9}{count('emotion-review'):>8}")
        if "-v" in sys.argv:
            for name, f in res.items():
                for kind, msg in f:
                    print(f"    {name:26} {kind:15} {msg}")
        bad |= bool(args) and any(k in ("magnitude", "numbers", "emotion") for f in res.values() for k, _ in f)
    sys.exit(1 if bad else 0)
