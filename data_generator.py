import pandas as pd
import numpy as np
from faker import Faker
import random
import os
from datetime import datetime, timedelta

# Ініціалізація Faker
fake = Faker('uk_UA')
Faker.seed(42)
random.seed(42)

# Створення папки Data Lake, якщо її немає
os.makedirs('data_lake', exist_ok=True)
print("Починаємо генерацію даних для криптобіржі (Варіант 9)...")

# =============================================
# 1. ТАБЛИЦІ ВИМІРІВ (DIMENSIONS)
# =============================================

# Вимір 1: Криптовалюти (Currencies)
def generate_currencies():
    print("Генерація криптовалют...")
    curr_list = [
        {'id': 1, 'code': 'BTC', 'name': 'Bitcoin'},
        {'id': 2, 'code': 'ETH', 'name': 'Ethereum'},
        {'id': 3, 'code': 'USDT', 'name': 'Tether'},
        {'id': 4, 'code': 'SOL', 'name': 'Solana'},
        {'id': 5, 'code': 'ADA', 'name': 'Cardano'}
    ]
    return pd.DataFrame(curr_list)

# Вимір 2: Трейдери (Traders) - з імітацією "брудних даних"
def generate_traders(n):
    print(f"Генерація {n} трейдерів...")
    data = []
    for i in range(1, n + 1):
        # 10% пропущених email для перевірки dbt-тестів
        email = fake.email() if random.random() > 0.1 else None
        data.append({
            'trader_id': i,
            'full_name': fake.name(),
            'email': email,
            'country': fake.country(),
            'registration_date': fake.date_between(start_date='-2y', end_date='today')
        })
    df = pd.DataFrame(data)
    
    # Штучно додаємо 5% дублікатів для перевірки очищення
    duplicates = df.sample(frac=0.05)
    df = pd.concat([df, duplicates], ignore_index=True)
    return df

# Вимір 3: Гаманці (Wallets)
def generate_wallets(n, trader_ids, currency_ids):
    print(f"Генерація {n} гаманців...")
    data = []
    for i in range(1, n + 1):
        data.append({
            'wallet_id': i,
            'trader_id': random.choice(trader_ids),
            'currency_id': random.choice(currency_ids),
            'balance': round(random.uniform(0.0, 15000.0), 4)
        })
    return pd.DataFrame(data)


# =============================================
# 2. ТАБЛИЦІ ФАКТІВ (FACTS)
# =============================================

# Факт 1: Угоди (Trades)
def generate_trades(n, trader_ids, currency_ids):
    print(f"Генерація {n} угод...")
    data = []
    for i in range(1, n + 1):
        trade_date = fake.date_time_between(start_date='-1y', end_date='now')
        data.append({
            'trade_id': fake.uuid4(),
            'trader_id': random.choice(trader_ids),
            'currency_id': random.choice(currency_ids),
            'amount': round(random.uniform(0.01, 5.0), 4),
            'price_usd': round(random.uniform(100.0, 60000.0), 2),
            'trade_date': trade_date
        })
    return pd.DataFrame(data)

# Факт 2: Введення/виведення коштів (Deposits & Withdrawals)
def generate_deposits_withdrawals(n, trader_ids, currency_ids):
    print(f"Генерація {n} транзакцій поповнення/виведення...")
    data = []
    for i in range(1, n + 1):
        data.append({
            'transaction_id': fake.uuid4(),
            'trader_id': random.choice(trader_ids),
            'currency_id': random.choice(currency_ids),
            'tx_type': random.choices(['deposit', 'withdrawal'], weights=[70, 30])[0],
            'amount': round(random.uniform(50.0, 10000.0), 2),
            'tx_date': fake.date_time_between(start_date='-1y', end_date='now')
        })
    return pd.DataFrame(data)


# =============================================
# 3. ВИКОНАННЯ ТА ЗБЕРЕЖЕННЯ
# =============================================
if __name__ == "__main__":
    df_currencies = generate_currencies()
    df_traders = generate_traders(300)
    
    # Отримуємо унікальні ID для підтримки зв'язків (Referential Integrity)[cite: 28]
    unique_trader_ids = df_traders['trader_id'].dropna().unique().tolist()
    currency_ids = df_currencies['id'].tolist()
    
    df_wallets = generate_wallets(400, unique_trader_ids, currency_ids)
    df_trades = generate_trades(3000, unique_trader_ids, currency_ids)
    df_deposits = generate_deposits_withdrawals(1500, unique_trader_ids, currency_ids)

    # Збереження у форматі Parquet (Data Lake)[cite: 27, 28]
    print("Збереження файлів у форматі Parquet...")
    df_currencies.to_parquet('data_lake/raw_currencies.parquet', index=False)
    df_traders.to_parquet('data_lake/raw_traders.parquet', index=False)
    df_wallets.to_parquet('data_lake/raw_wallets.parquet', index=False)
    df_trades.to_parquet('data_lake/raw_trades.parquet', index=False)
    df_deposits.to_parquet('data_lake/raw_deposits_withdrawals.parquet', index=False)

    print("Генерація успішно завершена! Файли збережено у папці /data_lake")