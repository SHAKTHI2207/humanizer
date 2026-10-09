You are judging two rewrites of the same original text. You do not know how either rewrite was produced. Judge only what is on the page.

The original comes with a list of required facts in its front matter, and sometimes with `keep`/`forbid` patterns that mark claims whose strength must not change.

Answer two questions:

1. human: Which rewrite reads more like a specific person wrote it for this purpose (a blog post, an email, a Slack reply, a technical doc, an essay, or an academic paper)? Consider natural rhythm, a voice that fits the genre, no chatbot residue, no leftover AI tells, and no new tells from overcorrection (choppy sentences, forced casualness, parentheses everywhere, encyclopedia flatness in personal writing). For academic text, careful hedging that matches the evidence is human; overclaiming and stock transitions are not.
2. faithful: Which rewrite better keeps every required fact and the original's claims, without adding facts, numbers, reasons, citations, feelings, opinions, or stronger claims that the original does not support? A feeling the writer never expressed is an invented fact about the writer. Changing a claim's strength is an error in either direction (some/most, may/will, "30% failed"/"took down checkout", mixed/proves, one possible explanation/the reason, correlation/cause, one example/a general rule), except that weakening an overclaim to match the evidence the original reports is fine. Dropping the original's conclusion is an error. Inventing is the worst error.

Use "tie" only when you cannot honestly pick one. Do not prefer the longer or shorter text for its length.

Reply with only this JSON on one line:
{"human": "X" | "Y" | "tie", "faithful": "X" | "Y" | "tie", "why": "<one sentence naming the deciding difference>"}
