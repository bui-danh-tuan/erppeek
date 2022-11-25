
import tkinter as tk
from tkinter import ttk
import erppeek
from functools import partial


def print_lable(lable, text):
    lable.configure(state='normal')
    lable.insert("end", text)
    lable.insert("end", "\n\n")
    lable.configure(state='disabled')


def conext_odoo(lable, text, sever, data, user, password, \
    limit, current_company, new_user, new_source, new_product, value_type):
    lable.delete(1.0,"end")
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
        return
    try:
        limit = limit.get() and int(limit.get()) or 0
        current_company = int(current_company.get())
        new_user = int(new_user.get())
        new_source = int(new_source.get())
        new_product = int(new_product.get())
        type = value_type == 'CRM' and 'crm.lead' or 'res.partner' 
        if not c.model('crm.group').search([('id', '=', current_company)]):
            print_lable(lable, "Không tìm thấy công ty!")
            return
        if not c.model('res.users').search([('id', '=', new_user)]):
            print_lable(lable, "Không tìm thấy người dùng!")
            return
        if not c.model('utm.source').search([('id', '=', new_source)]):
            print_lable(lable, "Không tìm thấy nguồn!")
            return
        if not c.model('product.category').search([('id', '=', new_product)]):
            print_lable(lable, "Không tìm thấy nhóm sản phẩm!")
            return
    except Exception as e:
        print_lable(lable, e)
        return
    if type == 'crm.lead':
        arr_search = [('contact_creator_crm_group_id', '=', current_company)]
    else:
        arr_search = [('crm_group_id', '=', current_company), ('res_partner_f99id', '!=', "Đang tạo")]
    if limit > 0:
        all_data = c.model(type).search(arr_search, limit=limit)
    else:
        all_data = c.model(type).search(arr_search)
    try:
        for a in all_data:
            model = c.model(type).browse(a)
            try:
                model.write({
                    'contact_creator_id': new_user,
                    'source_id': new_source,
                    'product_category_id': new_product
                    })
                print_lable(lable,f"chuyển đổi xong {value_type} - {a}")
                print(f"chuyển đổi xong {value_type} - {a}")
            except Exception as e:
                print_lable(lable,e)
    except Exception as e:
        print_lable(lable,e)
    
    



window = tk.Tk()
window.title("Text Widget Example")
window.geometry('773x700+0+0')
window.title("Chuyển data marketing")
t = tk.Text(window, width=30, height=43)
t.place(x=2, y=2)
l = tk.Text(window, width=42, height=43)
l. config(bg="#ccffff")
l.place(x=430, y=2)
sever = tk.Entry(window, width=30)
sever.insert(0, "https://dev.saleholding.com/")
sever.place(x=245, y=150)
data = tk.Entry(window, width=30)
data.insert(0, "dev")
data.place(x=245, y=180)
user = tk.Entry(window, width=30)
user.insert(0, "admin")
user.place(x=245, y=210)
password = tk.Entry(window, width=30)
password.insert(0, "Hebela@123")
password.place(x=245, y=240)

lable_current_company = tk.Label(window, height=1, text="Công ty cần đổi")
lable_current_company.place(x=246, y=350)
current_company = tk.Entry(window, width=27)
current_company.insert(0, "")
current_company.place(x=260, y=370)

lable_new_user = tk.Label(window, height=1, text="MKT mới")
lable_new_user.place(x=246, y=410)
new_user = tk.Entry(window, width=27)
new_user.insert(0, "")
new_user.place(x=260, y=430)

lable_new_source = tk.Label(window, height=1, text="Nguồn mới")
lable_new_source.place(x=246, y=450)
new_source = tk.Entry(window, width=27)
new_source.insert(0, "")
new_source.place(x=260, y=470)

lable_new_product = tk.Label(window, height=1, text="Nhóm sản phẩm mới")
lable_new_product.place(x=246, y=490)
new_product = tk.Entry(window, width=27)
new_product.insert(0, "")
new_product.place(x=260, y=510)

limit = tk.Entry(window, width=10)
limit.insert(0, "")
limit.place(x=300, y=80)

value_type = tk.StringVar()
type = ttk.Combobox(window, width = 7, 
                            textvariable = value_type)
type['values'] = (Partner, 'CRM')
type.current(0)
type.place(x=300, y=100)

set_up_button = tk.Button(window, height=1, width=10, text="Run",
                          command=partial(conext_odoo, l, t, sever, data, user, password,\
                            limit, current_company, new_user, new_source, new_product, value_type))
set_up_button.place(x=290, y=300)

window.mainloop()
