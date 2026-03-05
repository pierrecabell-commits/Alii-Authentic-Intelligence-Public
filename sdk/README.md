# Alii SDK

The Alii SDK defines the contract between your agent code and the Alii runtime. It consists of:

- The **agent folder structure** — what files are required and where
- The **agent.json schema** — the manifest format every agent must follow
- The **Agent class interface** — the Python (or Node) API your code implements
- The **context object** — runtime data Alii passes to your `run` method

---

## Agent Folder Structure

Every agent is a self-contained directory:

```
your-agent-id/
├── agent.json     # Manifest (required)
├── agent.py       # Python implementation (required for python runtime)
└── README.md      # Documentation (required for submission)
```

For Node runtime, replace `agent.py` with `agent.js` or `agent.ts` and export a compatible class.

---

## agent.json Fields

The manifest describes your agent to the Alii runtime and to the Agent Store registry.

| Field | Type | Required | Description |
|---|---|---|---|
| `id` | string | Yes | Unique agent identifier. Lowercase, hyphen-separated. Must match directory name. |
| `name` | string | Yes | Human-readable display name shown in the Agent Store. |
| `version` | string | Yes | Semantic version string (e.g. `"1.0.0"`). Increment on every change. |
| `description` | string | Yes | One sentence. What does this agent do? Be specific. |
| `author` | string | Yes | GitHub username of the primary author. |
| `tags` | string[] | Yes | Searchable labels. Minimum one. Use existing tags where possible. |
| `runtime` | string | Yes | Execution environment: `"python"` or `"node"`. |
| `entrypoint` | string | Yes | Filename containing the `Agent` class (e.g. `"agent.py"`). |
| `permissions` | string[] | Yes | Requested runtime permissions. Empty array if none needed. |
| `triggers` | object | Yes | Routing hints. See Triggers below. |
| `config_schema` | object | No | JSON Schema (draft-07) for the agent's configuration. |

### Triggers

```json
"triggers": {
  "keywords": ["search", "find", "look up"],
  "intents": ["web_search", "information_lookup"]
}
```

- `keywords` — words or phrases in the user's message that suggest this agent
- `intents` — semantic intent labels used by Alii's routing layer

Both are hints, not hard rules. Alii's routing engine makes the final decision.

### config_schema

Defines the configuration your agent accepts. Alii merges defaults, user-supplied values, and vault-injected secrets before calling `__init__`.

Mark secrets with `"secret": true` — Alii will fetch these from the vault and inject them silently:

```json
"config_schema": {
  "type": "object",
  "properties": {
    "api_key": {
      "type": "string",
      "description": "API key for the external service.",
      "secret": true
    },
    "max_results": {
      "type": "integer",
      "description": "Maximum results to return.",
      "default": 5
    }
  },
  "required": ["api_key"]
}
```

---

## Agent Class Interface

### Python

```python
from typing import Any

class Agent:
    def __init__(self, config: dict[str, Any]) -> None:
        """
        Called once when the agent is loaded.
        config contains resolved values including vault-injected secrets.
        """
        ...

    async def run(self, message: str, context: dict[str, Any]) -> str:
        """
        Called for every message routed to this agent.
        Must return a plain string in all code paths.
        """
        ...
```

### Node / TypeScript

```typescript
export class Agent {
  constructor(config: Record<string, unknown>) { ... }

  async run(message: string, context: Record<string, unknown>): Promise<string> { ... }
}
```

### Rules

1. `run` must be `async` (Python) or return a `Promise<string>` (Node).
2. `run` must return a `str`/`string` in every code path — never `None`, `undefined`, or raise uncaught exceptions.
3. `__init__`/`constructor` must not perform async I/O. Use a lazy-init pattern if needed.
4. Do not spawn background threads or processes that outlive the `run` call.

---

## Context Object

Alii passes a `context` dict to every `run` call. Available keys:

| Key | Type | Description |
|---|---|---|
| `user_id` | string | Stable, anonymized user identifier (consistent across sessions) |
| `channel` | string | Source channel: `"discord"`, `"telegram"`, `"slack"`, `"imessage"`, `"signal"`, `"whatsapp"`, `"web"` |
| `session_id` | string | Current session identifier |
| `message_id` | string | Unique ID of this specific message |
| `timestamp` | string | ISO 8601 timestamp of when the message was received |
| `history` | object[] | Recent message history. Each item: `{role, content, timestamp}` |
| `memory` | object[] | Retrieved memory fragments relevant to this message. Each: `{content, score, metadata}` |
| `user_location` | string \| null | User's location if shared (city or coordinates), else null |
| `attachments` | object[] | File attachments if any. Each: `{type, url, name}` |
| `agent_config` | object | The resolved config your agent was initialized with |

Access example:

```python
async def run(self, message: str, context: dict) -> str:
    channel = context.get("channel", "unknown")
    history = context.get("history", [])
    return f"You're on {channel}. You've sent {len(history)} messages this session."
```

---

## Schema Validation

Validate your `agent.json` before submitting:

```bash
# Using ajv-cli (Node)
npx ajv validate -s sdk/agent-schema.json -d agent-store/agents/your-agent-id/agent.json

# Using jsonschema (Python)
pip install jsonschema
python -c "
import json, jsonschema
schema = json.load(open('sdk/agent-schema.json'))
data   = json.load(open('agent-store/agents/your-agent-id/agent.json'))
jsonschema.validate(data, schema)
print('Valid')
"
```

The full schema is at [`sdk/agent-schema.json`](agent-schema.json).
