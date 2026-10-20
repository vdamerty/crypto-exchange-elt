{{ config(materialized='table') }}

with stg_currencies as (
    select * from {{ ref('stg_currencies') }}
)
select
    currency_id,
    code,
    currency_name
from stg_currencies