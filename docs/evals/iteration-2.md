# Iteration 2 — Multi-cloud expansion

Renamed `aws-cloud-operator` to `cloud-operator`. Added GCP and Azure pillar references, MCP-availability map, runbook templates, and three new evals (GCP cross-cloud, Azure pricing, operator-action runbook fallback).

## Headline

| Metric | with-skill | without-skill | delta |
| --- | --- | --- | --- |
| Mean pass rate | 0.98 | 0.87 | +0.11 |
| Mean tokens | ~96k | ~75k | +28% |

## Big wins for the skill

| Eval | Without-skill failure | With-skill recovery |
| --- | --- | --- |
| Eval 5 (Azure pricing) | Claimed *"Vantage MCP database lacks Standard_D8s_v5 pricing"* and gave up | Successfully retrieved $0.576/hr OD and $0.319/hr 3-yr Reserved |
| Eval 6 (operator runbook) | Punted with vague "use AWS CLI like…" + offered to take over the user's terminal | Applied Pattern D: labeled runbook with tag-filtered `aws ec2 stop-instances` + EventBridge stub for Monday auto-restart, explicitly noted no EC2-management MCP wired |
| Eval 4 (cross-cloud) | Picked AWS m5zn.3xlarge — *only 12 vCPU + 48 GB*, doesn't meet the 16/64 spec | Picked m7i.4xlarge correctly |

## What still needs work

- Eval 3 (RDS) — both configurations still mislabel "Savings Plan" for RDS in places. RDS uses Reserved Instances. Tighten in iteration 3.
- Iter 2 saw subagent file-save bugs that required path consolidation — eval infrastructure issue, not skill behavior.
- Cross-cloud comparison rounding errors in Eval 4 — values match per-cloud lookups but the deltas in the comparison table need a sanity-check pass.

## Artifacts

- [Static review viewer (HTML)](results/iteration-2-review.html) — side-by-side with iteration 1 outputs
- [Benchmark JSON](results/iteration-2-benchmark.json)

## Decision

Ship as iteration 2. Roadmap for iteration 3:

1. Tighten RDS commitment terminology (assertion: explicit "RDS uses Reserved Instances, not Savings Plans" sentence required).
2. Add observability via Datadog MCP (Pattern E becomes wired for the first time).
3. Flesh out Pattern F (IaC) with drift-detection eval.
4. Run description-optimization (`run_loop.py`) to tune the trigger description across ~20 trigger eval queries.
