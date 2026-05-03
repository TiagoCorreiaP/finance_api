from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from .. import crud, schemas, database, models, auth

router = APIRouter (
    prefix="/users",
    tags=["users"]
)

@router.post("/", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user: schemas.UserCreate, db: AsyncSession = Depends(database.get_db)):
    db_user = await crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=409,
            detail="Este email já está cadastrado"
        )
    
    return await crud.create_user(db=db, user=user)

@router.get("/me")
async def get_my_profile(current_user: models.User = Depends(auth.get_current_user)):
    return {
        "id": current_user.id,
        "name": current_user.full_name,
        "email": current_user.email,
        "phone": current_user.phone,
        "birthdate": current_user.birth_date,
        "profile_picture": current_user.profile_picture or "default_profile_picture.png"
    }

@router.post("/upload-photo")
async def upload_profile_photo(file: UploadFile = File(...), db: AsyncSession = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    if not file.filename.lower().endswith((".jpg", ".jpeg", ".png")):
        raise HTTPException(status_code=400, detail="Apenas arquivos JPG, JPEG ou PNG são permitidos.")

    photo_url = await crud.save_profile_picture(db, current_user, file)

    return{"url": photo_url}    

@router.get("/profile-picture-url")
async def update_profile_picture_url(
    data: schemas.ProfilePictureUpdate,
    db: AsyncSession = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    # Atualiza o campo no objeto do usuário logado
    current_user.profile_picture_url = data.url
    
    await db.commit()
    await db.refresh(current_user)
    
    return {"message": "Foto de perfil atualizada com sucesso!", "url": current_user.profile_picture_url}