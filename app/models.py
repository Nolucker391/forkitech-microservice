import datetime

from datetime import datetime, timezone
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, String, Integer, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./database/wallet_info.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class WalletRequest(BaseModel):
    """Модель для запроса информации по кошельку."""
    address: str

class WalletInfo(Base):
    """Модель для хранения информации о кошельке в базе данных."""
    __tablename__ = "wallet_info"

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, index=True)
    balance = Column(String)
    bandwidth = Column(Integer)
    energy = Column(Integer)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


def get_db():
    """Функция, подключения сессии к БД."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

