from _odoo_config import dev
p = dev()
c = p.get_client()

all_optimal_flow = c.model('res.partner.flow').search([('optimal', '=', True)])
all_mkt_team_ids = []
all_mkt_group_ids = []
for optimal_id in all_optimal_flow:
    optimal = c.model('res.partner.flow').browse(optimal_id)
    if optimal.team_id.id:
        all_mkt_team_ids.append(optimal.team_id.id)
    else:
        all_mkt_group_ids.append(optimal.cmr_group_id.id)

all_mkt_team_ids = list(set(all_mkt_team_ids))
all_mkt_group_ids = list(set(all_mkt_group_ids))
all_crm_lead = c.model('crm.lead').search([
    ('optimal_crm_lead_id', '=', False),
    ('state', 'not in', ('new', 'won', 'failed')),
    ('active', '=', True),
    ('opportunity_type', 'in', ('sale', 'optimal')),
    ('is_inprogress', '=', True),
    ('user_id', '!=', False),
    ('old_order_ids', '=', False),
    ('created_datetime', '<', '2022-10-02 00:00:00.000'),
    ('marketing_team_id', 'not in', all_mkt_team_ids),
    ('contact_creator_crm_group_id', 'not in', all_mkt_group_ids)
])
f = open("D:\\Code\\Other\\erp_peek\\linh tinh\\chạy số tối ưu.txt", "w")
for id in all_crm_lead:
    lead = c.model('crm.lead').browse(int(id))
    if len(lead.old_order_ids) <= 0:
        f.write(str(id)+"\n")
