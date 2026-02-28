"""
Hacker News scraper with AI keyword filtering.
"""

import httpx
import json
from pathlib import Path
from typing import List, Dict, Any


HN_TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
HN_ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"


def load_hackernews_config() -> Dict[str, Any]:
    """Load Hacker News configuration from sources.json"""
    sources_file = Path(__file__).parent.parent / "sources.json"
    with open(sources_file, 'r') as f:
        sources = json.load(f)
    
    return sources.get('hackernews', {
        'enabled': True,
        'top_stories_count': 30,
        'keywords': []
    })


def contains_ai_keywords(text: str, keywords: List[str]) -> bool:
    """Check if text contains any AI-related keywords."""
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in keywords)


def scrape_hackernews() -> List[Dict[str, Any]]:
    """
    Scrape top Hacker News stories filtered by AI keywords.
    
    Returns:
        List of items with title, url, summary, score, source
    """
    items = []
    
    # Load config
    config = load_hackernews_config()
    
    if not config.get('enabled', True):
        return items
    
    keywords = config.get('keywords', [])
    top_count = config.get('top_stories_count', 30)
    
    try:
        with httpx.Client(timeout=10.0) as client:
            # Get top story IDs
            response = client.get(HN_TOP_STORIES_URL)
            response.raise_for_status()
            story_ids = response.json()[:top_count]
            
            for story_id in story_ids:
                try:
                    # Fetch story details
                    story_response = client.get(HN_ITEM_URL.format(story_id))
                    story_response.raise_for_status()
                    story = story_response.json()
                    
                    if not story or story.get('type') != 'story':
                        continue
                    
                    title = story.get('title', '')
                    text = story.get('text', '')
                    
                    # Filter by AI keywords
                    if keywords and not contains_ai_keywords(title + ' ' + text, keywords):
                        continue
                    
                    item = {
                        'title': title,
                        'url': story.get('url', f"https://news.ycombinator.com/item?id={story_id}"),
                        'summary': text[:300] if text else f"Score: {story.get('score', 0)} | {story.get('descendants', 0)} comments",
                        'score': story.get('score', 0),
                        'source': 'Hacker News',
                        'source_type': 'hackernews',
                    }
                    items.append(item)
                
                except Exception as e:
                    print(f"Error fetching HN story {story_id}: {e}")
                    continue
    
    except Exception as e:
        print(f"Error scraping Hacker News: {e}")
    
    return items
