# Alii Agent Store

The Agent Store is the open extension layer for Alii. Each agent is a self-contained module that Alii can discover, load, and invoke dynamically. Agents live in `agents/`, are declared in `registry.json`, and follow a strict but simple schema.

---

## How to Submit an Agent

### 1. Fork this repository

Click **Fork** on GitHub. Clone your fork:

```bash
git clone https://github.com/YOUR_USERNAME/Alii-Authentic-Intelligence-Public.git
cd Alii-Authentic-Intelligence-Public
```

### 2. Copy the template

```bash
cp -r agent-store/agents/template agent-store/agents/your-agent-id
```

Use a short, lowercase, hyphen-separated ID (e.g. `github-search`, `stock-price`, `pdf-summarizer`).

### 3. Fill in `agent.json`

Edit `agent-store/agents/your-agent-id/agent.json`. Every field is required. Validate against the schema:

```bash
npx ajv validate -s sdk/agent-schema.json -d agent-store/agents/your-agent-id/agent.json
```

See [`sdk/README.md`](../sdk/README.md) for a full field reference.

### 4. Implement `agent.py` (or your runtime's entrypoint)

Your agent must export a class named `Agent` with:

```python
class Agent:
    def __init__(self, config: dict): ...
    async def run(self, message: str, context: dict) -> str: ...
```

The `run` method receives the user's message and a context object. It must return a plain string — the response Alii will deliver to the user.

### 5. Write a `README.md`

Include: what your agent does, what permissions it needs, example inputs and outputs, any required config keys.

### 6. Add an entry to `registry.json`

Open `agent-store/registry.json` and add your agent under the `"agents"` array:

```json
{
  "id": "your-agent-id",
  "name": "Your Agent Name",
  "version": "1.0.0",
  "description": "One sentence describing what this agent does.",
  "path": "agents/your-agent-id",
  "runtime": "python",
  "tags": ["tag1", "tag2"],
  "author": "your-github-handle"
}
```

### 7. Open a pull request

Branch name: `agent/your-agent-id`
PR title: `[agent] your-agent-id`

Include in your PR description:
- What the agent does
- What permissions it requests and why
- Example interaction

---

## Review Criteria

PRs are reviewed for:

| Criterion | Details |
|---|---|
| Schema validity | `agent.json` must pass schema validation |
| Least privilege | Only request permissions the agent actually uses |
| No secrets in code | All credentials via `config` keys, never hardcoded |
| Working implementation | `run()` must return a string in all code paths |
| Clear README | Non-technical users should understand what it does |

---

## Agent Permissions Reference

| Permission | What it allows |
|---|---|
| `network` | Outbound HTTP/HTTPS requests |
| `memory_read` | Read from Alii's vector memory store |
| `memory_write` | Write to Alii's vector memory store |
| `vault_read` | Read secrets from vault (injected, never exposed) |
| `file_read` | Read files from the user's allowed directories |
| `file_write` | Write files to the user's allowed directories |
| `shell` | Execute shell commands (requires explicit approval) |

Request only what you need. Agents requesting `shell` or `vault_read` receive additional scrutiny.

---

## Questions?

Open an issue or start a discussion. Tag it `agent-store`.

---

Copyright (c) 2026 Pierre Cabell. All Rights Reserved.
