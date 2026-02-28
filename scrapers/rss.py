"""
RSS feed scraper for AI news sources.
"""

import feedparser
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Any


def load_rss_feeds() -> List[str]:
    """Load RSS feeds from sources.json"""
    sources_file = Path(__file__).parent.parent / "sources.json"
    with open(sources_file, 'r') as f:
        sources = json.load(f)
    
    # Flatten all feeds from all categories
    feeds = []
    for category in sources.get('rss_feeds', []):
        feeds.extend(category.get('feeds', []))
    
    return feeds


def scrape_rss_feeds() -> List[Dict[str, Any]]:
    """
    Scrape all configured RSS feeds and return recent entries.
    
    Returns:
        List of items with title, url, summary, published, source
    """
    items = []
    cutoff_date = datetime.now() - timedelta(hours=48)
    
    # Load feeds from config
    rss_feeds = load_rss_feeds()
    
    for feed_url in rss_feeds:
        try:
            feed = feedparser.parse(feed_url)
            source_name = feed.feed.get('title', feed_url)
            
            for entry in feed.entries[:10]:  # Take top 10 from each feed
                # Parse published date
                published = None
                if hasattr(entry, 'published_parsed') and entry.published_parsed:
                    published = datetime(*entry.published_parsed[:6])
                elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                    published = datetime(*entry.updated_parsed[:6])
                
                # Filter by date if available
                if published and published < cutoff_date:
                    continue
                
                item = {
                    'title': entry.get('title', 'No title'),
                    'url': entry.get('link', ''),
                    'summary': entry.get('summary', entry.get('description', ''))[:500],
                    'published': published.isoformat() if published else None,
                    'source': source_name,
                    'source_type': 'rss',
                }
                items.append(item)
        
        except Exception as e:
            print(f"Error scraping RSS feed {feed_url}: {e}")
            continue
    
    return items
