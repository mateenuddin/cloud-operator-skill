# Iteration 1 — AWS-only baseline

First pass at the skill. Three evals × two conditions (with-skill vs no-skill). Used the Vantage MCP exclusively for AWS pricing.

## Headline

| Metric | with-skill | without-skill | delta |
| --- | --- | --- | --- |
| Mean pass rate | 1.00 | 0.92 | +0.08 |
| Mean tokens | ~91k | ~82k | +11% |

## What worked

- The index-first right-sizing pattern (Pattern B) consistently produced shorter, more focused responses.
- The "don't dump the full pricing matrix" guidance held — both configurations were comparable on length, but with-skill output was better organized.
- Skill explicitly cited Vantage's `>20%` Spot interrupt frequency rating; without-skill agents sometimes contradicted it from training-data memory.

## What needed work

- Assertions weren't discriminating enough — both configurations passed too many of them. The qualitative differences were larger than the numbers suggested.
- Without-skill answers occasionally hallucinated: in Eval 2, claimed `g6e.2xlarge` had 48 GB RAM (actual: 64 GB) and dismissed the option based on the false fact.
- Without-skill in Eval 3 picked older-generation `db.m5.2xlarge` instead of current-gen `db.m7i.2xlarge`.
- Both configurations may have mislabeled RDS pricing columns as "Savings Plans" — RDS uses Reserved Instances (worth verifying against the raw matrix).

## Artifacts

- [Static review viewer (HTML)](results/iteration-1-review.html) — click through each eval, see assertion grades
- [Benchmark JSON](results/iteration-1-benchmark.json) — machine-readable results

## Decision

Ship as iteration 1, then immediately scope iteration 2 to cover GCP + Azure + runbook fallback for operator actions.
