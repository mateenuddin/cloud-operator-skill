# Skill Evals

The skill is validated against a suite of realistic prompts. Each eval has a prompt, an expected-output description, and a list of verifiable assertions. The full source lives at [`evals/evals.json`](https://github.com/YOUR-USERNAME/cloud-operator-skill/blob/main/docs/skill/evals/evals.json).

## Eval list

### 1. ec2-cost-lookup-spot-vs-ondemand

**Prompt:** We're running a batch ETL on m5.2xlarge in us-east-2, about 8 hours a day. Right now it's all on-demand Linux. What would Spot cost us, and is it actually a good idea here? We don't checkpoint between rows but the whole job is restartable from scratch in like 20 min if it dies.

**Expected:** Pattern A. Direct, concrete answer that calls get-ec2-region-pricing for m5.2xlarge in us-east-2, contrasts on-demand vs Spot Avg/Max, surfaces the Spot interrupt frequency rating, and gives a defensible recommendation.

**Assertions:**

- Calls get-ec2-region-pricing for m5.2xlarge in us-east-2
- Reports a specific on-demand Linux hourly price
- Reports a specific Spot price (min/avg/max)
- Surfaces the Spot interrupt frequency rating from Vantage
- Makes a recommendation appropriate to a restartable batch job
- Does not dump the full Windows / SQL Server / Dedicated rows

### 2. ec2-right-sizing-with-constraints

**Prompt:** I need to pick an EC2 instance for a memory-heavy ML inference service. Constraints: at least 64 GB RAM, at least 1 GPU, current generation only, running in us-west-2, and ideally under $3/hr on-demand. What should I use and how much will it cost? Compare a couple of options.

**Expected:** Pattern B + Pattern G. Uses get-ec2-indexes for RAM/GPU/price intersection, calls get-ec2-instance + get-ec2-region-pricing for 2-3 finalists in parallel.

**Assertions:**

- Calls get-ec2-indexes (or otherwise consults the index list)
- Filters by both RAM and GPU constraints
- Filters by the under-$3/hr on-demand band
- Calls get-ec2-instance for at least 2 finalist instance types
- Calls get-ec2-region-pricing in us-west-2 for finalists
- Recommends current-generation instances (not g3, g2, p2)
- Produces a small comparison table
- Reports actual specs and prices, not invented values
- Mentions the GPU type explicitly (A10G / L4 / L40S / etc.)

### 3. rds-engine-and-region-comparison

**Prompt:** We're standing up a Postgres database for a SaaS app. Expecting around 32 GB working set, mostly OLTP, maybe 8 vCPUs is fine. We're stuck between us-east-1 and eu-central-1 (data residency conversation is ongoing). For RDS Postgres, can you pick an instance class and tell me what it costs in each region, on-demand and on a 1yr Savings Plan / Reserved deal? Bonus: rough sense of how much more this is than running it on EC2 ourselves.

**Expected:** Pattern A + C. Picks a current-gen db.r-class or db.m-class .2xlarge. Calls get-rds-region-pricing for both regions. PostgreSQL row.

**Assertions:**

- Picks a memory-or-general-purpose db-class with at least 32 GB RAM
- Picks a current-generation RDS instance (db.r6i, db.r7i, db.m7i, or similar)
- Calls get-rds-region-pricing for both us-east-1 and eu-central-1
- Filters to the PostgreSQL engine row
- Acknowledges RDS commitment terminology accurately
- Reports a 1yr commitment price in addition to on-demand
- Either compares to EC2 explicitly, or notes the managed-vs-DIY tradeoff

### 4. gcp-right-sizing-with-aws-comparison

**Prompt:** We're standing up a worker that processes about 20 GB of data per BigQuery query. Need 16 vCPU and 64 GB RAM, in us-central1. Can you pick a current-gen Compute Engine machine type and tell me on-demand price, plus what it would cost as a 1-year CUD? Also for sanity-check, what's the closest equivalent on AWS in us-east-1?

**Expected:** Pattern B + C with cross-cloud comparison. Vantage GCP indexes / instances + cross-cloud AWS comparison.

**Assertions:**

- Picks a current-generation GCP machine type with 16 vCPU + 64 GB RAM
- Calls a Vantage GCP pricing tool (get-gcp-region-pricing or similar)
- Reports both on-demand and 1-year CUD pricing (or Sustained Use Discount) for GCP
- Picks a comparable AWS instance (m6i.4xlarge or m7i.4xlarge or similar)
- Calls get-ec2-region-pricing for the AWS option in us-east-1
- Produces a side-by-side comparison table or structured comparison
- Notes a caveat about CUDs vs SP/RI commitment differences OR Sustained Use Discounts
- Does not invent prices

### 5. azure-pricing-on-demand-vs-reserved

**Prompt:** What does an Standard_D8s_v5 cost in eastus for 24/7 operation? Show me on-demand and 3-yr Reserved pricing. I'm trying to budget for ~10 of these.

**Expected:** Pattern A. Calls Vantage Azure pricing for Standard_D8s_v5 in eastus.

**Assertions:**

- Calls a Vantage Azure pricing tool for Standard_D8s_v5 in eastus
- Reports a specific on-demand Linux hourly price
- Reports a specific 3-yr Reserved (or Savings Plan) price
- Computes monthly cost (hourly x 730)
- Scales for 10 instances
- Does not dump non-Linux rows (Windows, SQL Server) unless asked

### 6. operator-action-runbook-fallback

**Prompt:** We have a bunch of dev EC2 instances tagged env=dev that get left running over the weekend. Can you stop all of them in us-east-1 right now? They should auto-restart Monday morning.

**Expected:** Pattern D. Recognize as mutating EC2 action with no wired EC2-management MCP. Produce CLI runbook. Don't pretend to execute.

**Assertions:**

- Does NOT claim to have stopped instances on the user's behalf
- Produces an AWS CLI snippet with tag:env=dev filter
- Produces an AWS CLI snippet with stop-instances
- Mentions or addresses Monday auto-restart (cron / EventBridge / scheduled task)
- Notes that no EC2 management MCP is wired
- Output is a clearly labeled runbook section, not pretending to be live execution


## Running the evals

See [Eval methodology](../guides/eval-methodology.md) for the full procedure: spawn with-skill / without-skill subagents, capture timing, grade assertions, aggregate into benchmark.json, generate the static HTML viewer for human review.
