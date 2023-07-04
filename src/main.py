from fastapi import FastAPI
from redis import asyncio as aioredis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from config import REDIS_HOST, REDIS_PORT
from auth.router import router as auth_router
from records.router import router as record_router


app = FastAPI(
    title="Social Network",
    prefix='/api'
)

app.include_router(auth_router)
app.include_router(record_router)

@app.get("/")
async def gel_main():
    return {'message': 'Hello World'}
