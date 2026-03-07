<p align="center">
  <strong>A L I I</strong>
</p>

<h1 align="center">Authentic Intelligence</h1>

<p align="center">
  <em>The self-evolving autonomous AI that lives where your people are.</em>
</p>

<p align="center">
  <a href="#the-agent-store"><img src="https://img.shields.io/badge/Agent%20Store-open-brightgreen?style=for-the-badge" alt="Agent Store" /></a>
  <a href="sdk/"><img src="https://img.shields.io/badge/SDK-stable-blue?style=for-the-badge" alt="SDK" /></a>
  <a href="#channels"><img src="https://img.shields.io/badge/Channels-7-orange?style=for-the-badge" alt="Channels" /></a>
</p>

---

## What is Alii?

Alii is an autonomous, multi-channel AI system engineered to operate across every platform your users inhabit -- simultaneously, coherently, and without manual intervention.

It routes intent, learns from interaction, manages credentials, persists memory, and deploys agents -- all from a single sovereign intelligence layer.

Alii is not a chatbot. It is not a wrapper around an LLM. It is an **operating system for AI presence**.

### Core Capabilities

| Capability | Description |
|---|---|
| **Multi-Channel Presence** | Single intelligence, many surfaces -- every message handled in context |
| **Autonomous Routing** | Incoming messages are scored, classified, and dispatched to the right agent automatically |
| **Persistent Memory** | Vector-backed recall via Qdrant -- Alii remembers what matters |
| **Vault-Guarded Secrets** | Credentials are injected at runtime, never exposed to agent code |
| **Self-Evolution** | The system learns from interaction patterns and refines its own behavior |
| **Agent Ecosystem** | Extend Alii's capabilities through community-built, modular agents |

---

## Channels

Alii operates natively across seven platforms, delivering a unified experience regardless of where the conversation happens:

| Channel | Status |
|---|---|
| Discord | Supported |
| Telegram | Supported |
| Slack | Supported |
| iMessage | Supported |
| Signal | Supported |
| WhatsApp | Supported |
| Web | Supported |

Each channel connector handles platform-specific formatting, media types, and interaction patterns -- your agents don't need to think about any of it.

---

## The Agent Store

The Agent Store is the open, community-contributed extension layer for Alii. Agents are discrete units of capability -- a search agent, a weather agent, a CRM lookup, a code reviewer -- packaged as self-describing modules that Alii discovers, loads, and invokes at runtime.

**Anyone can build an agent. Anyone can publish one. Alii routes to them automatically.**

This repository **is** the Agent Store. Browse [`agent-store/`](agent-store/), fork, build, and submit a PR.

### Available Agents

| Agent | Description | Tags |
|---|---|---|
| [Web Search](agent-store/agents/example-search/) | Performs web searches and returns summarized answers with sources | `search`, `web`, `research` |
| [Weather](agent-store/agents/example-weather/) | Returns current conditions and multi-day forecasts for any location | `weather`, `forecast`, `location` |
| [Template](agent-store/agents/template/) | Canonical starting point for building your own agent | `template`, `example` |

---

## Architecture

```
                         User Message
                              |
                    +---------+---------+
                    |   Alii Gateway    |   (Alii-Core: TypeScript)
                    |  Channel Routing  |
                    +---------+---------+
                              |
                    +---------+---------+
                    |    Alii Brain     |   (Alii-God: Python)
                    |  LLM Orchestration|
                    |  Memory (Qdrant)  |
                    |  Vault Guardian   |
                    |  Self-Evolution   |
                    +---------+---------+
                              |
                    +---------+---------+
                    |   Agent Store     |   (This Repo: Public)
                    |  Community Agents |
                    +-------------------+
```

Messages arrive through any channel, pass through the gateway for normalization and session management, reach the brain for intent classification and memory retrieval, and are dispatched to the appropriate agent. The agent's response travels the same path back.

---

## Repository Layout

```
Alii-Authentic-Intelligence-Public/
|
+-- README.md                              # You are here
+-- LICENSE                                # All Rights Reserved
+-- .gitignore
|
+-- agent-store/
|   +-- README.md                          # How to submit agents
|   +-- registry.json                      # Master agent registry
|   +-- agents/
|       +-- template/                      # Canonical agent template
|       |   +-- agent.json                 # Manifest
|       |   +-- agent.py                   # Implementation
|       |   +-- README.md
|       +-- example-search/                # Example: web search agent
|       |   +-- agent.json
|       |   +-- README.md
|       +-- example-weather/               # Example: weather agent
|           +-- agent.json
|           +-- README.md
|
+-- sdk/
|   +-- README.md                          # SDK documentation
|   +-- agent-schema.json                  # JSON Schema for agent.json
|
+-- docs/
    +-- getting-started.md                 # Zero-to-agent in 10 minutes
    +-- building-agents.md                 # Complete agent development guide
```

