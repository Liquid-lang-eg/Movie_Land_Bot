import jwt
from fastapi import Request
from sqladmin.authentication import AuthenticationBackend
from sqlalchemy import select
from config import settings
from app.services.auth import create_token, verify_password
from app.db.conn import AsyncSessionLocal
from app.db.models import User


class AdminAuth(AuthenticationBackend):

    async def login(self, request: Request) -> bool:
        form = await request.form()
        tg_id, password = form["telegram_id"], form["password"]
        async with AsyncSessionLocal() as session:
            query = select(User).where(User.tg_id == tg_id)
            result = await session.execute(query)
            db_user = result.scalar_one_or_none()
        if (
            not db_user
            or not verify_password(password, db_user.hashed_password)
            or not db_user.is_admin
        ):
            return False
        token = create_token(
            data={"tg_id": tg_id}, secret_key=settings.SECRET_KEY_ADMIN
        )
        request.session.update({"token": token})
        return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")
        if not token:
            return False
        try:

            payload = jwt.decode(
                token,
                settings.SECRET_KEY_ADMIN,
                algorithms=[settings.ALGORITHM],
            )
            tg_id = payload.get("tg_id")
            if not tg_id:
                return False
            async with AsyncSessionLocal() as session:
                query = select(User).where(User.tg_id == tg_id)
                result = await session.execute(query)
                db_user = result.scalar_one_or_none()
                if not db_user or not db_user.is_admin:
                    request.session.clear()
                    return False
            return True
        except jwt.ExpiredSignatureError:
            return False
        except jwt.PyJWKError:
            return False


authentication_backend = AdminAuth(secret_key=settings.SECRET_KEY_ADMIN)
