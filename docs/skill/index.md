# The Skill

This section holds the actual `SKILL.md` and reference files that Claude reads when this skill is loaded. If you're installing the skill, this is what you copy.

## Files

- **[SKILL.md](SKILL.md)** — The skill body. Routing logic, seven workflow patterns, output format guidance.
- **References** — Loaded only when relevant to the question Claude is answering:
    - [aws-pillars.md](references/aws-pillars.md) — EC2 / RDS / ElastiCache / OpenSearch / Redshift quirks
    - [gcp-pillars.md](references/gcp-pillars.md) — Compute Engine / Cloud SQL / Spanner / GKE / Vertex / BigQuery quirks
    - [azure-pillars.md](references/azure-pillars.md) — VM / SQL DB / Cosmos / AKS / Synapse / OpenAI quirks
    - [pricing-models.md](references/pricing-models.md) — On-demand / Spot / Savings Plans / RIs decision heuristic
    - [mcp-availability.md](references/mcp-availability.md) — Which MCPs cover which (cloud × capability) cells
    - [runbook-templates.md](references/runbook-templates.md) — Verified CLI / Terraform / Bicep snippets

## How progressive disclosure works

The skill body is always loaded when the skill triggers (~500 lines). Reference files are loaded **only** when the skill mentions them — either by following a link or by the agent recognizing a keyword. This keeps Claude's context lean while giving it deep knowledge on demand.

When you change a reference file, it doesn't change the skill's triggering surface — it just changes what Claude pulls when a relevant question appears.

## Eval suite

The eval suite that validates this skill lives at [`evals.json`](evals.md). Iteration 2 ran 6 evals × 2 conditions; with-skill mean pass rate was 0.98. Full benchmark and viewer in the [Eval Results](../evals/index.md) section.
