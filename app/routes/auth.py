from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from .. import crud, auth, database

router = APIRouter(tags=["auth"])

@router.post("/login")
async def login_acess_for_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: AsyncSession = Depends(database.get_db)
):
    user = await crud.get_user_by_email(db, email=form_data.username)

    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException (
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    acess_token = auth.create_access_token(data={"sub": user.email})

    return {"acess_token": acess_token, "token_type": "bearer"}