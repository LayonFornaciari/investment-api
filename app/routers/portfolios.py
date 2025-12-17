from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import schemas, models
from app.database import get_db

router = APIRouter(
    prefix="/portfolios",
    tags=["Portfolios"]
)


# 1. CRIAR PORTFOLIO (POST)
@router.post("/", response_model=schemas.PortfolioResponse, status_code=status.HTTP_201_CREATED)
def create_portfolio(portfolio: schemas.PortfolioCreate, db: Session = Depends(get_db)):
    # Cria a instância do Model
    new_portfolio = models.Portfolio(name=portfolio.name)

    # Salva no banco
    db.add(new_portfolio)
    db.commit()
    db.refresh(new_portfolio)

    return new_portfolio


# 2. LISTAR TODOS (GET)
@router.get("/", response_model=List[schemas.PortfolioResponse])
def list_portfolios(db: Session = Depends(get_db)):
    # Busca todos no banco
    portfolios = db.query(models.Portfolio).all()
    return portfolios


# 3. BUSCAR UM (GET /{id}) - CRÍTICO PARA O FRONTEND
@router.get("/{id}", response_model=schemas.PortfolioResponse)
def get_portfolio(id: int, db: Session = Depends(get_db)):
    # Busca pelo ID
    portfolio = db.query(models.Portfolio).filter(models.Portfolio.id == id).first()

    if not portfolio:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Portfolio com id {id} não encontrado"
        )

    # Lógica de Negócio (Placeholder por enquanto)
    # Na próxima fase, aqui calcularemos o 'total_value' e 'insight' real.
    portfolio.total_value = 0.0
    portfolio.insight = "Adicione ativos para ver a análise."

    return portfolio