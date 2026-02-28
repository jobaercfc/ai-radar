"""
GitHub Trending scraper for AI-related repositories.
"""

import httpx
import json
from pathlib import Path
from bs4 import BeautifulSoup
from typing import List, Dict, Any


def load_github_trending_config() -> Dict[str, Any]:
    """Load GitHub Trending configuration from sources.json"""
    sources_file = Path(__file__).parent.parent / "sources.json"
    with open(sources_file, 'r') as f:
        sources = json.load(f)
    
    return sources.get('github_trending', {
        'enabled': True,
        'urls': [
            "https://github.com/trending/python?since=daily",
            "https://github.com/trending?since=daily"
        ],
        'max_items_per_category': 10
    })


def scrape_github_trending() -> List[Dict[str, Any]]:
    """
    Scrape GitHub trending repositories.
    
    Returns:
        List of items with title, url, summary, stars, source
    """
    items = []
    
    # Load config
    config = load_github_trending_config()
    
    if not config.get('enabled', True):
        return items
    
    trending_urls = config.get('urls', [])
    max_items = config.get('max_items_per_category', 10)
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    for trending_url in trending_urls:
        try:
            with httpx.Client(timeout=10.0, follow_redirects=True) as client:
                response = client.get(trending_url, headers=headers)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.text, 'lxml')
                articles = soup.find_all('article', class_='Box-row')
                
                for article in articles[:max_items]:
                    try:
                        # Extract repo name and URL
                        h2 = article.find('h2')
                        if not h2:
                            continue
                        
                        link = h2.find('a')
                        if not link:
                            continue
                        
                        repo_path = link.get('href', '')
                        repo_name = repo_path.strip('/')
                        url = f"https://github.com{repo_path}"
                        
                        # Extract description
                        description_tag = article.find('p', class_='col-9')
                        description = description_tag.get_text(strip=True) if description_tag else ''
                        
                        # Extract stars today
                        stars_tag = article.find('span', class_='d-inline-block float-sm-right')
                        stars_today = stars_tag.get_text(strip=True) if stars_tag else 'N/A'
                        
                        item = {
                            'title': repo_name,
                            'url': url,
                            'summary': f"{description} | {stars_today} stars today",
                            'source': 'GitHub Trending',
                            'source_type': 'github',
                        }
                        items.append(item)
                    
                    except Exception as e:
                        print(f"Error parsing GitHub trending article: {e}")
                        continue
        
        except Exception as e:
            print(f"Error scraping GitHub trending {trending_url}: {e}")
            continue
    
    return items
