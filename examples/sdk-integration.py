"""
Example: load the cloud-operator skill into the Claude Agent SDK.

Two patterns shown:
  1. Static — bake the entire SKILL.md into the system prompt
  2. Dynamic — expose a tool that returns reference files on demand,
     so Claude only loads the references relevant to the current question

Run with:
    pip install anthropic
    export ANTHROPIC_API_KEY=...
    python sdk-integration.py
"""

from __future__ import annotations

import json
from pathlib import Path

from anthropic import Anthropic

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL_DIR = REPO_ROOT / "docs" / "skill"
SKILL_MD = (SKILL_DIR / "SKILL.md").read_text()


# -- Pattern 1: Static -- the whole skill in the system prompt.
def static_skill_system_prompt() -> str:
    return f"""You are a cloud operator assistant. Apply this skill when the user asks about cloud cost, sizing, lifecycle, identity, observability, IaC, or AI/GPU workloads.

<skill>
{SKILL_MD}
</skill>"""


# -- Pattern 2: Dynamic -- expose a tool the model calls when it wants a reference.
def reference_tool_definition() -> dict:
    references = sorted(p.name for p in (SKILL_DIR / "references").glob("*.md"))
    return {
        "name": "read_skill_reference",
        "description": (
            "Read one of the cloud-operator skill's reference files. "
            "Available files: " + ", ".join(references) + ". "
            "Call this when SKILL.md mentions a reference and you want to load it."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "filename": {
                    "type": "string",
                    "enum": references,
                    "description": "Filename of the reference to load.",
                }
            },
            "required": ["filename"],
        },
    }


def handle_reference_tool_call(filename: str) -> str:
    safe = SKILL_DIR / "references" / filename
    if not safe.is_file() or safe.parent != SKILL_DIR / "references":
        return f"ERROR: reference {filename!r} not found"
    return safe.read_text()


def run_dynamic(client: Anthropic, user_question: str) -> None:
    messages = [{"role": "user", "content": user_question}]

    while True:
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=4096,
            system=(
                "You are a cloud operator assistant. Apply this skill when relevant. "
                "Use read_skill_reference to load references on demand.\n\n"
                f"<skill>\n{SKILL_MD}\n</skill>"
            ),
            tools=[reference_tool_definition()],
            messages=messages,
        )

        if response.stop_reason == "tool_use":
            messages.append({"role": "assistant", "content": response.content})
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    output = handle_reference_tool_call(block.input["filename"])
                    tool_results.append(
                        {
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": output,
                        }
                    )
            messages.append({"role": "user", "content": tool_results})
            continue

        for block in response.content:
            if block.type == "text":
                print(block.text)
        return


if __name__ == "__main__":
    client = Anthropic()
    print("=== Pattern 2 (dynamic reference loading) ===\n")
    run_dynamic(
        client,
        "We're standing up a Postgres database for a SaaS app. About 32 GB working "
        "set, OLTP, 8 vCPUs in us-east-1. What RDS class should we pick, and what "
        "would it cost on-demand vs a 1-year reservation?",
    )
