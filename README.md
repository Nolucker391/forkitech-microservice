<h1>🚀 FastAPI TRON Wallet Info Microservice</h1>

## Описание 

Этот микросервис предоставляет cобой веб-сервис, включая в себя - информацию о кошельке в сети Tron (TRX), включая баланс, bandwidth и energy. На базе приложения - FASTApi, базы данных SQLALchemy и PostgreSQL (для тестов). Все компоненты работают в контейнерах Docker. Сервис предоставляет пользователям возможность:

- **Получение информации по адресу кошелька.**.
- **Сохранение данных в базе.**
- **Получение истории запросов.**
- **Интеграционные и юнит-тесты.**

## Инструкция по запуску проекта 

1. Скопировать файлы проекта. Создать и войти в виртуальное окружение.
```commandline
git clone https://github.com/Nolucker391/forkitech-microservice.git
```

2. Установка необходимых зависимостей. 
```commandline
pip install -r requirements.txt 

pip install --upgrade pip
```

3. Запуск проекта.
```commandline
docker compose up
```

4. Автотестирование проекта.
```commandline

pytest /tests/
```

## Инструменты разработки

| Библиотека           | Версия |
|----------------------|--------|
| FastApi              | `0.115.12` |
| SQLAlchemy      | `2.0.39` |
| Docker               | `27.3.1` |
| PostgreSQL           | `17.4.0`  |
| uvicorn               | `0.34.0` |
| pytest             | `8.3.5`  |
| pydantic             | `2.10.6` |
