import asyncio
from fastapi import HTTPException
import subprocess

# Lista de palabras
positive_words = ['bueno', 'excelente', 'útil', 'positivo', 'amable', 'eficiente']
negative_words = ['malo', 'inútil', 'problemático', 'negativo', 'difícil', 'ineficiente']

# Función para interactuar con Node.js y snoowrap
async def fetch_reddit_posts(subreddit: str, limit: int = 10):
    try:
        # Comando para ejecutar el script Node.js
        process = await asyncio.create_subprocess_exec(
            "node", "fetch_reddit.js", subreddit, str(limit),
            stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await process.communicate()

        if stderr:
            raise HTTPException(status_code=500, detail=f"Error en Node.js: {stderr.decode()}")

        # Parsear la salida de Node.js (se espera un JSON)
        return stdout.decode()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Función para analizar el sentimiento
def analyze_sentiment(posts: list):
    positive_count = 0
    negative_count = 0

    for post in posts:
        words = post.lower().split()
        positive_count += sum(1 for word in words if word in positive_words)
        negative_count += sum(1 for word in words if word in negative_words)

    return {
        "positive": positive_count,
        "negative": negative_count,
    }
