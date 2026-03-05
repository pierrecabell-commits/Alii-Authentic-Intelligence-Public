# Weather Agent

Returns current weather conditions and a configurable-day forecast for any city or location.

---

## What It Does

When Alii routes a message to this agent, it:

1. Extracts the location from the user's message (city name, coordinates, or "my location")
2. Queries the weather API for current conditions
3. Fetches the forecast for the configured number of days
4. Returns a clean, human-readable summary

---

## Example Interactions

**Input:**
> What's the weather like in Tokyo?

**Output:**
> **Tokyo — Current Weather**
> 🌤 Partly cloudy · 14°C · Feels like 12°C
> Humidity: 62% · Wind: 18 km/h NW
>
> **3-Day Forecast**
> Thu: ⛅ 16°C / 9°C — Partly cloudy
> Fri: 🌧 13°C / 8°C — Light rain
> Sat: ☀️ 18°C / 10°C — Sunny

---

**Input:**
> Will it rain in Paris this weekend?

**Output:**
> **Paris — Weekend Forecast**
> Sat: 🌧 11°C / 6°C — Rain (80% chance) · 12mm expected
> Sun: ⛅ 13°C / 7°C — Partly cloudy · 20% chance of showers

---

## Permissions

| Permission | Reason |
|---|---|
| `network` | Required for outbound HTTP requests to the weather API |

---

## Configuration

| Key | Type | Required | Description |
|---|---|---|---|
| `weather_api_key` | string | Yes | Weather provider API key (vault-injected) |
| `units` | string | No | `"metric"` (°C) or `"imperial"` (°F) — default: `"metric"` |
| `forecast_days` | integer | No | Days of forecast to include (default: 3, max: 7) |

---

## Supported Weather Providers

This agent works with any REST weather API. Tested against:

- [Open-Meteo](https://open-meteo.com/) — free, no API key required for basic use
- [OpenWeatherMap](https://openweathermap.org/api) — requires API key
- [WeatherAPI](https://www.weatherapi.com/) — requires API key

Set `weather_api_key` to an empty string if using Open-Meteo's free tier.

---

## Implementation Notes

The reference `agent.py` should:

- Use `aiohttp` or `httpx` for async HTTP
- Handle location ambiguity (ask for clarification if multiple cities match)
- Support "my location" by reading `context["user_location"]` if available
- Return formatted text, not raw JSON
- Handle API errors and rate limits gracefully
