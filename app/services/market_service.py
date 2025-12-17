import requests
import os
from datetime import datetime, timedelta

# Cache em memória: { "AAPL": {"price": 150.0, "time": ...} }
# Isso evita chamar a API externa toda hora
MARKET_CACHE = {}
CACHE_DURATION_MINUTES = 30

# Chave da API (Busca do ambiente ou usa 'demo')
# Dica: Para o vídeo, se não tiver chave, o 'demo' funciona para tickers como IBM
API_KEY = os.getenv("MARKET_API_KEY", "demo")
BASE_URL = "https://www.alphavantage.co/query"


def get_current_price(ticker: str) -> float:
    ticker = ticker.upper()
    now = datetime.now()

    # 1. Verifica se já temos no Cache recente
    if ticker in MARKET_CACHE:
        cached_data = MARKET_CACHE[ticker]
        age = now - cached_data["time"]

        if age < timedelta(minutes=CACHE_DURATION_MINUTES):
            print(f"💰 Cache Hit: Usando preço salvo para {ticker}")
            return cached_data["price"]

    # 2. Se não tem no cache, chama a API Externa
    print(f"🌍 API Call: Buscando preço real para {ticker} na Alpha Vantage...")

    try:
        params = {
            "function": "GLOBAL_QUOTE",
            "symbol": ticker,
            "apikey": API_KEY
        }

        response = requests.get(BASE_URL, params=params, timeout=10)
        data = response.json()

        # O json da Alpha Vantage vem assim: { "Global Quote": { "05. price": "150.00" } }
        price_str = data.get("Global Quote", {}).get("05. price")

        if price_str:
            price = float(price_str)
            # Salva no cache
            MARKET_CACHE[ticker] = {"price": price, "time": now}
            return price
        else:
            print(f"⚠️ Aviso: API não retornou preço para {ticker}. Dados: {data}")
            return 100.0  # Valor dummy para não quebrar a demo se a API falhar

    except Exception as e:
        print(f"❌ Erro ao conectar na API externa: {e}")
        return 100.0  # Fallback de segurança