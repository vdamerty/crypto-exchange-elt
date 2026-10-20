# Lab #2: Crypto Exchange ELT Pipeline

## Опис проєкту
Цей проєкт реалізує повний аналітичний пайплайн за архітектурою **ELT** (Extract, Load, Transform) для даних криптовалютної біржі. 

## Технологічний стек
- **Python** (Pandas, SQLAlchemy, Psycopg2) — вилучення та завантаження сирих даних.
- **PostgreSQL (Docker)** — реляційне сховище даних (DWH).
- **dbt (data build tool)** — трансформація даних і побудова зіркової схеми.

## Структура сховища
- Схема **`raw`**: сирі дані з parquet-файлів (`currencies`, `traders`, `wallets`, `trades`, тощо).
- Схема **`analytics`**: очищені staging-моделі та аналітичні вітрини:
  - `dim_currencies` (вимір валют)
  - `dim_traders` (вимір трейдерів)
  - `fct_trades` (таблиця фактів угод із розрахунком суми `quantity * price`)

## Як запустити проєкт
1. Завантажити сирі дані в базу даних:
   ```bash
   python load_to_dwh.py
