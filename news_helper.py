import requests
import os


def get_top_news(category="general", country="", num_articles=10):
    api_key = os.getenv("NEWS_API_KEY")

    if country:
        url = "https://newsapi.org/v2/top-headlines"
        params = {
            "apiKey": api_key,
            "category": category,
            "country": country,
            "pageSize": num_articles
        }
    else:
        url = "https://newsapi.org/v2/top-headlines"
        params = {
            "apiKey": api_key,
            "language": "en",
            "pageSize": num_articles
        }

    response = requests.get(url, params=params)
    data = response.json()

    articles = []
    for article in data.get("articles", []):
        title = article.get("title", "")
        description = article.get("description", "")
        source = article.get("source", {}).get("name", "")

        if title and description:
            articles.append({
                "title": title,
                "description": description,
                "source": source
            })

    return articles
