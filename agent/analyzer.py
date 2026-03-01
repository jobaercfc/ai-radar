"""
Multi-provider AI content analyzer.
Supports both Anthropic Claude and OpenAI GPT models.
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Any, Tuple


SYSTEM_PROMPT = """You are an AI news intelligence agent for senior software engineers and tech leads who build AI-powered tools. Process raw scraped content and return a JSON object with today's AI news brief.

Be ruthlessly concise and high-signal. Prioritize: model releases, new developer tools, API changes, deprecations, MCP/agent news.
Deprioritize: pure opinion, business-only news with no dev impact.
Skip anything older than 48 hours.
Return ONLY valid JSON, no markdown, no explanation."""


USER_PROMPT_TEMPLATE = """Process the following scraped AI news content and return a JSON object with this exact structure:

{{
  "date": "YYYY-MM-DD",
  "generated_at": "ISO timestamp",
  "headline": "One punchy sentence summarizing the biggest story today",
  "sections": [
    {{
      "id": "must_know",
      "title": "Must Know",
      "emoji": "🔥",
      "items": [
        {{
          "title": "Item title",
          "summary": "Comprehensive 4-5 sentence TLDR that covers: what happened, key details, technical specifics, and immediate impact. Be detailed but scannable.",
          "why_it_matters": "One sentence — why a tech lead building AI tools should care",
          "url": "source url",
          "source": "source name",
          "published": "YYYY-MM-DD or relative time like '2 hours ago'"
        }}
      ]
    }},
    {{
      "id": "new_tools",
      "title": "New Tools & Releases",
      "emoji": "📦",
      "items": [...]
    }},
    {{
      "id": "deprecations",
      "title": "Deprecations & Changes",
      "emoji": "📉",
      "items": [...]
    }},
    {{
      "id": "research",
      "title": "Research Worth Watching",
      "emoji": "🔬",
      "items": [...]
    }},
    {{
      "id": "community",
      "title": "Community Buzz",
      "emoji": "📌",
      "items": [...]
    }}
  ],
  "stats": {{
    "sources_checked": 8,
    "items_processed": 47,
    "items_categorized": 45
  }}
}}

Guidelines:
- Categorize ALL items into appropriate sections (no item limit per section)
- Remove duplicate items across sections (same URL = duplicate)
- Omit sections with nothing newsworthy
- Only "must_know" section items need "why_it_matters" field
- For summaries: Write 4-5 detailed sentences covering what, why, how, and impact
- Focus on developer-relevant technical details
- Be comprehensive but highly scannable
- Include "published" field for each item (extract from scraped data or use relative time like "2 hours ago", "yesterday")

Scraped content:
{content}

