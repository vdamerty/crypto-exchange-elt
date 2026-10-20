with source as (
    select * from {{ source('raw_crypto', 'trades') }}
)
select
    trade_id,
    trader_id,
    currency_id,
    amount,
    price_usd,
    trade_date
from source