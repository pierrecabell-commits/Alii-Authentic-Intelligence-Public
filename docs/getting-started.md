# Getting Started with Alii

This guide takes you from zero to a working agent in under 10 minutes.

---

## Prerequisites

You need:

- **Git** — to fork and clone the repository
- **Python 3.11+** — for Python agents
- **Node 20+** — for Node agents (optional)
- A text editor

You do not need to run Alii locally. Agents are loaded by the Alii runtime — you only write the agent code and submit a PR.

---

## Step 1: Fork the Repository

Click **Fork** on GitHub:

```
https://github.com/AVAlii1993/Alii-Authentic-Intelligence-Public
```

Then clone your fork:

```bash
git clone https://github.com/YOUR_USERNAME/Alii-Authentic-Intelligence-Public.git
cd Alii-Authentic-Intelligence-Public
```

---

## Step 2: Copy the Agent Template

```bash
cp -r agent-store/agents/template agent-store/agents/my-first-agent
cd agent-store/agents/my-first-agent
```

You now have three files:
- `agent.json` — the manifest
- `agent.py` — the implementation
- `README.md` — the documentation

---

## Step 3: Edit the Manifest

Open `agent.json` and fill in your details:

```json
{
  "id": "my-first-agent",
  "name": "My First Agent",
  "version": "1.0.0",
  "description": "Echoes the user's message back to them in uppercase.",
  "author": "your-github-username",
  "tags": ["example", "echo"],
  "runtime": "python",
  "entrypoint": "agent.py",
  "permissions": [],
  "triggers": {
    "keywords": ["echo", "repeat", "say back"],
    "intents": []
  }
}
```

---

## Step 4: Implement the Agent

Open `agent.py` and replace the body of `run`:

```python
class Agent:
    def __init__(self, config):
        self.config = config

    async def run(self, message, context):
        return f"You said: {message.upper()}"
```

That's a complete, working agent.

---

## Step 5: Validate Your Manifest

```bash
# From the repo root
npx ajv validate -s sdk/agent-schema.json \
  -d agent-store/agents/my-first-agent/agent.json
```

Or with the built-in validation script:

```bash
pip install jsonschema
python validate.py agent-store/agents/my-first-agent/agent.json
```

This also checks that your agent ID matches the directory name and cross-references the registry.

---

## Step 6: Register Your Agent

Open `agent-store/registry.json` and add your entry to the `"agents"` array:

```json
{
  "id": "my-first-agent",
  "name": "My First Agent",
  "version": "1.0.0",
  "description": "Echoes the user's message back to them in uppercase.",
  "path": "agents/my-first-agent",
  "runtime": "python",
  "tags": ["example", "echo"],
  "author": "your-github-username"
}
```

---

## Step 7: Write Your README

Replace the contents of `README.md` in your agent directory with documentation specific to your agent. Include what it does, example inputs/outputs, and any config keys.

See the [example-search README](../agent-store/agents/example-search/README.md) for a good model.

---

## Step 8: Submit a Pull Request

```bash
# Stage your changes
git checkout -b agent/my-first-agent
git add agent-store/agents/my-first-agent/ agent-store/registry.json
git commit -m "feat: add my-first-agent"
git push origin agent/my-first-agent
```

Then open a PR on GitHub:
- Title: `[agent] my-first-agent`
- Body: what it does, what permissions it needs (if any), an example interaction

---

## What Happens Next

Once merged, your agent is available in the Alii Agent Store. The Alii runtime picks it up on next reload and starts routing matching messages to it.

---

## Next Steps

- Read [`docs/building-agents.md`](building-agents.md) for the full guide including permissions, async patterns, error handling, and config secrets.
- Read [`sdk/README.md`](../sdk/README.md) for the complete context object reference.
- Browse existing agents in [`agent-store/agents/`](../agent-store/agents/) for inspiration.
