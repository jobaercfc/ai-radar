# ⚡ AI Radar

An AI news intelligence agent that runs daily via GitHub Actions, scrapes AI news from multiple sources, analyzes it with Claude API, and serves a beautiful daily brief on GitHub Pages. Completely free, no server required.

[![Live Demo](https://img.shields.io/badge/demo-live-brightgreen)](https://YOUR_USERNAME.github.io/ai-radar/)
[![Daily Brief](https://github.com/YOUR_USERNAME/ai-radar/actions/workflows/daily.yml/badge.svg)](https://github.com/YOUR_USERNAME/ai-radar/actions/workflows/daily.yml)

## Features

- 🤖 **Automated**: Runs daily via GitHub Actions
- 🧠 **AI-Powered**: Claude Sonnet 4 analyzes and summarizes news
- 📰 **Multi-Source**: RSS feeds, Hacker News, GitHub Trending, AI blogs
- 🎨 **Beautiful UI**: Single-file, modern dark mode interface
- 💾 **Archive**: Full history of past briefs
- 💰 **Free**: Hosted on GitHub Pages, no server costs

## Live Demo

![AI Radar Screenshot](docs/screenshot.png)

Visit the live demo: [YOUR_USERNAME.github.io/ai-radar](https://YOUR_USERNAME.github.io/ai-radar/)

## Quick Setup

### 1. Fork This Repository

Click the "Fork" button at the top of this page.

### 2. Add Your API Key

1. Get an Anthropic API key from [console.anthropic.com](https://console.anthropic.com/settings/keys)
2. Go to your fork's Settings → Secrets and variables → Actions
3. Click "New repository secret"
4. Name: `ANTHROPIC_API_KEY`
5. Value: Your API key
6. Click "Add secret"

### 3. Enable GitHub Pages

1. Go to Settings → Pages
2. Source: "Deploy from a branch"
3. Branch: `main` (or `master`)
4. Folder: `/docs`
5. Click "Save"

Your site will be live at `https://YOUR_USERNAME.github.io/ai-radar/` in a few minutes!

## Local Development

### Run a Test Generation

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/ai-radar.git
cd ai-radar

# Create .env file
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY

# Install dependencies
pip install -r requirements.txt

# Run in dry-run mode (no files saved)
python main.py --dry-run
```

### Generate a Real Brief Locally

```bash
python main.py
```

This will:
- Scrape all configured sources
- Analyze with Claude API
- Save to `data/latest.json` and `data/archive/YYYY-MM-DD.json`
- Update the archive index

## Configuration

### Add More RSS Feeds

Edit [`scrapers/rss.py`](scrapers/rss.py) and add URLs to the `RSS_FEEDS` list:

```python
RSS_FEEDS = [
    "https://openai.com/news/rss.xml",
    "https://your-new-feed.com/rss.xml",  # Add here
]
```

### Change the Schedule

Edit [`.github/workflows/daily.yml`](.github/workflows/daily.yml):

```yaml
on:
  schedule:
    - cron: '0 8 * * *'  # Change this cron expression
```

Cron examples:
- `0 8 * * *` - 8 AM UTC daily
- `0 */6 * * *` - Every 6 hours
- `0 12 * * 1` - Mondays at noon

### Customize the Frontend

The entire frontend is in [`docs/index.html`](docs/index.html). It's a single self-contained HTML file with Tailwind CSS via CDN and vanilla JavaScript. Modify as needed!

## Data Sources

AI Radar aggregates news from:

- **RSS Feeds**: OpenAI, Anthropic, Mistral, HuggingFace, Google AI, BAIR
- **Hacker News**: Top 30 stories filtered by AI keywords
- **GitHub Trending**: Daily trending repos (all languages + Python)
- **Blogs**: Simon Willison, Latent Space

## How It Works

1. **Scraping**: Python scripts fetch content from multiple sources
2. **Analysis**: Claude API processes raw content and returns structured JSON
3. **Storage**: Results saved to `data/latest.json` and archived
4. **Deployment**: GitHub Actions commits changes and GitHub Pages serves the UI

## Manual Trigger

You can manually trigger a brief generation:

1. Go to Actions → AI Radar Daily Brief
2. Click "Run workflow"
3. Click the green "Run workflow" button

## Troubleshooting

### No brief generated

- Check if `ANTHROPIC_API_KEY` is set in repository secrets
- Look at the GitHub Actions log for errors
- Verify you haven't hit Anthropic API rate limits

### GitHub Pages not updating

- Ensure Pages is enabled in Settings → Pages
- Wait a few minutes after the action completes
- Check that the `docs/` folder is being served

### Scraper errors

Individual scraper failures won't crash the entire process. Check the GitHub Actions log to see which sources failed and why.

## Contributing

Contributions welcome! Ideas:
- Add more data sources
- Improve the frontend design
- Better categorization logic
- Email notifications
- RSS feed output

## License

MIT License - feel free to fork and customize!

---

**Built with ❤️ using Claude API**
