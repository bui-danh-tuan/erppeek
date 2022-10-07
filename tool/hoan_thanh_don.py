
import tkinter as tk
from tkinter import ttk
import tkinter
import erppeek
from functools import partial


def print_lable(lable, text):
    print(f"{text} \n\n")
    lable.configure(state='normal')
    lable.insert("end",text)
    lable.insert("end","\n\n")
    lable.configure(state='disabled')

def conext_odoo(lable,text, sever, data, user, password):

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
    except Exception as e: 
        print_lable(lable, e)

    lable.delete(1.0,"end")

    all_text = text.get("1.0",'end-1c')
    list_order = all_text.splitlines()
    list_id = []
    for l in list_order:
        try:
            list_id.append(c.model('sale.order').search([('name', '=', l)], limit=1)[0])
        except Exception as e: 
            print_lable(lable, e)
    
    print_lable(lable, list_id)

    if len(list_order) == len(list_id):
        for id in list_id:
            try:
                order = c.model('sale.order').browse(id)
                if order.summary_state != 'shipping':
                    print_lable(lable,f"LỖI: ĐƠN HÀNG {order.name} ĐANG Ở TRẠNG THÁI {order.summary_state} NÊN KHÔNG HOÀN THÀNH ĐƯỢC.")
                    continue
                try:
                    order.action_done_multi()
                    print_lable(lable,order.name)
                except Exception as e:
                    print_lable(lable,e)
                    all_lead = c.model('crm.lead').search([("is_inprogress", "=", True), ("partner_id", "=", order.opportunity_id.partner_id.id)])
                    for l in all_lead:
                        if l != order.opportunity_id.id:
                            lead = c.model('crm.lead').browse(l)
                            lead.unlink()
                    print_lable(lable, f"ORDER = {order.name} - {id}! Xóa các lead thành công.")
                    order.action_done_multi()
                    print_lable(lable, f"ORDER = {order.name} - {id}! Hoàn thành thành công.")
            except Exception as e:
                print_lable(lable,e)
    if len(list_id) > 0:
        print_lable(lable, "\n\n----------------Done----------------\n\n")
      
window = tk.Tk()
window.title("Text Widget Example")
window.geometry('700x700+0+0')

t = tk.Text(window, width=30, height=43)
  
t.place(x=2, y=2)
  
l = tk.Text(window, width=42, height=43)

l. config(bg="#ccffff")

l.place(x=350, y=2)

sever = tk.Entry(window, width=17,)
sever.insert(0, "https://saleholding.com/")
sever.place(x=245,y=150)
data = tk.Entry(window, width=17)
data.insert(0, "saleholding")
data.place(x=245,y=180)
user = tk.Entry(window, width=17)
user.insert(0, "")
user.place(x=245,y=210)
password = tk.Entry(window, width=17)
password.insert(0, "")
password.place(x=245,y=240)

set_up_button = tk.Button(window, height=1, width=10, text="Run", 
                    command=partial(conext_odoo,l,t, sever, data, user, password))
                
set_up_button.place(x=256,y=300)

window.mainloop()