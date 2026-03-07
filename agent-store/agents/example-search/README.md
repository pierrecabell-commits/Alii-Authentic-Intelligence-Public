# Web Search Agent

Performs a real-time web search and returns a concise, summarized answer with source links.

---

## What It Does

When Alii routes a message to this agent, it:

1. Extracts the search query from the user's message
2. Queries the configured search API
3. Retrieves the top results (up to `max_results`)
4. Summarizes the findings into a single, readable response
5. Appends source URLs for verification

---

## Example Interactions

**Input:**
> Search for the latest news on open-source AI frameworks

**Output:**
> Here's what I found on open-source AI frameworks:
>
> The leading frameworks as of early 2026 are LangChain, LlamaIndex, and Haystack — all seeing rapid adoption for agent-based systems. Recent releases focus on...
>
> Sources:
> - https://example.com/ai-frameworks-2026
> - https://example.com/open-source-llm-tools

---

## Permissions

| Permission | Reason |
|---|---|
| `network` | Required for outbound HTTP requests to the search API |

---

## Configuration

| Key | Type | Required | Description |
|---|---|---|---|
| `search_api_key` | string | Yes | Search provider API key (vault-injected) |
| `max_results` | integer | No | Results to retrieve (default: 5, max: 20) |
| `language` | string | No | Language code for results (default: `"en"`) |

The `search_api_key` is injected by Alii's vault guardian at runtime. You never see or handle it directly.

---

## Supported Search Providers

This agent is provider-agnostic. Implement `agent.py` against your preferred search API (SerpAPI, Brave Search, Tavily, etc.). The `search_api_key` config key maps to your chosen provider's authentication.

---

## Implementation Notes

The included `agent.py` implementation:

- Uses `aiohttp` for async HTTP requests with a 15-second timeout
- Lazily initializes the HTTP session on first use
- Parses the provider's JSON response into formatted markdown
- Returns user-friendly error messages on failure
- Implements `cleanup()` to close the HTTP session on shutdown
