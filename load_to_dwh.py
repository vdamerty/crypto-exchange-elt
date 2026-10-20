import pandas as pd
from sqlalchemy import create_engine, text

# Рядок підключення до нашого Docker PostgreSQL
DB_URL = "postgresql+psycopg2://admin:adminpassword@localhost:5432/ecommerce_dwh"
engine = create_engine(DB_URL)

def load_data_to_dwh():
    with engine.connect() as conn:
        # ДОДАНО: видаляємо схему analytics разом із залежностями, щоб pandas міг оновити таблиці в raw
        conn.execute(text("DROP SCHEMA IF EXISTS analytics CASCADE;"))
        
        # Створення схеми raw, якщо її немає
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS raw;"))
        conn.commit()

    print("Завантаження даних у схему 'raw'...")
    
    # Читаємо з parquet і записуємо в таблиці PostgreSQL
    pd.read_parquet('data_lake/raw_currencies.parquet').to_sql('currencies', engine, schema='raw', if_exists='replace', index=False)
    pd.read_parquet('data_lake/raw_traders.parquet').to_sql('traders', engine, schema='raw', if_exists='replace', index=False)
    pd.read_parquet('data_lake/raw_wallets.parquet').to_sql('wallets', engine, schema='raw', if_exists='replace', index=False)
    pd.read_parquet('data_lake/raw_trades.parquet').to_sql('trades', engine, schema='raw', if_exists='replace', index=False)
    pd.read_parquet('data_lake/raw_deposits_withdrawals.parquet').to_sql('deposits_withdrawals', engine, schema='raw', if_exists='replace', index=False)

    print("Усі таблиці криптобіржі успішно завантажені у базу даних (схема raw)!")

if __name__ == "__main__":
    load_data_to_dwh()