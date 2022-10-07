from _odoo_config import product
p = product()
c = p.get_client()
partner_id = c.model('res.partner').browse(92572)
lead_ids = c.model('crm.lead').search([('partner_id', '=', 92572)])
partner_id.crm_lead_id = 153826
print(partner_id.crm_lead_id.id)
print(lead_ids)



