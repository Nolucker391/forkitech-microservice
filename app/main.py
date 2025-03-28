from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from tronpy import Tron

from app.models import WalletRequest, get_db, WalletInfo, Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()
tron_client = Tron()


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
