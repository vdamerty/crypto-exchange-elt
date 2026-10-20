select
    t.trade_id,
    t.trader_id,
    t.currency_id,
    t.trade_date,
    t.quantity,
    t.price,
    -- Розрахунок загальної суми угоди
    (t.quantity * t.price) as total_amount,
    t.trade_type
from {{ ref('stg_trades') }} t
left join {{ ref('dim_traders') }} tr on t.trader_id = tr.trader_id
left join {{ ref('dim_currencies') }} c on t.currency_id = c.currency_id