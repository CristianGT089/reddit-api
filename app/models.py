# Modelo para la respuesta
from typing import Dict
from pydantic import BaseModel


class SentimentResponse(BaseModel):
    query: str
    total_posts: int
    sentiment_summary: Dict[str, int]