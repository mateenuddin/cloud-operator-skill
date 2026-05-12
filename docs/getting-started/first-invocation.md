# First invocation

Three questions to ask Claude after install. Each demonstrates a different workflow pattern.

## 1. Cost lookup (Pattern A)

> *We're running a batch ETL on m5.2xlarge in us-east-2, about 8 hours a day. What would Spot cost us, and is it actually a good idea here?*

**What good output looks like:**

- Single tool call to `get-ec2-region-pricing` for `m5.2xlarge` in `us-east-2`
- Linux on-demand: ~$0.384/hr
- Spot avg: ~$0.087/hr (77% off)
- **Surfaces the >20% Spot interrupt frequency** (this is the make-or-break detail)
- Recommends Spot *with caveat* — appropriate for a restartable batch
- One small table, no full pricing matrix dump

If Claude dumps the entire OS × pricing-model grid, the skill is undertriggering — it should be filtering to Linux on-demand by default.

## 2. Right-sizing with constraints (Pattern B)

> *I need to pick an EC2 instance for a memory-heavy ML inference service. Constraints: at least 64 GB RAM, at least 1 GPU, current generation only, running in us-west-2, and ideally under $3/hr on-demand. What should I use and how much will it cost?*

**What good output looks like:**

- `get-ec2-indexes` call (proves the skill is using the index-first fast path)
- Multiple `use-ec2-index` calls intersected (RAM band + GPU band + price band)
- Two or three finalists fetched in **parallel** via `get-ec2-instance` and `get-ec2-region-pricing`
- A small comparison table
- Recommends a current-gen GPU family (g5 / g6 / g6e) — *not* g3 / g2 / p2
- Mentions GPU type explicitly (A10G / L4 / L40S) — the spec matters for inference latency

If Claude does naive "let me list all GPU families" enumeration, point it at [`docs/skill/SKILL.md`](../skill/SKILL.md) Pattern B explicitly.

## 3. Cross-cloud comparison (Pattern C)

> *We're standing up a worker that needs 16 vCPU and 64 GB RAM in us-central1 GCP. Can you pick a current-gen Compute Engine machine type and tell me on-demand price plus 1-year CUD? Also for sanity-check, what's the closest equivalent on AWS in us-east-1?*

**What good output looks like:**

- GCP pick (e.g., `n2-standard-16` or `n4-standard-16`) with on-demand and 1-yr CUD pricing
- AWS pick (e.g., `m7i.4xlarge` — exact spec match, current-gen)
- Side-by-side comparison table
- Honest caveat about CUDs (auto-applied) vs Savings Plans (purchased commitment)
- *Doesn't* normalize away the silicon difference — calls out Intel Sapphire Rapids vs Granite Rapids if relevant

## Pattern recognition

If you see Claude's output skipping these signals, the skill may not be loaded or may be undertriggering. Check `available_skills` for `cloud-operator` and try a more explicit prompt mentioning pricing / sizing / cost.

## Common stumble: vague regions

A user-friendly thing to ask is *"how much in Mumbai?"* — but the skill needs the region code (`ap-south-1`). Modern Claude will translate, but be explicit if you can. The skill defaults to `us-east-1` if no region is mentioned and labels that assumption.

## What to try next

- **Operator action (Pattern D)** — *"List all my running EC2 instances tagged env=dev in us-east-1"*. Should produce a runbook (no EC2-management MCP wired by default), not a fake response.
- **Observability (Pattern E)** — *"Show me CPU usage for i-0123abc over the last 24 hours"*. Same — runbook with `aws cloudwatch get-metric-data` command.
- **AI / GPU (Pattern G)** — *"Compare GPU instance options for Llama-3-70B inference across AWS, GCP, and Azure"*. Multi-cloud Pattern G + B.

Each of these is in [Cloud-operator concepts](concepts.md) with the exact pattern code and what success looks like.
