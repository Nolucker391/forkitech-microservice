import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from app.models import Base


# Настройки тестовой БД
DB_HOST_TEST = "localhost"
DB_PORT_TEST = 5433
DB_NAME_TEST = "test_db"
DB_USER_TEST = "test_user"
DB_PASS_TEST = "test_password"

TEST_DATABASE_URL = f"postgresql+psycopg2://{DB_USER_TEST}:{DB_PASS_TEST}@{DB_HOST_TEST}:{DB_PORT_TEST}/{DB_NAME_TEST}"
test_engine = create_engine(TEST_DATABASE_URL, echo=False)
TestSession = scoped_session(sessionmaker(bind=test_engine))

Base.metadata.create_all(bind=test_engine)

@pytest.fixture(scope="session")
def test_db():
    """
    Фикстура для создания тестовой базы данных перед тестами.
    """
    yield
    print("Очистка тестовой базы данных")
    Base.metadata.drop_all(bind=test_engine)

@pytest.fixture(scope="function")
def db_session(test_db):
    """Фикстура для предоставления сессии базы данных."""
    session = TestSession()
    try:
        yield session
    finally:
        session.rollback()
        session.close()