"""Usage: python bench.py [file_with_blank_line_separated_paragraphs] [context key, e.g. business]
Reports means over the set: sim, entail, kept (share passing all checks), change (word-level edit
distance), d_flesch (readability shift), ppl_src/ppl_out (distilgpt2 perplexity as a fluency proxy)."""
import math, re, sys, statistics as st
from difflib import SequenceMatcher
from functools import lru_cache

from core import rewrite_one

SAMPLES = [
    "The city council voted 7-2 on Tuesday to approve a $4.5 million budget for the new library branch on Elm Street. "
    "Construction is expected to begin in March 2027 and finish within eighteen months.",
    "Sleep researchers at Stanford found that participants who slept fewer than six hours a night scored 20% lower "
    "on memory tests. The effect was strongest in adults over fifty.",
    "Our team migrated the billing service from a monolith to three smaller services last quarter. Deployment time "
    "dropped from forty minutes to six, although on-call alerts increased for a few weeks.",
]


@lru_cache
def _lm():
    from transformers import AutoModelForCausalLM, AutoTokenizer
    return AutoTokenizer.from_pretrained("distilgpt2"), AutoModelForCausalLM.from_pretrained("distilgpt2")


def ppl(t):
    import torch
    tok, m = _lm()
    ids = tok(t, return_tensors="pt", truncation=True, max_length=512).input_ids
    with torch.no_grad():
        return math.exp(m(ids, labels=ids).loss.item())


def syl(w):
    return max(1, len(re.findall(r"[aeiouy]+", w.lower())))


def flesch(t):
    w = re.findall(r"[A-Za-z']+", t) or ["a"]
    s = max(1, len(re.findall(r"[.!?]+", t)))
    return 206.835 - 1.015 * len(w) / s - 84.6 * sum(map(syl, w)) / len(w)


def main(path=None, context="general"):
    segs = open(path).read().split("\n\n") if path else SAMPLES
    rows = []
    for s in (x.strip() for x in segs if x.strip()):
        r = rewrite_one(s, context)
        rows.append({"sim": r["sim"], "entail": r["entail"], "kept": r["ok"],
                     "change": 1 - SequenceMatcher(None, s.split(), r["out"].split()).ratio(),
                     "d_flesch": flesch(r["out"]) - flesch(s),
                     "ppl_src": ppl(s), "ppl_out": ppl(r["out"])})
    print(f"n={len(rows)} context={context}")
    for k in rows[0]:
        print(f"{k:9}", round(st.mean(x[k] for x in rows), 3))


if __name__ == "__main__":
    main(*sys.argv[1:3])
