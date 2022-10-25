from _odoo_config import product
from datetime import datetime
import requests

p = product()
c = p.get_client()

all_line = c.model('res.partner.flow.line').search([('flow_id', '=', False)])
print(all_line)
for l in all_line:
    c.model('res.partner.flow.line').browse(l).unlink()

all_line = c.model('res.partner.flow.line').search([('flow_id', '=', False)])
print(all_line)
