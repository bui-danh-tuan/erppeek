from _odoo_config import dev


p = dev()
c = p.get_client()
count = 0
while True:
    all_lead = c.model('crm.lead').search([('opportunity_type', '=', 'optimal'), ('is_inprogress', '=', False)], limit=100)
    for l in all_lead:
        c.model('crm.lead').browse(l).unlink()
        count += 1
        print(count)