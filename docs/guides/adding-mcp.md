# Adding a new MCP

When a new MCP becomes available for a (cloud × capability) cell, here's how to integrate it without breaking what already works.

## Step 1 — Probe before you wire

Don't trust the registry description; call the MCP's tools and inspect actual response shapes. This is the same playbook the skill itself uses.

```text
1. Call list-style tool first (e.g., list_instances, get_indexes).
2. Inspect the response shape — field names, units, pagination.
3. Call a get-style tool with one known input.
4. Inspect again. Note any "MCP wraps the API differently" surprises.
```

Document the surprises. They become the gotchas section in your reference file.

## Step 2 — Update mcp-availability.md

Edit [`docs/skill/references/mcp-availability.md`](../skill/references/mcp-availability.md):

- Move the cell from 🟦 (upstream) or 🟡 (registry) to ✅ (connected).
- Add the directoryUuid to the "Known UUIDs" list at the bottom of the file.
- If this MCP enables a *new* capability not in the matrix, add a row.

Be honest about what the MCP can and cannot do. If it's read-only, say so. If it requires authentication, note the OAuth or token flow.

## Step 3 — Update the relevant pillar reference

Edit [`docs/skill/references/aws-pillars.md`](../skill/references/aws-pillars.md), [`gcp-pillars.md`](../skill/references/gcp-pillars.md), or [`azure-pillars.md`](../skill/references/azure-pillars.md) — whichever cloud the MCP serves.

Add an "Operations cheatsheet" subsection if it's not there, and list the MCP's most useful tools with short descriptions. Mirror the format used for the Vantage tools.

## Step 4 — Update SKILL.md if the workflow changes

Most new MCPs slot into one of the existing seven workflow patterns. But if the new MCP enables something genuinely new (e.g., an IaC drift detector), add a new pattern or extend Pattern F.

Three things to keep when editing SKILL.md:

- **Routing pass stays at the top.** Always identify cloud × capability × inspection-vs-mutation first.
- **The new pattern includes a fallback.** What does the agent do if the MCP errors mid-call?
- **The skill remains under 500 lines.** Push detail into a new reference file if needed.

## Step 5 — Add an eval

Write at least one eval that exercises the new MCP end-to-end. Use the format in [`docs/skill/evals/evals.json`](../skill/evals/evals.json):

```json
{
  "id": 7,
  "name": "new-mcp-capability-name",
  "prompt": "A realistic question that should now use the new MCP",
  "expected_output": "Description of what good looks like",
  "expectations": [
    "Calls the new MCP tool",
    "Doesn't fall back to runbook (MCP is wired now)",
    "Reports a specific value from the MCP response",
    "Discriminating assertion about format / accuracy"
  ]
}
```

## Step 6 — Run the eval loop

Follow [Eval methodology](eval-methodology.md). Compare iteration N with the new MCP against iteration N-1 without. If pass rate doesn't improve materially, the MCP isn't pulling its weight — either the skill needs to teach Claude to use it better, or the MCP has gaps.

## Step 7 — Open a PR

Include in the PR:

- The updated SKILL.md, references, evals
- The benchmark.json showing improvement
- A brief note in the PR description explaining what the new MCP unlocks

Maintainer will review and merge.

## When *not* to add an MCP

- The MCP duplicates an existing one. (E.g., adding a second cost-explorer MCP.)
- The MCP is unreliable. Test it for a week before wiring.
- The MCP requires per-user auth that's painful to set up in eval environments. The skill should still work without it.
- The MCP encourages destructive default behavior. (E.g., a "delete-orphaned-resources" MCP that doesn't require confirmation.)

When in doubt, default to runbook fallback rather than adding a flaky MCP that produces inconsistent results.
