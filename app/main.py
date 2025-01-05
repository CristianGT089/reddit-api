from fastapi import FastAPI
from app.services import fetch_reddit_posts, analyze_sentiment

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API de análisis de opiniones en Reddit"}

@app.get("/analyze/")
async def analyze_reddit(subreddit: str, limit: int = 10):
    try:
        # Obtener publicaciones desde Reddit
        posts_json = await fetch_reddit_posts(subreddit, limit)
        
        # Parsear las publicaciones
        posts = eval(posts_json)  # Convertir JSON en lista

        # Analizar sentimiento
        sentiment = analyze_sentiment(posts)
        
        return {
            "subreddit": subreddit,
            "limit": limit,
            "sentiment": sentiment,
        }
    except Exception as e:
        return {"error": str(e)}
