# Multi-Cloud Cloud Operator Skill — Expansion Plan

How to grow the existing AWS-only Vantage skill into a true multi-cloud cloud-operator skill, with capability awareness and honest scope handling for MCPs that aren't connected.

---

## Goal

A single skill that, given any cloud-operator question, decides:

1. **Which cloud** is in scope (AWS / GCP / Azure / multi-cloud comparison)
2. **Which capability area** the question is in (pricing, compute ops, identity, observability, AI/GPU, etc.)
3. **Which MCP can actually do the work** today, or — if none — produces a runbook with the correct CLI/API calls and clearly says "you'll need to wire MCP X to make this executable"

This stays honest: the skill never pretends to provision when it can only read pricing, and never invents MCPs that aren't connected.

---

## New skill structure

```
cloud-operator/
├── SKILL.md                            # main: routing logic + capability decision tree
├── references/
│   ├── aws-pillars.md                  # (existing) AWS pillar quirks
│   ├── pricing-models.md               # (existing) pricing column navigation
│   ├── gcp-pillars.md                  # NEW — GCP service quirks (Vertex, Spanner, BQ, GKE)
│   ├── azure-pillars.md                # NEW — Azure quirks (Cosmos APIs, Synapse pools, AKS)
│   ├── operations-aws.md               # NEW — AWS operation cheatsheet (the new operations doc trimmed)
│   ├── operations-gcp.md               # NEW — GCP operation cheatsheet
│   ├── operations-azure.md             # NEW — Azure operation cheatsheet
│   ├── mcp-availability.md             # NEW — which MCPs are wired in this session, which need install, which are missing
│   └── runbook-templates.md            # NEW — patterns for "produce CLI / Terraform / Bicep when no MCP exists"
└── evals/
    └── evals.json                      # extend with GCP and Azure cases + at least one cross-cloud
```

The skill body stays under 500 lines. References are loaded only when they apply to the question — that's the point of progressive disclosure.

---

## Routing logic (the new heart of SKILL.md)

The expanded SKILL.md adds a routing pass at the top — before the workflow patterns it already has. Pseudocode:

```
1. Identify cloud(s) in scope.
   - Explicit mention ("EC2", "BigQuery", "AKS") → that cloud.
   - Generic terms ("VM", "instance", "object storage") with a region hint → infer.
   - Ask the user only if truly ambiguous.

2. Identify capability area.
   - Pricing / right-sizing / cost projection            → pricing patterns (existing A/B/C)
   - Resource lifecycle (create/start/stop/list/describe) → operator patterns (NEW)
   - Identity / policy / secret                          → identity patterns (NEW)
   - Metrics / logs / traces / alerts                    → observability patterns (NEW)
   - IaC / template / drift                              → IaC patterns (NEW)
   - Foundation models / training / inference endpoints  → AI patterns (NEW)

3. Check MCP availability for the cloud × capability cell.
   - If wired today → use the MCP.
   - If registered but not connected → tell the user "this needs MCP X — connect it via the connector menu, or I'll fall back to runbook output."
   - If only upstream (e.g. AWS Labs) → tell user "this would need plugin install" and produce a runbook in the meantime.
   - If no known MCP → produce a runbook (CLI / SDK / Terraform / Bicep) with caveats.

4. Execute or produce runbook.
```

This routing logic is the *only* part that fundamentally changes. The pricing patterns (A/B/C) carry over verbatim; they become one branch of the decision tree.

---

## Capability awareness — embedded in SKILL.md

A single source-of-truth table the skill reads:

```
| Capability       | AWS (today)                | GCP (today)        | Azure (today)        |
|------------------|----------------------------|--------------------|----------------------|
| Pricing/specs    | Vantage ✅                 | Vantage ✅          | Vantage ✅            |
| Cost actuals     | runbook (Cost Explorer)    | runbook (BQ export)| runbook (Cost Mgmt)  |
| Compute lifecycle| runbook (AWS CLI)          | GCE MCP 🟡          | runbook (az CLI)     |
| Storage ops      | runbook (S3 CLI)           | runbook            | runbook (az CLI)     |
| IAM/identity     | runbook                    | runbook            | runbook              |
| Observability    | runbook (CW)               | runbook            | runbook              |
| IaC              | runbook (CFN/Terraform)    | runbook (TF)       | runbook (Bicep)      |
| AI inference     | runbook (Bedrock SDK)      | runbook (Vertex)   | runbook (AOAI)       |
```

