from fastapi import APIRouter, HTTPException
from app.services import market_service

router = APIRouter(tags=["Market Data"])


@router.get("/market/{ticker}")
def get_market_price(ticker: str):
    """
    Retorna o preço atual.
    Usa cache interno para economizar chamadas à API externa.
    """
    price = market_service.get_current_price(ticker)

    return {
        "ticker": ticker.upper(),
        "price": price,
        "currency": "USD",
        "source": "Alpha Vantage (via Backend Cache)"
    }