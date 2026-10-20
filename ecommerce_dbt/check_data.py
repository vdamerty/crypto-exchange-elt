import pandas as pd
from sqlalchemy import create_engine

# Підключення до бази даних
DB_URL = "postgresql+psycopg2://admin:adminpassword@localhost:5432/ecommerce_dwh"
engine = create_engine(DB_URL)

# Виводимо перші 5 рядків вітрини fct_trades
df = pd.read_sql("SELECT * FROM analytics.fct_trades LIMIT 5", engine)
print(df)