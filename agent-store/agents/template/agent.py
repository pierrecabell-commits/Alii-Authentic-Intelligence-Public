"""
Template Agent for Alii

Copy this file into your agent directory and implement the `run` method.
The `Agent` class name is required -- Alii discovers agents by this name.
"""

from typing import Any


class Agent:
    """Alii Agent base class. Instantiated once; `run` called per message."""

    def __init__(self, config: dict[str, Any]) -> None:
        self.config = config
        self.max_results: int = config.get("max_results", 5)
        # Access vault-injected secrets declared in config_schema:
        # self.api_key: str = config["api_key"]

    async def run(self, message: str, context: dict[str, Any]) -> str:
        """Handle an incoming message and return a response.

        Args:
            message: The user's raw message text.
            context: Runtime context from Alii. Common keys:
                     user_id, channel, session_id, history, memory.

        Returns:
            A string response delivered to the user.
        """
        # Replace the body below with your actual implementation.
        return (
            f"Template agent received: '{message}'. "
            "Replace this with your real implementation."
        )

    async def cleanup(self) -> None:
        """Release resources. Called by Alii runtime on shutdown.

        Override this if your agent holds open connections, file handles,
        or other resources that need explicit cleanup.
        """
