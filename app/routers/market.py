from fastapi import APIRouter, HTTPException
from app.services import market_service

router = APIRouter(
    prefix="/market",
    tags=["Market Data"]
)

@router.get("/{ticker}")

def get_market_price(ticker: str):
    price = market_service.get_current_price(ticker)

    return {
        "ticker": ticker.upper(),
        "price": price,
        "currency": "USD",
        "source": "Alpha Vantage (via Backend Cache)"
    }