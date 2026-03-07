# Contributing to Alii

Thank you for your interest in contributing to the Alii Agent Store. This document covers the process for submitting agents and the standards we expect.

---

## Before You Start

1. Read the [Agent Store README](agent-store/README.md) for submission guidelines
2. Read the [SDK Reference](sdk/README.md) for the agent interface contract
3. Browse [existing agents](agent-store/agents/) for reference implementations

---

## Submitting an Agent

### 1. Fork and clone

```bash
git clone https://github.com/YOUR_USERNAME/Alii-Authentic-Intelligence-Public.git
cd Alii-Authentic-Intelligence-Public
```

### 2. Create your agent

```bash
cp -r agent-store/agents/template agent-store/agents/your-agent-id
```

### 3. Implement and validate

- Fill in `agent.json` with your manifest
- Implement `agent.py` with your logic
- Write a clear `README.md`
- Validate: `python validate.py agent-store/agents/your-agent-id/agent.json`

### 4. Register and submit

- Add your agent to `agent-store/registry.json`
- Branch: `agent/your-agent-id`
- PR title: `[agent] your-agent-id`

---

## Standards

- **One agent per PR**
- **Least privilege** -- only request permissions your agent actually uses
- **No secrets in code** -- use `config_schema` with `"secret": true`
- **Error handling** -- `run()` must return a string in all code paths, never raise
- **Async I/O** -- use `aiohttp` or `httpx`, never synchronous `requests`
- **Clean README** -- include what it does, example I/O, permissions, and config keys
- **Resource cleanup** -- implement `cleanup()` if your agent holds open connections

---

## Code Style

- Python: follow PEP 8, use type hints
- Use descriptive variable names
- Keep agents focused -- one capability per agent

---

## Review Process

Maintainers review for schema validity, least privilege, working implementation, clear documentation, and no hardcoded secrets. Expect feedback within a few days of submission.

---

## Questions

Open an issue tagged `agent-store` or start a GitHub Discussion.

---

Copyright (c) 2026 Pierre Cabell. All Rights Reserved.
