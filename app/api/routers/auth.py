from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.conn import get_db
from app.db.models import User
from app.api.schemas import UserSchema
from app.api.utils import hash_id  # импортируем нашу функцию для хэширования

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register")
async def register(user: UserSchema, db: AsyncSession = Depends(get_db)):
    tg_hashed = hash_id(user.tg_id)
    query = select(User).filter(User.tg_id == tg_hashed)
    result = await db.execute(query)
    db_user = result.scalars().first()

    if db_user:
        return {"message": "Пользователь уже существует"}

    new_user = User(tg_id=tg_hashed)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return {"message": "Пользователь успешно создан"}
