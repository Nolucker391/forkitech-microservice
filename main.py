import datetime

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, String, Integer, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from tronpy import Tron
from tronpy.keys import PrivateKey

DATABASE_URL = "sqlite:///./wallet_info.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

app = FastAPI()
tron_client = Tron()

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
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

Base.metadata.create_all(bind=engine)

def get_db():
    """Функция, подключения сессии к БД."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/wallet-info/")
def get_wallet_info(wallet: WalletRequest, db: Session = Depends(get_db)):
    """Обработчик POST-запроса для получения информации о кошельке TRX."""
    try:
        address = wallet.address
        account = tron_client.get_account(address)

        balance = account.get("balance", 0) / 1_000_000
        resources = tron_client.get_account_resource(address)
        bandwidth = resources.get("free_net_limit", 0)
        energy = resources.get("EnergyLimit", 0)

        wallet_info = WalletInfo(
            address=address,
            balance=str(balance),
            bandwidth=bandwidth,
            energy=energy
        )
        db.add(wallet_info)
        db.commit()
        db.refresh(wallet_info)

        return {
            "address": address,
            "balance": balance,
            "bandwidth": bandwidth,
            "energy": energy
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Ошибка: {str(e)}")

@app.get("/wallet-info/")
def get_wallet_history(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """Обработчик GET-запроса для получения истории информации о кошельках."""
    records = db.query(WalletInfo).order_by(WalletInfo.created_at.desc()).offset(skip).limit(limit).all()
    return records
