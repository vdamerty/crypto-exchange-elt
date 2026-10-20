with source as (
    select * from {{ source('raw_crypto', 'traders') }}
)
select
    trader_id,
    full_name,
    email,
    country,
    registration_date
from source