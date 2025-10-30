import settings
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger


from utils.lifespan import lifespan
from index_router import index_router


app = FastAPI(
    lifespan=lifespan
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(index_router, prefix="/api")


@app.get("/")
def root():
    return {"message": "Hello World"}


if __name__ == "__main__":

    logger.info(f"Starting application with FASTAPI_ENVIRONMENT={settings.FASTAPI_ENVIRONMENT}")

    if settings.FASTAPI_ENVIRONMENT == "DEVELOPMENT":
        uvicorn.run("main:app", host=settings.SERVER_IP, port=settings.SERVER_PORT, reload=True)
    else:
        uvicorn.run("main:app", host=settings.SERVER_IP, port=settings.SERVER_PORT)

# TODO: [HTTPS] openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout key.pem -out cert.pem
# ssl_keyfile="./ssl/key.pem",
# ssl_certfile="./ssl/cert.pem",
