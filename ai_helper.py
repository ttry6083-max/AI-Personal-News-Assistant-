import anthropic
import os
import json

CATEGORIES = ["general", "technology", "sports", "business", "health", "science", "entertainment"]


def decide_action(conversation_history):
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    system_prompt = """You are a friendly personal news assistant. You have a casual, warm personality.

Based on the conversation, decide what action to take and respond naturally.

You MUST reply with ONLY a raw JSON object. No markdown. No code blocks. No backticks. No explanation. Just the JSON itself.

Use one of these formats:

If the user wants to read news:
{"type": "fetch_news", "category": "technology", "country": "us", "response": "Sure! Let me grab the latest tech news from the US..."}

For global news or when no country is mentioned:
{"type": "fetch_news", "category": "general", "country": "", "response": "Here are today's global headlines..."}

If the user wants to email the last digest:
{"type": "send_email", "response": "Done! Just sent it to your inbox."}

For greetings, questions, or anything else:
{"type": "chat", "response": "your natural friendly response here"}

Rules:
- Valid categories: general, technology, sports, business, health, science, entertainment
- Always pick the closest matching category
- For country: use the 2-letter code (us, gb, in, au, sg, ca, de, fr, jp, cn, ae, np, pk, ng)
- If no country is mentioned, set country to empty string "" for global news"""

    message = client.messages.create(
        model="claude-opus-4-8",
        max_tokens=200,
        system=system_prompt,
        messages=conversation_history
    )

    try:
        text = message.content[0].text.strip()
        start = text.find("{")
        end = text.rfind("}") + 1
        if start != -1 and end != 0:
            text = text[start:end]
        return json.loads(text)
    except Exception:
        return {"type": "chat", "response": message.content[0].text}


def summarize_news(articles):
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    articles_text = ""
    for i, article in enumerate(articles, 1):
        articles_text += f"{i}. {article['title']}\n"
        articles_text += f"   {article['description']}\n"
        articles_text += f"   Source: {article['source']}\n\n"

    prompt = f"""You are a friendly morning news assistant.

Here are today's top news articles:

{articles_text}

Write a clean, friendly news digest with:
- A warm intro line
- 5 to 7 key stories, each summarized in 2 to 3 sentences
- Simple language anyone can understand
- A short closing line

Keep it conversational and easy to read."""

    message = client.messages.create(
        model="claude-opus-4-8",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )

    return message.content[0].text
