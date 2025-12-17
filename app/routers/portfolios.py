from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import schemas, models
from app.database import get_db
from app.services import market_service  # <--- Importamos o serviço

router = APIRouter(prefix="/portfolios", tags=["Portfolios"])


@router.post("/", response_model=schemas.PortfolioResponse, status_code=status.HTTP_201_CREATED)
def create_portfolio(portfolio: schemas.PortfolioCreate, db: Session = Depends(get_db)):
    new_portfolio = models.Portfolio(name=portfolio.name)
    db.add(new_portfolio)
    db.commit()
    db.refresh(new_portfolio)
    return new_portfolio


@router.get("/", response_model=List[schemas.PortfolioResponse])
def list_portfolios(db: Session = Depends(get_db)):
    return db.query(models.Portfolio).all()


@router.get("/{id}", response_model=schemas.PortfolioResponse)
def get_portfolio(id: int, db: Session = Depends(get_db)):
    portfolio = db.query(models.Portfolio).filter(models.Portfolio.id == id).first()

    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio não encontrado")

    # --- LÓGICA DE NEGÓCIO REAL ---
    total_value = 0.0
    asset_details = []  # Lista auxiliar para calcular concentração

    # Itera sobre os ativos do banco e busca preço atualizado
    for asset in portfolio.assets:
        # Chama nosso serviço (com Cache)
        price = market_service.get_current_price(asset.ticker)

        # Calcula valor total deste ativo
        position_value = price * asset.quantity

        # Preenche os campos virtuais do Schema (não salva no banco, só na resposta)
        asset.current_price = price
        asset.total_value = position_value

        total_value += position_value
        asset_details.append({"ticker": asset.ticker, "value": position_value})

    portfolio.total_value = total_value

    # --- GERADOR DE INSIGHT AUTOMÁTICO ---
    if total_value > 0:
        # Encontra o ativo com maior valor na carteira
        top_asset = max(asset_details, key=lambda x: x["value"])
        concentration = (top_asset["value"] / total_value) * 100

        if concentration > 50:
            portfolio.insight = f"⚠️ Alerta: {concentration:.1f}% do seu capital está concentrado em {top_asset['ticker']}."
        else:
            portfolio.insight = "✅ Parabéns! Sua carteira está bem diversificada."
    else:
        portfolio.insight = "Sua carteira está vazia. Adicione ativos."

    return portfolio