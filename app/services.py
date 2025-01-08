import praw
from typing import List, Dict
from textblob import TextBlob


# Método para buscar posts relacionados con una temática
def search_posts(reddit: praw.Reddit, query: str, subreddit: str = "all", limit: int = 10) -> List[Dict]:
    results = []
    for submission in reddit.subreddit(subreddit).search(query, limit=limit):
        results.append({
            "title": submission.title,
            "url": submission.url,
            "comments": fetch_comments(submission),
        })
    return results

# Método para extraer comentarios de un post
def fetch_comments(submission: praw.models.Submission) -> List[str]:
    submission.comments.replace_more(limit=0)  # Expandir todos los comentarios
    return [comment.body for comment in submission.comments.list()]

# Análisis de sentimiento (positivo, negativo o neutral)
def analyze_sentiment(text: str) -> str:
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity
    if polarity > 0:
        return "positive"
    elif polarity < 0:
        return "negative"
    else:
        return "neutral"

# Procesar todos los posts y sus comentarios
def analyze_posts(posts: List[Dict]) -> Dict[str, int]:
    sentiment_counts = {"positive": 0, "negative": 0, "neutral": 0}
    for post in posts:
        # Analizar sentimiento del título
        post_sentiment = analyze_sentiment(post["title"])
        sentiment_counts[post_sentiment] += 1

        # Analizar sentimientos de los comentarios
        for comment in post["comments"]:
            comment_sentiment = analyze_sentiment(comment)
            sentiment_counts[comment_sentiment] += 1
    return sentiment_counts
