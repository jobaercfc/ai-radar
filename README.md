# ⚡ AI Radar

An AI news intelligence agent that runs daily via GitHub Actions, scrapes AI news from 100+ sources, analyzes it with AI (Anthropic Claude or OpenAI GPT), and serves a beautiful daily brief. Completely automated, no server required.

[![Live Demo](https://img.shields.io/badge/demo-live-brightgreen)](https://ai-radar-beige.vercel.app)
[![Daily Brief](https://github.com/jobaercfc/ai-radar/actions/workflows/daily.yml/badge.svg)](https://github.com/jobaercfc/ai-radar/actions/workflows/daily.yml)

## 🎯 Live Demo

**[ai-radar-beige.vercel.app](https://ai-radar-beige.vercel.app)**

## ✨ Features

- 🤖 **Automated**: Runs daily at 8 AM UTC via GitHub Actions
- 🧠 **Multi-Provider AI**: Choose between Anthropic Claude or OpenAI GPT models
- 📰 **100+ Sources**: RSS feeds, Hacker News, GitHub Trending, Reddit, arXiv, AI blogs
- 🎨 **Interactive UI**: Dark/light mode, bookmarks, reading progress, keyboard shortcuts
- 📊 **Smart Categorization**: AI categorizes ALL items into must-know, tools, research, etc.
- 💾 **Token Tracking**: See real-time API usage and costs
- 💰 **Free Infrastructure**: Hosted on Vercel, runs on GitHub Actions

## 🚀 Quick Setup

### 1. Fork This Repository

Click the "Fork" button at the top of this page.

### 2. Choose Your AI Provider

You can use either **Anthropic Claude** (recommended) or **OpenAI GPT**:

#### Option A: Anthropic Claude (Recommended)

1. Get an API key from [console.anthropic.com](https://console.anthropic.com/settings/keys)
2. Go to your fork's **Settings → Secrets and variables → Actions**
3. Click **"New repository secret"**
4. Name: `ANTHROPIC_API_KEY`
5. Value: Your API key
6. Click **"Add secret"**

#### Option B: OpenAI GPT

1. Get an API key from [platform.openai.com](https://platform.openai.com/api-keys)
2. Go to your fork's **Settings → Secrets and variables → Actions**
3. Add two secrets:
   - Name: `AI_PROVIDER`, Value: `openai`
   - Name: `OPENAI_API_KEY`, Value: Your API key

**Optional**: Add `AI_MODEL` secret to use a specific model:
- For Anthropic: `claude-sonnet-4-20241022` (default) or `claude-opus-4-20241022`
- For OpenAI: `gpt-4o` (default), `gpt-4o-mini`, or `gpt-4-turbo`

### 3. Deploy to Vercel

1. Go to [vercel.com](https://vercel.com) and sign in with GitHub
2. Click **"Add New... → Project"**
3. Import your forked `ai-radar` repository
4. Click **"Deploy"**

Your site will be live in ~30 seconds! 🎉

### 4. Run the Workflow

The workflow runs automatically at 8 AM UTC daily, but you can trigger it manually:

1. Go to **Actions → AI Radar Daily Brief**
2. Click **"Run workflow"**
3. Click the green **"Run workflow"** button

## 💻 Local Development

### Run a Test Generation

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/ai-radar.git
cd ai-radar

# Set up Python environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cat > .env << EOF
AI_PROVIDER=anthropic  # or 'openai'
ANTHROPIC_API_KEY=your_anthropic_key_here
# OPENAI_API_KEY=your_openai_key_here  # if using OpenAI
EOF

# Generate brief
python main.py
```

This will:
- Scrape all 100+ configured sources
- Analyze with your chosen AI provider
- Display token usage and costs
- Save to `data/latest.json`

### View Locally

```bash
# Serve the site locally
python -m http.server 8000

# Open http://localhost:8000 in your browser
```

## 🛠️ Configuration

### Customize Sources

All sources are configured in [`sources.json`](sources.json):

```json
{
  "rss_feeds": [
    { "category": "Major AI Companies", "feeds": ["..."] }
  ],
  "blogs": [
    { "name": "Simon Willison", "feed_url": "..." }
  ],
  "hackernews": {
    "enabled": true,
    "keywords": ["ai", "llm", "gpt", ...]
  },
  "reddit": {
    "enabled": true,
    "feed_urls": [...]
  }
}
```

### Change the Schedule

Edit [`.github/workflows/daily.yml`](.github/workflows/daily.yml):

```yaml
on:
  schedule:
    - cron: '0 8 * * *'  # 8 AM UTC daily (change as needed)
  workflow_dispatch:  # Allows manual trigger
```

**Cron examples:**
- `0 8 * * *` - 8 AM UTC daily
- `0 */6 * * *` - Every 6 hours
- `0 12 * * 1` - Mondays at noon UTC

### Customize the Frontend

The entire UI is in [`index.html`](index.html) - a single self-contained HTML file with:
- Tailwind CSS (via CDN)
- Vanilla JavaScript
- localStorage for persistence
- Keyboard shortcuts (press `?` to see all)

## 📦 Data Sources

AI Radar aggregates news from 100+ sources:

### RSS Feeds (60+)
- **Major AI Companies**: OpenAI, Anthropic, Mistral, HuggingFace, Google AI, DeepMind
- **Research**: BAIR, Google AI Blog, AWS ML Blog
- **Developer Tools**: GitHub AI/ML Blog, NVIDIA Developer Blog
- **News & Analysis**: MIT Tech Review, VentureBeat AI

### Blogs (18)
- Simon Willison, Latent Space, Sebastian Raschka, Eugene Yan, Chip Huyen, and more

### Other Sources
- **Hacker News**: Top 30 stories filtered by 50+ AI keywords
- **GitHub Trending**: Python + All languages (daily)
- **Reddit**: r/MachineLearning, r/LocalLLaMA, r/singularity, r/ArtificialIntelligence
- **arXiv**: Latest AI/ML papers from cs.AI, cs.LG, cs.CL, cs.CV

## 🏗️ How It Works

1. **Scraping**: Python scripts fetch content from 100+ sources in parallel
2. **Analysis**: AI (Claude or GPT) processes raw content:
   - Categorizes into sections (Must Know, New Tools, Research, etc.)
   - Generates comprehensive 4-5 sentence summaries
   - Deduplicates across sections
   - Extracts metadata (source, published date)
3. **Storage**: Saves structured JSON to repository
4. **Deployment**:
   - GitHub Actions commits `data/latest.json`
   - Vercel auto-deploys the updated site

## 🔧 Troubleshooting

### No brief generated

- Check if API key secret is set correctly in **Settings → Secrets**
- Look at **Actions** log for errors
- Verify you haven't hit API rate limits
- Ensure `data/latest.json` is being committed (check git log)

### Vercel deployment not updating

- Check that Vercel is connected to your GitHub repository
- Verify automatic deployments are enabled in Vercel settings
- Pull latest changes: `git pull origin main`

### Scraper errors

Individual scraper failures won't crash the process. Check the **Actions** log to see which sources failed and why (rate limits, changed URLs, etc.).

### High API costs

- Use `gpt-4o-mini` instead of `gpt-4o` (90% cheaper)
- Use `claude-sonnet-4` instead of `claude-opus-4` (5x cheaper)
- Reduce sources in `sources.json`
- The workflow shows token usage and costs in the logs

## 📊 Model Pricing (as of 2024)

| Provider | Model | Input (per 1M tokens) | Output (per 1M tokens) |
|----------|-------|----------------------|------------------------|
| Anthropic | Claude Sonnet 4 | $3.00 | $15.00 |
| Anthropic | Claude Opus 4 | $15.00 | $75.00 |
| OpenAI | GPT-4o | $2.50 | $10.00 |
| OpenAI | GPT-4o-mini | $0.15 | $0.60 |
| OpenAI | GPT-4 Turbo | $10.00 | $30.00 |

💡 **Tip**: For daily briefs with 100+ sources, expect ~50K-100K tokens (~$0.50-$2.00 per run with recommended models).

## 🤝 Contributing

Contributions welcome! Ideas:
- Add more data sources (Twitter/X, YouTube, newsletters)
- Improve categorization logic
- Email/Slack notifications
- RSS feed output
- Better error handling
- UI improvements

## 📄 License

MIT License - feel free to fork and customize!

---
