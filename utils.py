import httpx

from models import Hook


async def fetch_url(client: httpx.AsyncClient, hook: Hook):
    """Coroutine to fetch a single URL and return the result."""
    try:
        # Just hard-coded order ID, in production it should be real order id
        params = {"order_id": 1}
        response = await client.get(hook.url, params=params, timeout=10.0)
        response.raise_for_status()
        return {
            "url": hook.url,
            "status": "success",
            "status_code": response.status_code,
        }
    except httpx.RequestError as exc:
        return {"url": hook.url, "status": "error", "detail": f"Request failed: {exc}"}
    except httpx.HTTPStatusError as exc:
        return {
            "url": hook.url,
            "status": "error",
            "detail": f"HTTP error: {exc.response.status_code}",
        }
