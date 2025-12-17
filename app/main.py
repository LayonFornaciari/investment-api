from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import Base, engine
from app.models import Portfolio, Asset  # noqa: F401
from app.routers import portfolios, assets, market
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(
    title="Investment Portfolio API",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(portfolios.router)
app.include_router(assets.router)
app.include_router(market.router)

@app.get("/")
def health_check():
    return {"status": "API running"}