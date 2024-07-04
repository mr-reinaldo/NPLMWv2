from fastapi import FastAPI
from uvicorn import run
from contextlib import asynccontextmanager

from app.core.database import close_db_connection
from app.core.settings import settings


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


@app.get("/")
def read_root():
    return {"Hello": "World"}


if __name__ == "__main__":
    run(
        "main:app",
        host=str(settings.api.server_host),
        port=settings.api.server_port,
        reload=True,
    )
