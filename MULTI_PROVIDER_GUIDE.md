# 🔄 Multi-Provider AI Support Guide

AI Radar now supports **both Anthropic Claude and OpenAI GPT** models! Switch between providers using environment variables.

---

## 🎯 Quick Start

### **Option 1: Use Anthropic (Default)**

```bash
# .env file
AI_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

### **Option 2: Use OpenAI**

```bash
# .env file
AI_PROVIDER=openai
OPENAI_API_KEY=sk-your-key-here
```

### **Option 3: Use Both (Switch Anytime)**

```bash
# .env file
AI_PROVIDER=anthropic  # Change to 'openai' to switch
ANTHROPIC_API_KEY=sk-ant-your-key-here
OPENAI_API_KEY=sk-your-key-here
```

---

## 📋 Supported Models

### **Anthropic Models**

| Model | Input Cost | Output Cost | Best For |
|-------|-----------|-------------|----------|
| `claude-sonnet-4-20250514` (default) | $3/MTok | $15/MTok | Balanced performance & cost |
| `claude-opus-4-20250514` | $15/MTok | $75/MTok | Maximum quality |

### **OpenAI Models**

| Model | Input Cost | Output Cost | Best For |
|-------|-----------|-------------|----------|
| `gpt-4o` (default) | $2.50/MTok | $10/MTok | Best value (faster & cheaper) |
| `gpt-4o-mini` | $0.15/MTok | $0.60/MTok | Ultra-low cost |
| `gpt-4-turbo` | $10/MTok | $30/MTok | High performance |

---

## 💰 Cost Comparison

Based on typical AI Radar run (15K input tokens, 4K output tokens):

| Provider | Model | Cost per Run | Monthly (30 runs) |
|----------|-------|--------------|-------------------|
| Anthropic | Claude Sonnet 4 | **$0.105** | **$3.15** |
| Anthropic | Claude Opus 4 | $0.525 | $15.75 |
| OpenAI | GPT-4o | **$0.078** ⭐ | **$2.33** ⭐ |
| OpenAI | GPT-4o-mini | **$0.0046** 🔥 | **$0.14** 🔥 |
| OpenAI | GPT-4-turbo | $0.270 | $8.10 |

**Winner: GPT-4o-mini** at ~$0.005 per brief! 🎉

---

## 🔧 Configuration Examples

### **1. Use Default Provider (Anthropic Sonnet)**

```bash
# .env
ANTHROPIC_API_KEY=sk-ant-your-key-here
# That's it! Uses anthropic + claude-sonnet-4-20250514 by default
```

### **2. Use OpenAI GPT-4o (Cheapest Quality Option)**

```bash
# .env
AI_PROVIDER=openai
OPENAI_API_KEY=sk-your-key-here
# Uses gpt-4o by default
```

### **3. Use OpenAI GPT-4o-mini (Ultra-Cheap)**

```bash
# .env
AI_PROVIDER=openai
AI_MODEL=gpt-4o-mini
OPENAI_API_KEY=sk-your-key-here
```

### **4. Use Anthropic Opus (Best Quality)**

```bash
# .env
AI_PROVIDER=anthropic
AI_MODEL=claude-opus-4-20250514
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

---

## 🚀 Usage

### **Test Locally**

```bash
# With Anthropic
AI_PROVIDER=anthropic python main.py --dry-run

# With OpenAI
AI_PROVIDER=openai python main.py --dry-run

# Override model
AI_PROVIDER=openai AI_MODEL=gpt-4o-mini python main.py --dry-run
```

### **Check Output**

You'll see which provider/model is being used:

```
Step 2: Analyzing with Claude API...
Using OPENAI - Model: gpt-4o
✓ Analysis complete

💰 API USAGE & COST
============================================================
Provider: OPENAI
Model: gpt-4o

Tokens:
  Input:  14,892 tokens
  Output: 3,764 tokens
  Total:  18,656 tokens

Cost:
  Input:  $0.0372
  Output: $0.0376
  Total:  $0.0748
============================================================
```

---

## 🌐 GitHub Actions Setup

### **Configure Secrets**

1. Go to repo **Settings** → **Secrets and variables** → **Actions**
2. Add these secrets:

**For Anthropic:**
- `ANTHROPIC_API_KEY`: Your Anthropic API key
- `AI_PROVIDER`: `anthropic` (optional, this is default)

**For OpenAI:**
- `OPENAI_API_KEY`: Your OpenAI API key
- `AI_PROVIDER`: `openai`

**Optional:**
- `AI_MODEL`: Specific model name (e.g., `gpt-4o-mini`)

### **Switch Providers**

Just update the `AI_PROVIDER` secret:
- Set to `anthropic` → Uses Claude
- Set to `openai` → Uses GPT

---

## 🎯 Recommendations

### **For Daily Production Use:**
**OpenAI GPT-4o** - Best balance of cost, speed, and quality
```bash
AI_PROVIDER=openai
AI_MODEL=gpt-4o  # Optional, this is the default
```

### **For Maximum Savings:**
**OpenAI GPT-4o-mini** - 97% cheaper than Claude Sonnet!
```bash
AI_PROVIDER=openai
AI_MODEL=gpt-4o-mini
```

### **For Best Quality:**
**Anthropic Claude Opus 4** - Highest quality output
```bash
AI_PROVIDER=anthropic
AI_MODEL=claude-opus-4-20250514
```

---

## 🔍 Troubleshooting

### **"ANTHROPIC_API_KEY environment variable not set"**
- You set `AI_PROVIDER=anthropic` but forgot to set `ANTHROPIC_API_KEY`
- Solution: Add your Anthropic API key to `.env`

### **"OPENAI_API_KEY environment variable not set"**
- You set `AI_PROVIDER=openai` but forgot to set `OPENAI_API_KEY`
- Solution: Add your OpenAI API key to `.env`

### **"Invalid AI_PROVIDER"**
- You set `AI_PROVIDER` to something other than `anthropic` or `openai`
- Solution: Use `AI_PROVIDER=anthropic` or `AI_PROVIDER=openai`

### **"Invalid model"**
- You specified a model that doesn't exist or is misspelled
- Solution: Check the supported models table above

---

## 📦 Installation

After pulling these changes, reinstall dependencies:

```bash
pip install -r requirements.txt
```

This adds the `openai` package alongside `anthropic`.

---

## 🎉 Summary

✅ **Dual provider support** (Anthropic + OpenAI)
✅ **Environment variable switching** (no code changes needed)
✅ **Automatic cost calculation** for both providers
✅ **5 model options** to choose from
✅ **Up to 97% cost savings** with GPT-4o-mini

**Default setup (no changes needed):**
- Provider: Anthropic
- Model: Claude Sonnet 4
- Cost: ~$0.10 per brief

**Recommended setup (best value):**
- Provider: OpenAI
- Model: GPT-4o
- Cost: ~$0.08 per brief (25% cheaper!)

**Budget setup (maximum savings):**
- Provider: OpenAI
- Model: GPT-4o-mini
- Cost: ~$0.005 per brief (95% cheaper!)

---

Happy news aggregating! 🚀
