# Examples

Working code samples for using the cloud-operator skill.

## Files

- **[sdk-integration.py](sdk-integration.py)** — Load the skill into the Claude Agent SDK with two patterns: static (entire SKILL.md baked into the system prompt) and dynamic (Claude calls a tool to load reference files on demand).

## Running

```bash
pip install anthropic
export ANTHROPIC_API_KEY=sk-...
python examples/sdk-integration.py
```

## Adding more examples

Welcome additions:

- A bash script that wraps the skill into a CLI helper (`cloudops "what's the cheapest GPU under $2/hr in us-east-1"`)
- A LangChain / LlamaIndex integration showing the skill as a tool in a larger agent pipeline
- A CI workflow that runs the eval suite on every skill PR
