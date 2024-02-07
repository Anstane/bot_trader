import os
import asyncio

from dotenv import load_dotenv

from sqlalchemy import Column, String, Integer, select, delete
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

load_dotenv()

db_user = os.getenv("POSTGRES_USER")
db_password = os.getenv("POSTGRES_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("POSTGRES_DB")

engine  = create_async_engine(f"postgresql+asyncpg://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}", echo=True)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False) # Асинхронная сессия.

Base = declarative_base() # Из классов делаем модели.

class Wallet(Base):
    __tablename__ = "wallets"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    wallet_address = Column(String)

async def create_database() -> None:
    """Функция для создания БД."""

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all) # Стираем все старые таблицы.
        await conn.run_sync(Base.metadata.create_all) # Создаём новые таблицы.

async def add_user_wallet(user_id: int, wallet_address: str) -> bool:
    """Функция для добавления кошелька в БД."""

    async with async_session() as session:
        # Проверяем есть ли в БД запись с полученными данными.
        select_wallet = select(Wallet).where(
            (Wallet.user_id == user_id) & (Wallet.wallet_address == wallet_address)
        )
        result = await session.execute(select_wallet)
        existing_wallet = result.scalar() # Этот метод возвращает объект или None.

        if existing_wallet: # Если объект существует - возвращаем False.
            return False

        # В обратном случае - создаём и возвращаем True.
        new_wallet = Wallet(user_id=user_id, wallet_address=wallet_address)
        session.add(new_wallet)
        await session.commit()
        return True

async def get_user_wallets(user_id: int) -> list:
    """Функция, которая получает список существующих кошельков."""

    async with async_session() as session:
        select_wallet = select(Wallet).where((Wallet.user_id == user_id))
        result = await session.execute(select_wallet)
        return result.scalars().all()

async def delete_user_wallet(user_id: int, wallet_address: str) -> bool:
    """Функция для удаления выбранного кошелька."""

    async with async_session() as session:
        # Проверяем есть ли в БД запись с полученными данными.
        select_wallet = select(Wallet).where(
            (Wallet.user_id == user_id) & (Wallet.wallet_address == wallet_address)
        )
        result = await session.execute(select_wallet)
        existing_wallet = result.scalar() # Этот метод возвращает объект или None.

        if existing_wallet: # Если объект существует - удаляем и возвращаем True.
            select_wallet = delete(Wallet).where(
                (Wallet.user_id == user_id) & (Wallet.wallet_address == wallet_address)
            )
            await session.execute(select_wallet)
            await session.commit()
            return True

        return False # Если объект не найден, возвращаем False.

async def main() -> None:
    """Вспомогательная функция для запуска БД."""

    await create_database()

if __name__ == "__main__":
    asyncio.run(main())
