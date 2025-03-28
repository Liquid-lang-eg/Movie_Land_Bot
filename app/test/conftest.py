import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.api.fastapi_main import app
from app.api.utils import hash_id
from app.db.models import Base, User
from app.db.conn import get_db
from config import DATABASE_URL

DATABASE_URL = DATABASE_URL

engine = create_async_engine(DATABASE_URL, echo=False)
TestingSessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

# Переопределение зависимости get_db для тестовой базы данных
async def override_get_db():
    async with TestingSessionLocal() as session:
        yield session

app.dependency_overrides[get_db] = override_get_db

# Фикстура для синхронного клиента (TestClient)
@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

# Фикстура для асинхронного клиента (AsyncClient)
@pytest.fixture(scope="module")
async def async_client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

# Фикстура для подготовки базы данных (создание и заполнение тестовыми данными)
@pytest.fixture(scope="module", autouse=True)
async def prepare_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with TestingSessionLocal() as session:
        # Например, создаём тестового пользователя с tg_id, хэш которого соответствует hash_id(123)
        test_user = User(id=1, tg_id=hash_id(123))
        session.add(test_user)
        await session.commit()
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)