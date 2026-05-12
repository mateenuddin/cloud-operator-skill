# Guides

How-to guides for extending, evaluating, and operating this skill.

## Pages

- **[Skill expansion roadmap](expansion-plan.md)** — the design document for evolving from AWS-only (iteration 1) to multi-cloud (iteration 2) and beyond. Read this if you want to fork and adapt the skill to your own scope.
- **[Eval methodology](eval-methodology.md)** — how to spawn with-skill / without-skill subagent runs, capture timing, grade assertions, aggregate into a benchmark, and generate the static HTML viewer. The full loop the maintainers run between iterations.
- **[Adding a new MCP](adding-mcp.md)** — when a new MCP becomes available for a (cloud × capability) cell, how to update the skill, the availability table, and the relevant workflow patterns.

## Suggested reading order

If you're forking the skill: **expansion-plan → adding-mcp → eval-methodology**. The expansion plan gives you the design vocabulary; adding-mcp shows how to wire something new; eval-methodology validates whatever you wired.

If you're benchmarking: **eval-methodology → expansion-plan**.

If you're a maintainer reviewing a PR: **eval-methodology** is the bar.
