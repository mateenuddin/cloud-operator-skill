# Cloud-operator concepts

The mental model for how the skill thinks. Read this once and the rest of the docs will make sense.

## The routing pass

Before the skill does anything, it identifies three things from the user's question:

1. **Which cloud** — explicit (EC2, BigQuery, AKS) or implicit (region hints).
2. **Which capability** — pricing, lifecycle, identity, observability, IaC, or AI/GPU.
3. **Inspection vs. mutation** — read-only or does-something.

Then it picks one of seven workflow patterns.

## The seven workflow patterns

| Pattern | Trigger | What it does |
| --- | --- | --- |
| **A — Cost lookup** | "How much does X cost in region R?" | One pricing call, filter to the OS/term row, surface the column the user cares about. |
| **B — Right-sizing** | "Pick an instance that meets X constraints." | Index-first intersection: pull `get-*-indexes`, intersect candidates, then enrich 2–3 finalists in parallel. |
| **C — Cross-region / cross-cloud comparison** | "Compare X across regions / providers." | Parallel pricing calls, normalized table, honest caveats (CUDs vs SP/RI, silicon differences). |
| **D — Resource lifecycle** | "List / start / stop / modify resources." | Use wired MCP if available; otherwise produce a labeled runbook (CLI / Terraform / Bicep). |
| **E — Observability** | "Show me metrics / logs / traces." | Read-only by default; runbook fallback when no MCP is wired. |
| **F — IaC** | "Deploy / drift / plan." | Produce template + deploy command; never execute. |
| **G — AI / GPU** | "Foundation model / GPU instance / ML platform." | Three sub-patterns: model invocation, ML platform ops, GPU compute provisioning. |

## The runbook fallback

When the user asks for an action and no MCP is wired for it, the skill **does not** pretend to act. Instead it:

1. Tells the user *"this needs MCP X, which isn't connected."*
2. Produces a precise CLI / Terraform / Bicep snippet they can run themselves.
3. Optionally suggests the connector if there's one in the registry.

This is the difference between a useful operator skill and a hallucinating one. The skill never claims to have stopped an EC2 instance it cannot actually stop.

## The pricing matrix

Vantage's `get-*-region-pricing` returns a wide table — up to ~14 OS rows × ~24 pricing columns. Most of those are noise for any one question. The skill teaches Claude to:

- Pick the right OS row (Linux default for EC2; PostgreSQL default for RDS; Redis default for ElastiCache).
- Pick the right pricing column based on workload duty cycle (24/7 → Reserved/SP; bursty → on-demand; restartable → Spot).
- Surface only the columns the user cares about — not the full grid.

See [`pricing-models.md`](../skill/references/pricing-models.md) for the column-by-column reference.

## The capability awareness table

Every (cloud × capability) cell has an MCP-availability status:

- ✅ **Connected today** — call the MCP directly.
- 🟡 **Registered but not connected** — ask the user to connect, then call.
- 🟦 **Upstream available** — published by AWS Labs / Microsoft / community; needs install.
- ❌ **No known MCP** — runbook is the only path.

The skill consults this table before promising to act. See [`mcp-availability.md`](../skill/references/mcp-availability.md).

## The five AWS pillars (and their GCP / Azure equivalents)

Vantage organizes its data around five "high-cost pillars":

| Vantage pillar | What it is | GCP equivalent | Azure equivalent |
| --- | --- | --- | --- |
| EC2 | Compute | Compute Engine | Virtual Machines |
| RDS | Managed relational DB | Cloud SQL / AlloyDB | Azure SQL DB / DB for PG/MySQL |
| ElastiCache | Managed Redis / Memcached | Memorystore | Cache for Redis |
| OpenSearch | Managed search / log analytics | (no direct; OpenSearch on GKE) | (no direct; community offerings) |
| Redshift | Cloud data warehouse | BigQuery (different model) | Synapse (dedicated SQL pool) |

Pillar-specific quirks live in the per-cloud reference files: [aws-pillars.md](../skill/references/aws-pillars.md), [gcp-pillars.md](../skill/references/gcp-pillars.md), [azure-pillars.md](../skill/references/azure-pillars.md).

## Honesty as a design principle

Three things the skill explicitly will not do:

- **Invent prices.** Always calls the MCP. The pricing model is too dimensional for memory-based estimation.
- **Pretend to act.** Every mutation needs a wired MCP or a runbook handoff.
- **Hide caveats.** Spot interrupt frequency, region availability, silicon differences, and CUDs-vs-RI mechanics all surface explicitly.

This is the difference between a skill that's useful in production and one that produces confident-sounding garbage.
