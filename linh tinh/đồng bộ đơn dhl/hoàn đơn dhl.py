from _odoo_config import product
from datetime import datetime
import requests

p = product()
c = p.get_client()
p_r = "PROD"

all_order = c.model('sale.order').search([
    ('latest_delivery_order_state', '=', '77225'),
    ('shipping_unit_id', '=', 4),
    ('summary_state', '=', 'shipping')
])
n = len(all_order)
i = 0
for o in all_order:
    order =  c.model('sale.order').browse(o)
    order.summary_state = 'returning'
    print(f"{i}/{str(n).ljust(10)} {order.name} - {o}")
    i += 1