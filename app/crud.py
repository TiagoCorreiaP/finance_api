from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from . import models, schemas, auth

async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(models.User).filter(models.User.email == email))
    return result.scalars().first()

async def create_user(db: AsyncSession, user: schemas.UserCreate):
    hashed_pwd = auth.get_password_hash(user.password)
    db_user = models.User(
        full_name=user.full_name,
        email=user.email,
        hashed_password=hashed_pwd
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def create_trasactions(db: AsyncSession,transaction: schemas.TransactionCreate, user_id: int):
    db_transaction = models.Transaction(
        description=transaction.description,
        amount=transaction.amount,
        type=transaction.type,
        category=transaction.category,
        interest=transaction.interest,
        owner_id=user_id
    )
    db.add(db_transaction)
    await db.commit()
    await db.refresh(db_transaction)
    return db_transaction

async def get_user_transactions(db: AsyncSession, user_id: int):
    result = await db.execute(select(models.Transaction).filter(models.Transaction.owner_id == user_id))
    return result.scalars().all()

async def get_transaction_summary(db: AsyncSession, user_id: int):
    result = await db.execute(
        select(models.Transaction).filter(models.Transaction.user_id == user_id)
    )
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