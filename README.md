# Alii — Authentic Intelligence

> **The self-evolving autonomous AI that lives where your people are.**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Agent Store](https://img.shields.io/badge/Agent%20Store-open-brightgreen)](agent-store/)
[![SDK](https://img.shields.io/badge/SDK-stable-blue)](sdk/)

---

## What is Alii?

Alii is an autonomous, multi-channel AI system built to operate across every platform your users inhabit — simultaneously, coherently, and without manual intervention.

Alii routes intent, learns from interaction, manages credentials, persists memory, and deploys agents — all from a single sovereign intelligence layer. It is not a chatbot. It is not a wrapper. It is an operating system for AI presence.

**Channels supported out of the box:**
Discord · Telegram · Slack · iMessage · Signal · WhatsApp · Web

---

## The Agent Store

The Agent Store is the open, community-contributed extension layer for Alii. Agents are discrete units of capability — a search agent, a weather agent, a CRM lookup agent, a code reviewer — packaged as self-describing modules that Alii can discover, load, and invoke at runtime.

Anyone can build an agent. Anyone can publish one. Alii routes to them automatically.

This repository **is** the Agent Store. Browse [`agent-store/`](agent-store/), fork, build, and submit a PR.

---

## Repository Layout

```
Alii-Authentic-Intelligence-Public/
├── README.md                          # You are here
├── .gitignore
│
├── agent-store/
│   ├── README.md                      # How to submit agents
│   ├── registry.json                  # Master agent registry
│   └── agents/
│       ├── template/                  # Canonical agent template
│       │   ├── agent.json             # Manifest
│       │   ├── agent.py               # Implementation
│       │   └── README.md
│       ├── example-search/            # Example: web search agent
│       │   ├── agent.json
│       │   └── README.md
│       └── example-weather/           # Example: weather agent
│           ├── agent.json
│           └── README.md
│
├── sdk/
│   ├── README.md                      # SDK documentation
│   └── agent-schema.json              # JSON Schema for agent.json
│
└── docs/
    ├── getting-started.md
    └── building-agents.md
```

---

## Quick Start

```bash
# Clone the repo
git clone https://github.com/AVAlii1993/Alii-Authentic-Intelligence-Public.git
cd Alii-Authentic-Intelligence-Public

# Copy the agent template
cp -r agent-store/agents/template agent-store/agents/my-agent
cd agent-store/agents/my-agent

# Edit the manifest
nano agent.json

# Edit the implementation
nano agent.py

# Validate against the schema
npx ajv validate -s ../../sdk/agent-schema.json -d agent.json

# Register your agent
# Add an entry to agent-store/registry.json, then open a PR
```

---

## How to Build an Agent

**Step 1 — Fork this repository**

Click "Fork" on GitHub. Clone your fork locally.

**Step 2 — Copy the template**

```bash
cp -r agent-store/agents/template agent-store/agents/your-agent-id
```

**Step 3 — Fill in `agent.json` and `agent.py`**

Open `agent.json` and set your `id`, `name`, `description`, `tags`, and `permissions`. Open `agent.py` and implement the `run(message, context)` method. Your agent receives the user's message and a context object, and returns a string response.

**Step 4 — Register and submit a PR**

Add your agent entry to `agent-store/registry.json`. Write a clear `README.md` in your agent folder. Open a pull request with the title `[agent] your-agent-id`. The maintainer will review and merge.

See [`docs/building-agents.md`](docs/building-agents.md) for the full guide.

---

## Ecosystem

| Repository | Access | Description |
|---|---|---|
| **Alii-Authentic-Intelligence-Public** | Public | Open agent store, SDK, and documentation. This repo. |
| **Alii-Core** | Private | TypeScript gateway — channel connectors (Discord, Telegram, Slack, iMessage, Signal, WhatsApp, web), routing engine, session management. |
| **Alii-God** | Private | Python brain — LLM orchestration, memory (Qdrant), vault guardian, todo agent, account agent, self-evolution loop. |

Community contributions live here. The intelligence that uses them lives in the private repos above.

---

## Contributing

1. Read [`agent-store/README.md`](agent-store/README.md) before submitting an agent.
2. Validate your `agent.json` against [`sdk/agent-schema.json`](sdk/agent-schema.json).
3. One agent per PR. Include a clear README and working implementation.
4. Be excellent.

---

## License

MIT — see [LICENSE](LICENSE).

---

Built by **Pierre Cabell**.
