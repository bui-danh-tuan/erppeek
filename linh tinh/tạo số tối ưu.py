from _odoo_config import dev
from datetime import datetime, timedelta
d = dev()
c = d.get_client()

for i in range(1000):
    partner = c.model('res.partner').create({
        'name': 'Tuấn - Số tối ưu', 
        'phone': "0"+str(210000000+i+2000),
        'contact_creator_id': 28,
        'marketing_team_id': 14,
        'source_id': 112,
        'crm_group_id': 2,
        'crmf99_system_id': 3,
        'crm_lead_user_id': 12,
        'crm_lead_team_id': 5,
        'crm_lead_crm_group_id': 2,
        'crm_lead_crmf99_system_id': 3,
        'country_type_id': 4,
        'product_category_id': 209,
    })
    partner.init_opportunity()
    partner.crm_lead_id.state = 'qualified'
    partner.crm_lead_id.created_datetime = '2022-06-24 04:51:40'
    print(f"{i}-{partner.crm_lead_id.id}")