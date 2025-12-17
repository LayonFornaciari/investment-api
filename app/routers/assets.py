from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import schemas, models
from app.database import get_db

# Tag Assets para agrupar no Swagger
router = APIRouter(tags=["Assets"])


# 1. ADICIONAR ATIVO NA CARTEIRA (POST)
@router.post("/portfolios/{portfolio_id}/assets", response_model=schemas.AssetResponse,
             status_code=status.HTTP_201_CREATED)
def add_asset(portfolio_id: int, asset: schemas.AssetCreate, db: Session = Depends(get_db)):
    # Verifica se a carteira existe
    portfolio = db.query(models.Portfolio).filter(models.Portfolio.id == portfolio_id).first()

    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio não encontrado")

    # Cria o ativo vinculado à carteira
    # .upper() garante que o ticker fique sempre maiúsculo (ex: aapl -> AAPL)
    new_asset = models.Asset(
        ticker=asset.ticker.upper(),
        quantity=asset.quantity,
        portfolio_id=portfolio_id
    )

    db.add(new_asset)
    db.commit()
    db.refresh(new_asset)

    return new_asset


# 2. EDITAR QUANTIDADE (PUT) - ⚠️ ROTA OBRIGATÓRIA PARA A BANCA
@router.put("/assets/{id}", response_model=schemas.AssetResponse)
def update_asset(id: int, asset_update: schemas.AssetBase, db: Session = Depends(get_db)):
    # Busca o ativo pelo ID
    asset = db.query(models.Asset).filter(models.Asset.id == id).first()

    if not asset:
        raise HTTPException(status_code=404, detail="Ativo não encontrado")

    # Atualiza a quantidade
    asset.quantity = asset_update.quantity

    db.commit()
    db.refresh(asset)

    return asset


# 3. REMOVER ATIVO (DELETE)
@router.delete("/assets/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_asset(id: int, db: Session = Depends(get_db)):
    asset = db.query(models.Asset).filter(models.Asset.id == id).first()

    if not asset:
        raise HTTPException(status_code=404, detail="Ativo não encontrado")

    db.delete(asset)
    db.commit()
    return None