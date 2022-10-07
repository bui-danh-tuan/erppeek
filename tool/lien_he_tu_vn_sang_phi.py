
import tkinter as tk
from tkinter import ttk
import tkinter
import erppeek
from functools import partial


def print(lable, text):
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
        print(lable, e)

    lable.delete(1.0,"end")

    all_text = text.get("1.0",'end-1c')
    list_pick = all_text.splitlines()
    list_id = []
    for l in list_pick:
        try:
            p = c.model('res.partner').search([('phone', '=', l), ('country_type_id', '=', 1), ('was_closed', '=', False)])
            if len(p) == 1:
                list_id.append(p[0])
            else:
                print(lable, f"LỖI: liên hệ {l} có id nằm trong {p}")
        except Exception as e: 
            print(lable, e)
    
    print(lable, list_id)

    if len(list_pick) == len(list_id):
        for id in list_id:
            try:
                partner = c.model('res.partner').browse(id)
                partner.country_type_id = 6
                print(lable,f"Đổi VN -> PHIL: {partner.phone}")
            except Exception as e:
                print(lable,e)
    if len(list_id) > 0:
        print(lable, "\n\n----------------Done----------------\n\n")

window = tk.Tk()
window.title("Text Widget Example")
window.geometry('773x700+0+0')                                                                                                
window.title("Đổi liên hệ từ VN->PHIL")
t = tk.Text(window, width=30, height=43)
t.place(x=2, y=2)
l = tk.Text(window, width=42, height=43)
l. config(bg="#ccffff")
l.place(x=430, y=2)
sever = tk.Entry(window, width=30)
sever.insert(0, "https://dev.saleholding.com/")
sever.place(x=245,y=150)
data = tk.Entry(window, width=30)
data.insert(0, "dev")
data.place(x=245,y=180)
user = tk.Entry(window, width=30)
user.insert(0, "admin")
user.place(x=245,y=210)
password = tk.Entry(window, width=30)
password.insert(0, "Hebela@123")
password.place(x=245,y=240)
set_up_button = tk.Button(window, height=1, width=10, text="Run", 
                    command=partial(conext_odoo,l,t, sever, data, user, password))
set_up_button.place(x=256,y=300)
window.mainloop()