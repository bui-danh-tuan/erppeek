
import tkinter as tk
from datetime import datetime, timedelta
import erppeek
from functools import partial


def print_lable(lable, text):
    lable.configure(state='normal')
    lable.insert("end",text)
    lable.configure(state='disabled')



def conext_odoo(lable, text, sever, data, user, password):
    try:
        SERVER = sever.get()
        DATABASE = data.get()
        USERNAME = user.get()
        PASSWORD = password.get()
        c = erppeek.Client(
            SERVER,
            DATABASE,
            USERNAME,
            PASSWORD
        )
        return c
    except Exception as e: 
        print_lable(lable, e)

def tim_so(c, num_limit, start):
    all_optimal_flow = c.model('res.partner.flow').search([('optimal', '=', True)])
    all_mkt_team_ids = []
    all_mkt_group_ids = []
    for optimal_id in all_optimal_flow:
        optimal = c.model('res.partner.flow').browse(optimal_id)
        if optimal.team_id and optimal.team_id.id:
            all_mkt_team_ids.append(optimal.team_id.id)
        else:
            all_mkt_group_ids.append(optimal.crm_group_id.id)

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
        ('created_datetime', '<', str(datetime.now() - timedelta(hours = 7) - timedelta(days = 3))[:19]),
        ('marketing_team_id', 'not in', all_mkt_team_ids),
        ('contact_creator_crm_group_id', 'not in', all_mkt_group_ids),
        ('id', '>=', start),
    ],  limit=num_limit, order="id asc")
    tmp_string = ""
    count = 0
    n = len(all_crm_lead)
    for id in all_crm_lead:
        count += 1
        print(f"{count}-{n}")
        lead = c.model('crm.lead').browse(int(id))
        if len(lead.old_order_ids) <= 0:
            tmp_string += str(id)+"\n"
    if not tmp_string:
        tmp_string = "Không có số nào."
    total = tmp_string.count("\n")
    print(f"Tổng cơ hội tìm được: {total}")
    return tmp_string

def chay_so(c, arr_id):
    str_tmp = ""
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
                        'create_date': str(datetime.now()- timedelta(hours = 7))[:19],
                        'created_datetime': str(datetime.now()- timedelta(hours = 7))[:19],
                        'stage_id': 1,
                        'opportunity_type': 'optimal',
                        'is_inprogress': False,
                        'optimal_crm_lead_id': False
                    })
                    lead.is_inprogress = False
                    new_lead = c.model('crm.lead').create(val)
                    lead.optimal_crm_lead_id = new_lead.id
                    str_tmp += f"{str(lead.id)}          {new_lead.id}"
            except Exception as e:
                str_tmp += str(e)
    return str_tmp

def button_tim(lable, text, sever, data, user, password, limit, start):
    text.configure(state='normal')
    lable.configure(state='normal')
    text.delete("1.0","end")
    lable.delete("1.0","end")
    str_limit = limit.get()
    str_start = start.get()
    text.configure(state='disabled')
    lable.configure(state='disabled')
    num_limit = 100000
    num_start = 0
    try:
        num_limit = int(str_limit)
    except:
        num_limit = 100000
    try:
        num_start = int(str_start)
    except:
        num_start = 0
        
    c = conext_odoo(lable, text, sever, data, user, password)
    string_tim_so = tim_so(c, num_limit, num_start)
    limit.delete('0', "end")
    start.delete('0', "end")
    print_lable(limit, str(num_limit))
    print_lable(start, str(num_start))
    print_lable(text, string_tim_so)
    limit.configure(state='normal')
    start.configure(state='normal')

def button_chay(lable, text, sever, data, user, password):
    c = conext_odoo(lable, text, sever, data, user, password)
    all_text = text.get("1.0",'end-1c')
    list_lead = all_text.splitlines()
    tmp_string = chay_so(c, list_lead)
    print_lable(lable, tmp_string)

window = tk.Tk()
window.title("Chạy số tối ưu theo luồng")
window.geometry('700x700+0+0')

t = tk.Text(window, width=30, height=43)
  
t.place(x=2, y=2)
  
l = tk.Text(window, width=42, height=43)

l. config(bg="#ccffff")

l.place(x=350, y=2)


l.configure(state='disabled')
t.configure(state='disabled')

sever = tk.Entry(window, width=17,)
sever.insert(0, "https://dev.saleholding.com/")
sever.place(x=245,y=150)
data = tk.Entry(window, width=17)
data.insert(0, "dev")
data.place(x=245,y=180)
user = tk.Entry(window, width=17)
user.insert(0, "admin")
user.place(x=245,y=210)
password = tk.Entry(window, width=17)
password.insert(0, "Hebela@123")
password.place(x=245,y=240)
limit = tk.Entry(window, width=17)
limit.insert(0, "limit")
limit.place(x=245,y=400)
start = tk.Entry(window, width=17)
start.insert(0, "start")
start.place(x=245,y=450)

set_up_button = tk.Button(window, height=1, width=10, text="Tìm", 
                    command=partial(button_tim,l,t, sever, data, user, password, limit, start))
                
set_up_button.place(x=256,y=300)



set_up_button_run = tk.Button(window, height=1, width=10, text="Chạy", 
                    command=partial(button_chay,l,t, sever, data, user, password))
                
set_up_button_run.place(x=256,y=350)

window.mainloop()