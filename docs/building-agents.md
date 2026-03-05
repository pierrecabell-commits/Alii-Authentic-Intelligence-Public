# Building Agents for Alii

A complete guide to designing, implementing, and submitting production-quality agents.

---

## The Agent Lifecycle

Understanding how Alii handles agents helps you write better ones.

```
1. Discovery   Alii scans agent-store/registry.json on startup
2. Load        Alii imports your entrypoint and instantiates Agent(config)
3. Route       A user message arrives; Alii scores all loaded agents
4. Invoke      Alii calls agent.run(message, context)
5. Deliver     Your return string is sent to the user's channel
```

Your code only touches steps 2–4. Everything else is handled by the runtime.

---

## Step 1: Choose Your Agent ID

Your agent ID must be:
- Unique across the entire registry
- Lowercase, hyphen-separated
- Descriptive of what the agent does

Good: `github-issue-lookup`, `currency-converter`, `pdf-summarizer`
Bad: `agent1`, `myagent`, `test`

---

## Step 2: Define Permissions

Only request what your agent needs. Alii enforces permissions at runtime — requesting extras will slow approval and confuse users.

| Permission | What It Grants | When to Use |
|---|---|---|
| `network` | Outbound HTTP/HTTPS | Any agent that calls an external API |
| `memory_read` | Read from Alii's Qdrant vector store | Personalized responses, recall previous context |
| `memory_write` | Write to Alii's Qdrant vector store | Agents that learn or persist state |
| `vault_read` | Read secrets (injected, never exposed) | Any agent with an API key in config_schema |
| `file_read` | Read files from allowed directories | Document analysis, local data processing |
| `file_write` | Write files to allowed directories | Report generation, data export |
| `shell` | Execute shell commands | Strongly discouraged; requires explicit approval |

### Implicit permissions

If you declare a `secret: true` config key, Alii automatically grants `vault_read` for that key. You still need to declare `vault_read` in `permissions` if your agent calls the vault API directly.

---

## Step 3: Design Your Config Schema

Config schema keys map to values your agent receives at init time. Group them into:

- **Secrets** — API keys, tokens. Mark `"secret": true`. Alii fetches from vault and injects before `__init__`.
- **User preferences** — Tunable behavior (result count, language, units). Provide sensible defaults.
- **Fixed settings** — Rarely changed. Provide defaults.

```json
"config_schema": {
  "type": "object",
  "properties": {
    "api_key": {
      "type": "string",
      "description": "API key for ExternalService (vault-injected).",
      "secret": true
    },
    "max_results": {
      "type": "integer",
      "description": "Maximum results to return per query.",
      "default": 5,
      "minimum": 1,
      "maximum": 50
    },
    "language": {
      "type": "string",
      "description": "Response language code.",
      "default": "en"
    }
  },
  "required": ["api_key"]
}
```

---

## Step 4: Implement the Agent Class

### Minimal working agent

```python
class Agent:
    def __init__(self, config):
        self.api_key = config["api_key"]
        self.max_results = config.get("max_results", 5)

    async def run(self, message, context):
        return "Hello from my agent!"
```

### Async HTTP with aiohttp

```python
import aiohttp

class Agent:
    def __init__(self, config):
        self.api_key = config["api_key"]
        self.max_results = config.get("max_results", 5)
        self._session = None

    def _get_session(self):
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession(
                headers={"Authorization": f"Bearer {self.api_key}"}
            )
        return self._session

    async def run(self, message, context):
        try:
            session = self._get_session()
            async with session.get(
                "https://api.example.com/query",
                params={"q": message, "limit": self.max_results},
                timeout=aiohttp.ClientTimeout(total=10)
            ) as resp:
                resp.raise_for_status()
                data = await resp.json()
            return self._format(data)
        except aiohttp.ClientError as e:
            return f"Sorry, I couldn't reach the service right now. ({type(e).__name__})"
        except Exception as e:
            return f"Something went wrong. Please try again."

    def _format(self, data):
        results = data.get("results", [])
        if not results:
            return "No results found."
        lines = [f"- {r['title']}: {r['url']}" for r in results[:self.max_results]]
        return "Here's what I found:\n" + "\n".join(lines)
```

### Using context

