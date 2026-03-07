#!/usr/bin/env python3
"""
Validate all agent manifests in the Agent Store against the schema.

Usage:
    python validate.py                          # Validate all agents
    python validate.py agent-store/agents/my-agent/agent.json  # Validate one

Requires: pip install jsonschema
"""

import json
import sys
from pathlib import Path

try:
    import jsonschema
except ImportError:
    print("Error: jsonschema is required. Install it with: pip install jsonschema")
    sys.exit(1)

REPO_ROOT = Path(__file__).resolve().parent
SCHEMA_PATH = REPO_ROOT / "sdk" / "agent-schema.json"
AGENTS_DIR = REPO_ROOT / "agent-store" / "agents"
REGISTRY_PATH = REPO_ROOT / "agent-store" / "registry.json"


def load_json(path: Path) -> dict:
    with open(path) as f:
        return json.load(f)


def validate_manifest(schema: dict, manifest_path: Path) -> list[str]:
    """Validate a single agent.json against the schema. Returns list of errors."""
    errors = []
    try:
        data = load_json(manifest_path)
    except json.JSONDecodeError as e:
        return [f"Invalid JSON: {e}"]

    validator = jsonschema.Draft7Validator(schema)
    for error in sorted(validator.iter_errors(data), key=lambda e: list(e.path)):
        path = ".".join(str(p) for p in error.path) or "(root)"
        errors.append(f"  {path}: {error.message}")

    # Check that id matches directory name
    agent_id = data.get("id", "")
    dir_name = manifest_path.parent.name
    if agent_id and agent_id != dir_name and dir_name != "template":
        errors.append(f"  id '{agent_id}' does not match directory name '{dir_name}'")

    return errors


def validate_registry(schema: dict) -> list[str]:
    """Cross-check registry.json against actual agent directories."""
    errors = []
    if not REGISTRY_PATH.exists():
        return ["registry.json not found"]

    registry = load_json(REGISTRY_PATH)
    agents = registry.get("agents", [])
    registered_ids = set()

    for entry in agents:
        agent_id = entry.get("id", "<missing>")
        registered_ids.add(agent_id)
        agent_path = AGENTS_DIR / agent_id
        if not agent_path.exists():
            errors.append(f"  Registry references '{agent_id}' but directory not found")

    # Check for unregistered agents (excluding template)
    if AGENTS_DIR.exists():
        for agent_dir in sorted(AGENTS_DIR.iterdir()):
            if agent_dir.is_dir() and agent_dir.name != "template":
                if agent_dir.name not in registered_ids:
                    errors.append(f"  Agent '{agent_dir.name}' exists but is not in registry.json")

    return errors


def main() -> int:
    schema = load_json(SCHEMA_PATH)
    total_errors = 0

    # Determine targets
    if len(sys.argv) > 1:
        targets = [Path(p) for p in sys.argv[1:]]
    else:
        targets = sorted(AGENTS_DIR.glob("*/agent.json")) if AGENTS_DIR.exists() else []

    # Validate manifests
    for manifest_path in targets:
        errors = validate_manifest(schema, manifest_path)
        if errors:
            print(f"FAIL  {manifest_path.relative_to(REPO_ROOT)}")
            for e in errors:
                print(e)
            total_errors += len(errors)
        else:
            print(f"OK    {manifest_path.relative_to(REPO_ROOT)}")

    # Validate registry cross-references
    if len(sys.argv) <= 1:
        print()
        registry_errors = validate_registry(schema)
        if registry_errors:
            print("FAIL  agent-store/registry.json (cross-check)")
            for e in registry_errors:
                print(e)
            total_errors += len(registry_errors)
        else:
            print("OK    agent-store/registry.json (cross-check)")

    print(f"\n{'All checks passed.' if total_errors == 0 else f'{total_errors} error(s) found.'}")
    return 1 if total_errors else 0


if __name__ == "__main__":
    sys.exit(main())
