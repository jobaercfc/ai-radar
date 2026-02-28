# 🚀 AI Radar - Complete Setup Guide

Your AI news intelligence agent is fully built and ready!

---

## ✅ What's Included

### **📊 Data Sources (100+ feeds)**
- **60+ RSS Feeds** across 6 categories
- **18 Expert Blogs** (Karpathy, Lilian Weng, etc.)
- **Hacker News** (top 50 stories, 50+ keywords)
- **GitHub Trending** (4 categories)
- **Reddit** (4 AI subreddits)
- **arXiv Papers** (4 ML/AI categories)

### **🤖 AI Providers**
- Anthropic Claude (Sonnet 4, Opus 4)
- OpenAI GPT (4o, 4o-mini, 4-turbo)
- Switch via environment variables

### **✨ Interactive UI Features**
- Mark as read (localStorage)
- Bookmarks
- Reading stats
- Keyboard shortcuts
- Export to Markdown
- Search/filter
- Progress tracking
- All News view (200+ items)

---

## 🏃 Quick Start

### **1. Install Dependencies**

```bash
cd ai-radar
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### **2. Configure API Key**

```bash
cp .env.example .env
# Edit .env and add your API key
```

**Option A: Anthropic (default)**
```bash
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

**Option B: OpenAI (cheaper)**
```bash
AI_PROVIDER=openai
OPENAI_API_KEY=sk-your-key-here
```

### **3. Test Locally**

```bash
# Dry run (no files saved)
python main.py --dry-run

# Generate actual brief
python main.py

# View UI
python3 -m http.server 8000
# Open: http://localhost:8000/docs/
```

---

## 📈 Expected Output

```
🔍 AI Radar - Starting daily brief generation

Step 1: Scraping sources...
Running scraper: RSS Feeds...
  ✓ Collected 85 items from RSS Feeds
Running scraper: Hacker News...
  ✓ Collected 15 items from Hacker News
Running scraper: GitHub Trending...
  ✓ Collected 30 items from GitHub Trending
Running scraper: Blogs...
  ✓ Collected 40 items from Blogs
Running scraper: Reddit...
  ✓ Collected 20 items from Reddit
Running scraper: arXiv Papers...
  ✓ Collected 35 items from arXiv Papers

✓ Total items collected: 225 from 6 sources

Step 2: Analyzing with Claude API...
Using ANTHROPIC - Model: claude-sonnet-4-20250514
✓ Analysis complete

Step 3: Saving results...
✓ Saved to data/latest.json
✓ Saved to data/archive/2026-03-01.json
✓ Updated archive index with 1 dates

📡 BRIEF SUMMARY
============================================================
Date: 2026-03-01
Headline: Claude Code Goes Open Source...
Sections: 5
  🔥 Must Know: 5 items
  📦 New Tools & Releases: 8 items
  🔬 Research Worth Watching: 4 items
  📌 Community Buzz: 6 items

Total items featured: 23
Sources checked: 6
Items processed: 225

💰 API USAGE & COST
============================================================
Provider: ANTHROPIC
Model: claude-sonnet-4-20250514

Tokens:
  Input:  18,450 tokens
  Output: 4,892 tokens
  Total:  23,342 tokens

Cost:
  Input:  $0.0554
  Output: $0.0734
  Total:  $0.1288
============================================================
```

---

## ⌨️ UI Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `m` | Mark as read |
| `b` | Bookmark |
| `s` | Show stats |
| `e` | Export to Markdown |
| `?` | Show help |
| `Esc` | Close modals |

---

## 📝 Adding New Sources

Edit `sources.json`:

```json
{
  "rss_feeds": [
    {
      "category": "Your Category",
      "feeds": [
        "https://your-new-feed.com/rss.xml"
      ]
    }
  ]
}
```

No code changes needed! 🎉

---

## 🌐 Deploy to GitHub

### **1. Create Repo & Push**

```bash
git init
git add .
git commit -m "Initial AI Radar setup"
git remote add origin https://github.com/YOUR_USERNAME/ai-radar.git
git push -u origin main
```

### **2. Add API Key Secret**

Settings → Secrets and variables → Actions → New secret

- Name: `ANTHROPIC_API_KEY` (or `OPENAI_API_KEY`)
- Value: Your API key

### **3. Enable GitHub Pages**

Settings → Pages:
- Source: Deploy from branch
- Branch: `main`
- Folder: `/docs`

**Live at:** `https://YOUR_USERNAME.github.io/ai-radar/`

### **4. Trigger First Run**

Actions → AI Radar Daily Brief → Run workflow

---

## 💰 Cost Estimates

### **Anthropic Claude Sonnet 4**
- Per brief: ~$0.12
- Monthly (daily): ~$3.60
- Yearly: ~$43.80

### **OpenAI GPT-4o (Recommended)**
- Per brief: ~$0.08
- Monthly (daily): ~$2.40
- Yearly: ~$29.20

### **OpenAI GPT-4o-mini (Budget)**
- Per brief: ~$0.005
- Monthly (daily): ~$0.15
- Yearly: ~$1.80

---

## 🎯 Daily Workflow

**Morning Routine (1 hour):**

1. Open `https://YOUR_USERNAME.github.io/ai-radar/`
2. Read **Must Know** section (5 items, ~10 min)
3. Skim **New Tools** (8 items, ~15 min)
4. Browse **Research** (4 items, ~15 min)
5. Check **Community Buzz** (6 items, ~10 min)
6. Search **All News** for specific interests (~10 min)

**Keyboard shortcuts make it fast!**

---

## 🔧 Customization

### **Change Schedule**

Edit `.github/workflows/daily.yml`:

```yaml
schedule:
  - cron: '0 8 * * *'  # 8 AM UTC daily
```

### **Switch AI Provider**

```bash
# Use OpenAI instead
AI_PROVIDER=openai python main.py
```

### **Adjust Limits**

Edit `sources.json`:

```json
{
  "hackernews": {
    "top_stories_count": 100  # Get more stories
  }
}
```

---

## 🐛 Troubleshooting

**No items collected?**
- Check internet connection
- Some feeds may be temporarily down
- GitHub/Reddit scrapers can be rate-limited

**API errors?**
- Verify API key is correct
- Check API credits/quota
- Try switching providers

**UI not loading data?**
- Must use local server (`python3 -m http.server 8000`)
- Can't open index.html directly (CORS issues)

---

## 📚 Documentation

- [sources.json](sources.json) - All data sources
- [.env.example](.env.example) - Configuration template
- [MULTI_PROVIDER_GUIDE.md](MULTI_PROVIDER_GUIDE.md) - AI provider switching
- [CHANGELOG.md](CHANGELOG.md) - Recent updates

---

## 🎉 You're Ready!

Your AI Radar is now:
- ✅ Scraping 100+ sources daily
- ✅ Powered by Claude/GPT
- ✅ Auto-running via GitHub Actions
- ✅ Serving beautiful briefs on GitHub Pages
- ✅ 100% free to operate

**Next:** Star the repo, share with colleagues, enjoy your morning AI news! ☕

---

**Questions?** Check the Actions logs or create an issue.

**Happy reading!** 📡
