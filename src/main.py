from fastapi import FastAPI

from auth.router import router as auth_router
from records.router import router as record_router

from database import DATABASE_URL

app = FastAPI(
    title="Social Network",
    prefix='/api'
)

app.include_router(auth_router)
app.include_router(record_router)

@app.get("/")
async def gel_main():
    return {'message': 'Hello World'}
