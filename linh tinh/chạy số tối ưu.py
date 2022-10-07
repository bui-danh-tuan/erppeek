from _odoo_config import dev
from datetime import datetime
p = dev()
c = p.get_client()

arr_id = []
f = open("D:\\Code\\Other\\erp_peek\\linh tinh\\chạy số tối ưu.txt", "r")
if len(arr_id) == 0:
    for x in f:
        y = x
        if '\n' in x:
            y = x.replace('\n',"")
        if y:
            arr_id.append(y)

model_crm_lead = c.model('ir.model').search([('model', '=', 'crm.lead')])
if len(model_crm_lead) == 1:
    all_col = [line.get('name') for line in c.model('ir.model.fields').search_read([('model_id', '=', model_crm_lead[0]), ('store', '=', True)], ['name'])]
    [all_col.remove(x) for x in ["id", "stage_id", "description", "user_id", "team_id",
                                                 "created_datetime", "date_open", "latest_read_datetime",
                                                 "create_date", "create_uid", "write_date", "write_uid", "date_open7", "create_date7" ,"message_follower_ids", "message_ids"] if x in all_col]
    for id in arr_id:
        try:
            lead = c.model('crm.lead').browse(int(id))
            if len(lead.old_order_ids) <= 0:
                val = {}
                for col in all_col:
                    try:
                        val[col] = getattr(lead, col)
                    except Exception as e:
                        print(e)
                val.update({
                    'tag_ids': [(6, 0, lead.tag_ids.ids)],
                    # 'create_date': str(datetime.now())[:23],
                    # 'created_datetime': str(datetime.now())[:23],
                    'stage_id': 1,
                    'opportunity_type': 'optimal',
                    'is_inprogress': False,
                    'optimal_crm_lead_id': False
                })
                lead.is_inprogress = False
                new_lead = c.model('crm.lead').create(val)
                lead.optimal_crm_lead_id = new_lead.id
                print(f"{str(lead.id).ljust(10,' ')}{new_lead.id}")
        except Exception as e:
            print(e)