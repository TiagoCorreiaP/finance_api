import shutil
import os
from fastapi import File, UploadFile, Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from app import crud, models

router = APIRouter(prefix="/profile", tags=["profile"])
@router.post("/upload-avatar")
async def upload_avatar(file: UploadFile = File(...),db: AsyncSession = Depends(crud.get_db),current_user: models.User = Depends(crud.get_current_user),):
    os.makedirs("profile_pics", exist_ok=True)
    file_extension = file.filename.split(".")[-1]
    file_path = f"profile_pics/{current_user.id}_avatar.{file_extension}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    current_user.profile_picture = file_path
    await db.commit()

    return {"info": "foto atualizada!", "url": file_path}
