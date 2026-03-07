"""
Web Search Agent for Alii

Performs real-time web searches and returns summarized answers with source links.
"""

from typing import Any

try:
    import aiohttp
except ImportError:
    aiohttp = None  # type: ignore[assignment]


class Agent:
    """Searches the web via a configurable search API and returns summarized results."""

    def __init__(self, config: dict[str, Any]) -> None:
        self.api_key: str = config["search_api_key"]
        self.max_results: int = config.get("max_results", 5)
        self.language: str = config.get("language", "en")
        self._session: aiohttp.ClientSession | None = None

    def _get_session(self) -> "aiohttp.ClientSession":
        if aiohttp is None:
            raise RuntimeError("aiohttp is required: pip install aiohttp")
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession(
                headers={"Authorization": f"Bearer {self.api_key}"},
                timeout=aiohttp.ClientTimeout(total=15),
            )
        return self._session

    async def run(self, message: str, context: dict[str, Any]) -> str:
        try:
            session = self._get_session()
            async with session.get(
                "https://api.search-provider.example.com/search",
                params={
                    "q": message,
                    "limit": self.max_results,
                    "lang": self.language,
                },
            ) as resp:
                resp.raise_for_status()
                data = await resp.json()
            return self._format(data)
        except RuntimeError as e:
            return str(e)
        except Exception as e:
            return f"Sorry, the search service is unavailable right now. ({type(e).__name__})"

    def _format(self, data: dict[str, Any]) -> str:
        results = data.get("results", [])
        if not results:
            return "No results found for your query."
        lines = [f"- **{r['title']}**: {r['url']}" for r in results[: self.max_results]]
        return "Here's what I found:\n\n" + "\n".join(lines)

    async def cleanup(self) -> None:
        """Release resources. Called by Alii runtime on shutdown."""
        if self._session and not self._session.closed:
            await self._session.close()
