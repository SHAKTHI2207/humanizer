#!/usr/bin/env python3
"""Count AI tells and overcorrection signs in humanizer outputs.

Usage:
  python3 eval/tells.py                    # score samples/ and every runs/<label>/
  python3 eval/tells.py runs/v4-step4      # score one folder, per file

Rates are per 100 words, so long and short texts compare fairly.
Lower is better for "tells" and "overcorrection". "shape" is descriptive:
human prose usually has a sentence-length CV around 0.4-0.7 and some contractions.
"""
import re
import statistics
import sys
from pathlib import Path

HERE = Path(__file__).parent

def words(pattern_list):
    return re.compile(r"\b(?:" + "|".join(pattern_list) + r")\b", re.I)

TELLS = {
    "s1_not_x_but_y": re.compile(
        r"\b(?:not (?:just|only|merely)|isn'?t (?:just|only|merely|about)|it'?s not\b[^.]{0,60}?[,;] it'?s)\b", re.I),
    "s2_closer": re.compile(
        r"(?:^|\n)\s*(?:In conclusion|Ultimately|Overall|In the end|In summary)\b|Let that sink in|Read that again"
        r"|\b(?:That|This) (?:is the real|distinction matters)", re.I),
    "s4_runup": re.compile(
        r"Let'?s (?:dive|explore|break|be honest)|Here'?s the thing|The thing is|Honestly\?|Real talk|"
        r"here'?s what you need to know|without further ado|\b(?:The result|The lesson|The best part|The catch)\?", re.I),
    "s8_dash": re.compile(r"—|–| -- "),
    "s12_ai_word": words([
        "additionally", "align(?:s|ed)? with", "bolster(?:ed)?", "crucial", "deep dive", "delve[sd]?", "enduring",
        "enhanc(?:e|es|ed|ing)", "garner(?:ed)?", "highlight(?:s|ed|ing)?", "interplay", "intricac(?:y|ies)", "intricate",
        "landscape", "meticulous(?:ly)?", "pivotal", "robust", "showcas(?:e|es|ed|ing)", "tapestry", "testament",
        "underscor(?:e|es|ed|ing)", "vibrant", "leverag(?:e|es|ed|ing)", "seamless(?:ly)?", "navigat(?:e|ing)",
        "unlock(?:s|ing)?", "empower(?:s|ing)?", "streamlin(?:e|es|ed|ing)", "elevat(?:e|es|ing)", "realm",
        "embark(?:ed)?", "journey", "game-changer", "transformative", "ever-evolving", "fast-paced"]),
    "s13_inflation": re.compile(
        r"stands as|plays? a (?:key|vital|crucial|pivotal) role|marking a|the future looks bright|exciting times|"
        r"step in the right direction|continues to thrive|reflects a broader|setting the stage", re.I),
    "s16_sales": words(["profound", "nestled", "in the heart of", "groundbreaking", "renowned", "breathtaking",
                        "stunning", "must-visit", "whether you'?re"]),
    "s19_bold": re.compile(r"\*\*[^*]+\*\*"),
    "s20_emoji": re.compile("[\U0001F300-\U0001FAFF☀-➿→]"),
    "s22_chat": re.compile(
        r"I hope this (?:helps|email finds you)|Let me know|Great question|Certainly!|Of course!|Happy to help|"
        r"Feel free to|Don'?t hesitate|truly (?:honored|grateful)|invaluable", re.I),
    "triad": re.compile(r"\b\w+(?: \w+)?, \w+(?: \w+)?,? and \w+", re.I),
}

OVERCORRECTION = {
    "parens": re.compile(r"\((?![^)]*(?:\d{4}|=))[^)]{3,}\)"),  # citations and stats are not asides
    "semicolon": re.compile(r";"),
    "casual_filler": words(["honestly", "kind of", "basically", "pretty much", "literally", "super"]),
}

STARTERS = re.compile(r"^(?:And|So|But)\b")

# Grammar and vocabulary signals from register studies of AI text (e.g. Reinhart et al., PNAS 2025):
# instruction-tuned models use participial clauses and nominalizations far more often than people,
# and their vocabulary is less varied. Academic writers hedge; models overclaim.
STYLE = {
    "participial": re.compile(r",\s+(?!during|according|including|regarding|concerning|nothing|something|anything|everything)[a-z]+ing\b"),
    "nominalization": re.compile(r"\b[a-z]{4,}(?:tion|sion|ment|ness|ity|ance|ence)s?\b", re.I),
    "agentless_passive": re.compile(r"\b(?:is|are|was|were|been|being|be)\s+(?:\w+ly\s+)?\w+(?:ed|en)\b(?![^.]*\bby\b)", re.I),
    "transition": re.compile(r"(?:^|(?<=[.!?]\s))(?:Moreover|Furthermore|Additionally|In addition|Notably|Importantly|Interestingly|Consequently|Thus|Hence|Taken together),", re.M),
    "overclaim": words(["demonstrates?", "proves?", "provides? (?:compelling|robust|strong) (?:evidence|support)", "makes clear",
                       "clearly shows?", "undeniabl[ey]", "revolutioni[sz]e", "paving the way", "seminal", "powerful intervention"]),
    "hedge": words(["may", "might", "could", "suggests?", "appears?", "likely", "possibly", "however", "although",
                    "though", "but", "tentative(?:ly)?", "we cannot", "unclear"]),
}