Return ONLY the JSON object, no other text."""


# Model configurations and pricing
PROVIDER_CONFIGS = {
    'anthropic': {
        'models': {
            'claude-sonnet-4-20241022': {
                'input_price_per_mtk': 3.00,   # $3 per million tokens
                'output_price_per_mtk': 15.00,  # $15 per million tokens
            },
            'claude-opus-4-20241022': {
                'input_price_per_mtk': 15.00,   # $15 per million tokens
                'output_price_per_mtk': 75.00,  # $75 per million tokens
            },
        },
        'default_model': 'claude-sonnet-4-20241022',
    },
    'openai': {
        'models': {
            'gpt-4o': {
                'input_price_per_mtk': 2.50,    # $2.50 per million tokens
                'output_price_per_mtk': 10.00,  # $10 per million tokens
            },
            'gpt-4o-mini': {
                'input_price_per_mtk': 0.15,    # $0.15 per million tokens
                'output_price_per_mtk': 0.60,   # $0.60 per million tokens
            },
            'gpt-4-turbo': {
                'input_price_per_mtk': 10.00,   # $10 per million tokens
                'output_price_per_mtk': 30.00,  # $30 per million tokens
            },
        },
        'default_model': 'gpt-4o',
    },
}


def call_anthropic(content_text: str, model: str) -> Tuple[str, int, int]:
    """
    Call Anthropic API.

    Returns:
        Tuple of (response_text, input_tokens, output_tokens)
    """
    from anthropic import Anthropic

    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable not set")

    client = Anthropic(api_key=api_key)
    user_prompt = USER_PROMPT_TEMPLATE.format(content=content_text)

    response = client.messages.create(
        model=model,
        max_tokens=4096,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": user_prompt
            }
        ]
    )

    response_text = response.content[0].text.strip()
    input_tokens = response.usage.input_tokens
    output_tokens = response.usage.output_tokens

    return response_text, input_tokens, output_tokens


def call_openai(content_text: str, model: str) -> Tuple[str, int, int]:
    """
    Call OpenAI API.

    Returns:
        Tuple of (response_text, input_tokens, output_tokens)
    """
    from openai import OpenAI

    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")

    client = OpenAI(api_key=api_key)
    user_prompt = USER_PROMPT_TEMPLATE.format(content=content_text)

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.7,
        max_tokens=4096,
    )

    response_text = response.choices[0].message.content.strip()
    input_tokens = response.usage.prompt_tokens
    output_tokens = response.usage.completion_tokens

    return response_text, input_tokens, output_tokens


def analyze_content(scraped_items: List[Dict[str, Any]], sources_checked: int) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """
    Analyze scraped content using configured AI provider.

    Args:
        scraped_items: List of scraped items from all sources
        sources_checked: Total number of sources that were checked

    Returns:
        Tuple of (brief, usage_stats)
        - brief: Structured JSON brief
        - usage_stats: Token usage and cost information
    """
    # Get provider from environment (default: anthropic)
    provider = os.getenv('AI_PROVIDER', 'anthropic').lower()

    if provider not in PROVIDER_CONFIGS:
        raise ValueError(f"Invalid AI_PROVIDER: {provider}. Must be 'anthropic' or 'openai'")

    # Get model from environment or use default
    provider_config = PROVIDER_CONFIGS[provider]
    model = os.getenv('AI_MODEL', provider_config['default_model'])

    if model not in provider_config['models']:
        raise ValueError(f"Invalid model {model} for provider {provider}")

    model_config = provider_config['models'][model]

    # Format scraped content
    content_text = json.dumps(scraped_items, indent=2)

    print(f"Using {provider.upper()} - Model: {model}")

    try:
        # Call appropriate API
        if provider == 'anthropic':
            response_text, input_tokens, output_tokens = call_anthropic(content_text, model)
        elif provider == 'openai':
            response_text, input_tokens, output_tokens = call_openai(content_text, model)
        else:
            raise ValueError(f"Unsupported provider: {provider}")

        # Parse JSON response
        try:
            brief = json.loads(response_text)
        except json.JSONDecodeError:
            # If wrapped in markdown, try to extract
            if "```json" in response_text:
                json_start = response_text.find("```json") + 7
                json_end = response_text.rfind("```")
                response_text = response_text[json_start:json_end].strip()
                brief = json.loads(response_text)
            else:
                raise

        # Ensure date and timestamp are set
        brief['date'] = datetime.now().strftime('%Y-%m-%d')
        brief['generated_at'] = datetime.now().isoformat()

        # Update stats
        if 'stats' not in brief:
            brief['stats'] = {}
        brief['stats']['sources_checked'] = sources_checked
        brief['stats']['items_processed'] = len(scraped_items)

        # Count categorized items
        categorized_count = sum(len(section.get('items', [])) for section in brief.get('sections', []))
        brief['stats']['items_categorized'] = categorized_count

        # Calculate costs
        total_tokens = input_tokens + output_tokens
        input_cost = (input_tokens / 1_000_000) * model_config['input_price_per_mtk']
        output_cost = (output_tokens / 1_000_000) * model_config['output_price_per_mtk']
        total_cost = input_cost + output_cost

        usage_stats = {
            'provider': provider,
            'model': model,
            'input_tokens': input_tokens,
            'output_tokens': output_tokens,
            'total_tokens': total_tokens,
            'input_cost': input_cost,
            'output_cost': output_cost,
            'total_cost': total_cost,
        }

        return brief, usage_stats

    except Exception as e:
        raise Exception(f"Error calling {provider.upper()} API: {e}")
