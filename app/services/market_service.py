import yfinance as yf
from datetime import datetime, timedelta

# Cache simples em memória
MARKET_CACHE = {}
CACHE_DURATION_MINUTES = 30


def get_current_price(ticker: str) -> float:
    ticker = ticker.upper()
    now = datetime.now()

    # 1. Verifica Cache
    if ticker in MARKET_CACHE:
        cached_data = MARKET_CACHE[ticker]
        age = now - cached_data["time"]
        if age < timedelta(minutes=CACHE_DURATION_MINUTES):
            print(f"💰 Cache Hit: {ticker}")
            return cached_data["price"]

    print(f"🌍 API Call: Buscando {ticker} no Yahoo Finance...")

    try:
        # 2. Usa a biblioteca yfinance (Yahoo Finance)
        # Ela substitui a chamada manual com requests/AlphaVantage
        stock = yf.Ticker(ticker)

        # Pega o histórico do dia
        history = stock.history(period="1d")

        # 3. AQUI ESTÁ A CORREÇÃO DO BUG:
        # Se o histórico vier vazio, significa que o ticker NÃO EXISTE.
        if history.empty:
            # Em vez de retornar 100.0, lançamos um erro real!
            raise ValueError(f"Ticker '{ticker}' não encontrado.")

        # Pega o último preço de fechamento
        price = float(history['Close'].iloc[-1])

        # Salva no cache
        MARKET_CACHE[ticker] = {"price": price, "time": now}

        return price

    except Exception as e:
        # Se for o nosso erro de "não encontrado", deixa subir para o router pegar
        if "não encontrado" in str(e):
            raise e

        # Se for erro de conexão/internet, avisa (sem retornar 100!)
        print(f"❌ Erro na API: {e}")
        raise ValueError("Erro ao consultar serviço de preços.")