from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import Base, engine
from app.models import Portfolio, Asset  # noqa: F401
from app.routers import portfolios, assets


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(
    title="Investment Portfolio API",
    lifespan=lifespan
)

app.include_router(portfolios.router)
app.include_router(assets.router)

@app.get("/")
def health_check():
    return {"status": "API running"}