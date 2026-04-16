from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from .. import crud, schemas, database, auth, models

router = APIRouter(prefix="/transactions", tags=["transactions"])

@router.post("/", response_model=schemas.TransactionResponse)
async def create_new_transaction(
    transaction: schemas.TransactionCreate,
    db: AsyncSession = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    return await crud.create_trasactions(db=db, transaction=transaction, user_id=current_user.id)

@router.get("/summary")
async def get_summary(db: AsyncSession = Depends(database.get_db),current_user: models.User = Depends(auth.get_current_user)):
    result = await db.execute(select(models.Transaction).filter(models.Transaction.user_id == current_user.id))
    transactions = result.scalars().all()
    entradas = sum(t.amount for t in transactions if t.type == "entrada")
    saidas = sum(t.amount for t in transactions if t.type == "saida")
    juros = sum(t.interest for t in transactions if t.interest)
    saldo = entradas - saidas
    return {
        "total_entradas": entradas,
        "total_saidas": saidas,
        "total_juros": juros,
        "saldo_atual": saldo
    }

@router.get("/listar")
async def list_my_transactions(
    db: AsyncSession = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    print(f"DEBUG: Usuário logado é {current_user.email}")
    return await crud.get_user_transactions(db, user_id=current_user.id)
