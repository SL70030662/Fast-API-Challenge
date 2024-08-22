# app/main.py

from fastapi import FastAPI
from app.database import engine, Base
from app.routers import webhook, data, sync, tasks

app = FastAPI()

# Initialize the database
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(webhook.router)
app.include_router(data.router)
app.include_router(sync.router)
app.include_router(tasks.router)


@app.get("/")
def read_root():
    return {"message": "FastAPI Data Warehouse"}
