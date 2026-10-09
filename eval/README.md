# Humanizer eval

A small harness for checking whether a change to `SKILL.md` makes rewrites read more like a person wrote them, without adding or losing facts.

## What is here

- `samples/`: 23 AI-written texts (blog, email, technical, essay, Slack, academic, report, reflective). Each has a `facts` list in its front matter, and many have `keep`/`forbid` patterns for claims whose strength must not change, `may_drop` for numbers a reply may leave out, and `states_feeling: true` when the source expresses a feeling the word list misses. The rewriter never sees the front matter; the judge does. Samples 19 to 23 bait the fidelity failure modes.
- `prompts/`: the exact prompt each sample is sent with (no front matter; replies include the thread they answer). `run.py` builds a missing one.
- `skills/`: one frozen copy of the skill per version. `v4-final.md` is the shipped `SKILL.md`; `v4-final-r1.md` and `v4-final-r2.md` are earlier drafts of 4.0, kept with their runs and judgments as `*-r1` and `*-r2`.
- `runs/<label>/`: the final rewrite of each sample by one skill version.
- `blind/<A>-vs-<B>/`: blind pairwise judgments and the key that unblinds them.
- `tells.py`: counts AI tells, overcorrection signs, and register signals (participial clauses, nominalizations, agentless passives, stock transitions, overclaims, hedges, lexical diversity) per 100 words. No model needed.
- `test_fidelity.py`: deterministic fidelity tests (magnitude, numbers, invented feelings). `--self-test` checks the checker.
- `judge_prompt.md`, `rewrite_prompt.md`: the shared prompts for rewriting and judging.
- `run.py`, `judge.py`: run the whole loop with the `claude` CLI.
- `blind_pairs.py`: builds blind pair files and tallies them when judges are run some other way (for example, as agents).
- `human_eval.py`, `human/`: printable blind packets for human readers (4.0 vs 3.1.0 and 4.0 vs step 5), two versions each with X and Y swapped, plus a response template. `python3 eval/human_eval.py tally <A> <B> --keydir <dir>` scores the returned CSVs. Keep the key out of readers' reach; the 4.0 keys are stored outside the repository.

## Run it

Check the checkers and score every run, no model needed:

```bash
python3 eval/test_fidelity.py --self-test
```

```bash
python3 eval/test_fidelity.py v4-final -v
```

`test_fidelity.py` exits with status 1 if a named run has any magnitude, number, or invented-feeling failure, so it can gate a release.

Score every run without a model:

```bash
python3 eval/tells.py
```

Score one genre only (`blog`, `email`, `tech`, `essay`, `slack`, `academic`, `report`, `reflective`):

```bash
python3 eval/tells.py academic
```

Rewrite all samples with a skill version and judge it against another, using a logged-in `claude` CLI:

```bash
python3 eval/run.py eval/skills/v4-step5.md v4-step5
```

```bash
python3 eval/judge.py v3.1.0 v4-step5
```

Set `CLAUDE_BIN` if `claude` is not on your PATH.

If you run rewriters and judges some other way (the 4.0 results used separate agent sessions, because the CLI was not logged in for headless use), build the blind files with `blind_pairs.py make A B --keydir <dir outside the repo>`, have one judge per `order0.md`/`order1.md` write `judgments0.json`/`judgments1.json`, then run `blind_pairs.py tally A B --keydir <dir>`. The tally copies the key into `blind/` so the result can be checked later.

## How to read the results

The judge answers two questions per sample: which rewrite reads more like a person wrote it, and which keeps the facts without inventing any. Each sample is judged twice with X and Y swapped. A version wins a sample only if it wins both times; a split counts as a tie. With 23 samples, a margin of two or three is noise. Look for wins in both columns and read the `why` lines.

`tells.py` catches regressions a judge can miss, such as a version that starts adding "Let me know" to every reply. It cannot tell a good rewrite from a bad one on its own.
