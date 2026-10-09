# Humanizer

[![GitHub stars](https://img.shields.io/github/stars/blader/humanizer?style=flat)](https://github.com/blader/humanizer/stargazers) [![skills.sh installs](https://skills.sh/b/blader/humanizer)](https://skills.sh/blader/humanizer)

> **This is a fork.** Version 4.0 is maintained by Shakthivel Manivanan on top of [blader/humanizer](https://github.com/blader/humanizer) 3.1.0. See [PROVENANCE.md](PROVENANCE.md) for who contributed what. The install commands below still point at the upstream repository; replace `blader/humanizer` with this fork's path once it is published.

Humanizer makes AI-written text sound like a person wrote it, without changing what it says. It is built on Wikipedia's [Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), the guide Wikipedia editors use to catch AI-generated text, and it works in Claude Code, Codex, and any other agent that supports skills.

**Before:**
> I'm thrilled to announce that shared drafts are finally here! 🚀 For months, our own team was drowning in files named final_v7.docx — and we knew there had to be a better way. Now two people can edit the same doc at once, with every change appearing live for both of them. It's not just a feature; it's a whole new way to collaborate. Comments stay anchored to the exact sentence they reference, even as the text around them evolves. And the best part? It's available today on every plan, completely free. Let that sink in.

**After:**
> Shared drafts are out today. For months our own team passed around files named final_v7.docx, so we built a way for two people to edit the same doc at once, with each person's changes showing up live for the other. Comments stay pinned to the sentence they're about, even when the text around them changes. It's free on every plan.

In an upstream blind test, judges preferred Humanizer's rewrite over the original AI text 16 times out of 16 ([#229](https://github.com/blader/humanizer/issues/229)). For 4.0's own results, see [Evaluation](#evaluation).

Humanizer edits for human readers. Getting past AI detectors is not a goal, and 4.0 makes no claim about detector scores. See [Detectors](#detectors-what-is-documented-and-what-is-not).

## The five strongest tells

These are the most common signs of AI writing, and Humanizer rewrites any of them on sight:

1. **Not X but Y:** "It's not just a feature, it's a shift."
2. **One-line closers:** "Let that sink in."
3. **Sayings that sound deep:** "At its core, what really matters is..."
4. **A staged run-up:** "Here's the thing." "Honestly?"
5. **Arguing with no one:** "I'm not saying X, but..."

Humanizer checks for [26 patterns](#the-26-patterns) in all.

## Installation

Once installed, the skill answers to `/humanizer`.

### Claude Code

```text
/plugin marketplace add blader/humanizer
/plugin install humanizer@humanizer
```

The plugin answers to `/humanizer:humanizer`. It needs Claude Code 2.1.142 or newer; on older versions, use `npx skills add blader/humanizer --global --agent claude-code`.

### Codex

```bash
npx skills add blader/humanizer --global --agent codex
```

### Claude.ai and Claude Desktop

Download this repository as a ZIP (**Code → Download ZIP**) and upload it as a skill in Settings.

### Other agents

```bash
npx skills add blader/humanizer --global --agent '*'
```

This installs Humanizer for every agent the Skills CLI supports, including Gemini CLI, GitHub Copilot, and Windsurf. Leave off `--global` in any command above to install it only in the current project. For an agent the Skills CLI does not know, copy `SKILL.md` into its skill folder.

## Usage

Call the skill directly:

```
/humanizer

[paste your text here]
```

Or ask in plain language:

```
Please humanize this text: [your text]
```

To rewrite a file, give Humanizer its path:

```
Humanize the prose in docs/launch-post.md
```

### Match your voice

If you want the rewrite to sound more like you, include a sample:

```
/humanizer

Here's a sample of my writing for voice matching:
[paste 2-3 paragraphs of your own writing]

Now humanize this text:
[paste AI text to humanize]
```

Humanizer follows the sample's rhythm, word choice, punctuation, and deliberate quirks, including dashes if you use them.

## How it works

A language model writes whatever is most likely to come next, so by default it makes the choice that fits the widest range of readers and subjects. A person chooses for one reader and one subject. Every tell Humanizer looks for is a form of that default choice: a sentence that signals importance instead of adding a fact, rhythm or formatting applied by rule, an ordinary fact dressed as a pivotal one, text left over from the chat, or a reply that re-explains what the reader already knows.

> "LLMs use statistical algorithms to guess what should come next. The result tends toward the most statistically likely result that applies to the widest variety of cases."
> Wikipedia, ["Signs of AI writing"](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)

Humanizer marks every tell it finds, strongest first. It drafts a rewrite without treating the original structure as fixed, checks the draft against the patterns and the original claims, and then writes the final version. It does not make things up. A name, number, date, quote, citation, or other factual detail must come from the source or the writer, and if a sentence needs a detail that is missing, Humanizer asks instead of inventing one. Since 4.0 the same rule covers the writer's feelings and the strength of every claim: Humanizer may voice a feeling the writer stated more naturally, but never adds one, and "some" stays "some", "may" stays "may", a correlation stays a correlation, and "the evidence is mixed" stays mixed.

When you paste text, Humanizer returns the final rewrite first, as text you can publish as your own, followed by at most three short notes: the main changes, anything only you can supply, and, for personal writing that states no feeling, up to two optional reactions you may add or ignore. Those suggestions never appear inside the rewrite. Ask to see the draft and the critique if you want them. Point it at a file and it changes only the prose, leaving code, data, frontmatter, and link targets alone. Personal writing keeps the writer's opinions and quirks at the strength the writer gave them. Academic writing keeps hedges that mark real limits and loses overclaims and stock transitions. Technical and reference prose stays neutral and plain.

## What 4.0 changes

Version 4.0 keeps all 26 patterns and changes what the rewrite is allowed to do. The target is the most natural prose possible without changing anything the writer said.

- **Sharpen feelings, never invent them.** If the source says "Devastating," the rewrite may say "I took it harder than I'd like to admit." If the source states no feeling, the rewrite adds none. For personal writing, Humanizer may list up to two reactions *below* the rewrite as optional suggestions. They never appear inside it.
- **Claims keep their strength.** "Some" never becomes "most", "may" never becomes "will", "30% of requests failed" never becomes "the outage took down checkout", one possible explanation never becomes the reason, a correlation never becomes a cause, and "the evidence is mixed" stays mixed.
- **Academic writing stays academic.** Hedges that mark real limits stay. Overclaims (demonstrates, proves, paving the way) and stock transitions (Moreover, Furthermore, Notably) go. Citations are left as written and flagged when they look doubtful.
- **No new tells.** The rewrite is checked for the tells that editing creates: parentheses everywhere, chopped sentences, casual words the writer never used, and flat encyclopedia prose in personal writing.
- **No new comparisons.** A comparison or superlative the source does not make ("more patience than any hobby I've tried") is an invented claim.

The rewrite is text you can publish as your own. The suggestions are ideas you may take or leave.

## What makes prose read as human

Version 4.0 treats human writing as variation that follows the content, not as a list of cosmetic tricks. Adding contractions, typos, slang, or personal feelings by rule produces its own recognizable style, and the forced casualness of many "humanizer" tools ("Basically," "kind of," "folks" inside an academic paragraph) is one of the easiest tells to spot. What the skill aims for instead:

- Sentence length that changes because the thought changes: a short sentence for a plain fact, a longer one for a qualified claim.
- Specific detail when the source has it, and plain statement when it does not.
- Transitions that state a real relation (because, so, but) instead of ritual ones (Moreover, Furthermore).
- Repetition of the right term instead of rotating synonyms.
- Uncertainty where the writer is uncertain, and confidence where the evidence supports it.
- The writer's own perspective, at the strength the writer gave it.
- A register that fits the reader: a Slack reply leads with the answer, an abstract hedges to its evidence, a blog post can sound like a person thinking.

## Evaluation

The harness is in [`eval/`](eval/README.md). It has 23 AI-written samples across seven kinds of writing (blog, email, technical, essay, Slack, academic, report and reflective). Each comes with its required facts and, where relevant, patterns that mark claims whose strength must not change. Five samples were written to bait the failure modes: neutral text that invites an invented feeling, and claims that invite a stronger quantifier, a cause, or a general rule.

Three kinds of checks:

1. **Blind pairwise judging.** A separate model instance sees the original and two unlabeled rewrites and picks which reads more like a person wrote it and which is more faithful. Every pair is judged twice with the positions swapped, by separate judges. A version wins a sample only if it wins both times, so a judge that always prefers the first text produces only ties.
2. **Deterministic fidelity tests** (`eval/test_fidelity.py`): required claims present, forbidden distortions absent, every number kept, and no feeling words the source never used.
3. **Tell and register counts** (`eval/tells.py`): AI tells, overcorrection signs, participial clauses, nominalizations, agentless passives, stock transitions, overclaims, hedges, sentence-length variation, and lexical diversity.

### Results (October 2026, 23 samples)

4.0 is a release candidate. Its rules were tuned over three evaluation rounds, and all three are reported here, not only the best one. Round 3 is the shipped text. Round 2 differs from it by one clause (no added comparisons or superlatives); round 1 lacked the clarifications about conclusions and hype. Every round rewrote all 23 samples once and was judged blind against each earlier version in both presentation orders. Wins count only when both orders agree (4.0 – other – tie).

| 4.0 vs | Round | Sounds more human | More faithful |
|---|---|---|---|
| 3.1.0 (upstream) | 1 | **11** – 7 – 5 | **11** – 1 – 11 |
| | 2 | **11** – 4 – 8 | **9** – 3 – 11 |
| | 3 (shipped) | **9** – 6 – 8 | **10** – 5 – 8 |
| step 4 (experimental) | 1 | 8 – 8 – 7 | **8** – 2 – 13 |
| | 2 | **14** – 5 – 4 | **8** – 4 – 11 |
| | 3 (shipped) | **10** – 7 – 6 | 4 – **6** – 13 |
| step 5 (experimental) | 1 | 3 – **14** – 6 | **10** – 1 – 12 |
| | 2 | 3 – **12** – 8 | **12** – 3 – 8 |
| | 3 (shipped) | 0 – **18** – 5 | **12** – 2 – 9 |

What holds across all three rounds:

- **Against 3.1.0, 4.0 is both more natural and more faithful.**
- **Against step 5, 4.0 is far more faithful and clearly less natural.** Step 5 told the rewriter to add the writer's reactions. Its edge comes largely from content the writer never wrote ("that one still bothers me", "I haven't settled how I feel"). 4.0 gives that up on purpose.
- **Against step 4, the result is unstable.** 4.0 won on naturalness in two rounds out of three. Faithfulness flipped in round 3, when the rewriter dropped real conclusions ("how we work matters more than where") while cutting stock send-offs.

**Rounds 2 and 3 differ by one clause, but their step 4 results differ by more than many version-to-version gaps.** A single rewrite per sample is not enough to rank close versions. The next validation step is several runs per version.

Deterministic fidelity tests on the same 23 samples:

| Version | Magnitude distortions | Lost numbers | Invented feelings | Feeling changes to review |
|---|---|---|---|---|
| 3.1.0 | 2 | 0 | 0 | 5 |
| step 4 | 1 | 0 | 1 | 5 |
| step 5 | 3 | 0 | 1 | 8 |
| 4.0, round 1 | 0 | 0 | 0 | 7 |
| 4.0, round 2 | 1 | 0 | 0 | 2 |
| **4.0, round 3 (shipped)** | **1** | **0** | **0** | **2** |

The round 2 failure was an invented comparison ("more patience than any hobby I've tried"); the rule that fixed it is the one added in round 3. The round 3 failure is a literature review that never says the evidence is mixed, only that "the outcome depends on context". The judges counted that as a dropped conclusion, and so does the test. Review items are stated feelings voiced differently ("a pleasure" becoming "I enjoyed", "poignant" becoming "sad"), which the rules allow. The judges also caught two small intensifiers the tests miss: "almost overnight" and "in my lifetime".

Register signals, mean per 100 words (lower is better except hedges and lexical diversity):

| | AI tells | Overcorrection | Stock transitions | Overclaims | Nominalizations | Hedges | Lexical diversity (MATTR) |
|---|---|---|---|---|---|---|---|
| Input samples | 5.99 | 0.13 | 0.35 | 0.25 | 5.49 | 0.67 | 0.87 |
| 3.1.0 | 0.24 | 0.04 | 0.00 | 0.04 | 3.60 | 1.22 | 0.85 |
| 4.0 (round 3) | 0.12 | 0.07 | 0.00 | 0.00 | 3.88 | 1.37 | 0.86 |

4.0 halves the remaining AI tells and removes overclaims entirely. It does not reduce nominalizations. The instruction to prefer verbs has no measurable effect, and academic prose is nominal by nature.

### Limits of this evaluation

- The judges are language models, not human readers. They agree with each other more than people do, and they may share the rewriter's taste.
- 23 samples is small, and each round rewrote each sample once. Results moved by up to six wins between rounds with nearly identical skill text. Only the patterns that held across all three rounds are reported as findings.
- The samples were written for this test by the same kind of model that rewrites them.
- The fidelity tests are regular expressions and a word list. They catch the failure modes seen so far, not every paraphrase, and the judges cover the rest.
- The tell counter's passive-voice pattern also counts adjectives such as "is mixed".
- No human-written baseline was scored, so the register numbers show direction, not distance from human prose.

## Detectors: what is documented and what is not

Humanizer does not target any detector. Here is what is known, kept apart by kind of evidence.

**Documented by Turnitin** ([AI writing detection capabilities FAQs](https://guides.turnitin.com/), read October 2026):

- The submission is split into overlapping segments. Each segment gets a probability from a transformer-based classifier, and the sentence scores are pooled into a document percentage.
- The model is "not explicitly programmed" to score burstiness, perplexity, or other single metrics. It learns patterns from training data, so individual predictions may not be explainable feature by feature.
- It also flags AI text that was modified by "paraphraser or bypasser (also called humanizers)" tools, for English submissions.
- It processes only long-form prose sentences (at least 300 words), not lists or bullets. It reports a false-positive rate under 1% for documents with more than 20% AI writing, and shows no score below 20%.
- Turnitin says false positives can come from text with little structural variation, text that repeats itself, and text paraphrased without new ideas. It says the score must not be the sole basis for action.

**Research findings:**

- Reinhart et al. (2025, *PNAS*, doi:10.1073/pnas.2422455122) found that instruction-tuned models use features such as present participial clauses and nominalizations at markedly higher rates than human writers.
- Liang et al. (2023, *Patterns*, doi:10.1016/j.patter.2023.100779) found that GPT detectors misclassify non-native English writing as AI-generated at high rates. A detector score is evidence about statistical style, not proof of authorship.

**Observed by the maintainer** (two reports on the maintainer's own documents, not published here): one detector labeled a draft that mixed formal AI register with forced casual phrasing as "Mix of AI and Human" and highlighted nearly all of it. One observation is not evidence of how any detector works.

**Hypotheses, not tested here:** a tool that rewrites only surface features may be exactly what bypasser detection is trained to catch, and prose that reads naturally to people because it is specific, calibrated, and varied with the content is a more defensible goal than any score. 4.0 has not been run through Turnitin or any other detector, and it makes no claim about detector results.

## The 26 patterns

The patterns are numbered by strength and frequency. The first five justify an edit on a single sighting. Patterns marked *weak alone* count only when several tells share a passage, because a careful writer may use any one of them on purpose.

### A. Staging instead of stating

| # | Pattern | Before | After |
|---|---------|--------|-------|
| 1 | **Not X but Y** | "It's not just X, it's Y", "This doesn't mean X. It means Y." | State the point directly |
| 2 | **One-line closers and dramatic fragments** | "That is the real win." after every section; "This shows the importance of..." after an example; "No prior. No nostalgia." | Cut the closer that repeats or explains the example; merge fragments into a specific claim |
| 3 | **Sayings that sound deep** | "At its core, what matters is...", "Symmetry is the language of trust" | Replace the saying with the specific claim |
| 4 | **Staged run-up before the point** | "Let's dive in", "Honestly? It depends..." | Remove the run-up and state the point |
| 5 | **Arguing with no one** | "This isn't mainly about...", "A tempting approach would be..." | Remove the unraised objection or fake option; keep any real claim |

### B. Rhythm by rule

| # | Pattern | Before | After |
|---|---------|--------|-------|
| 6 | **Forced triads** | "innovation, inspiration, and insights"; three examples plus a lesson | Use the number of items the meaning needs |
| 7 | **Repeated sentence openings** | "She noted... She noted... She filed..." | Merge the sentences or change the subject |
| 8 | **Dashes as the universal connector** (*weak alone*) | "institutions—not the people—yet this continues—" | Use periods, commas, colons, or parentheses; match a sample that uses dashes |
| 9 | **Stacked qualifiers** (*weak alone*) | "could potentially possibly be argued" | Keep only qualifiers the source supports |
| 10 | **Hyphenated pairs everywhere** (*weak alone*) | "the report is high-quality" | Keep the hyphen before the noun or where the dictionary has one |
| 11 | **Passive voice and missing subjects** (*weak alone*) | "No configuration file needed" | Name the actor when that helps |

### C. Inflation and borrowed authority

| # | Pattern | Before | After |
|---|---------|--------|-------|
| 12 | **Overused AI words** | "delve... testament... landscape... showcasing" | Use plain words |
| 13 | **Inflated significance** | "marking a pivotal moment", "Despite challenges... continues to thrive", "The future looks bright" | Keep the fact and drop the significance; end on the last concrete fact |
| 14 | **Vague connection or association** | "associated with the leadership of", "in connection with" | State the relationship the source gives |
| 15 | **Shallow -ing riders** | "symbolizing... reflecting... showcasing..." | Keep only what the source supports |
| 16 | **Sales language** | "nestled within the breathtaking region" | State what the thing is |
| 17 | **Borrowed authority** | "Experts believe...", "cited in NYT, BBC, FT, and The Hindu" | Name a real source and what it said, or remove the claim or list |
| 18 | **Avoiding is, are, and has** | "serves as... features... boasts" | "is... has" |

### D. Formatting by rule

| # | Pattern | Before | After |
|---|---------|--------|-------|
| 19 | **Bold as decoration** | "**OKRs**, **KPIs**"; "**Performance:** Performance improved" | Remove the bold; turn a labeled list into prose |
| 20 | **Decorative headings** | "Strategic Negotiations And Partnerships", "🚀 Launch Phase:", "The decision, on one screen" | Sentence case; remove emojis and arrows; name what the section holds |
| 21 | **Curly quotation marks** (*weak alone*) | `said “the project”` | `said "the project"` |

### E. Leftovers from the chat and the draft

| # | Pattern | Before | After |
|---|---------|--------|-------|
| 22 | **Chatbot residue** | "Great question! ... I hope this helps!" | Remove the wrapper and keep the content |
| 23 | **Knowledge-limit disclaimers and guesses** | "While details are limited in available sources, it appears..." | State what the source shows, or remove the sentence |
| 24 | **A heading repeated in the first sentence** | "## Performance" + "Speed matters." | Let the heading do the work |
| 25 | **Writing about the document instead of its subject** | "This function was added to replace...", "compiled from...", "The table below compares..." | Describe the subject; state a convention only when the reader cannot see it |

### F. Writing for the wrong reader

| # | Pattern | Before | After |
|---|---------|--------|-------|
| 26 | **Re-explaining what the reader knows** | A reply that walks the diagnosis and proves the plan works before the decision | Lead with the decision; leave the diagnosis and the proof for the ticket that follows |

## Full example

**Before (AI-sounding):**
> I recently spent five unforgettable days in Lisbon last October, and let me tell you — this city completely stole my heart. From the moment I checked into my charming hotel perched high in the historic Alfama district, I knew I was somewhere truly special.
>
> Yes, the famous hills are challenging — with countless stairs between my hotel and everything else, my legs certainly felt it! — but every climb rewards you with breathtaking, panoramic views that make it all worthwhile.
>
> No trip would be complete without riding the iconic Tram 28, a roughly forty-minute journey shared with plenty of fellow travelers eager to capture the magic. And the food? Simply divine. While the pastéis de nata at Pastéis de Belém are a beloved national treasure, my absolute favorite came from a hidden gem in Graça, still warm from the oven.
>
> But what truly makes Lisbon special isn't just the sights — it's the feeling. Wander just a block or two above the main squares and you'll discover a quieter, more authentic side of the city, inviting you to slow down and savor every moment.
>
> Of course, the must-see São Jorge Castle offers stunning views over the rooftops below. The queues can be long, but the experience is absolutely worth it for any history buff or curious traveler.
>
> Would I go back? Absolutely — next time in spring, and with better shoes! Lisbon isn't just a place to visit; it's a place to fall in love with, again and again. ✨

**After:**
> I spent five days in Lisbon last October. My hotel was up in Alfama, with a lot of stairs between it and everything else, and my legs felt every one of them. The views from the top were worth the climb.
>
> Everyone tells you to ride Tram 28, so I did. The trip took about forty minutes, and most of the car was other tourists taking pictures out the windows. The custard tarts at Pastéis de Belém are the famous ones, but my favorite came from a place in Graça, still warm from the oven.
>
> The part of Lisbon I liked best starts a block or two above the main squares, where the streets go quiet and nobody is in a hurry. São Jorge Castle has good views over the rooftops and a long queue to get them.
>
> I'd go back, in spring next time, and with better shoes.

## Sources

- [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) is the source for the pattern list.
- [WikiProject AI Cleanup](https://en.wikipedia.org/wiki/Wikipedia:WikiProject_AI_Cleanup) maintains the page.

## Version history

See [CHANGELOG.md](CHANGELOG.md).

## License

MIT. Copyright 2025 Siqi Chen (upstream); fork changes by Shakthivel Manivanan. See [LICENSE](LICENSE) and [PROVENANCE.md](PROVENANCE.md).

If Humanizer helps you, a star helps other people find it.
