from fastapi import FastAPI
from uvicorn import run
from app.core.settings import settings


app = FastAPI()


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
