select
    product_id,
    product_name,
    -- Очищуємо ціну: переконуємося, що вона не менша за 0
    case 
        when price < 0 then 0 
        else price 
    end as price
from {{ source('raw', 'products') }}