def mattr(tokens, w=50):
    """Moving-average type-token ratio: lexical diversity that does not shrink with text length."""
    if len(tokens) <= w:
        return len(set(tokens)) / max(len(tokens), 1)
    return statistics.mean(len(set(tokens[i:i + w])) / w for i in range(len(tokens) - w + 1))


def clean(text):
    # Drop YAML front matter (samples) and the change notes some formats append.
    text = re.sub(r"\A---\n.*?\n---\n", "", text, flags=re.S)
    text = re.split(r"\n\s*(?:Changes|Only you can add|Remaining patterns)\s*:", text)[0]
    text = re.sub(r"```.*?```|`[^`]*`", "", text, flags=re.S)
    return text.strip()


def sentences(text):
    body = re.sub(r"^#.*$", "", text, flags=re.M)
    parts = re.split(r"(?<=[.!?])\s+|\n+", body)
    return [p.strip() for p in parts if len(p.split()) >= 1 and p.strip()]


def cv(xs):
    return statistics.pstdev(xs) / statistics.mean(xs) if len(xs) > 1 and statistics.mean(xs) else 0.0


def score(text):
    text = clean(text)
    n = max(len(text.split()), 1)
    per100 = lambda c: 100 * c / n
    out = {"words": n}
    for k, rx in TELLS.items():
        out[k] = per100(len(rx.findall(text)))
    out["tells_total"] = sum(out[k] for k in TELLS)
    for k, rx in OVERCORRECTION.items():
        out[k] = per100(len(rx.findall(text)))
    sents = sentences(text)
    lens = [len(s.split()) for s in sents] or [0]
    out["and_so_but_starts"] = 100 * sum(bool(STARTERS.match(s)) for s in sents) / max(len(sents), 1)
    out["short_sents_pct"] = 100 * sum(l <= 5 for l in lens) / max(len(lens), 1)
    out["overcorrection_total"] = out["parens"] + out["semicolon"] + out["casual_filler"]
    out["sent_len_mean"] = statistics.mean(lens)
    out["sent_len_cv"] = cv(lens)
    paras = [p for p in re.split(r"\n\s*\n", text) if p.strip() and not p.lstrip().startswith("#")]
    out["para_len_cv"] = cv([len(p.split()) for p in paras])
    for k, rx in STYLE.items():
        out[k] = per100(len(rx.findall(text)))
    out["lex_diversity"] = mattr(re.findall(r"[a-z']+", text.lower()))
    out["contractions"] = per100(len(re.findall(r"\b\w+'(?:s|t|re|ve|ll|d|m)\b", text)))
    return out


def score_dir(d):
    files = sorted(Path(d).glob("*.md"))
    return {f.stem: score(f.read_text()) for f in files}


def mean_of(scores):
    keys = next(iter(scores.values())).keys()
    return {k: statistics.mean(s[k] for s in scores.values()) for k in keys}


COLS = [("tells_total", "tells"), ("s1_not_x_but_y", "§1"), ("s8_dash", "dash"), ("s12_ai_word", "aiword"),
        ("s22_chat", "chat"), ("triad", "triad"), ("overcorrection_total", "overcorr"), ("parens", "paren"),
        ("semicolon", "semi"), ("and_so_but_starts", "and/so%"), ("short_sents_pct", "short%"),
        ("sent_len_cv", "sentCV"), ("para_len_cv", "paraCV"), ("contractions", "contr"), ("words", "words")]


STYLE_COLS = [("participial", "partic"), ("nominalization", "nominal"), ("agentless_passive", "passive"),
              ("transition", "transit"), ("overclaim", "overclm"), ("hedge", "hedge"), ("lex_diversity", "MATTR")]


def table(rows, cols=COLS):
    head = f"{'':24}" + "".join(f"{label:>9}" for _, label in cols)
    lines = [head]
    for name, s in rows:
        lines.append(f"{name:24}" + "".join(f"{s[k]:9.2f}" if k != "words" else f"{s[k]:9.0f}" for k, _ in cols))
    return "\n".join(lines)


def summarize(only=None):
    """Mean scores for samples and each run, optionally limited to sample names containing `only`."""
    keep = lambda sc: {k: v for k, v in sc.items() if only is None or only in k}
    rows = [("samples (input)", mean_of(keep(score_dir(HERE / "samples"))))]
    for d in sorted((HERE / "runs").iterdir()):
        sc = keep(score_dir(d))
        if sc:
            rows.append((f"{d.name} (n={len(sc)})", mean_of(sc)))
    return rows


if __name__ == "__main__":
    if len(sys.argv) > 1 and Path(sys.argv[1]).is_dir():
        sc = score_dir(sys.argv[1]).items()
        print(table(sc)); print(); print(table(sc, STYLE_COLS))
    else:
        only = sys.argv[1] if len(sys.argv) > 1 else None  # e.g. "academic" or "slack"
        rows = summarize(only)
        print(f"Mean per text{' (' + only + ' only)' if only else ''}; rates are per 100 words.")
        print("Tells and overcorrection: lower is better.\n")
        print(table(rows))
        print("\nStyle (Reinhart et al.-type signals): lower partic/nominal/transit/overclm is more human;"
              " higher MATTR is more varied vocabulary; hedges matter most in academic text.\n")
        print(table(rows, STYLE_COLS))
