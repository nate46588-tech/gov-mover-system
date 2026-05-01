import requests
from config import NEWS_API_KEY

def get_news_api(company_name):
    try:
        url = "https://newsapi.org/v2/everything"

        params = {
            "q": company_name,
            "sortBy": "publishedAt",
            "pageSize": 3,
            "apiKey": NEWS_API_KEY
        }

        r = requests.get(url, params=params)
        data = r.json()

        articles = data.get("articles", [])

        if not articles:
            return None

        return articles[0]["title"]

    except:
        return None