This table lives in `references/mcp-availability.md` and the skill knows to consult it before promising to do something. The skill *does not hardcode* server UUIDs — it references MCPs by name, and the runtime lookup happens via `list_connectors`-style introspection so the table updates automatically as new MCPs get connected.

---

## Runbook output — the always-available fallback

When no MCP is wired, the skill produces a runbook. Format:

```markdown
## What to run

Since no Compute Engine MCP is connected in your session, I'll produce a runbook.

### gcloud CLI
```bash
gcloud compute instances list \
  --project=YOUR_PROJECT \
  --filter="zone:us-central1-* AND status=RUNNING"
```

### Terraform (declarative)
```hcl
resource "google_compute_instance" "default" {
  name         = "example"
  machine_type = "e2-standard-2"
  ...
}
```

### Equivalent Python (google-cloud-compute)
```python
from google.cloud import compute_v1
...
```

If you want me to actually execute this, install the **Google Compute Engine MCP** (in the registry, not yet connected) and re-run.
```

This keeps the agent honest, useful, and offers an upgrade path.

---

## Extending evals

The current `evals/evals.json` has 3 AWS cases. The expansion adds:

- **Eval 4** — GCP right-sizing: "Pick a Compute Engine instance for a 16-vCPU 64GB BigQuery query worker in us-central1. Compare against the equivalent AWS EC2 cost."
- **Eval 5** — Azure pricing: "What does an `Standard_D8s_v5` cost in `eastus` for 24/7 operation? Show on-demand and 3-yr Reserved."
- **Eval 6** — Compute lifecycle (operator action): "Stop all `t2.*` and `t3.*` EC2 instances in `us-east-1` that are tagged `env=dev`." Tests runbook output when EC2 management MCP isn't wired.
- **Eval 7** — Cross-cloud comparison: "We're running 12 EC2 m6i.4xlarge in us-east-1 24/7. What would the equivalent on GCP and Azure cost?"
- **Eval 8** — AI cost: "We want to run a Llama-3-70B inference workload. Compare GPU instances on AWS, GCP, and Azure for ~50 tokens/sec throughput." Tests the AI/GPU branch.
- **Eval 9** — Observability runbook: "Show me CPU and memory utilization for `i-0123abc` over the last 24 hours." Tests CloudWatch runbook output.

Each new eval gets specific assertions ("includes runbook section when MCP not wired", "asks the user to confirm region when ambiguous", "uses Vantage GPU index for any GPU question").

---

## Iteration plan

Three iterations to get the multi-cloud skill stable:

1. **Iteration 2 (next)** — Add the routing pass, GCP and Azure pillar references, and `mcp-availability.md`. Re-run the existing 3 AWS evals + add 2 new GCP and Azure pricing evals. Verify the AWS evals still pass.
2. **Iteration 3** — Add operator-action evals (lifecycle, observability, IaC) that test runbook output quality. Add the runbook templates reference. Refine until runbook output is consistently useful even when no MCP is wired.
3. **Iteration 4** — AI/GPU branch + cross-cloud comparison eval. Polish the routing logic against any failure modes that surfaced.

Description optimization (`run_loop.py`) at the end of iteration 4 once the scope is fully baked.

---

## Risks and how to mitigate

| Risk | Mitigation |
| --- | --- |
| Skill becomes >500 lines — hard for the model to load efficiently | Aggressive use of references; SKILL.md only has routing + the pricing patterns; everything else lives in references. |
| Model confidently produces runbooks for clouds with no MCP, hallucinating CLI flags | Runbook templates reference includes verified syntax; encourage Claude to flag uncertainty rather than invent. |
| Vantage MCP becomes the entire skill's identity — feels like a Vantage wrapper not a cloud-operator skill | Keep pricing patterns as one of N branches; demos in evals deliberately exercise non-pricing flows. |
| New MCPs appear in registry that we miss | The `mcp-availability.md` table is a generated artifact, not hand-written — we re-run a registry-scan script as part of CI / before each iteration. |
| Cross-cloud comparisons drift due to different cost models (GCP CUDs auto-apply; AWS RIs do not) | `references/pricing-models.md` is extended with a "cross-cloud comparison checklist" so the skill normalizes these before reporting deltas. |

---

## Naming and packaging

- Rename the existing `aws-cloud-operator/` directory to `cloud-operator/` to reflect the broader scope.
- Update the skill `name` frontmatter to `cloud-operator` and rewrite the description to be cloud-agnostic, while keeping it pushy about pricing/sizing triggers.
- Re-package as `cloud-operator.skill` once iteration 4 is happy.
- Old AWS-only artifact remains in the workspace history if the user wants to roll back.
