# Contributing

Thanks for considering a contribution. This skill is a living artifact — every cloud-cost question Claude botches is a candidate for a new eval and a refinement.

## Ways to contribute

### Add or improve eval cases

The eval suite lives at [`docs/skill/evals/evals.json`](docs/skill/evals/evals.json). Good additions:

- **Edge cases** — questions that mix two clouds with conflicting region naming, ambiguous workloads, missing constraints
- **Adversarial prompts** — phrasings that have caused the skill to hallucinate or undertrigger
- **New capability areas** — IAM workflows, observability runbooks, IaC drift detection, etc.

Each eval needs:
- A realistic prompt (write it the way a stressed engineer would type it, not as a clean exam question)
- An `expected_output` description
- 5–10 verifiable `expectations` (boolean assertions; prefer ones that *discriminate* between with-skill and without-skill behavior)

Run the eval loop with the skill-creator (see [docs/guides/eval-methodology.md](docs/guides/eval-methodology.md)) and submit the results in your PR.

### Add MCP integrations

When a new MCP becomes available for a (cloud × capability) cell, update [`docs/skill/references/mcp-availability.md`](docs/skill/references/mcp-availability.md). If the new MCP changes how a workflow pattern operates, update the relevant pattern in `SKILL.md` too.

### Improve pillar references

GCP and Azure references are thinner than AWS today. Particularly welcome:

- More right-sizing recipes (e.g., "Memorystore for cache fronting Cloud SQL Postgres")
- Family-naming clarifications as new generations land (n4, c4, c8i, Granite Rapids, etc.)
- Cross-cloud cost-comparison gotchas (CUDs vs SP, free tiers, license-included pricing differences)

### Fix typos / improve clarity

Always welcome. Open a PR with a clear title.

## Development workflow

```bash
# 1. Fork and clone
git clone https://github.com/YOUR-FORK/cloud-operator-skill.git
cd cloud-operator-skill

# 2. Install MkDocs Material for local docs preview
pip install mkdocs-material

# 3. Make changes and preview live
mkdocs serve
# → http://127.0.0.1:8000

# 4. Run tests / evals if you changed the skill
#    (see docs/guides/eval-methodology.md)

# 5. Commit and open PR
git checkout -b your-feature
git commit -am "describe your change"
git push
```

## Style

- Markdown — semantic line breaks (one sentence per line) preferred for diff legibility, but not enforced.
- Skill text — imperative voice ("Call the index" not "You should call the index"). Explain *why*, not just *what*. Keep `SKILL.md` under 500 lines.
- Reference files — flat structure, table-heavy where it helps scanning, no decorative headers.

## Code of conduct

Be respectful. Assume good intent. Disagree with ideas, not people. The maintainers reserve the right to remove or edit comments and reject contributions that don't follow these norms.

## License

By contributing, you agree your contributions are licensed under the MIT License (see [LICENSE](LICENSE)).
