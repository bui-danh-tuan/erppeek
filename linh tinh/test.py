from _odoo_config import product
from datetime import datetime
import requests

p = product()
c = p.get_client()
arr = c.model('res.partner.flow.line').search(
    [('flow_id', '=', False)]
)
for flow in arr:
    c.model('res.partner.flow.line').browse(flow).unlink()
# print(c.model('crm.lead').search([
#     ("crm_group_id", "=", 23),
#     ("state", "not in", ["failed","won"]),
#     ("opportunity_type", "=", 'sale'),
#     ("user_id", "=", False),
#     ("user_id", "=", False),
#     ("optimal_crm_lead_id", "=", False),
#     "|", "|",
#     ("team_id", "=", False),
#     ("team_id", "in", []),
#     ("team_id", "=", 10)
# ]))
