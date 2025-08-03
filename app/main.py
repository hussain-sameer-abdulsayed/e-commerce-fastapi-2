from fastapi import FastAPI
from app.db.database import engine
from sqlmodel import SQLModel
import uvicorn

app = FastAPI()

@app.get("/")  # <-- make sure to use @ here!
async def root():
    return {"message": "Hello world"}  # <-- proper key-value JSON





@app.on_event("startup")
async def on_startup():
   async with engine.begin() as conn:
      await conn.run_sync(SQLModel.metadata.create_all) 