"""
Scraper for specific AI-focused blogs.
"""

import httpx
import json
from pathlib import Path
from bs4 import BeautifulSoup
from typing import List, Dict, Any
import feedparser


def load_blog_sources() -> List[Dict[str, str]]:
    """Load blog sources from sources.json"""
    sources_file = Path(__file__).parent.parent / "sources.json"
    with open(sources_file, 'r') as f:
        sources = json.load(f)
    
    # Add type='rss' to each blog source
    blogs = sources.get('blogs', [])
    for blog in blogs:
        blog['type'] = 'rss'
    
    return blogs


def scrape_blogs() -> List[Dict[str, Any]]:
    """
    Scrape AI-focused blogs.
    
    Returns:
        List of items with title, url, summary, source
    """
    items = []
    
    # Load blog sources from config
    blog_sources = load_blog_sources()
    
    for blog in blog_sources:
        try:
            if blog['type'] == 'rss':
                feed = feedparser.parse(blog['feed_url'])
                
                for entry in feed.entries[:5]:  # Top 5 recent posts
                    item = {
                        'title': entry.get('title', 'No title'),
                        'url': entry.get('link', ''),
                        'summary': entry.get('summary', entry.get('description', ''))[:400],
                        'source': blog['name'],
                        'source_type': 'blog',
                    }
                    items.append(item)
        
        except Exception as e:
            print(f"Error scraping blog {blog['name']}: {e}")
            continue
    
    return items
