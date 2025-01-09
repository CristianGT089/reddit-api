from fastapi import FastAPI, Query
from app.models import SentimentResponse
from app.reddit_services import analyze_posts, save_results_to_file, search_posts
from app.settings import get_reddit_client
from app.x_services import analyze_sentiment, get_tweets

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API de análisis de Reddit"}

# Endpoint para el análisis de sentimiento
@app.get("/reddit_analyze", response_model=SentimentResponse)
async def analyze_reddit_sentiment_endpoint(
    query: str = Query(..., description="Palabra clave para buscar en Reddit"),
    subreddit: str = Query("all", description="Subreddit donde buscar, por defecto 'all'"),
    limit: int = Query(10, description="Cantidad máxima de posts a analizar"),
):
    reddit = get_reddit_client()
    posts = search_posts(reddit, query, subreddit, limit)
    sentiment_summary = analyze_posts(posts)
    sentiment_response = SentimentResponse(
        query=query,
        total_posts=len(posts),
        sentiment_summary=sentiment_summary,
    )

    save_results_to_file(query, posts, sentiment_response)
    
    return sentiment_response 

# Endpoint para el análisis de sentimiento de tweets
@app.get("/twitter_analyze", response_model=SentimentResponse)
async def analyze_twitter_sentiment_endpoint(
    query: str = Query(..., description="Palabra clave para buscar en Twitter"),
    limit: int = Query(10, description="Cantidad máxima de tweets a analizar"),
):
    # Buscar tweets
    tweets = get_tweets(query, limit)

    # Realizar análisis de sentimiento
    sentiment_summary = {"positive": 0, "negative": 0, "neutral": 0}
    for tweet in tweets:
        sentiment = analyze_sentiment(tweet)
        sentiment_summary[sentiment] += 1

    # Guardar resultados en un archivo
    save_results_to_file(query, tweets)

    # Retornar respuesta
    return SentimentResponse(
        query=query,
        total_posts=len(tweets),
        sentiment_summary=sentiment_summary,
    )