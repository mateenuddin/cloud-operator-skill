# Install the skill

The skill is a folder of markdown files. Three install paths depending on where you run Claude.

## Path 1 — Claude Code

```bash
# From the repo root
mkdir -p ~/.claude/skills
cp -r docs/skill/ ~/.claude/skills/cloud-operator/

# Or, if you're inside a specific project, use the project-scoped folder:
mkdir -p .claude/skills
cp -r docs/skill/ .claude/skills/cloud-operator/
```

Restart Claude Code. The skill should appear in `available_skills` and trigger automatically on cloud-operator questions. Verify with:

```
/skills
```

## Path 2 — Cowork

Bundle the skill folder into a `.skill` file using the skill-creator's packaging script:

```bash
# Clone the skill-creator if you don't have it
git clone https://github.com/anthropics/skills.git
cd skills/skill-creator

python -m scripts.package_skill /path/to/cloud-operator-skill/docs/skill
# Produces cloud-operator.skill in /path/to/cloud-operator-skill/docs/skill/
```

Then drag the `.skill` file into Cowork via Settings → Skills → Install from file.

## Path 3 — Claude Agent SDK

Load the skill content as part of your system prompt or pass via the SDK's skills parameter:

```python
from anthropic import Anthropic

client = Anthropic()

with open("docs/skill/SKILL.md") as f:
    skill_md = f.read()

system_prompt = f"""
You have access to the following skill. Apply it when the user asks about cloud cost / sizing / operations:

{skill_md}
"""

response = client.messages.create(
    model="claude-sonnet-4-6",
    system=system_prompt,
    messages=[{"role": "user", "content": "How much is an m5.large in us-east-1?"}],
    max_tokens=2048,
)
```

For dynamic reference loading (so Claude only loads `aws-pillars.md` when the question is about AWS), use a tool-use pattern:

```python
# Expose a "read_reference" tool that returns the contents of one of the reference files
# on demand. The skill mentions filenames; Claude calls the tool to fetch them.
```

See [`examples/sdk-integration.py`](https://github.com/YOUR-USERNAME/cloud-operator-skill/blob/main/examples/sdk-integration.py) for a full working example.

## Connect the Vantage MCP

The skill assumes the Vantage `instances` MCP is wired. In Cowork or Claude Code with MCP support:

1. Open the connector menu / Settings → MCP servers.
2. Search for "Vantage" or "instances".
3. Click Connect (no auth required — the public Vantage pricing endpoint is open).
4. Verify the tools are available — you should see `get-ec2-region-pricing`, `get-azure-instance`, etc.

If your Claude environment doesn't support MCP, the skill still works — it'll just fall back to runbook output for every pricing question (less useful, but honest about its limits).

## Verify the install

Ask Claude:

> *How much does an m5.2xlarge cost in us-east-1?*

You should see Claude:

1. Call `get-ec2-region-pricing` (proof the MCP is wired)
2. Surface a specific Linux on-demand price (around $0.384/hr)
3. Optionally note Spot, Savings Plan, and monthly conversion

If that works, head to [First invocation](first-invocation.md) to run more substantial flows.

## Troubleshooting

| Symptom | Cause | Fix |
| --- | --- | --- |
| Skill triggers but says "no Vantage MCP wired" | The MCP isn't connected | Connect it via the connector menu (see above) |
| Skill doesn't trigger at all | Description not pushy enough or your Claude doesn't have skills enabled | Check `available_skills`; if missing, re-install. If present, try a more explicit prompt that mentions pricing or sizing. |
| Vantage tools return errors | Vantage public API hiccup | Retry; check status at vantage.sh |
| Wrong region returned | You said a city; the skill assumed `us-east-1` | Always state the region explicitly (`ap-south-1` not "Mumbai") |