---

## Quick Start

Get from zero to a working agent in under 10 minutes.

### Prerequisites

- **Git** -- to fork and clone
- **Python 3.11+** -- for Python agents
- **Node 20+** -- for Node agents (optional)

### Steps

```bash
# 1. Clone the repo
git clone https://github.com/AVAlii1993/Alii-Authentic-Intelligence-Public.git
cd Alii-Authentic-Intelligence-Public

# 2. Copy the agent template
cp -r agent-store/agents/template agent-store/agents/my-agent
cd agent-store/agents/my-agent

# 3. Edit the manifest and implementation
# Set your id, name, description, tags, and permissions in agent.json
# Implement the run(message, context) method in agent.py

# 4. Validate against the schema
npx ajv validate -s ../../sdk/agent-schema.json -d agent.json

# 5. Register your agent in agent-store/registry.json and open a PR
```

For the full walkthrough, see [Getting Started](docs/getting-started.md).

---

## How to Build an Agent

Every Alii agent follows the same contract:

```python
class Agent:
    def __init__(self, config: dict) -> None:
        """Called once at load time with resolved config (including vault secrets)."""
        ...

    async def run(self, message: str, context: dict) -> str:
        """Called for every routed message. Must return a string. Must not raise."""
        ...
```

### The Development Cycle

1. **Fork** this repository
2. **Copy** `agent-store/agents/template` to `agent-store/agents/your-agent-id`
3. **Implement** your agent in `agent.json` (manifest) and `agent.py` (logic)
4. **Test** locally with a simple async runner (see [Building Agents](docs/building-agents.md#step-8-test-locally))
5. **Validate** your manifest against `sdk/agent-schema.json`
6. **Register** in `agent-store/registry.json`
7. **Submit** a PR titled `[agent] your-agent-id`

### Agent Permissions

Agents operate under a least-privilege model. Only request what you need:

| Permission | Grants | Use Case |
|---|---|---|
| `network` | Outbound HTTP/HTTPS | Calling external APIs |
| `memory_read` | Read from Qdrant vector store | Personalized responses, context recall |
| `memory_write` | Write to Qdrant vector store | Learning, state persistence |
| `vault_read` | Read secrets (injected, never exposed) | API key access |
| `file_read` | Read from allowed directories | Document analysis |
| `file_write` | Write to allowed directories | Report generation |
| `shell` | Execute shell commands | Requires explicit approval |

---

## Ecosystem

| Repository | Access | Description |
|---|---|---|
| **Alii-Authentic-Intelligence-Public** | Public | Open Agent Store, SDK, and documentation (this repo) |
| **Alii-Core** | Private | TypeScript gateway -- channel connectors (Discord, Telegram, Slack, iMessage, Signal, WhatsApp, Web), routing engine, session management |
| **Alii-God** | Private | Python brain -- LLM orchestration, memory (Qdrant), vault guardian, todo agent, account agent, self-evolution loop |

Community contributions live here. The intelligence that consumes them lives in the private repositories above.

---

## Contributing

1. Read [`agent-store/README.md`](agent-store/README.md) before submitting an agent
2. Validate your `agent.json` against [`sdk/agent-schema.json`](sdk/agent-schema.json)
3. One agent per PR -- include a clear README and working implementation
4. Follow the naming convention: lowercase, hyphen-separated IDs
5. Request only the permissions your agent actually uses
6. Handle all errors gracefully -- `run()` must never raise uncaught exceptions

---

## Documentation

| Document | Description |
|---|---|
| [Getting Started](docs/getting-started.md) | Zero-to-agent quickstart guide |
| [Building Agents](docs/building-agents.md) | Complete development guide with patterns and best practices |
| [SDK Reference](sdk/README.md) | Agent class interface, context object, and schema details |
| [Agent Store Guide](agent-store/README.md) | Submission process and review criteria |

---

## License

Copyright (c) 2026 Pierre Cabell. All Rights Reserved.

This software and associated documentation files (the "Software") are the proprietary
property of Pierre Cabell. No part of the Software may be reproduced, distributed,
modified, reverse-engineered, or transmitted in any form or by any means without the
prior written permission of the copyright holder.

Unauthorized use, copying, or distribution of the Software is strictly prohibited and
may result in legal action.

For licensing inquiries, contact the copyright holder via GitHub:
[AVAlii1993](https://github.com/AVAlii1993)

---

<p align="center">
  Built by <strong>Pierre Cabell</strong>
</p>