```python
async def run(self, message, context):
    channel = context.get("channel", "unknown")
    history = context.get("history", [])
    memory  = context.get("memory", [])

    # Personalize based on channel
    if channel == "discord":
        prefix = "**Result:**"
    else:
        prefix = "Result:"

    # Use retrieved memory for context
    prior_context = ""
    if memory:
        prior_context = f"\n(Relevant context: {memory[0]['content']})"

    result = await self._fetch(message)
    return f"{prefix} {result}{prior_context}"
```

---

## Step 5: Error Handling

**Golden rule: `run` must never raise an uncaught exception.** Alii catches exceptions as a last resort, but your agent should handle its own errors gracefully.

```python
async def run(self, message, context):
    try:
        return await self._do_work(message, context)
    except ValueError as e:
        # Expected input errors
        return f"I couldn't understand that input: {e}"
    except TimeoutError:
        return "The request timed out. Please try again."
    except Exception:
        # Catch-all — never expose internal details
        return "Something went wrong on my end. Please try again in a moment."
```

---

## Step 6: Triggers and Routing

Triggers are hints, not hard rules. Alii's router uses them along with semantic similarity and conversation context.

```json
"triggers": {
  "keywords": ["stock", "price", "share", "market cap", "ticker"],
  "intents": ["stock_price", "financial_data"]
}
```

- List the most specific keywords users actually say
- Avoid very common words ("what", "how", "tell me") that would match everything
- Intent strings are free-form but should be specific (prefer `stock_price_lookup` over `finance`)

---

## Step 7: Write the README

Every agent needs a README that answers:

1. What does this agent do? (one paragraph)
2. What does it say when working? (example input/output)
3. What permissions does it need and why?
4. What config keys does it use?

Use the [example-search README](../agent-store/agents/example-search/README.md) as a template.

---

## Step 8: Test Locally

You can test your `run` method without the full Alii runtime:

```python
import asyncio
from agent import Agent

config = {
    "api_key": "test-key-do-not-commit",
    "max_results": 3,
}
context = {
    "user_id": "test-user",
    "channel": "web",
    "session_id": "test-session",
    "history": [],
    "memory": [],
}

agent = Agent(config)
result = asyncio.run(agent.run("test query here", context))
print(result)
```

Never commit real API keys. Use environment variables or a local `.env` file (which is gitignored).

---

## Step 9: Validate and Submit

```bash
# Validate manifest
npx ajv validate -s sdk/agent-schema.json \
  -d agent-store/agents/your-agent-id/agent.json

# Create a branch and commit
git checkout -b agent/your-agent-id
git add agent-store/agents/your-agent-id/ agent-store/registry.json
git commit -m "feat: add your-agent-id agent"
git push origin agent/your-agent-id

# Open a PR with title: [agent] your-agent-id
```

---

## Common Mistakes

| Mistake | Fix |
|---|---|
| Returning `None` from `run` | Always return a string |
| Raising exceptions from `run` | Catch and return error strings |
| Hardcoding API keys | Use `config_schema` with `"secret": true` |
| Requesting unused permissions | Remove any permission your code doesn't use |
| Synchronous I/O in `run` | Use `aiohttp`/`httpx` not `requests` |
| Blocking `__init__` with network calls | Move I/O into `run` or use lazy init |
| Over-broad keyword triggers | Be specific — don't match common words |
| Missing error handling | Wrap all external calls in try/except |

---

## Advanced Patterns

### Lazy initialization (when you need async setup)

```python
class Agent:
    def __init__(self, config):
        self.config = config
        self._client = None

    async def _ensure_client(self):
        if self._client is None:
            self._client = await SomeAsyncClient.create(self.config["api_key"])

    async def run(self, message, context):
        await self._ensure_client()
        return await self._client.query(message)
```

### Multi-turn conversation awareness

```python
async def run(self, message, context):
    history = context.get("history", [])
    # Last 3 exchanges for context
    recent = history[-6:] if len(history) > 6 else history
    formatted_history = "\n".join(
        f"{m['role']}: {m['content']}" for m in recent
    )
    return await self._query_with_context(message, formatted_history)
```

### Memory integration

```python
async def run(self, message, context):
    memory_fragments = context.get("memory", [])
    # memory_write permission required to use memory API
    # memory_read permission for reading (already done by Alii before run)
    enriched_context = " | ".join(m["content"] for m in memory_fragments[:3])
    return await self._answer(message, enriched_context)
```

---

## Getting Help

- Open an issue on GitHub and tag it `building-agents`
- Browse existing agents for patterns: [`agent-store/agents/`](../agent-store/agents/)
- Read the SDK reference: [`sdk/README.md`](../sdk/README.md)
