# Cloud Operator Skill

A multi-cloud operator agent skill for **AWS, GCP, and Azure** — built on the Claude Agent SDK. The skill turns Claude into a competent cost analyst, right-sizing advisor, and operations assistant, grounded in live data from connected MCPs.

!!! tip "New here? Start with [Getting Started](getting-started/index.md)"
    Five-minute install, then a guided first invocation against the Vantage pricing MCP.

## What this skill does

| Capability | What it covers |
| --- | --- |
| **Pricing & right-sizing** | EC2 / RDS / ElastiCache / OpenSearch / Redshift on AWS, plus GCP and Azure compute. Index-first intersection for fast filtering. |
| **Cross-cloud comparison** | Normalize a workload across AWS / GCP / Azure with honest CUDs vs SP/RI caveats. |
| **Resource lifecycle** | List / start / stop / modify via wired MCPs; runbook output (CLI / Terraform / Bicep) when no MCP is wired. |
| **Identity & secrets** | IAM, KMS, Secrets Manager / Key Vault — runbook-backed today. |
| **Observability** | Metrics / logs / traces — runbook-backed; Datadog MCP integration roadmapped. |
| **AI / GPU** | GPU instance selection via Vantage indexes; foundation-model invocation routing (Bedrock / Vertex / Azure OpenAI). |

## How it's organized

<div class="grid cards" markdown>

-   :material-rocket-launch: **[Getting Started](getting-started/index.md)**

    ---
    Install the skill, run your first prompt, learn the core concepts.

-   :material-book-open-variant: **[The Skill](skill/index.md)**

    ---
    The actual `SKILL.md` plus all reference files. This is what Claude reads.

-   :material-format-list-bulleted-square: **[Reference Catalog](reference/index.md)**

    ---
    Service catalog, operations catalog, interactive mindmap.

-   :material-school: **[Guides](guides/index.md)**

    ---
    How to extend the skill, eval methodology, adding new MCPs.

-   :material-chart-bar: **[Eval Results](evals/index.md)**

    ---
    Iteration-by-iteration benchmark results and review viewers.

</div>

## Browse every resource

Direct links to every catalog, pillar reference, and template — also reachable from the left sidebar or via search.

### The cloud-operator toolset

- [**Service catalog**](reference/service-catalog.md) — ~245 services across AWS, GCP, and Azure organized by capability (compute, storage, database, networking, identity, observability, ML, integration). One-line "what it does" per entry.
- [**Operations catalog**](reference/operations-catalog.md) — drills from service to actual API operations (e.g. `aws_ec2_describe_instances`, `gcp_compute_list_instances`, `azure_vm_resize`), each annotated with MCP-availability status.
- [**Interactive mindmap**](reference/mindmap.md) — same hierarchy as a pannable / zoomable Mermaid diagram with 283 nodes.

### The pricing pillars (per-cloud reference)

- [**AWS pillars**](skill/references/aws-pillars.md) — EC2, RDS, ElastiCache, OpenSearch, Redshift family conventions, engine pricing, gotchas.
- [**GCP pillars**](skill/references/gcp-pillars.md) — Compute Engine, Cloud SQL, AlloyDB, Spanner, BigQuery, GKE, Memorystore, Vertex AI quirks.
- [**Azure pillars**](skill/references/azure-pillars.md) — VM series, SQL DB, Cosmos DB, Synapse, AKS, Cache for Redis, Azure OpenAI deployment types.
- [**Pricing models**](skill/references/pricing-models.md) — on-demand / Spot / Savings Plans / Reserved Instances / CUDs. The wide pricing-matrix navigation guide.

### Tooling and operations

- [**MCP availability map**](skill/references/mcp-availability.md) — which MCPs cover which (cloud × capability) cells, what's connected today, what's wirable, what's still custom.
- [**Runbook templates**](skill/references/runbook-templates.md) — verified `aws` / `gcloud` / `az` CLI plus Terraform / Bicep snippets to drop into the agent's output when no MCP is wired.

### Methodology

- [**SKILL.md**](skill/SKILL.md) — the actual skill body Claude reads (routing logic + seven workflow patterns).
- [**Skill expansion roadmap**](guides/expansion-plan.md) — design doc for evolving the skill scope.
- [**Eval methodology**](guides/eval-methodology.md) — the full benchmark loop.
- [**Iteration 1 results**](evals/iteration-1.md) · [**Iteration 2 results**](evals/iteration-2.md) — measured progress.

## Quick search

Use the search box at the top of every page (or press `/` to focus it). The site indexes every page and every code snippet — typing "spot interrupt", "savings plan", "n2-standard", "Granite Rapids", "pricing pillar", or "stop EC2" jumps straight to the relevant section.

## Wired MCPs at a glance

| MCP | Purpose | Status in this repo's reference setup |
| --- | --- | --- |
| Vantage `instances` | Pricing across AWS / GCP / Azure compute & data pillars | ✅ Required — the skill assumes it's connected |
| Google Compute Engine | GCE VM management (29+ tools) | 🟡 Optional — connect for live GCE actions |
| Google Cloud BigQuery | SQL execution + dataset introspection | 🟡 Optional — connect for billing-export queries |
| AWS Marketplace | Marketplace discovery & evaluation | 🟡 Optional |
| Datadog | Cross-cloud observability | 🟡 Optional, pending integration |

See the full [MCP availability map](skill/references/mcp-availability.md) for which (cloud × capability) cells are wired today.

## Project status

Iteration 2 shipped — 6 evals × 2 conditions, with-skill mean pass rate **0.98**. Iteration 3 will tighten RDS commitment terminology, add observability via Datadog, and flesh out IaC drift workflows.

## License

[MIT](https://github.com/YOUR-USERNAME/cloud-operator-skill/blob/main/LICENSE) — free to use, modify, fork.
