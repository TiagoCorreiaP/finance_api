from fastapi import FastAPI, Depends
from . auth import get_current_user
from contextlib import asynccontextmanager
from .database import engine, Base
from .routes import users, auth, transactions
from fastapi.staticfiles import StaticFiles
import os

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(title="Finance API Async", lifespan=lifespan)

@app.get("/teste_logado")
async def teste_logado(user = Depends(get_current_user)):
    return {"message": f"Olá, {user.full_name}! Você está logado."}

@app.get("/")
async def read_root():
    return{"status": "API Async rodando no MySQL porta 3008"}

if not os.path.exists("profile_pics"):
    os.makedirs("profile_pics")

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(transactions.router)