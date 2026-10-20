with source as (
    select * from {{ source('raw_crypto', 'currencies') }}
)
select
    id as currency_id,
    code,
    name as currency_name
from source