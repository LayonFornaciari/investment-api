from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from pydantic import BaseModel, Field


# --- ASSETS (Precisamos definir antes para usar no Portfolio) ---
class AssetBase(BaseModel):
    ticker: str
    quantity: int = Field(..., gt=0)

class AssetCreate(AssetBase):
    pass

class AssetSell(BaseModel):
    quantity: float

class AssetResponse(AssetBase):
    id: int
    portfolio_id: int
    # Campos que calcularemos dinamicamente depois
    current_price: Optional[float] = 0.0
    total_value: Optional[float] = 0.0

    class Config:
        from_attributes = True


# --- PORTFOLIOS ---
class PortfolioBase(BaseModel):
    name: str


class PortfolioCreate(PortfolioBase):
    pass


class PortfolioResponse(PortfolioBase):
    id: int
    created_at: datetime

    # Lista de ativos (relacionamento)
    assets: List[AssetResponse] = []

    # Campos calculados (Regra de Negócio)
    total_value: Optional[float] = 0.0
    insight: Optional[str] = None

    class Config:
        from_attributes = True