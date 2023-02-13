from _odoo_config import stage

d = stage()
c = d.get_client()
all_user = c.model('res.users').search([])
count = 0
for u in all_user:
    s = c.model('res.users').browse(u)
    all_sale_crm_group_ids = []
    all_marketing_crm_group_ids = []

    all_sale_crm_group_ids.append(s.crm_group_id.id)
    all_sale_crm_group_ids.extend(s.crm_group_ids.id)
    all_sale_crm_group_ids.extend(s.sale_crm_group_ids.id)

    all_marketing_crm_group_ids.append(s.crm_group_id.id)
    all_marketing_crm_group_ids.extend(s.crm_group_ids.id)
    all_marketing_crm_group_ids.extend(s.marketing_crm_group_ids.id)

    s.all_sale_crm_group_ids = [(6, 0, all_sale_crm_group_ids)]
    s.all_marketing_crm_group_ids = [(6, 0, all_marketing_crm_group_ids)]
    count += 1
    print(f"{count}\t{u}")
    print(f"{count}\t{u}")