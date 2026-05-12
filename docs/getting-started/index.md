# Getting Started

This section is for engineers picking up the cloud-operator skill for the first time. By the end of this section you will:

1. Have the skill installed and discoverable by Claude.
2. Have run your first pricing query end-to-end against the Vantage MCP.
3. Understand the skill's seven workflow patterns and when to expect each.
4. Know the vocabulary used throughout the rest of the docs.

## Reading order

1. **[Install the skill](install.md)** — drop it into Claude Code, Cowork, or load via the Agent SDK.
2. **[First invocation](first-invocation.md)** — run a pricing question and a right-sizing question; see what good output looks like.
3. **[Cloud-operator concepts](concepts.md)** — the seven patterns, the routing pass, the runbook fallback.
4. **[Glossary](glossary.md)** — every acronym from CUDs to ASGs to PTUs in one place.

If you only have ten minutes, read [Install](install.md) and [First invocation](first-invocation.md).

## Prerequisites

- A Claude environment that supports skills — Claude Code, Cowork, or the Agent SDK.
- The **Vantage `instances` MCP** connected. Without it, pricing patterns degrade to runbook fallback.
- Familiarity with at least one of AWS, GCP, or Azure at the "I know what an EC2 instance is" level.

## What you don't need

- AWS / GCP / Azure credentials *for this skill alone*. The Vantage pricing MCP is read-only and unauthenticated. You'll need credentials for any *action* MCPs you wire up later (e.g., GCE management).
- A pre-existing operator workflow. The skill works for ad-hoc questions ("how much for this VM?") and standing workflows alike.

## What if I get stuck

Two good escape valves:

- The [Glossary](glossary.md) — covers every term used in the skill.
- The [MCP availability map](../skill/references/mcp-availability.md) — tells you which capabilities are wired today and which fall back to runbooks.

If something's still unclear, [open an issue](https://github.com/YOUR-USERNAME/cloud-operator-skill/issues) — that's how the docs improve.
