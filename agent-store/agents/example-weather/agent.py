"""
Weather Agent for Alii

Returns current weather conditions and a configurable-day forecast for any location.
"""

from typing import Any

try:
    import aiohttp
except ImportError:
    aiohttp = None  # type: ignore[assignment]


class Agent:
    """Fetches current weather and forecasts from a configurable weather API."""

    def __init__(self, config: dict[str, Any]) -> None:
        self.api_key: str = config["weather_api_key"]
        self.units: str = config.get("units", "metric")
        self.forecast_days: int = config.get("forecast_days", 3)
        self._session: aiohttp.ClientSession | None = None

    def _get_session(self) -> "aiohttp.ClientSession":
        if aiohttp is None:
            raise RuntimeError("aiohttp is required: pip install aiohttp")
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=15),
            )
        return self._session

    async def run(self, message: str, context: dict[str, Any]) -> str:
        location = self._extract_location(message, context)
        if not location:
            return "Please specify a location (e.g., 'weather in Tokyo')."

        try:
            session = self._get_session()
            async with session.get(
                "https://api.weather-provider.example.com/forecast",
                params={
                    "q": location,
                    "days": self.forecast_days,
                    "units": self.units,
                    "key": self.api_key,
                },
            ) as resp:
                resp.raise_for_status()
                data = await resp.json()
            return self._format(data, location)
        except RuntimeError as e:
            return str(e)
        except Exception as e:
            return f"Sorry, the weather service is unavailable right now. ({type(e).__name__})"

    def _extract_location(self, message: str, context: dict[str, Any]) -> str:
        """Extract location from user message or context."""
        # Check for explicit user location in context
        user_location = context.get("user_location")
        if user_location and ("my location" in message.lower() or "here" in message.lower()):
            return user_location

        # Simple keyword-based extraction: strip common prefixes
        lowered = message.lower()
        for prefix in ("weather in ", "forecast for ", "temperature in ", "what's the weather in "):
            if prefix in lowered:
                idx = lowered.index(prefix) + len(prefix)
                return message[idx:].strip().rstrip("?.,!")
        # Fallback: use the full message as the location query
        return message.strip()

    def _format(self, data: dict[str, Any], location: str) -> str:
        unit_symbol = "°C" if self.units == "metric" else "°F"

        current = data.get("current", {})
        forecast_days = data.get("forecast", [])

        lines = [f"**{location.title()} -- Current Weather**"]
        if current:
            temp = current.get("temp", "N/A")
            feels = current.get("feels_like", "N/A")
            desc = current.get("description", "")
            humidity = current.get("humidity", "N/A")
            lines.append(f"{desc} | {temp}{unit_symbol} (feels like {feels}{unit_symbol})")
            lines.append(f"Humidity: {humidity}%")

        if forecast_days:
            lines.append(f"\n**{len(forecast_days)}-Day Forecast**")
            for day in forecast_days[: self.forecast_days]:
                date = day.get("date", "")
                high = day.get("high", "N/A")
                low = day.get("low", "N/A")
                desc = day.get("description", "")
                lines.append(f"{date}: {high}{unit_symbol} / {low}{unit_symbol} -- {desc}")

        return "\n".join(lines)

    async def cleanup(self) -> None:
        """Release resources. Called by Alii runtime on shutdown."""
        if self._session and not self._session.closed:
            await self._session.close()
