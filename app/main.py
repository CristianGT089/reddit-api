from fastapi import FastAPI, Query
from app.models import SentimentResponse
from app.services import analyze_posts, search_posts
from app.settings import get_reddit_client

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API de análisis de Reddit"}

# Endpoint para el análisis de sentimiento
@app.get("/analyze", response_model=SentimentResponse)
async def analyze_sentiment_endpoint(
    query: str = Query(..., description="Palabra clave para buscar en Reddit"),
    subreddit: str = Query("all", description="Subreddit donde buscar, por defecto 'all'"),
    limit: int = Query(10, description="Cantidad máxima de posts a analizar"),
):
    reddit = get_reddit_client()
    posts = search_posts(reddit, query, subreddit, limit)
    sentiment_summary = analyze_posts(posts)
    
    return SentimentResponse(
        query=query,
        total_posts=len(posts),
        sentiment_summary=sentiment_summary,
    )