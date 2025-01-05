import os

REDDIT_CONFIG = {
    "userAgent": "UnoMas_UnoMenos/1.0",
    "clientId": os.getenv("REDDIT_CLIENT_ID", "heb2VXcSiegulvbOO-Y5-w"),
    "clientSecret": os.getenv("REDDIT_CLIENT_SECRET", "_uzEu15A-Zr1bbFbS-EorDhrOE24vA"),
    "username": os.getenv("REDDIT_USERNAME", "UnoMas_UnoMenos"),
    "password": os.getenv("REDDIT_PASSWORD", "HelloWorld0809!"),
}
