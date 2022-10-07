from _odoo_config import product

p = product()
c = p.get_client()

crm_lead = c.model("crm.lead").browse(552076)

flow = [f for f in c.model("crm.lead.flow").search([("team_id", "=", crm_lead.team_id.id)])
        if crm_lead.contact_creator_crm_group_id.id in c.model("crm.lead.flow").browse(f).marketing_crm_group_ids.id]
if len(flow) >= 1:
    flow = flow[0]
if not flow:
    flow = [f for f in c.model("crm.lead.flow").search([("crm_group_id", "=", crm_lead.crm_group_id.id), ("team_id", "=", False)])
            if crm_lead.contact_creator_crm_group_id.id in c.model("crm.lead.flow").browse(f).marketing_crm_group_ids.id]
    if len(flow) >= 1:
        flow = flow[0]
if not flow:
    flow = [f for f in c.model("crm.lead.flow").search([("team_id", "=", crm_lead.team_id.id)])
            if len(c.model("crm.lead.flow").browse(f).marketing_crm_group_ids) == 0]
    if len(flow) >= 1:
        flow = flow[0]
if not flow:
    flow = [f for f in c.model("crm.lead.flow").search([("crm_group_id", "=", crm_lead.crm_group_id.id), ("team_id", "=", False)])
            if len(c.model("crm.lead.flow").browse(f).marketing_crm_group_ids) == 0]
    if len(flow) >= 1:
        flow = flow[0]
flow = c.model("crm.lead.flow").browse(flow)
flow_line_ids = flow.flow_line_ids
count_history = []
for line in flow_line_ids:
    line_count = c.model('crm.lead.flow.history') \
        .search_count([('flow_id', '=', flow.id),
                        ('team_id', '=', line.team_id.id),
                        ('crm_group_id', '=', line.crm_group_id.id),
                        ('crmf99_system_id', '=', line.crmf99_system_id.id)])
    count_history.append({
        'line_id': line.id,
        'weight': line_count / line.weight,
    })
line_id = min(count_history, key=lambda x: x['weight']).get('line_id')
line = flow.flow_line_ids.browse(line_id)
resale_crm_lead = c.model("crm.lead").create({
    "partner_id": crm_lead.partner_id.id,
    "type": "opportunity",
    "name": " ".join([crm_lead.partner_id.name, "Resale"]),
    "opportunity_type": "resale",
    "tag_ids": [(6, 0, crm_lead.tag_ids.id), (3, crm_lead.env.ref("crmf99.crmf99_crm_tag_sale").id, False), (3, crm_lead.env.ref("crmf99.crmf99_crm_tag_new_contact").id, False), (4, crm_lead.env.ref("crmf99.crmf99_crm_tag_resale").id, False)],
    "customer_note": crm_lead.customer_note,
    "origin_id": crm_lead.id,
    "sale_crm_lead_id": crm_lead.id,
    "description": crm_lead.description,
    "state": "new",
    "user_id": False,
    "team_id": line.team_id.id,
    "crm_group_id": line.team_id.crm_group_id.id if line.team_id else line.crm_group_id.id,
    "crmf99_system_id": line.team_id.crmf99_system_id.id if line.team_id else line.crm_group_id.crmf99_system_id.id if line.crm_group_id else line.crmf99_system_id.id,
})
c.model("crm.lead.flow.history").create({
    "flow_id": flow.id,
    "crm_lead_id": crm_lead.id,
    "dest_crm_lead_id": resale_crm_lead.id,
    "team_id": line.team_id.id,
    "crm_group_id": line.team_id.crm_group_id.id if line.team_id else line.crm_group_id.id,
    "crmf99_system_id": line.team_id.crmf99_system_id.id if line.team_id else line.crm_group_id.crmf99_system_id.id if line.crm_group_id else line.crmf99_system_id.id,
})
print(resale_crm_lead)