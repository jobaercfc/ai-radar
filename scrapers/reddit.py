"""
Reddit scraper for AI-related subreddits.
"""

import httpx
import json
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime


def load_reddit_config() -> Dict[str, Any]:
    """Load Reddit configuration from sources.json"""
    sources_file = Path(__file__).parent.parent / "sources.json"
    with open(sources_file, 'r') as f:
        sources = json.load(f)

    return sources.get('reddit', {
        'enabled': True,
        'feed_urls': []
    })


def scrape_reddit() -> List[Dict[str, Any]]:
    """
    Scrape top Reddit posts from AI subreddits.

    Returns:
        List of items with title, url, summary, score, source
    """
    items = []

    # Load config
    config = load_reddit_config()

    if not config.get('enabled', True):
        return items

    feed_urls = config.get('feed_urls', [])

    headers = {
        'User-Agent': 'web:ai-radar:v1.0 (by /u/ai-radar-bot)',
        'Accept': 'application/json',
    }

    for feed_url in feed_urls:
        try:
            with httpx.Client(timeout=10.0) as client:
                response = client.get(feed_url, headers=headers)
                response.raise_for_status()
                data = response.json()

                posts = data.get('data', {}).get('children', [])

                for post in posts:
                    post_data = post.get('data', {})

                    # Extract subreddit name
                    subreddit = post_data.get('subreddit', 'unknown')

                    item = {
                        'title': post_data.get('title', 'No title'),
                        'url': f"https://reddit.com{post_data.get('permalink', '')}",
                        'summary': (post_data.get('selftext', '') or f"{post_data.get('num_comments', 0)} comments | {post_data.get('score', 0)} upvotes")[:400],
                        'score': post_data.get('score', 0),
                        'source': f'r/{subreddit}',
                        'source_type': 'reddit',
                        'published': datetime.fromtimestamp(post_data.get('created_utc', 0)).isoformat() if post_data.get('created_utc') else None,
                    }
                    items.append(item)

        except Exception as e:
            print(f"Error scraping Reddit {feed_url}: {e}")
            continue

    return items
