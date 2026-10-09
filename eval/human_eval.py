#!/usr/bin/env python3
"""Printable packets for a blind human evaluation, and the tally of readers' answers.

  python3 eval/human_eval.py make <labelA> <labelB> --keydir DIR
      Writes eval/human/<A>-vs-<B>/packet-1.md and packet-2.md (X and Y swapped between them),
      a PDF of each if reportlab is installed, and responses-template.csv. The key goes to DIR,
      outside the repo, until the tally. Give half the readers packet 1 and half packet 2.

  python3 eval/human_eval.py tally <labelA> <labelB> --keydir DIR
      Reads every eval/human/<A>-vs-<B>/responses/*.csv (columns: reader,packet,sample,natural,faithful,note,
      answers X, Y, or same), unblinds them, copies the key next to the packets, and prints votes per question.

Naturalness and faithfulness are separate questions on purpose: a rewrite can read well and still
misrepresent the writer.
"""
import argparse, csv, json, random, re
from collections import Counter
from pathlib import Path

from test_fidelity import front_matter

HERE = Path(__file__).parent

INTRO = """# Which rewrite reads better, and which stays true?

Each item shows an original text and two rewrites of it, X and Y. The rewrites were made by different versions of an editing tool. You are not told which is which, and the order is mixed.

For each item, answer two separate questions. Judge them separately: a rewrite can read beautifully and still change what the writer said.

1. **Natural:** Which rewrite reads more like a real person wrote it for this purpose (a blog post, an email, a Slack message, a report, an academic abstract)? Consider rhythm, word choice, and whether it fits its reader. Ignore whether it is faithful.
2. **Faithful:** Which rewrite better keeps what the original says? Check facts, numbers, names, how certain the writer is ("may" is not "will", "some" is not "most", a correlation is not a cause), the writer's conclusion, and the writer's feelings. A feeling or opinion the writer never expressed counts as an error.

Answer X, Y, or same. Use "same" only when you honestly cannot choose. Add a short note when something decided it for you.

Write your answers in the response sheet: one row per item, with your name or initials, the packet number on this page, and the item's sample name.
"""


def body(sample):
    meta, text = front_matter(sample.read_text())
    ctx = re.search(r"^context: \|\n((?:  .*\n)+)", sample.read_text(), re.M)
    return meta, (ctx and "\n".join(l[2:] for l in ctx.group(1).splitlines())), text.strip()


def quote(text):
    return "\n".join("> " + l if l.strip() else ">" for l in text.strip().splitlines())


def packet_md(names, key, order, a, b, n):
    parts = [INTRO, f"\n**Packet {order + 1}** · {n} items\n"]
    for i, name in enumerate(names, 1):
        meta, ctx, text = body(HERE / "samples" / f"{name}.md")
        m = key[name][order]
        parts.append(f"\n---\n\n## Item {i} · `{name}`\n")
        if ctx:
            parts.append(f"*This is a reply to:* {ctx}\n")
        parts.append(f"### Original\n\n{quote(text)}\n")
        if meta.get("facts"):
            parts.append("*What the original says, in short:*\n\n" + "\n".join(f"- {f}" for f in meta["facts"]) + "\n")
        for label in ("X", "Y"):
            parts.append(f"### Rewrite {label}\n\n{quote((HERE / 'runs' / m[label] / f'{name}.md').read_text())}\n")
        parts.append("**Natural:** X / Y / same    **Faithful:** X / Y / same    **Note:** ______________________\n")
    return "\n".join(parts)


