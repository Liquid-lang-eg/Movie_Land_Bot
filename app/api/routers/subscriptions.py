from fastapi import APIRouter, Depends, HTTPException, Query, Body
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.models import Genre, UserGenreSubscription, User
from app.db.conn import get_db
from app.api.utils import hash_id

router = APIRouter(prefix="/subscription", tags=["subscription"])


@router.get("/genres/")
async def get_genres_endpoint(session: AsyncSession = Depends(get_db)):
    result = await session.execute(select(Genre))
    genres = result.scalars().all()
    return [{"id": genre.id, "name": genre.name} for genre in genres]

@router.get("/subscriptions/")
async def get_user_subscriptions_endpoint(user_tg_id: int = Query(...), session: AsyncSession = Depends(get_db)):
    hashed_tg = hash_id(user_tg_id)
    result = await session.execute(
        select(UserGenreSubscription)
        .join(User, UserGenreSubscription.user_id == User.id)
        .where(User.tg_id == hashed_tg)
    )
    subscriptions = result.scalars().all()
    return [{"genre_id": sub.genre_id} for sub in subscriptions]

@router.post("/subscribe/")
async def subscribe_endpoint(
    user_tg_id: int = Body(...),
    genre_id: int = Body(...),
    session: AsyncSession = Depends(get_db)
):
    hashed_tg = hash_id(user_tg_id)
    user_result = await session.execute(
        select(User).where(User.tg_id == hashed_tg)
    )
    user = user_result.scalars().first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    sub_result = await session.execute(
        select(UserGenreSubscription).where(
            UserGenreSubscription.user_id == user.id,
            UserGenreSubscription.genre_id == genre_id
        )
    )
    if sub_result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Already subscribed")

    new_sub = UserGenreSubscription(user_id=user.id, genre_id=genre_id)
    session.add(new_sub)
    await session.commit()
    return {"detail": "Subscribed"}


@router.post("/unsubscribe/")
async def unsubscribe_endpoint(
        user_tg_id: int = Body(...),
        genre_id: int = Body(...),
        session: AsyncSession = Depends(get_db)
):
    hashed_tg = hash_id(user_tg_id)
    user_result = await session.execute(
        select(User).where(User.tg_id == hashed_tg)
    )
    user = user_result.scalars().first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    sub_result = await session.execute(
        select(UserGenreSubscription).where(
            UserGenreSubscription.user_id == user.id,
            UserGenreSubscription.genre_id == genre_id
        )
    )
    subscription = sub_result.scalar_one_or_none()
    if not subscription:
        raise HTTPException(status_code=400, detail="Not subscribed")

    # Удаляем подписку
    await session.delete(subscription)
    await session.commit()
    return {"detail": "Unsubscribed"}