import pytest

from fastapi.testclient import TestClient
from app.main import app, WalletInfo, get_db


@pytest.fixture(scope="function")
def override_get_db(db_session):
    """Подменяем функцию get_db на использование тестовой БД."""
    def _get_db():
        yield db_session
    return _get_db

@pytest.fixture(scope="function")
def client(override_get_db):
    """Фикстура для тестового клиента FastAPI."""
    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def test_get_wallet_info(client):
    """
    Интеграционный тест: проверяем API `POST /wallet-info/`

    - Тестирует получение информации о кошельке через API.
    """
    response = client.post("/wallet-info/", json={"address": "TPfH11yvvZN6xSPPcwCTnANzhUKCLujxHQ"})
    assert response.status_code == 200

    data = response.json()

    assert "address" in data
    assert "balance" in data
    assert "bandwidth" in data
    assert "energy" in data
    assert data["address"] == "TPfH11yvvZN6xSPPcwCTnANzhUKCLujxHQ"


def test_wallet_info_model(db_session):
    """
    Юнит-тест: проверяем запись в БД
    Тестирует запись кошелька в БД.
    """
    wallet = WalletInfo(
        address="TPfH11yvvZN6xSPPcwCTnANzhUKCLujxHQ",
        balance="100.5",
        bandwidth=500,
        energy=1000
    )

    db_session.add(wallet)
    db_session.commit()
    db_session.refresh(wallet)

    assert wallet.id is not None
    assert wallet.address == "TPfH11yvvZN6xSPPcwCTnANzhUKCLujxHQ"
    assert wallet.balance == "100.5"
    assert wallet.bandwidth == 500
    assert wallet.energy == 1000