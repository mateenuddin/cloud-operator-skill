# cloud-operator-skill

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Docs](https://img.shields.io/badge/docs-mkdocs--material-blue.svg)](https://YOUR-USERNAME.github.io/cloud-operator-skill/)

> A multi-cloud operator agent skill for AWS, GCP, and Azure — covering pricing analysis, right-sizing, cross-cloud comparison, resource lifecycle, identity, observability, IaC, and AI/GPU workloads. Built on the [Claude Agent SDK](https://docs.claude.com) and the Vantage pricing MCP.

---

## What this is

A complete, production-grade **agent skill** that turns Claude into a capable cloud operator. The skill knows when to call which MCP, how to navigate AWS/GCP/Azure pricing matrices, when to produce runbooks instead of pretending to act, and how to compare workloads across clouds honestly.

Beyond the skill itself, this repo is a **learning resource**: catalogs of every operator-relevant service across the three clouds, MCP availability annotations, eval methodology, and a roadmap for extending the skill to your own MCPs.

## What you'll find here

| Path | What's inside |
| --- | --- |
| [`docs/`](docs/index.md) | Full documentation site (MkDocs Material + search). Start here. |
| [`docs/getting-started/`](docs/getting-started/) | New-engineer onboarding — install, first invocation, quick wins |
| [`docs/skill/`](docs/skill/) | The actual `SKILL.md` and reference files (the skill itself) |
| [`docs/reference/`](docs/reference/) | Service catalog, operations catalog, mindmap |
| [`docs/guides/`](docs/guides/) | Skill-expansion plan, iteration methodology |
| [`docs/evals/`](docs/evals/) | Eval prompts, assertions, results from each iteration |
| [`examples/`](examples/) | Sample invocations and expected outputs |

## Quick start

### Read the docs

```bash
# Local preview (auto-reloads on edits, full search)
pip install mkdocs-material
mkdocs serve
# → open http://127.0.0.1:8000
```

Or read the published site at `https://YOUR-USERNAME.github.io/cloud-operator-skill/` once you've enabled GitHub Pages (see [PUBLISHING.md](PUBLISHING.md)).

### Use the skill

The skill lives at [`docs/skill/SKILL.md`](docs/skill/SKILL.md) plus references in [`docs/skill/references/`](docs/skill/references/). To use it with Claude:

1. **Cowork mode (drag-and-drop)** — bundle the skill folder as a `.skill` file and add it via the Cowork plugin/skill installer.
2. **Claude Code** — drop the skill folder into your project's `.claude/skills/cloud-operator/` and Claude Code will discover it.
3. **Claude Agent SDK** — load the SKILL.md content into your system prompt or pass via the SDK's skills parameter.

Full details in [`docs/getting-started/install.md`](docs/getting-started/install.md).

### Required MCP

The skill is built around the **Vantage pricing MCP** (`instances-mcp.vantage.sh`) — read-only pricing for AWS EC2/RDS/ElastiCache/OpenSearch/Redshift, plus Azure and GCP compute. Without it, pricing patterns degrade to runbook fallback. See [`docs/skill/references/mcp-availability.md`](docs/skill/references/mcp-availability.md) for the full MCP availability map.

## Why this exists

Cloud cost analysis and right-sizing decisions burn a lot of engineer hours. A general-purpose Claude can answer "what's an m5.large cost" approximately, but it doesn't know to call the Vantage indexes for fast intersection queries, doesn't know that RDS uses Reserved Instances not Savings Plans, doesn't know to surface Spot interrupt frequency before recommending Spot, and won't honestly say "no MCP wired for this — here's a runbook." This skill encodes those operator instincts.

## Who this is for

- **New engineers** picking up a cloud-operator role and needing a structured map of services, capabilities, and tooling
- **Platform / infra teams** who want a Claude-driven cost analyst as part of their toolchain
- **Skill authors** looking for a worked example of a multi-cloud agent skill with eval methodology
- **Anyone evaluating Claude as a FinOps assistant**

## Project status

| | Status |
| --- | --- |
| AWS pricing & right-sizing (Patterns A/B/C) | ✅ Iteration 2, eval pass-rate 0.98 |
| GCP pricing & cross-cloud comparison | ✅ Iteration 2 |
| Azure pricing | ✅ Iteration 2 |
| Resource lifecycle (Pattern D) — runbook fallback | ✅ Iteration 2 |
| Observability (Pattern E) | 🚧 Runbook only; Datadog MCP integration pending |
| IaC (Pattern F) | 🚧 Runbook only |
| AI / GPU (Pattern G) | ✅ Pricing + GPU-index right-sizing; foundation-model invocation TBD |

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Particularly welcome:

- New eval cases (especially edge cases that expose skill weaknesses)
- New MCP integrations (note them in `docs/skill/references/mcp-availability.md`)
- GCP / Azure pillar reference improvements (these are thinner than AWS today)
- Translation of the skill description for non-English users

## License

MIT — see [LICENSE](LICENSE).

## Acknowledgments

- [Vantage](https://vantage.sh) for the public pricing MCP
- [Anthropic](https://anthropic.com) for the skills framework and Claude Agent SDK
- [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) for the docs theme
