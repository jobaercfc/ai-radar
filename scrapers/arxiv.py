"""
arXiv paper scraper for AI/ML research.
"""

import feedparser
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Any


def load_arxiv_config() -> Dict[str, Any]:
    """Load arXiv configuration from sources.json"""
    sources_file = Path(__file__).parent.parent / "sources.json"
    with open(sources_file, 'r') as f:
        sources = json.load(f)

    return sources.get('arxiv', {
        'enabled': True,
        'feeds': []
    })


def scrape_arxiv() -> List[Dict[str, Any]]:
    """
    Scrape arXiv papers from AI/ML categories.

    Returns:
        List of items with title, url, summary, authors, source
    """
    items = []

    # Load config
    config = load_arxiv_config()

    if not config.get('enabled', True):
        return items

    feeds = config.get('feeds', [])
    cutoff_date = datetime.now() - timedelta(hours=48)

    for feed_config in feeds:
        feed_url = feed_config.get('url')
        category = feed_config.get('category', 'arXiv')

        if not feed_url:
            continue

        try:
            feed = feedparser.parse(feed_url)

            for entry in feed.entries[:20]:  # Top 20 per category
                # Parse published date
                published = None
                if hasattr(entry, 'published_parsed') and entry.published_parsed:
                    published = datetime(*entry.published_parsed[:6])
                elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                    published = datetime(*entry.updated_parsed[:6])

                # Filter by date
                if published and published < cutoff_date:
                    continue

                # Extract authors
                authors = []
                if hasattr(entry, 'authors'):
                    authors = [author.get('name', '') for author in entry.authors]
                author_str = ', '.join(authors[:3])  # First 3 authors
                if len(authors) > 3:
                    author_str += ' et al.'

                item = {
                    'title': entry.get('title', 'No title').replace('\n', ' ').strip(),
                    'url': entry.get('link', ''),
                    'summary': entry.get('summary', '')[:500].replace('\n', ' ').strip(),
                    'authors': author_str,
                    'published': published.isoformat() if published else None,
                    'source': category,
                    'source_type': 'arxiv',
                }
                items.append(item)

        except Exception as e:
            print(f"Error scraping arXiv feed {feed_url}: {e}")
            continue

    return items
