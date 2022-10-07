
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
            list_id.append(c.model('stock.picking').search([('name', '=', l)], limit=1)[0])
        except Exception as e: 
            print(lable, e)
    
    print(lable, list_id)

    if len(list_pick) == len(list_id):
        for id in list_id:
            try:
                pick = c.model('stock.picking').browse(id)
                origin = pick.origin.replace('Trả lại ', "")
                origin_pick = c.model('stock.picking').search([('name', '=', origin)])
                if len(origin_pick) != 1:
                    origin = pick.origin.replace('Return of ', "")
                    origin_pick = c.model('stock.picking').search([('name', '=', origin)])
                    if len(origin_pick) != 1:
                        print(lable,f"Sai số lượng phiếu nguồn: {origin_pick}")
                        continue
                if pick.state != 'cancel':
                    print(lable,f"Phiếu chưa bị hủy: {pick} - {pick.state}")
                    continue
                if pick.picking_description == 'out_return' or pick.picking_description == 'pick_return':
                    pick.unlink()
                    pick_return = c.model('stock.return.picking').create({
                        'picking_id': origin_pick[0]
                    })
                    pick_return.create_returns()
                    new_pick = c.model('stock.picking').search([('origin', 'ilike',  origin)], order='id DESC', limit=1)
                    stock_return = c.model('stock.immediate.transfer').create({
                        'pick_ids': [(4,new_pick[0])],
                        'immediate_transfer_line_ids':
                            [(0,0,{
                                'picking_id': new_pick[0],
                                'to_immediate': True
                            })]
                    })
                    stock_return.process()
                    c.model('stock.picking').browse(new_pick[0]).button_validate()
            except Exception as e:
                print(lable,e)
    if len(list_id) > 0:
        print(lable, "\n\n----------------Done----------------\n\n")

window = tk.Tk()
window.title("Text Widget Example")
window.geometry('773x700+0+0')                                                                                                
window.title("Hoàn hủy phiếu pick")
t = tk.Text(window, width=30, height=43)
t.place(x=2, y=2)
l = tk.Text(window, width=42, height=43)
l. config(bg="#ccffff")
l.place(x=430, y=2)
sever = tk.Entry(window, width=30)
sever.insert(0, "http://localhost:8069/")
sever.place(x=245,y=150)
data = tk.Entry(window, width=30)
data.insert(0, "Trading-DEV")
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