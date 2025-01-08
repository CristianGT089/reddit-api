import os
import praw

REDDIT_CONFIG = {
    "client_id": os.getenv("REDDIT_CLIENT_ID", "heb2VXcSiegulvbOO-Y5-w"),
    "client_secret": os.getenv("REDDIT_CLIENT_SECRET", "_uzEu15A-Zr1bbFbS-EorDhrOE24vA"),
    "user_agent": os.getenv("REDDIT_USER_AGENT", "Cristian-Analisis/1.0"),
    "username": os.getenv("REDDIT_USERNAME", "UnoMas_UnoMenos"),
    "password": os.getenv("REDDIT_PASSWORD", "HelloWorld0809!"),
}

# Configuración de la API de Reddit
def get_reddit_client() -> praw.Reddit:
    return praw.Reddit(
        client_id="heb2VXcSiegulvbOO-Y5-w",
        client_secret="_uzEu15A-Zr1bbFbS-EorDhrOE24vA",
        user_agent="Cristian-Analisis/1.0",
    )