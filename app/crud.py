from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from . import models, schemas, auth
from fastapi import UploadFile
import os
import shutil

async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(models.User).filter(models.User.email == email))
    return result.scalars().first()

async def create_user(db: AsyncSession, user: schemas.UserCreate):
    hashed_pwd = auth.get_password_hash(user.password)
    db_user = models.User(
        full_name=user.full_name,
        email=user.email,
        hashed_password=hashed_pwd,
        phone=user.phone,
        birth_date=user.birth_date
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
    result = await db.execute(select(models.Transaction).filter(models.Transaction.owner_id == user_id))
    trasactions = result.scalars().all()

    entradas = sum(t.amount for t in trasactions if t.type == "entrada")
    saidas = sum(t.amount for t in trasactions if t.type == "saida")
    saldo = entradas - saidas

    return {
        "total_entradas": entradas,
        "total_saidas": saidas,
        "saldo_atual": saldo,
        "status_financeiro": "positivo" if saldo >= 0 else "negativo"
    }

async def get_finance_health(db: AsyncSession, user_id: int):
    result = await db.execute(select(models.Transaction).filter(models.Transaction.owner_id == user_id))
    transactions = result.scalars().all()

    income = sum(t.amount for t in transactions if t.type == "entrada")
    expense = sum(t.amount for t in transactions if t.type == "saida")
    
    if income == 0:
        return{"status": "Sem dados", "ratio": 0}
    
    ratio = (income / expense) * 100

    if ratio < 50:
        msg  = "Saúde excelente! Você está economizando."
    elif ratio < 80:
        msg = "Cuidado! Seus gastos estão chegando perto do seu limite da sua renda."
    else:
        msg = "Alerta! Você está gastando quase tudo (ou mais) do que ganha."

    return {
        "porcentagem_gastos": round(ratio, 2),
        "status": msg,
        "sugestao": "Tende manter seus gastos abaixo de 70% da sua renda para uma saúde financeira mais equilibrada."
    }

async def get_top_expenses(db: AsyncSession, user_id: int):
    result = await db.execute(select(models.Transaction).filter(models.Transaction.owner_id == user_id, models.Transaction.type == "saida"))
    transactions = result.scalars().all()

    category_totals = {}
    for t in transactions:
            category_totals[t.category] = category_totals.get(t.category, 0) + t.amount   
    sorted_cats = sorted(category_totals.items(), key=lambda x: x[1], reverse=True) 
    return [{"category": cat, "total": val} for cat, val in sorted_cats[:5]]

async def get_finance_stats(db: AsyncSession, user_id: int):
    result = await db.execute(
        select(models.Transaction).filter(models.Transaction.owner_id == user_id)
    )
    transactions = result.scalars().all()

    total_entradas = sum(t.amount for t in transactions if t.type == "entrada")
    total_saidas = sum(t.amount for t in transactions if t.type == "saida")
    
    categories = {}
    for t in transactions:
        if t.type == "saida":
            categories[t.category] = categories.get(t.category, 0) + t.amount

        categories_stats = []
        for cat, val in categories.items():
            perc = (val / total_saidas * 100) if total_saidas > 0 else 0
            categories_stats.append({
                "category": cat,
                "value": val,
                "percentage": round(perc, 2)
            })

    return {
        "total_entradas": total_entradas,
        "total_saidas": total_saidas,
        "balance": total_entradas - total_saidas,
        "categories_stats": categories_stats
    }

async def delete_transaction(db: AsyncSession, transaction_id: int, user_id: int):
    result = await db.execute(select(models.Transaction).filter(models.Transaction.id == transaction_id, models.Transaction.owner_id == user_id))
    db_transaction = result.scalar_one_or_none()
    if db_transaction:
        await db.delete(db_transaction)
        await db.commit()
        return True
    return False

async def save_profile_picture(db: AsyncSession, user: models.User, file: UploadFile):
    upload_dir = "static/profile_pics"
    extension = file.filename.split(".")[-1].lower()
    filename = f"user_{user.id}.{extension}"
    file_path = os.path.join(upload_dir, filename)

    os.makedirs(upload_dir, exist_ok=True)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    user.profile_picture = f"{file_path}"
    await db.commit()
    await db.refresh(user)

    return user.profile_picture
