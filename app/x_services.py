from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service
from textblob import TextBlob
from webdriver_manager.firefox import GeckoDriverManager  # Usamos GeckoDriverManager para Firefox
from bs4 import BeautifulSoup
import time
import json

# Configuración de Selenium con Chrome
options = webdriver.FirefoxOptions()
options.add_argument("--headless")  # Para que no se abra la ventana del navegador
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Inicializamos el navegador
driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)

def get_tweets(query, max_tweets=100):
    url = f"https://x.com/search?q={query}&src=typed_query&f=top"
    driver.get(url)

    # Esperar que la página cargue
    time.sleep(5)

    # Hacer scroll para cargar más tweets
    body = driver.find_element("tag name", "body")
    for _ in range(5):  # Scroll para cargar más tweets
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(2)

    # Analizar la página con BeautifulSoup
    soup = BeautifulSoup(driver.page_source, "html.parser")
    
    tweets = []
    for tweet in soup.find_all("div", {"data-testid": "tweet"}):
        try:
            tweet_text = tweet.find("div", {"lang": "es"}).get_text()
            tweets.append(tweet_text)
            if len(tweets) >= max_tweets:
                break
        except AttributeError:
            continue

    return tweets

# Método para analizar el sentimiento
def analyze_sentiment(text: str) -> str:
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity
    if polarity > 0:
        return "positive"
    elif polarity < 0:
        return "negative"
    else:
        return "neutral"

# Guardar los resultados en un archivo de texto
def save_results_to_file(query, tweets, sentiment_summary):
    filename = f"twitter_{query.replace(' ', '_').lower()}.txt"
    with open(filename, "w", encoding="utf-8") as file:
        file.write(f"Query: {query}\n\n")
        for idx, tweet in enumerate(tweets, start=1):
            file.write(f"Tweet #{idx}: {tweet}\n")
        file.write(f"\nSentiment Summary: {json.dumps(sentiment_summary)}")
    driver.quit()

