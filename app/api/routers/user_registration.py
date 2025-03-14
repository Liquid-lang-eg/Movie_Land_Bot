from fastapi import APIRouter, Depends
from app.db.models import User
from ..schemas import UserSchema
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.conn import get_db
router = APIRouter()


@router.post("/register")
def register(user: UserSchema, db: AsyncSession = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user.id).first()

    if not db_user:
        new_user = User(id=user.id, tg_id=user.tg_id)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

    return {"message": "OK"}