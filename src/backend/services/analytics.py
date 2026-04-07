from datetime import datetime
from database import record_analytics, get_url_by_code, increment_click


def track_click(
    short_code: str, ip_address: str = None, user_agent: str = None
) -> dict:
    url_data = get_url_by_code(short_code)

    if not url_data:
        return {"error": "URL not found", "status": 404}

    if url_data.get("expires_at"):
        from services.shortener import is_expired

        if is_expired(url_data["expires_at"]):
            return {"error": "URL expired", "status": 410}

    increment_click(short_code)

    if url_data["id"]:
        record_analytics(url_data["id"], ip_address, user_agent)

    return {
        "original_url": url_data["original_url"],
        "short_code": short_code,
        "clicked": True,
    }


def get_analytics_summary(short_code: str) -> dict:
    from database import get_stats

    return get_stats(short_code)
