from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.routes import api as api_router
from app.routes import web as web_router
from .config import get_settings
from app.infra.persistence.json_store_repository import JsonStoreRepository

settings = get_settings()
app = FastAPI(title=settings.app_name)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await JsonStoreRepository().enrich_if_needed()
    yield

app = FastAPI(
    title="Your App",
    lifespan=lifespan,
)

app.include_router(api_router.router, prefix="/api")
app.include_router(web_router.router)

