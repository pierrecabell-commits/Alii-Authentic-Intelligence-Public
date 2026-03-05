# Template Agent

This is the canonical starting point for every Alii agent. It does nothing useful on its own — that's your job.

---

## How to Use This Template

1. Copy this directory: `cp -r template ../your-agent-id`
2. Edit `agent.json` — set your `id`, `name`, `description`, `tags`, and any `config_schema` keys your agent needs.
3. Edit `agent.py` — implement `__init__` and `run`.
4. Write this `README.md` with real content about your agent.
5. Register in `agent-store/registry.json` and open a PR.

---

## Agent Structure

```
your-agent-id/
├── agent.json   # Manifest — required
├── agent.py     # Implementation — required for python runtime
└── README.md    # Documentation — required
```

---

## agent.json Fields

| Field | Type | Required | Description |
|---|---|---|---|
| `id` | string | Yes | Unique, lowercase, hyphen-separated identifier |
| `name` | string | Yes | Human-readable display name |
| `version` | string | Yes | Semantic version (e.g. `1.0.0`) |
| `description` | string | Yes | One sentence describing what this agent does |
| `author` | string | Yes | GitHub username |
| `tags` | string[] | Yes | Searchable tags (at least one) |
| `runtime` | string | Yes | `"python"` or `"node"` |
| `entrypoint` | string | Yes | Filename containing the `Agent` class |
| `permissions` | string[] | Yes | Requested permissions (can be empty array) |
| `triggers` | object | Yes | `keywords` and `intents` arrays for routing |
| `config_schema` | object | No | JSON Schema for agent config |

---

## The `run` Method Contract

```python
async def run(self, message: str, context: dict) -> str
```

- Always `async`
- Always returns `str`
- Never raises — handle exceptions internally and return a user-friendly error string

---

## Permissions

Only declare permissions your agent actually uses. See [`agent-store/README.md`](../../README.md) for the full permissions table.
