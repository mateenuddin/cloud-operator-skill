# Eval Results

Iteration-by-iteration benchmark results.

## Pages

- **[Iteration 1](iteration-1.md)** — Initial AWS-only skill (3 evals × 2 conditions). Validated the Vantage workflow patterns A/B/C.
- **[Iteration 2](iteration-2.md)** — Multi-cloud expansion (6 evals × 2 conditions). Added GCP, Azure, runbook-fallback patterns. Mean pass rate 0.98 with-skill vs 0.87 without-skill.

## Reading the viewer

Each iteration links to a static HTML viewer that lets you click through every eval and see:

- The user's prompt
- The with-skill answer
- The without-skill answer
- Programmatic grading (assertion-by-assertion pass/fail)

Plus a Benchmark tab with pass rates, time, and tokens for each configuration.

If you want to reproduce the runs, see [Eval methodology](../guides/eval-methodology.md).
