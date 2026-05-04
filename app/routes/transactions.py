from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from .. import crud, schemas, database, auth, models

router = APIRouter(prefix="/transactions", tags=["transactions"]
                   )

@router.post("/", response_model=schemas.TransactionResponse)
async def create_new_transaction(
    transaction: schemas.TransactionCreate,
    db: AsyncSession = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    return await crud.create_trasactions(db=db, transaction=transaction, user_id=current_user.id)

@router.get("/summary")
async def get_transaction_summary(
    db: AsyncSession = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    return await crud.get_transaction_summary(db, user_id=current_user.id)

@router.get("/listar")
async def list_my_transactions(
    db: AsyncSession = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    print(f"DEBUG: Usuário logado é {current_user.email}")
    return await crud.get_user_transactions(db, user_id=current_user.id)

@router.get("/stats")
async def get_finance_stats(
    db: AsyncSession = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    return await crud.get_finance_stats(db, user_id=current_user.id)

@router.get("/health")
async def get_finance_health(db: AsyncSession = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    return await crud.get_finance_health(db, user_id=current_user.id)

@router.get("/top-expenses")
async def get_top_expenses(db: AsyncSession = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    return await crud.get_top_expenses(db, user_id=current_user.id)

@router.delete("/transactions/delete-all")
async def clear_transactions(db: AsyncSession = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    success = await crud.delete_all_transactions(db, current_user)
    if not success:
        raise HTTPException(status_code=500, detail="Erro ao deletar transações")
    return {"detail": "Todas as transações foram deletadas com sucesso"}

@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_transaction(transaction_id: int, db: AsyncSession = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    success = await crud.delete_transaction(db, transaction_id, user_id=current_user.id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transação não encontrada ou não pertence ao usuário")
    return{"detail": "Transação deletada com sucesso"}

@router.put("/transactions/{transaction_id}", response_model=schemas.TransactionResponse)
async def edit_transaction(
    transaction_id: int,
    transaction_data: schemas.TransactionCreate,
    db: AsyncSession = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    updated_transaction = await crud.update_transaction(
        db, transaction_id, current_user.id, transaction_data
    )
    
    if updated_transaction is None:
        raise HTTPException(status_code=404, detail="Transação não encontrada ou acesso negado")
        
    return updated_transaction

@router.get("/export/pdf")
async def export_transactions_pdf(
    db: AsyncSession = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    try:
        pdf_data = await crud.generate_transactions_pdf(db, current_user.id)
        
        return Response(
            content=pdf_data,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename=extrato_{current_user.id}.pdf",
                "Access-Control-Expose-Headers": "Content-Disposition"
            }
        )
    except Exception as e:
        print(f"Erro: {e}") 
        raise HTTPException(status_code=500, detail="Erro ao gerar PDF.")