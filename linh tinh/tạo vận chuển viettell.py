from _odoo_config import product
from datetime import datetime
p = product()
c = p.get_client()

arr = [
    "BSO083132",
    # "BSO083136",
    # "BSO083109",
    # "BSO083286",
    # "BSO083352",
    # "BSO083057",
    # "BSO083018",
    # "BSO082938",
    # "BSO082987",
    # "BSO083251",
    # "BSO082575",
    # "BSO083381",
    # "BSO083107",
    # "BSO083141",
    # "BSO082930",
    # "BSO083208",
    # "BSO083326",
    # "BSO083335",
    # "BSO083267",
    # "BSO082976",
    # "BSO081438",
    # "BSO083074",
    # "BSO083174",
    # "BSO082207",
    # "BSO083266",
    # "BSO083350"
]
all_order = c.model('sale.order').search([('name', 'in', arr)])
for id in all_order:
    order = c.model('sale.order').browse(id)
    if not order.latest_delivery_order_id:
        c.model('apif99.delivery.order').create({
                            'name': order.name,
                            'sale_id': order.id,
                            "third_party_shipping_state": "Giao cho Bưu tá đi nhận",
                            "cpn_created_datetime": datetime.now(),
                            "third_party_shipping_type": 'VIETTEL_POST',
                        })
        print(f"Tạo thành công: {order.name}")