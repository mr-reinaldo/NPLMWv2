from fastapi import FastAPI
from uvicorn import run
from contextlib import asynccontextmanager

from app.core.database import close_db_connection
from app.core.settings import settings

from app.routers.user import router as user_router
from app.routers.device import router as device_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gerenciador de contexto para finalizar a conexão com o banco de dados
    quando a aplicação é encerrada.

    Args:
        app (FastAPI): Instância da aplicação FastAPI.

    """

    try:
        yield
    finally:
        await close_db_connection()


app = FastAPI(lifespan=lifespan)


app.include_router(user_router, prefix=settings.api.api_prefix)
app.include_router(device_router, prefix=settings.api.api_prefix)


@app.get("/")
def read_root():
    return {
        "message": "Bem-vindo ao projeto de exemplo FastAPI com SQLAlchemy e PostgreSQL"
    }


if __name__ == "__main__":
    run(
        "main:app",
        host=str(settings.api.server_host),
        port=settings.api.server_port,
        reload=True,
    )
