from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from app.core.config import settings
from app.routers.membership import router as membership_router
from app.routers.payment import router as payment_router

from app.routers.plan import router as plan_router
from app.routers.member import router as member_router

from app.routers.plan import router as plan_router
from app.routers.member import router as member_router

logging.basicConfig(
    level=logging.DEBUG if settings.DEBUG else logging.INFO,
    format="[%(asctime)s] %(levelname)s %(name)s — %(message)s",
)
logger = logging.getLogger("gymapi")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"🏋️  {settings.APP_NAME} arrancando...")
    yield
    logger.info("👋 GymAPI cerrando.")


app = FastAPI(
    title=settings.APP_NAME,
    description="API REST para gestión integral de gimnasio. Madrid 2026.",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    lifespan=lifespan,
)

# CONECTAMOS EL ROUTER DE LOS PLANES Y DE LOS MIEMBROS
app.include_router(plan_router)
app.include_router(member_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(membership_router, prefix="/api/v1")
app.include_router(payment_router, prefix="/api/v1")


@app.get("/", tags=["health"])
def health():
    return {"status": "ok", "app": settings.APP_NAME, "version": "1.0.0"}
