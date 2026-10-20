with source as (
    select * from {{ source('raw_crypto', 'wallets') }}
)
select
    wallet_id,
    trader_id,
    currency_id,
    cast(balance as float) as balance
from source