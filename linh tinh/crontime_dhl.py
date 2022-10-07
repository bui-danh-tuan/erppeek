from _odoo_config import product

p = product()
c = p.get_client()

# all_sale_order = c.model('sale.order').search([('shipping_unit_id', '=', 4), 
# ('summary_state', 'not in', ['rfq', 'completed', 'cancel']), 
# ('create_date', '>', '2022-08-01 00:00:00')])
# print(len(all_sale_order))
# i = 0
# for s in all_sale_order:
#     print(f"{i} - {len(all_sale_order)}")
#     i += 1
#     c.model('sale.order').browse(s).dhl_cron_time = False

all_order_name =  c.model('sale.order').search_read([
    ('summary_state', 'not in', ['rfq', 'completed', 'cancel']),
    ('shipping_unit_id', '=', 4),
    ('crm_group_id', '=', crm_group_id)],
    ['name'], order='dhl_cron_time asc, id desc')

