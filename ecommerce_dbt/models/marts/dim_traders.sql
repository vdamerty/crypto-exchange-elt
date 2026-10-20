{{ config(materialized='table') }}

with stg_traders as (
    select * from {{ ref('stg_traders') }}
)
select
    trader_id,
    full_name,
    email,
    country,
    registration_date
from stg_traders