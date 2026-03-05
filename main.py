#!/usr/bin/env python3
"""
AI Radar - AI News Intelligence Agent

Scrapes AI news from multiple sources, analyzes with AI,
and generates a daily brief.
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

from scrapers import (
    scrape_rss_feeds,
    scrape_hackernews,
    scrape_github_trending,
    scrape_blogs,
    scrape_reddit,
    scrape_arxiv,
)
from scrapers.readtime import enrich_items_with_read_time
from agent import analyze_content


def run_scrapers():
    """
    Run all scrapers and collect items.

    Returns:
        Tuple of (all_items, sources_checked)
    """
    all_items = []
    sources_checked = 0

    scrapers = [
        ("RSS Feeds", scrape_rss_feeds),
        ("Hacker News", scrape_hackernews),
        ("GitHub Trending", scrape_github_trending),
        ("Blogs", scrape_blogs),
        ("Reddit", scrape_reddit),
        ("arXiv Papers", scrape_arxiv),
    ]

    for scraper_name, scraper_func in scrapers:
        try:
            print(f"Running scraper: {scraper_name}...")
            items = scraper_func()
            all_items.extend(items)
            sources_checked += 1
            print(f"  ✓ Collected {len(items)} items from {scraper_name}")
        except Exception as e:
            print(f"  ✗ Error in {scraper_name}: {e}")
            continue

    return all_items, sources_checked


def save_brief(brief: dict, dry_run: bool = False):
    """
    Save brief to data/latest.json and data/archive/YYYY-MM-DD.json

    Args:
        brief: The generated brief
        dry_run: If True, only print to console
    """
    if dry_run:
        print("\n" + "="*60)
        print("DRY RUN - Brief would be saved as:")
        print("="*60)
        print(json.dumps(brief, indent=2))
        return

    # Ensure directories exist
    data_dir = Path("data")
    archive_dir = data_dir / "archive"
    data_dir.mkdir(exist_ok=True)
    archive_dir.mkdir(exist_ok=True)

    # Save to latest.json
    latest_path = data_dir / "latest.json"
    with open(latest_path, 'w') as f:
        json.dump(brief, f, indent=2)
    print(f"\n✓ Saved to {latest_path}")

    # Save to archive
    date_str = brief.get('date', datetime.now().strftime('%Y-%m-%d'))
    archive_path = archive_dir / f"{date_str}.json"
    with open(archive_path, 'w') as f:
        json.dump(brief, f, indent=2)
    print(f"✓ Saved to {archive_path}")

    # Update archive index
    update_archive_index()


def update_archive_index():
    """
    Update data/archive/index.json with list of available dates.
    """
    archive_dir = Path("data/archive")
    if not archive_dir.exists():
        return

    # Get all JSON files (excluding index.json)
    archive_files = sorted(
        [f.stem for f in archive_dir.glob("*.json") if f.stem != "index"],
        reverse=True  # Most recent first
    )

    index_path = archive_dir / "index.json"
    with open(index_path, 'w') as f:
        json.dump(archive_files, f, indent=2)
    print(f"✓ Updated archive index with {len(archive_files)} dates")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="AI Radar - AI News Intelligence Agent")
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Print output to console without saving files'
    )
    args = parser.parse_args()

    # Load environment variables
    load_dotenv()

    print("🔍 AI Radar - Starting daily brief generation\n")

    # Run scrapers
    print("Step 1: Scraping sources...")
    all_items, sources_checked = run_scrapers()
    print(f"\n✓ Total items collected: {len(all_items)} from {sources_checked} sources\n")

    if len(all_items) == 0:
        print("⚠️  No items collected. Exiting.")
        sys.exit(1)

    # Estimate reading times by fetching articles
    print("Step 2: Estimating article reading times...")
    enrich_items_with_read_time(all_items)
    enriched = sum(1 for it in all_items if 'read_time_minutes' in it)
    print(f"✓ Estimated read time for {enriched}/{len(all_items)} articles\n")

    # Analyze with AI
    print("Step 3: Analyzing with AI...")
    try:
        brief, usage_stats = analyze_content(all_items, sources_checked)
        print("✓ Analysis complete\n")
    except Exception as e:
        print(f"✗ Error during analysis: {e}")
        sys.exit(1)

    # Propagate read_time_minutes from scraped items to section items by URL
    read_times = {it['url']: it['read_time_minutes'] for it in all_items if 'read_time_minutes' in it}
    for section in brief.get('sections', []):
        for item in section.get('items', []):
            if item.get('url') in read_times:
                item['read_time_minutes'] = read_times[item['url']]

    # Add all scraped items to the brief for transparency
    brief['all_items'] = all_items

    # Save results
    print("Step 4: Saving results...")
    save_brief(brief, dry_run=args.dry_run)

    # Print summary
    print("\n" + "="*60)
    print("📡 BRIEF SUMMARY")
    print("="*60)
    print(f"Date: {brief.get('date')}")
    print(f"Headline: {brief.get('headline')}")
    print(f"Sections: {len(brief.get('sections', []))}")

    section_count = 0
    item_count = 0
    for section in brief.get('sections', []):
        section_count += 1
        items = len(section.get('items', []))
        item_count += items
        print(f"  {section.get('emoji', '')} {section.get('title')}: {items} items")

    print(f"\nTotal items featured: {item_count}")
    print(f"Sources checked: {brief.get('stats', {}).get('sources_checked', 0)}")
    print(f"Items processed: {brief.get('stats', {}).get('items_processed', 0)}")

    # Print token usage and cost
    print("\n" + "="*60)
    print("💰 API USAGE & COST")
    print("="*60)
    print(f"Provider: {usage_stats['provider'].upper()}")
    print(f"Model: {usage_stats['model']}")
    print(f"\nTokens:")
    print(f"  Input:  {usage_stats['input_tokens']:,} tokens")
    print(f"  Output: {usage_stats['output_tokens']:,} tokens")
    print(f"  Total:  {usage_stats['total_tokens']:,} tokens")
    print(f"\nCost:")
    print(f"  Input:  ${usage_stats['input_cost']:.4f}")
    print(f"  Output: ${usage_stats['output_cost']:.4f}")
    print(f"  Total:  ${usage_stats['total_cost']:.4f}")
    print("="*60)

    if not args.dry_run:
        print("\n✅ Brief generated successfully!")
    else:
        print("\n✅ Dry run complete (no files saved)")


if __name__ == "__main__":
    main()
