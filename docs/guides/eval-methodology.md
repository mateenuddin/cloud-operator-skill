# Eval Methodology

How to validate the skill — the same loop the maintainers run between iterations.

## Why evals matter for skills

A skill that works on the three prompts you tested might fail on the millionth. Evals are how you know your changes don't regress, how you tell the user "this is iteration 2 and here's what got better," and how you decide when to ship. The bar for shipping iteration N is *measurably* better than iteration N-1, not just "feels better."

## The loop

```
1. Snapshot the existing skill (if iterating)
2. Edit the skill
3. Spawn N evals × 2 conditions (with-skill / without-skill)
4. Capture per-run timing and tool counts
5. Grade each run programmatically against assertions
6. Aggregate into benchmark.json
7. Generate static HTML review viewer
8. Read user's qualitative feedback (feedback.json)
9. Decide: ship, iterate, or roll back
```

## Setting up the workspace

The maintainers use the [skill-creator](https://github.com/anthropics/skills/tree/main/skill-creator) helper which provides scripts for steps 6–7. Workspace layout:

```
<workspace>/
├── iteration-1/
│   ├── eval-1-<name>/
│   │   ├── with_skill/
│   │   │   ├── outputs/answer.md
│   │   │   ├── timing.json
│   │   │   └── grading.json
│   │   └── without_skill/
│   │       └── (same structure)
│   ├── eval-2-<name>/
│   │   └── ...
│   └── benchmark.json
├── iteration-2/
│   └── ...
```

## Spawning runs

Each eval × condition runs in its own subagent. Subagents run in parallel and each produces an `answer.md` and `metrics.json`.

Critical detail: subagents in some environments save files to the wrong path silently. Always have the subagent run `ls -la` on the target directory after writing and report what it sees. Verify before grading.

## Grading

Two grading modes:

**Programmatic** — write assertions as boolean expressions over the answer text. Cheap, repeatable, scales. Use this when assertions are objectively verifiable (specific number present, specific tool called, specific keyword surfaced).

**LLM-as-judge** — pass the answer + assertion to a separate Claude call and ask "did the answer satisfy this assertion?" Use this when assertions need judgment (tone, completeness, defensible recommendation).

Mixed mode is fine — many evals have a mix.

## Discriminating assertions

The biggest pitfall: assertions that pass for both with-skill and without-skill, telling you nothing. Look for assertions that *discriminate* between configurations. Examples:

- ❌ "Output mentions a price" — both will, since both call the MCP. Non-discriminating.
- ✅ "Output cites the >20% Spot interrupt frequency from Vantage" — without-skill agents tend to gloss this. Discriminating.
- ❌ "Output is a runbook" — both might produce one. Non-discriminating if grader matches loosely.
- ✅ "Output explicitly notes that no EC2-management MCP is wired" — only the skill teaches this. Discriminating.

If your benchmark shows pass rates close to 1.0 for both, your assertions aren't discriminating. Tighten or replace.

## Aggregating into benchmark.json

Use the skill-creator's `aggregate_benchmark.py`:

```bash
python -m scripts.aggregate_benchmark <workspace>/iteration-N --skill-name cloud-operator
```

Or write benchmark.json by hand following the schema in [`schemas.md`](https://github.com/anthropics/skills/blob/main/skill-creator/references/schemas.md). Key fields the viewer needs:

- `runs[].configuration` — must be exactly `"with_skill"` or `"without_skill"` (the viewer color-codes by this string)
- `runs[].result.pass_rate` — 0.0 to 1.0
- `run_summary.delta` — string deltas like `"+0.107"`, `"+13.0"`, `"+1700"`

## The static HTML viewer

```bash
python <skill-creator>/eval-viewer/generate_review.py \
  <workspace>/iteration-N \
  --skill-name "cloud-operator (iteration N)" \
  --benchmark <workspace>/iteration-N/benchmark.json \
  --previous-workspace <workspace>/iteration-<N-1> \
  --static <output_path>
```

The viewer has two tabs: **Outputs** (click through each eval, leave feedback per run) and **Benchmark** (pass rates, time, tokens, deltas). For iteration 2+, `--previous-workspace` shows the previous iteration's outputs in a collapsible "Previous Output" panel under each new run — instant regression check.

## Reading feedback

The viewer downloads `feedback.json` when the user clicks "Submit All Reviews". Empty feedback = the user thought it was fine. Focus iteration N+1 on test cases with specific complaints.

## When to ship

Three signals it's time to ship:

1. Pass rate stable across two consecutive iterations.
2. User feedback shows no major issues, only nice-to-haves.
3. Token / time costs aren't growing with quality (or growth is acceptable for the gain).

When you do ship, also run **description optimization** (see the skill-creator) to tune the skill's `description` field for triggering accuracy.
