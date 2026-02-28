# AI Radar Changelog

## Latest Updates (2026-03-01)

### ✨ New Features

#### 1. Token Usage & Cost Tracking
- **Real-time cost visibility**: See exactly how much each brief generation costs
- **Token breakdown**: View input/output token counts
- **Transparent pricing**: Based on Claude Sonnet 4 pricing ($3/MTok input, $15/MTok output)

Example output:
```
💰 API USAGE & COST
============================================================
Model: claude-sonnet-4-20250514

Tokens:
  Input:  12,456 tokens
  Output: 3,892 tokens
  Total:  16,348 tokens

Cost:
  Input:  $0.0374
  Output: $0.0584
  Total:  $0.0958
============================================================
```

#### 2. Enhanced TLDR Summaries
- **Longer, more detailed summaries**: 4-5 sentences instead of 2-3
- **Comprehensive coverage**: What happened, key details, technical specifics, and impact
- **Developer-focused**: Technical details that matter to builders
- **Highly scannable**: Detailed but easy to skim

#### 3. Expanded News Sources
Added **6 new RSS feeds** and **3 new expert blogs**:

**New RSS Feeds:**
- DeepMind Blog
- Google AI Blog
- AWS Machine Learning Blog
- GitHub AI/ML Blog
- NVIDIA Developer Blog
- MIT Technology Review

**New Expert Blogs:**
- Sebastian Raschka (LLM researcher)
- Eugene Yan (Applied ML)
- Chip Huyen (ML Systems)

**Total Sources:** 13 RSS feeds + 5 expert blogs + Hacker News + GitHub Trending = **20+ sources**

---

## Impact

### Before:
- ❌ No visibility into API costs
- ❌ Brief 2-3 sentence summaries
- ❌ 6 RSS feeds only

### After:
- ✅ Full cost transparency
- ✅ Comprehensive 4-5 sentence TLDRs with technical depth
- ✅ 13 RSS feeds + 5 expert blogs (20+ total sources)
- ✅ Better signal-to-noise ratio

---

## Usage

No changes to usage - everything works the same:

```bash
# Dry run to see token usage without saving
python main.py --dry-run

# Generate actual brief
python main.py
```

---

## Cost Estimates

Based on typical runs:
- **Input tokens**: ~10,000-15,000 (varies by news volume)
- **Output tokens**: ~3,000-5,000 (comprehensive summaries)
- **Cost per run**: ~$0.05-$0.10
- **Monthly cost** (daily runs): ~$1.50-$3.00

Still essentially free! 💰
