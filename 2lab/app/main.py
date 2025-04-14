from fastapi import FastAPI

app = FastAPI()

from app.api.auth import router as auth_router
from app.api.crypto import router as crypto_router
from app.api.async_crypto import router as async_crypto_router

app.include_router(auth_router, prefix="/api")
app.include_router(crypto_router, prefix="/api")
app.include_router(async_crypto_router, prefix="/api")
