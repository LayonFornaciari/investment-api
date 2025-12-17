from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import Base, engine
from app.models import Portfolio, Asset  # noqa: F401


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown (não precisamos fazer nada aqui por enquanto)


app = FastAPI(
    title="Investment Portfolio API",
    lifespan=lifespan
)


@app.get("/")
def health_check():
    return {"status": "API running"}