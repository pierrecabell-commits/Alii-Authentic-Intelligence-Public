"""
Template Agent for Alii

Copy this file into your agent directory and implement the `run` method.
The `Agent` class name is required — Alii discovers agents by this name.
"""

from typing import Any


class Agent:
    """
    Alii Agent base class.

    Alii instantiates your agent once with the merged config (defaults +
    user-supplied values + vault-injected secrets). The `run` method is
    called for every message routed to this agent.
    """

    def __init__(self, config: dict[str, Any]) -> None:
        """
        Initialize the agent with resolved config.

        Args:
            config: Merged configuration dict. Keys match your agent.json
                    config_schema properties. Secrets are injected by Alii
                    before this method is called — never fetch them yourself.
        """
        self.config = config
        self.max_results: int = config.get("max_results", 5)
        # If you declared an api_key in config_schema, access it here:
        # self.api_key: str = config.get("api_key", "")

    async def run(self, message: str, context: dict[str, Any]) -> str:
        """
        Handle an incoming message and return a response.

        This is the only method Alii calls at runtime. It must:
        - Be async
        - Accept `message` (str) and `context` (dict)
        - Return a plain string in all code paths

        Args:
            message:  The user's raw message text.
            context:  Runtime context provided by Alii. Common keys:
                        - context["user_id"]      str  — stable user identifier
                        - context["channel"]      str  — "discord" | "telegram" | etc.
                        - context["session_id"]   str  — current session
                        - context["history"]      list — recent message history
                        - context["memory"]       dict — retrieved memory fragments

        Returns:
            A string response that Alii will deliver to the user.
        """
        # Replace the body below with your actual implementation.
        return (
            f"Template agent received: '{message}'. "
            "Replace this with your real implementation."
        )
