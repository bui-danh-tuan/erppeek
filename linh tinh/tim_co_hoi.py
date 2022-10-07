from _odoo_config import product, dev, stage
from datetime import datetime, timedelta

import xlsxwriter
 
workbook = xlsxwriter.Workbook('hello.xlsx')
worksheet = workbook.add_worksheet()
p = product()
c = p.get_client()

crm_lead_id =  c.model('crm.lead').browse(149593)
crm_lead_id.optimal_crm_lead_id = False
print(crm_lead_id.optimal_crm_lead_id)
