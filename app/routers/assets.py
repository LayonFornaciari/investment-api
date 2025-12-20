from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import schemas, models
from app.database import get_db

router = APIRouter(tags=["Assets"])


# 1. COMPRAR ATIVO
@router.post(
    "/portfolios/{portfolio_id}/assets",
    response_model=schemas.AssetResponse,
    status_code=status.HTTP_201_CREATED
)
def buy_asset(
    portfolio_id: int,
    asset: schemas.AssetCreate,
    db: Session = Depends(get_db)
):
    # 1. Verifica se a carteira existe
    portfolio = db.query(models.Portfolio).filter(
        models.Portfolio.id == portfolio_id
    ).first()

    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio não encontrado")

    ticker = asset.ticker.upper()

    # 2. Verifica se o ativo já existe na carteira
    existing_asset = db.query(models.Asset).filter(
        models.Asset.portfolio_id == portfolio_id,
        models.Asset.ticker == ticker
    ).first()

    # 3. Se existir → CONSOLIDA POSIÇÃO
    if existing_asset:
        existing_asset.quantity += asset.quantity
        db.commit()
        db.refresh(existing_asset)
        return existing_asset

    # 4. Se não existir → CRIA NOVO
    new_asset = models.Asset(
        ticker=ticker,
        quantity=asset.quantity,
        portfolio_id=portfolio_id
    )

    db.add(new_asset)
    db.commit()
    db.refresh(new_asset)

    return new_asset

@router.post("/assets/{id}/sell")
def sell_asset(id: int, sell_data: schemas.AssetSell, db: Session = Depends(get_db)):
    # 1. Busca o ativo
    asset = db.query(models.Asset).filter(models.Asset.id == id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Ativo não encontrado")

    # 2. Verifica se tem saldo suficiente
    if sell_data.quantity > asset.quantity:
        raise HTTPException(status_code=400, detail="Quantidade insuficiente para venda")

    # 3. Subtrai a quantidade
    asset.quantity -= sell_data.quantity

    # 4. Se zerou, deleta o registro. Se sobrou, atualiza.
    if asset.quantity <= 0:
        db.delete(asset)
        db.commit()
        return {"message": "Ativo vendido completamente e removido"}
    else:
        db.commit()
        db.refresh(asset)
        return asset