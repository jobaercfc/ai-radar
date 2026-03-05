"""
Estimate article reading time by fetching the actual page content.
"""

import math
import httpx
from bs4 import BeautifulSoup
from typing import List, Dict, Any

WORDS_PER_MINUTE = 200
REQUEST_TIMEOUT = 8.0
HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; AIRadar/1.0)"
}

# Tags that typically contain article body text
ARTICLE_SELECTORS = ["article", "[role='main']", "main", ".post-content", ".entry-content", ".article-body"]

# Tags to strip before counting words
STRIP_TAGS = ["script", "style", "nav", "header", "footer", "aside", "form", "noscript", "iframe"]


def _extract_text(html: str) -> str:
    """Extract readable text from HTML."""
    soup = BeautifulSoup(html, "lxml")

    # Remove non-content tags
    for tag in soup.find_all(STRIP_TAGS):
        tag.decompose()

    # Try to find the article body specifically
    for selector in ARTICLE_SELECTORS:
        el = soup.select_one(selector)
        if el:
            text = el.get_text(separator=" ", strip=True)
            if len(text.split()) > 50:  # Only use if substantial
                return text

    # Fallback to body text
    body = soup.find("body")
    if body:
        return body.get_text(separator=" ", strip=True)

    return soup.get_text(separator=" ", strip=True)


def estimate_read_time(url: str) -> int | None:
    """
    Fetch article at URL and return estimated reading time in minutes.

    Returns None if the page can't be fetched or parsed.
    """
    try:
        with httpx.Client(timeout=REQUEST_TIMEOUT, follow_redirects=True) as client:
            resp = client.get(url, headers=HEADERS)
            resp.raise_for_status()

            content_type = resp.headers.get("content-type", "")
            if "text/html" not in content_type:
                return None

            text = _extract_text(resp.text)
            word_count = len(text.split())

            if word_count < 20:
                return None

            return max(1, math.ceil(word_count / WORDS_PER_MINUTE))

    except Exception:
        return None


def enrich_items_with_read_time(items: List[Dict[str, Any]]) -> None:
    """
    Add 'read_time_minutes' field to each item by fetching the article URL.

    Modifies items in place. Skips items that already have the field
    or where the URL can't be fetched.
    """
    seen_urls = {}

    for i, item in enumerate(items):
        url = item.get("url", "")
        if not url:
            continue

        # Reuse result for duplicate URLs
        if url in seen_urls:
            item["read_time_minutes"] = seen_urls[url]
            continue

        minutes = estimate_read_time(url)
        if minutes is not None:
            item["read_time_minutes"] = minutes
        seen_urls[url] = minutes

        if (i + 1) % 10 == 0:
            print(f"  ... estimated read time for {i + 1}/{len(items)} items")