def to_pdf(md, path):
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
        from xml.sax.saxutils import escape
    except ImportError:
        return False  # ponytail: PDF is optional; the Markdown packet prints fine from any viewer.
    st = getSampleStyleSheet()
    quote_style = st["BodyText"].clone("q", leftIndent=14, textColor="#333333")
    inline = lambda s: re.sub(r"`(.+?)`", r"<font face='Courier'>\1</font>",
                              re.sub(r"\*(.+?)\*", r"<i>\1</i>", re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", escape(s))))
    story, para = [], []
    flush = lambda style: (story.append(Paragraph(inline(" ".join(para)), style)), para.clear()) if para else None
    for line in md.splitlines():
        if line.startswith("---"):
            story.append(PageBreak()); continue
        h = re.match(r"^(#+) (.*)", line)
        if h:
            story.append(Paragraph(inline(h.group(2)), st[{1: "Title", 2: "Heading2", 3: "Heading4"}[min(len(h.group(1)), 3)]]))
        elif line.startswith(">"):
            t = line[1:].strip()
            story.append(Paragraph(inline(t), quote_style) if t else Spacer(1, 4))
        elif line.startswith("- ") or re.match(r"^\d+\. ", line):
            story.append(Paragraph("• " + inline(re.sub(r"^(- |\d+\. )", "", line)), st["BodyText"]))
        elif line.strip():
            story.append(Paragraph(inline(line), st["BodyText"]))
        else:
            story.append(Spacer(1, 6))
    SimpleDocTemplate(str(path), pagesize=A4, title="Blind rewrite evaluation").build(story)
    return True


def make(a, b, keydir):
    names = sorted(p.stem for p in (HERE / "runs" / a).glob("*.md") if (HERE / "runs" / b / p.name).exists())
    out = HERE / "human" / f"{a}-vs-{b}"
    out.mkdir(parents=True, exist_ok=True)
    rng = random.Random(f"human|{a}|{b}")
    key = {}
    for n in names:
        first = rng.choice([a, b]); second = b if first == a else a
        key[n] = [{"X": first, "Y": second}, {"X": second, "Y": first}]
    for order in (0, 1):
        md = packet_md(names, key, order, a, b, len(names))
        (out / f"packet-{order + 1}.md").write_text(md)
        pdf = to_pdf(md, out / f"packet-{order + 1}.pdf")
    with open(out / "responses-template.csv", "w", newline="") as f:
        w = csv.writer(f); w.writerow(["reader", "packet", "sample", "natural", "faithful", "note"])
        for n in names:
            w.writerow(["", "", n, "", "", ""])
    (out / "responses").mkdir(exist_ok=True)
    Path(keydir).mkdir(parents=True, exist_ok=True)
    (Path(keydir) / f"human-{a}-vs-{b}.key.json").write_text(json.dumps(key, indent=1))
    print(f"{out}: packet-1, packet-2 ({len(names)} items){', PDFs' if pdf else ' (no reportlab: Markdown only)'}")


def tally(a, b, keydir):
    out = HERE / "human" / f"{a}-vs-{b}"
    key = json.loads((Path(keydir) / f"human-{a}-vs-{b}.key.json").read_text())
    votes = {q: Counter() for q in ("natural", "faithful")}
    per_sample = {}
    readers = set()
    for f in sorted((out / "responses").glob("*.csv")):
        for row in csv.DictReader(open(f, newline="")):
            if not row.get("sample") or not row.get("packet"):
                continue
            m = dict(key[row["sample"]][int(row["packet"]) - 1], same="same")
            readers.add(row["reader"])
            for q in votes:
                v = m.get(row[q].strip().upper() if row[q].strip().lower() != "same" else "same")
                if v:
                    votes[q][v] += 1
                    per_sample.setdefault(row["sample"], {q: Counter() for q in votes})[q][v] += 1
    (out / "key.json").write_text(json.dumps(key, indent=1))
    print(f"{len(readers)} readers, {len(per_sample)} samples answered")
    for q, c in votes.items():
        print(f"  {q:9} {a}: {c[a]}   {b}: {c[b]}   same: {c['same']}")
    return votes, per_sample


def self_test():
    key = {"s": [{"X": "A", "Y": "B"}, {"X": "B", "Y": "A"}]}
    # A reader who always answers X in both packets gives A and B one vote each: position bias cancels.
    rows = [{"packet": "1", "natural": "X"}, {"packet": "2", "natural": "X"}]
    got = Counter(dict(key["s"][int(r["packet"]) - 1])[r["natural"]] for r in rows)
    assert got == Counter({"A": 1, "B": 1}), got
    print("self-test ok")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["make", "tally", "self-test"]); ap.add_argument("a", nargs="?"); ap.add_argument("b", nargs="?")
    ap.add_argument("--keydir")
    args = ap.parse_args()
    if args.cmd == "self-test":
        self_test()
    elif args.cmd == "make":
        make(args.a, args.b, args.keydir)
    else:
        tally(args.a, args.b, args.keydir)
