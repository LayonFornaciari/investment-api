from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app import models, schemas
from app.services import market_service, advisor

router = APIRouter(
    prefix="/portfolios",
    tags=["Portfolios"]
)

@router.get("/", response_model=List[schemas.PortfolioResponse])
def get_all_portfolios(db: Session = Depends(get_db)):
    portfolios = db.query(models.Portfolio).all()
    return portfolios


@router.post("/", response_model=schemas.PortfolioResponse, status_code=status.HTTP_201_CREATED)
def create_portfolio(portfolio: schemas.PortfolioCreate, db: Session = Depends(get_db)):
    new_portfolio = models.Portfolio(name=portfolio.name)
    db.add(new_portfolio)
    db.commit()
    db.refresh(new_portfolio)
    return new_portfolio


@router.get("/{id}", response_model=schemas.PortfolioResponse)
def get_portfolio_details(id: int, db: Session = Depends(get_db)):
    # 1. Busca a carteira no banco
    portfolio = db.query(models.Portfolio).filter(models.Portfolio.id == id).first()

    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio não encontrado")

    # 2. Lógica de Atualização em Tempo Real
    total_portfolio_value = 0.0
    asset_list_for_advisor = []

    for asset in portfolio.assets:
        try:
            # Pega preço atualizado (Yahoo)
            current_price = market_service.get_current_price(asset.ticker)

            # Calcula valor total deste ativo
            asset_total = current_price * asset.quantity

            # Injeta esses valores no objeto asset
            asset.current_price = current_price
            asset.total_value = asset_total

            # Soma no total da carteira
            total_portfolio_value += asset_total

            # Guarda dados para o Advisor analisar
            asset_list_for_advisor.append({
                "ticker": asset.ticker,
                "total_value": asset_total
            })

        except Exception as e:
            print(f"Erro ao atualizar {asset.ticker}: {e}")
            asset.current_price = 0.0
            asset.total_value = 0.0

    # 3. Injeta o valor total calculado na resposta
    portfolio.total_value = total_portfolio_value

    insight_text = advisor.analyze_portfolio(asset_list_for_advisor, total_portfolio_value)
    portfolio.insight = insight_text

    return portfolio

@router.put("/{id}", response_model=schemas.PortfolioResponse)
def update_portfolio(id: int, portfolio_update: schemas.PortfolioUpdate, db: Session = Depends(get_db)):
    portfolio = db.query(models.Portfolio).filter(models.Portfolio.id == id).first()

    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio não encontrado")

    portfolio.name = portfolio_update.name
    db.commit()
    db.refresh(portfolio)
    return portfolio

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_portfolio(id: int, db: Session = Depends(get_db)):
    portfolio = db.query(models.Portfolio).filter(models.Portfolio.id == id).first()

    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio não encontrado")

    db.delete(portfolio)
    db.commit()
    return None